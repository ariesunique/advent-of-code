from aocd.models import Puzzle

class Signal():
    def __init__(self, segment_str):
        this.segments = segments



def get_input(puzzle=None, mode="test", debug=False):
    if mode=="test":
        raw_data = """
be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce        
""".splitlines()[1:]

    else:
        raw_data = puzzle.input_data.splitlines()
    

    data = [(input.split(), output.split()) for input, output in [ line.split("|") for line in raw_data ] ]
    
    if debug:
        print(f"Num inputs is {len(data)}\n")
        print("Here's your first three inputs and outputs:\n")
        for i in range(3):
            input, output =  data[i]
            assert len(input) == 10
            assert len(output) == 4
            print(f"Input {input}")
            print(f"Output {output}")
            print()

    return data

def contains_encoded_val(encoded_seg, encoded_val):
    return set(encoded_val).issubset(set(encoded_seg))

def process_of_elimination(known_encodings, possibles ):

    for digit in possibles[:]:
        if known_encodings[digit]:
            possibles.remove(digit)

    if (len(possibles)==1):
        return possibles[0]
    
    return ""

def find_digit_based_on_encoding(known_encodings, possibles, encoded_seg):
    for digit in possibles:
        encoding = known_encodings[digit]
        if encoding == encoded_seg:
            return digit
    return ""

def decode(encoded_seg, known_encodings):
    if len(encoded_seg) == 2:
        return "1"
    elif len(encoded_seg) == 3:
        return "7"
    elif len(encoded_seg) == 4:
        return "4"
    elif len(encoded_seg) == 7:
        return "8"
    elif len(encoded_seg) == 5:
        encoded_one = known_encodings["1"]
        if encoded_one and contains_encoded_val(encoded_seg, encoded_one):
            return "3"
        
        encoded_six = known_encodings["6"]
        if encoded_six and contains_encoded_val(encoded_six, encoded_seg):
            return "5"

        possibles = ["2", "3", "5"]
        digit = find_digit_based_on_encoding(known_encodings, possibles, encoded_seg)
        if digit:
            return digit

        return process_of_elimination(known_encodings, possibles)

    elif len(encoded_seg) == 6:
        encoded_one = known_encodings["1"]
        if encoded_one and not contains_encoded_val(encoded_seg, encoded_one):
            return "6"
        
        encoded_four = known_encodings["4"]
        if encoded_four and contains_encoded_val(encoded_seg, encoded_four):
            return "9"
        
        possibles = ["0", "6", "9"]
        digit = find_digit_based_on_encoding(known_encodings, possibles, encoded_seg)
        if digit:
            return digit

        return process_of_elimination(known_encodings, possibles)
     

def main():
    digits = {
        0: "abcefg",
        1: "cf",
        2: "acdeg",
        3: "acdfg",
        4: "bcdf",
        5: "acdfg",
        6: "abdefg",
        7: "acf",
        8: "abcdefg",
        9: "abcdfg"
    }

    puzzle = Puzzle(year=2021, day=8)

    data = get_input(debug=False)
    #data = get_input(puzzle, mode="real", debug=False) # real input  

    # PART A
    # unique_seg_lenths = [2,3,4,7]
    # outputs_only = [ item for sublist in data for item in sublist[1] ]
    # partA = sum([True for seg in outputs_only if len(seg) in unique_seg_lenths ])
    # print(partA)
    # print()

    # PART B
    MAX_ATTEMPTS = 3
    EXPECTED_NUM_DIGITS = 4
    mycodes = []
    for line, (input, output) in enumerate(data):

        known_encodings = {
            "0":None,
            "1":None,
            "2":None,
            "3":None,
            "4":None,
            "5":None,
            "6":None,
            "7":None,
            "8":None,
            "9":None
        }
        
        mydigits = []
        more_digits_to_find = len(mydigits) < EXPECTED_NUM_DIGITS
        attempts_remaining = MAX_ATTEMPTS

        while ( more_digits_to_find and attempts_remaining):
            mydigits = []
            attempts_remaining -= 1
            for code in input:
                code = sorted(code)
                digit = decode(code, known_encodings)
                if digit:
                    known_encodings[digit] = code
            
            for code in output:
                code = sorted(code)
                digit = decode(code, known_encodings)
                if digit:
                    mydigits.append(digit)
                else:
                    break


        assert len(mydigits) == EXPECTED_NUM_DIGITS, f"Error processing line with index {line}; Didn't find all 4 digits\nInput: {input}\nOutput: {output}\nKnowns: {known_encodings}\nMy digits: {mydigits}"
        output_code = int("".join(mydigits))
        #print(output_code)
        mycodes.append(output_code)
        #print()

    ans = sum(mycodes)
    print(ans)

if __name__ == "__main__":
    main()    