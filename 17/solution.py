import argparse
import time

shapes = [
    (0, 1, 2, 3),
    (1 + 2j, 0 + 1j, 1 + 1j, 2 + 1j, 1),
    (2 + 2j, 2 + 1j, 0, 1, 2),
    (3j, 2j, 1j, 0),
    (0 + 1j, 1 + 1j, 0, 1),
]


def read_file(fname):
    with open(fname, "r") as file:
        for line in file:
            strip = line.strip()
            if strip != "":
                return strip


def overlap(positions, pile):
    for pos in positions:
        if pos.real < 0 or pos.real > 6:
            return True
        if pos.imag <= 0:
            return True
        if pos in pile:
            return True
    return False


def parts(data):
    n_rocks = int(1e12)
    n_shapes = len(shapes)
    n_jet = len(data)
    current_jet = 0
    out_y = 0
    out_y_1 = None
    out_y_2 = None
    pile = {-1}
    cache = dict()
    for rock in range(n_rocks):
        pos = complex(2, out_y + 4)
        current_shape = rock % n_shapes
        shape = shapes[rock % n_shapes]

        if (current_jet, current_shape) in cache:
            n, diff_y = cache[current_jet, current_shape]
            div, mod = divmod(n_rocks - rock, rock - n)
            if not mod:
                out_y_2 = out_y + (out_y - diff_y) * div
        else:
            cache[(current_jet, current_shape)] = (rock, out_y)

        while True:
            jet = data[current_jet]
            current_jet = (current_jet + 1) % n_jet
            # go left
            if jet == "<":
                dif_x = -1
            # go right
            else:
                dif_x = +1
            temp_pos_x = (s + pos + dif_x for s in shape)
            if not overlap(temp_pos_x, pile):
                pos += dif_x
            temp_pos_y = (s + pos - 1j for s in shape)
            if not overlap(temp_pos_y, pile):
                pos -= 1j
            else:
                break
        pile |= {pos + s for s in shape}
        max_s_y = max((pos + s).imag for s in shape)
        out_y = max(out_y, max_s_y)
        if rock == 2022:
            out_y_1 = out_y
        if out_y_1 and out_y_2:
            return out_y_1, out_y_2


def main(fname):
    start = time.time()
    data = read_file(fname)
    total1, total2 = parts(data)
    print(f"Part 1: {total1}")
    print(f"Part 2: {total2}")
    print(f"Ran in {time.time()-start} s")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    filename = args.filename
    main(filename)
