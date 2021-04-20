import PyQt5
import matplotlib.pyplot as plt
import sys
import os
import scale_plots


class PLOTS_GUI(PyQt5.QtWidgets.QMainWindow):

    def __init__(self):
        PyQt5.QtWidgets.QMainWindow.__init__(self)

        # Grab the plots object
        self.plots = scale_plots.Plots()
        # Variables for filenames
        self.filename_widgets = []
        self.filenames = []
        # Variables for reaction selection and legends
        self.keys = []
        self.labels = []
        self.legend_entry_edits = {}

        # Current directory for file selection
        self.cwd = os.getcwd()

        # Main widget
        self.widget = PyQt5.QtWidgets.QWidget()
        self.layout = PyQt5.QtWidgets.QGridLayout()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

        # Create grid widget and layout for file selection
        self.file_grid_widget = PyQt5.QtWidgets.QWidget()
        self.file_grid_layout = PyQt5.QtWidgets.QGridLayout()
        self.file_grid_widget.setLayout(self.file_grid_layout)

        # Setup the file selet menu
        self.layout.addWidget(self.file_grid_widget, 0, 0)

        # Create the file select button
        self.file_select_btn = PyQt5.QtWidgets.QPushButton('Select New File')
        self.file_select_btn.clicked.connect(self.parse_file)
        self.layout.addWidget(self.file_select_btn, 1, 0)

        # Create the reset files widget
        row = len(self.filenames)
        self.reset_files_btn = PyQt5.QtWidgets.QPushButton('Reset Files')
        self.reset_files_btn.clicked.connect(self.reset_files)
        self.layout.addWidget(self.reset_files_btn, 2, 0)
        
        # Insert horizontal line between file and reaction selections
        self.file_reaction_line = PyQt5.QtWidgets.QFrame()
        self.file_reaction_line.setLineWidth(2)
        self.file_reaction_line.setFrameShape(PyQt5.QtWidgets.QFrame.HLine)
        self.layout.addWidget(self.file_reaction_line, 3, 0)

        # Create and add the data grid widget for reactions
        self.data_grid_widget = PyQt5.QtWidgets.QWidget()
        self.data_grid_layout = PyQt5.QtWidgets.QGridLayout()
        self.data_grid_widget.setLayout(self.data_grid_layout)
        self.layout.addWidget(self.data_grid_widget, 4, 0)

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
        self.add_button = PyQt5.QtWidgets.QPushButton('Add')
        self.add_button.clicked.connect(self.add_clicked)
        self.data_grid_layout.addWidget(self.add_button, 1, 4)

        # Create the reset button
        self.plot_data_reset_btn = PyQt5.QtWidgets.QPushButton('Reset Reactions')
        self.plot_data_reset_btn.clicked.connect(self.plot_data_reset_clicked)
        self.layout.addWidget(self.plot_data_reset_btn, 5, 0)

        # Insert horizontal line between reaction and sensitivity areas
        self.reaction_sens_line = PyQt5.QtWidgets.QFrame()
        self.reaction_sens_line.setLineWidth(2)
        self.reaction_sens_line.setFrameShape(PyQt5.QtWidgets.QFrame.HLine)
        self.layout.addWidget(self.reaction_sens_line, 6, 0)
        
        # Create label for options affecting sensitivity plots
        self.sens_options_label = PyQt5.QtWidgets.QLabel('Sensitivity Plotting Options:')
        self.sens_options_label.setFont(PyQt5.QtGui.QFont('Arial', 14))
        self.layout.addWidget(self.sens_options_label, 7, 0)

        # Put the sensitivities extra options into the main layout
        self.sens_extra_options_widget = PyQt5.QtWidgets.QWidget()
        self.sens_extra_options_layout = PyQt5.QtWidgets.QGridLayout()
        self.sens_extra_options_widget.setLayout(self.sens_extra_options_layout)
        self.layout.addWidget(self.sens_extra_options_widget, 8, 0)

        # Create the check box for plotting error bars
        self.error_bar_check = PyQt5.QtWidgets.QCheckBox('Plot Errorbars')
        self.error_bar_check.stateChanged.connect(self.single_check)
        self.sens_extra_options_layout.addWidget(self.error_bar_check, 0, 0)

        # Create the check boc for plotting fill between error bars
        self.fill_bet_check = PyQt5.QtWidgets.QCheckBox('Plot Fill Between')
        self.fill_bet_check.stateChanged.connect(self.single_check)
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
        self.layout.addWidget(self.plot_sens_btn, 9, 0)

        # Create the sensitivities per lethargy button
        self.plot_per_lethargy_btn = PyQt5.QtWidgets.QPushButton('Plot Sensitivities per Unit Lethargy')
        self.plot_per_lethargy_btn.clicked.connect(self.plot_sens)
        self.layout.addWidget(self.plot_per_lethargy_btn, 10, 0)

        # Insert horizontal line between sensitivity and correlation areas
        self.sens_corr_line = PyQt5.QtWidgets.QFrame()
        self.sens_corr_line.setLineWidth(2)
        self.sens_corr_line.setFrameShape(PyQt5.QtWidgets.QFrame.HLine)
        self.layout.addWidget(self.sens_corr_line, 11, 0)

        # Create the label for options affecting the correlation plot
        self.corr_options_label = PyQt5.QtWidgets.QLabel('Correlation/Covariance Plotting Options:')
        self.corr_options_label.setFont(PyQt5.QtGui.QFont('Arial', 14))
        self.layout.addWidget(self.corr_options_label, 12, 0)

        # Put the correlation extra options into the main widget
        self.corr_extra_options_widget = PyQt5.QtWidgets.QWidget()
        self.corr_extra_options_layout = PyQt5.QtWidgets.QGridLayout()
        self.corr_extra_options_widget.setLayout(self.corr_extra_options_layout)
        self.layout.addWidget(self.corr_extra_options_widget, 13, 0)

        # Create the combo box to decide which reaction to plot correlations for
        self.corr_reaction_box_label = PyQt5.QtWidgets.QLabel('Reaction to Plot:')
        self.corr_extra_options_layout.addWidget(self.corr_reaction_box_label, 0, 0)
        self.corr_reaction_box = PyQt5.QtWidgets.QComboBox()
        self.corr_extra_options_layout.addWidget(self.corr_reaction_box, 0, 1, 1, 2)

        # Create the high and low bounds for the correlation plot
        self.corr_elow_box = PyQt5.QtWidgets.QComboBox()
        self.corr_ehigh_box = PyQt5.QtWidgets.QComboBox()
        self.corr_elow_label = PyQt5.QtWidgets.QLabel('Low Energy Bound (eV):')
        self.corr_ehigh_label = PyQt5.QtWidgets.QLabel('High Energy Bound (eV):')

        # Add energy bound boxes and labels to layout
        self.corr_extra_options_layout.addWidget(self.corr_elow_label, 1, 1)
        self.corr_extra_options_layout.addWidget(self.corr_ehigh_label, 2, 1)
        self.corr_extra_options_layout.addWidget(self.corr_elow_box, 1, 2)
        self.corr_extra_options_layout.addWidget(self.corr_ehigh_box, 2, 2)

        # Create the covariance plotting button
        self.plot_cov_btn = PyQt5.QtWidgets.QPushButton('Plot Covariance Matrix')
        self.plot_cov_btn.clicked.connect(self.plot_corr)
        self.layout.addWidget(self.plot_cov_btn, 14, 0)

        # Create the correlation plotting button
        self.plot_corr_btn = PyQt5.QtWidgets.QPushButton('Plot Correlation Matrix')
        self.plot_corr_btn.clicked.connect(self.plot_corr)
        self.layout.addWidget(self.plot_corr_btn, 15, 0)

    def parse_file(self):
        # Let the user pick the sdf file to read in
        filename = PyQt5.QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', self.cwd)[0]
        # Parse the selected sdf file into a DataFrame
        if filename != '' and filename not in self.filenames:
            self.plots.sdf_to_df(filename)
            row = len(self.filenames)

            # Update the widget to show the filename
            file_name_widget = PyQt5.QtWidgets.QLabel(filename)
            self.file_grid_layout.addWidget(file_name_widget, row, 0)
            self.filename_widgets.append(file_name_widget)
            self.filenames.append(filename)

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

            # Clear the 4 energy bound combo boxes
            self.sens_elow_box.clear()
            self.sens_ehigh_box.clear()
            self.corr_elow_box.clear()
            self.corr_ehigh_box.clear()

            # Update the 4 energy bound combo boxes
            self.sens_elow_box.addItems(elows)
            self.sens_ehigh_box.addItems(ehighs)
            self.corr_elow_box.addItems(elows)
            self.corr_ehigh_box.addItems(ehighs)

            # Update reaction combo boxes
            self.update_exp_box()

    def reset_files(self):
        if len(self.filenames) > 0:
            # Clear file name widgets
            for filename_widget in self.filename_widgets:
                self.file_grid_delete(filename_widget)
            # Remove saved information
            self.filename_widgets = []
            self.filenames = []
            self.plots.df = None
            # Clear the combo boxes
            combos = [self.exp_box, self.iso_box, self.inter_box,
                      self.unit_reg_box, self.sens_ehigh_box, self.sens_elow_box,
                      self.corr_ehigh_box, self.corr_elow_box]
            for combo in combos:
                combo.clear()
            # Clear the selected data
            self.plot_data_reset_clicked()

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

    def add_clicked(self):
        # For each drop down menu
        key = []
        boxes = [self.exp_box, self.iso_box, self.inter_box, self.unit_reg_box]
        for box in boxes:
            # Save the value
            key.append(box.currentText())

        # Do not add the selected reaction if it has already been added
        if key not in self.keys and '' not in key:
            # Create the legend entry text edit
            legend_title = ' '.join(key)
            legend_entry_edit = PyQt5.QtWidgets.QLineEdit(legend_title)
            self.data_grid_layout.addWidget(legend_entry_edit, len(self.keys)+2, 4)
            self.legend_entry_edits[tuple(key)] = legend_entry_edit

            for i in range(len(boxes)):
                # Make Qlabels below the selected data
                label = PyQt5.QtWidgets.QLabel(key[i])
                self.data_grid_layout.addWidget(label, len(self.keys)+2, i)
                self.labels.append(label)

            # Add the key to the keys list
            self.keys.append(key)
            
            # Update the correlation reaction combo box
            self.corr_reaction_box.addItem(' '.join(key))

    def single_check(self, state):
        # Ensure that only one error checkbox is marked
        if state == PyQt5.QtCore.Qt.Checked:
            # If the error bar is checked
            if self.sender() == self.error_bar_check:
                # Uncheck the fill between checkbox
                self.fill_bet_check.setChecked(False)
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
        self.keys = []
        self.labels = []
        self.legend_entry_edits = {}
        self.corr_reaction_box.clear()

    def plot_sens(self):
        # If there is anything to plot
        if len(self.keys) > 0:
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
            if len(self.keys) > 1:
                corr_flag = self.corr_check.isChecked()
                r_pos = self.corr_text_pos_box.currentText()               
            # Stops 'QCoreApplication::exec: The event loop is already running' warning
            plt.ion()
            # If sensitivity button was pressed
            if self.sender() == self.plot_sens_btn:
                self.plots.sensitivity_plot(self.keys, elow=elow, ehigh=ehigh, plot_err_bar=error_bar_flag,
                                            plot_fill_bet=fill_bet_flag, plot_corr=corr_flag,
                                            legend_dict=legend_entries, r_pos=r_pos)
            # If sensitivity per unit lethargy button was pressed
            else:
                self.plots.sensitivity_lethargy_plot(self.keys, elow=elow, ehigh=ehigh, plot_err_bar=error_bar_flag,
                                                    plot_fill_bet=fill_bet_flag, plot_corr=corr_flag,
                                                    legend_dict=legend_entries, r_pos=r_pos)

    def plot_corr(self):
        # If there is anything to plot
        if len(self.keys) > 0:
            # Get the high and low bounds
            elow = float(self.corr_elow_box.currentText())
            ehigh = float(self.corr_ehigh_box.currentText())
            # Get the reaction to plot
            key = tuple(self.corr_reaction_box.currentText().split())

    def file_grid_delete(self, widget):
        # Deletes a widget from the data add object
        self.file_grid_layout.removeWidget(widget)
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
