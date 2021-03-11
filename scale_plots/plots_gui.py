import PyQt5
import PyQt5.QtWidgets
import matplotlib.pyplot as plt
import sys
import os
import scale_plots


class PLOTS_GUI(PyQt5.QtWidgets.QMainWindow):

    def __init__(self):
        PyQt5.QtWidgets.QMainWindow.__init__(self)

        # Grab the plots object
        self.plots = scale_plots.Plots()
        self.filenames = []
        self.cwd = os.getcwd()

        self.data_grid_widget = PyQt5.QtWidgets.QWidget()
        self.extra_options_widget = PyQt5.QtWidgets.QWidget()
        self.widget = PyQt5.QtWidgets.QWidget()

        # Create grid layouts
        self.data_add_layout = PyQt5.QtWidgets.QGridLayout()
        self.data_grid_widget.setLayout(self.data_add_layout)
        self.extra_options_layout = PyQt5.QtWidgets.QGridLayout()
        self.extra_options_widget.setLayout(self.extra_options_layout)
        self.layout = PyQt5.QtWidgets.QGridLayout()
        self.widget.setLayout(self.layout)

        # Create the file select button
        self.file_select_btn = PyQt5.QtWidgets.QPushButton('Select New File')
        self.file_select_btn.clicked.connect(self.parse_file)
        self.layout.addWidget(self.file_select_btn, 0, 0)

        # Create the button to select data for plotting
        self.select_data_btn = PyQt5.QtWidgets.QPushButton('Pick Data to Plot')
        self.select_data_btn.clicked.connect(self.setup_plot_data)

        # Setup the file selet menu
        self.setCentralWidget(self.widget)        

    def parse_file(self):
        # Let the user pick the sdf file to read in
        filename = PyQt5.QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', self.cwd)[0]
        # Parse the selected sdf file into a DataFrame
        if filename != '':
            self.plots.sdf_to_df(filename)

            # Update the widget to show the filename
            row = len(self.filenames)
            self.data_add_layout.removeWidget(self.file_select_btn)
            file_name = PyQt5.QtWidgets.QLabel(filename)
            self.layout.addWidget(file_name, row, 0)
            self.filenames.append(file_name)
            self.layout.addWidget(self.file_select_btn, row+1, 0)
            self.layout.addWidget(self.select_data_btn, row+2, 0)

    def setup_plot_data(self):
        # Remove the widgets from the file selection part of the gui
        if self.filenames != []:
            for filename in self.filenames:
                self.layout_delete(filename)
            self.layout_delete(self.file_select_btn)
            self.layout_delete(self.select_data_btn)
            self.filenames = []

        self.layout.addWidget(self.data_grid_widget, 0, 0)
        self.layout.addWidget(self.extra_options_widget, 1, 0)

        # Create labels for drop down menus
        exp_label = PyQt5.QtWidgets.QLabel('Experiment')
        self.data_add_layout.addWidget(exp_label, 0, 0)
        iso_label = PyQt5.QtWidgets.QLabel('Isotope')
        self.data_add_layout.addWidget(iso_label, 0, 1)
        inter_label = PyQt5.QtWidgets.QLabel('Interaction')
        self.data_add_layout.addWidget(inter_label, 0, 2)
        unit_reg_label = PyQt5.QtWidgets.QLabel('(Unit,Region)')
        self.data_add_layout.addWidget(unit_reg_label, 0, 3)
        legend_entry_label = PyQt5.QtWidgets.QLabel('Legend Entry')
        self.data_add_layout.addWidget(legend_entry_label, 0, 4)
        self.labels = [exp_label, iso_label, inter_label, unit_reg_label, legend_entry_label]

        # Create the experiment drop down menus
        self.keys = []
        self.legend_entry_edits = {}
        self.create_btns = True
        self.make_boxes()
    
    def make_boxes(self):
        # Create the drop down menus for the experiments
        self.exp_box = PyQt5.QtWidgets.QComboBox()
        exps = []
        for column in self.plots.df.columns:
            exps.append(column[0])
        self.exp_box.addItems(sorted(set(exps)))
        self.exp_box.activated.connect(self.update_iso_box)
        self.data_add_layout.addWidget(self.exp_box, 1, 0)

        # Create the drop down menu for the isotopes
        self.iso_box = PyQt5.QtWidgets.QComboBox()
        isos = []
        for column in self.plots.df.columns:
            if self.exp_box.currentText() == column[0]:
                isos.append(column[1])
        self.iso_box.addItems(sorted(set(isos)))
        self.iso_box.activated.connect(self.update_inter_box)
        self.data_add_layout.addWidget(self.iso_box, 1, 1)

        # Create the drop down menu for the interactions
        self.inter_box = PyQt5.QtWidgets.QComboBox()
        inters = []
        for column in self.plots.df.columns:
            if self.exp_box.currentText() == column[0]:
                if self.iso_box.currentText() == column[1]:
                    inters.append(column[2])
        self.inter_box.addItems(sorted(set(inters)))
        self.inter_box.activated.connect(self.update_unit_reg_box)
        self.data_add_layout.addWidget(self.inter_box, 1, 2)

        # Create the drop down menu for the unit region numbers
        self.unit_reg_box = PyQt5.QtWidgets.QComboBox()
        unit_regs = []
        for column in self.plots.df.columns:
            if self.exp_box.currentText() == column[0]:
                if self.iso_box.currentText() == column[1]:
                    if self.inter_box.currentText() == column[2]:
                        unit_regs.append(column[3])
        self.unit_reg_box.addItems(sorted(set(unit_regs), reverse=True))
        self.data_add_layout.addWidget(self.unit_reg_box, 1, 3)

        # Create the add button to enter the key
        self.add_button = PyQt5.QtWidgets.QPushButton('Add')
        self.add_button.clicked.connect(self.add_clicked)
        self.data_add_layout.addWidget(self.add_button, 1, 4)

    def update_iso_box(self):
        # Update the available options in the isotope drop down   
        self.iso_box.clear()
        isos = []
        for column in self.plots.df.columns:
            if self.exp_box.currentText() == column[0]:
                isos.append(column[1])
        self.iso_box.addItems(sorted(set(isos)))
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

    def add_clicked(self):
        # For each drop down menu
        key = []
        boxes = [self.exp_box, self.iso_box, self.inter_box, self.unit_reg_box]
        for i in range(len(boxes)):
            # Save the value
            key.append(boxes[i].currentText())
            # Make Qlabels below of the selected data
            label = PyQt5.QtWidgets.QLabel(key[i])
            self.data_add_layout.addWidget(label, len(self.keys)+2, i)
            self.labels.append(label)

        # Create the legend entry text edit
        legend_title = ' '.join(key)
        legend_entry_edit = PyQt5.QtWidgets.QLineEdit(legend_title)
        self.data_add_layout.addWidget(legend_entry_edit, len(self.keys)+2, 4)
        self.legend_entry_edits[tuple(key)] = legend_entry_edit

        # Add the key to the keys list
        self.keys.append(key)

        # If the add button is clicked for the first time
        if self.create_btns:
            # Create the check box for plotting error bars
            self.error_bar_check = PyQt5.QtWidgets.QCheckBox('Plot Errorbars')
            self.error_bar_check.toggle()
            self.extra_options_layout.addWidget(self.error_bar_check, 0, 0)

            # Create the energy bounds boxes and label
            self.elow_box = PyQt5.QtWidgets.QComboBox()
            self.ehigh_box = PyQt5.QtWidgets.QComboBox()
            self.elow_label = PyQt5.QtWidgets.QLabel('Low Energy Bound (eV):')
            self.ehigh_label = PyQt5.QtWidgets.QLabel('High Energy Bound (eV):')
            elows = []
            ehighs = []
            for bound in self.plots.df.index:
                # Add the high and low bounds to their list
                elows.append(float(bound.split(':')[1]))
                ehighs.append(float(bound.split(':')[0]))
            # Sort the energy bounds and turn them back into strings
            elows = [str(e) for e in sorted(elows)]
            ehighs = [str(e) for e in sorted(ehighs, reverse=True)]
            self.elow_box.addItems(elows)
            self.ehigh_box.addItems(ehighs)
            self.extra_options_layout.addWidget(self.elow_label, 0, 1)
            self.extra_options_layout.addWidget(self.ehigh_label, 1, 1)
            self.extra_options_layout.addWidget(self.elow_box, 0, 2)
            self.extra_options_layout.addWidget(self.ehigh_box, 1, 2)

            # Create the sensitivities plot button
            self.plot_sens_btn = PyQt5.QtWidgets.QPushButton('Plot Sensitivities')
            self.plot_sens_btn.clicked.connect(self.plot_sens)
            self.layout.addWidget(self.plot_sens_btn, 2, 0)

            # Create the sensitivities per lethargy button
            self.plot_per_lethargy_btn = PyQt5.QtWidgets.QPushButton('Plot Sensitivities per Unit Lethargy')
            self.plot_per_lethargy_btn.clicked.connect(self.plot_sens_per_lethargy)
            self.layout.addWidget(self.plot_per_lethargy_btn, 3, 0)

            # Create the reset button
            self.plot_data_reset_btn = PyQt5.QtWidgets.QPushButton('Reset All')
            self.plot_data_reset_btn.clicked.connect(self.plot_data_reset_clicked)
            self.layout.addWidget(self.plot_data_reset_btn, 4, 0)

            self.create_btns = False
        # If 2 keys then make correlation checking an option
        elif len(self.keys) == 2:
            # Create the check box for showing the correlation
            self.corr_check = PyQt5.QtWidgets.QCheckBox('Show Correlation')
            self.extra_options_layout.addWidget(self.corr_check, 1, 0)

            # Create the label and combo box for correlation text position
            self.corr_text_pos_label = PyQt5.QtWidgets.QLabel('Correlation Text Position:')
            self.corr_text_pos_box = PyQt5.QtWidgets.QComboBox()
            positions = ['Bottom Right', 'Bottom Left', 'Top Right', 'Top Left']
            self.corr_text_pos_box.addItems(positions)
            self.extra_options_layout.addWidget(self.corr_text_pos_label, 2, 0)
            self.extra_options_layout.addWidget(self.corr_text_pos_box, 2, 1)

    def plot_data_reset_clicked(self):
        # Setup GUI to select new data
        self.clear_plot_data()
        self.setup_plot_data()

    def plot_sens(self):
        # Get plotting data
        elow, ehigh, error_flag, corr_flag, legend_entries, r_pos = self.preplot()
        # Make new window of the sensitivity plot
        self.plots.sensitivity_plot(self.keys, elow=elow, ehigh=ehigh, plot_std_dev=error_flag,
                                    plot_corr=corr_flag, legend_dict=legend_entries, r_pos=r_pos)

    def plot_sens_per_lethargy(self):
        # Get plotting data
        elow, ehigh, error_flag, corr_flag, legend_entries, r_pos = self.preplot()
        # Make new window of the sensitivity plot
        self.plots.sensitivity_lethargy_plot(self.keys, elow=elow, ehigh=ehigh, plot_std_dev=error_flag,
                                             plot_corr=corr_flag, legend_dict=legend_entries, r_pos=r_pos)

    def preplot(self):
        # Get the high and low bounds
        elow = float(self.elow_box.currentText())
        ehigh = float(self.ehigh_box.currentText())
        # Collect the legend line edits
        legend_entries = {}
        for key, legend_edit in self.legend_entry_edits.items():
            legend_entries[key] = legend_edit.text()
        # Check whether the error and correlation should be plotted
        error_flag = self.error_bar_check.isChecked()
        if len(self.keys) > 1:
            corr_flag = self.corr_check.isChecked()
            r_pos = self.corr_text_pos_box.currentText()
        else:
            corr_flag = False
            r_pos = 'bottom right'
        # Stops 'QCoreApplication::exec: The event loop is already running' warning
        plt.ion()
        plt.clf()
        return elow, ehigh, error_flag, corr_flag, legend_entries, r_pos

    def clear_plot_data(self):
        # Remove all uneeded widgets
        for box in [self.exp_box, self.iso_box, self.inter_box, self.unit_reg_box]:
            self.data_add_grid_delete(box)
        for label in self.labels:
            self.data_add_grid_delete(label)
        for key in self.legend_entry_edits:
            self.data_add_grid_delete(self.legend_entry_edits[key])
        self.data_add_grid_delete(self.add_button)
        self.extra_options_grid_delete(self.error_bar_check)
        self.extra_options_grid_delete(self.elow_box)
        self.extra_options_grid_delete(self.ehigh_box)
        self.extra_options_grid_delete(self.elow_label)
        self.extra_options_grid_delete(self.ehigh_label)
        self.extra_options_grid_delete(self.corr_text_pos_label)
        self.extra_options_grid_delete(self.corr_text_pos)
        if len(self.keys) > 1:
            self.extra_options_grid_delete(self.corr_check)
        self.layout_delete(self.plot_data_reset_btn)
        self.layout_delete(self.plot_sens_btn)
        self.layout_delete(self.plot_per_lethargy_btn)

    def data_add_grid_delete(self, widget):
        # Deletes a widget from the data add object
        self.data_add_layout.removeWidget(widget)
        widget.deleteLater()
        widget = None

    def extra_options_grid_delete(self, widget):
        # Deletes a widget from the extra options object
        self.extra_options_layout.removeWidget(widget)
        widget.deleteLater()
        widget = None

    def layout_delete(self, widget):
        # Deletes a widget from the layout object
        self.layout.removeWidget(widget)
        widget.deleteLater()
        widget = None


if __name__ == '__main__':
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    widget = PLOTS_GUI()
    widget.show()
    app.exec_()
