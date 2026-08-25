import re
import sys


def filter_gpu(filename):
    gpu_usage = []
    gpu_memory = []
    with open(filename, "r") as ifp:
        for line in ifp.readlines():
            if "55W" in line:
                gpu_usage.append(re.search("[0-9]+%", line).group()[:-1])
            elif "python3" in line:
                gpu_memory.append(re.search("[0-9]+M", line).group()[:-1])

    return gpu_usage, gpu_memory


def filter_cpu(filename):
    cpu_usage = []
    cpu_memory = []
    with open(filename, "r") as ifp:
        for line in ifp.readlines():
            if "grep" not in line:
                line = line.split(" ")
                line = list(filter(lambda x: x != "", line))
                cpu_usage.append(line[2])
                cpu_memory.append(line[3])
                
    return cpu_usage, cpu_memory


def main():

    if len(sys.argv) < 2:
        print("USAGE: python3 clean_data.py <cpu_data_file> <gpu_data_file>")
        exit(-1)

    cpu_usage, cpu_memory = filter_cpu(sys.argv[1].strip())
    with open("cleaned_cpu.txt", "w") as ofp:
        for i in range(len(cpu_usage)):
            ofp.write(f"{cpu_usage[i]}, {cpu_memory[i]}\n")

    try:
        gpu_usage, gpu_memory = filter_gpu(sys.argv[2].strip())
        with open("cleaned_gpu.txt", "w") as ofp:
            for i in range(len(gpu_usage)):
                ofp.write(f"{gpu_usage[i]}, {gpu_memory[i]}\n")
    except:
        pass
    

if __name__ == "__main__":
    main()