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

        self.grid_widget = PyQt5.QtWidgets.QWidget()
        self.widget = PyQt5.QtWidgets.QWidget()

        # Create grid and box layout
        self.grid_layout = PyQt5.QtWidgets.QGridLayout()
        self.grid_widget.setLayout(self.grid_layout)
        self.layout = PyQt5.QtWidgets.QVBoxLayout()

        # Create the file select button
        self.file_select_btn = PyQt5.QtWidgets.QPushButton('Select New File')
        self.file_select_btn.clicked.connect(self.parse_file)
        self.layout.addWidget(self.file_select_btn, 0)

        # Create the button to select data for plotting
        self.select_data_btn = PyQt5.QtWidgets.QPushButton('Pick Data to Plot')
        self.select_data_btn.clicked.connect(self.setup_plot_data)

        # Setup the file selet menu
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)        

    def parse_file(self):
        # Let the user pick the sdf file to read in
        filename = PyQt5.QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', self.cwd)[0]
        # Parse the selected sdf file into a DataFrame
        if filename != '':
            self.plots.sdf_to_df(filename)

            # Update the widget to show the filename
            row = len(self.filenames)
            self.grid_layout.removeWidget(self.file_select_btn)
            file_name = PyQt5.QtWidgets.QLabel(filename)
            self.layout.addWidget(file_name, row)
            self.filenames.append(file_name)
            self.layout.addWidget(self.file_select_btn, row+1)
            self.layout.addWidget(self.select_data_btn, row+2)

    def setup_plot_data(self):
        # Remove the widgets from the file selection part of the gui
        if self.filenames != []:
            for filename in self.filenames:
                self.layout_delete(filename)
            self.layout_delete(self.file_select_btn)
            self.layout_delete(self.select_data_btn)
            self.filenames = []

        self.layout.addWidget(self.grid_widget)

        # Create labels for drop down menus
        exp_label = PyQt5.QtWidgets.QLabel('Experiment')
        self.grid_layout.addWidget(exp_label, 0, 0)
        iso_label = PyQt5.QtWidgets.QLabel('Isotope')
        self.grid_layout.addWidget(iso_label, 0, 1)
        inter_label = PyQt5.QtWidgets.QLabel('Interaction')
        self.grid_layout.addWidget(inter_label, 0, 2)
        unit_reg_label = PyQt5.QtWidgets.QLabel('(Unit,Region)')
        self.grid_layout.addWidget(unit_reg_label, 0, 3)
        legend_entry_label = PyQt5.QtWidgets.QLabel('Legend Entry')
        self.grid_layout.addWidget(legend_entry_label, 0, 4)
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
        self.grid_layout.addWidget(self.exp_box, len(self.keys)+1, 0)

        # Create the drop down menu for the isotopes
        self.iso_box = PyQt5.QtWidgets.QComboBox()
        isos = []
        for column in self.plots.df.columns:
            if self.exp_box.currentText() == column[0]:
                isos.append(column[1])
        self.iso_box.addItems(sorted(set(isos)))
        self.iso_box.activated.connect(self.update_inter_box)
        self.grid_layout.addWidget(self.iso_box, len(self.keys)+1, 1)

        # Create the drop down menu for the interactions
        self.inter_box = PyQt5.QtWidgets.QComboBox()
        inters = []
        for column in self.plots.df.columns:
            if self.exp_box.currentText() == column[0]:
                if self.iso_box.currentText() == column[1]:
                    inters.append(column[2])
        self.inter_box.addItems(sorted(set(inters)))
        self.inter_box.activated.connect(self.update_unit_reg_box)
        self.grid_layout.addWidget(self.inter_box, len(self.keys)+1, 2)

        # Create the drop down menu for the unit region numbers
        self.unit_reg_box = PyQt5.QtWidgets.QComboBox()
        unit_regs = []
        for column in self.plots.df.columns:
            if self.exp_box.currentText() == column[0]:
                if self.iso_box.currentText() == column[1]:
                    if self.inter_box.currentText() == column[2]:
                        unit_regs.append(column[3])
        self.unit_reg_box.addItems(sorted(set(unit_regs), reverse=True))
        self.grid_layout.addWidget(self.unit_reg_box, len(self.keys)+1, 3)

        # Create the add button to enter the key
        self.add_button = PyQt5.QtWidgets.QPushButton('Add')
        self.add_button.clicked.connect(self.add_clicked)
        self.grid_layout.addWidget(self.add_button, len(self.keys)+1, 4)

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
            # Remove the widget and leave a qlabel in its place
            self.grid_delete(boxes[i])
            label = PyQt5.QtWidgets.QLabel(key[i])
            self.grid_layout.addWidget(label, len(self.keys)+1, i)
            self.labels.append(label)

        # Create the legend entry text edit
        legend_title = ' '.join(key)
        legend_entry_edit = PyQt5.QtWidgets.QLineEdit(legend_title)
        self.grid_layout.addWidget(legend_entry_edit, len(self.keys)+1, 4)
        self.legend_entry_edits[tuple(key)] = legend_entry_edit

        # Remove the add button
        self.grid_delete(self.add_button)

        # Add the key to the keys list
        self.keys.append(key)
        self.make_boxes()

        # If the add button is clicked for the first time
        if self.create_btns:
            # Create the check box for plotting error bars
            self.error_bar_check = PyQt5.QtWidgets.QCheckBox('Plot Errorbars')
            self.error_bar_check.toggle()
            self.layout.addWidget(self.error_bar_check)

            # Create the reset button
            self.plot_data_reset_btn = PyQt5.QtWidgets.QPushButton('Reset All')
            self.plot_data_reset_btn.clicked.connect(self.plot_data_reset_clicked)
            self.layout.addWidget(self.plot_data_reset_btn)

            # Create the sensitivities plot button
            self.plot_sens_btn = PyQt5.QtWidgets.QPushButton('Plot Sensitivities')
            self.plot_sens_btn.clicked.connect(self.plot_sens)
            self.layout.addWidget(self.plot_sens_btn)

            # Create the sensitivities per lethargy button
            self.plot_per_lethargy_btn = PyQt5.QtWidgets.QPushButton('Plot Sensitivities per Unit Lethargy')
            self.plot_per_lethargy_btn.clicked.connect(self.plot_sens_per_lethargy)
            self.layout.addWidget(self.plot_per_lethargy_btn)

            self.create_btns = False

    def plot_data_reset_clicked(self):
        # Setup GUI to select new data
        self.clear_plot_data()
        self.setup_plot_data()

    def plot_sens(self):
        # Collect the legend line edits
        legend_entries = {}
        for key, legend_edit in self.legend_entry_edits.items():
            legend_entries[key] = legend_edit.text()
        # Check whether the error should be plotted
        error_flag = self.error_bar_check.isChecked()
        # Stops 'QCoreApplication::exec: The event loop is already running' warning
        plt.ion()
        plt.clf()
        # Make new window of the sensitivity plot
        self.plots.sensitivity_plot(self.keys, plot_std_dev=error_flag,legend_dict=legend_entries)

    def plot_sens_per_lethargy(self):
        # Collect the legend line edits
        legend_entries = {}
        for key, legend_edit in self.legend_entry_edits.items():
            legend_entries[key] = legend_edit.text()
        # Check whether the error should be plotted
        error_flag = self.error_bar_check.isChecked()
        # Stops 'QCoreApplication::exec: The event loop is already running' warning
        plt.ion()
        plt.clf()
        # Make new window of the sensitivity plot
        self.plots.sensitivity_lethargy_plot(self.keys, plot_std_dev=error_flag, legend_dict=legend_entries)

    def clear_plot_data(self):
        # Remove all uneeded widgets
        for box in [self.exp_box, self.iso_box, self.inter_box, self.unit_reg_box]:
            self.grid_delete(box)
        for label in self.labels:
            self.grid_delete(label)
        for key in self.legend_entry_edits:
            self.grid_delete(self.legend_entry_edits[key])
        self.grid_delete(self.add_button)
        self.layout_delete(self.error_bar_check)
        self.layout_delete(self.plot_data_reset_btn)
        self.layout_delete(self.plot_sens_btn)
        self.layout_delete(self.plot_per_lethargy_btn)

    def grid_delete(self, widget):
        # Deletes a widget from the grid layout object
        self.grid_layout.removeWidget(widget)
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
