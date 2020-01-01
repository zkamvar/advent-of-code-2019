#!/usr/local/bin/env python3

import io
import math

class Asteroid:
    def __init__(self, y, x):
        self.coord = (y, x)
        self.name = "{},{}".format(y, x)
        self.seen = dict() # dictionary to hold angles as keys
    def look(self, Asteroid):
        coord = self.rel_coord(Asteroid)
        angle = round(math.atan2(*coord), 16)
        if angle not in self.seen:
            self.seen[angle] = Asteroid
        else:
            pass
        return(self)
    def rel_coord(self, Asteroid):
        return((Asteroid.coord[0] - self.coord[0], Asteroid.coord[1] - self.coord[1]))


def read_input(path):
    asteroids = dict()
    with io.open(path, "r") as f:
        y = 0
        x = 0
        for row in f.readlines():
            for point in row: 
                if point == '#':
                    roid = Asteroid(y, x)
                    asteroids[roid.name] = roid
                else:
                    pass
                x = x + 1
            x = 0
            y = y + 1
        f.close()
    return(asteroids)

def look_around(field):
    asteroids = list(field.keys())
    while len(asteroids) > 0:
        aster = field[asteroids.pop()]
        for point in field.keys():
            if aster.name is not point:
                aster.look(field[point])
            else:
                pass
    return(field)

def part_one(field):
    field = look_around(field)
    max = 0
    the_asteroid = None
    for asteroid in field.values():
        seen = len(asteroid.seen)
        the_asteroid, max = (the_asteroid, max) if seen <= max else (asteroid, seen)
    return(the_asteroid)
        
def part_two(field):
    the_asteroid = part_one(field)
    angles = list(the_asteroid.seen.keys())
    angles.sort()
    le_pew = list()
    # The 90 degree mark has an arctan value of math.pi * 0.5
    # The arctan value decreases from pi to negative pi starting at 270 degrees
    # Steps:
    #   1. Sort the list of seen asteroids
    #   2. Start at the asteriod just greater than math.pi * 0.5
    #   3. if the asteroid has one behind it, replace the key with the value of
    #      the latter asteroid
    #   4. else replace the value of the list index with Inf
    #   4. pew --- record the asteroids name in a list
    #   5. 
    here = 0
    still_looking = True
    for i in range(len(angles)):
        if angles[i] >= round(math.pi * -0.5, 16):
            here = i
            break
        else:
            pass
    while still_looking:
        if here < len(angles):
            if angles[here] == 9:
                continue
            angle = angles[here]
            destroy_me = the_asteroid.seen[angle]
            if angles[here] in destroy_me.seen:
                the_asteroid.seen[angle] = destroy_me.seen[angle]
            else:
                angles[here] = 9
            le_pew.append(destroy_me.coord)
            del destroy_me
            here = here + 1
        else:
            here = 0
            pass
        if (len(le_pew) == 200):
            still_looking = False
    the_coord = le_pew[199]
    return((the_coord[1] * 100) + the_coord[0])
           
    


    



if __name__ == '__main__':
    t1 = read_input('zkamvar-input.txt')
    p1 = part_one(t1)
    print("There are {} asteroids detectable from {}".format(len(p1.seen), p1.name))
    print("Part two: {}".format(part_two(t1)))
