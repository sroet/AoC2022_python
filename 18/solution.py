import argparse
import time
from collections import Counter


def read_file(fname):
    data = []
    with open(fname, "r") as file:
        for line in file:
            strip = line.strip()
            if strip != "":
                data.append(tuple(int(i) for i in strip.split(",")))
    return set(data)


directions = [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]


def part_1(data):
    out = 0
    surfaces = []
    for x, y, z in data:
        temp = 0
        for dx, dy, dz in directions:
            new = (x + dx, y + dy, z + dz)
            if new in data:
                temp += 1
            else:
                surfaces.append(new)
        out += 6 - temp
    surfaces = Counter(surfaces)
    return out, surfaces


def part_2(data, surfaces):
    out = 0
    options = [key for key, val in surfaces.items() if val != 6]
    xs, ys, zs = zip(*surfaces)
    min_x = min(xs)
    max_x = max(xs)
    min_y = min(ys)
    max_y = max(ys)
    min_z = min(zs)
    max_z = max(zs)
    outsides = set()
    insides = set()
    for option in options:
        outside = False
        todo = [option]
        done = set()
        done.add(option)
        while todo:
            x, y, z = todo.pop()
            if (
                x in [min_x, max_x]
                or y in [min_y, max_y]
                or z in [min_z, max_z]
                or (x, y, z) in outsides
            ):
                outside = True
                outsides.add(option)
                break
            if (x, y, z) in insides:
                break
            for dx, dy, dz in directions:
                new = (x + dx, y + dy, z + dz)
                if new in data or new in done:
                    continue
                done.add(new)
                todo.append(new)

        if not outside:
            insides.add(option)
            continue
        out += surfaces[option]
    return out


def main(fname):
    start = time.time()
    data = read_file(fname)
    total1, surfaces = part_1(data)
    total2 = part_2(data, surfaces)
    print(f"Part 1: {total1}")
    print(f"Part 2: {total2}")
    print(f"Ran in {time.time()-start} s")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    filename = args.filename
    main(filename)
