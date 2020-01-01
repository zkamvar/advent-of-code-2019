#!/usr/bin/env python3


import io
import itertools
import time

class Intcode:
    def __init__(self, string, input = 0, phase = 0, verbose = False):
        self.code = [int(x) for x in string.split(",")]
        self.backup = self.code.copy()
        self.input = input
        self.phase = phase
        self.phased = False
        self.output = None
        self.halted = False
        self.finished = False
        self.verbose = verbose
        self.i = 0

    def update(self, input = None, phase = None, verbose = False):
        self.phase = phase if phase is not None else self.phase
        self.input = input if input is not None else self.input
        self.verbose = verbose
        self.halted = False
        return(self)

    def reset(self, software = True, input = 0, phase = 0, verbose = False):
        if software:
            self.code = self.backup.copy()
            self.i = 0
        self.input = input
        self.phase = phase
        self.phased = False
        self.output = None
        self.halted = False
        self.verbose = verbose
        return(self)

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

    def play(self):
        if self.verbose:
            print("Input: {} | Phase: {}".format(self.input, self.phase))
        while True:
            i = self.i
            if self.verbose:
                print(self.string())
            if self.halted:
                break
            opcode = self.parse_optcode(i)
            inst   = opcode[0] + (10 * opcode[1])
            if inst == 99:
            # 99 is the kill signal which will signal that the program is finished
                self.finished = True
                self.halted = True
                break
            a = (self.get(i + 1), opcode[2])
            if inst > 2 and inst < 5:
                # Opcodes 3 and 4 only take one argument
                steps = 2
            else:
                b = (self.get(i + 2), opcode[3])
                if inst > 4 and inst < 7:
                # Opcodes 5 and 6 take two arguments
                    steps = 3
                else:
                # Opcodes 1, 2, 7, and 8 get three arguments
                    steps = 4
                    pos = self.get(i + 3)

            if self.verbose:
                time.sleep(1)
                instructions = [str(self.get(x)) for x in range(i, i + steps)]
                print("i: {} \t| Inst: {} [{}]".format(i, inst, ", ".join(instructions)))

            if inst == 1:
                self.add(a, b, pos)
            elif inst == 2:
                self.mult(a, b, pos)
            elif inst == 3:
                self.set(a[0], self.get_input())
            elif inst == 4:
            # Opcode 4 sets the output value AND THEN halts/waits until it's 
            # given another instruction.
                self.output = self.get(a)
                self.halted = True
            elif inst == 5:
            # Opcode 5 is jump-if-true: if the first parameter is non-zero, it
            # sets the instruction pointer to the value from the second
            # parameter. Otherwise, it does nothing.
                if self.get(a):
                    self.i = self.get(b)
                    continue
                else:
                    pass

            elif inst == 6:
            # Opcode 6 is jump-if-false: if the first parameter is zero, it
            # sets the instruction pointer to the value from the second
            # parameter. Otherwise, it does nothing.
                if not self.get(a):
                    self.i = self.get(b)
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
                
            self.i = i + steps
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

    out = E.output

    while loop: 
        out = E.output
        A.update(input = E.output, phase = phase[0], verbose = False).play()
        B.update(input = A.output, phase = phase[1], verbose = False).play()
        C.update(input = B.output, phase = phase[2], verbose = False).play()
        D.update(input = C.output, phase = phase[3], verbose = False).play()
        E.update(input = D.output, phase = phase[4], verbose = False).play()
        loop = False if E.finished else True 
        
    return(out)

def part_one(string):
    res = list()
    for i in itertools.permutations(range(5)):
        res.append(amp_circuit(string, i))
    return(max(res))

def part_two(string):
    res = list()
    for i in itertools.permutations(range(5, 10)):
        res.append(amp_circuit(string, i, loop = True))
    return(max(res))



if __name__ == "__main__":

    print("\nLoading...\n")

    string = load_program("zkamvar-input.txt")

    print("Part 1: {}".format(part_one(string)))
    print("Part 2: {}".format(part_two(string))) 
