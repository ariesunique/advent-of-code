from collections import Counter
from aocd.models import Puzzle

def is_valid_point(point, data):
    row, col = point
    return row >= 0 and row < len(data) and col >= 0 and col < len(data[0])


def get_neighbors(row_index, col_index, data, include_self=False):
    # append (point, value)
    neighbors = []
    for i in range(row_index-1, row_index+2):
        for j in range(col_index-1, col_index+2):
            is_self = i == row_index and j == col_index
            if (not is_self) or (is_self and include_self):                
                same_col = j == col_index
                same_row = i == row_index
                if (same_col or same_row) and is_valid_point((i,j), data):
                    neighbors.append( ((i,j), int(data[i][j])) )

    return neighbors

def get_input(puzzle=None, mode="test"):
    if mode=="test":
        data = """
2199943210
3987894921
9856789892
8767896789
9899965678
""".splitlines()[1:]

    else:
        data = puzzle.input_data.splitlines()
    
    return data


def main():
    puzzle = Puzzle(year=2021, day=9)

    #data = get_input()
    data = get_input(puzzle, mode="real") # real input 

    """
    window function
    (-1,-1) (-1,0) (-1,1)
    (0,-1)  (0,0) (0,1)
    (1,-1)  (1,0) (1,1)
    """

    # PART A
    low_points_and_values = set()
    for row_index in range(-1,len(data)):
        for col_index in range(-1, len(data[0])):
            if is_valid_point((row_index, col_index), data):
                curr_point = (row_index, col_index)
                neighbors = get_neighbors(row_index, col_index, data, include_self=True)
                # each neighbor is a tuple like this (point, val); we need to compare the values
                (lowest_point, lowest_val) = min(neighbors, key=lambda x: x[1])
                if lowest_point == curr_point:
                    low_points_and_values.add((lowest_point, lowest_val))

    ans = sum( [lowest_val+1 for (lowest_point, lowest_val) in low_points_and_values] )
    #print(low_points_and_values)
    print(f"Part A ans: {ans}")

    # PART B
    basin_sizes = { lowest_point:0 for (lowest_point, lowest_val) in low_points_and_values  }
   
    # do a DFS starting from each basin
    for key in basin_sizes:
        seen = set()
        points_to_process = [key]
        while points_to_process:
            point = points_to_process.pop()
            if point not in seen:
                seen.add(point)
                basin_sizes[key] += 1

            neighbor_list = get_neighbors(*point, data)
            points_to_process.extend([point for (point, val) in neighbor_list if val!=9 and point not in seen])
        
    prod = 1
    for (lowest_point, num_basins) in Counter(basin_sizes).most_common(3):
        prod *= num_basins
    
    print(f"Part B ans: {prod}")




if __name__ == "__main__":
    main()   