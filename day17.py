from aocd.models import Puzzle
import itertools
import math

def get_input(puzzle=None, mode="test"):
    if mode=="test":
        raw_data = "target area: x=20..30, y=-10..-5"
    else:
        raw_data = puzzle.input_data
    
    target_area = {}
    for target_area_coords in raw_data.strip("target area: ").split(","):
        axis, vals = target_area_coords.split("=")
        minpos, maxpos = vals.split("..")
        target_area[axis.strip()] = (int(minpos), int(maxpos))

    return target_area


def missed_target(position, target):
    
    missedX = position[0] > target["x"][1]
    missedY =  position[1] < target["y"][0] if target["y"][0] < 0 else position[1] < target["y"][1]

    return missedX or missedY
    #return position[0] > target["x"][1] or position[1] < target["y"][1]

def hit_target(position, target):
    return target["x"][1] >= position[0] >= target["x"][0] and \
           target["y"][1] >= position[1] >= target["y"][0]



def update_position_and_velocity(position, velocity):
    xpos, ypos = position
    xvel, yvel = velocity
    xpos += xvel
    ypos += yvel
    if xvel > 0: xvel -= 1
    elif xvel < 0: xvel += 1
    yvel -= 1
    return (xpos, ypos), (xvel, yvel)


def fire_probe(velocity, start, target):
    position = start
    got_a_hit = False
    num_steps = 0
    highest_ypos = 0
    while not missed_target(position, target):
        num_steps += 1
        position, velocity = update_position_and_velocity(position, velocity)
        xpos, ypos = position
        if ypos > highest_ypos:
            highest_ypos = ypos
        got_a_hit = hit_target(position, target)
        if got_a_hit:
            break
    return got_a_hit, position, num_steps, highest_ypos

def calc_distance(x2,y2,x1,y1):
    return math.sqrt( (x2-x1)**2 + (y2-y1)**2  )

def brute_force(start, target):
    
    prev_distance = None
    num_incs_of_distance = 0
    highest_ypos = 0
    midway_target = (target["x"][0] + (target["x"][1]-target["x"][0])//2, \
                     target["y"][0] + (target["y"][1]-target["y"][0])//2)

    num_hits = 0
    
    for xvel in itertools.count(0):
        for yvel in itertools.count(-100):   
            hit_or_miss, last_position, num_steps, highest_ypos_this_time = fire_probe((xvel,yvel),start, target)
            
            if hit_or_miss:
                #print(f"got a hit at {last_position} with velocity {(xvel,yvel)}; reached height of {highest_ypos_this_time} ")
                num_hits += 1
                if highest_ypos_this_time > highest_ypos:
                    highest_ypos = highest_ypos_this_time
                
            distance = calc_distance(*last_position, *midway_target)

            if prev_distance and distance > prev_distance:
                num_incs_of_distance += 1
            else:
                num_incs_of_distance = 0
                       
            prev_distance = distance
            # arbitrary numbers to break out of the loop. Not great, but best I came up with at the time.
            if num_incs_of_distance > 500: break
        if xvel > 1000: break
    print(f"\n highest height reached was {highest_ypos}")
    print(f"num hits {num_hits}")


def main():
    puzzle = Puzzle(year=2021, day=17)

    target_area = get_input()
    #target_area = get_input(puzzle, mode="real") 

    brute_force((0,0), target_area)




if __name__ == "__main__":
    main()  