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
        the_needed, amount_needed = element.reqs[key]
        
        if the_needed.name in basket:
            remaining = basket[the_needed.name]["leftovers"]
        else:
            remaining = 0
        # what's needed of the current element 
        for_fuel = basket[element.name]["needs"]

        # How much we need to make the current element's product
        i_need_this_much = (amount_needed * for_fuel) - remaining

        # the amount we overshot
        the_remainder = i_need_this_much % the_needed.quantity

        # the amount we'll make
        topoff = int(the_remainder > 0)
        mult   = i_need_this_much // the_needed.quantity
        i_make_this_much = the_needed.quantity * (topoff + mult)
        
        # updating our cart
        basket[key]["leftovers"] = the_remainder
        basket[key]["needs"] += i_make_this_much
        the_needed.add_product(element)
        
        # going one level deeper
        basket = find_ore(the_needed, basket)
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
        quant = FUEL.reqs[key][1] if key in FUEL.reqs else 0
        basket[key] = {"needs": quant, "increments": ingredients[key].quantity, "leftovers": 0}
    for element, _ in FUEL.reqs.values():
        find_ore(element, basket)
    much_ore = 0
    for e in needs_ore:
        ore_needed = ingredients[e].reqs["ORE"][1] 
        the_needed = basket[e]["needs"]
        increment = basket[e]["increments"]
        much_ore += ore_needed * math.ceil(the_needed/increment)

    return(much_ore, needs_ore, basket)

if __name__ == '__main__':

    '''
    9 ORE => 2 A
    8 ORE => 3 B
    7 ORE => 5 C
    3 A, 4 B => 1 AB
    5 B, 7 C => 1 BC
    4 C, 1 A => 1 CA
    2 AB, 3 BC, 4 CA => 1 FUEL
    
    # 2 AB = 6 A, 8 B
    #      = 2*3 A + 3*3 B
    #      = 9*3   + 8*3 ORE
    #      = 27    + 24  ORE
    #      = 51 ORE
    # remainder : 1 B

    # 3 BC = 15 B, 21 C
    #      = 3*5 B + 5*5 C
    #      = 8*5   + 7*5 ORE
    #      = 40    + 35  ORE
    #      = 75 ORE
    # remainder: 4 C

    # 4 CA = 16 C, 4 A
    #      = 5*4 C + 2*2 A
    #      = 7*4   + 9*2 ORE
    #      = 28    + 18  ORE
    #      = 46 ORE
    # remainder: 4 C
    '''
    print(part_one(get_input("example1_31.txt")))
    print(part_one(get_input("example1_znk.txt")))
    print(part_one(get_input("example2_165.txt")))
    print(part_one(get_input("example3_13312.txt")))

