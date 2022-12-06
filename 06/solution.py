import argparse
import time


def read_file(fname):
    data = []
    with open(fname, "r") as file:
        for line in file:
            strip = line.strip()
            if strip != "":
                data.append(strip)
    return data


def parts(line, num=4):
    chars = [(i for i in line[j:]) for j in range(num)]
    for i, tup in enumerate(zip(*chars)):
        if len(set(tup)) == num:
            return i + num


def main(fname):
    start = time.time()
    data = read_file(fname)
    for line in data:
        total1 = parts(line, 4)
        total2 = parts(line, 14)
        print(f"Part 1: {total1}")
        print(f"Part 2: {total2}")
    print(f"Ran in {time.time()-start} s")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    filename = args.filename
    main(filename)
