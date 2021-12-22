from aocd.models import Puzzle
from pprint import pprint
from collections import Counter

def get_input(puzzle=None, mode="test"):
    if mode=="test":
        raw_data = """
6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
""".strip()

    else:
        raw_data = puzzle.input_data
 
    lines= raw_data.splitlines()
    empty_index = lines.index("")

    coords = [ [ int(p) for p in line.split(",") ] for line in lines[:empty_index]  ]
    instructions = [ line.strip("fold along ") for line in lines[empty_index+1:] ]

    return coords, instructions

EMPTY = "."
MARKED = "#"

def init_grid(coords):
    maxX = max( x for x, y in coords  )
    maxY = max( y for x, y in coords  )

    grid = []
    for y in range(maxY+1):
        grid.append([EMPTY]*(maxX+1))

    return grid


def print_grid(grid):
    print()
    for line in grid:
        print("".join(line))
    print()    


def mark_paper(grid, coords):
    for x,y in coords:
        grid[y][x] = MARKED


def count_marks(grid):
    flattend_grid = [x for line in grid for x in line]
    return Counter(flattend_grid)[MARKED]

def horizontal_fold(grid, value):
    lines_to_keep = grid[:value]
    lines_to_transpose = grid[value:] # keeping the fold line here simplifies the math in line 76

    for index, line in enumerate(lines_to_transpose):
        line_to_modify = lines_to_keep[-1*index]
        for j, mark in enumerate(line):
            if mark == MARKED:
                line_to_modify[j] = MARKED

    return lines_to_keep


def vertical_fold(grid, value):
    
    new_grid = []
    grid_to_transpose = []
    for line in grid:
        new_grid.append(line[:value])
        grid_to_transpose.append(line[value:])

    for yindex, line in enumerate(grid_to_transpose):
        for xindex, mark in enumerate(line):
            if mark == MARKED:
                new_grid[yindex][-1*xindex] = MARKED

    return new_grid

def main():
    puzzle = Puzzle(year=2021, day=13)

    #coords, instructions = get_input()
    coords, instructions = get_input(puzzle, mode="real") 
    
    # pprint(coords[:5])
    # pprint(instructions[:5])

    grid = init_grid(coords)
    mark_paper(grid, coords)

    # fold_paper
    for line in instructions:
        axis, value_str = line.split("=")   
        if axis == "y":
            grid = horizontal_fold(grid, int(value_str))
        else:
            grid = vertical_fold(grid, int(value_str)) 
        
        
    print_grid(grid)
    #num_marks = count_marks(grid)
    #print(num_marks)


    

if __name__ == "__main__":
    main()      