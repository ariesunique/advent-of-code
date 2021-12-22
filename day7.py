from aocd.models import Puzzle

def get_input(puzzle=None, mode="test"):
    if mode=="test":
        return [ int(i) for i in "16,1,2,0,4,2,7,1,2,14".split(",") ]

    else:
        return [ int(i) for i in puzzle.input_data.split(",") ]


def get_best_position_partA(data):
    best_position = None
    min_cost = None
    for i in range(max(data)+1):
        cost = sum([ abs(pos-i) for pos in data])
        if min_cost is None or cost < min_cost:
            min_cost = cost
            best_position = i
    return best_position, min_cost


def get_best_position_partB(data):
    best_position = None
    min_cost = None
    cost_map = { i:sum(range(i+1)) for i in range(max(data)+1)  }
    # print(cost_map)
    for i in range(max(data)+1):
        cost = sum([ cost_map[abs(pos-i)] for pos in data])
        #print(f"{i}\t{cost}")
        if min_cost is None or cost < min_cost:
            min_cost = cost
            best_position = i
    return best_position, min_cost


def main():
    puzzle = Puzzle(year=2021, day=7)

    #data = get_input()
    data = get_input(puzzle, mode="real") # real input  
    #print(data[:15])

    # pos, cost = get_best_position_partA(data)
    # print(f"Best position is {pos} with cost of {cost}")
    
    pos, cost = get_best_position_partB(data)
    print(f"Best position is {pos} with cost of {cost}")

if __name__ == "__main__":
    main()