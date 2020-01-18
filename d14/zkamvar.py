#!/usr/bin/env python3

import io
import re
from math import ceil
from queue import Queue
from collections import defaultdict

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

'''
I was going the absolute wrong way with this one, so I had to go to the
solutions thread. This particular solution was adapted to a particularly
well-documented solution here:
https://github.com/jeffjeffjeffrey/advent-of-code/blob/f3f9ee1cc706210eca04e05775021793aa8c5086/2019/day_14.ipynb

Whereas I was attempting to use a dictionary to keep track of all the
ingredients needed (and failing miserably), jjj used a Queue and treated all
of the ingredients like orders at a restaraunt. It effectively starts like this:

Your first order is an amount of FUEL, but you need certain ingredients to
make that fuel, so you take each item needed for the recipe, figure out how
much you need to make in "amount" and keep a record of how much is left over
in supply. You put each item in the orders queue and then go through until
there are no more orders left to take (which happens to be when you start
adding up the ORE you need).
'''
def make_fuel(amount, recipes):
    supply = defaultdict(int)
    orders = Queue()
    orders.put({"ingredient": "FUEL", "amount": amount})
    ore_needed = 0

    while not orders.empty():
        order = orders.get()
        if order["ingredient"] == "ORE":
            ore_needed += order["amount"]
        elif order["amount"] <= supply[order["ingredient"]]:
            supply[order["ingredient"]] -= order["amount"]
        else:
            amount_needed = order["amount"] - supply[order["ingredient"]]
            recipe = recipes[order["ingredient"]]
            batches = ceil(amount_needed / recipe.quantity)
            for ingredient, amount in recipe.reqs.values():
                orders.put({"ingredient": ingredient.name, "amount": amount * batches})
            leftover_amount = batches * recipe.quantity - amount_needed
            supply[order["ingredient"]] = leftover_amount
    return ore_needed

def part_one(ingredients):
    return(make_fuel(1, ingredients))


if __name__ == '__main__':
    print("To make one fuel we need {} ORE".format(part_one(get_input("zkamvar-input.txt"))))
