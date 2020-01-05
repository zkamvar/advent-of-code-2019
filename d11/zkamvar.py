#!/usr/bin/env python3


import io

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

    def update(self, input = None, verbose = False):
        self.input = input if input is not None else self.input
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

    def set_params(self, noun, verb):
        self.set(1, noun)
        self.set(2, verb)
        return(self)

    def set_input(self, input):
        self.input = input

directions = {
    "up"    : {0 : "left" , 1  : "right"} ,
    "left"  : {0 : "down" , 1  : "up"}    ,
    "down"  : {0 : "right", 1  : "left"}  ,
    "right" : {0 : "up"   , 1  : "down"}
}

moves = {
    "up"    : (1 , 0) ,
    "left"  : (0 , -1),
    "down"  : (-1, 0) ,
    "right" : (0 , 1)
}
        
class Robot:
    def __init__(self, brain, start = 0):
        self.brain = Intcode(brain, input = start, halts = True)
        self.direction = "up"
        self.coord = (0, 0)
        self.panel = {"0,0": start}

    def move(self):
        where          = self.brain.get_output()
        new_direction  = directions[self.direction][where]
        new_moves      = moves[new_direction]
        self.direction = new_direction
        self.coord     = (self.coord[0] + new_moves[0], self.coord[1] + new_moves[1])
        return(self)

    def paint(self):
        name = ",".join([str(x) for x in self.coord]) 
        self.panel[name] = self.brain.get_output()
        return(self)

    def get_color(self):
        color = ",".join([str(x) for x in self.coord]) 
        if color in self.panel:
            return(self.panel[color])
        else:
            return(0)

    def paint_and_move(self):
        self.brain.update(input = self.get_color()).play()
        self.paint()
        self.brain.update().play()
        self.move()

    def run(self):
        while not self.brain.finished:
            self.paint_and_move()
        return(self)

    def view_panels(self):
        coords = [x.split(",") for x in self.panel.keys()]
        ycoords = [int(x[0]) for x in coords]
        xcoords = [int(x[1]) for x in coords]
        ymax = max(ycoords)
        ymin = min(ycoords)
        xmax = max(xcoords)
        xmin = min(xcoords)
        for y in range(ymax, ymin - 1, -1):
            for x in range(xmin, xmax + 1):
                coord = ",".join([str(y), str(x)])
                if coord in self.panel:
                    p = self.panel[coord]
                else:
                    p = 0
                p = " " if p is 0 else "#"
                print(p, end = '')
            print()
        return(self)

def load_program(path):
    with io.open(path, "r") as f:
        string = "".join(f.readlines())
        f.close()
    return(string)

def part_one(path):
    brain = load_program(path)
    robo = Robot(brain)
    robo.run()
    robo.view_panels()
    return(len(robo.panel))

def part_two(path):
    brain = load_program(path)
    robo = Robot(brain, start = 1)
    robo.run()
    robo.view_panels()
    

    


if __name__ == "__main__":



    print("\nLoading...\n")

    print("Panels: {}".format(part_one("zkamvar-input.txt")))
    part_two("zkamvar-input.txt")

