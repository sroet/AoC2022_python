import argparse
import time as t
from collections import Counter


def read_file(fname):
    walls = set()
    path = set()
    ins = []
    with open(fname, "r") as file:
        instructions = False
        for y, line in enumerate(file):
            if line == "\n":
                instructions = True
                continue
            if instructions is True:
                temp = ""
                for c in line.strip():
                    if c.isnumeric():
                        temp += c
                        continue
                    ins.append(int(temp))
                    ins.append(c)
                    temp = ""
            for x, c in enumerate(line):
                coord = complex(x + 1, y + 1)
                if c == "\n":
                    continue
                if c == ".":
                    path.add(coord)
                elif c == "#":
                    walls.add(coord)
    if temp != "":
        ins.append(int(temp))

    return ins, walls, path


def go_right(num):
    return complex(-num.imag, num.real)


def go_left(num):
    return complex(num.imag, -num.real)


turn = {"R": go_right, "L": go_left}


def part_1(data):
    ins, walls, path = data
    ins = ins[::-1].copy()
    all_coord = walls | path
    start_x = min(i.real for i in path if i.imag == 1)
    start = complex(start_x, 1)
    current_place = start
    direction = complex(1, 0)
    top = round(min(i.imag for i in all_coord))
    bottom = round(max(i.imag for i in all_coord))
    left = round(min(i.real for i in all_coord))
    right = round(max(i.real for i in all_coord))

    top_edges = [
        complex(i, min(j.imag for j in all_coord if j.real == i))
        for i in range(left, right + 1)
    ]
    bottom_edges = [
        complex(i, max(j.imag for j in all_coord if j.real == i))
        for i in range(left, right + 1)
    ]
    left_edges = [
        complex(min(j.real for j in all_coord if j.imag == i), i)
        for i in range(top, bottom + 1)
    ]
    right_edges = [
        complex(max(j.real for j in all_coord if j.imag == i), i)
        for i in range(top, bottom + 1)
    ]

    while ins:
        i = ins.pop()
        if i in turn:
            direction = turn[i](direction)
            continue
        for _ in range(i):
            trial = current_place + direction
            if trial not in all_coord:
                if direction == complex(1, 0):
                    current_edge = right_edges
                    other_edge = left_edges
                elif direction == complex(-1, 0):
                    current_edge = left_edges
                    other_edge = right_edges
                elif direction == complex(0, -1):
                    current_edge = top_edges
                    other_edge = bottom_edges
                elif direction == complex(0, 1):
                    current_edge = bottom_edges
                    other_edge = top_edges
                idx = current_edge.index(current_place)
                trial = other_edge[idx]
            if trial in walls:
                break
            current_place = trial
    dir_cost = 0
    while direction != complex(1, 0):
        dir_cost += 1
        direction = go_left(direction)
    cost = 1000 * current_place.imag + 4 * current_place.real + dir_cost
    return round(cost)


def map_cube(all_coord):
    top = round(min(i.imag for i in all_coord))
    bottom = round(max(i.imag for i in all_coord))
    left = round(min(i.real for i in all_coord))
    right = round(max(i.real for i in all_coord))
    top_edges = [
        complex(i, min(j.imag for j in all_coord if j.real == i) - 1)
        for i in range(left, right + 1)
    ]
    bottom_edges = [
        complex(i, max(j.imag for j in all_coord if j.real == i) + 1)
        for i in range(left, right + 1)
    ]
    left_edges = [
        complex(min(j.real for j in all_coord if j.imag == i) - 1, i)
        for i in range(top, bottom + 1)
    ]
    right_edges = [
        complex(max(j.real for j in all_coord if j.imag == i) + 1, i)
        for i in range(top, bottom + 1)
    ]
    counts = Counter(top_edges + bottom_edges + left_edges + right_edges)
    out = {}
    corners = [key for key, val in counts.items() if val == 2]
    for corner in corners:
        if corner in right_edges:
            direction1 = complex(1, 0)
            face_dir2 = complex(-1, 0)
        else:
            direction1 = complex(-1, 0)
            face_dir2 = complex(1, 0)

        if corner in top_edges:
            direction2 = complex(0, -1)
            face_dir1 = complex(0, 1)
        else:
            direction2 = complex(0, 1)
            face_dir1 = complex(0, -1)
        edge_1 = corner
        edge_2 = corner
        while edge_1 in counts or edge_2 in counts:
            if edge_1 not in counts:
                # Hit an outer corner
                for rot in [go_right, go_left]:
                    trial_dir = rot(direction1)
                    if edge_1 + trial_dir in counts:
                        direction1 = trial_dir
                        face_dir1 = rot(face_dir1)
                        edge_1 += direction1
                        break
            if edge_2 not in counts:
                # Hit an outer corner
                for rot in [go_right, go_left]:
                    trial_dir = rot(direction2)
                    if edge_2 + trial_dir in counts:
                        direction2 = trial_dir
                        face_dir2 = rot(face_dir2)
                        edge_2 += direction2
                        break
            out[(edge_1, -face_dir1)] = (edge_2 + face_dir2, face_dir2)
            out[(edge_2, -face_dir2)] = (edge_1 + face_dir1, face_dir1)
            edge_1 += direction1
            edge_2 += direction2
    return out


def part_2(data):
    ins, walls, path = data
    ins = ins[::-1].copy()
    all_coord = walls | path
    edges = map_cube(all_coord)
    start_x = min(i.real for i in path if i.imag == 1)
    start = complex(start_x, 1)
    current_place = start
    direction = complex(1, 0)

    while ins:
        i = ins.pop()
        if i in turn:
            direction = turn[i](direction)
            continue
        for _ in range(i):
            trial = current_place + direction
            trial_direction = direction
            if trial not in all_coord:
                trial, trial_direction = edges[trial, direction]
            if trial in walls:
                break
            current_place = trial
            direction = trial_direction
    dir_cost = 0
    while direction != complex(1, 0):
        dir_cost += 1
        direction = go_left(direction)
    cost = 1000 * current_place.imag + 4 * current_place.real + dir_cost
    return round(cost)


def main(fname):
    start = t.time()
    data = read_file(fname)
    total1 = part_1(data)
    t2 = t.time()
    total2 = part_2(data)
    t3 = t.time()
    print(f"Part 1: {total1}")
    print(f"time 1: {t2-start}")
    print(f"Part 2: {total2}")
    print(f"time 2: {t3-t2}")
    print(f"Ran in {t.time()-start} s")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    filename = args.filename
    main(filename)
