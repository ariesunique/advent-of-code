"""
Example answers:
Part A: 7
part B: 5

From Input answers are 
Part A: 1292
Part B: 1262

PART A BRUTE FORCE SOLUTION

nums = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]

num_increases = 0
prev = None
for num in nums:
    if prev != None and num > prev:
        num_increases += 1
    prev = num
print(num_increases)

PART A NICER SOLUTION

nums = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]
newlist = [(x,y) for x, y in zip(nums, nums[1:]) ]
num_increases = sum([1 for (x,y) in newlist if y > x])
print(num_increases)

PART B BRUTE FORCE SOLUTION

nums = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]

num_increases = 0

num_items = 3
itr = 0
prev = None

for itr in range( len(nums)-num_items+1 ):
    total = sum(nums[itr:itr+num_items])
    #print(itr, nums[itr:itr+num_items], total)
    if prev != None and total > prev:
        num_increases += 1
    prev = total
print(num_increases)

====
Nice general solution
TIL (or remembered):
- zip can be a nice way to combine a list with itself offset by a few elements
- True is truthy and evals to 1 when used in a sum or other numirical calculation
- don't need the brackets for a list comprehension when used in sum (forgot why)
- nice trick that you don't need to do an actual summation of the window since it's a sliding window and two
elements in the window stay constant, therefore we are really comparing the first and fourth elements in 
Part B - that simplifies the code
"""

#nums = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]

with open("input.txt") as f:
    nums = [ int(x) for x in f.readlines() ]

PARTA_OFFSET = 1
PARTB_OFFSET = 3

offset = PARTB_OFFSET
newlist = [(x,y) for x, y in zip(nums, nums[offset:]) ]
num_increases = sum(y > x for x,y in newlist)
print(num_increases)