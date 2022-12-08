import argparse
import time
import numpy as np


def read_file(fname):
    data = []
    with open(fname, "r") as file:
        for line in file:
            strip = line.strip()
            if strip != "":
                data.append([int(i) for i in strip])
    return np.array(data)


def part_1(data):
    total = data.shape[0] * 2 + data.shape[1] * 2 - 4
    for i, row in enumerate(data[1:-1]):
        for j, val in enumerate(row[1:-1]):
            if (
                np.all(row[: j + 1] < val)
                or np.all(row[j + 2 :] < val)
                or np.all(data[: i + 1, j + 1] < val)
                or np.all(data[i + 2 :, j + 1] < val)
            ):
                total += 1
    return total


def part_2(data):
    max_val = float("-inf")
    for i, row in enumerate(data):
        for j, val in enumerate(row):
            total = 1
            ranges = []
            if i == 0 or i == len(data) - 1 or j == 0 or j == len(row) - 1:
                # one distance is 0, so skip
                continue
            # up
            ranges.append(data[i - 1 :: -1, j])
            # down
            ranges.append(data[i + 1 :, j])
            # left
            ranges.append(row[j - 1 :: -1])
            # right
            ranges.append(row[j + 1 :])
            for rang in ranges:
                temp = 1
                for val2 in rang:
                    if val2 >= val:
                        break
                    temp += 1
                else:
                    # correct overcounting of the edges
                    temp -= 1
                total *= temp
            if total > max_val:
                max_val = total
    return max_val


def main(fname):
    start = time.time()
    data = read_file(fname)
    total1 = part_1(data)
    total2 = part_2(data)
    print(f"Part 1: {total1}")
    print(f"Part 2: {total2}")
    print(f"Ran in {time.time()-start} s")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    filename = args.filename
    main(filename)
