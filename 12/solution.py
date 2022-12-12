import argparse
import time
from heapq import heappush, heappop

ALPHABET = "abcdefghijklmnopqrstuvwxyz"


def read_file(fname):
    heights = []
    start = None
    end = None
    with open(fname, "r") as file:
        temp = []
        for row, line in enumerate(file):
            temp = []
            strip = line.strip()
            if strip != "":
                for col, char in enumerate(strip):
                    if char == "S":
                        start = (row, col)
                        temp.append(0)
                    elif char == "E":
                        end = (row, col)
                        temp.append(ALPHABET.index("z"))
                    else:
                        temp.append(ALPHABET.index(char))
            heights.append(temp)
    return heights, start, end


def part_1(data):
    heights, start, end = data
    visited = set()
    todo = set()
    todo.add(start)
    current = start
    steps = 0
    queue = []
    heappush(queue, (0, start))
    dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    while current != end:
        steps, current = heappop(queue)
        if current in visited:
            continue
        visited.add(current)
        todo.remove(current)
        x, y = current
        height = heights[x][y]
        for xs, ys in dirs:
            next_x = x + xs
            next_y = y + ys
            if next_y < 0 or next_y >= len(heights[0]):
                continue
            if next_x < 0 or next_x >= len(heights):
                continue
            if (next_x, next_y) in visited or (next_x, next_y) in todo:
                continue
            next_height = heights[next_x][next_y]
            if next_height - height > 1:
                continue
            next_steps = steps + 1
            heappush(queue, (next_steps, (next_x, next_y)))
            todo.add((next_x, next_y))
    return steps


def part_2(data):
    # invert logic, start at end and find shortest path to any low point
    heights, _, end = data
    visited = set()
    todo = set()
    todo.add(end)
    current = end
    steps = 0
    queue = []
    heappush(queue, (0, end))
    dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    while True:
        steps, current = heappop(queue)
        if current in visited:
            continue
        visited.add(current)
        todo.remove(current)
        x, y = current
        height = heights[x][y]
        if height == 0:
            return steps
        for xs, ys in dirs:
            next_x = x + xs
            next_y = y + ys
            if next_y < 0 or next_y >= len(heights[0]):
                continue
            if next_x < 0 or next_x >= len(heights):
                continue
            if (next_x, next_y) in visited or (next_x, next_y) in todo:
                continue
            next_height = heights[next_x][next_y]
            if next_height - height < -1:
                continue
            next_steps = steps + 1
            heappush(queue, (next_steps, (next_x, next_y)))
            todo.add((next_x, next_y))


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
