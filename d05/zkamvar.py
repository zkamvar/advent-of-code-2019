#!/usr/bin/env python3


# - Opcode 3 takes a single integer as input and saves it to the position given
#   by its only parameter. For example, the instruction 3,50 would take an input
#   value and store it at address 50.
# - Opcode 4 outputs the value of its only parameter. For example, the
#   instruction 4,50 would output the value at address 50.

import io

class Intcode:
    def __init__(self, string):
        self.code = [int(x) for x in string.split(",")]
        self.backup = self.code.copy()
        self.record = list()
    
    def string(self):
        return(",".join([str(x) for x in self.code]))

    def get(self, position):
        return(self.code[position])

    def set(self, position, value):
        self.code[position] = value
        return(self)

    def add(self, a, b, position):
        self.code[position] = self.code[a] + self.code[b]
        return(self)

    def mult(self, a, b, position):
        self.code[position] = self.code[a] * self.code[b]
        return(self)

    def log(self, inst, a, b, position):
        self.record.append([inst, self.code[a], self.code[b], self.code[position], position])
        return(self)

    def get_log(self):
        return(self.record)

    def reset(self):
        self.code = self.backup.copy()
        self.log = list()
        return(self)

    def play(self):
        i = 0
        while True:
            inst = self.code[i]
            if inst == 99:
                break
            a   = self.code[i + 1]
            b   = self.code[i + 2]
            pos = self.code[i + 3]
            # self.log(inst, a, b, pos)
            if inst == 1:
                self.add(a, b, pos)
            elif inst == 2:
                self.mult(a, b, pos)
            else:
                ValueError("This ain't right")
            i = i + 4
        return(self)

    def set_params(self, noun, verb):
        self.set(1, noun)
        self.set(2, verb)
        return(self)

    """
    Brute force an answer to the noun-verb question
    """
    def et_tu(self, value):
        result = None
        for noun in range(100):
            for verb in range(100):
                self.reset()
                self.set_params(noun, verb)
                self.play()
                if self.get(0) == value:
                    result = 100 * noun + verb
                    break # This whole for/else buisness is weird
            else:         # https://stackoverflow.com/a/6346536/2752888
                continue
            break
        return(result)

        

def load_program(path):
    with io.open(path, "r") as f:
        string = "".join(f.readlines())
        f.close()
    return(string)

if __name__ == "__main__":

    t1 = Intcode("1,9,10,3,2,3,11,0,99,30,40,50").play()
    t2 = Intcode("1,0,0,0,99").play() # becomes 2,0,0,0,99 (1 + 1 = 2).
    t3 = Intcode("2,3,0,3,99").play() # becomes 2,3,0,6,99 (3 * 2 = 6).
    t4 = Intcode("2,4,4,5,99,0").play() # becomes 2,4,4,5,99,9801 (99 * 99 = 9801).
    t5 = Intcode("1,1,1,4,99,5,6,0,99").play() # becomes 30,1,1,4,2,5,6,0,99.

    assert(t1.get(0)   == 3500),                  "t1 is wrong: {}".format(t1.string())
    assert(t2.string() == "2,0,0,0,99"),          "t2 is wrong: {}".format(t2.string())
    assert(t3.string() == "2,3,0,6,99"),          "t3 is wrong: {}".format(t3.string())
    assert(t4.string() == "2,4,4,5,99,9801"),     "t4 is wrong: {}".format(t4.string())
    assert(t5.string() == "30,1,1,4,2,5,6,0,99"), "t5 is wrong: {}".format(t5.string())
    

    string = load_program("zkamvar-input.txt")
    codes = Intcode(string)
    codes.set_params(12, 2)
    codes.play()
    print("\nFirst code was: {}".format(codes.get(0)))
    print("The value of the 100 * noun + verb is: {}\n".format(codes.et_tu(19690720)))
