import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt

class Plots():

    def sdf_to_df(self, filename):
        '''Parse the keno sdf output file into
        a pandas df
        '''
        sensitivities = {}
        self.extra_data = {}
        with open(filename, 'r') as file:
            lines = file.readlines()

            # Read in the header data
            num_neutron_groups = int(lines[1].split()[0])
            num_sens_profiles = int(lines[2].split()[0])
            num_nuc_integrated = int(lines[2].split()[5])
            self.extra_data['keff'] = {}
            self.extra_data['keff']['value'] = float(lines[3].split()[0])
            self.extra_data['keff']['stdev'] = float(lines[3].split()[2])

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
                self.extra_data[(nuclide, interaction, unit_region, 'integral_value')] = integral_value
                self.extra_data[(nuclide, interaction, unit_region, 'integral_stdev')] = integral_stdev

                # Place the sensitivities and standard deviations into the dictionary
                sens = ''.join(lines[line_start+4 : line_start+4+lines_values]).split()
                sensitivities[(nuclide, interaction, unit_region, 'sensitivity')] = np.array(sens, dtype=float)
                stdevs = ''.join(lines[line_start+4+lines_values : line_start+lines_profile]).split()
                sensitivities[(nuclide, interaction, unit_region, 'std dev')] = np.array(stdevs, dtype=float)

        # Create the dataframe indexed by energy groups
        self.df = pd.DataFrame(sensitivities, index=energy_bounds)
        # Name the idices and columns
        self.df.index.name = 'energy bounds (ev)'
        self.df.columns.names = ['isotope', 'reaction', '(unit, region)', '']
        return self.df

    def sensitivity_plot(self, keys, plot_std_dev=True):
        '''Plot the sensitivites for the given isotopes, reactions,
        unit numbers, and region numbers. Creates a matplotlib.pyplot
        step plot for the energy bounds from the DataFrame.
        '''
        # Collect the energy bounds (x-axis)
        energy_bounds = []
        for bound in self.df.index:
            energy_bounds.append(float(bound.split(':')[0]))
            energy_bounds.append(float(bound.split(':')[1]))

        i = 0
        colors = ['g', 'r', 'c', 'm', 'k', 'y']
        legends = []
        for key in keys:
            # Collect the sensitvities and standard deviations
            sens = self.df[key[0]][key[1]][key[2]]['sensitivity']
            stdevs = self.df[key[0]][key[1]][key[2]]['std dev']

            # Make each sensitivity appear twice for step feature
            sens_step = []
            for sen in sens:
                sens_step.append(sen)
                sens_step.append(sen)

            # Plot the sensitivity and increment color variable
            plt.plot(energy_bounds, sens_step, linestyle='-', color=colors[i])
            # Save the legend title
            # This will be less ugly when I add these to the df
            integral_value = self.extra_data[tuple((' '.join(key)+' integral_value').split())]
            integral_stdev = self.extra_data[tuple((' '.join(key)+' integral_stdev').split())]
            legend_title = '{}\nIntegral Value = {} +/- {}'.format(key[0], integral_value, integral_stdev)
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
        plt.ylabel('Sensitivity')
        plt.title('tbd')
        plt.grid()
        plt.show()
    
    def sensitivity_lethargy_plot(self, keys, plot_std_dev=True):
        '''Plot the sensitivites for the given isotopes, reactions,
        unit numbers, and region numbers. Creates a matplotlib.pyplot
        step plot for the energy bounds from the DataFrame.
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
            lethargies = np.append(lethargies, math.log(ehigh/elow, 10))


        i = 0
        colors = ['g', 'r', 'c', 'm', 'k', 'y']
        legends = []
        for key in keys:
            # Collect the sensitvities and standard deviations
            sens = np.array(self.df[key[0]][key[1]][key[2]]['sensitivity'], dtype=float)
            stdevs = np.array(self.df[key[0]][key[1]][key[2]]['std dev'], dtype=float)

            # Calculate the sensitivities per lethargy
            sens = sens/lethargies
            stdevs = stdevs/lethargies

            # Make each sensitivity appear twice for step feature
            sens_step = []
            for sen in sens:
                sens_step.append(sen)
                sens_step.append(sen)

            # Plot the sensitivity and increment color variable
            plt.plot(energy_bounds, sens_step, linestyle='-', color=colors[i])
            # Save the legend title
            # This will be less ugly when I add these to the df
            integral_value = self.extra_data[tuple((' '.join(key)+' integral_value').split())]
            integral_stdev = self.extra_data[tuple((' '.join(key)+' integral_stdev').split())]
            legend_title = '{}\nIntegral Value = {} +/- {}'.format(key[0], integral_value, integral_stdev)
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
        plt.ylabel('Sensitivity')
        plt.title('tbd')
        plt.grid()
        plt.show()


if __name__ == '__main__':
    plots = Plots()
    plots.sdf_to_df('KENO_slovenia_tsunami.sdf')
    keys = [('h-1', 'total', '(0,0)'),('h-1', 'elastic', '(0,0)'),('h-1', 'capture', '(0,0)')]
    plots.sensitivity_lethargy_plot(keys)
