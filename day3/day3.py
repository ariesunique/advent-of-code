from collections import Counter
from aocd.models import Puzzle

def get_rate_decimal(data, rate="gamma"):
    if rate=="gamma":
        n = 0
    elif rate=="epsilon":
        n = -1 
    else:
        print("unknown rate type")
        return 1   

    rate_binary = "".join([ Counter(code).most_common()[n][0] for code in zip(*data) ])
    return int(rate_binary, 2)
    

def get_complex_rate_decimal(data, rating="oxygen"):
    if rating=="oxygen":
        n = 0
        tie_bit = '1'
    elif rating=="co2":
        n = -1
        tie_bit = '0'
    else:
        print("unknown rating type")
        return 1

    for i in range(len(data[0])):
        most_common_bits = Counter( list(zip(*data))[i] ).most_common()
        top_bit_count = most_common_bits[0][1]
        next_top_bit_count = most_common_bits[1][1]
        bit_to_keep = tie_bit if top_bit_count == next_top_bit_count else most_common_bits[n][0]

        data = [ item for item in data if item[i]==bit_to_keep ]

        if len(data) == 1:
            break

    return int(data[0], 2)

    
def main():
    puzzle = Puzzle(year=2021, day=3)

    # Personal input data. Your data will be different.
    data = puzzle.input_data.splitlines()

    # test data
#     data = """
# 00100
# 11110
# 10110
# 10111
# 10101
# 01111
# 00111
# 11100
# 10000
# 11001
# 00010
# 01010
# """.splitlines()[1:]

#     for d in data:
#         print(d)
#     print("")  

    # part 1
    gamma_rate = get_rate_decimal(data)
    epsilon_rate = get_rate_decimal(data, "epsilon")
    power = gamma_rate * epsilon_rate
    print(f"Part 1: power is {power}\n")

    # part 2
    oxygen_generator_rating = get_complex_rate_decimal(data)
    co2_scrubber_rating = get_complex_rate_decimal(data,"co2")
    life_support_rating = oxygen_generator_rating * co2_scrubber_rating
    print(f"Part 2: life support rating is {life_support_rating}")


if __name__ == '__main__':
    main()
