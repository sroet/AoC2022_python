import argparse
import time


def read_file(fname):
    data = []
    with open(fname, "r") as file:
        for line in file:
            strip = line.strip()
            if strip != "":
                data.append(strip)
    return data


def add_to_tree(current_dict, left_path, file):
    if len(left_path) == 0:
        if file[0] == "dir":
            current_dict[file[1]] = {}
        else:
            current_dict[file[1]] = int(file[0])
        return current_dict
    node = left_path.pop()
    next_dict = current_dict[node]
    current_dict[node] = add_to_tree(next_dict, left_path, file)
    return current_dict


def change_dir(cwd, command):
    if command == "..":
        _ = cwd.pop()
        return cwd
    if command == "/":
        return ["/"]
    cwd.append(command)
    return cwd


def list_dir(cwd, current_tree, files):
    for file in files:
        temp = cwd.copy()[::-1]
        current_tree = add_to_tree(current_tree, temp, file)
    return current_tree


def file_size_dirs(layout, current_dir="/", output=None):
    if output is None:
        output = {}
    total = 0
    for key, val in layout[current_dir].items():
        if isinstance(val, int):
            total += val
        else:
            temp, output = file_size_dirs(
                layout[current_dir], current_dir=key, output=output
            )
            total += temp
    if current_dir in output:
        i = 0
        while current_dir in output:
            current_dir = current_dir + str(i)
            i += 1
    output[current_dir] = total
    return total, output


def part_1(data, cwd="/"):
    layout = {"/": {}}
    itt = (i for i in data)
    in_list = False
    current_list = []
    for line in itt:
        split = line.split()
        if in_list:
            if split[0] == "$":
                layout = list_dir(cwd, layout, current_list)
                current_list = []
                in_list = False
            else:
                current_list.append(tuple(split))
                continue
        if split[1] == "cd":
            cwd = change_dir(cwd, split[2])
        elif split[1] == "ls":
            in_list = True
        else:
            raise ValueError
    if in_list:
        layout = list_dir(cwd, layout, current_list)

    dir_sizes = file_size_dirs(layout)[1]
    total = 0
    for val in dir_sizes.values():
        if val <= 100_000:
            total += val
    return total, dir_sizes


def part_2(data):
    data_avail = 70_000_000 - data["/"]
    data_needed = 30_000_000 - data_avail
    current_val = float("inf")
    for val in data.values():
        if data_needed <= val < current_val:
            current_val = val
    return current_val


def main(fname):
    start = time.time()
    data = read_file(fname)
    total1, dir_sizes = part_1(data)
    total2 = part_2(dir_sizes)
    print(f"Part 1: {total1}")
    print(f"Part 2: {total2}")
    print(f"Ran in {time.time()-start} s")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    filename = args.filename
    main(filename)
