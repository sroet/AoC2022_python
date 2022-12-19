import argparse
import time as t
import tqdm

# order = ore, clay, obsidian, geode


def read_file(fname):
    data = []
    with open(fname, "r") as file:
        for line in file:
            temp = {}
            strip = line.strip()
            if strip != "":
                split = strip.split()
                temp["ore"] = ((int(split[6]), 0, 0, 0), (1, 0, 0, 0))
                temp["clay"] = ((int(split[12]), 0, 0, 0), (0, 1, 0, 0))
                temp["obsi"] = ((int(split[18]), int(split[21]), 0, 0), (0, 0, 1, 0))
                temp["geo"] = ((int(split[27]), 0, int(split[30]), 0), (0, 0, 0, 1))
                data.append(temp)
    return data


def rec_dfs(
    time, components, production, blueprint, cache={}, current_max=[0], reset=False
):
    # Uses a mutable default cache, should never be used in production code
    if reset:
        keys = list(cache)
        for key in keys:
            cache.pop(key)
        current_max[0] = 0
        return
    if (time, components, production) in cache:
        return cache[(time, components, production)]
    if time == 0:
        current_max[0] = max(components[-1], current_max[0])
        return components[-1]
    # More aggresive pruning
    max_ore_production = (
        production[0] * time + components[0] + sum(i for i in range(time))
    )
    max_new_clay_production = max_ore_production // blueprint["clay"][0][0]
    max_clay_production = (
        production[1] * time
        + components[1]
        + sum(
            time - (i + 1) for i in range(max_new_clay_production) if time - (i + 1) > 0
        )
    )
    max_new_obsidian_production = min(
        max_ore_production // blueprint["obsi"][0][0],
        max_clay_production // blueprint["obsi"][0][1],
    )

    max_obsidian = (
        production[2] * time
        + components[-2]
        + sum(
            time - (i + 1)
            for i in range(max_new_obsidian_production)
            if time - (i + 1) > 0
        )
    )
    max_new_geo = min(
        max_ore_production // blueprint["geo"][0][0],
        max_obsidian // blueprint["geo"][0][-2],
    )
    max_geo = production[-1] * time + sum(
        (time - (i + 1)) for i in range(max_new_geo) if time - (i + 1) > 0
    )
    if max_geo + components[-1] < current_max[0]:
        # can never be higher
        return -1
    new_time = time - 1
    options = []
    new_components = tuple(c + p for c, p in zip(components, production))
    # do nothing
    options.append((new_time, new_components, production, blueprint))
    costs = [i[0] for i in blueprint.values()]
    costs += [(0, 0, 0, float("inf"))]
    max_cost = list(max(i) for i in zip(*costs))

    for cost, prod in blueprint.values():
        if all(i <= j for i, j in zip(cost, components)):
            components_after_build = tuple(j - i for i, j in zip(cost, new_components))
            new_production = tuple(i + j for i, j in zip(prod, production))
            if any(i > j for i, j in zip(new_production, max_cost)):
                # more production than can be consumed
                continue
            options.append(
                (time - 1, components_after_build, new_production, blueprint)
            )
    val = max(rec_dfs(*i) for i in options)
    cache[(time, components, production)] = val
    return val


def part_1(data):
    total_1 = 0
    for num, blueprint in tqdm.tqdm(enumerate(data)):
        # reset_cache
        rec_dfs(None, None, None, None, reset=True)
        time = 24
        components = (0, 0, 0, 0)
        production = (1, 0, 0, 0)
        total = rec_dfs(time, components, production, blueprint)
        total_1 += total * (num + 1)
    return total_1


def part_2(data):
    total_2 = 1
    for blueprint in tqdm.tqdm(data[:3]):
        # reset_cache
        rec_dfs(None, None, None, None, reset=True)
        time = 32
        components = (0, 0, 0, 0)
        production = (1, 0, 0, 0)
        total = rec_dfs(time, components, production, blueprint)
        total_2 *= total
    return total_2


def main(fname):
    start = t.time()
    data = read_file(fname)
    total1 = part_1(data)
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
