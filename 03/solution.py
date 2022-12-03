import argparse
import itertools as itt
import time

ALPHABET = "abcdefghijklmnopqrstuvwxyz"
ALPHABETU = ALPHABET.upper()
priorities = {e: i + 1 for i, e in enumerate(itt.chain(ALPHABET, ALPHABETU))}


def read_file(fname):
    out = []
    with open(fname, "r") as file:
        for line in file:
            line = line.strip()
            half = len(line) // 2
            if len(line) > 0:
                out.append((line[:half], line[half:]))
    return out


def part_1(data):
    total1 = 0
    for compart1, compart2 in data:
        overlap = set(compart1) & set(compart2)
        item = overlap.pop()
        total1 += priorities[item]
    return total1


def part_2(data):
    total2 = 0
    for (c11, c12), (c21, c22), (c31, c32) in zip(data[::3], data[1::3], data[2::3]):
        ru1 = set(c11) | set(c12)
        ru2 = set(c21) | set(c22)
        ru3 = set(c31) | set(c32)
        overlap = ru1 & ru2 & ru3
        item = overlap.pop()
        total2 += priorities[item]
    return total2


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
