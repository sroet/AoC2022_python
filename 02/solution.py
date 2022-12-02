import argparse

point_shape = {
    "R": 1,
    "P": 2,
    "S": 3,
}

map_them = {"A": "R", "B": "P", "C": "S"}

map_me_part1 = {"X": "R", "Y": "P", "Z": "S"}
# Oponent you
point_results = {
    "RR": 3,
    "RS": 0,
    "RP": 6,
    "SR": 6,
    "SS": 3,
    "SP": 0,
    "PR": 0,
    "PS": 6,
    "PP": 3,
}

map_me_part2 = {
    "RY": "R",
    "RX": "S",
    "RZ": "P",
    "SZ": "R",
    "SY": "S",
    "SX": "P",
    "PX": "R",
    "PZ": "S",
    "PY": "P",
}


def read_file(fname):
    out = []
    with open(fname, "r") as file:
        for line in file:
            temp = line.split()
            if len(temp) > 0:
                out.append(tuple(temp))
    return out


def main(fname):
    data = read_file(fname)
    total1 = 0
    total2 = 0
    for them, mine in data:
        them = map_them[them]
        me1 = map_me_part1[mine]
        me2 = map_me_part2[them + mine]
        total1 += point_shape[me1] + point_results[them + me1]
        total2 += point_shape[me2] + point_results[them + me2]
    print(f"Part 1: {total1}")
    print(f"Part 2: {total2}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    fname = args.filename
    main(fname)
