import argparse
import time as t
from collections import deque
import itertools
from heapq import heappush, heappop


def read_file(fname):
    left = set()
    right = set()
    up = set()
    down = set()
    start = None
    end = None
    with open(fname, "r") as file:
        for y, line in enumerate(file):
            strip = line.strip()
            if strip != "":
                for x, c in enumerate(strip):
                    coord = complex(x, y)
                    if start is None and c == ".":
                        start = coord
                    if c == "<":
                        left.add(coord)
                    elif c == ">":
                        right.add(coord)
                    elif c == "v":
                        down.add(coord)
                    elif c == "^":
                        up.add(coord)
                    elif c == ".":
                        end = coord
    return (left, up, right, down), start, end, x, y


UP = complex(0, -1)
DOWN = complex(0, 1)
RIGHT = complex(1, 0)
LEFT = complex(-1, 0)
NULL = 0


def part_1_v1(data):
    (left, up, right, down), start, end, max_x, max_y = data
    steps = 0
    coord = start
    queue = deque([(steps, start, left, up, right, down)])
    while coord != end:
        steps, coord, left, up, right, down = queue.popleft()
        # figure out next state
        left = set(
            i + LEFT if (i + LEFT).real > 0 else complex(max_x - 1, i.imag)
            for i in left
        )
        right = set(
            i + RIGHT if (i + RIGHT).real < max_x else complex(1, i.imag) for i in right
        )
        up = set(
            i + UP if (i + UP).imag > 0 else complex(i.real, max_y - 1) for i in up
        )
        down = set(
            i + DOWN if (i + DOWN).imag < max_y else complex(i.real, 1) for i in down
        )
        blizzards = left | right | up | down
        for direction in [UP, DOWN, LEFT, RIGHT, NULL]:
            next_coord = coord + direction
            if next_coord in blizzards:
                continue
            if next_coord == end:
                return steps + 1
            if next_coord.real < 1 or next_coord.real > max_x - 1:
                continue
            if (
                next_coord.imag < 1 and next_coord != start
            ) or next_coord.imag > max_y - 1:
                continue
            queue.append((steps + 1, next_coord, left, up, right, down))


def sort_complex(inp):
    return inp.real + inp.imag * 1000


def make_hashable(inp):
    temp = list(inp)
    temp.sort(key=sort_complex)
    return tuple(temp)


def parts(data):
    (left, up, right, down), start, end, max_x, max_y = data

    steps, (left, up, right, down) = search(
        ((left, up, right, down), start, end, max_x, max_y)
    )
    total1 = steps
    total2 = steps
    steps, (left, up, right, down) = search(
        ((left, up, right, down), end, start, max_x, max_y)
    )
    total2 += steps
    steps, (left, up, right, down) = search(
        ((left, up, right, down), start, end, max_x, max_y)
    )
    total2 += steps
    return total1, total2


def search(data):
    (left, up, right, down), start, end, max_x, max_y = data
    # Taken from heapq docs:
    pq = []  # list of entries arranged in a heap
    entry_finder = {}  # mapping of tasks to entries
    REMOVED = "<removed-task>"  # placeholder for a removed task
    counter = itertools.count()  # unique sequence count

    def add_task(task, priority=0):
        "Add a new task or update the priority of an existing task"
        if task in entry_finder:
            if entry_finder[task][-1][0] <= task[0]:
                return
            remove_task(task)
        count = next(counter)
        entry = [priority, count, task]
        entry_finder[task] = entry
        heappush(pq, entry)

    def remove_task(task):
        "Mark an existing task as REMOVED.  Raise KeyError if not found."
        entry = entry_finder.pop(task)
        entry[-1] = REMOVED

    def pop_task():
        "Remove and return the lowest priority task. Raise KeyError if empty."
        while pq:
            priority, count, task = heappop(pq)
            if task is not REMOVED:
                del entry_finder[task]
                return task
        raise KeyError("pop from an empty priority queue")

    ### strart own code ###
    def A_prio(steps, coord):
        temp = steps
        temp += abs(coord.real - end.real)
        temp += abs(coord.imag - end.imag)
        return temp

    steps = 0
    coord = start
    prio = A_prio(steps, coord)
    add_task(
        (
            steps,
            start,
            make_hashable(left),
            make_hashable(up),
            make_hashable(right),
            make_hashable(down),
        ),
        prio,
    )
    while coord != end:
        steps, coord, left, up, right, down = pop_task()
        # figure out next state
        left = set(
            i + LEFT if (i + LEFT).real > 0 else complex(max_x - 1, i.imag)
            for i in left
        )
        right = set(
            i + RIGHT if (i + RIGHT).real < max_x else complex(1, i.imag) for i in right
        )
        up = set(
            i + UP if (i + UP).imag > 0 else complex(i.real, max_y - 1) for i in up
        )
        down = set(
            i + DOWN if (i + DOWN).imag < max_y else complex(i.real, 1) for i in down
        )
        blizzards = left | right | up | down
        for direction in [UP, DOWN, LEFT, RIGHT, NULL]:
            next_coord = coord + direction
            if next_coord in blizzards:
                continue
            if next_coord == end:
                return steps + 1, (left, up, right, down)
            if next_coord.real < 1 or next_coord.real > max_x - 1:
                continue
            if next_coord != start and (
                next_coord.imag < 1 or next_coord.imag > max_y - 1
            ):
                continue
            prio = A_prio(steps + 1, next_coord)
            add_task(
                (
                    steps + 1,
                    next_coord,
                    make_hashable(left),
                    make_hashable(up),
                    make_hashable(right),
                    make_hashable(down),
                ),
                prio,
            )


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
