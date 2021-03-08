import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt

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
            lines_energy_bound = math.ceil((num_neutron_groups+1) / 5)
            energy_bounds = []
            bounds = ''.join(lines[5 : 5+lines_energy_bound]).split()
            # Loop through the lines of energy group numbers
            for i in range(num_neutron_groups):
                bound = '{}:{}'.format(bounds[i],bounds[i+1])
                energy_bounds.append(bound)

            # Number of lines each profile has of sensitivity values
            lines_values = math.ceil(num_neutron_groups/5)
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

    def get_integral(self, key):
        # Collect the dx values
        dxs = np.array([], dtype=float)
        lethargies = np.array([], dtype=float)
        for bound in self.df.index:
            # Add the high and low bounds to energy bounds
            ehigh = float(bound.split(':')[0])
            elow = float(bound.split(':')[1])
            dxs = np.append(dxs, ehigh - elow)

            # Calculate the lethargies for each energy grouping
            lethargies = np.append(lethargies, math.log(ehigh/elow))

        # Collect the sensitivites and uncertainties
        sens = np.array(self.df[key[0]][key[1]][key[2]][key[3]]['sensitivity'], dtype=float)
        stdevs = np.array(self.df[key[0]][key[1]][key[2]][key[3]]['std dev'], dtype=float)

        value = np.sum(sens*dxs)
        stdev = np.sum(stdevs*dxs)

        return value, stdev

    def sensitivity_plot(self, keys, plot_std_dev=True, legend_dict=None):
        '''Plot the sensitivites for the given isotopes, reactions,
        unit numbers, and region numbers. Creates a matplotlib.pyplot
        step plot for the energy bounds from the DataFrame.

        Default unit and region number are (0,0).

        Parameters
        ----------
        keys : list of lists
            Indices in the pandas DataFrame where the desired
            sensitivities are stored.
        plot_std_dev : bool, optional
            Whether the user wants the error bars to be included
            in the generated plot. Defaults to True.
        legend_dict : dictionary, optional
            keys : key in the keys list of the selected isotope
            value : string to replace the automatically generated legend

        '''
        # Collect the energy bounds (x-axis)
        energy_bounds = np.array([], dtype=float)
        for bound in self.df.index:
            # Add the high and low bounds to energy bounds
            ehigh = float(bound.split(':')[0])
            elow = float(bound.split(':')[1])
            energy_bounds = np.append(energy_bounds, [ehigh, elow])

        ylabel = 'Sensitivity'
        lethargies = None

        # Send the data to the plot making function
        self.__make_plot(keys, energy_bounds, ylabel, plot_std_dev, legend_dict, lethargies)

    def sensitivity_lethargy_plot(self, keys, plot_std_dev=True, legend_dict=None):
        '''Plot the sensitivites per unit lethargy for the given isotopes,
        reactions, unit numbers, and region numbers. Creates a matplotlib.pyplot
        step plot for the energy bounds from the DataFrame.

        Default unit and region number are (0,0).

        Parameters
        ----------
        keys : list of lists
            Indices in the pandas DataFrame where the desired
            sensitivities are stored.
        plot_std_dev : bool, optional
            Whether the user wants the error bars to be included
            in the generated plot. Defaults to True.
        legend_dict : dictionary, optional
            keys : key in the keys list of the selected isotope
            value : string to replace the automatically generated legend

        '''
        # Collect the energy bounds (x-axis)
        energy_bounds = np.array([], dtype=float)
        lethargies = np.array([], dtype=float)
        for bound in self.df.index:
            # Add the high and low bounds to energy bounds
            ehigh = float(bound.split(':')[0])
            elow = float(bound.split(':')[1])
            energy_bounds = np.append(energy_bounds, [ehigh, elow])

            # Calculate the lethargies for each energy grouping
            lethargies = np.append(lethargies, math.log(ehigh/elow))

        ylabel = 'Sensitivity per unit lethargy'

        # Send the data to the plot making function
        self.__make_plot(keys, energy_bounds, ylabel, plot_std_dev, legend_dict, lethargies)

    def __make_plot(self, keys, energy_bounds, ylabel, plot_std_dev, legend_dict, lethargies):
        '''The parts of making a plot that are repeated.'''
        # Make sure keys is a list of lists
        if type(keys[0]) is not list:
            keys = [keys]
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

            # Add unit and region numbers of 0 if none given
            if len(key) == 3:
                key.append('(0,0)')
            
            # Raise an error if less than 3 values were passed in
            assert len(key) > 3, 'Must pass 3 or more identifiers in each key'

            # Collect the sensitvities and standard deviations
            sens = np.array(self.df[key[0]][key[1]][key[2]][key[3]]['sensitivity'], dtype=float)
            stdevs = np.array(self.df[key[0]][key[1]][key[2]][key[3]]['std dev'], dtype=float)

            # Calculate the sensitivities per lethargy if passed in
            if lethargies is not None:
                sens = sens/lethargies
                stdevs = stdevs/lethargies

            # Make each sensitivity appear twice for step feature
            sens_step = []
            for sen in sens:
                sens_step.append(sen)
                sens_step.append(sen)

            # Plot the sensitivity and increment color variable
            plt.plot(energy_bounds, sens_step, linestyle='-', color=colors[i], linewidth=1)

            # Add the integral value information
            integral_value = self.df[key[0]][key[1]][key[2]][key[3]]['integral'][0]
            integral_stdev = self.df[key[0]][key[1]][key[2]][key[3]]['integral std dev'][0]
            legend_title += '\nIntegral Value = {} +/- {}'.format(integral_value, integral_stdev)
            legends.append(legend_title)

            i += 1
            # If standard deviation is desired then plot the bars
            if plot_std_dev:
                plotline, caps, eb = plt.errorbar(energy_bounds[1::2], sens, yerr=stdevs, fmt='none', ecolor='b', elinewidth=1, capsize=2, capthick=1)
                eb[0].set_linestyle(':')
        # Final plot settings
        plt.legend(legends)
        plt.xscale('log')
        plt.xlabel('Energy (eV)')
        plt.ylabel(ylabel)
        plt.title('title')
        plt.grid(b=True)
        plt.show()
