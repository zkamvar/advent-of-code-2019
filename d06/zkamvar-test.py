from zkamvar import *

def test_one():
    the_tree = get_input("test-input1.txt")
    assert(part_one(the_tree) == 42), "wrong mother father"

def test_two():
    the_tree = get_input("test-input2.txt")
    assert(part_two(the_tree) == 4), "no santa"
