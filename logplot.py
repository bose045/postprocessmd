import argparse
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def parse_data_segments(filename, columns):
    segments = []
    with open(filename, 'r') as file:
        buffer = []
        headers = None
        collecting = False

        for line in file:
            parts = ' '.join(line.strip().split()).split()

            if all(col in parts for col in columns):
                header_map = {col: parts.index(col) for col in columns}
                headers = parts
                collecting = True
                continue

            if collecting:
                if (len(parts) == len(headers) and all(is_float(part) for part in parts)):
                    selected_data = [float(parts[header_map[col]]) for col in columns]
                    buffer.append(selected_data)
                else:
                    if buffer:
                        segments.append(pd.DataFrame(buffer, columns=columns))
                        buffer = []
                    collecting = False

        if buffer:
            segments.append(pd.DataFrame(buffer, columns=columns))

    return segments

def is_float(element):
    try:
        float(element)
        return True
    except ValueError:
        return False

def apply_operations(data, operations):
    local_context = data.to_dict('series')
    local_context['np'] = np

    for operation in operations:
        lhs, rhs = operation.split('=')
        lhs = lhs.strip()
        rhs = rhs.strip()

        try:
            data[lhs] = eval(rhs, {"__builtins__": None}, local_context)
        except Exception as e:
            print(f"Error evaluating expression '{rhs}': {e}")

    return data

def main():
    parser = argparse.ArgumentParser(description='Plot data segments from a log file with flexible instance selection.')
    parser.add_argument('filename', type=str, help='Path to the data file')
    parser.add_argument('--instance', type=str, default='first', help='Instance to plot: "first", "last", or a number (1-based)')
    parser.add_argument('--columns', nargs='+', help='Column names to plot as x y. First one is x-axis, followed by one or more y-axis columns.')
    parser.add_argument('--operations', nargs='+', help='Math operations to apply on columns, e.g., "new_col=x1+x2"')
    parser.add_argument('--xlabel', type=str, default='X-axis', help='Label for the x-axis')
    parser.add_argument('--ylabel', type=str, default='Y-axis', help='Label for the y-axis')
    parser.add_argument('--legends', type=str, help='List of legends as a string (e.g., \'["Curve 1", "Curve 2"]\')')
    parser.add_argument('--logscale', action='store_true', help='Set log scale for the y-axis')
    parser.add_argument('--outfile', type=str, default='plot.png', help='Output file for the plot (default: plot.png)')
    args = parser.parse_args()

    segments = parse_data_segments(args.filename, args.columns)
    print(f"Total data segments found: {len(segments)}")

    if not segments:
        print("No valid data segments found.")
        return

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

    if args.operations:
        data = apply_operations(data, args.operations)

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
    plt.savefig(args.outfile)
    plt.show()

if __name__ == "__main__":
    main()

