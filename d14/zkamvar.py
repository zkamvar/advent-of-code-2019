#!/usr/bin/env python3

import io
import re

class Chem:
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity
        self.reqs = {}

    def add_req(self, chem, quantity):
        self.reqs[chem.name] = (chem, quantity)
        return(self)

    def has_req(self, req):
        return(req.name in self.reqs)

    def n_req(self):
        return(len(self.reqs))

# Notes:
# Each element needs to be increased by its own quantity.
#
# 1. have a separate dictionary that lists the quantity of each element we need
# 2. walk from the fuel back to the ORE and record the immediate quantity of
#    each needed 
# 3. balance???

def get_input(path):
    with io.open(path, "r") as f:
        data = f.readlines()
        f.close()
    nodes = {}
    for line in range(len(data)):
        chem = re.compile(r'[0-9]+ [A-Z]+')
        nm = re.compile(r'[A-Z]+')
        qt = re.compile(r'[0-9]+')
        the_chemicals = chem.findall(data[line].strip())
        this = [(nm.findall(x)[0], int(qt.findall(x)[0])) for x in the_chemicals]
        this_node = Chem(*this.pop())
        nodes[this_node.name] = this_node
        for node in this:
            if node[0] not in nodes:
                nodes[node[0]] = Chem(*node)
            this_node.add_req(nodes[node[0]], node[1])
    return(nodes)

def find_ore(element, basket):
    if element.name == "ORE":
        return(basket)
    for key in element.reqs.keys():
        print("{} needs {} {}".format(element.name, element.reqs[key][1], key))
        basket[key]["needs"].append(element.reqs[key][1])
        basket = find_ore(element.reqs[key][0], basket)
    return(basket)
        

def part_one(ingredients):
    basket = {}
    FUEL = ingredients["FUEL"]
    for key in ingredients.keys():
        quant = [FUEL.reqs[key][1]] if key in FUEL.reqs else []
        basket[key] = {"needs": quant, "increments": ingredients[key].quantity}
    for element, quantity in FUEL.reqs.values():
        find_ore(element, basket)
    return(basket)

if __name__ == '__main__':
    print(part_one(get_input("example1_31.txt")))

