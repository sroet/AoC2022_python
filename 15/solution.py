import argparse
import time
import itertools as itt


def read_file(fname):
    data = {}
    with open(fname, "r") as file:
        for line in file:
            strip = line.strip()
            if strip != "":
                split = strip.split()
                x_sensor = int(split[2].split("=")[-1][:-1])
                y_sensor = int(split[3].split("=")[-1][:-1])
                x_beacon = int(split[-2].split("=")[-1][:-1])
                y_beacon = int(split[-1].split("=")[-1])
                data[(x_sensor, y_sensor)] = (x_beacon, y_beacon)
    return data


class Overlap:
    def __init__(self):
        self.ranges = []
        self.min = float("-inf")
        self.max = float("inf")

    def add(self, new_range):
        new_left, new_right = new_range
        new_left = max(new_left, self.min)
        new_right = min(new_right, self.max)
        for i, (left, right) in enumerate(self.ranges):
            if new_right < left:
                self.ranges.insert(i, new_range)
                break
            if right >= new_left:
                self.ranges.pop(i)
                joined_left = min(left, new_left)
                joined_right = max(right, new_right)
                self.add((joined_left, joined_right))
                break
        else:
            # reached end of ranges
            self.ranges.append(new_range)

    def total(self):
        total = 0
        for left, right in self.ranges:
            total += right - left + 1
        return total


def part_1(data, y):
    ranges = Overlap()
    for key, val in data.items():
        x_sens, y_sens = key
        x_beac, y_beac = val
        dist = abs(x_sens - x_beac) + abs(y_sens - y_beac)
        dist_to_y = abs(y_sens - y)
        if dist_to_y > dist:
            continue
        x_range = dist - dist_to_y
        ranges.add((x_sens - x_range, x_sens + x_range))
    beacons_on_y = set(val for val in data.values() if val[1] == y)
    return ranges.total() - len(beacons_on_y)


def part_2_v1(data):
    # Slow (~50 sec) but gives correct result for example
    overlap_expected = 4_000_000
    y_out = 0
    x_out = 0
    for y in range(4_000_000):
        ranges = Overlap()
        ranges.min = 0
        ranges.max = overlap_expected
        for key, val in data.items():
            x_sens, y_sens = key
            x_beac, y_beac = val
            dist = abs(x_sens - x_beac) + abs(y_sens - y_beac)
            dist_to_y = abs(y_sens - y)
            if dist_to_y > dist:
                continue
            x_range = dist - dist_to_y
            ranges.add((x_sens - x_range, x_sens + x_range))
        if len(ranges.ranges) != 1:
            y_out = y
            x_out = ranges.ranges[0][1] + 1
            break
    return x_out * 4_000_000 + y_out


def intersect(posline, negline):
    b_pos, left_pos, right_pos = posline
    b_neg, left_neg, right_neg = negline
    if not (left_pos[1] <= left_neg[1] and right_pos[1] >= right_neg[1]):
        return False
    x = (b_neg - b_pos) // 2
    y = -x + b_neg
    return (x, y)


def part_2_v2(data):
    # Fast, but only gives correct result for real input
    top_pos = []  # top of hole in example plot, pos dir
    bot_pos = []  # bottom of hole in example plot, pos dir
    top_neg = []  # top of hole, neg dir
    bot_neg = []  # bottom of hole, neg dir
    for key, val in data.items():
        x_sens, y_sens = key
        x_beac, y_beac = val
        dist = abs(x_sens - x_beac) + abs(y_sens - y_beac)
        # y = ax + b; a in {-1, 1}
        bottom = (x_sens, y_sens + dist)
        top = (x_sens, y_sens - dist)
        left = (x_sens - dist, y_sens)
        right = (x_sens + dist, y_sens)
        # left corner
        bpos1 = y_sens - (x_sens - dist)
        bneg1 = y_sens + (x_sens - dist)
        # right corner
        bpos2 = y_sens - (x_sens + dist)
        bneg2 = y_sens + (x_sens + dist)
        top_pos.append((bpos1, left, bottom))
        bot_pos.append((bpos2, top, right))
        top_neg.append((bneg2, bottom, right))
        bot_neg.append((bneg1, left, top))
    allowed_pos = []
    allowed_neg = []

    for a, b in itt.product(top_pos, bot_pos):
        if a[0] == b[0] - 2:
            allowed_pos.append((a, b))
    for c, d in itt.product(top_neg, bot_neg):
        if c[0] == d[0] - 2:
            allowed_neg.append((c, d))
    for pos, neg in itt.product(allowed_pos, allowed_neg):
        # Check if everything intersects
        temp = []
        for pos_line, neg_line in itt.product(pos, neg):
            out = intersect(pos_line, neg_line)
            if out is False:
                break
            temp.append(out)
        else:
            # This only works for the non_example_input
            x = None
            y = None
            x_seen = set()
            y_seen = set()
            for xt, yt in temp:
                if xt in x_seen:
                    x = xt
                else:
                    x_seen.add(xt)
                if yt in y_seen:
                    y = yt
                else:
                    y_seen.add(yt)
            break
    return x * 4_000_000 + y


def main(fname, y):
    start = time.time()
    data = read_file(fname)
    total_1 = part_1(data, y)
    total_2 = part_2_v2(data)
    print(f"Part 1: {total_1}")
    print(f"Part 2: {total_2}")
    print(f"Ran in {time.time()-start} s")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    parser.add_argument("y", type=int)  # for part 1
    args = parser.parse_args()
    filename = args.filename
    inp_y = args.y
    main(filename, inp_y)
