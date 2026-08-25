import sys
import numpy
import matplotlib.pyplot as pyplot


def load_data(filename):
    """
    Loads the generation times from the supplied file
    params:
        filename (str) - The name of the data file
    returns:
        times (list(floats)) - The data from the file
    """
    times = []
    with open(filename, "r") as ifp:
        for line in ifp.readlines():
            times.append(float(line.strip()))

    return times


def main():
    """
    The main method. This is a simple file to allow you to make a box plot of generation times
      This served as the base for my private file for more complex generations
    returns:
        None
    """

    if len(sys.argv) < 2:
        print("USAGE: python3 usage.py <filename>")
        exit(-1)

    times = load_data(sys.argv[1].strip())
    print(f"Generation Time Stats:\n\n\tMean: {numpy.mean(times)}\n\tMedian: {numpy.median(times)}\n\tStd Dev: {numpy.std(times)}\n\tMin: {numpy.min(times)}\n\tMax: {numpy.max(times)}\n")
    pyplot.boxplot(times, vert=False)
    pyplot.show()


if __name__ == "__main__":
    main()