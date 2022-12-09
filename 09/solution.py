import argparse
import time
from collections import Counter

DIRS = {"R": (1, 0), "L": (-1, 0), "U": (0, 1), "D": (0, -1)}


def read_file(fname):
    data = []
    with open(fname, "r") as file:
        for line in file:
            strip = line.strip()
            split = strip.split()
            if strip != "":
                data.append((split[0], int(split[1])))
    return data


def update_tail(head_x, head_y, tail_x, tail_y):
    if head_x > tail_x + 1:
        # right
        tail_x += 1
        if head_y > tail_y:
            # up-right
            tail_y += 1
        elif head_y < tail_y:
            # down-right
            tail_y -= 1
    elif head_x < tail_x - 1:
        # left
        tail_x -= 1
        if head_y > tail_y:
            # up-left
            tail_y += 1
        elif head_y < tail_y:
            # down-left
            tail_y -= 1
    elif head_y > tail_y + 1:
        # up
        tail_y += 1
        if head_x > tail_x:
            # up right
            tail_x += 1
        elif head_x < tail_x:
            # up left
            tail_x -= 1
    elif head_y < tail_y - 1:
        # down
        tail_y -= 1
        if head_x > tail_x:
            # down right
            tail_x += 1
        elif head_x < tail_x:
            # down left
            tail_x -= 1
    return tail_x, tail_y


def part_1(data):
    head_x, head_y = (0, 0)
    tail_x, tail_y = (0, 0)
    counts = Counter()
    counts.update([(tail_x, tail_y)])
    for direction, n in data:
        xs, ys = DIRS[direction]
        for _ in range(n):
            head_x += xs
            head_y += ys
            tail_x, tail_y = update_tail(head_x, head_y, tail_x, tail_y)
            counts.update([(tail_x, tail_y)])
    return len(counts)


def part_2(data):
    knots = [(0, 0) for _ in range(10)]
    counts = Counter()
    counts.update([knots[-1]])
    for direction, n in data:
        xs, ys = DIRS[direction]
        for _ in range(n):
            head_x, head_y = knots[0]
            head_x += xs
            head_y += ys
            knots[0] = (head_x, head_y)
            for i, knot in enumerate(knots[1:]):
                temp_head_x, temp_head_y = knots[i]  # i because the we start at item 1
                temp_tail_x, temp_tail_y = knot
                tail_x, tail_y = update_tail(
                    temp_head_x, temp_head_y, temp_tail_x, temp_tail_y
                )
                knots[i + 1] = (tail_x, tail_y)
            counts.update([knots[-1]])
    return len(counts)


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
