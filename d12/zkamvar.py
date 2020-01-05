#!/usr/bin/env python3

import io
import re

class Moon:
    def __init__(self, string):
        p = re.compile(r'[-]?\d+')
        coords = p.findall(string)
        self.coords = [int(x) for x in coords]
        self.velocity = [0, 0, 0]

    def apply_gravity(self, luna):
        shifts = compare_bodies(self, luna)
        self.velocity = [self.velocity[i] + shifts[i] for i in range(3)]
        return(self)

    def apply_velocity(self):
        self.coords = [self.coords[i] + self.velocity[i] for i in range(3)]
        return(self)

    def p_energy(self):
        return(sum([abs(x) for x in self.coords]))

    def k_energy(self):
        return(sum([abs(x) for x in self.velocity]))





def compare_coords(a, b):
    if a < b:
        return(1)
    elif a > b:
        return(-1)
    else:
        return(0)

def compare_bodies(a, b):
    return([compare_coords(a.coords[i], b.coords[i]) for i in range(3)])
    


def load_program(path):
    with io.open(path, "r") as f:
        bodies = f.readlines()
        f.close()
    for i in range(len(bodies)):
        bodies[i] = Moon(bodies[i].strip())
    return(bodies)

def step(bodies, show = False):
    for i in range(len(bodies)):
        a = bodies[i]
        for j in range(i + 1, len(bodies)):
            b = bodies[j]
            a.apply_gravity(b)
            b.apply_gravity(a)

    for i in range(len(bodies)):
        bodies[i].apply_velocity()
        if show:
            p = "pos = {}, vel = {}".format(bodies[i].coords, bodies[i].velocity)
            print(p)

    if show:
        print()
    return(bodies)
    


def find_energy(bodies, steps = 1):
    for i in range(steps):
        bodies = step(bodies)
    e = 0
    for i in range(len(bodies)):
        e += bodies[i].p_energy() * bodies[i].k_energy()
    return(e)

def aligned(a, b):
    unequal_coords = sum([a[i].coords != b[i].coords for i in range(len(a))])
    unequal_vels   = sum([a[i].velocity != b[i].velocity for i in range(len(a))])
    return(unequal_coords + unequal_vels == 0)



def part_one():
    return(find_energy(load_program("zkamvar-input.txt"), 1000))

def part_two(path):
    bodies = load_program(path)
    start  = load_program(path)
    bodies = step(bodies)
    steps = 1
    while not aligned(bodies, start):
        steps += 1
        bodies = step(bodies)
    return(steps)


if __name__ == '__main__':

    print("Part one: {}".format(part_one()))
    # print("Part two: {}".format(part_two("zkamvar-input.txt")))

