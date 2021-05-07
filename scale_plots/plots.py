import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import ceil, log
from scipy.stats import pearsonr
from struct import unpack

import scale_plots
from .scale_ids import mt_ids, elements, specials

class Plots():
    '''Object that contains the functions needed 
    to parse and plot the data from a sdf file.
    '''

    def __init__(self):
        self.df = None
        self.cov_matrices = {}
        self.cov_groups = {}
        self.mat_xs = {}

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
        # Check for an sdf file
        if filename[-4:] != '.sdf':
            print("File must be a '.sdf' file.")
            return
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
                elif type_b:
                    # Type B
                    unit_num = lines[key_start+1].split()[0]
                    region_num = lines[key_start+1].split()[1]
                    unit_region = '({},{})'.format(unit_num, region_num)

                    # Type A has no stdev so grab it here
                    sens_start = key_start+4
                    stdevs = ''.join(lines[sens_start+lines_values : key_start+lines_profile]).split()
                    data[(experiment, nuclide, interaction, unit_region, 'std dev')] = np.array(stdevs, dtype=float)
                # Place the sensitivities into the dictionary
                sens = ''.join(lines[sens_start : sens_start+lines_values]).split()
                data[(experiment, nuclide, interaction, unit_region, 'sensitivity')] = np.array(sens, dtype=float)

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

    def parse_coverx(self, filename):
        '''Parse the covariance matrix file. Save the 
        matrices into a dictionary as well as the 
        energy groups. 
        An exlanation of the file format is located in 
        the parse_coverx jupyter notebook.

        Parameters
        ----------
        filename : str
            Name of the covariance file to parse.

        '''
        fname = filename.split('/')[-1]
        # Check for the file not being a covariance file
        if fname[0:6] != 'scale.' and 'groupcov' not in fname:
            print('File must be a scale covariance file.')
            return
        # Read in and save the full binary file
        with open(filename, 'rb') as file:
            full_file = file.read()

        # Read the file identification length in bytes to skip
        # Find out if the file is big or little endian
        # Scale decided to switch that for some of their libraries
        file_id_len = unpack('>i', full_file[0:4])[0]
        # If the length is massive its little-endian
        if file_id_len > 1000:
            sym = '<'
            file_id_len = unpack('<i', full_file[0:4])[0]
        else:
            sym = '>'

        # Start is file id length + 3 integers for sections length
        file_cont_st = file_id_len + 12
        # File control should always be 28 bytes
        file_cont_end = file_cont_st + 28
        # Read in file control values and store important ones
        file_cont = unpack(sym+'iiiiiii', full_file[file_cont_st: file_cont_end])
        num_energy_group = file_cont[0]
        num_neutron_group = file_cont[1]
        num_mat_mt = file_cont[4]
        num_matrix = file_cont[5]

        # Read file description length to skip it
        file_desc_len = unpack(sym+'i', full_file[file_cont_end+4:file_cont_end+8])[0]

        n_start = file_cont_end + 8 + file_desc_len + 8
        n_end = n_start + (num_neutron_group+1)*4
        n_string = sym + 'f'*(num_neutron_group+1)
        n_groups = np.array(unpack(n_string, full_file[n_start:n_end]))
        n_end += 4
        
        # Add the neutron groups to the groups dictionary
        self.cov_groups[fname] = n_groups

        # Read in the material reaction control data
        mat_controls = []
        for i in range(num_mat_mt):
            # Setup for 3 integers
            mat_start = n_end + 4 + i*12
            mat_end = mat_start + 8
            # Mat ID, Reaction ID, xs weighting option 1-5
            mat_controls.append(unpack(sym+'ii', full_file[mat_start:mat_end]))
        mat_end += 4

        # Read in the material cross sections and errors into a nested dict
        file_xs_dict = {}
        # Iterate through all material reactions
        for i in range(num_mat_mt):
            file_mat_xs = {}
            # Setup for number of energy groups floats
            xs_start = mat_end + i*(num_energy_group+1)*8 + 8
            xs_end = xs_start + num_energy_group*4
            xs_string = sym + 'f'*num_energy_group
            # Read in the cross sections for current material reaction
            file_mat_xs['xs'] = list(unpack(xs_string, full_file[xs_start:xs_end]))
            
            # Setup for number of energy groups floats
            err_start = xs_end
            err_end = err_start + num_energy_group*4
            err_string = xs_string
            # Read in the cross section errors for current material reaction
            file_mat_xs['std'] = list(unpack(err_string, full_file[err_start:err_end]))
            
            # Put the xs and error in the full xs dictionary
            file_xs_dict[mat_controls[i]] = file_mat_xs

        err_end += 4
        # Put the xs information in the saved dictionary
        self.mat_xs[fname] = file_xs_dict

        # Start prev_end at start of the matrices section
        prev_end = err_end
        # Read in the covariance matrices
        matrices = {}
        for _ in range(num_matrix):
            # Read in the matrix control data
            # Setup to read 5 integers
            matrix_cntrl_start = prev_end + 4
            matrix_cntrl_end = matrix_cntrl_start + 20
            matrix_cntrl = unpack(sym+'iiiii', full_file[matrix_cntrl_start:matrix_cntrl_end])
            mat_1 = matrix_cntrl[0]
            reac_1 = matrix_cntrl[1]
            mat_2 = matrix_cntrl[2]
            reac_2 = matrix_cntrl[3]
            # Iterate past number of bytes value
            matrix_cntrl_end += 4

            # Read in the block control values
            block_cntrl = []
            # Iterate past the number of bytes in block control value
            block_cntrl_start = matrix_cntrl_end + 4
            block_cntrl_end = block_cntrl_start + 2*num_energy_group*4 + 8
            # Iterate through all energy groups
            for j in range(num_energy_group):
                start = block_cntrl_start + j*8
                # Values per group and position of diagonal element for group
                block_cntrl.append(unpack(sym+'ii', full_file[start:start+8]))

            # Read in the relative covariance matrix
            matrix_start = block_cntrl_end + 4
            prev_read = 0
            # Initialize the matrix to an array of zeros
            matrix = np.zeros((num_energy_group, num_energy_group), dtype=float)
            col = 0
            # For each energy grouping
            for num_vals, diag_pos in block_cntrl:
                # Read in each energy group's column
                start = matrix_start + prev_read
                end = start + num_vals*4
                string = sym + 'f'*num_vals
                full_col = unpack(string, full_file[start:end])
                for row in range(num_vals):
                    # Place the values so the diagonal position is in the diagonal
                    matrix[col+row-diag_pos+1][col] = full_col[row]
                # Update the previous read value to past this energy groups
                prev_read += num_vals*4
                col += 1
            matrices[(mat_1, reac_1, mat_2, reac_2)] = matrix
            prev_end = end + 4
        
        # Save the covariance matrices for this file
        self.cov_matrices[fname] = matrices

    def get_mat_name(self, matid):
        '''Translate the material ID into 
        the name. IDs are mostly the same 
        as MCNP IDs/1000 except for some 
        special cases that scale made 
        impossible to program without a dict.
        '''
        E = {v: k for k, v in elements.items()}
        # Check for special cases
        if matid // 1000000 > 0:
            # One of the specials with 7 digits
            return specials[matid]
        elif matid == 1002:
            # If H-2
            return 'D'
        # Extract the mass number
        A = str(matid % 1000)
        # Translate the atomic number
        Z = E[matid // 1000]
        return Z + '-' + A

    def get_mt_name(self, mtid):
        '''Same as get_mat_name 
        but used for reactions. 
        Sorry if the names make 
        no sense. I pulled directly 
        from the Scale documentation. 
        Check scale_ids.py for details.
        '''
        return mt_ids[mtid]

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
        key_df = self.df[key[0]][key[1]][key[2]][key[3]].dropna()
        sens = np.array(key_df['sensitivity'], dtype=float)
        # Calculate the integral
        int_value = np.sum(sens)
        if len(key_df.columns) == 2:
            stdevs = np.array(key_df['std dev'], dtype=float)
            # Calculate the uncertainty (root sum square)
            int_unc = np.sqrt(np.sum(np.square(stdevs)))
        else:
            int_unc = np.nan

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
                sens_x = np.array(self.df[keys[i][0]][keys[i][1]][keys[i][2]][keys[i][3]]['sensitivity'].loc[indices].dropna(), dtype=float)
                sens_y = np.array(self.df[keys[j][0]][keys[j][1]][keys[j][2]][keys[j][3]]['sensitivity'].loc[indices].dropna(), dtype=float)
                if lethargy is False:
                    sens_x = sens_x/lethargies
                    sens_y = sens_y/lethargies

                r[(tuple(keys[i]),tuple(keys[j]))] = pearsonr(sens_x, sens_y)[0]
        return r

    def sensitivity_plot(self, keys, elow=float('-inf'), ehigh=float('inf'), plot_err_bar=True,
                         plot_fill_bet=False, plot_corr=False, legend_dict=None, r_pos='bottom right'):
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
        plot_err_bar : bool, optional
            Whether the user wants the error bars to be included 
            in the generated plot. Defaults to True.
        plot_fill_bet : bool, optional
            Whether the user wants the error to be plotted as a 
            fill between. Defaults to False.
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
        self.__make_plot(keys, elow, ehigh, plot_err_bar, plot_fill_bet, plot_corr, plot_lethargy, legend_dict, r_pos, ylabel)

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
        plot_lethargy = True

        # Send the data to the plot making function
        self.__make_plot(keys, elow, ehigh, plot_err_bar, plot_fill_bet, plot_corr, plot_lethargy, legend_dict, r_pos, ylabel)

    def heatmap_plot(self, mat_mt_1, mat_mt_2, filename, covariance=True, elow=float('-inf'),
                     ehigh=float('inf'), cmap='viridis', tick_step=1, mode='publication',
                     label1=None, label2=None):
        '''Create a heatmap of the covariance or 
        correlation matrix for the selected material 
        and reaction pairs.

        Parameters
        ----------
        mat_mt_1 : tuple
            The material and reaction id number 
            for one of the cross sections.
        mat_mt_2 : tuple
            The material and reaction id number 
            for the second cross sectionss.
        filename : str
            Name of the file that where the matrix 
            was found. 
        covariance : bool, optional
            If true the covariance matrix is plotted. 
            If false the correlation matrix is plotted.
        elow : float, optional
            The low bound for energies to plot. 
            Defaults to -inf.
        ehigh : float, optional
            The high bound for energies to plot. 
            Defaults to inf.
        cmap : str, optional
            Color mapping to be used for heatmap. 
            Can be set as any Matplotlib cmap.
        tick_step : int, optional
            How often the tick marks should be 
            placed on axis.
        mode : str, optional
            Can be either 'research' or 
            'publication'. Research is geared towards 
            finding the group and value for a matrix spot 
            while publication looks more like the heatmaps 
            found in published papers.
        label1 : str, optional
            Desired text for the first nuclide and reaction.
        label2 : str, optional
            Desired text for the second nuclide and reaction.
        
        '''
        # Figure out which nuclide and reaction should come first in the key
        if tuple([mat_mt_1[0], mat_mt_1[1], mat_mt_2[0],  mat_mt_2[1]]) in self.cov_matrices[filename].keys():
            mat_mt_pair = tuple([mat_mt_1[0], mat_mt_1[1], mat_mt_2[0],  mat_mt_2[1]])
        elif tuple([mat_mt_2[0], mat_mt_2[1], mat_mt_1[0],  mat_mt_1[1]]) in self.cov_matrices[filename].keys():
            mat_mt_pair = tuple([mat_mt_2[0], mat_mt_2[1], mat_mt_1[0],  mat_mt_1[1]])
        else:
            assert False, 'Material and Reaction pairs not found'

        # Filter the boundaries for ehigh and elow
        max_bounds_full = self.cov_groups[filename][:-1]
        max_bounds = np.array([])
        indices = []
        for i in range(len(max_bounds_full)):
            if max_bounds_full[i] <= ehigh and max_bounds_full[i] > elow:
                max_bounds = np.append(max_bounds, max_bounds_full[i])
                indices.append(i)
        # Grab the indices of the maximum and minimum energy bound
        i_max = indices[0]
        i_min = indices[-1]+1

        # Grab the matrix data
        if covariance:
            matrix_full = self.cov_matrices[filename][mat_mt_pair]
            st = 'Covariance'

        else:
            # Calculate the correlation matrix
            matrix_full = self.__cov_to_corr(mat_mt_pair, filename)
            st = 'Correlation'
        # Index the matrix data
        matrix = matrix_full[i_max:i_min, i_max:i_min]

        #Turn the matrix into a heatmap
        fig, ax = plt.subplots()
        fig.set_size_inches(13.25, 10)
        im = ax.imshow(matrix, cmap=cmap, interpolation='none')
        
        # Show the colorbar
        cbar = ax.figure.colorbar(im, ax=ax)
        # Set the tick labels for either mode
        if mode == 'publication':
            # Make the labels show the max energy bounds
            ax.set_xticks(np.arange(0, len(indices), tick_step))
            ax.set_yticks(np.arange(0, len(indices), tick_step))
            # Make labels in scientific notation with 2 decimal places
            labels = ['{:.2e}'.format(bound) for bound in max_bounds][::tick_step]
            ax.set_xticklabels(labels)
            ax.set_yticklabels(labels)
        elif mode == 'research':
            # Make the labels show the energy groups index
            # Preserves the x and y coordinates in top right corner
            ax.set_xticks(np.arange(0, len(indices), tick_step))
            ax.set_yticks(np.arange(0, len(indices), tick_step))
            # Put the max energy bounds on the right of the plot
            s1 = 'Max Bounds (eV)\n'
            s2 = '\n'.join(['{}-{} : {:.2e}'.format(i-0.5, i+0.5, max_bounds[i]) for i in range(0,len(indices),tick_step)])
            ax.text(float(-len(indices))/3.45, len(indices)/2, s1+s2, ha='left', va='center')
        else:
            assert False, "mode must be either 'research' or 'mode' not '{}'".format(mode)

        # Place x axis tick labels on top
        ax.xaxis.tick_top()
        # Put tick marks on all sides
        ax.tick_params(bottom=True, top=True, left=True, right=True)
        # Rotate the x axis tick labels by 45 degrees.
        plt.setp(ax.get_xticklabels(), rotation=45, ha='left', rotation_mode='anchor')

        # Put the IDs into readable text if no labels given
        if label1 is None:
            label1 = self.get_mat_name(mat_mt_1[0])
            label1 += ' '
            label1 += self.get_mt_name(mat_mt_1[1])
        if label2 is None:
            label1 = self.get_mat_name(mat_mt_2[0])
            label1 += ' '
            label1 += self.get_mt_name(mat_mt_2[1])
        # Put a title and axis titles on the plot
        ax.set_title('{} matrix for {} and {}'.format(st, label1, label2))
        cbar.set_label(st)

        # Make the layout tight and show the plot
        for _ in range(5):
            fig.tight_layout()
        plt.show()

    def __make_plot(self, keys, elow, ehigh, plot_err_bar, plot_fill_bet, plot_corr,
                    plot_lethargy, legend_dict, r_pos, ylabel):
        '''The parts of making a plot that are repeated.'''
        # Make sure keys is a list of lists
        if type(keys[0]) is not list:
            keys = [keys]
        # Assert maximum number of keys to plot
        assert len(keys) < 24, 'Maximum number of keys to plot is 24'
        # Create the title
        exp_list = []
        for exp, _, _, _ in keys:
            exp_list.append(exp)
        exp_set = set(exp_list)
        title = '-'.join(exp_set)
        # Create the text for the correlation
        r_text = ''
        # The energy bounds information
        indices_dict = {}
        energy_vals_dict = {}
        lethargies_dict = {}
        for exp in exp_set:
            indices_list = []
            energy_vals_array = np.array([], dtype=float)
            lethargies_array = np.array([], dtype=float)
            for bound in self.df[exp].dropna().index:
                # Add the high and low bounds to energy bounds
                e_upper = float(bound.split(':')[0])
                e_lower = float(bound.split(':')[1])
                # Only add in energy values within given elow and ehigh
                if e_upper <= ehigh and e_lower >= elow:
                    indices_list.append(bound)
                    energy_vals_array = np.append(energy_vals_array, [e_upper, e_lower])
                    # Calculate the lethargies for each energy grouping
                    lethargies_array = np.append(lethargies_array, log(e_upper/e_lower))
            indices_dict[exp] = indices_list
            energy_vals_dict[exp] = energy_vals_array
            lethargies_dict[exp] = lethargies_array
        if plot_corr:
            r_text += 'Correlations:'
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
                    r_text += '\n{} and {} r = {:.4}'.format(key_text1, key_text2, r)
        i = 0
        colors = ['g', 'r', 'c', 'm', 'k', 'y']
        ls = ['-', '--', '.-', '.']
        legends = []
        plt.figure()
        for key in keys:
            # Get the keys energy bound info
            indices = indices_dict[key[0]]
            energy_vals = energy_vals_dict[key[0]]
            lethargies = lethargies_dict[key[0]]
            # Create the legend title
            if legend_dict is None:
                # If no legend was passed in create one
                legend_title = ' '.join(tuple(key))
            else:
                # If legend titles were passed in then use them
                legend_title = legend_dict[tuple(key)]
            
            # Raise an error if passed in keys are not 4
            assert len(key) == 4, 'Must pass 4 identifiers in each key'

            # Collect the the data for the key in given energy bounds and remove NaN
            key_df = self.df[key[0]][key[1]][key[2]][key[3]].loc[indices].dropna()
            sens = np.array(key_df['sensitivity'], dtype=float)
            # Flag for stdev values existing
            typeB = False
            if len(key_df.columns) == 2:
                stdevs = np.array(self.df[key[0]][key[1]][key[2]][key[3]]['std dev'].loc[indices].dropna(), dtype=float)
                typeB = True

            # Calculate the sensitivities per lethargy if passed in
            if plot_lethargy:
                sens = sens/lethargies
                if typeB:
                    stdevs = stdevs/lethargies

            # Make each sensitivity std dev appear twice for step feature
            sens_step = np.array([], dtype=float)
            stdev_step = np.array([], dtype=float)
            for j in range(len(sens)):
                sens_step = np.append(sens_step, [sens[j], sens[j]])
                if typeB:
                    stdev_step = np.append(stdev_step, [stdevs[j], stdevs[j]])

            # Plot the sensitivity
            if not plot_fill_bet:
                plt.plot(energy_vals, sens_step, ls=ls[i//6], color=colors[i%6], linewidth=1)
            else:
                plt.plot(energy_vals, sens_step, ls=ls[i//6], color=colors[i%6], linewidth=1, alpha=0)

            # If standard deviations exist
            if typeB:
                if plot_err_bar:
                    assert plot_fill_bet is False, 'plot_err_bar and plot_fill_bet cannot both be True' 
                    # Plot the error bars
                    mid_vals = np.power(10, (np.log10(energy_vals[::2]) + np.log10(energy_vals[1::2]))/2)
                    _, _, eb = plt.errorbar(mid_vals, sens, yerr=stdevs, fmt='none', ecolor=colors[i%6], elinewidth=1, capsize=2, capthick=1)
                    eb[0].set_linestyle(':')
                elif plot_fill_bet:
                    # Plot the std dev as a fill between
                    plt.fill_between(energy_vals, sens_step-stdev_step, sens_step+stdev_step, ls=ls[i//6], color=colors[i%6], alpha=0.3)

            # Add the integral value information
            int_value, int_unc = self.get_integral(key)
            if not typeB:
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
        plt.title(title)
        plt.grid(b=True)
        plt.tight_layout()
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

    def __cov_to_corr(self, mat_mt_pair, filename):
        # Grab the covariance matrix
        cov_mat = self.cov_matrices[filename][mat_mt_pair]
        num_groups = len(cov_mat)
        mat_mt1 = (mat_mt_pair[0], mat_mt_pair[1])
        mat_mt2 = (mat_mt_pair[2], mat_mt_pair[3])
        # Initialize correlation matrix
        corr = np.zeros((num_groups, num_groups))
        for i in range(num_groups):
            for j in range(num_groups):
                # corr[i][j] = cov[i][j] / (xs_error[i] * xs_error[j])
                std1 = self.mat_xs[filename][mat_mt1]['std'][i]
                std2 = self.mat_xs[filename][mat_mt2]['std'][j]
                corr[i][j] =  cov_mat[i][j] / (std1 * std2)
        return corr
