import numpy as np
import pandas as pd
import math

class Plots():

    def sdf_to_df(self, filename):
        # Read sdf data into a pandas df
        sensitivities = {}
        with open(filename, 'r') as file:
            lines = file.readlines()

            # Read in the header data
            num_neutron_groups = int(lines[1].split()[0])
            num_sens_profiles = int(lines[2].split()[0])
            num_nuc_integrated = int(lines[2].split()[5])
            keff = float(lines[3].split()[0])
            keff_unc = float(lines[3].split()[2])

            # Collect the engergy boundaries
            lines_energy_bound = math.ceil((num_neutron_groups+1) / 5)
            energy_bounds = []
            bounds = ''.join(lines[5 : 5+lines_energy_bound]).split()
            # Loop through the lines of energy group numbers
            for i in range(num_neutron_groups):
                bound = '{}-{}'.format(bounds[i],bounds[i+1])
                energy_bounds.append(bound)

            # Number of lines each profile has of sensitivity values
            lines_values = math.ceil(num_neutron_groups/5)
            # Number of lines each sensitivity profile takes
            lines_profile = (2 * lines_values + 4)
            # Place the sensitivities into a dictionary of 2xn numpy arrays
            for i in range(num_sens_profiles):
                # Grab the title for the sensitivities
                line_start = lines_energy_bound + 5 + i * lines_profile
                nuclide = lines[line_start].split()[0]
                interaction = lines[line_start].split()[1]
                unit_num = lines[line_start+1].split()[0]
                region_num = lines[line_start+1].split()[1]

                # Place the sensitivities and uncertainties into the dictionary
                sens = ''.join(lines[line_start+4 : line_start+4+lines_values]).split()
                sensitivities[(nuclide, interaction, unit_num, region_num, 'sensitivity')] = np.array(sens, dtype=float)
                uncs = ''.join(lines[line_start+4+lines_values : line_start+lines_profile]).split()
                sensitivities[(nuclide, interaction, unit_num, region_num, 'uncertainty')] = np.array(uncs, dtype=float)

        df = pd.DataFrame(sensitivities, index=energy_bounds)
        df.index.name = 'energy bounds (ev)'
        df.columns.names = ['isotope', 'reaction', 'unit number', 'region number', '']
        return df




if __name__ == '__main__':
    plots = Plots()
    df = plots.sdf_to_df('KENO_slovenia_tsunami.sdf')
    print(df)
