from zkamvar import *

def test_one():
    e = get_input("example1_31.txt")
    assert(part_one(e) == 31)

def test_two():
    e = get_input("example2_165.txt")
    assert(part_one(e) == 165)

def test_three():
    e = get_input("example3_13312.txt")
    assert(part_one(e) == 13312)

def test_four():
    e = get_input("example4_180697.txt")
    assert(part_one(e) == 180697)

def test_five():
    e = get_input("example5_2210736.txt")
    assert(part_one(e) == 2210736)

