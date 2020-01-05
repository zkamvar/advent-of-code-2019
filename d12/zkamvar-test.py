from zkamvar import *

def test_one():
    x = load_program("example1_10_179.txt")
    assert(find_energy(x, 10) == 179), ""

def test_two():
    x = load_program("example2_100_1940.txt")
    assert(find_energy(x, 100) == 1940), ""

def test_three():
    x = load_program("example1_10_179.txt")
    y = load_program("example1_10_179.txt")
    x = step(x, True)
    assert(aligned(x, y) == False)
    assert(part_two("example1_10_179.txt") == 2772), "dang"

# def test_four():
#    assert(part_two("example3_4686774924.txt") == 4686774924), "double dang"
