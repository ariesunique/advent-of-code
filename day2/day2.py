"""
ANS: 1982495697
BRUTE-FORCE SOLUTION
no functions, just a single block of code

# input = '''
# forward 5
# down 5
# forward 8
# up 3
# down 8
# forward 2
# '''
# commands = [ str for str in input.strip().split("\n") ]  

with open("input.txt") as f:
    input = f.readlines()
commands = [ str.strip() for str in input ]   


xdirs = {"forward":1}
aimdirs = {"down":1, "up":-1}
 

x = 0
y = 0
aim = 0
for command in commands:
    dir, val = command.split()
    val = int(val)
    x += xdirs.get(dir, 0) * val
    aim += aimdirs.get(dir, 0) * val
    if dir == "forward":
        y += aim * val    

    #print(x, y, aim)
print("\nres", x,y,x*y)
"""

import math
def read_input(mode):
    if mode=="TEST":
        input = '''
forward 5
down 5
forward 8
up 3
down 8
forward 2
        '''
        return [ str for str in input.strip().split("\n") ] 
    else:
        with open("input.txt") as f:
            input = f.readlines()
        return [ str.strip() for str in input ]  

pos = (0, 0)
aim = 0

def forward(val):
    global pos, aim
    pos = (pos[0]+val, pos[1]+aim*val)

def down(val):
    global aim 
    aim += val

def up(val):
    global aim
    aim -= val

cmd_func_map = {"forward":forward, "up":up, "down": down}

def main(mode=None):
    commands = read_input(mode)
    print(commands[:10])
    for command in commands:
        f, val = command.split()
        val = int(val)
        cmd_func_map.get(f)(val)
    print(pos, math.prod(pos))

if __name__ == "__main__":
    main()

