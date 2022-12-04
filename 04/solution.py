import argparse
import time


def read_file(fname):
    out = []
    with open(fname, "r") as file:
        for line in file:
            line = line.strip()
            if len(line) > 0:
                left, right = line.split(",")
                out.append(
                    (
                        tuple(int(i) for i in left.split("-")),
                        tuple(int(i) for i in right.split("-")),
                    )
                )
    return out


def part_1(data):
    total1 = 0
    for (left1, right1), (left2, right2) in data:
        if (left1 <= left2 and right1 >= right2) or (
            left2 <= left1 and right2 >= right1
        ):
            total1 += 1
    return total1


def part_2(data):
    total2 = 0
    for (left1, right1), (left2, right2) in data:
        # Total overlap
        if (left1 <= left2 and right1 >= right2) or (
            left2 <= left1 and right2 >= right1
        ):
            total2 += 1
        # First shift to the left
        elif left1 < left2 <= right1 < right2:
            total2 += 1
        # First shift to the right
        elif left2 < left1 <= right2 < right1:
            total2 += 1
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
