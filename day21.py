from aocd.models import Puzzle
import random
import string

def get_input(puzzle=None, mode="test"):
    if mode=="test":
        raw_data = """
Player 1 starting position: 4
Player 2 starting position: 8
""".strip().splitlines()
    else:
        raw_data = puzzle.input_data.splitlines()
    
    return [ Player(int(line.split(": ")[1])) for line in raw_data ]


class Player():

    def __init__(self, start, name=None):
        self.position = start
        self.score = 0
        self.name = name if name else f"Player {''.join(random.choices(string.ascii_lowercase, k=3))}"

    def __str__(self):
        return f"{self.name} is currently on space {self.position} and has score {self.score}"

    def __repr__(self):
        return str(self)

    def move(self, die, verbose=False):
        rolls = [next(die) for x in range(3)]
        moves = sum(rolls)
        intermediary_position = self.position + moves
        self.position = 10 if intermediary_position % 10 == 0 else intermediary_position % 10
        self.score += self.position
        
        if verbose:
            print(f"Player {self.name} rolls {rolls} and moves to space {self.position} for a total score of {self.score}.")


def infinite_sequence():
    num = 1
    while True:
        yield num
        num += 1
        if num > 100: num = 1


def play_game(players):
    WINNING_SCORE = 1000
    num_rolls = 0
    die = infinite_sequence()
    while True:
        for player in players:
            player.move(die, verbose=False)
            num_rolls += 3
            if player.score >= WINNING_SCORE:
                return player, num_rolls


def calculate_scores(players, winner, num_rolls):
    for player in players:
        if player != winner:
            return player.score * num_rolls


def main():
    puzzle = Puzzle(year=2021, day=21)

    #players = get_input()
    players = get_input(puzzle, mode="real") 
    print(players)

    ## PART ONE
    winner, num_rolls = play_game(players)
    game_score = calculate_scores(players, winner, num_rolls)
    print(game_score)






if __name__ == "__main__":
    main()  