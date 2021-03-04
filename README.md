# scale_plots
Importable module for parsing sdf files from keno and storing the data in a Pandas DataFrame. The collected data can then be plotted for sensitivity vs energy or sensitivity per unit lethargy vs energy. A GUI for easier use and functionality will be added in future updates.

Required python libraries:
* NumPy
* pandas
* Matplotlib

To import the module add `PYTHONPATH="$PYTHONPATH:/path/to/scale_plots"` to your bashrc.

#### `class scale_plots.Plots()`
Object that contains the functions needed to parse and plot the data from a sdf file.

##### `sdf_to_df(filename)`
Parse the keno sdf output file into a pandas DataFrame

Parameters:
* **filename** (str) - Name of the sdf file to parse

Returns:
* **df** (pandas.DataFrame) - DataFrame containing all of the data needed for plotting from the sdf file.

##### `sensitivity_plot(keys, plot_std_dev=True)`
Plot the sensitivity of the given `keys` from the pandas DataFrame stored in `scale_plots.Plots()`.
Default unit and region number are (0,0).

Parameters:
* **keys** (list of lists) - Indices in the pandas DataFrame where the desired sensitivities are stored.
* **plot_std_dev** (bool, *optional*) - Whether the user wants the error bars to be included in the generated plot. Defaults to True.
* **legend_dict** (dictionary, *optional*)
keys : key in the keys list of the selected isotope
value : string to replace the automatically generated legend

##### `sensitivity_lethargy_plot(keys, plot_std_dev=True)`
Plot the sensitivity per unit lethargy of the given `keys` from the pandas DataFrame stored in `scale_plots.Plots()`
Default unit and region number are (0,0).

Parameters:
* **keys** (list of lists) - Indices in the pandas DataFrame where the desired sensitivities are stored.
* **plot_std_dev** (bool, *optional*) - Whether the user wants the error bars to be included in the generated plot. Defaults to True.
* * **legend_dict** (dictionary, *optional*)
keys : key in the keys list of the selected isotope
value : string to replace the automatically generated legend
