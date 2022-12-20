import argparse
import time as t


def read_file(fname):
    data = []
    with open(fname, "r") as file:
        for line in file:
            strip = line.strip()
            if strip != "":
                data.append((int(strip), 0))
    return data


def part_1(data):
    i = 0
    len_data = len(data)
    while i < len_data:
        if data[i][1]:
            i += 1
            continue
        val, _ = data.pop(i)
        new_place = (i + val) % (len_data - 1)
        if new_place == 0:
            new_place = len_data
        data.insert(new_place, (val, 1))
        if new_place > i or 0 > new_place > i - len_data:
            continue
        i += 1
    total = 0
    i_0 = data.index((0, 1))
    for i in [1000, 2000, 3000]:
        total += data[(i + i_0) % len_data][0]
    return total


def part_2(data):
    new_data = []
    len_data = len(data)
    for i, e in enumerate(data):
        new_data.append((e[0] * 811589153, i))
    data = new_data.copy()
    for _ in range(10):
        i = 0
        while i < len(new_data):
            idx = new_data.index(data[i])
            val, _ = new_data.pop(idx)
            new_place = (idx + val) % (len_data - 1)
            if new_place == 0 and idx != 0:
                new_place = len_data
            new_data.insert(new_place, (val, i))
            i += 1
    total = 0
    i_0 = [i for i, e in enumerate(new_data) if e[0] == 0][0]
    for i in [1000, 2000, 3000]:
        total += new_data[(i + i_0) % len_data][0]
    return total


def main(fname):
    start = t.time()
    data = read_file(fname)
    total1 = part_1(data.copy())
    total2 = part_2(data)
    print(f"Part 1: {total1}")
    print(f"Part 2: {total2}")
    print(f"Ran in {t.time()-start} s")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    filename = args.filename
    main(filename)
