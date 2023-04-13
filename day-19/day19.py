import copy
from functools import lru_cache

from parse import parse


class Blueprint:
    def __init__(self, number, ore, clay, obsidian, geode):
        self.number = number
        self.ore_robot_cost = ore
        self.clay_robot_cost = clay
        self.obsidian_robot_cost = obsidian
        self.geode_robot_cost = geode


blueprint_list = []
f = open("day19.txt").read().split("\n")
for blueprint in f:
    blueprint.strip()
    input = parse(
        "Blueprint {number}: Each ore robot costs {ore} ore. Each clay robot costs {clay} ore. Each obsidian robot costs {obsidian0} ore and {obsidian1} clay. Each geode robot costs {geode0} ore and {geode1} obsidian.",
        blueprint,
    )

    blueprint_list.append(
        Blueprint(
            int(input["number"]),
            int(input["ore"]),
            int(input["clay"]),
            (int(input["obsidian0"]), int(input["obsidian1"])),
            (int(input["geode0"]), int(input["geode1"])),
        )
    )


def make_ore_robot(blueprint, r_vals):
    return tuple(
        map(sum, zip(r_vals, (1, 0, 0, 0, -1 * blueprint.ore_robot_cost, 0, 0, 0)))
    )


def make_clay_robot(blueprint, r_vals):
    return tuple(
        map(sum, zip(r_vals, (0, 1, 0, 0, -1 * blueprint.clay_robot_cost, 0, 0, 0)))
    )


def make_obsidian_robot(blueprint, r_vals):
    return tuple(
        map(
            sum,
            zip(
                r_vals,
                (
                    0,
                    0,
                    1,
                    0,
                    -1 * blueprint.obsidian_robot_cost[0],
                    -1 * blueprint.obsidian_robot_cost[1],
                    0,
                    0,
                ),
            ),
        )
    )


def make_geode_robot(blueprint, r_vals):
    return tuple(
        map(
            sum,
            zip(
                r_vals,
                (
                    0,
                    0,
                    0,
                    1,
                    -1 * blueprint.geode_robot_cost[0],
                    0,
                    -1 * blueprint.geode_robot_cost[1],
                    0,
                ),
            ),
        )
    )


def make_no_robot(blueprint, r_vals):
    return r_vals


def can_make_ore_robot(blueprint, r_vals):
    if r_vals[0] >= max(
        blueprint.ore_robot_cost,
        blueprint.clay_robot_cost,
        blueprint.obsidian_robot_cost[0],
        blueprint.geode_robot_cost[0],
    ):
        return False
    return r_vals[4] >= blueprint.ore_robot_cost


def can_make_clay_robot(blueprint, r_vals):
    if r_vals[1] >= blueprint.obsidian_robot_cost[1]:
        return False
    return r_vals[5] >= blueprint.clay_robot_cost


def can_make_obsidian_robot(blueprint, r_vals):
    if r_vals[2] >= blueprint.geode_robot_cost[1]:
        return False
    return (
        r_vals[4] >= blueprint.obsidian_robot_cost[0]
        and r_vals[5] >= blueprint.obsidian_robot_cost[1]
    )


def can_make_geode_robot(blueprint, r_vals):
    return (
        r_vals[4] >= blueprint.geode_robot_cost[0]
        and r_vals[6] >= blueprint.geode_robot_cost[1]
    )


def add_new_resources(r_vals):
    return tuple(
        map(sum, zip(r_vals, (0, 0, 0, 0, r_vals[0], r_vals[1], r_vals[2], r_vals[3])))
    )


def max_geodes_possible(r_vals, time):
    return r_vals[7] + r_vals[3] * time + sum(range(time + 1))


@lru_cache(maxsize=None)
def run_simulation(blueprint, time=24, max_geodes=0, r_vals=(1, 0, 0, 0, 0, 0, 0, 0)):
    if time == 0:
        return r_vals[7]
    call_funcs = []
    if time > 0:
        if max_geodes_possible(r_vals, time) <= max_geodes:
            return max_geodes
        if can_make_obsidian_robot(blueprint, r_vals):
            call_funcs.append(make_obsidian_robot)
        if can_make_clay_robot(blueprint, r_vals):
            call_funcs.append(make_clay_robot)
        if can_make_ore_robot(blueprint, r_vals):
            call_funcs.append(make_ore_robot)
        call_funcs.append(make_no_robot)

        # Always make a geode robot if possible
        if can_make_geode_robot(blueprint, r_vals):
            call_funcs = [make_geode_robot]

        for make_robot in call_funcs:
            geodes = run_simulation(
                blueprint,
                time - 1,
                max_geodes,
                make_robot(blueprint, add_new_resources(r_vals)),
            )

            if geodes > max_geodes:
                max_geodes = geodes

    return max_geodes


def part1(blueprint_list):
    score = 0
    for blueprint in blueprint_list:
        newscore = run_simulation(blueprint, time=24)
        score += blueprint.number * newscore
    return score


def part2(blueprint_list):
    scores = []
    for blueprint in blueprint_list[:3]:
        newscore = run_simulation(blueprint, time=32)
        scores.append(newscore)
    return scores[0] * scores[1] * scores[2]


print(f"Part 1: {part1(blueprint_list)}")
print(f"Part 2: {part2(blueprint_list)}")
