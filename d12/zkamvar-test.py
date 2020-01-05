from zkamvar import *

def test_one():
    x = load_program("example1_10_179.txt")
    assert(find_energy(x, 10) == 179), ""

def test_two():
    x = load_program("example2_100_1940.txt")
    assert(find_energy(x, 100) == 1940), ""

