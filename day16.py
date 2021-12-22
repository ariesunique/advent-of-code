from aocd.models import Puzzle
import math


def get_input(puzzle=None, mode="test"):
    if mode=="test":
        return raw_data = "9C0141080250320F1802104A08"
    else:
        return raw_data = puzzle.input_data
        


hex_to_bin_map = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111"    
}


def hex_to_binary(hexstr):
    res = []
    for ch in hexstr:
        res.append(hex_to_bin_map[ch])
    return "".join(res)


def process_subpackets(typeid, subpacket_values):
    if typeid == 0:
        return sum(subpacket_values)
    elif typeid == 1:
        return math.prod(subpacket_values)
    elif typeid == 2:
        return min(subpacket_values)
    elif typeid == 3:
        return max(subpacket_values)
    elif typeid == 5:
        return int(subpacket_values[0] > subpacket_values[1])
    elif typeid == 6:
        return int(subpacket_values[0] < subpacket_values[1])    
    elif typeid == 7:
        return int(subpacket_values[0] == subpacket_values[1])          



def decode_bits(binstr, packet_versions):
    
    remaining_str = binstr
    num_bits_processed = 0

    # print(f"\ndecoding {remaining_str}")
    version = remaining_str[:3]
    typeid = int(remaining_str[3:6], 2)
    packet_versions.append(version)

    num_bits_processed+= 6

    if typeid == 4:
        remaining_str = remaining_str[6:]
        bits = []
        while True:
            first_bit = remaining_str[0]
            bits.append(remaining_str[1:5])
            remaining_str = remaining_str[5:]
            num_bits_processed += 5

            if first_bit == "0":
                break

        value = int("".join(bits), 2)
        return num_bits_processed, remaining_str, value

    else:
        length_type_id = remaining_str[6]
        num_bits_processed += 1
        subpacket_values = []
        if length_type_id == "0":
            target_num_bits = int(remaining_str[7:22], 2)
            num_bits_processed += 15

            mybits = 0
            leftover_str = remaining_str[22:22+target_num_bits]
            while mybits < target_num_bits:  
                bits1, leftover_str, literal_value = decode_bits(leftover_str, packet_versions)
                subpacket_values.append(literal_value)
                mybits += bits1
                        
            return num_bits_processed+target_num_bits, remaining_str[22+target_num_bits:], process_subpackets(typeid, subpacket_values)

        elif length_type_id == "1":
            number_subpackets = int(remaining_str[7:18], 2)
            num_bits_processed += 11
            leftover_str = remaining_str[18:]
            for _ in range(number_subpackets):
                bits2, _, literal_value = decode_bits(leftover_str, packet_versions)
                subpacket_values.append(literal_value)
                num_bits_processed += bits2
                leftover_str = remaining_str[num_bits_processed:]

            return num_bits_processed, leftover_str, process_subpackets(typeid, subpacket_values)
                

        
    


def main():
    puzzle = Puzzle(year=2021, day=16)

    # hexstr = get_input()
    hexstr = get_input(puzzle, mode="real") 

    binstr = hex_to_binary(hexstr)
    # print(binstr)

    packet_versions = []
    bits, remainder, partB = decode_bits(binstr, packet_versions)
    # print("booyah", bits, remainder)

    # print(packet_versions)
    # print([ int(v, 2) for v in packet_versions])
    partA = sum([ int(v, 2) for v in packet_versions])
    # print(partA)
    print(partB)



if __name__ == "__main__":
    main()  