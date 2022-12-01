import argparse


def read_file(fname):
    out = []
    with open(fname, "r") as file:
        temp = []
        for line in file:
            line = line.strip()
            if line == "":
                if len(temp) > 0:
                    out.append(temp)
                    temp = []
                continue
            temp.append(int(line))
    return out


def main(fname):
    data = read_file(fname)
    print(f"Part 1: {max(sum(i) for i in data)}")
    part_2 = [sum(i) for i in data]
    part_2.sort()
    print(f"Part 2: {sum(part_2[-3:])}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    fname = args.filename
    main(fname)
