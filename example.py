import scale_plots

plots = scale_plots.Plots()
# Parse the sdf file to create a pandas DataFrame
plots.sdf_to_df('KENO_slovenia_tsunami.sdf')
# Place keys in a list of lists or just a list if only one key
keys = [['KENO_slovenia_tsunami', 'zr90-zr5h8', 'total'],['KENO_slovenia_tsunami', 'zr90-zr5h8', 'elastic']]
legend = {tuple(keys[0]) : 'total', tuple(keys[1]) : 'elastic'}
# Can also pass plot_std_dev=False to remove error bars
plots.sensitivity_lethargy_plot(keys, plot_std_dev=True, legend_dict=legend)