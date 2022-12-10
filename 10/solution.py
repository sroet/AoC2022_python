import argparse
import time
from collections import Counter


def read_file(fname):
    data = []
    with open(fname, "r") as file:
        for line in file:
            strip = line.strip()
            split = strip.split()
            if strip != "":
                func = split[0]
                val = [int(i) for i in split[1:]]
                data.append((func, val))
    return data


class Clock:
    def __init__(self):
        self.cycle = 0
        self.p1_output = 0
        self.register = [1]
        self.p2_output = []
        self.p2_row = ""

    def tick(self):
        self.cycle += 1
        point = self.cycle % 40 - 1
        if self.register[0] - 1 <= point <= self.register[0] + 1:
            self.p2_row += "#"
        else:
            self.p2_row += " "
        if self.cycle % 40 == 20:
            self.p1_output += self.register[0] * self.cycle
        if self.cycle % 40 == 0:
            self.p2_output.append(self.p2_row)
            self.p2_row = ""


def noop(clock):
    clock.tick()


def addx(clock, val):
    clock.tick()
    clock.tick()
    clock.register[0] += int(val)


FUNCS = {"noop": noop, "addx": addx}


def parts(data):
    clock = Clock()
    for func, val in data:
        f = FUNCS[func]
        f(clock, *val)
        if clock.cycle > 240:
            break
    return clock


def main(fname):
    start = time.time()
    data = read_file(fname)
    clock = parts(data)
    print(f"Part 1: {clock.p1_output}")
    print("Part 2:")
    for row in clock.p2_output:
        print(row)
    print(f"Ran in {time.time()-start} s")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    filename = args.filename
    main(filename)
