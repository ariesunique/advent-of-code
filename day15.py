from aocd.models import Puzzle
from pprint import pprint
from collections import deque
import heapq as hq
import math
import itertools

grid = []
SIZE_FACTOR = 5
#current_location_in_larger_grid = (0,0)
#larger_grid = [ [0]*SIZE_FACTOR for i in range(SIZE_FACTOR) ]

def get_input(puzzle=None, mode="test"):
    if mode=="test":
        raw_data = """
1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
""".strip()

    else:
        raw_data = puzzle.input_data
        
    #grid = [ [ int(x) for x in line] for line in raw_data.splitlines() ]

    for line in raw_data.splitlines():
        grid.append([ int(x) for x in line])

    #pprint(grid)
    print(f"Size of your input is {len(grid)} x {len(grid[0])}")
    #return grid

def on_grid(x, y):
    return x >= 0 and x < len(grid) and y >= 0 and y < len(grid[0])


"""
window function
(-1,-1) (-1,0) (-1,1)
(0,-1)  (0,0)  (0,1)
(1,-1)  (1,0)   (1,1)
"""
def _get_neighbors(grid, x, y):
    neighbors = []
    for i in range(-1,2):
        for j in range(-1,2):
            move_down = i==0 and j>0
            move_right = j==0 and i>0
            is_self = i==0 and j==0
            neighbor = (x+i, y+j)
            if not is_self and (move_down or move_right) and on_grid( *neighbor):
                neighbors.append(neighbor)
    return neighbors


def get_value(grid, x, y):
    return grid[x][y]


"""Naive solution 1"""
def _find_path(grid, start=(0,0), end=None):
    if not end:
        end = (len(grid)-1, len(grid[0])-1 )
    print(f"find cheapest path from {start} to {end}")

    # each item is a tuple (path_so_far, total_risk_so_far)
    possible_paths = []

    # each item in queued is a tuple
    # (position, parent, value, path-so-far, total-risk-so-far)    
    queued = deque()

    # the items here are just the positions
    queued_positions = deque()

    # the items here are just the positions
    seen = []

    queued.append((start, None, 0, str(start), 0))
    queued_positions.append(start)
    
    count = 0
    while queued and count < 500000  :
        count += 1
        curr_position, parent, value, path_so_far, total_risk_so_far = queued.popleft()
        _ = queued_positions.popleft()
        seen.append(curr_position)

        #print(f"\n{count}: processing {curr_position}")
        if curr_position == end:
            # found a path
            #print(f"{count} found a path")
            possible_paths.append((path_so_far, total_risk_so_far))
            #break

        neighbors = _get_neighbors(grid, *curr_position)
        #print(f"neighbors of {curr_position} are {neighbors}")
        for neighbor in neighbors:
            if str(neighbor) not in path_so_far:
                #print(f"adding {neighbor} to queue")
                neighbor_value = get_value(grid, *neighbor)
                queued.append((neighbor, curr_position, neighbor_value, f"{path_so_far}-{neighbor}", total_risk_so_far+neighbor_value))
                queued_positions.append(neighbor)       
        #print(f"queued: {queued_positions}")
        #pprint(queued_positions)
        #pprint(queued)

    print(f"\nAfter {count} iterations, Found {len(possible_paths)} possible paths")  
    for path, risk in possible_paths:
        print(path, risk)


### Bad dfs attempt
def get_neighbors(grid, x, y):
    neighbors = [ ]
    for i in range(-1,2):
        for j in range(-1,2):
            move_vert = i==0 
            move_horiz = j==0 
            is_self = i==0 and j==0
            neighbor = (x+i, y+j)
            if not is_self and (move_vert or move_horiz) and on_grid( *neighbor):
                neighbors.append(neighbor)
    return neighbors

def get_cheapest_neighbor(grid, neighbors, path_so_far):
    best_move = None
    best_val = None
    for x,y in neighbors:
        if (best_val == None or grid[x][y] < best_val) and str((x,y)) not in path_so_far:
            best_val = grid[x][y]
            best_move = (x,y)
    print(f"of {neighbors}, cheapest is {best_move} valued at {best_val}")
    return best_move, best_val

def dfs_find_path(grid, start=(0,0), end=None):
    if not end:
        end = (len(grid)-1, len(grid[0])-1 )
    print(f"find cheapest path from {start} to {end}")

    # each item is a tuple (path_so_far, total_risk_so_far)
    possible_paths = []

    # each item in queued is a tuple
    # (position, parent, value, path-so-far, total-risk-so-far)    
    stack = []

    # the items here are just the positions
    stacked_positions = []

    # the items here are just the positions
    seen = []

    stack.append((start, None, 0, str(start), 0))
    stacked_positions.append(start)
    
    count = 0
    while stack and count < 500000  :
        count += 1
        curr_position, parent, value, path_so_far, total_risk_so_far = stack.pop()
        _ = stacked_positions.pop()
        seen.append(curr_position)

        print(f"\n{count}: processing {curr_position}")
        if curr_position == end:
            # found a path
            print(f"{count} found a path")
            possible_paths.append((path_so_far, total_risk_so_far))
            break

        neighbors = get_neighbors(grid, *curr_position)
        print(f"neighbors of {curr_position} are {neighbors}")
        cheapest_neighbor, neighbor_value = get_cheapest_neighbor(grid, neighbors, path_so_far)
        if cheapest_neighbor:
            stack.append((cheapest_neighbor, curr_position, neighbor_value, f"{path_so_far}-{cheapest_neighbor}", total_risk_so_far+neighbor_value))
            stacked_positions.append(cheapest_neighbor)         
        pprint(stacked_positions)
        pprint(stack)

    print(f"\nAfter {count} iterations, Found {len(possible_paths)} possible paths")  
    for path, risk in possible_paths:
        print(path, risk)

### Bad dfs attempt







def find_path(grid, start=(0,0), end=None):
    if not end:
        end = (len(grid)-1, len(grid[0])-1 )
    print(f"find cheapest path from {start} to {end}")

    # this is a heapq (ie priority queue); each item in queued is a tuple
    # (total-risk-so-far, path-so-far, position  )    
    h = []

    # the items here are just the positions
    seen = []

    hq.heappush(h, (0, str(start), start ))
    
    count = 0
    while h  :
        count += 1
        total_risk_so_far, path_so_far, curr_position  = hq.heappop(h)
        seen.append(curr_position)

        #print(f"\n{count}: processing {curr_position}")
        if curr_position == end:
            # found a path
            print(f"Iteration {count} found a path")
            print("risk", total_risk_so_far)
            print("path:", path_so_far)
            break

        neighbors = get_neighbors(grid, *curr_position)
        #print(f"neighbors of {curr_position} are {neighbors}")
        for neighbor in neighbors:
            if str(neighbor) not in path_so_far:
                #print(f"adding {neighbor} to queue")
                neighbor_value = get_value(grid, *neighbor)
                hq.heappush(h, (total_risk_so_far+neighbor_value, f"{path_so_far}-{neighbor}", neighbor ))
        #pprint(h)






"""
borrowed from https://docs.python.org/3/library/heapq.html
"""
entry_finder = {}               # mapping of tasks to entries
REMOVED = '<removed-task>'      # placeholder for a removed task
counter = itertools.count()     # unique sequence count

def add_task(heap, task, priority=0):
    'Add a new task or update the priority of an existing task'
    if task in entry_finder:
        remove_task(task)
    count = next(counter)
    entry = [priority, count, task]
    entry_finder[task] = entry
    hq.heappush(heap, entry)

def remove_task(task):
    'Mark an existing task as REMOVED.  Raise KeyError if not found.'
    entry = entry_finder.pop(task)
    entry[-1] = REMOVED

def pop_task(heap):
    'Remove and return the lowest priority task. Raise KeyError if empty.'
    while heap:
        priority, count, task = hq.heappop(heap)
        if task is not REMOVED:
            del entry_finder[task]
            return priority, task
    raise KeyError('pop from an empty priority queue')

"""
My implementation after reading this: https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm#Algorithm 
"""
def dijkstra(start=(0,0), end=None):
    if not end:
        end = (len(grid)-1, len(grid[0])-1 )
    print(f"find cheapest path from {start} to {end}")

    unvisited_heap = []
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if x==0 and y==0:
                add_task(unvisited_heap, (x,y), priority=0)
            else:
                add_task(unvisited_heap, (x,y), priority=math.inf)
    
    count = 0
    while unvisited_heap:
        count+= 1
        total_risk_so_far, current_node = pop_task(unvisited_heap)
        neighbors = neighbors_partA(*current_node)

        for neighbor in neighbors:
            if neighbor in entry_finder:
                neighbor_risk = grid[neighbor[0]][neighbor[1]]
                tentative_risk_so_far_for_neighbor, _, _ = entry_finder[neighbor]
                if total_risk_so_far+neighbor_risk < tentative_risk_so_far_for_neighbor:
                    if neighbor == end:
                        print(f"iteration {count} updating {neighbor} to {total_risk_so_far+neighbor_risk}")
                        return total_risk_so_far+neighbor_risk
                    add_task(unvisited_heap, neighbor, priority=total_risk_so_far+neighbor_risk)

    print("No path found")

def neighbors_partA( x, y):
    return [  point for point in [(x-1,y), (x+1,y), (x,y-1), (x,y+1)] if on_grid( *point) ]


############

partb_path = [
(0,0,0,0),
(0,0,1,0),
(0,0,2,0),
(0,0,3,0),
(0,0,4,0),
(0,0,5,0),
(0,0,6,0),
(0,0,7,0),
(0,0,8,0),
(0,0,9,0),
(1,0,0,0),
(1,0,1,0),
(1,0,2,0),
(1,0,2,1),
(1,0,2,2),
(1,0,3,2),
(1,0,3,3),
(1,0,4,3),
(1,0,5,3),
(1,0,6,3),
(1,0,6,4),
(1,0,6,5),
(1,0,6,6),
(1,0,6,7),
(1,0,6,8),
(1,0,6,9),
(1,0,7,9),
(1,0,8,9),
(1,1,8,0),
(1,1,8,1),
(1,1,8,2),
(1,1,9,2),
(1,1,9,3),
(1,1,9,4),
(2,1,0,4),
(2,1,1,4),
(2,1,1,5),
(2,1,2,5),
(2,1,2,6),
(2,1,3,6),
(2,1,4,6),
(2,1,5,6),
(2,1,5,7),
(2,1,5,8),
(2,1,5,9),
(2,1,6,9),
(2,1,7,9),
(2,1,8,9),
(2,2,8,0),
(2,2,8,1),
(2,2,8,2),
(2,2,9,2),
(2,2,9,3),
(2,2,9,4),
(3,2,0,4),
(3,2,0,5),
(3,2,0,6),
(3,2,0,7),
(3,2,1,7),
(3,2,2,7),
(3,2,3,7),
(3,2,3,8),
(3,2,3,9),
(3,2,4,9),
(3,3,4,0),
(3,3,4,1),
(3,3,4,2),
(3,3,5,2),
(3,3,6,2),
(3,3,6,3),
(3,3,7,3),
(3,3,7,4),
(3,3,8,4),
(3,3,9,4),
(3,3,9,5),
(3,3,9,6),
(3,3,9,7),
(4,3,0,7),
(4,3,1,7),
(4,3,2,7),
(4,3,3,7),
(4,3,3,8),
(4,3,3,9),
(4,4,3,0),
(4,4,3,1),
(4,4,4,1),
(4,4,5,1),
(4,4,6,1),
(4,4,6,2),
(4,4,7,2),
(4,4,7,3),
(4,4,7,4),
(4,4,7,5),
(4,4,8,5),
(4,4,9,5),
(4,4,9,6),
(4,4,9,7),
(4,4,9,8),
(4,4,9,9)
]

def dijkstra_partB(start, end):

    print(f"find cheapest path from {start} to {end}")

    unvisited_heap = []
    for i in range(SIZE_FACTOR):
        for j in range(SIZE_FACTOR):
            for x in range(len(grid)):
                for y in range(len(grid[0])):
                    if i ==0 and j==0 and x==0 and y==0:
                        add_task(unvisited_heap, (i, j, x,y), priority=0)
                    else:
                        add_task(unvisited_heap, (i, j, x,y), priority=math.inf)
    
    #pprint(unvisited_heap[705:715])
    count = 0
    while unvisited_heap  :
        count+= 1
        try:
            total_risk_so_far, current_node = pop_task(unvisited_heap)
        except:
            print(f"exception on iteration {count}", total_risk_so_far, current_node)
            break
        
        neighbors = neighbors_partB(*current_node)

        # if current_node in partb_path:
        #     print(f"iteration {count} processing {current_node} with risk {total_risk_so_far} and value {get_risk(*current_node)}")
        # if current_node in  [(1,0,8,9)]:
        #     print(f"neighbors are {neighbors}")

        for neighbor in neighbors:
            if neighbor in entry_finder:
                neighbor_risk = get_risk(*neighbor)
                tentative_risk_so_far_for_neighbor, _, _ = entry_finder[neighbor]
                if total_risk_so_far+neighbor_risk < tentative_risk_so_far_for_neighbor:
                    if neighbor == end:
                        #print(f"iteration {count} updating {neighbor} to {total_risk_so_far+neighbor_risk}")
                        #pprint(unvisited_heap)
                        return total_risk_so_far+neighbor_risk
                    # if neighbor in [(1,0,8,9)]:
                    #     print(f"updating value for {neighbor} to {total_risk_so_far+neighbor_risk}")
                    add_task(unvisited_heap, neighbor, priority=total_risk_so_far+neighbor_risk)

    #pprint(unvisited_heap)
    print("No path found")

def neighbors_partB(i, j, x, y):
    neighbors = []
    for newX, newY in [(x-1,y), (x+1,y), (x,y-1), (x,y+1)]:
        if newX >= 0 and newX < len(grid) and newY >= 0 and newY < len(grid[0]):
            neighbors.append((i,j,newX,newY))
        elif newX < 0 and i-1 >= 0:
            # to the left of the current grid
            newX = len(grid) - 1
            neighbors.append((i-1, j, newX, newY))
        elif newX >= len(grid) and i+1 < SIZE_FACTOR:
            # to the right of the current grid
            newX = 0
            neighbors.append((i+1, j, newX, newY))
        elif newY < 0 and j-1 >=0:
            # above the current grid
            newY = len(grid[0]) -1
            neighbors.append((i, j-1, newX, newY))
        elif newY >= len(grid[0]) and j+1 < SIZE_FACTOR:
            # below the current grid
            newY = 0
            neighbors.append((i, j+1, newX, newY))
    return neighbors



def get_risk(i, j, x, y):
    if i==0 and j==0:
        return grid[x][y]
    basenum = grid[x][y]
    basenum += i
    if basenum > 9:
        basenum -= 9
    basenum += j
    if basenum > 9:
        basenum -= 9
    return basenum    


# grid = []
def main():
    puzzle = Puzzle(year=2021, day=15)

    #get_input()
    get_input(puzzle, mode="real") 
    #pprint(grid)

    # Part A
    # ans = dijkstra()
    # print(ans)

    # Part B
    ans = dijkstra_partB((0,0,0,0), (SIZE_FACTOR-1, SIZE_FACTOR-1, len(grid)-1, len(grid[0])-1))
    print(ans)


if __name__ == "__main__":
    main()  