from zkamvar import *

def test_example1():
    t1 = read_input('example1_8.txt')
    p1 = part_one(t1)
    assert(len(t1) == 10), "number of asteroids is wrong"
    assert(p1.coord == (4, 3)), "coordinates are wrong"
    assert(len(p1.seen) == 8), "number of asteroids is wrong"

def test_example2():
    t1 = read_input('example2_33.txt')
    p1 = part_one(t1)
    assert(p1.coord == (8, 5)), "coordinates are wrong"
    assert(len(p1.seen) == 33), "number of asteroids is wrong"

def test_example3():
    t1 = read_input('example3_35.txt')
    p1 = part_one(t1)
    assert(p1.coord == (2, 1)), "coordinates are wrong"
    assert(len(p1.seen) == 35), "number of asteroids is wrong"

def test_example4():
    t1 = read_input('example4_41.txt')
    p1 = part_one(t1)
    assert(p1.coord == (3, 6)), "coordinates are wrong"
    assert(len(p1.seen) == 41), "number of asteroids is wrong"

def test_example5():
    t1 = read_input('example5_210.txt')
    p1 = part_one(t1)
    assert(p1.coord == (13, 11)), "coordinates are wrong"
    assert(len(p1.seen) == 210), "number of asteroids is wrong"

def test_part_two():
    t2 = read_input('example5_210.txt')
    p2 = part_two(t2)
    assert(p2 == 802), "whoopsiedaisy"
