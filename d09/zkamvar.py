#!/usr/bin/env python3


# - Opcode 3 takes a single integer as input and saves it to the position given
#   by its only parameter. For example, the instruction 3,50 would take an input
#   value and store it at address 50.
# - Opcode 4 outputs the value of its only parameter. For example, the
#   instruction 4,50 would output the value at address 50.

import io
import time

class Intcode:
    def __init__(self, string, input = 0, verbose = False):
        self.code = [int(x) for x in string.split(",")]
        self.backup = self.code.copy()
        self.record = list()
        self.input = input
        self.output = list()
        self.base = 0
        self.overflow = dict()
        self.verbose = verbose
    
    def string(self):
        return(",".join([str(x) for x in self.code]))

    def output_string(self):
        return(",".join([str(x) for x in self.output]))

    def get_output(self, position = None):
        if position is not None:
            pos = position
        elif len(self.output) == 0:
            pos = 0
        else:
            pos = len(self.output) - 1
        return(self.output[pos])
    
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

    def get(self, position, value = True):
        if position is None:
            return(None)
        if isinstance(position, int):
            return(self.get_internal(position))
        else:
            pass
        pos, mode = position
        pos = pos + self.base if mode is 2 else pos
        return(pos if mode is 1 or not value else self.get_internal(pos))

    def get_internal(self, position):
        if len(self.code) <= position:
            position = self.overflow[position] if position in self.overflow else 0
        else:
            position = self.code[position]
        return(position)

    def set(self, position, value):
        if len(self.code) <= position:
            self.overflow[position] = value
        else:
            self.code[position] = value
        return(self)

    def adjust_base(self, value):
        self.base = self.base + value
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
            steplister = [0, 4, 4, 2, 2, 3, 3, 4, 4, 2]
            if inst == 99:
                break
            a = (self.get(i + 1), opcode[2])
            b = None
            pos = None
            steps = steplister[inst]
            if steps > 2:
                b = (self.get(i + 2), opcode[3])
                if steps == 4:
                    pos =  self.get(i + 3)
                    pos = pos + self.base if opcode[4] is 2 else pos
                else:
                    pos = None
            else:
                b = None

            if self.verbose:
                time.sleep(0.005)
                instructions = [str(self.get(x)) for x in range(i, i + steps)]
                print("0: {} | i: {} \t| Inst: {} [{}]".format(self.get(0), i, inst, ", ".join(instructions)))

            if inst == 1:
                self.add(a, b, pos)
            elif inst == 2:
                self.mult(a, b, pos)
            elif inst == 3:
                self.set(self.get(a, value = False), self.get_input())
            elif inst == 4:
                self.output.append(self.get(a))
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
            
            elif inst == 9:
                self.adjust_base(self.get(a))
                if self.verbose:
                    print("\tbase: {}".format(self.base))
            else:
                ValueError("This ain't right")
            i = i + steps
            steps = 0
        return(self)

    def set_params(self, noun, verb):
        self.set(1, noun)
        self.set(2, verb)
        return(self)

    def set_input(self, input):
        self.input = input

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

def part_one(string, verbose = True):
    codes = Intcode(string, input = 1, verbose = verbose)
    return(codes.play().output_string())

if __name__ == "__main__":

    print("\nLoading...\n")

    string = load_program("zkamvar-input.txt")
    print("Part one:\t{}".format(part_one(string, verbose = False)))
    # warmer = Intcode(string, input = 5).play()
    # print("\nWarmer output was: {}".format(warmer.output))
