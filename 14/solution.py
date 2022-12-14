import argparse
import time
import numpy as np


def read_file(fname):
    data = []
    with open(fname, "r") as file:
        for line in file:
            temp = []
            strip = line.strip()
            if strip != "":
                for point in strip.split("->"):
                    temp.append(tuple(int(i) for i in point.split(",")))
            data.append(temp)
    return data


def create_arr(data):
    min_x = min(i[0] for j in data for i in j)
    max_x = max(i[0] for j in data for i in j)
    max_y = max(i[1] for j in data for i in j)
    arr = np.zeros((max_y + 1, max_x - min_x + 1))
    for line in data:
        temp = (i for i in line)
        x, y = next(temp)
        for nx, ny in temp:
            if x < nx:
                arr[y, x - min_x : nx - min_x + 1] = 1
            elif x > nx:
                arr[y, nx - min_x : x - min_x + 1] = 1
            elif y < ny:
                arr[y : ny + 1, x - min_x] = 1
            elif y > ny:
                arr[ny : y + 1, x - min_x] = 1
            else:
                raise ValueError("this should not happen")
            x, y = nx, ny
    return arr, min_x


def part_1(data):
    arr, min_x = create_arr(data)

    total = 0
    start = (0, 500 - min_x)
    stack = []
    cy, cx = start
    while cy < arr.shape[0] and 0 <= cx < arr.shape[1]:
        # free fall
        if cy == arr.shape[0] - 1:
            break
        if arr[cy + 1][cx] == 0:
            stack.append((cy, cx))
            cy += 1
            continue
        # go left
        if cx == 0:
            break
        if arr[cy + 1][cx - 1] == 0:
            stack.append((cy, cx))
            cy += 1
            cx -= 1
            continue
        # go right
        if cx == arr.shape[1] - 1:
            break
        if arr[cy + 1][cx + 1] == 0:
            stack.append((cy, cx))
            cy += 1
            cx += 1
            continue
        # settle
        arr[cy][cx] = 2
        total += 1
        if not stack:
            # needed for part 2
            break
        cy, cx = stack.pop()
    return total


def part_2(data):
    min_x = min(i[0] for j in data for i in j)
    max_x = max(i[0] for j in data for i in j)
    max_y = max(i[1] for j in data for i in j)

    # assume max a triangle
    max_y += 2
    min_x = min(500 - max_y, min_x)
    max_x = max(500 + max_y, max_x)
    data.append([(min_x, max_y), (max_x + 1, max_y)])
    return part_1(data)


def main(fname):
    start = time.time()
    data = read_file(fname)
    total_1 = part_1(data)
    total_2 = part_2(data)
    print(f"Part 1: {total_1}")
    print(f"Part 2: {total_2}")
    print(f"Ran in {time.time()-start} s")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    filename = args.filename
    main(filename)
