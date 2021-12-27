from aocd.models import Puzzle
import random
import string
from pprint import pprint
import sys

def get_input(puzzle=None, mode="test"):
    if mode=="test":
        raw_data = """
[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]
""".strip().splitlines()
    else:
        raw_data = puzzle.input_data.splitlines()
    
    #print(raw_data)
    list_of_snailfish_trees = [ parse(line) for line in raw_data ]
    return list_of_snailfish_trees

OPEN = "["
CLOSE = "]"
def parse(line):
    stack = []
    for ch in line:
        if ch == OPEN:
            stack.append(ch)
        elif ch == CLOSE:
            right = stack.pop()
            left = stack.pop()
            _ = stack.pop()

            parent = Node(f"({left},{right})")
            parent.left = Node(left) if isinstance(left, int) else left
            parent.right = Node(right) if isinstance(right, int) else right
            stack.append(parent)

        elif ch.isdigit():
            stack.append(int(ch))
    return stack[0]


class Node():
    all_snailfish = {}

    def __init__(self, value=None):
        self.left = None
        self.right = None
        self.value = value
        self.name = self.generate_name()
        Node.all_snailfish[self.name] = self

    def __str__(self):
        return f"({'' if not self.left else self.left.value}, {'' if not self.right else self.right.value})" if self.left or self.right else str(self.value)

    def __repr__(self):
        return str(self)

    def __add__(self, other):
        new_node = Node(f"({self},{other})")
        new_node.left = self
        new_node.right = other
        return new_node

    def generate_name(self):
        return "".join(random.choices(string.ascii_lowercase, k=6))

    def reset_value(self):
        if not isinstance(self.value, int):
            self.value = str(self)


def inorder(root, parent=None, level=0, ordered_tree=[]):
    if root is None:
        return
    #print(f"getting order for {root}: my left is {root.left}; my right is {root.right}")
    inorder(root.left, parent=root.name, level=level+1, ordered_tree=ordered_tree)
    #print(f"{root.name}, {root.value}, Level {level} ")
    ordered_tree.append((root.name,root.value,level, parent))
    inorder(root.right, parent=root.name, level=level+1, ordered_tree=ordered_tree)
    root.reset_value()


def update_neighbor(ordered_snail_tree, startindex, direction, value_to_add):
    for name, value, _, parent in ordered_snail_tree[startindex::direction]:
        if isinstance(value, int):
            node_to_update = Node.all_snailfish[name]
            node_to_update.value += value_to_add
            #parent_node = Node.all_snailfish[parent] 
            #parent_node.value = f"({parent_node.left},{parent_node.right})"
            break


def splitInt(ordered_snail_tree, index):
    name, value, level, parent = ordered_snail_tree[index]
    #print(f"\nspliting int {name} {value}")
    
    current_node = Node.all_snailfish[name] 
    parent_node = Node.all_snailfish[parent] 

    left_value = value//2
    right_value = value - value//2
    new_left_node = Node(left_value)
    new_right_node = Node(right_value)
    new_node = Node(f"({left_value},{right_value})")
    new_node.left = new_left_node
    new_node.right = new_right_node
    
    if parent_node.left == current_node:
        parent_node.left = new_node
    else:
        parent_node.right = new_node
    #parent_node.value = f"({parent_node.left},{parent_node.right})"

    del Node.all_snailfish[name]    
    #print("done splitting int")


def explodePair(ordered_snail_tree, index):
    name, value, level, parent = ordered_snail_tree[index]
    current_node = Node.all_snailfish[name]
    #print(f"\nexploding {name} {current_node}")

    left_neighbor = None
    right_neighbor = None
    if index-2 > 0:
        update_neighbor(ordered_snail_tree, index-2, -1, current_node.left.value)

    if index+2 < len(ordered_snail_tree):
        update_neighbor(ordered_snail_tree, index+2, 1, current_node.right.value)

    parent_node = Node.all_snailfish[parent]
    #print("parent",parent_node)
    if parent_node.left == current_node:
        parent_node.left = Node(0)
    else:
        parent_node.right = Node(0)
    #del ordered_snail_tree[index]
    #print(f"Update {parent_node} value to {({parent_node.left},{parent_node.right})}")
    #parent_node.value = f"({parent_node.left},{parent_node.right})"
    #print(f"Now it's {parent_node}")
    del Node.all_snailfish[current_node.left.name]
    del Node.all_snailfish[current_node.right.name]
    del Node.all_snailfish[name]


def reduce(snailfish):
    done = False
    while not done:
        ordered_snail_tree = []
        inorder(snailfish, ordered_tree=ordered_snail_tree)        
        for index1, (name, value, level, parent) in enumerate(ordered_snail_tree):
            if not isinstance(value, int) and level >= 4:  
                explodePair(ordered_snail_tree, index1)
                break
        if index1 < len(ordered_snail_tree)-1: 
            continue
        for index2, (name, value, level, parent) in enumerate(ordered_snail_tree):
            if isinstance(value, int) and value >= 10:
                splitInt(ordered_snail_tree, index2)
                break
        if index2 == len(ordered_snail_tree)-1: 
            done=True
    # just to update the display - turn off when running on large input
    #inorder(snailfish, ordered_tree=ordered_snail_tree)


def main():
    puzzle = Puzzle(year=2021, day=18)

    snail_list = get_input()
    #target_area = get_input(puzzle, mode="real") 

    #print(Node.all_snailfish)
    res = snail_list[0]
    for sf in snail_list[1:]:
        #print(f"Adding {res} and {sf}")
        res = res + sf
        reduce(res)
        # need to call again to fix the very last pair in the sequence, should that one need splitting or exploding
        reduce(res)
        

    print("\n",res)
    # ordered_snail_tree = []
    # inorder(res, ordered_tree=ordered_snail_tree)
    # pprint(ordered_snail_tree)     

    # sf1 = parse("[[[[4,3],4],4],[7,[[8,4],9]]]")
    # sf2 = parse("[1,1]")
    # sf3 = sf1 + sf2
    # print(sf3)
    # print("all snailfish", len(Node.all_snailfish))
    # reduce(sf3)

    # print("\nUpdated\n")
    # ordered_snail_tree = []
    # inorder(res, ordered_tree=ordered_snail_tree)
    # pprint(ordered_snail_tree)   
    # print("all snailfish", len(Node.all_snailfish))     
    #pprint(Node.all_snailfish)

    # for key, x in Node.all_snailfish.items():
    #     print(f"{x.value} => Left: {x.left}; Right: {x.right}")




if __name__ == "__main__":
    main()  