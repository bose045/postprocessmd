import matplotlib.pyplot as plt
import numpy as np
import argparse
import pandas as pd

import pandas as pd

def parse_data_segments(filename, columns):
    segments = []
    with open(filename, 'r') as file:
        buffer = []
        headers = None
        collecting = False
        line_counter = 0  # To help identify the exact line being processed

        for line in file:
            line_counter += 1
            parts = ' '.join(line.strip().split()).split()
            
            if all(col in parts for col in columns):  # Header line check
                header_map = {col: parts.index(col) for col in columns}
                headers = parts
                collecting = True
                print(f"Starting data collection at line {line_counter}: {line.strip()}")
                continue

            if collecting:
                if (len(parts) == len(headers) and all(is_float(part) for part in parts)):
                    selected_data = [parts[header_map[col]] for col in columns]
                    buffer.append(selected_data)
                else:
                    print(f"Non-data line or format mismatch at line {line_counter}: {line.strip()}")
                    if buffer:
                        segments.append(pd.DataFrame(buffer, columns=columns))
                        print(f"Ending data collection at line {line_counter}: {line.strip()} with {len(buffer)} rows collected")
                        buffer = []
                    collecting = False

        if buffer:
            segments.append(pd.DataFrame(buffer, columns=columns))
            print(f"Ending data collection at EOF with {len(buffer)} rows collected")

    return segments

def is_float(element):
    try:
        float(element)
        return True
    except ValueError:
        return False



def main():
    parser = argparse.ArgumentParser(description='Plot data segments from a log file with flexible instance selection.')
    parser.add_argument('filename', type=str, help='Path to the data file')
    parser.add_argument('--instance', type=str, default='first', help='Instance to plot: "first", "last" or a number (1-based)')
    parser.add_argument('--columns', nargs='+', help='Column names to plot as x y. First one is x-axis, followed by one or more y-axis columns.')
    parser.add_argument('--xlabel', type=str, default='X-axis', help='Label for the x-axis')
    parser.add_argument('--ylabel', type=str, default='Y-axis', help='Label for the y-axis')
    parser.add_argument('--legends', type=str, help='List of legends as a string (e.g., \'["Curve 1", "Curve 2"]\')')
    parser.add_argument('--logscale', action='store_true', help='Set log scale for the y-axis')
    parser.add_argument('--outfile', type=str, default='plot.png', help='Output file for the plot (default: plot.png)')

    args = parser.parse_args()

    if not args.columns:
        print("Error: No columns specified for plotting.")
        return

    # Extract data segments
    segments = parse_data_segments(args.filename, args.columns)
    print(f"Total data segments found: {len(segments)}")

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

