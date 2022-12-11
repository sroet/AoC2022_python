import argparse
import time
import copy
import math


def make_monkey(lines):
    for line in lines:
        if "Starting items" in line:
            split = line.split(":")[1].split(",")
            starting_items = [int(i) for i in split]
        elif "Operation" in line:
            split = line.split("=")
            operation = eval(f"lambda old: {split[-1]}")
        elif "Test" in line:
            test = int(line.split()[-1])
        elif "true" in line:
            true_idx = int(line.split()[-1])
        elif "false" in line:
            false_idx = int(line.split()[-1])
    return Monkey(starting_items, operation, test, true_idx, false_idx)


def read_file(fname):
    data = []
    with open(fname, "r") as file:
        temp = []
        for line in file:
            strip = line.strip()
            if strip != "":
                temp.append(strip)
            else:
                data.append(make_monkey(temp))
                temp = []
    if len(temp) > 0:
        data.append(make_monkey(temp))
    return data


class Monkey:
    def __init__(self, starting_items, operation, test, true_idx, false_idx):
        self.items = starting_items.copy()
        self.operation = operation
        self.test = test
        self.true_idx = true_idx
        self.false_idx = false_idx
        self.monkeys = {}
        self.inspect = 0
        self.div = 3
        self.mod = 0

    def turn(self):
        for item in self.items:
            self.inspect += 1
            item = self.operation(item)
            item = item // self.div
            if self.mod and item > self.mod:
                item = item % self.mod
            if item % self.test == 0:
                idx = self.true_idx
            else:
                idx = self.false_idx
            self.monkeys[idx].items.append(item)
        self.items = []


def part_1(data):
    monkeys = dict(enumerate(data))
    for monkey in data:
        monkey.monkeys = monkeys
    for _ in range(20):
        for monkey in data:
            monkey.turn()
    vals = [m.inspect for m in data]
    vals.sort()

    return vals[-1] * vals[-2]


def part_2(data):
    monkeys = dict(enumerate(data))
    mod = math.lcm(*[m.test for m in data])
    for monkey in data:
        monkey.monkeys = monkeys
        monkey.div = 1
        monkey.mod = mod
    for _ in range(10_000):
        for monkey in data:
            monkey.turn()
    vals = [m.inspect for m in data]
    vals.sort()

    return vals[-1] * vals[-2]


def main(fname):
    start = time.time()
    data = read_file(fname)
    total1 = part_1(copy.deepcopy(data))
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
