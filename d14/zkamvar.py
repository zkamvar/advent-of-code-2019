#!/usr/bin/env python3

import io
import re
import math

class Chem:
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity
        self.reqs = {}
        self.makes = {}

    def add_req(self, chem, quantity):
        self.reqs[chem.name] = (chem, quantity)
        return(self)
    
    def add_product(self, product):
        self.makes[product.name] = product
        return(self)

    def has_req(self, req):
        return(req in self.reqs)

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
        the_needed = element.reqs[key]
        # print("{} needs {} {}".format(element.name, the_needed[1], key))
        basket[key]["needs"].append(the_needed[1])
        the_needed[0].add_product(element)
        basket = find_ore(the_needed[0], basket)
    return(basket)
        

def part_one(ingredients):
    basket = {}
    needs_ore = []
    FUEL = ingredients["FUEL"]
    for key in ingredients.keys():
        if ingredients[key].has_req("ORE"):
            needs_ore.append(ingredients[key].name)
        else:
            pass
        quant = [FUEL.reqs[key][1]] if key in FUEL.reqs else []
        basket[key] = {"needs": quant, "increments": ingredients[key].quantity}
    for element, _ in FUEL.reqs.values():
        find_ore(element, basket)
    much_ore = 0
    for e in needs_ore:
        the_needed = sum(basket[e]["needs"])
        increment = basket[e]["increments"]
        much_ore += increment * math.ceil(the_needed/increment)

    return(much_ore)

if __name__ == '__main__':
    print(part_one(get_input("example1_31.txt")))

