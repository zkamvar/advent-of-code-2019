from zkamvar import *


def test_one():
    t1s = '109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99'
    t1 = Intcode(t1s).play()
    assert t1.output_string() == t1s

def test_two():
    t2s = '1102,34915192,34915192,7,4,7,99,0'
    t2 = Intcode(t2s).play()
    assert len(str(t2.get_output())) == 16
    assert t2.get_output() == 34915192 * 34915192

def test_three():
    t3s = '104,1125899906842624,99'
    t3 = Intcode(t3s).play()
    assert t3.get_output() == 1125899906842624

def test1():
    t1 = Intcode("1,9,10,3,2,3,11,0,99,30,40,50").play()
    assert(t1.get(0)   == 3500),                  "t1 is wrong: {}".format(t1.string())

def test2():
    t2 = Intcode("1,0,0,0,99").play() # becomes 2,0,0,0,99 (1 + 1 = 2).
    assert(t2.string() == "2,0,0,0,99"),          "t2 is wrong: {}".format(t2.string())

def test3():
    t3 = Intcode("2,3,0,3,99").play() # becomes 2,3,0,6,99 (3 * 2 = 6).
    assert(t3.string() == "2,3,0,6,99"),          "t3 is wrong: {}".format(t3.string())

def test4():
    t4 = Intcode("2,4,4,5,99,0").play() # becomes 2,4,4,5,99,9801 (99 * 99 = 9801).
    assert(t4.string() == "2,4,4,5,99,9801"),     "t4 is wrong: {}".format(t4.string())

def test5():
    t5 = Intcode("1,1,1,4,99,5,6,0,99").play() # becomes 30,1,1,4,2,5,6,0,99.
    assert(t5.string() == "30,1,1,4,2,5,6,0,99"), "t5 is wrong: {}".format(t5.string())
    
def test6():
    t6 = Intcode("3,0,4,0,99", input = 27).play()
    assert(t6.get_output() == 27)

def test7():
    t7 = Intcode("1002,4,3,4,33,99", input = 27).play()
    assert(t7.get(4) == 99)

def test8():
    t8 = Intcode("3,9,8,9,10,9,4,9,99,-1,8", input = 8).play()
    assert(t8.get_output() == 1)
    t8 = Intcode("3,9,8,9,10,9,4,9,99,-1,8", input = 7).play()
    assert(t8.get_output() == 0)

    ti8 = Intcode("3,3,1108,-1,8,3,4,3,99", input = 8).play()
    assert(ti8.get_output() == 1)
    ti8 = Intcode("3,3,1108,-1,8,3,4,3,99", input = 7).play()
    assert(ti8.get_output() == 0)

    tl8 = Intcode("3,9,7,9,10,9,4,9,99,-1,8", input = 7).play()
    assert(tl8.get_output() == 1)
    tl8 = Intcode("3,9,7,9,10,9,4,9,99,-1,8", input = 87).play()
    assert(tl8.get_output() == 0)

    til8 = Intcode("3,3,1107,-1,8,3,4,3,99", input = 7).play()
    assert(til8.get_output() == 1)
    til8 = Intcode("3,3,1107,-1,8,3,4,3,99", input = 87).play()
    assert(til8.get_output() == 0)

def jump_tests():
    t0 = Intcode("3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9", input = 0).play()
    assert(t0.get_output() == 0)

    t0 = Intcode("3,3,1105,-1,9,1101,0,0,12,4,12,99,1", input = 0).play()
    assert(t0.get_output() == 0)

    tl = Intcode("3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99", input = 8).play()
    assert(tl.get_output() == 1000), print(tl.get_output())
