#!/usr/bin/env python3


# - Opcode 3 takes a single integer as input and saves it to the position given
#   by its only parameter. For example, the instruction 3,50 would take an input
#   value and store it at address 50.
# - Opcode 4 outputs the value of its only parameter. For example, the
#   instruction 4,50 would output the value at address 50.

import io

class Intcode:
    def __init__(self, string, input = 0):
        self.code = [int(x) for x in string.split(",")]
        self.backup = self.code.copy()
        self.record = list()
        self.input = input
        self.output = None
    
    def string(self):
        return(",".join([str(x) for x in self.code]))
    
    def get_input(self):
        return(self.input)

    def parse_optcode(self, position):
        inst = self.get(position)
        the_params = [0, 0, 0, 0, 0]
        i = 0
        while inst > 0:
            remaining = (inst // 10) 
            the_params[i] = inst - (remaining * 10)
            inst = remaining
            i = i + 1
        return(the_params)

    def get(self, position):
        if (isinstance(position, int)):
            return(self.code[position])
        else:
            return(position[0] if position[1] else self.code[position[0]])

    def set(self, position, value):
        self.code[position] = value
        return(self)

    def add(self, a, b, position):
        self.set(position, self.get(a) + self.get(b))
        return(self)

    def mult(self, a, b, position):
        self.set(position, self.get(a) * self.get(b))
        return(self)

    def log(self, inst, a, b, position):
        self.record.append([inst, self.get(a), self.get(b), self.get(position), position])
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
            opcode = self.parse_optcode(i)
            inst   = opcode[0] + (10 * opcode[1])
            if inst == 99:
                break
            a = (self.get(i + 1), opcode[2])
            if inst == 3:
                steps = 2
            elif inst == 4:
                steps = 2
            else:
                b   = (self.get(i + 2), opcode[3])
                if inst == 5:
                    steps = 3
                elif inst == 6:
                    steps = 3
                else:
                    steps = 4
                    pos =  self.get(i + 3)

            if inst == 1:
                self.add(a, b, pos)
            elif inst == 2:
                self.mult(a, b, pos)
            elif inst == 3:
                self.set(a[0], self.get_input())
            elif inst == 4:
                self.output = self.get(a)
                p = "{}\r" if self.output == 0 else "{}"
                print(p.format(self.output))
            elif inst == 5:
            # Opcode 5 is jump-if-true: if the first parameter is non-zero, it
            # sets the instruction pointer to the value from the second
            # parameter. Otherwise, it does nothing.
                if self.get(a):
                    i = self.get(b)
                    continue
                else:
                    pass

            elif inst == 6:
            # Opcode 6 is jump-if-false: if the first parameter is zero, it
            # sets the instruction pointer to the value from the second
            # parameter. Otherwise, it does nothing.
                if not self.get(a):
                    i = self.get(b)
                    continue
                else:
                    pass

            elif inst == 7:
            # Opcode 7 is less than: if the first parameter is less than the
            # second parameter, it stores 1 in the position given by the third
            # parameter.  Otherwise, it stores 0.
                val = 1 if self.get(a) < self.get(b) else 0
                self.set(pos, val)

            elif inst == 8:
            # Opcode 8 is equals: if the first parameter is equal to the second
            # parameter, it stores 1 in the position given by the third
            # parameter. Otherwise, it stores 0.
                val = 1 if self.get(a) == self.get(b) else 0
                self.set(pos, val)

            else:
                ValueError("This ain't right")
            i = i + steps
            steps = 0
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
    
    t6 = Intcode("3,0,4,0,99", input = 27).play()
    assert(t6.output == 27)

    t7 = Intcode("1002,4,3,4,33,99", input = 27).play()
    assert(t7.get(4) == 99)

    t8 = Intcode("3,9,8,9,10,9,4,9,99,-1,8", input = 8).play()
    assert(t8.output == 1)
    t8 = Intcode("3,9,8,9,10,9,4,9,99,-1,8", input = 7).play()
    assert(t8.output == 0)

    ti8 = Intcode("3,3,1108,-1,8,3,4,3,99", input = 8).play()
    assert(ti8.output == 1)
    ti8 = Intcode("3,3,1108,-1,8,3,4,3,99", input = 7).play()
    assert(ti8.output == 0)

    tl8 = Intcode("3,9,7,9,10,9,4,9,99,-1,8", input = 7).play()
    assert(tl8.output == 1)
    tl8 = Intcode("3,9,7,9,10,9,4,9,99,-1,8", input = 87).play()
    assert(tl8.output == 0)

    til8 = Intcode("3,3,1107,-1,8,3,4,3,99", input = 7).play()
    assert(til8.output == 1)
    til8 = Intcode("3,3,1107,-1,8,3,4,3,99", input = 87).play()
    assert(til8.output == 0)

    print("Jump tests")
    t0 = Intcode("3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9", input = 0).play()
    assert(t0.output == 0)

    t0 = Intcode("3,3,1105,-1,9,1101,0,0,12,4,12,99,1", input = 0).play()
    assert(t0.output == 0)

    tl = Intcode("3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99", input = 8).play()
    assert(tl.output == 1000), print(tl.output)


    print("\nLoading...\n")

    string = load_program("zkamvar-input.txt")
    codes = Intcode(string, input = 1)
    codes.play()
    print("\nOutput was: {}".format(codes.output))
    warmer = Intcode(string, input = 5).play()
    print("\nWarmer output was: {}".format(warmer.output))
