import PyQt5
import matplotlib.pyplot as plt
import sys
import os
import scale_plots
from scale_ids import mat_ids, mt_ids


class PLOTS_GUI(PyQt5.QtWidgets.QMainWindow):

    def __init__(self):
        PyQt5.QtWidgets.QMainWindow.__init__(self)

        # Grab the plots object
        self.plots = scale_plots.Plots()
        # Variables for filenames
        self.sens_filename_widgets = []
        self.sens_filenames = []
        self.cov_filename_widgets = []
        self.cov_filenames = []
        # Variables for reaction selection and legends
        self.sens_keys = []
        self.labels = []
        self.legend_entry_edits = {}
        # Color mapping options
        self.cmaps = ['viridis', 'plasma', 'inferno', 'magma', 'cividis',
                      'PiYG', 'PRGn', 'BrBG', 'RdBu', 'bwr']

        # Current directory for file selection
        self.cwd = os.getcwd()

        # Main widget
        self.widget = PyQt5.QtWidgets.QWidget()
        self.layout = PyQt5.QtWidgets.QHBoxLayout()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

        # Sensitivity widget
        self.sens_widget = PyQt5.QtWidgets.QGroupBox()
        self.sens_layout = PyQt5.QtWidgets.QVBoxLayout()
        self.sens_widget.setLayout(self.sens_layout)
        self.layout.addWidget(self.sens_widget, 0)

        # Create label for sensitivity file selection
        self.sens_files_label = PyQt5.QtWidgets.QLabel('Sensitivity Files')
        self.sens_files_label.setFont(PyQt5.QtGui.QFont('Arial', 14))
        self.sens_layout.addWidget(self.sens_files_label, 0)

        # Create grid widget and layout for file selection
        self.sens_file_grid_widget = PyQt5.QtWidgets.QWidget()
        self.sens_file_grid_layout = PyQt5.QtWidgets.QGridLayout()
        self.sens_file_grid_widget.setLayout(self.sens_file_grid_layout)

        # Setup the file selet menu
        self.sens_layout.addWidget(self.sens_file_grid_widget, 1)

        # Create the file select button
        self.sens_file_select_btn = PyQt5.QtWidgets.QPushButton('Select New File')
        self.sens_file_select_btn.clicked.connect(self.parse_sens_file)
        self.sens_layout.addWidget(self.sens_file_select_btn, 2)

        # Create the reset files widget
        self.reset_sens_files_btn = PyQt5.QtWidgets.QPushButton('Reset Files')
        self.reset_sens_files_btn.clicked.connect(self.reset_sens_files)
        self.sens_layout.addWidget(self.reset_sens_files_btn, 3)
        
        # Insert horizontal line between file and reaction selections
        self.sens_file_reaction_line = PyQt5.QtWidgets.QFrame()
        self.sens_file_reaction_line.setLineWidth(2)
        self.sens_file_reaction_line.setFrameShape(PyQt5.QtWidgets.QFrame.HLine)
        self.sens_layout.addWidget(self.sens_file_reaction_line, 4)

        # Create label for sensitivity reaction selection
        self.sens_reaction_label = PyQt5.QtWidgets.QLabel('Sensitivity Reaction Selection')
        self.sens_reaction_label.setFont(PyQt5.QtGui.QFont('Arial', 14))
        self.sens_layout.addWidget(self.sens_reaction_label, 5)

        # Create and add the data grid widget for reactions
        self.data_grid_widget = PyQt5.QtWidgets.QWidget()
        self.data_grid_layout = PyQt5.QtWidgets.QGridLayout()
        self.data_grid_widget.setLayout(self.data_grid_layout)
        self.sens_layout.addWidget(self.data_grid_widget, 6)

        # Create labels for drop down menus
        exp_label = PyQt5.QtWidgets.QLabel('Experiment')
        self.data_grid_layout.addWidget(exp_label, 0, 0)
        iso_label = PyQt5.QtWidgets.QLabel('Isotope')
        self.data_grid_layout.addWidget(iso_label, 0, 1)
        inter_label = PyQt5.QtWidgets.QLabel('Interaction')
        self.data_grid_layout.addWidget(inter_label, 0, 2)
        unit_reg_label = PyQt5.QtWidgets.QLabel('(Unit,Region)')
        self.data_grid_layout.addWidget(unit_reg_label, 0, 3)
        legend_entry_label = PyQt5.QtWidgets.QLabel('Legend Entry')
        self.data_grid_layout.addWidget(legend_entry_label, 0, 4)

        # Create the drop down menus for the experiments
        self.exp_box = PyQt5.QtWidgets.QComboBox()
        self.exp_box.activated.connect(self.update_iso_box)
        self.data_grid_layout.addWidget(self.exp_box, 1, 0)

        # Create the drop down menu for the isotopes
        self.iso_box = PyQt5.QtWidgets.QComboBox()
        self.iso_box.activated.connect(self.update_inter_box)
        self.data_grid_layout.addWidget(self.iso_box, 1, 1)

        # Create the drop down menu for the interactions
        self.inter_box = PyQt5.QtWidgets.QComboBox()
        self.inter_box.activated.connect(self.update_unit_reg_box)
        self.data_grid_layout.addWidget(self.inter_box, 1, 2)

        # Create the drop down menu for the unit region numbers
        self.unit_reg_box = PyQt5.QtWidgets.QComboBox()
        self.data_grid_layout.addWidget(self.unit_reg_box, 1, 3)

        # Create the add button to enter the key
        self.sens_add_button = PyQt5.QtWidgets.QPushButton('Add')
        self.sens_add_button.clicked.connect(self.sens_add_clicked)
        self.data_grid_layout.addWidget(self.sens_add_button, 1, 4)

        # Create the reset button
        self.plot_data_reset_btn = PyQt5.QtWidgets.QPushButton('Reset Reactions')
        self.plot_data_reset_btn.clicked.connect(self.plot_data_reset_clicked)
        self.sens_layout.addWidget(self.plot_data_reset_btn, 7)

        # Insert horizontal line between reaction and sensitivity areas
        self.reaction_sens_line = PyQt5.QtWidgets.QFrame()
        self.reaction_sens_line.setLineWidth(2)
        self.reaction_sens_line.setFrameShape(PyQt5.QtWidgets.QFrame.HLine)
        self.sens_layout.addWidget(self.reaction_sens_line, 8)
        
        # Create label for options affecting sensitivity plots
        self.sens_options_label = PyQt5.QtWidgets.QLabel('Sensitivity Plotting Options')
        self.sens_options_label.setFont(PyQt5.QtGui.QFont('Arial', 14))
        self.sens_layout.addWidget(self.sens_options_label, 9)

        # Put the sensitivities extra options into the main layout
        self.sens_extra_options_widget = PyQt5.QtWidgets.QWidget()
        self.sens_extra_options_layout = PyQt5.QtWidgets.QGridLayout()
        self.sens_extra_options_widget.setLayout(self.sens_extra_options_layout)
        self.sens_layout.addWidget(self.sens_extra_options_widget, 10)

        # Create the check box for plotting error bars
        self.error_bar_check = PyQt5.QtWidgets.QCheckBox('Plot Errorbars')
        self.error_bar_check.stateChanged.connect(self.sens_single_check)
        self.sens_extra_options_layout.addWidget(self.error_bar_check, 0, 0)

        # Create the check boc for plotting fill between error bars
        self.fill_bet_check = PyQt5.QtWidgets.QCheckBox('Plot Fill Between')
        self.fill_bet_check.stateChanged.connect(self.sens_single_check)
        self.sens_extra_options_layout.addWidget(self.fill_bet_check, 1, 0)

        # Create the energy bounds boxes and label
        self.sens_elow_label = PyQt5.QtWidgets.QLabel('Low Energy Bound (eV):')
        self.sens_ehigh_label = PyQt5.QtWidgets.QLabel('High Energy Bound (eV):')
        self.sens_elow_box = PyQt5.QtWidgets.QComboBox()
        self.sens_ehigh_box = PyQt5.QtWidgets.QComboBox()

        # Add energy bound boxes and labels to layout
        self.sens_extra_options_layout.addWidget(self.sens_elow_label, 0, 1)
        self.sens_extra_options_layout.addWidget(self.sens_ehigh_label, 1, 1)
        self.sens_extra_options_layout.addWidget(self.sens_elow_box, 0, 2)
        self.sens_extra_options_layout.addWidget(self.sens_ehigh_box, 1, 2)

        # Create the check box for showing the correlation
        self.corr_check = PyQt5.QtWidgets.QCheckBox('Show Correlation')
        self.sens_extra_options_layout.addWidget(self.corr_check, 2, 0)

        # Create the label and combo box for correlation text position
        self.corr_text_pos_label = PyQt5.QtWidgets.QLabel('Correlation Text Position:')
        self.corr_text_pos_box = PyQt5.QtWidgets.QComboBox()
        positions = ['Bottom Right', 'Bottom Left', 'Top Right', 'Top Left']
        self.corr_text_pos_box.addItems(positions)
        self.sens_extra_options_layout.addWidget(self.corr_text_pos_label, 2, 1)
        self.sens_extra_options_layout.addWidget(self.corr_text_pos_box, 2, 2)

        # Create the sensitivities plot button
        self.plot_sens_btn = PyQt5.QtWidgets.QPushButton('Plot Sensitivities')
        self.plot_sens_btn.clicked.connect(self.plot_sens)
        self.sens_layout.addWidget(self.plot_sens_btn, 11)

        # Create the sensitivities per lethargy button
        self.plot_per_lethargy_btn = PyQt5.QtWidgets.QPushButton('Plot Sensitivities per Unit Lethargy')
        self.plot_per_lethargy_btn.clicked.connect(self.plot_sens)
        self.sens_layout.addWidget(self.plot_per_lethargy_btn, 12)




        # Covariance widget
        self.cov_widget = PyQt5.QtWidgets.QGroupBox()
        self.cov_layout = PyQt5.QtWidgets.QVBoxLayout()
        self.cov_widget.setLayout(self.cov_layout)
        self.layout.addWidget(self.cov_widget, 1)

        # Create label for covariance file selection
        self.cov_files_label = PyQt5.QtWidgets.QLabel('Covariance Files')
        self.cov_files_label.setFont(PyQt5.QtGui.QFont('Arial', 14))
        self.cov_layout.addWidget(self.cov_files_label, 0)

        # Create grid widget and layout for file selection
        self.cov_file_grid_widget = PyQt5.QtWidgets.QWidget()
        self.cov_file_grid_layout = PyQt5.QtWidgets.QGridLayout()
        self.cov_file_grid_widget.setLayout(self.cov_file_grid_layout)

        # Setup the file selet menu
        self.cov_layout.addWidget(self.cov_file_grid_widget, 1)

        # Create the file select button
        self.cov_file_select_btn = PyQt5.QtWidgets.QPushButton('Select New File')
        self.cov_file_select_btn.clicked.connect(self.parse_cov_file)
        self.cov_layout.addWidget(self.cov_file_select_btn, 2)

        # Create the reset files widget
        self.reset_cov_files_btn = PyQt5.QtWidgets.QPushButton('Reset Files')
        self.reset_cov_files_btn.clicked.connect(self.reset_cov_files)
        self.cov_layout.addWidget(self.reset_cov_files_btn, 3)
        
        # Insert horizontal line between file and reaction selections
        self.cov_file_reaction_line = PyQt5.QtWidgets.QFrame()
        self.cov_file_reaction_line.setLineWidth(2)
        self.cov_file_reaction_line.setFrameShape(PyQt5.QtWidgets.QFrame.HLine)
        self.cov_layout.addWidget(self.cov_file_reaction_line, 4)

        # Create the label for options affecting the correlation plot
        self.cov_reactions_label = PyQt5.QtWidgets.QLabel('Covariance Reaction Selection')
        self.cov_reactions_label.setFont(PyQt5.QtGui.QFont('Arial', 14))
        self.cov_layout.addWidget(self.cov_reactions_label, 5)

        # Put the correlation reaction selection into the main widget
        self.cov_reaction_widget = PyQt5.QtWidgets.QWidget()
        self.cov_reaction_layout = PyQt5.QtWidgets.QGridLayout()
        self.cov_reaction_widget.setLayout(self.cov_reaction_layout)
        self.cov_layout.addWidget(self.cov_reaction_widget, 6)

        # Create the combo box for covariance files
        self.cov_file_box_label = PyQt5.QtWidgets.QLabel('Filename:')
        self.cov_reaction_layout.addWidget(self.cov_file_box_label, 0, 0)
        self.cov_file_box = PyQt5.QtWidgets.QComboBox()
        self.cov_file_box.activated.connect(self.update_nuclide1_box)
        self.cov_file_box.activated.connect(self.update_cov_ebounds)
        self.cov_reaction_layout.addWidget(self.cov_file_box, 0, 1, 1, 3)

        # Create the labels for the matrix selection combo boxes
        cov_nuclide_box_label = PyQt5.QtWidgets.QLabel('Nuclides')
        self.cov_reaction_layout.addWidget(cov_nuclide_box_label, 1, 1)
        cov_interaction_box_label = PyQt5.QtWidgets.QLabel('Interactions')
        self.cov_reaction_layout.addWidget(cov_interaction_box_label, 1, 2)
        cov_label_label = PyQt5.QtWidgets.QLabel('Label')
        self.cov_reaction_layout.addWidget(legend_entry_label, 1, 3)
        cov_reac1_box_label = PyQt5.QtWidgets.QLabel('Reaction 1:')
        self.cov_reaction_layout.addWidget(cov_reac1_box_label, 2, 0)
        cov_reac2_box_label = PyQt5.QtWidgets.QLabel('Reaction 2:')
        self.cov_reaction_layout.addWidget(cov_reac2_box_label, 3, 0)

        # Create the combo boxes for reactions 1 and 2
        self.cov_reac1_nuclide_box = PyQt5.QtWidgets.QComboBox()
        self.cov_reac1_nuclide_box.activated.connect(self.update_interaction1_box)
        self.cov_reaction_layout.addWidget(self.cov_reac1_nuclide_box, 2, 1)

        self.cov_reac1_interaction_box = PyQt5.QtWidgets.QComboBox()
        self.cov_reac1_interaction_box.activated.connect(self.update_nuclide2_box)
        self.cov_reaction_layout.addWidget(self.cov_reac1_interaction_box, 2, 2)

        self.cov_reac1_label_edit = PyQt5.QtWidgets.QLineEdit()
        self.cov_reaction_layout.addWidget(self.cov_reac1_label_edit, 2, 3)

        self.cov_reac2_nuclide_box = PyQt5.QtWidgets.QComboBox()
        self.cov_reac2_nuclide_box.activated.connect(self.update_interaction2_box)
        self.cov_reaction_layout.addWidget(self.cov_reac2_nuclide_box, 3, 1)

        self.cov_reac2_interaction_box = PyQt5.QtWidgets.QComboBox()
        self.cov_reac2_interaction_box.activated.connect(self.update_edits)
        self.cov_reaction_layout.addWidget(self.cov_reac2_interaction_box, 3, 2)

        self.cov_reac2_label_edit = PyQt5.QtWidgets.QLineEdit()
        self.cov_reaction_layout.addWidget(self.cov_reac2_label_edit, 3, 3)

        # Insert horizontal line between reaction selection and plotting options
        self.cov_reaction_options_line = PyQt5.QtWidgets.QFrame()
        self.cov_reaction_options_line.setLineWidth(2)
        self.cov_reaction_options_line.setFrameShape(PyQt5.QtWidgets.QFrame.HLine)
        self.cov_layout.addWidget(self.cov_reaction_options_line, 8)

        # Create the label for options affecting the correlation plot
        self.cov_options_label = PyQt5.QtWidgets.QLabel('Covariance Plotting Options')
        self.cov_options_label.setFont(PyQt5.QtGui.QFont('Arial', 14))
        self.cov_layout.addWidget(self.cov_options_label, 9)

        # Put the correlation reaction selection into the main widget
        self.cov_extra_options_widget = PyQt5.QtWidgets.QWidget()
        self.cov_extra_options_layout = PyQt5.QtWidgets.QGridLayout()
        self.cov_extra_options_widget.setLayout(self.cov_extra_options_layout)
        self.cov_layout.addWidget(self.cov_extra_options_widget, 10)

        # Create the mode selection radio buttons
        self.research = PyQt5.QtWidgets.QRadioButton('Research Mode')
        self.research.setChecked(True)
        self.cov_extra_options_layout.addWidget(self.research, 0, 0, 1, 2)
        self.publication = PyQt5.QtWidgets.QRadioButton('Publication Mode')
        self.cov_extra_options_layout.addWidget(self.publication, 1, 0, 1, 2)

        # Create the high and low labels for energy bounds
        self.cov_elow_label = PyQt5.QtWidgets.QLabel('Low Energy Bound (eV):')
        self.cov_extra_options_layout.addWidget(self.cov_elow_label, 0, 2)
        self.cov_ehigh_label = PyQt5.QtWidgets.QLabel('High Energy Bound (eV):')
        self.cov_extra_options_layout.addWidget(self.cov_ehigh_label, 1, 2)

        # Create the combo boxes for the high and low energy bounds
        self.cov_elow_box = PyQt5.QtWidgets.QComboBox()
        self.cov_extra_options_layout.addWidget(self.cov_elow_box, 0, 3)
        self.cov_ehigh_box = PyQt5.QtWidgets.QComboBox()
        self.cov_extra_options_layout.addWidget(self.cov_ehigh_box, 1, 3)

        # Create the spin box for selecting the number of values between ticks
        self.cov_tick_step_label = PyQt5.QtWidgets.QLabel('Tick Step')
        self.cov_extra_options_layout.addWidget(self.cov_tick_step_label, 2, 1)
        self.cov_tick_step_spinbox = PyQt5.QtWidgets.QSpinBox()
        self.cov_tick_step_spinbox.setMinimum(1)
        self.cov_extra_options_layout.addWidget(self.cov_tick_step_spinbox, 2, 0)

        # Create the color mapping lable and combo box
        self.cov_cmap_label = PyQt5.QtWidgets.QLabel('Color Mapping:')
        self.cov_extra_options_layout.addWidget(self.cov_cmap_label, 2, 2)
        self.cov_cmap_box = PyQt5.QtWidgets.QComboBox()
        self.cov_cmap_box.addItems(self.cmaps)
        self.cov_extra_options_layout.addWidget(self.cov_cmap_box, 2, 3)

        # Create the relative covariance plotting button
        self.plot_rel_cov_btn = PyQt5.QtWidgets.QPushButton('Plot Relative Covariance Matrix')
        self.plot_rel_cov_btn.clicked.connect(self.plot_cov)
        self.cov_layout.addWidget(self.plot_rel_cov_btn, 11)
        
        # Create the covariance plotting button
        self.plot_cov_btn = PyQt5.QtWidgets.QPushButton('Plot Covariance Matrix')
        self.plot_cov_btn.clicked.connect(self.plot_cov)
        self.cov_layout.addWidget(self.plot_cov_btn, 12)

        # Create the correlation plotting button
        self.plot_corr_btn = PyQt5.QtWidgets.QPushButton('Plot Correlation Matrix')
        self.plot_corr_btn.clicked.connect(self.plot_cov)
        self.cov_layout.addWidget(self.plot_corr_btn, 13)

    def parse_sens_file(self):
        # Let the user pick the sdf file to read in
        sens_filename = PyQt5.QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', self.cwd)[0]
        # Parse the selected sdf file into a DataFrame
        if sens_filename != '' and sens_filename not in self.sens_filenames:
            self.plots.sdf_to_df(sens_filename)
            row = len(self.sens_filenames)

            # Update the widget to show the filename
            sens_file_name_widget = PyQt5.QtWidgets.QLabel(sens_filename)
            self.sens_file_grid_layout.addWidget(sens_file_name_widget, row, 0)
            self.sens_filename_widgets.append(sens_file_name_widget)
            self.sens_filenames.append(sens_filename)

            # Get the high and low bounds
            elows = []
            ehighs = []
            for bound in self.plots.df.index:
                # Add the high and low bounds to their list
                elows.append(float(bound.split(':')[1]))
                ehighs.append(float(bound.split(':')[0]))
            # Sort the energy bounds and turn them back into strings
            elows = [str(e) for e in sorted(elows)]
            ehighs = [str(e) for e in sorted(ehighs, reverse=True)]

            # Clear the energy bound combo boxes
            self.sens_elow_box.clear()
            self.sens_ehigh_box.clear()

            # Update the energy bound combo boxes
            self.sens_elow_box.addItems(elows)
            self.sens_ehigh_box.addItems(ehighs)

            # Update reaction combo boxes
            self.update_exp_box()
    
    def parse_cov_file(self):
        # Let the user pick the covariance file to read in
        cov_filename = PyQt5.QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', self.cwd)[0]
        # Parse the selected covariance file into the dictionary
        if cov_filename != '' and cov_filename not in self.cov_filenames:
            self.plots.parse_coverx(cov_filename)
            row = len(self.cov_filenames)

            # Update the widget to show the filename
            cov_file_name_widget = PyQt5.QtWidgets.QLabel(cov_filename)
            self.cov_file_grid_layout.addWidget(cov_file_name_widget, row, 0)
            self.cov_filename_widgets.append(cov_file_name_widget)
            self.cov_filenames.append(cov_filename.split('/')[-1])

            # Update reaction combo boxes
            self.update_filename_box()


    def reset_sens_files(self):
        if len(self.sens_filenames) > 0:
            # Clear file name widgets
            for sens_filename_widget in self.sens_filename_widgets:
                self.sens_file_grid_delete(sens_filename_widget)
            # Remove saved information
            self.sens_filename_widgets = []
            self.sens_filenames = []
            self.plots.df = None
            # Clear the combo boxes
            combos = [self.exp_box, self.iso_box, self.inter_box,
                      self.unit_reg_box, self.sens_ehigh_box, self.sens_elow_box]
            for combo in combos:
                combo.clear()
            # Clear the selected data
            self.plot_data_reset_clicked()

    def reset_cov_files(self):
        if len(self.cov_filenames) > 0:
            # Clear the file name widgets
            for cov_filename_widget in self.cov_filename_widgets:
                self.cov_file_grid_delete(cov_filename_widget)
            # Remove saved information
            self.cov_filename_widgets = []
            self.cov_filenames = []
            self.plots.cov_matrices = {}
            # Clear the combo boxes
            self.cov_ehigh_box.clear()
            self.cov_elow_box.clear()

    def update_exp_box(self):
        # Update the available options in the experiment drop down
        self.exp_box.clear()
        exps = []
        for column in self.plots.df.columns:
            exps.append(column[0])
        self.exp_box.addItems(sorted(set(exps)))
        # Update the combo box size for new text
        self.exp_box.resize(self.exp_box.sizeHint())
        # Update the interactions drop down
        self.update_iso_box()

    def update_iso_box(self):
        # Update the available options in the isotope drop down
        self.iso_box.clear()
        isos = []
        for column in self.plots.df.columns:
            if self.exp_box.currentText() == column[0]:
                isos.append(column[1])
        self.iso_box.addItems(sorted(set(isos)))
        # Update the combo box size for new text
        self.iso_box.resize(self.iso_box.sizeHint())
        # Update the interactions drop down
        self.update_inter_box()

    def update_inter_box(self):
        # Update the available options in the interactions drop down 
        self.inter_box.clear()
        inters = []
        for column in self.plots.df.columns:
            if self.exp_box.currentText() == column[0]:
                if self.iso_box.currentText() == column[1]:
                    inters.append(column[2])
        self.inter_box.addItems(sorted(set(inters)))
        # Update the combo box size for new text
        self.inter_box.resize(self.inter_box.sizeHint())
        # Update the unit region drop down
        self.update_unit_reg_box()

    def update_unit_reg_box(self):
        # Update the available options in the unit and region number drop down
        self.unit_reg_box.clear()
        unit_regs = []
        for column in self.plots.df.columns:
            if self.exp_box.currentText() == column[0]:
                if self.iso_box.currentText() == column[1]:
                    if self.inter_box.currentText() == column[2]:
                        unit_regs.append(column[3])
        self.unit_reg_box.addItems(sorted(set(unit_regs), reverse=True))
        # Update the combo box size for new text
        self.unit_reg_box.resize(self.unit_reg_box.sizeHint())
    
    def update_filename_box(self):
        # Update the available options in the filename drop down
        self.cov_file_box.clear()
        self.cov_file_box.addItems(self.cov_filenames)
        self.update_nuclide1_box()

    def update_nuclide1_box(self):
        # Update the available options for the first nuclide drop down
        filename = self.cov_file_box.currentText()
        self.cov_reac1_nuclide_box.clear()
        mats = []
        for mat1, _, mat2, _ in self.plots.cov_matrices[filename].keys():
            #mats.append(mat_ids[mat1])
            #mats.append(mat_ids[mat2])
            if mat1 not in mat_ids.keys():
                print(mat1)
            if mat2 not in mat_ids.keys():
                print(mat2)
        mats = set(mats)
        self.cov_reac1_nuclide_box.addItems(mats)
    
    def update_interaction1_box(self):
        pass

    def update_nuclide2_box(self):
        pass

    def update_interaction2_box(self):
        pass

    def update_edits(self):
        pass
    
    def update_cov_ebounds(self):
        # Get the high and low bounds
        filename = self.cov_file_box.currentText()
        elows = []
        ehighs = [float(self.plots.cov_n_groups[filename][0])]
        # Place all but first and last value into the arrays
        for i in range(1, len(self.plots.cov_n_groups[filename])-1):
            elows.append(float(self.plots.cov_n_groups[filename][i]))
            ehighs.append(float(self.plots.cov_n_groups[filename][i]))
        elows.append(float(self.plots.cov_n_groups[filename][-1]))

            # Sort the energy bounds and turn them back into strings
        elows = [str(e) for e in sorted(elows)]
        ehighs = [str(e) for e in sorted(ehighs, reverse=True)]

        # Clear the energy bound combo boxes
        self.cov_elow_box.clear()
        self.cov_ehigh_box.clear()

        # Update the energy bound combo boxes
        self.cov_elow_box.addItems(elows)
        self.cov_ehigh_box.addItems(ehighs)

    def sens_add_clicked(self):
        # For each drop down menu
        key = []
        boxes = [self.exp_box, self.iso_box, self.inter_box, self.unit_reg_box]
        for box in boxes:
            # Save the value
            key.append(box.currentText())

        # Do not add the selected reaction if it has already been added
        if key not in self.sens_keys and '' not in key:
            # Create the legend entry text edit
            legend_title = ' '.join(key)
            legend_entry_edit = PyQt5.QtWidgets.QLineEdit(legend_title)
            self.data_grid_layout.addWidget(legend_entry_edit, len(self.sens_keys)+2, 4)
            self.legend_entry_edits[tuple(key)] = legend_entry_edit

            for i in range(len(boxes)):
                # Make Qlabels below the selected data
                label = PyQt5.QtWidgets.QLabel(key[i])
                self.data_grid_layout.addWidget(label, len(self.sens_keys)+2, i)
                self.labels.append(label)

            # Add the key to the keys list
            self.sens_keys.append(key)

    def sens_single_check(self, state):
        # Ensure that only one error checkbox is marked
        if state == PyQt5.QtCore.Qt.Checked:
            # If the error bar is checked
            if self.sender() == self.error_bar_check:
                # Uncheck the fill between checkbox
                self.fill_bet_check.setChecked(False)
            # If the fill between is checked
            elif self.sender() == self.fill_bet_check:
                # Uncheck the error bar checkbox
                self.error_bar_check.setChecked(False)

    def plot_data_reset_clicked(self):
        # Remove labels and edits for reactions
        for label in self.labels:
            self.data_add_grid_delete(label)
        for edit in self.legend_entry_edits.values():
            self.data_add_grid_delete(edit)
        # Remove the save reactions
        self.sens_keys = []
        self.labels = []
        self.legend_entry_edits = {}

    def plot_sens(self):
        # If there is anything to plot
        if len(self.sens_keys) > 0:
            # Get the high and low bounds
            elow = float(self.sens_elow_box.currentText())
            ehigh = float(self.sens_ehigh_box.currentText())
            # Collect the legend line edits
            legend_entries = {}
            for key, legend_edit in self.legend_entry_edits.items():
                legend_entries[key] = legend_edit.text()
            # Check whether the error and correlation should be plotted
            error_bar_flag = self.error_bar_check.isChecked()
            fill_bet_flag = self.fill_bet_check.isChecked()
            # Default correlation
            corr_flag = False
            r_pos = 'bottom right'
            if len(self.sens_keys) > 1:
                corr_flag = self.corr_check.isChecked()
                r_pos = self.corr_text_pos_box.currentText()               
            # Stops 'QCoreApplication::exec: The event loop is already running' warning
            plt.ion()
            # If sensitivity button was pressed
            if self.sender() == self.plot_sens_btn:
                self.plots.sensitivity_plot(self.sens_keys, elow=elow, ehigh=ehigh, plot_err_bar=error_bar_flag,
                                            plot_fill_bet=fill_bet_flag, plot_corr=corr_flag,
                                            legend_dict=legend_entries, r_pos=r_pos)
            # If sensitivity per unit lethargy button was pressed
            else:
                self.plots.sensitivity_lethargy_plot(self.sens_keys, elow=elow, ehigh=ehigh, plot_err_bar=error_bar_flag,
                                                    plot_fill_bet=fill_bet_flag, plot_corr=corr_flag,
                                                    legend_dict=legend_entries, r_pos=r_pos)

    def plot_cov(self):
        # If there is anything to plot
        if len(self.sens_keys) > 0:
            # Get the high and low bounds
            elow = float(self.cov_elow_box.currentText())
            ehigh = float(self.cov_ehigh_box.currentText())
            # Get the reaction to plot
            key = tuple(self.cov_reaction_box.currentText().split())

    def sens_file_grid_delete(self, widget):
        # Deletes a widget from the sensitivity file grid
        self.sens_file_grid_layout.removeWidget(widget)
        widget.deleteLater()
        widget = None

    def cov_file_grid_delete(self, widget):
        # Deletes a widget from the covariance file grid
        self.cov_file_grid_layout.removeWidget(widget)
        widget.deleteLater()
        widget = None

    def data_add_grid_delete(self, widget):
        # Deletes a widget from the data add object
        self.data_grid_layout.removeWidget(widget)
        widget.deleteLater()
        widget = None


if __name__ == '__main__':
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    widget = PLOTS_GUI()
    widget.show()
    app.exec_()
