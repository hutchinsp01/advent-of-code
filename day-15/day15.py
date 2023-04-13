import re

f = open("day15.txt").read().splitlines()
checkrow = 2000000


class Sensor:
    def __init__(self, location, beacon):
        self.location = location
        self.beacon = beacon

    def get_distance_to_beacon(self):
        return manhattan_distance(self.location, self.beacon.location)

    def get_distance_to_row(self, row):
        return manhattan_distance(self.location, (self.location[0], row))

    def get_radius(self):
        radiuspoints = []
        distance = self.get_distance_to_beacon() + 1
        for x in range(distance + 1):
            radiuspoints.append(
                (self.location[0] + x, self.location[1] + (distance - x))
            )
            radiuspoints.append(
                (self.location[0] - x, self.location[1] + (distance - x))
            )
            radiuspoints.append(
                (self.location[0] + x, self.location[1] - (distance - x))
            )
            radiuspoints.append(
                (self.location[0] - x, self.location[1] - (distance - x))
            )

        self.radius = radiuspoints


class Beacon:
    def __init__(self, location):
        self.location = location


def manhattan_distance(loc1, loc2):
    return abs(loc1[0] - loc2[0]) + abs(loc1[1] - loc2[1])


sensors = []
beacons = []
# Sensor at x=2, y=18: closest beacon is at x=-2, y=15
for line in f:
    numbers = re.compile("-?\d+")
    x, y, x1, y1 = list(map(int, numbers.findall(line)))
    sensors.append(Sensor((x, y), Beacon((x1, y1))))
    beacons.append(Beacon((x1, y1)))


def find_where_beacon_cant_be(row):
    no_beacon = set([])
    for sensor in sensors:
        row_distance = sensor.get_distance_to_row(row)
        beacon_distance = sensor.get_distance_to_beacon()
        safe_distance = beacon_distance - row_distance
        if safe_distance > 0:
            for x in range(
                sensor.location[0] - safe_distance, sensor.location[0] + safe_distance
            ):
                no_beacon.add(x)

    return no_beacon


# print(find_where_beacon_cant_be(checkrow))
print(len(find_where_beacon_cant_be(checkrow)))


def find_hidden_beacon():
    for sensor in sensors:
        sensor.get_radius()
    for sensor in sensors:
        for radiuspoint in sensor.radius:
            if 4000000 > radiuspoint[0] > 0 and 4000000 > radiuspoint[1] > 0:
                valid = True
                for sensor in sensors:
                    if (
                        manhattan_distance(radiuspoint, sensor.location)
                        - sensor.get_distance_to_beacon()
                        <= 0
                    ):
                        valid = False
                        break

                if valid:
                    print(radiuspoint, 4000000 * radiuspoint[0] + radiuspoint[1])
                    return


find_hidden_beacon()
