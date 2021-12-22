from aocd.models import Puzzle
from pprint import pprint
import itertools as it
from collections import Counter, defaultdict
import math
from shutil import copyfile




### NAIVE APPROACH ####
"""
Builds the string at each step by making the specified replacements
The string grows exponentially, so this will quickly start to lag
This works until about steps=15 (definitely will not work for steps=40)
"""

def naive_process(polymer, pair_insertion_rule_map):
    replacements = []
    for tuple_pair in pairwise(polymer):
        pair = "".join(tuple_pair)
        ch, str, tuple = pair_insertion_rule_map[pair]
        replacements.append( str )  
    
    #print(replacements)
    result = replacements[0]
    for str in replacements[1:]:
        result += str[1:]
    
    return result

def simulate_naive(num_steps, polymer, pair_insertion_rule_map, verbose=False):
    if verbose:
        print(f"Template:\t{polymer}")

    for i in range(num_steps):
        polymer = naive_process(polymer, pair_insertion_rule_map)
        if verbose:
            print(f"After step {i+1}:\t{polymer}")
    
    if verbose:
        print(len(polymer))  

    counter = Counter(polymer).most_common()
    most_common_letter, most_quantity = counter[0]
    least_common_letter, least_quantity = counter[-1]
    diff = most_quantity - least_quantity
    print(diff)

def partA_naive_approach():
    puzzle = Puzzle(year=2021, day=14)
    #polymer_template = get_input()
    polymer_template = get_input(puzzle, mode="real")     
    simulate_naive(num_steps, polymer_template, pair_insertion_rule_map, verbose=False)

### END NAIVE APPROACH ####


### LESS NAIVE APPROACH THAT STILL FAILS ####
"""
Tried to be a little bit smarter and use generators here so that I would not 
store the entire sequence in memory. BUT, still storing too much of the sequence
in memory. Essentially, this is taking the first pair of the initial seq 
and doing a deep dive into the stack to get the resulting sequence that results
from just that pair after all the steps have been completed. That is still too much
to store in memory.
This works until about steps=20 (definitely will not work for steps=40)
"""
def replacement_func(tuple_pair, insertion_char):
    first, second = tuple_pair
    return [ (first, insertion_char), ( insertion_char, second)  ]

def process_w_gen_and_recursion(iterable, step=0):
    if step == num_steps:
        counts = defaultdict(int)
        for tuple_pair in iterable:   
            first, second = tuple_pair 
            counts[first] += 1 
        return counts, second

    allcounts = Counter(defaultdict(int))
    for tuple_pair in iterable:
        insertion_char, str, tuple = pair_insertion_rule_map["".join(tuple_pair)]
        new_seq = replacement_func(tuple_pair, insertion_char)
        counts, second = process_w_gen_and_recursion(new_seq, step+1)
        allcounts += Counter(counts)

    last_letter = new_seq[1][1]
    return allcounts, last_letter

def simulate_w_generators( polymer):
    allcounts, last_letter = process_w_gen_and_recursion(pairwise(polymer))
    allcounts[last_letter] += 1

    most_common = allcounts.most_common()
    most_common_letter, most_quantity = most_common[0]
    least_common_letter, least_quantity = most_common[-1]
    diff = most_quantity - least_quantity
    print(diff)  

def partB_less_naive_but_still_fails():
    puzzle = Puzzle(year=2021, day=14)
    #polymer_template = get_input()
    polymer_template = get_input(puzzle, mode="real")      
    simulate_w_generators( polymer_template)

### END LESS NAIVE APPROACH THAT STILL FAILS ####


### YET ANOTHER FAILED ATTEMPT ####
"""
Tried to be really clever and create my own iterator/generator class to process
the pairs and keep track of the counts of each pair seen 
BUT, this is still essentially doing a step-by-step replacement of each tuple
I tried to be smarter about how I was storing the results since memory is an issue.
Essentially, this has the same problem as the previous solution. I can't save the 
next set of tuples. I even attempted to write the data to a file (didn't work)
"""
class MyIterables():

    def __init__(self, iterable, steps, tmpfile="tmp.txt"):
        self.myiter = it.chain(iterable)
        self.waiting = []
        self.step = 1
        self.steps = steps
        self.tmpfile = tmpfile

    def __iter__(self):
        return self

    def __next__(self):
        try:
            nextitem = next(self.myiter)
            return nextitem
        except StopIteration:
            #print(f"beginning new chain, ")
            self.step += 1
            if self.step > self.steps:
                raise StopIteration
            self.myiter = it.chain( x for x in self.waiting   )
            self.waiting = []
            nextitem = next(self.myiter)
            return nextitem
        
    def extend(self, seq):
        # with open(self.tmpfile, "a") as f:
        #     for tuple_pair in seq:
        #         f.write("".join(tuple_pair)+"\n")
        self.waiting.extend(seq)

def simulate(polymer):
    myiters = MyIterables(pairwise(polymer), num_steps)

    counts = defaultdict(int)
    for tuple_pair in myiters:
        insertion_char, _, _ = pair_insertion_rule_map["".join(tuple_pair)]
        new_seq = replacement_func(tuple_pair, insertion_char)
        for tp in new_seq:
            counts["".join(tp)] += 1
        myiters.extend( new_seq )
    print(counts)

def partB_yet_another_failed_attempt():
    puzzle = Puzzle(year=2021, day=14)
    #polymer_template = get_input()
    polymer_template = get_input(puzzle, mode="real")      
    simulate(polymer_template)
### END YET ANOTHER FAILED ATTEMPT ####














### WORKING SOLUTION STARTS HERE ###

pair_insertion_rule_map = {}

def get_input(puzzle=None, mode="test"):
    global pair_insertion_rule_map

    if mode=="test":
        raw_data = """
NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C
""".strip()

    else:
        raw_data = puzzle.input_data
        
    data_as_list = raw_data.splitlines()

    polymer_template, pair_insertion_rules = data_as_list[0], data_as_list[2:]
    
    # pair_insertion_rule_map = { line.split(' -> ')[0]:line.split(' -> ')[1] for line in pair_insertion_rules  }

    pair_insertion_rule_map = {}
    for line in pair_insertion_rules:
        pair, insertion_char = line.split(' -> ')
        """
        Given: CH -> B
        Store: CH: ( B, CBH, (CB, BH) )
        """
        pair_insertion_rule_map[pair] = ( insertion_char, pair[0] + insertion_char + pair[1], (pair[0] + insertion_char, insertion_char + pair[1]) )
        
    return polymer_template



"""defining here since I'm not on python 3.10 yet"""
def pairwise(iterable):
    # pairwise('ABCDEFG') --> AB BC CD DE EF FG
    a, b = it.tee(iterable)
    next(b, None)
    return zip(a, b)


num_steps = 10
def main():
    puzzle = Puzzle(year=2021, day=14)

    #polymer_template = get_input()
    polymer_template = get_input(puzzle, mode="real") 

    # determine the # pairs that will be in the final polymer string
    counts = Counter([ "".join(tuple_pair) for tuple_pair in pairwise(polymer_template)   ])
    save_counts = counts.copy()
    pairs_to_process = list(counts.keys())

    for i in range(num_steps):
        counts = defaultdict(int)
        for pair in pairs_to_process:
            # pair -> pair1, pair2
            _, _, (pair1, pair2) = pair_insertion_rule_map[pair]            
            initial_pair_count = save_counts[pair]
            counts[pair1] += initial_pair_count
            counts[pair2] += initial_pair_count
        pairs_to_process = list(counts.keys())
        save_counts = counts.copy()

    # count the individual letters in the polymer
    letter_counts = defaultdict(int)
    for (ch1, ch2), value in save_counts.items():
        letter_counts[ch1] += value
    
    # adjust for last letter
    letter_counts[polymer_template[-1]] += 1

    # get the diff between the most frequent and last frequent letters
    most_common = Counter(letter_counts).most_common()
    most_common_letter, most_quantity = most_common[0]
    least_common_letter, least_quantity = most_common[-1]
    diff = most_quantity - least_quantity
    print(diff)      


if __name__ == "__main__":
    main()   
    #partA_naive_approach()
    #partB_less_naive_but_still_fails()
    #partB_yet_another_failed_attempt()