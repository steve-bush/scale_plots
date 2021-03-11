# scale_plots
Importable module for parsing sdf files from keno and storing the data in a Pandas DataFrame. The collected data can then be plotted for sensitivity vs energy or sensitivity per unit lethargy vs energy. A GUI for easier use is included by typing `python scale_plots/plots_gui.py` into the terminal while in the main `scale_plots/` directory.

Required python libraries:
* NumPy
* SciPy
* pandas
* Matplotlib
* PyQt5

To import the module add `PYTHONPATH="$PYTHONPATH:/path/to/scale_plots"` to your bashrc.

#### `class scale_plots.Plots()`
Object that contains the functions needed to parse and plot the data from a sdf file.

##### `sdf_to_df(filename)`
Parse the keno sdf output file into a pandas DataFrame

Parameters:
* **filename** (str) - Name of the sdf file to parse

Returns:
* **df** (pandas.DataFrame) - DataFrame containing all of the data needed for plotting from the sdf file.

##### `get_corr(self, keys, elow=float('-inf'), ehigh=float('inf'), lethargy=False)`
Return the correlation coefficients for the given keys
Parameters:
* **keys** (list of lists) - Indices in the pandas DataFrame where the desired data is stored.
* **elow** (float, *optional*) - The low bound for energies to calculate correlation. Defaults to -inf.
* **ehigh** (float, *optional*) - The high bound for energies to calculate correlation. Defaults to inf.
* **lethargy** (bool, *optional*) - Whether to find the correlation between sensitivites in unit lethargy. Defaults to False.

Returns:
* **r** (dict)
  - key - tuple of tuples for keys
  - value - correlation coefficient for the 2 reactions in the key

##### `sensitivity_plot(keys, plot_std_dev=True)`
Plot the sensitivity of the given `keys` from the pandas DataFrame stored in `scale_plots.Plots()`.
Default unit and region number are (0,0).

Parameters:
* **keys** (list of lists) - Indices in the pandas DataFrame where the desired sensitivities are stored.
* **elow** (float, *optional*) - The low bound for energies to plot. Defaults to -inf.
* **ehigh** (float, *optional*) - The high bound for energies to plot. Defaults to inf.
* **plot_std_dev** (bool, *optional*) - Whether the user wants the error bars to be included in the generated plot. Defaults to True.
* **plot_corr** (bool, *optional*) - Whether the user wants the correlation coefficient to be given in the plot. Defaults to False.
* **legend_dict** (dictionary, *optional*)
  - keys - key in the keys list of the selected isotope
  - value - string to replace the automatically generated legend
* **r_pos** (str, *optional*) - Where the correlation coefficient should go on the plot. Defaults to 'bottom right'. Can also be 'top right', 'bottom left', and 'top left'.

##### `sensitivity_lethargy_plot(keys, plot_std_dev=True)`
Plot the sensitivity per unit lethargy of the given `keys` from the pandas DataFrame stored in `scale_plots.Plots()`
Default unit and region number are (0,0).

Parameters:
* **keys** (list of lists) - Indices in the pandas DataFrame where the desired sensitivities are stored.
* **elow** (float, *optional*) - The low bound for energies to plot. Defaults to -inf.
* **ehigh** (float, *optional*) - The high bound for energies to plot. Defaults to inf.
* **plot_std_dev** (bool, *optional*) - Whether the user wants the error bars to be included in the generated plot. Defaults to True.
* **plot_corr** (bool, *optional*) - Whether the user wants the correlation coefficient to be given in the plot. Defaults to False.
* **legend_dict** (dictionary, *optional*)
  - keys - key in the keys list of the selected isotope
  - value - string to replace the automatically generated legend
* **r_pos** (str, *optional*) - Where the correlation coefficient should go on the plot. Defaults to 'bottom right'. Can also be 'top right', 'bottom left', and 'top left'.
