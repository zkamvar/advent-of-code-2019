#!/usr/bin/env python3


# - Opcode 3 takes a single integer as input and saves it to the position given
#   by its only parameter. For example, the instruction 3,50 would take an input
#   value and store it at address 50.
# - Opcode 4 outputs the value of its only parameter. For example, the
#   instruction 4,50 would output the value at address 50.

import io
import itertools

class Intcode:
    def __init__(self, string, input = 0, phase = 0):
        self.code = [int(x) for x in string.split(",")]
        self.backup = self.code.copy()
        self.input = input
        self.phase = phase
        self.phased = False
        self.output = None
        self.halted = False
    
    def string(self):
        return(",".join([str(x) for x in self.code]))
    
    def get_input(self):
        if not self.phased:
            self.phased = True
            return(self.phase)
        else:
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

    def reset(self, software = True, input = 0, phase = 0):
        if software:
            self.code = self.backup.copy()
        self.input = input
        self.phase = phase
        self.phased = False
        self.output = None
        self.halted = False
        return(self)

    def play(self):
        i = 0
        while True:
            if self.halted:
                break
            opcode = self.parse_optcode(i)
            inst   = opcode[0] + (10 * opcode[1])
            if inst == 99:
                self.halted = True
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
                # if self.output != 0:
                #     print("Output: {}".format(self.output))
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

def amp_circuit(program, phase = [0, 1, 2, 3, 4], loop = False):
    A = Intcode(program, input = 0,        phase = phase[0]).play()
    B = Intcode(program, input = A.output, phase = phase[1]).play()
    C = Intcode(program, input = B.output, phase = phase[2]).play()
    D = Intcode(program, input = C.output, phase = phase[3]).play()
    E = Intcode(program, input = D.output, phase = phase[4]).play()

    stopping = False
    out = E.output

    while loop and not stopping:
        out = E.output
        print(E.output)
        A.reset(True, input = E.output, phase = phase[0]).play()
        B.reset(True, input = A.output, phase = phase[1]).play()
        C.reset(True, input = B.output, phase = phase[2]).play()
        D.reset(True, input = C.output, phase = phase[3]).play()
        E.reset(True, input = D.output, phase = phase[4]).play()
        stopping = False if E.output is not None else True 
        
    return(out)


if __name__ == "__main__":


    t1 = amp_circuit('3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0', [4, 3, 2, 1, 0])
    t2 = amp_circuit('3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0')   
    t3 = amp_circuit('3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0', [1, 0, 4, 3, 2])

    assert(t1 == 43210)
    assert(t2 == 54321)
    assert(t3 == 65210)

    tx = Intcode('3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0', 0, 1).play()
    assert(tx.output is not None)
    assert(tx.reset().play().output is not None)
    assert(tx.reset(False).output is None)

    # t4 = amp_circuit('3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5', [9,8,7,6,5], loop = True)
    # assert(t4 == 139629729)



    print("\nLoading...\n")

    string = load_program("zkamvar-input.txt")
    res = list()
    for i in itertools.permutations(range(5)):
        res.append(amp_circuit(string, i))

    print("Part 1: {}".format(max(res)))
    print("Part 2: (屮ﾟДﾟ)屮") 

