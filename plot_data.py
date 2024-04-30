import matplotlib.pyplot as plt
import numpy as np
import argparse
import ast
import pandas as pd

# eg: python plot_data.py log.lammps --columns Step PotEng TotEng --instance last --xlabel "Timestep" --ylabel "Energy" --legends '["PE","Total"]'

def parse_data_segments(filename, column_names):
    """Parse the file and extract data segments based on headers."""
    with open(filename, 'r') as file:
        content = file.readlines()

    segments = []
    buffer = []
    headers = []
    capture = False

    for line in content:
        line_split = line.strip().split()
        # Check if the current line contains column headers
        if set(column_names).issubset(line_split):
            if buffer:
                # Convert buffer to DataFrame with only the required columns
                segments.append(pd.DataFrame(buffer, columns=headers)[column_names])
                buffer = []
            headers = line_split
            capture = True
            continue
        if capture:
            try:
                buffer.append(list(map(float, line_split)))
            except ValueError:
                capture = False

    if buffer and headers:
        # Handle the last segment
        segments.append(pd.DataFrame(buffer, columns=headers)[column_names])

    return segments

def main():
    parser = argparse.ArgumentParser(description='Plot data segments from a log file with flexible instance selection.')
    parser.add_argument('filename', type=str, help='Path to the data file')
    parser.add_argument('--instance', type=str, default='last', help='Instance to plot: "first", "last" or a number (1-based)')
    parser.add_argument('--columns', nargs='+', help='Column names to plot as x y. First one is x-axis, followed by one or more y-axis columns.')
    parser.add_argument('--xlabel', type=str, default='X-axis', help='Label for the x-axis')
    parser.add_argument('--ylabel', type=str, default='Y-axis', help='Label for the y-axis')
    parser.add_argument('--legends', type=str, help='List of legends as a string (e.g., \'["Curve 1", "Curve 2"]\')')
    parser.add_argument('--logscale', action='store_true', help='Set log scale for the y-axis')

    args = parser.parse_args()
    
    if not args.columns:
        print("Error: No columns specified for plotting.")
        return

    # Extract data segments
    segments = parse_data_segments(args.filename, args.columns)
    if not segments:
        print("No valid data segments found.")
        return
    
    # Determine which instance to plot
    if args.instance.isdigit():
        instance_index = int(args.instance) - 1
    elif args.instance == 'first':
        instance_index = 0
    elif args.instance == 'last':
        instance_index = len(segments) - 1
    else:
        print("Invalid instance specifier. Use 'first', 'last', or an integer.")
        return

    if instance_index < 0 or instance_index >= len(segments):
        print("Instance number out of range.")
        return

    data = segments[instance_index]

    fig, ax = plt.subplots(figsize=(10, 5))

    x_data = data[args.columns[0]]
    for y_col in args.columns[1:]:
        ax.plot(x_data, data[y_col], label=y_col if len(args.columns[1:]) > 1 else "Data")

    ax.set_xlabel(args.xlabel, fontsize=14)
    ax.set_ylabel(args.ylabel, fontsize=14)
    if args.logscale:
        ax.set_yscale('log')

    ax.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()

