import argparse
import time
import copy


def read_file(fname):
    start = []
    moves = []
    with open(fname, "r") as file:
        temp = []
        for line in file:
            if "[" not in line:
                # full start found
                break
            temp.append([i for i in line[1::4]])
        stacks = int(line.strip().split()[-1])
        for _ in range(stacks):
            start.append(list())
        for line in temp[::-1]:
            for i, crate in enumerate(line):
                if crate != " ":
                    start[i].append(crate)
        # read the moves
        for line in file:
            temp = line.strip().split()
            if len(temp) > 0:
                moves.append((int(temp[1]), int(temp[3]) - 1, int(temp[-1]) - 1))
    return start, moves


def part_1(data):
    start, moves = data
    state = copy.deepcopy(start)
    for times, start, end in moves:
        for _ in range(times):
            state[end].append(state[start].pop())
    return "".join(i.pop() for i in state)


def part_2(data):
    start, moves = data
    state = copy.deepcopy(start)
    for times, start, end in moves:
        temp = []
        for _ in range(times):
            temp.append(state[start].pop())
        for crate in temp[::-1]:
            state[end].append(crate)
    return "".join(i.pop() for i in state)


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
