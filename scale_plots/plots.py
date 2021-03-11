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

    def sdf_to_df(self, filename):
        '''Parse the keno sdf output file into
        a pandas DataFrame.

        Parameters
        ----------
        filename : str
            Name of the sdf file to parse
        
        Returns
        -------
        df : pandas.DataFrame
            DataFrame containing all of the data 
            needed for plotting from the sdf file.

        '''
        data = {}
        experiment = filename[:-4].split('/')[-1]
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
            lines_profile = (2 * lines_values + 4)
            # Place the sensitivities into a dictionary of 2xn numpy arrays
            for i in range(num_sens_profiles):
                # Grab the identifying keys for the sensitivities
                line_start = lines_energy_bound + 5 + i * lines_profile
                nuclide = lines[line_start].split()[0]
                interaction = lines[line_start].split()[1]
                unit_num = lines[line_start+1].split()[0]
                region_num = lines[line_start+1].split()[1]
                unit_region = '({},{})'.format(unit_num, region_num)

                # Grab the additional data available
                integral_value = float(lines[line_start+3].split()[0])
                integral_stdev = float(lines[line_start+3].split()[1])
                data[(experiment, nuclide, interaction, unit_region, 'integral')] = integral_value
                data[(experiment, nuclide, interaction, unit_region, 'integral std dev')] = integral_stdev

                # Place the sensitivities and standard deviations into the dictionary
                sens = ''.join(lines[line_start+4 : line_start+4+lines_values]).split()
                data[(experiment, nuclide, interaction, unit_region, 'sensitivity')] = np.array(sens, dtype=float)
                stdevs = ''.join(lines[line_start+4+lines_values : line_start+lines_profile]).split()
                data[(experiment, nuclide, interaction, unit_region, 'std dev')] = np.array(stdevs, dtype=float)

        # Create or append the dataframe indexed by energy groups
        if self.df is None:
            self.df = pd.DataFrame(data, index=energy_bounds)
            # Name the idices and columns
            self.df.index.name = 'energy bounds (ev)'
            self.df.columns.names = ['experiment', 'isotope', 'reaction', '(unit, region)', '']
        else:
            # Concatenate current DataFrame with new DataFrame
            new_df = pd.DataFrame(data, index=energy_bounds)
            self.df = pd.concat([self.df, new_df], axis=1)
        return self.df

    def get_corr(self, keys, elow=float('-inf'), ehigh=float('inf'), lethargy=False):
        '''Return the correlation coefficients for the given keys

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
                if lethargy is False:
                    sens_x = sens_x/lethargies
                    sens_y = sens_y/lethargies
                
                r[(tuple(keys[i]),tuple(keys[j]))] = pearsonr(sens_x, sens_y)[0]
        return r

    def sensitivity_plot(self, keys, elow=float('-inf'), ehigh=float('inf'), plot_std_dev=True,
                         plot_corr=False, legend_dict=None, r_pos='bottom right'):
        '''Plot the sensitivites for the given isotopes, reactions,
        unit numbers, and region numbers. Creates a matplotlib.pyplot
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
        plot_std_dev : bool, optional
            Whether the user wants the error bars to be included
            in the generated plot. Defaults to True.
        plot_corr : bool, optional
            Whether the user wants the correlation coefficient to
            be given in the plot. Defaults to False.
        legend_dict : dictionary, optional
            keys : key in the keys list of the selected isotope
            value : string to replace the automatically generated legend
        r_pos : str, optional
            Where the correlation coefficient should go on the plot.
            Defaults to 'bottom right'. Can also be 'top right',
            'bottom left', and 'top left'.

        '''
        ylabel = 'Sensitivity'
        plot_lethargy = False

        # Send the data to the plot making function
        self.__make_plot(keys, elow, ehigh, plot_std_dev, plot_corr, plot_lethargy, legend_dict, r_pos, ylabel)

    def sensitivity_lethargy_plot(self, keys, elow=float('-inf'), ehigh=float('inf'), plot_std_dev=True,
                                  plot_corr=False, legend_dict=None, r_pos='bottom right'):
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
        plot_std_dev : bool, optional
            Whether the user wants the error bars to be included
            in the generated plot. Defaults to True.
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
        plot_lethargy = True

        # Send the data to the plot making function
        self.__make_plot(keys, elow, ehigh, plot_std_dev, plot_corr, plot_lethargy, legend_dict, r_pos, ylabel)

    def __make_plot(self, keys, elow, ehigh, plot_std_dev, plot_corr, plot_lethargy, legend_dict, r_pos, ylabel):
        '''The parts of making a plot that are repeated.'''
        # Make sure keys is a list of lists
        if type(keys[0]) is not list:
            keys = [keys]
        # Create the text for the correlation
        r_text = ''
        # The energy bounds information
        indices, energy_vals, lethargies = self.__get_energy_bounds(elow, ehigh)
        if plot_corr:
            # Get the correlation coefficients
            r_dict = self.get_corr(keys, elow=elow, ehigh=ehigh, lethargy=plot_lethargy)
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
                    r_text += '\n{} and {} r = {}'.format(key_text1, key_text2, r)
        i = 0
        colors = ['g', 'r', 'c', 'm', 'k', 'y']
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

            # Calculate the sensitivities per lethargy if passed in
            if plot_lethargy:
                sens = sens/lethargies
                stdevs = stdevs/lethargies

            # Make each sensitivity appear twice for step feature
            sens_step = []
            for sen in sens:
                sens_step.append(sen)
                sens_step.append(sen)

            # Plot the sensitivity and increment color variable
            plt.plot(energy_vals, sens_step, linestyle='-', color=colors[i], linewidth=1)
            # If standard deviation is desired then plot the bars
            if plot_std_dev:
                plotline, caps, eb = plt.errorbar(energy_vals[1::2], sens, yerr=stdevs, fmt='none', ecolor='b', elinewidth=1, capsize=2, capthick=1)
                eb[0].set_linestyle(':')

            # Add the integral value information
            integral_value = self.df[key[0]][key[1]][key[2]][key[3]]['integral'][0]
            integral_stdev = self.df[key[0]][key[1]][key[2]][key[3]]['integral std dev'][0]
            legend_title += '\nIntegral Value = {} +/- {}'.format(integral_value, integral_stdev)
            legends.append(legend_title)

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
        plt.legend(legends)
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

    def __get_integral(self, key):
        '''Doesn't work'''
        # Collect the dx values
        dxs = np.array([], dtype=float)
        lethargies = np.array([], dtype=float)
        for bound in self.df.index:
            # Add the high and low bounds to energy bounds
            ehigh = float(bound.split(':')[0])
            elow = float(bound.split(':')[1])
            dxs = np.append(dxs, ehigh - elow)

            # Calculate the lethargies for each energy grouping
            lethargies = np.append(lethargies, log(ehigh/elow))

        # Collect the sensitivites and uncertainties
        sens = np.array(self.df[key[0]][key[1]][key[2]][key[3]]['sensitivity'], dtype=float)
        stdevs = np.array(self.df[key[0]][key[1]][key[2]][key[3]]['std dev'], dtype=float)

        value = np.sum(sens/lethargies)
        stdev = np.sum(stdevs/lethargies)

        return value, stdev
