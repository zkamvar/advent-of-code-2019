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
        self.step = 0

    def get_wire(self, wire):
        if wire == 1:
            return(self.first)
        else:
            return(self.second)

    def get_intersections(self):
        return(self.intersect)

    def get_visited(self):
        return(self.visited)

    def visit(self, key, wire):

        if key == '0,0':
            return(self)

        self.step = self.step + 1

        if key in self.visited:
            # If there is a key, then it has been visited
            wires = self.visited[key].keys()
            if wire in self.visited[key]:
                # if it's been visited by ourselves, increment
                self.visited[key][wire][0] = self.visited[key][wire][0] + 1
            elif len(wires) > 0:
                # if it's been visited by another wire, add our wire and record intersection
                self.visited[key][wire] = [1, self.step]
                self.intersect.append([int(x) for x in key.split(',')])
            else:
                # otherwise, just add our key (this shouldn't happen)
                self.visited[key] = {wire : [1, self.step]}
        else:
            # if there is no key, it hasn't been visited
            self.visited[key] = {wire : [1, self.step]}

        return(self)

    def trace(self, wire):

        self.current['x'] = 0
        self.current['y'] = 0
        self.step = 0

        for direction in self.get_wire(wire):

            vector = DIRECTIONS[direction[:1]]
            start  = self.current[vector[0]]
            end    = int(direction[1:]) * vector[1] + start

            if vector[0] == 'x':
                keystring = "{}," + str(self.current['y'])
            else:
                keystring = str(self.current['x']) + ",{}"

            for point in range(start + vector[1], end + vector[1], vector[1]):
                self.visit(keystring.format(str(point)), str(wire))

            self.current[vector[0]] = end
        return(self)

    def find_closest_point(self):
        if len(self.get_visited()) == 0:
            self.trace_wires()

        return(min([abs(x[0]) + abs(x[1]) for x in self.get_intersections()]))

    def trace_wires(self):
        self.trace(1).trace(2)
        return(self)

    def find_smallest_intersection(self):
        if len(self.get_visited()) == 0:
            self.trace_wires()

        ikeys = ["{},{}".format(x[0], x[1]) for x in self.get_intersections()]
        sums = []

        for key in ikeys:
            val = self.get_visited()[key]
            sums.append(val['1'][1] + val['2'][1])

        return(min(sums))





if __name__ == "__main__":


    w0 = Wires('R8,U5,L5,D3\nU7,R6,D4,L4')
    assert(w0.find_closest_point() == 6), "example 0 wrong"
    assert(w0.find_smallest_intersection() == 30), print(w0.find_smallest_intersection())

    w1 = Wires('R75,D30,R83,U83,L12,D49,R71,U7,L72\nU62,R66,U55,R34,D71,R55,D58,R83')
    assert(w1.find_closest_point() == 159), "example 1 wrong"
    assert(w1.find_smallest_intersection() == 610), print(w1.find_smallest_intersection())

    w2 = Wires('R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51\nU98,R91,D20,R16,D67,R40,U7,R15,U6,R7')
    assert(w2.find_closest_point() == 135), "example 2 wrong"
    assert(w2.find_smallest_intersection() == 410), print(w2.find_smallest_intersection())

    znk = Wires(get_input("zkamvar-input.txt"))
    print("closest distance: {}".format(znk.find_closest_point()))
    print("smallest intersection: {}".format(znk.find_smallest_intersection()))


    



