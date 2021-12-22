from aocd.models import Puzzle


class Board():
    def __init__(self, lines):
        self.rows = [ line.split() for line in lines ]
        self.cols = [ list(line) for line in zip(*self.rows) ]
        self.numrows = len(self.cols[0])
        self.numcols = len(self.rows[0])
        self.nums = []
        for arr in self.rows:
            self.nums.extend(arr)

    def __str__(self):
        res = f"Rows: {self.rows}\nCols: {self.cols}\nNums: {self.nums}\n"
        return res

    def is_winner(self):
        for row in self.rows:
            if len(set(row)) == 1:
                return True

        for col in self.cols:
            if len(set(col)) == 1:
                return True                

    def mark(self, num):
        if num in self.nums:
            self.nums[self.nums.index(num)] = 'X'
            #self.rows = [ 'X' if num == mynum else mynum for row in self.rows for mynum in row ]
            for row in self.rows: 
                for mynum in row:
                    if num == mynum:
                        row[row.index(mynum)] = 'X'

            for col in self.cols: 
                for mynum in col:
                    if num == mynum:
                        col[col.index(mynum)] = 'X'                        

        return self.is_winner()

    def score(self, winning_num):
        return sum([ int(num) for num in self.nums if num != 'X' ]) * int(winning_num)


def get_input(puzzle=None, mode="test"):
    if mode=="test":
        return """
7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7    
""".splitlines()[1:]

    else:
        return puzzle.input_data.splitlines()


def build_game(data):
    numbers = data[0].split(",")

    boards = []
    first_board_starting_line = 2  # the first line of the input is the numbers followed by a blank line
    num_lines_btwn_board = 6
    num_lines_on_board = num_lines_btwn_board - 1
    for i in range(first_board_starting_line, len(data), num_lines_btwn_board):
        boards.append(Board(data[i:i+num_lines_on_board]))  

    return numbers, boards  


def play_game(numbers, boards, strategy="win"):
    if strategy == "win":
        for num in numbers:
            for board in boards:
                winner = board.mark(num)
                if winner:
                    return board.score(num)   
    else:
        for num in numbers:
            #print(f"There are {len(boards)} remaining; Called num {num}")
            for index, board in enumerate(boards[:]):
                winner = board.mark(num)
                #print(board)
                if winner: 
                    #print(f"Board {index} wins")
                    if len(boards) == 1:
                        return board.score(num)
                    else:
                        boards.remove(board)            
                    

def main():
    puzzle = Puzzle(year=2021, day=4)

    ### GET INPUT
    #data = get_input()   # test input
    data = get_input(puzzle, mode="real") # real input

    ### BUILD GAME
    numbers, boards = build_game(data)

    print(f"You have {len(boards)} boards")
    # for board in boards:
    #     print(board)
    #     print()
    #     break

    ### PLAY GAME
    # PART 1
    # score = play_game(numbers, boards)
    # print(f"Winning Score: {score}")

    # PART 2
    score = play_game(numbers, boards, strategy="lose")
    print(f"Losing Score: {score}")
                

if __name__ == "__main__":
    main()