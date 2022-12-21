import argparse
import time as t

operations = {"+": "__add__", "-": "__sub__", "*": "__mul__", "/": "__floordiv__"}

inv_op = {"-": "+", "+": "-", "/": "*", "*": "/"}


def read_file(fname):
    data = {}
    with open(fname, "r") as file:
        for line in file:
            strip = line.strip()
            if strip != "":
                split = strip.split()
                key = split[0][:-1]
                if len(split) == 2:
                    data[key] = int(split[-1])
                else:
                    data[key] = tuple(split[1:])
    return data


def scream(in_dct, key="root"):
    op = in_dct[key]
    if isinstance(op, int):
        return op
    key1, f, key2 = op
    val1 = scream(in_dct, key=key1)
    val2 = scream(in_dct, key=key2)
    val = getattr(val1, operations[f])(val2)
    in_dct[key] = val
    return val


def scream_requiring_human(in_dct, requires_humn, key="root"):
    op = in_dct[key]
    if isinstance(op, int):
        return op, 0
    if isinstance(op, tuple) and len(op) == 2:
        return op
    key1, f, key2 = op
    val1, hmn1 = scream_requiring_human(in_dct, requires_humn, key=key1)
    val2, hmn2 = scream_requiring_human(in_dct, requires_humn, key=key2)
    val = getattr(val1, operations[f])(val2)
    hmn = int(hmn1 or hmn2)
    if hmn:
        requires_humn.add(key)
    in_dct[key] = val, hmn
    return val, hmn


def create_inv_dict(in_dct, requires_humn, val_dict):
    new_dct = {}
    for key, op in in_dct.items():
        if key == "root":
            pass
            if op[0] not in requires_humn:
                new_dct[key] = val_dict[op[0]][0]
            elif op[2] not in requires_humn:
                new_dct[key] = val_dict[op[2]][0]
            else:
                raise ValueError
        elif isinstance(op, int):
            new_dct[key] = op
        elif key not in requires_humn:
            new_dct[key] = val_dict[key][0]
        else:
            # Now we need to inverse
            for prev_key, prev_op in in_dct.items():
                if isinstance(prev_op, tuple) and key in prev_op:
                    break
            left, op, right = prev_op
            new_op = inv_op[op]
            if key == left:
                other_key = right
            else:
                other_key = left
            if prev_key == "root":
                new_dct[key] = val_dict[other_key][0]
            elif key == left or op in ["+", "*"]:
                new_dct[key] = (prev_key, new_op, other_key)
            else:
                # deal with asymmetric operations
                new_dct[key] = (other_key, op, prev_key)

    return new_dct


def part_1(data):
    new_data = data.copy()
    val = scream(new_data)
    return val


def part_2(data):
    new_data = data.copy()
    new_data["humn"] = (0, 1)
    requires_humn = set()
    requires_humn.add("humn")
    _ = scream_requiring_human(new_data, requires_humn)
    inv_data = data.copy()
    inv_data["humn"] = None
    new_dct = create_inv_dict(inv_data, requires_humn, new_data)
    val = scream(new_dct, "humn")
    return val


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
