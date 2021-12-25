from aocd.models import Puzzle
import random
import string

def get_input(puzzle=None, mode="test"):
    if mode=="test":
        raw_data = """
[1,2]
[[1,2],3]
[9,[8,7]]
[[1,9],[8,5]]
[[[[1,2],[3,4]],[[5,6],[7,8]]],9]
[[[9,[3,8]],[[0,9],6]],[[[3,7],[4,9]],3]]
[[[[1,3],[5,3]],[[1,3],[8,7]]],[[[4,9],[6,9]],[[8,2],[7,3]]]]        
""".strip().splitlines()
    else:
        raw_data = puzzle.input_data.splitlines()
    
    #print(raw_data)
    res = [ parse(line) for line in raw_data ]
    return res

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
    def __init__(self, value=None):
        self.left = None
        self.right = None
        self.value = value

    def __str__(self):
        return f"({'' if not self.left else self.left.value}, {'' if not self.right else self.right.value})"

    def __repr__(self):
        return str(self)

def inorder(root):
    if root is None:
        return
    inorder(root.left)
    print(root.value, end=' ')
    inorder(root.right)

def main():
    puzzle = Puzzle(year=2021, day=18)

    snail_list = get_input()
    #target_area = get_input(puzzle, mode="real") 

    for s in snail_list[1:2]:
        inorder(s)
        print()
        break




if __name__ == "__main__":
    main()  