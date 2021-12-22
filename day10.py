from aocd.models import Puzzle
from collections import Counter

char_open_close_map = {"(":")", "[":"]", "{":"}", "<":">"}

illegal_char_score_map = {")":3, "]":57, "}":1197, ">":25137}

autocomplete_char_score_map = {")":1, "]":2, "}":3, ">":4}

def get_input(puzzle=None, mode="test"):
    if mode=="test":
        data = """
[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]
""".splitlines()[1:]

    else:
        data = puzzle.input_data.splitlines()
    
    return data

def is_open_char(ch):
    return ch in char_open_close_map.keys()

def partition(data):
    corrupted = []
    incomplete = []

    for line in data:
        syntax_score = get_syntax_score(line)
        if syntax_score:
            corrupted.append( (line,syntax_score)  )
        else:
            incomplete.append(line)
    
    return corrupted, incomplete


def get_syntax_score(line):
    seen = []
    for ch in line:
        if is_open_char(ch):
            seen.append(ch)
        else:
            last_open_char = seen.pop()
            if ch != char_open_close_map[last_open_char]:
                #print(f"found corrupted line\t{line}")
                return illegal_char_score_map[ch]
    # if we get here, we have an incomplete line 
    return 0

def get_completion_score(line):
    seen = []
    for ch in line:
        if is_open_char(ch):
            seen.append(ch)
        else:
            last_open_char = seen.pop()
            assert( ch == char_open_close_map[last_open_char] )

    # if we get here, we have an incomplete line 
    completion_sequence = []
    while seen:
        completion_sequence.append( char_open_close_map[seen.pop()] )
    
    score = 0
    for ch in completion_sequence:
        score = score * 5 + autocomplete_char_score_map[ch]

    #print("".join(completion_sequence), score)

    return score    


def main():
    puzzle = Puzzle(year=2021, day=10)

    data = get_input()
    #data = get_input(puzzle, mode="real") # real input 
    #print(data[:5])    

    # PART A
    # ans = sum( [get_syntax_score(line) for line in data] )
    # print(ans)

    # Parts A and B
    corrupted, incomplete = partition(data)
    partA_ans = sum( [score for (line, score) in corrupted]  )
    print(f"Part A answer is {partA_ans}")

    completion_scores = sorted([ get_completion_score(line) for line in incomplete  ])
    middle_score = completion_scores[  len(completion_scores)//2  ]
    print(f"Part B answer is {middle_score}")



if __name__ == "__main__":
    main()     