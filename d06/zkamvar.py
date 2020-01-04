#!usr/local/bin env python3


import io

class Mass:
    def __init__(self, name):
        self.name = name
        self.parent = None
        self.kids = dict()

    def add_parent(self, parent):
        self.parent = parent
        return(self)

    def add_kid(self, child):
        if child.name not in self.kids:
            self.kids[child.name] = child
        else:
            pass
        return(self)

    def get_child(self, name):
        return(self.kids[name])

    def get_parent(self):
        return(self.parent)

    def count_kids(self):
        return(len(self.kids))

    def has_kids(self):
        return(len(self.kids) > 0)

    def has_parent(self):
        return(self.parent is not None)

    def get_tips(self):
        
        if not self.has_kids():
            return([self])

        kids = list()
        for kid in self.kids.values():
            if isinstance(kid, Mass) and kid.has_kids():
                kids += kid.get_tips()
            else:
                kids += [kid]
        return(kids)

    def count_ancestors(self):
        parent = self.get_parent()
        if parent is None:
            return(0)
        else:
            pass
        n = 1
        while parent.has_parent():
           n = n + 1
           parent = parent.get_parent()
        return(n)

    def get_ancestors(self):
        parents = list()
        parent  = self.get_parent()
        while parent is not None:
            parents.append(parent)
            parent = parent.get_parent()
        return(parents)


def get_input(path):
    with io.open(path, "r") as f:
        data = f.readlines()
        f.close()
    
    nodes = dict()
    for orbit in data:
        parent, child = orbit.strip().split(")")

        # Add new nodes if they don't exist already
        if parent not in nodes:
            nodes[parent] = Mass(parent)
        if child not in nodes:
            nodes[child] = Mass(child)

        # Add the relationship
        nodes[parent].add_kid(nodes[child])
        nodes[child].add_parent(nodes[parent])

    return(nodes)

def part_one(the_nodes):
    return(sum([node.count_ancestors() for node in the_nodes.values()]))

def part_two(the_nodes):
    me = the_nodes["YOU"].get_ancestors()
    santa = the_nodes["SAN"].get_ancestors()
    while me[len(me) - 1].name == santa[len(santa) - 1].name:
        me.pop()
        santa.pop()
    return(len(me) + len(santa))





if __name__ == '__main__':

    nodes = get_input("zkamvar-input.txt")
    print("Part 1: {}".format(part_one(nodes)))
    print("Part 2: {}".format(part_two(nodes)))
    
