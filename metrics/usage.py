import sys
import numpy
import matplotlib.pyplot as pyplot


def load_data(filename):
    """
    Loads data from the supplied file
    params:
        filename (str) - The data file to load
    returns:
        usage (list(float)) - A list of CPU/GPU usage measurements
        memory (list(float)) - A list of Memory usage measurments
    """
    usage = []
    memory = []
    with open(filename, "r") as ifp:
        for line in ifp.readlines():
            line = line.split(",")
            usage.append(float(line[0].strip()))
            memory.append(float(line[1].strip()))

    return usage, memory


def print_stats(type, data):
    """
    Prints out the statistics of the supplied data
    params:
        type (bool) - Whether we are processing core or memory usage data
        data (list(float)) - The data to work on
    returns:
        None
    """
    if type:
        print("Usage Stats:\n")
    else:
        print("Memory Stats:\n")

    print(f"\tMean: {numpy.mean(data)}\n\tMedian: {numpy.median(data)}\n\tStd Dev: {numpy.std(data)}\n\tMin: {numpy.min(data)}\n\tMax: {numpy.max(data)}\n")


def main():
    """
    The mian method. Another file to make individual graphs of test data. 
      Serves as the baseline for my actual graph generation files
    returns:
        None
    """

    if len(sys.argv) < 2:
        print("USAGE: python3 usage.py <filename>")
        exit(-1)

    usage_data, memory_data = load_data(sys.argv[1].strip())
    print_stats(True, usage_data)
    print_stats(False, memory_data)

    for i in range(2):
        figure, axis = pyplot.subplots()
        axis.plot(range(len(usage_data)), usage_data if i == 0 else memory_data, linewidth=2)

        pyplot.xlabel("Time (s)")
        pyplot.ylabel("Percentage")
        pyplot.title("CPU Usage" if i == 0 else "Memory Usage")
        # pyplot.title("GPU Usage" if i == 0 else "GPU Memory Usage")

        pyplot.show()



if __name__ == "__main__":
    main()