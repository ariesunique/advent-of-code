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
            pair=(left, right)
            stack.append(pair)
        elif ch.isdigit():
            stack.append(int(ch))
    return stack[0]

class Snailfish():
    all_snailfish = {}

    def __init__(self, pair=None, parent=None, nesting=0, left_or_right=None, xchild=None, ychild=None):
        if not pair and not xchild and not ychild:
            print("uh oh")
            return

        if xchild and ychild:
            self.xchild = xchild
            self.ychild = ychild
            self.name = "".join(random.choice(string.ascii_lowercase) for i in range(8))
            Snailfish.all_snailfish[self.name] = self
            return

        self.x = pair[0]
        self.y = pair[1]
        self.xType = "int" if isinstance(self.x, int) else "list"
        self.yType = "int" if isinstance(self.y, int) else "list"
        self.name = "".join(random.choice(string.ascii_lowercase) for i in range(8))
        self.parent = parent
        self.nesting = nesting
        self.left_or_right = left_or_right
        self.xchild = None
        self.ychild = None
        if self.xType == "list":
            self.xchild = Snailfish(self.x, parent=self.name, nesting=self.nesting+1, left_or_right="left")
        if self.yType == "list":
            self.ychild = Snailfish(self.y, parent=self.name, nesting=self.nesting+1, left_or_right="right")

        Snailfish.all_snailfish[self.name] = self

    def __add__(self, other):
        print(f"adding {self} and {other}")
        return Snailfish(xchild=self, ychild=other)

    def __str__(self):
        if self.xchild and self.ychild:
            res = f"\nSnailfish: {self.name}\nx is {repr(self.xchild)}\ny is {repr(self.ychild)}"
        else:
            res = f"\nSnailfish: {self.name}\nx is {self.x} type {self.xType}\ny is {self.y} type {self.yType};\nchild of {self.parent}\nI'm on the {self.left_or_right} \nnested level is {self.nesting}"
        return res

    def __repr__(self):
        if self.xchild and self.ychild:
            return str((self.xchild, self.ychild))
        return str((self.x, self.y))

    def explode(self):
        print("\nexploding")
        print("parent", Snailfish.all_snailfish[self.parent])
        number_on_the_right, sfname = self.get_number_on_the_right()
        number_on_the_left = self.get_number_on_the_left()
        print("right", number_on_the_right, "found in", sfname)
        if number_on_the_right:
            Snailfish.all_snailfish[sfname]
        print("left", number_on_the_left)
        

    def get_number_on_the_right(self):
        parent = Snailfish.all_snailfish[self.parent]
        while parent:
            if parent.yType == "int":
                return parent.y, parent.name
            parent = Snailfish.all_snailfish[parent.parent]

    def get_number_on_the_left(self):
        parent = Snailfish.all_snailfish[self.parent]
        if parent.xType == "int":
            return parent.x


def main():
    puzzle = Puzzle(year=2021, day=18)

    snail_list = get_input()
    #target_area = get_input(puzzle, mode="real") 

    # prev_snail = Snailfish(pair=snail_list[0])
    # for i in range(1, len(snail_list)):
    #     next_snail = Snailfish(pair=snail_list[i])
    #     prev_snail = prev_snail + next_snail
    #     #break
    # print(prev_snail)



    #     print(repr(snail))
    # print(len(Snailfish.all_snailfish))

    # parse("[[[[1,3],[5,3]],[[1,3],[8,7]]],[[[4,9],[6,9]],[[8,2],[7,3]]]]")

    sf1 = Snailfish(pair=[[6,[5,[4,[3,2]]]],1])
    print(sf1)
    # sf2 = Snailfish(pair=[7,9])
    # sf3 = sf1 + sf2

    #print("S3 is", sf3)

    # sf = Snailfish([1,2])
    # print(sf)

    # sf = Snailfish([[1,2],3])
    # print(sf)

    #print()
    #print(Snailfish.all_snailfish)

    print()
    for x in Snailfish.all_snailfish.values():
        if x.nesting == 4:
            print(x)
            x.explode()

    print()
    print(sf1)

    #print()
    #print(sf.xchild.name, sf.x)




if __name__ == "__main__":
    main()  