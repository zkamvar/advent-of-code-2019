#!usr/local/env python3
import io

DIRECTIONS = {
    'L': ('x', -1),
    'R': ('x', 1),
    'U': ('y', 1),
    'D': ('y', -1),
}


def get_input(path):
    with io.open(path, "r") as f:
        data = "".join(f.readlines())
        f.close()
    return(data)

class Wires:
    def __init__(self, input):
        dat = input.split("\n")
        self.first = dat[0].split(",")
        self.second = dat[1].split(",")
        self.current = {'x' : 0, 'y' : 0}
        self.visited = dict()
        self.intersect = list()

    def get_wire(self, wire):
        if wire == 1:
            return(self.first)
        else:
            return(self.second)

    def get_intersections(self):
        return(self.intersect)

    def visit(self, key, wire):
        if key in self.visited:
            # If there is a key, then it has been visited
            wires = self.visited[key].keys()
            if wire in self.visited[key]:
                # if it's been visited by ourselves, increment
                self.visited[key][wire] = self.visited[key][wire] + 1
            elif wires is not None:
                # if it's been visited by another wire, add our wire and record intersection
                self.visited[key][wire] = 1
                if key is not '0,0':
                    self.intersect.append(key.split(','))
            else:
                # otherwise, just add our key (this shouldn't happen)
                self.visited[key] = {wire : 1}
        else:
            # if there is no key, it hasn't been visited
            self.visited[key] = {wire : 1}
        return(self)

    def trace(self, wire):
        for direction in self.get_wire(wire):
            vector = DIRECTIONS[direction[:1]]
            start  = self.current[vector[0]]
            end    = int(direction[1:]) * vector[1] + start
            if vector[0] == 'x':
                keystring = "{}," + str(self.current['y'])
            else:
                keystring = str(self.current['x']) + ",{}"

            for point in range(start, end + vector[1]):
                self.visit(keystring.format(str(point)), wire)

            self.current[vector[0]] = end
        return(self)


if __name__ == "__main__":


    w1 = Wires('R75,D30,R83,U83,L12,D49,R71,U7,L72\nU62,R66,U55,R34,D71,R55,D58,R83')
    w1.trace(1).trace(2)
    print(w1.get_intersections())    
    w2 = Wires('R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51\nU98,R91,D20,R16,D67,R40,U7,R15,U6,R7')
    w2.trace(1).trace(2)
    print(w2.get_intersections())
    



