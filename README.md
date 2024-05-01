# LogPlot Tool

The `logplot.py` script is a versatile tool designed for processing and visualizing data from structured log files. It allows users to specify columns for plotting, apply mathematical operations to the data, and customize the output plot.

## Features

- **Data Segmentation**: Automatically segments data based on headers.
- **Mathematical Operations**: Apply operations on data columns before plotting.
- **Flexible Plotting Options**: Customizable plots with options for axis labels, legends, and log scale.
- **Output Control**: Save the plot directly to a file.

## Requirements

This script requires Python 3.x and the following Python libraries:
- `pandas`
- `matplotlib`
- `numpy`

You can install these packages using pip:

'pip install pandas matplotlib numpy'

## Usage

### Basic Command Structure

python logplot.py <filename> --columns <column_names> [options]

### Mandatory Arguments

- **`filename`**: Path to the data file (CSV format expected).
- **`--columns`**: Specifies the column names to load from the file for operations and plotting.

### Optional Arguments

- **`--operations`**: Specifies mathematical operations to apply to the columns, e.g., `"new_col=x1+x2"`.
- **`--plot_columns`**: Specifies which columns to plot against each other, e.g., `x`, `y`.
- **`--xlabel`**: Label for the x-axis.
- **`--ylabel`**: Label for the y-axis.
- **`--legends`**: List of legends for the plot, formatted as a string array.
- **`--logscale`**: Enables log scaling for the y-axis.
- **`--outfile`**: Specifies the filename for the output plot. Defaults to `plot.png`.
- **`--instance`**: Specifies which instance of data to plot if multiple segments are found. Options are `first`, `last`, or an integer (1-based index).

### Example Command

```bash
python logplot.py data.csv --columns Step PotEng TotEng --operations "Step=Step/1e6" "PE=PotEng/1000" --plot_columns Step PE --xlabel "Timestep (ns)" --ylabel "Potential Energy (kJ)" --legends '["Timestep","Potential Energy"]' --logscale --outfile "energy_plot.png"

python logplot.py log.lammps --columns Step Pxx Pyy Pzz Press --operations "Step=Step/1e6" "Press=Press/100" "Pxx=Pxx/100" "Pyy=Pyy/100" "Pzz=Pzz/100" --instance last --xlabel Timestep --ylabel Pressure --outfile Time_vs_Pressure.png
