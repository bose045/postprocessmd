# plot_data.py

## Description

`plot_data.py` is a Python script for plotting data from log files with customizable options, specially suitable for log files from lammps. You might have multiple data segments in the file. But the script will collect the data from the asked segment and plot them.

## Requirements

- Python 3.x
- matplotlib
- pandas

## Installation

1. Clone or download the `plot_data.py` script to your local machine.
2. Ensure that you have Python 3.x installed.
3. Install the required dependencies using pip:


## Usage

```bash
python plot_data.py filename [--instance INSTANCE] [--columns COLUMNS [COLUMNS ...]] [--xlabel XLABEL] [--ylabel YLABEL] [--legends LEGENDS] [--logscale]
python plot_data.py log.lammps --outfile time_vs_energy.png --columns Step PotEng TotEng --instance last --xlabel "Timestep" --ylabel "Energy" --legends '["PE","Total"]'
Arguments
filename: Path to the data file.
--instance INSTANCE: Instance to plot: "first", "last", or an integer (1-based). Default is "first".
--columns COLUMNS [COLUMNS ...]: Column names or indices to plot. First one is x-axis, followed by one or more y-axis columns.
--xlabel XLABEL: Label for the x-axis. Default is "X-axis".
--ylabel YLABEL: Label for the y-axis. Default is "Y-axis".
--legends LEGENDS: List of legends as a string (e.g., '["Curve 1", "Curve 2"]'). Default is None.
--logscale: Set log scale for the y-axis. Default is False.
--outfile: filename for outputfile 

Additional Notes

The script automatically detects and parses data segments within the log file based on the provided column names.
If column names are not specified, the script will attempt to identify them from the header line in the log file.
The plotted data can be customized with options such as xlabel, ylabel, legends, and logscale.

