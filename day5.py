from collections import Counter
from aocd.models import Puzzle

def get_input(puzzle=None, mode="test"):
    if mode=="test":
        raw_input = """
0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2   
""".splitlines()[1:]

    else:
        raw_input = puzzle.input_data.splitlines()
    
    data = []
    for points in raw_input:
        point1, point2 = points.split("->")
        x1,y1 = list(map(lambda x: int(x), point1.split(",")))
        x2,y2 = list(map(lambda x: int(x), point2.split(",")))
        data.append([(x1,y1),(x2,y2)])
    return data

def main():
    puzzle = Puzzle(year=2021, day=5)

    #data = get_input()   # test input
    data = get_input(puzzle, mode="real") # real input  

    all_points_on_any_line = []
    for v in data:
        (x1, y1), (x2, y2) = v[0], v[1]
        is_horiz = y1 == y2
        is_vert = x1 == x2
        if is_horiz:
            (x_start, x_end) = (x1, x2) if x2 > x1 else (x2, x1)
            for x in range(x_start,x_end+1):
                all_points_on_any_line.append((x, y1))
        elif is_vert:
            (y_start, y_end) = (y1, y2) if y2 > y1 else (y2, y1)
            for y in range(y_start,y_end+1):
                all_points_on_any_line.append((x1, y))
        else:
            if x2 > x1:
                (x_start, y_start) = (x1, y1)
                (x_end, y_end) = (x2, y2)
            else:
                (x_start, y_start) = (x2, y2)
                (x_end, y_end) = (x1, y1)
            y_delta = 1 if y_end > y_start else -1
            all_points_on_any_line.append((x_start, y_start))
            for delta in range(1, x_end-x_start+1):
                all_points_on_any_line.append((x_start+delta, y_start+delta*y_delta))
                
    # print("Points on line")
    # print(all_points_on_any_line)
    # print(len(all_points_on_any_line))

    counter = Counter(all_points_on_any_line)
    danger_pts = [ (pt) for pt, count in counter.items() if count >= 2 ]
    #print(danger_pts)
    print(len(danger_pts))

if __name__ == "__main__":
    main()