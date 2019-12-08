#!/usr/bin/env python3

import io
import numpy as np

class BIOS:
    def __init__(self, image, height = 6, width = 25):
        image = [int(x) for x in image]
        depth = int(len(image) / (height * width))
        layers = np.array(image).reshape((height,  width, depth), order = "F")

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

    def print(self):
        ii = self.get_image()
        for k in range(ii.shape[2]):
                for j in range(ii.shape[1]):
                    for i in range(ii.shape[0]):
                        print(ii[i, j, k], end = " ")
                    print("")
                print("\n---------")

    def part_two(self):
        i = self.get_image()
        mask = np.zeroes(i[..., 0].shape)



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
    t2 = BIOS(s, 5, 5)
    assert(t2.part_one() == 80)

    print("Loading...")
    img = BIOS(read_image("zkamvar-input.txt"), height = 6, width = 25)
    assert(img.part_one() == 1935)
    print("Part 1: {}".format(img.part_one()))
    


