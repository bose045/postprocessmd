import matplotlib.pyplot as plt
import numpy as np
import argparse
import ast

def main():
    # Create the parser
    parser = argparse.ArgumentParser(description='Plot data from a file with optional labels and legends.')
    parser.add_argument('filename', type=str, help='Path to the data file')
    parser.add_argument('columns', type=int, nargs='+', help='A sequence of columns to plot as x1 y1 x2 y2 ...')
    parser.add_argument('--xlabel', type=str, default='X-axis', help='Label for the x-axis')
    parser.add_argument('--ylabel', type=str, default='Y-axis', help='Label for the y-axis')
    parser.add_argument('--legends', type=str, help='List of legends as a string (e.g., \'["Curve 1", "Curve 2"]\')')

    # Parse the arguments
    args = parser.parse_args()

    # Load data from file
    data = np.genfromtxt(args.filename, delimiter=None, skip_header=1)
    data = data[~np.isnan(data).any(axis=1)]

    # Ensure we have an even number of column indices (for pairs)
    if len(args.columns) % 2 != 0:
        raise ValueError('Columns must be in pairs of x and y.')

    # Attempt to parse legends if provided
    if args.legends:
        try:
            legends = ast.literal_eval(args.legends)
            if len(legends) != len(args.columns) // 2:
                raise ValueError('Number of legends must match the number of plots.')
        except:
            raise ValueError('Invalid format for legends. Ensure it is a proper list string, e.g., \'["label1", "label2"]\'.')
    else:
        legends = [f'Plot {i+1}' for i in range(len(args.columns) // 2)]

    # Create the plot
    plt.figure(figsize=(10, 5))
    for i in range(0, len(args.columns), 2):
        x_col = args.columns[i]
        y_col = args.columns[i+1]
        plt.plot(data[:, x_col], data[:, y_col], label=legends[i//2])

    # Setting labels and legend
    plt.xlabel(args.xlabel)
    plt.ylabel(args.ylabel)
    plt.legend()
    plt.title('Plot from Terminal')
    plt.show()

if __name__ == "__main__":
    main()

