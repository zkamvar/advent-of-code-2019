#!/usr/bin/env python3

import io
import os
import time

class Intcode:
    def __init__(self, string, input = 0, verbose = False, halts = False):
        self.code = [int(x) for x in string.split(",")]
        self.backup = self.code.copy()
        self.record = list()
        self.input = input
        self.output = list()
        self.base = 0
        self.overflow = dict()
        self.halted = False
        self.halts = halts
        self.finished = False
        self.verbose = verbose
        self.i = 0

    def update(self, input = None, verbose = False, i = None):
        self.input = input if input is not None else self.input
        self.i     = i     if i     is not None else self.i
        self.verbose = verbose
        self.halted = False
        return(self)
    
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
        while True:
            i = self.i
            if self.verbose:
                print(self.string())
            if self.halts and self.halted:
                break
            opcode = self.parse_optcode(i)
            inst   = opcode[0] + (10 * opcode[1])
            steplister = [0, 4, 4, 2, 2, 3, 3, 4, 4, 2]
            if inst == 99:
            # 99 is the kill signal which will signal that the program is finished
                self.finished = True
                self.halted = True
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
            # Opcode 4 sets the output value AND THEN halts/waits until it's 
            # given another instruction.
                self.output.append(self.get(a))
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
            
            elif inst == 9:
                self.adjust_base(self.get(a))
                if self.verbose:
                    print("\tbase: {}".format(self.base))
            else:
                ValueError("This ain't right")
            self.i = i + steps
            steps = 0
        return(self)

    def set_params(self, noun = None, verb = None):
        self.set(1, self.get(1) if noun is None else noun)
        self.set(2, self.get(2) if verb is None else verb)
        return(self)

    def set_input(self, input):
        self.input = input


def load_program(path):
    with io.open(path, "r") as f:
        string = "".join(f.readlines())
        f.close()
    return(string)

tiles = [" ", "|", "#", "_", "o"]

def print_screen(the_game, score = 0):
    lasty = 0
    ball = -1
    paddle = -1
    blocks = 0
    print("\nCurrent Score: {}".format(score))
    for i in range(0, len(the_game), 3):
        x, y, tile = the_game[i:i+3]
        if tile == 2:
            blocks += 1
        if tile == 3:
            paddle = x
        if tile == 4:
            ball = x
        if x == -1 and y == 0:
            return((tile, blocks, ball, paddle))
        if y > lasty:
            lasty = y
            print()
        print(tiles[tile], end = '')
    print()
    return((score, blocks, ball, paddle))

def clear():
    if os.name == "nt":
        _ = os.system('cls')
    else:
        _ = os.system('clear')

def part_one(path):
    game = load_program(path)
    cab  = Intcode(game, input = 0).play()
    blocks = 0
    score, blocks, ball, paddle = print_screen(cab.output)
    return(blocks)

def stick(ball, paddle):
    both_found = ball > 0 and paddle > 0
    if not both_found:
        return(0)
    if ball == paddle:
        direction = 0
    elif ball > paddle:
        direction = 1
    else:
        direction = -1
    return(direction)

class Screen:
    def __init__(self):
        self.x = 0 
        self.y = 0
        self.tiles = {}
        self.shapes = [" ", "|", "#", "_", "o"]
        self.score = 0
    
    def update(self, x, y, tile):
        self.x = x if x > self.x else self.x
        self.y = y if y > self.y else self.y
        if x == -1 and y == 0:
            self.score = tile
        else:
            self.tiles["{},{}".format(x, y)] = self.shapes[tile]
        return(self)

    def print(self):
        clear()
        print("Score: {}".format(self.score))
        for y in range(self.y):
            for x in range(self.x):
                the_tile = self.tiles["{},{}".format(x, y)]
                print(the_tile, end = "")
            print()
        print()
        return(self)

def part_two(path):
    game = load_program(path)
    cab  = Intcode(game, input = 0, halts = True)
    cab.set(0, 2)
    the_screen = Screen()
    paddle = -1
    ball = -1
    step = 0
    current_tile = [0, 0, 0]
    cab.play()
    current_tile[step % 3] = cab.get_output()
    while not cab.finished:
        step += 1
        if step % 3 == 0:
            x, y, tile = current_tile
            the_screen.update(x, y, tile)
            the_screen.print()
            if tile == 3:
                paddle = x
            if tile == 4:
                ball = x
        else:
            pass
        joy = stick(ball, paddle)
        current_tile[step % 3] = cab.update(input = joy).play().get_output()
    return(the_screen.score)
        
if __name__ == "__main__":



    print("\nLoading...\n")

    print("Panels: {}".format(part_one("zkamvar-input.txt")))
    print("Final Score: {}".format(part_two("zkamvar-input.txt")))

