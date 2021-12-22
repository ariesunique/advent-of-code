from aocd.models import Puzzle
from collections import Counter, defaultdict

class LanternfishPopulation_PartA():
    NEW_TIMER = 8
    RESET_TIMER = 6

    # fish_pop is a list of ints
    def __init__(self, fish_pop):
        self.population = fish_pop

    def spawn_new_fish(self, num_new_fish):
        for i in range(num_new_fish):
            self.population.append(self.NEW_TIMER)

    def age_fish(self):
        num_new_fish = Counter(self.population)[0]
        self.population = [ fish-1 if fish > 0 else self.RESET_TIMER for fish in self.population ] 
        self.spawn_new_fish(num_new_fish)
        
    def __str__(self):
        return str(self.population)

    def __len__(self):
        return len(self.population)  

    def simulate(self, num_days, verbose=False):
        if verbose:
            print(f"Starting Lanternfish population simulation with {num_days} day(s)")
            print(f"Initial state: {self.population}, Num fish = {len(self.population)}" )
        for i in range(num_days):
            self.age_fish()
            if verbose:
                print(f"After {i+1} day(s): {len(self.population)}\t{self.population}")
        return len(self.population)            

class LanternfishPopulation():
    NEW_TIMER = 9
    RESET_TIMER = 7

    # fish_pop is a list of ints
    def __init__(self, fish_pop):
        self.initial_population = fish_pop
        self.total_pop = len(fish_pop)
        # key is the day, val is the num of new fish that will be added on that day
        self.days_when_new_fish_get_added = defaultdict(int)

        for fish_timer in self.initial_population:
            self.days_when_new_fish_get_added[fish_timer+1] += 1 
        
        assert sum(self.days_when_new_fish_get_added.values()) == len(fish_pop)

    def update_population_count(self, day):
        num_new_fish = self.days_when_new_fish_get_added.pop(day)
        self.days_when_new_fish_get_added[day+self.RESET_TIMER] += num_new_fish  
        self.days_when_new_fish_get_added[day+self.NEW_TIMER] += num_new_fish 
        self.total_pop = sum(self.days_when_new_fish_get_added.values())


    def simulate(self, num_days, verbose=False):
        if verbose:
            print(f"Starting Lanternfish population simulation with {num_days} day(s)")
            print(f"Initial state: {self.initial_population}, Num fish = {self.total_pop}" )
            print(self.days_when_new_fish_get_added)

        for day in range(1,num_days+1):
            if day in self.days_when_new_fish_get_added:
                self.update_population_count(day)
            if verbose:
                print(f"After {day} day(s), there are\t{self.total_pop}\tfish")

        return self.total_pop

           
def get_input(puzzle=None, mode="test"):
    if mode=="test":
        return "3,4,3,1,2".split(",")

    else:
        return puzzle.input_data.split(",")


def main():
    puzzle = Puzzle(year=2021, day=6)

    data = get_input()
    #data = get_input(puzzle, mode="real") # real input  

    # PART A
    # fish_pop = LanternfishPopulation_PartA([ int(str_num) for str_num in data ])    
    # day = 80
    # num_fish = fish_pop.simulate(day, verbose=False)
    # print(num_fish)
    # print(f"After {day} days there are {num_fish} fish.")
    # print()

    # PART B
    fish_pop = LanternfishPopulation([ int(str_num) for str_num in data ])    
    day = 256
    num_fish = fish_pop.simulate(day, verbose=False)
    print(num_fish)
    


if __name__ == "__main__":
    main()