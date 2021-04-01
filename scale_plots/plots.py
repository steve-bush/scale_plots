import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import ceil, log
from scipy.stats import pearsonr

class Plots():
    '''Object that contains the functions needed
    to parse and plot the data from a sdf file.
    '''

    def __init__(self):
        self.df = None
        self.sig_figs = 4

    def sdf_to_df(self, filename):
        '''Parse the keno sdf output file into
        a pandas DataFrame.

        Parameters
        ----------
        filename : str
            Name of the sdf file to parse.
        
        Returns
        -------
        df : pandas.DataFrame
            DataFrame containing all of the data 
            needed for plotting from the sdf file.

        '''
        data = {}
        experiment = filename[:-4].split('/')[-1]
        type_a = False
        type_b = False
        with open(filename, 'r') as file:
            lines = file.readlines()

            # Read in the header data
            num_neutron_groups = int(lines[1].split()[0])
            num_sens_profiles = int(lines[2].split()[0])
            #num_nuc_integrated = int(lines[2].split()[5])
            #data[(experiment, 'keff', 'value')] = float(lines[3].split()[0])
            #data[(experiment, 'keff', 'std dev')] = float(lines[3].split()[2])

            # Collect the engergy boundaries
            lines_energy_bound = ceil((num_neutron_groups+1) / 5)
            energy_bounds = []
            bounds = ''.join(lines[5 : 5+lines_energy_bound]).split()
            # Loop through the lines of energy group numbers
            for i in range(num_neutron_groups):
                bound = '{}:{}'.format(bounds[i],bounds[i+1])
                energy_bounds.append(bound)

            # Number of lines each profile has of sensitivity values
            lines_values = ceil(num_neutron_groups/5)
            # Number of lines each sensitivity profile takes
            if len(lines[lines_energy_bound + 5].split()) == 6:
                # Type A
                lines_profile = lines_values + 2
                type_a = True
            elif len(lines[lines_energy_bound + 5].split()) == 4:
                # Type B
                lines_profile = 2 * lines_values + 4
                type_b = True
            # Place the sensitivities into a dictionary of 2xn numpy arrays
            for i in range(num_sens_profiles):
                # Grab the identifying keys for the sensitivities
                key_start = lines_energy_bound + 5 + i * lines_profile
                nuclide = lines[key_start].split()[0]
                interaction = lines[key_start].split()[1]
                # Check if the file is type A or type B
                if type_a:
                    #  Type A
                    unit_region = lines[key_start].split()[4]

                    # Setup the sensitivity data
                    sens_start = key_start+2
                    stdevs = np.nan
                elif type_b:
                    # Type B
                    unit_num = lines[key_start+1].split()[0]
                    region_num = lines[key_start+1].split()[1]
                    unit_region = '({},{})'.format(unit_num, region_num)

                    # Type A has no stdev so grab it here
                    sens_start = key_start+4
                    stdevs = ''.join(lines[sens_start+lines_values : key_start+lines_profile]).split()
                # Place the sensitivities into the dictionary
                sens = ''.join(lines[sens_start : sens_start+lines_values]).split()
                data[(experiment, nuclide, interaction, unit_region, 'sensitivity')] = np.array(sens, dtype=float)
                data[(experiment, nuclide, interaction, unit_region, 'std dev')] = np.array(stdevs, dtype=float)

        # Create or append the dataframe indexed by energy groups
        if self.df is None:
            self.df = pd.DataFrame(data, index=energy_bounds)
            # Name the idices and columns
            self.df.index.name = 'energy bounds (ev)'
            if type_a:
                self.df.columns.names = ['experiment', 'isotope', 'reaction', '(unit, region)', '']
            elif type_b:
                self.df.columns.names = ['experiment', 'isotope', 'reaction', 'region', '']
        else:
            # Concatenate current DataFrame with new DataFrame
            new_df = pd.DataFrame(data, index=energy_bounds)
            self.df = pd.concat([self.df, new_df], axis=1)
        return self.df

    def get_integral(self, key):
        '''Returns the integral value of the
        sensitivity data and the uncertainty.

        Parameters
        ----------
        key : list
            Indices in the pandas DataFrame where the desired
            sensitivities are stored.

        Returns
        -------
        int_value : float
            Integral value of the sensitivity data.
        int_unc : float
            Uncertainty of the integral value.
        '''
        # Collect the sensitivites and uncertainties
        sens = np.array(self.df[key[0]][key[1]][key[2]][key[3]]['sensitivity'], dtype=float)
        stdevs = np.array(self.df[key[0]][key[1]][key[2]][key[3]]['std dev'], dtype=float)
        # Calculate the integral
        int_value = np.sum(sens)
        # Calculate the uncertainty (root sum square)
        int_unc = np.sqrt(np.sum(np.square(stdevs)))

        return int_value, int_unc

    def get_corr(self, keys, elow=float('-inf'), ehigh=float('inf'), lethargy=False):
        '''Return the correlation coefficients for the given keys.

        Parameters
        ----------
        keys : list of lists
            Indices in the pandas DataFrame where the desired
            data is stored.
        elow : float, optional
            The low bound for energies to calculate correlation.
            Defaults to -inf.
        ehigh : float, optional
            The high bound for energies to calculate correlation.
            Defaults to inf.
        lethargy : bool, optional
            Whether to find the correlation between sensitivites
            in unit lethargy. Defaults to False.

        Returns
        -------
        r : dict
            key : tuple of tuples for keys
            value : correlation coefficient for the 2 reactions in the key

        '''
        # Get the energy bound indices and lethargies
        indices, _, lethargies = self.__get_energy_bounds(elow, ehigh)
        assert len(indices) > 1, 'Must have at least 2 data points to calculate correlation coefficient'
        # Calculate the pearson correlation coefficient
        r = {}
        for i in range(len(keys)-1):
            for j in range(i+1, len(keys)):
                # Compare each data set
                sens_x = np.array(self.df[keys[i][0]][keys[i][1]][keys[i][2]][keys[i][3]]['sensitivity'].loc[indices], dtype=float)
                sens_y = np.array(self.df[keys[j][0]][keys[j][1]][keys[j][2]][keys[j][3]]['sensitivity'].loc[indices], dtype=float)
                sens_x = sens_x/lethargies
                sens_y = sens_y/lethargies
                
                r[(tuple(keys[i]),tuple(keys[j]))] = pearsonr(sens_x, sens_y)[0]
        return r

    def sensitivity_lethargy_plot(self, keys, elow=float('-inf'), ehigh=float('inf'), plot_err_bar=True,
                                  plot_fill_bet=False, plot_corr=False, legend_dict=None, r_pos='bottom right'):
        '''Plot the sensitivites per unit lethargy for the given isotopes,
        reactions, unit numbers, and region numbers. Creates a matplotlib.pyplot
        step plot for the energy bounds from the DataFrame.

        Parameters
        ----------
        keys : list of lists
            Indices in the pandas DataFrame where the desired
            sensitivities are stored.
        elow : float, optional
            The low bound for energies to plot.
            Defaults to -inf.
        ehigh : float, optional
            The high bound for energies to plot.
            Defaults to inf.
        plot_err_bar : bool, optional
            Whether the user wants the error bars to be included
            in the generated plot. Defaults to True.
        plot_fill_bet : bool, optional
            Whether the user wants the error to be plotted as a
            fill between. Defaults to False.
        plot_corr : bool, optional
            Whether the user wants the correlation coefficient to
            be given in the plot. Defaults to False
        legend_dict : dictionary, optional
            keys : key in the keys list of the selected isotope
            value : string to replace the automatically generated legend
        r_pos : str, optional
            Where the correlation coefficient should go on the plot.
            Defaults to 'bottom right'. Can also be 'top right',
            'bottom left', and 'top left'.

        '''
        ylabel = 'Sensitivity per unit lethargy'

        # Make sure keys is a list of lists
        if type(keys[0]) is not list:
            keys = [keys]
        # Assert maximum number of keys to plot
        assert len(keys) < 24, 'Maximum number of keys to plot is 24'
        # Create the text for the correlation
        r_text = ''
        # The energy bounds information
        indices, energy_vals, lethargies = self.__get_energy_bounds(elow, ehigh)
        if plot_corr:
            r_text += 'Correlations:'
            # Get the correlation coefficients
            r_dict = self.get_corr(keys, elow=elow, ehigh=ehigh)
            # Put the correlation coefficients into a string
            for i in range(len(keys)-1):
                for j in range(i+1, len(keys)):
                    # Make the coefficient title look nice
                    if legend_dict is None:
                        key_text1 = ' '.join(tuple(keys[i]))
                        key_text2 = ' '.join(tuple(keys[j]))
                    else:
                        key_text1 = legend_dict[tuple(keys[i])]
                        key_text2 = legend_dict[tuple(keys[j])]
                    # Get the correlation coefficients
                    r = r_dict[(tuple(keys[i]),tuple(keys[j]))]
                    r_text += '\n{} and {} r = {:.4}'.format(key_text1, key_text2, r)
        i = 0
        colors = ['g', 'r', 'c', 'm', 'k', 'y']
        ls = ['-', '--', '.-', '.']
        legends = []
        for key in keys:
            # Create the legend title
            if legend_dict is None:
                # If no legend was passed in create one
                legend_title = ' '.join(tuple(key))
            else:
                # If legend titles were passed in then use them
                legend_title = legend_dict[tuple(key)]
            
            # Raise an error if passed in keys are not 4
            assert len(key) == 4, 'Must pass 4 identifiers in each key'

            # Collect the sensitvities and standard deviations
            sens = np.array(self.df[key[0]][key[1]][key[2]][key[3]]['sensitivity'].loc[indices], dtype=float)
            stdevs = np.array(self.df[key[0]][key[1]][key[2]][key[3]]['std dev'].loc[indices], dtype=float)

            # Calculate the sensitivities per lethargy
            sens = sens/lethargies
            stdevs = stdevs/lethargies

            # Make each sensitivity std dev appear twice for step feature
            sens_step = np.array([], dtype=float)
            stdev_step = np.array([], dtype=float)
            for j in range(len(sens)):
                sens_step = np.append(sens_step, [sens[j], sens[j]])
                stdev_step = np.append(stdev_step, [stdevs[j], stdevs[j]])

            # Plot the sensitivity
            if not plot_fill_bet:
                plt.plot(energy_vals, sens_step, ls=ls[i//6], color=colors[i%6], linewidth=1)
            else:
                plt.plot(energy_vals, sens_step, ls=ls[i//6], color=colors[i%6], linewidth=1, alpha=0.2)

            # If standard deviations exist
            if not np.isnan(stdevs).all():
                if plot_err_bar:
                    assert plot_fill_bet is False, 'plot_err_bar and plot_fill_bet cannot both be True' 
                    # Plot the error bars
                    mid_vals = np.power(10, (np.log10(energy_vals[::2]) + np.log10(energy_vals[1::2]))/2)
                    plotline, caps, eb = plt.errorbar(mid_vals, sens, yerr=stdevs, fmt='none', ecolor=colors[i%6], elinewidth=1, capsize=2, capthick=1)
                    eb[0].set_linestyle(':')
                elif plot_fill_bet:
                    # Plot the std dev as a fill between
                    plt.fill_between(energy_vals, sens_step-stdev_step, sens_step+stdev_step, ls=ls[i//6], color=colors[i%6], alpha=0.2)              

            # Add the integral value information
            int_value, int_unc = self.get_integral(key)
            if np.isnan(stdevs).all():
                # If there is no integral std dev
                legend_title += '\nIntegral Value = {:.4}'.format(int_value)
            else:
                # If there is an integral std dev
                legend_title += '\nIntegral Value = {:.4} \u00B1 {:.4}'.format(int_value, int_unc)

            legends.append(legend_title)

            # Increment color variable
            i += 1
        # Put the correlation coefficients on the plot
        ax = plt.gca()
        if r_pos.lower() == 'top right':
            ax.text(0.01, 1, r_text, horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
        elif r_pos.lower() == 'top left':
            ax.text(1, 1, r_text, horizontalalignment='right', verticalalignment='top', transform=ax.transAxes)
        elif r_pos.lower() == 'bottom left':
            ax.text(1, 0, r_text, horizontalalignment='right', verticalalignment='bottom', transform=ax.transAxes)
        else:
            ax.text(0.01, 0, r_text, horizontalalignment='left', verticalalignment='bottom', transform=ax.transAxes)

        # Final plot settings
        legend = plt.legend(legends)
        # Make the legend markers opaque
        for l in legend.legendHandles:
            l.set_alpha(1)
        plt.xscale('log')
        plt.xlabel('Energy (eV)')
        plt.ylabel(ylabel)
        plt.title('title')
        plt.grid(b=True)
        plt.show()

    def __get_energy_bounds(self, elow, ehigh):
        # Collect the energy bounds (x-axis)
        indices = []
        energy_vals = np.array([], dtype=float)
        lethargies = np.array([], dtype=float)
        for bound in self.df.index:
            # Add the high and low bounds to energy bounds
            e_upper = float(bound.split(':')[0])
            e_lower = float(bound.split(':')[1])
            # Only add in energy values within given elow and ehigh
            if e_upper <= ehigh and e_lower >= elow:
                indices.append(bound)
                energy_vals = np.append(energy_vals, [e_upper, e_lower])
                # Calculate the lethargies for each energy grouping
                lethargies = np.append(lethargies, log(e_upper/e_lower))
        return indices, energy_vals, lethargies
