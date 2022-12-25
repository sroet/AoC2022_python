import argparse
import time as t
from collections import deque
import itertools
from heapq import heappush, heappop


def read_file(fname):
    data = 0
    with open(fname, "r") as file:
        for line in file:
            strip = line.strip()
            if strip != "":
                for x, c in enumerate(strip[::-1]):
                    if c == "-":
                        c = "-1"
                    elif c == "=":
                        c = "-2"
                    c = int(c)
                    data += 5**x * c

    return data


snafu = {0: "0", 1: "1", 2: "2", 3: "=", 4: "-"}


def add_one(data):
    i = len(data) - 1
    while i >= 0:
        data[i] += 1
        if data[i] == 5:
            data[i] = 0
        if data[i] != 3:
            break
        i -= 1
    else:
        return [1] + data
    return data


def parts(data):
    out_vals = []
    current_root = 0
    while data // (5**current_root) != 0:
        current_root += 1
    current_root -= 1
    temp = []
    while current_root >= 0:
        div, data = divmod(data, 5**current_root)
        temp.append(0)
        for _ in range(div):
            temp = add_one(temp)
        current_root -= 1
    return "".join(snafu[i] for i in temp)


def main(fname):
    start = t.time()
    data = read_file(fname)
    total1 = parts(data)
    print(f"Part 1: {total1}")
    print(f"Ran in {t.time()-start} s")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    filename = args.filename
    main(filename)
