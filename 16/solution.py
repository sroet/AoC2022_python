import argparse
import time
from collections import deque
import itertools as itt


def read_file(fname):
    flow_rates = {}
    connected_valves = {}

    with open(fname, "r") as file:
        for line in file:
            strip = line.strip()
            if strip != "":
                split = strip.split(" ", 9)
                key = split[1]
                flow_rates[key] = int(split[4].split("=")[-1][:-1])
                connected_valves[key] = split[-1].split(", ")
    return flow_rates, dist_to_valves(connected_valves)


def find_dist(connected_valves, start_node):
    todo = set(connected_valves)
    out = {}
    todo.remove(start_node)
    queue = deque([(start_node, 0)])
    while todo:
        node, dist = queue.popleft()
        if node in todo:
            todo.remove(node)
            out[node] = dist
        for next_node in connected_valves[node]:
            if next_node in todo:
                queue.append((next_node, dist + 1))
    return out


def dist_to_valves(connected_valves):
    out = {}
    for key in connected_valves:
        out[key] = find_dist(connected_valves, key)
    return out


def part_1_v2(data):
    flow_rates, distances = data
    max_score = 0
    todo = {key for key, val in flow_rates.items() if val != 0}
    queue = []
    time_me = 30
    place = "AA"
    score = 0
    queue.append((score, time_me, place, todo.copy()))
    while queue:
        score, time_me, place, todo = queue.pop()
        if score > max_score:
            max_score = score
        if score + sum(flow_rates[i] for i in todo) * time_me < max_score:
            continue
        for next_node in todo:
            next_todo = todo.copy()
            next_todo.remove(next_node)
            dist = distances[place][next_node] + 1
            next_time = time_me - dist
            if next_time < 0:
                continue
            next_score = score + flow_rates[next_node] * next_time
            queue.append((next_score, next_time, next_node, next_todo))
    return max_score


def part_2(data):
    flow_rates, distances = data
    max_score = 0
    todo = {key for key, val in flow_rates.items() if val != 0}
    queue = []
    time_me = 26
    place_me = "AA"
    time_o = 26
    place_o = "AA"
    score = 0
    queue.append((score, time_me, place_me, time_o, place_o, todo.copy()))
    while queue:
        score, time_me, place_me, time_o, place_o, todo = queue.pop()

        if score > max_score:
            max_score = score
        if score + sum(flow_rates[i] for i in todo) * max(time_me, time_o) < max_score:
            continue
        if time_me == time_o == 0:
            continue

        # Me and O both need to make a decision
        if time_me == time_o:
            if place_me in todo:
                score += time_me * flow_rates[place_me]
                todo.remove(place_me)
            if place_o in todo:
                score += time_o * flow_rates[place_o]
                todo.remove(place_o)
            if not todo:
                queue.append((score, 0, "DONE", 0, "DONE", todo.copy()))
            for next_node_me, next_node_o in itt.product(todo, todo):
                if len(todo) > 1 and next_node_me == next_node_o:
                    continue
                dist_me = distances[place_me][next_node_me] + 1
                next_time_me = max(0, time_me - dist_me)
                dist_o = distances[place_o][next_node_o] + 1
                next_time_o = max(0, time_o - dist_o)
                queue.append(
                    (
                        score,
                        next_time_me,
                        next_node_me,
                        next_time_o,
                        next_node_o,
                        todo.copy(),
                    )
                )
        # Only me making a new choice
        elif time_me > time_o:
            if place_me in todo:
                score += time_me * flow_rates[place_me]
                todo.remove(place_me)
            next_time_o = time_o
            next_node_o = place_o
            for next_node_me in todo:
                if next_node_me == next_node_o:
                    continue
                dist_me = distances[place_me][next_node_me] + 1
                next_time_me = max(0, time_me - dist_me)
                queue.append(
                    (
                        score,
                        next_time_me,
                        next_node_me,
                        next_time_o,
                        next_node_o,
                        todo.copy(),
                    )
                )
            if not todo:
                queue.append((score, 0, "Done", next_time_o, next_node_o, todo.copy()))
        # Only O makes a new choice
        elif time_o > time_me:
            if place_o in todo:
                score += time_o * flow_rates[place_o]
                todo.remove(place_o)
            next_time_me = time_me
            next_node_me = place_me
            if not todo:
                queue.append(
                    (score, next_time_me, next_node_me, 0, "Done", todo.copy())
                )
            for next_node_o in todo:
                dist_o = distances[place_o][next_node_o] + 1
                next_time_o = max(0, time_o - dist_o)
                queue.append(
                    (
                        score,
                        next_time_me,
                        next_node_me,
                        next_time_o,
                        next_node_o,
                        todo.copy(),
                    )
                )

    return max_score


def main(fname):
    start = time.time()
    data = read_file(fname)
    total1 = part_1_v2(data)
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
