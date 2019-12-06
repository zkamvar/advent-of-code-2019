#!usr/local/bin env python3


import io
import anytree as atree



def get_input(path):
    with io.open(path, "r") as f:
        data = f.readlines()
        f.close()
    
    nodes = dict()
    root = None
    
    for pair in data:
        parent, child = pair.strip().split(")")
        if parent in nodes:
            nodes[child] = atree.Node(child, parent = nodes[parent])
        else:
            nodes[parent] = atree.Node(parent) # root node
            if root is None:
                root = parent
            else:
                pass
            nodes[child] = atree.Node(child, parent = nodes[parent])

    return((root, nodes))


if __name__ == '__main__':

    (t1_root, t1) = get_input("test-input1.txt")
    for pre, fill, node in atree.RenderTree(t1[t1_root]):
        print("%s%s" % (pre, node.name))

    print([[node.name for node in children] for children in atree.LevelGroupOrderIter(t1[t1_root])])
