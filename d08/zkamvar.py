#!/usr/bin/env python3

import io
import numpy as np

class BIOS:
    def __init__(self, image, height = 6, width = 25):
        image = [int(x) for x in image]
        depth = int(len(image) / (height * width))
        layers = np.array(image).reshape((width, height, depth), order = "F")

        self.image = layers

    def get_image(self):
        return(self.image)

    def least_zeroes(self):
        zeroes = self.image == 0
        res = zeroes.sum(axis = 0).sum(axis = 0).tolist()
        return(self.image[..., res.index(min(res))])

    def part_one(self):
        im_full = self.least_zeroes()
        ones = im_full == 1
        twos = im_full == 2
        return(ones.sum() * twos.sum())

    def print(self, style = False):
        ii = self.get_image()
        print_image(ii, style)

    def part_two(self):
        img = self.get_image()
        mask = img == 2
        levels = np.zeros(img[...,0].shape, dtype = int, order = "F")
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                k = 0
                while mask[i, j, k]:
                    k = k + 1
                levels[i, j] = img[i, j, k]
        print_image(levels)
        return(levels)


def print_image(img, style = True):
    if len(img.shape) == 3:
        for k in range(img.shape[2]):
            for j in range(img.shape[1]):
                for i in range(img.shape[0]):
                    if style:
                        res = "█" if img[i, j, k] else " "
                    else:
                        res = img[i, j, k]
                    print(res, end = " ")
                print("")
            print("---------")
    elif len(img.shape) == 2:
        for j in range(img.shape[1]):
            for i in range(img.shape[0]):
                if style:
                    res = "█" if img[i, j] else " "
                else:
                    res = img[i, j]
                print(res, end = " ")
            print("")
    else:
        for i in range(img.shape[0]):
            if style:
                res = "█" if img[i] else " "
            else:
                res = img[i]
            print(res, end = " ")


def read_image(path):
    with io.open(path, "r") as f:
        string = "".join(f.readlines()).strip()
        f.close()
    return(string)

if __name__ == '__main__':

    x = BIOS('123456789012', 2, 3)

    im_full = x.least_zeroes()
    ones = im_full == 1
    twos = im_full == 2
    svns = im_full == 7
    assert(ones.sum() == 1)
    assert(twos.sum() == 1)
    assert(svns.sum() == 0)
    assert(ones.sum() * twos.sum() == 1)
    assert(x.part_one() == 1)
    s = '012222221012222222221102000220220102022222211221221122022012112012201202221'
    s = s + '0'*25
    t2 = BIOS(s, 5, 5)
    assert(t2.part_one() == 80)

    print("Loading...")
    img = BIOS(read_image("zkamvar-input.txt"), height = 6, width = 25)
    assert(img.part_one() == 1935)
    print("Part 1: {}".format(img.part_one()))
    print("Part 2: ")
    lvls = img.part_two()
    
