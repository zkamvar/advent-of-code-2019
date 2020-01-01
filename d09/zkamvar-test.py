from zkamvar import *

def test1():
    t1s = '109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99'
    t1 = Intcode(t1s).play()
    assert t1.output_string() == t1s

def test2():
    t2s = '1102,34915192,34915192,7,4,7,99,0'
    t2 = Intcode(t2s).play()
    assert len(str(t2.get_output())) == 16
    assert t2.get_output() == 34915192 * 34915192

def test3():
    t3s = '104,1125899906842624,99'
    t3 = Intcode(t3s).play()
    assert t3.get_output() == 1125899906842624
