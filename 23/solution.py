import argparse
import time as t
from collections import deque


def read_file(fname):
    elves = set()
    with open(fname, "r") as file:
        for y, line in enumerate(file):
            strip = line.strip()
            if strip != "":
                for x, c in enumerate(strip):
                    if c == "#":
                        elves.add(complex(x, y))
    return elves, x, y


N = complex(0, -1)
S = complex(0, 1)
E = complex(1, 0)
W = complex(-1, 0)
NE = N + E
NW = N + W
SE = S + E
SW = S + W


def resolve_conflicts(dct):
    for key, val in dct.items():
        if len(val) == 1:
            yield key
        else:
            for v in val:
                yield v


def print_state(dct):
    min_y, min_x = float("inf"), float("inf")
    max_y, max_x = float("-inf"), float("-inf")
    for val in dct:
        imag = val.imag
        real = val.real
        if imag < min_y:
            min_y = imag
        if imag > max_y:
            max_y = imag
        if real < min_x:
            min_x = real
        if real > max_x:
            max_x = real
    min_x = round(min_x)
    max_x = round(max_x)
    min_y = round(min_x)
    max_y = round(max_x)

    for y in range(min_y, max_y + 1):
        print(
            "".join(
                ["#" if complex(x, y) in dct else "." for x in range(min_x, max_x + 1)]
            )
        )


def parts(data):
    current_step, max_x, max_y = data
    # NW, N, NE, E, SE, S, SW, W
    loops = deque([((0, 1, 2), N), ((4, 5, 6), S), ((6, 7, 0), W), ((2, 3, 4), E)])
    j = 0
    moved = True
    while moved:
        j += 1
        next_step = {}
        moved = False
        for elf in current_step:
            checks = [elf + i not in current_step for i in [NW, N, NE, E, SE, S, SW, W]]
            if all(checks):
                direction = 0
            else:
                for indices, dirs in loops:
                    if all(checks[i] for i in indices):
                        moved = True
                        direction = dirs
                        break
                else:
                    direction = 0
            temp = next_step.get(elf + direction, [])
            temp.append(elf)
            next_step[elf + direction] = temp
        if not moved:
            break
        current_step = set(key for key in resolve_conflicts(next_step))
        loops.rotate(-1)
        if j == 10:
            min_y, min_x = float("inf"), float("inf")
            max_y, max_x = float("-inf"), float("-inf")
            for val in current_step:
                imag = val.imag
                real = val.real
                if imag < min_y:
                    min_y = imag
                if imag > max_y:
                    max_y = imag
                if real < min_x:
                    min_x = real
                if real > max_x:
                    max_x = real
            total1 = (max_y - min_y + 1) * (max_x - min_x + 1) - len(current_step)
    return total1, j


def main(fname):
    start = t.time()
    data = read_file(fname)
    total1, total2 = parts(data)
    print(f"Part 1: {total1}")
    print(f"Part 2: {total2}")
    print(f"Ran in {t.time()-start} s")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    filename = args.filename
    main(filename)
