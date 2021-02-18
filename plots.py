import numpy as np
import pandas as pd
import math

class Plots():

    def sdf_to_dict(self, filename):
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
            energy_bounds = np.array([])
            # Loop through the lines of energy group numbers
            for line in lines[5:lines_energy_bound+5]:
                energy_bounds = np.append(energy_bounds, line.split())
            # Convert the array of strings to floats
            energy_bounds = np.asarray(energy_bounds, float)

            # Variables for parsing sensitivities and uncertainties
            count = 0
            # Number of lines each profile has of sensitivity values
            lines_values = math.ceil(num_neutron_groups/5)
            # Number of lines each sensitivity profile takes
            lines_profile = (2 * lines_values + 4)
            sensitivities = {}
            nuclides = []

            # Place the sensitivities into a dictionary of 2xn numpy arrays
            for i in range(num_sens_profiles):
                # Grab the title for the sensitivities
                line_start = lines_energy_bound + 5 + i * lines_profile
                nuclide = lines[line_start].split()[0]
                interaction = lines[line_start].split()[1]
                tbd = lines[line_start+1].split()[0]

                # Create new dictionary for nuclide if needed
                if nuclide not in nuclides:
                    nuclides.append(nuclide)
                    sensitivities[nuclide] = {}
                sensitivities[nuclide][interaction] = {}

                # Place the sensitivities and uncertainties into the dictionary
                sens = ''.join(lines[line_start+4 : line_start+4+lines_values]).split()
                sensitivities[nuclide][interaction]['sensitivity'] = np.array(sens, dtype=float)
                uncs = ''.join(lines[line_start+4+lines_values : line_start+lines_profile]).split()
                sensitivities[nuclide][interaction]['uncertainty'] = np.array(uncs, dtype=float)
            
            return sensitivities


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
            energy_bounds = np.array([])
            # Loop through the lines of energy group numbers
            for line in lines[5:lines_energy_bound+5]:
                energy_bounds = np.append(energy_bounds, line.split())
            # Convert the array of strings to floats
            energy_bounds = np.asarray(energy_bounds, float)

            # Variables for parsing sensitivities and uncertainties
            count = 0
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
                tbd = lines[line_start+1].split()[0]

                # Place the sensitivities and uncertainties into the dictionary
                sens = ''.join(lines[line_start+4 : line_start+4+lines_values]).split()
                sensitivities[(nuclide, interaction, tbd, 'sensitivity')] = np.array(sens, dtype=float)
                uncs = ''.join(lines[line_start+4+lines_values : line_start+lines_profile]).split()
                sensitivities[(nuclide, interaction, tbd, 'uncertainty')] = np.array(uncs, dtype=float)

        return pd.DataFrame(sensitivities)




if __name__ == '__main__':
    plots = Plots()
    plots.sdf_to_df('KENO_slovenia_tsunami.sdf')