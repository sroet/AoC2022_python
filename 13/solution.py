import argparse
import time


def read_file(fname):
    data = []
    with open(fname, "r") as file:
        left = None
        right = None
        for line in file:
            strip = line.strip()
            if strip != "":
                if left is None:
                    left = eval(strip)
                elif right is None:
                    right = eval(strip)
            else:
                data.append((left, right))
                left = None
                right = None
    if left is not None:
        data.append((left, right))
    return data


def compare(left, right):
    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return True
        if left > right:
            return False
        return None
    if isinstance(left, int):
        # right is list
        return compare([left], right)
    if isinstance(right, int):
        # left is list
        return compare(left, [right])
    # Otherwise both lists
    # check list values
    for i, j in zip(left, right):
        result = compare(i, j)
        if result is not None:
            return result
    # check list lengths
    if len(left) < len(right):
        return True
    if len(left) > len(right):
        return False
    return None


def part_1(data):
    total = 0
    for i, (left, right) in enumerate(data):
        if compare(left, right):
            total += i + 1
    return total


def part_2(data):
    data2 = []
    for left, right in data:
        data2.append(left)
        data2.append(right)
    data2.append([[2]])
    data2.append([[6]])

    unsorted = True
    # Simple bubble sort
    while unsorted:
        unsorted = False
        for i in range(len(data2) - 1):
            left = data2[i]
            right = data2[i + 1]
            if not compare(left, right):
                data2[i] = right
                data2[i + 1] = left
                unsorted = True
    total = data2.index([[2]]) + 1
    total *= data2.index([[6]]) + 1
    return total


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
