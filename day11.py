from aocd.models import Puzzle
from pprint import pprint
from collections import Counter

GRID_WIDTH = 10
GRID_HEIGHT = 10

FLASH_ENERGY_LEVEL = 10

def get_input(puzzle=None, mode="test"):
    if mode=="test":
        raw_data = """
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
""".strip()

    else:
        raw_data = puzzle.input_data

    data = [ [ int(ch) for ch in line ] for line in raw_data.splitlines() ] 
    
    return data


def get_flashing_octos(data):
    flashing_octos = []
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            if data[row][col] == FLASH_ENERGY_LEVEL:
                flashing_octos.append((row,col))
    return flashing_octos


def get_flashing_octos_specific_locations(data, positions):
    flashing_octos = []
    for (row, col) in positions:
        if data[row][col] == FLASH_ENERGY_LEVEL:
            flashing_octos.append((row,col))
    return flashing_octos


def ongrid(row, col):
    return row >= 0 and row < GRID_HEIGHT and col >= 0 and col < GRID_WIDTH

"""
window function
(-1,-1) (-1,0) (-1,1)
(0,-1)  (0,0) (0,1)
(1,-1)  (1,0) (1,1)
"""
def get_neighbors(row, col):
    neighbors = []
    for row_index in range(-1,2):
        for col_index in range(-1, 2):
            neighbor = (row + row_index, col + col_index)
            is_self = neighbor == (row, col)
            if not is_self and ongrid(*neighbor):
                neighbors.append(neighbor)
    return neighbors


def increase_energy_levels(data, positions):
    for (row, col) in positions:
        data[row][col] += 1


def all_flashing(data):
    zero_count = Counter([num for line in data for num in line])[0]
    return zero_count == GRID_WIDTH * GRID_HEIGHT


def simulate(data, num_steps, display=False, display_type="LAST"):
    # display_type options are [LAST, ALL]

    if display and display_type == "ALL":
        pprint(data)

    flashes_per_step = []
    for i in range(num_steps):
        if display and display_type == "ALL":
            print(f"\nStep {i+1}")

        # increase the energy level of each octopus by 1
        data = [ [num+1 for num in line] for line in data ]

        # keep track of the octopuses that flash during this step, stored as tuples (row, col)
        flashes_already_counted = set()
        
        # flashing_octos is a list of octopuses that recently started flashing 
        #     this is a list of tuples (row, col) indicating the octo's position     
        flashing_octos = get_flashing_octos(data)
        
        while flashing_octos:
            current_flashing_octo = flashing_octos.pop()
            flashes_already_counted.add(current_flashing_octo)
            neighbors = get_neighbors(*current_flashing_octo)
            increase_energy_levels(data, neighbors)
            newly_flashing_octos = get_flashing_octos_specific_locations(data, neighbors)
            flashing_octos.extend(newly_flashing_octos)
            
        # reset the energy levels for octopuses that flashed
        data = [ [0 if num >= FLASH_ENERGY_LEVEL else num for num in line] for line in data ]
        
        # count num flashes for this step
        flashes_per_step.append(len(flashes_already_counted))

        if display and display_type == "ALL":
            pprint(data)
        
        if all_flashing(data):
            print(f"At step {i+1}, all octopuses flash simultaneously!!")
            break
    
    if display and display_type == "LAST":
        print(f"After step {i+1}:")
        pprint(data)

    return sum(flashes_per_step)


def main():
    puzzle = Puzzle(year=2021, day=11)

    #data = get_input()
    data = get_input(puzzle, mode="real") # real input 
    #pprint(data)

    num_steps = 100
    num_flashes = simulate(data, num_steps, display=True)
    print(num_flashes)
    

if __name__ == "__main__":
    main()  