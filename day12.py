from aocd.models import Puzzle
from collections import defaultdict, deque, Counter
from pprint import pprint

def get_input(puzzle=None, mode="test"):
    if mode=="test":
        raw_data = """
fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW
""".strip()

    else:
        raw_data = puzzle.input_data

    connections = [ line.split("-") for line in raw_data.splitlines()   ]

    graph = defaultdict(list)
    for v1, v2 in connections:
        graph[v1].append(v2)
        graph[v2].append(v1)
        
    return graph


def can_revisit(node, partAorB, path_so_far):
    if partAorB == "A":
        return node.isupper()
    else:
        if node.isupper():
            return True
        elif node in ["start", "end"]:
            return False
        else:
            most_common = Counter(path_so_far).most_common()
            for cave, count in most_common:
                if cave.islower() and count == 2:
                    return False
            return True



def dfs(start, end, graph, partAorB, verbose=False):
    paths = []
    if start not in graph.keys() or end not in graph.keys():
        print("Oops, one of those vertices does not exist")
        return paths

    # stack will contain tuples (node_name, parent, path_so_far)
    stack = []
 
    stack.append((start, None, f"{start}-"))

    while stack:
        current, parent, path_so_far = stack.pop()

        if current != end:
            neighbors_not_queued = [ (neighbor,current,path_so_far+neighbor+"-") for neighbor in graph[current] if neighbor not in path_so_far or can_revisit(neighbor, partAorB, path_so_far.split("-"))  ]
            stack.extend(neighbors_not_queued)
        else:
            paths.append(path_so_far)
            if verbose:
                print(path_so_far)
    return paths  


def main():
    puzzle = Puzzle(year=2021, day=12)

    #cavemap = get_input()
    cavemap = get_input(puzzle, mode="real") 
    pprint(cavemap)

    # PART A
    paths = dfs("start", "end", cavemap, "A", verbose=False)
    print("Part A", len(paths))

    # PART B
    paths = dfs("start", "end", cavemap, "B", verbose=False)
    print("Part B", len(paths))
    

if __name__ == "__main__":
    main()      