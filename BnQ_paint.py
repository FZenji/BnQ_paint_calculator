import math

def wallSize():
    length = ""
    while length not in range(0, 501):
        length = input("What is the length of the wall (meters)? ")
    width = ""
    while width not in range(0, 501):
        width = float(input("What is the width of the wall (meters)? "))
    
    wall_size = float(length) * float(width)
    obs = obstructions(wall_size)
    wall_size_obs = (float(length) * float(width)) - obs

    print(f"Your wall is {wall_size_obs}m large.")

    return wall_size_obs

def obstructions(wall_size):
    c = ""
    while c.lower not in ["y", "n"]:
        c = input("Are there any obstructions on the wall? (Y/N)")
    if c.lower() == "y":
        obs_area = 0
        while obs_area >= wall_size:
            nos = ""
            while nos not in range(10):
                try:
                    nos = int(input("How many obstructions are there on the wall? "))
                except ValueError:
                    print("Not an integer. Try again.")
                    nos = ""
            for i in range(nos):
                print(f"Obstruction {i+1}:")
                print("What shape is this obstruction?")
                print(" 1. Rectangle")
                print(" 2. Triangle")
                print(" 3. Circle")
                shape = ""
                while shape not in ['1', '2', '3']:
                    shape = input()
                if shape == '1':
                    width = float(input("What is the width of the obstruction (meters)? "))
                    height = float(input("What is the height of the obstruction (meters)? "))
                    obs_area += width * height
                elif shape == '2':
                    a = float(input("Side 1: "))
                    b = float(input("Side 2: "))
                    c = float(input("Side 3: "))
                    s = (a + b + c) / 2
                    obs_area += math.sqrt(s * (s - a) * (s - b) * (s - c))
                elif shape == '3':
                    diameter = float(input("What is the diameter of the circle (meters)? "))
                    obs_area += math.pi * ((diameter / 2) ** 2)
                else:
                    print("Invalid, defaulting to rectangle")
                    width = float(input("What is the width of the obstruction (meters)? "))
                    height = float(input("What is the height of the obstruction (meters)? "))
                    obs_area += width * height
            
        return obs_area
    elif c.lower() == "n":
        return 0
    else:
        print("Invalid, defaulting to no obstructions")
        return 0

def bucketsCalc(final_area):
    round_area = math.ceil(final_area)
    
    tenL = (round_area) // 10
    fiveL = (round_area - (tenL * 10)) // 5
    twoL = (round_area - (tenL * 10) - (fiveL * 5)) // 2
    oneL = (round_area - (tenL * 10) - (fiveL * 5) - (twoL * 2)) // 1

    bucketDict = {"10L": tenL,
                  "5L": fiveL,
                  "2L": twoL,
                  "1L": oneL}
    
    bucketsNeeded = []

    for key, value in bucketDict.items():
        if value != 0:
            bucketsNeeded.append([key, value])

    return bucketsNeeded

def finish(total_size):
    cost = 0
    brand = 1
    prices = [{"10L": 40,
              "5L": 22,
              "2L": 10,
              "1L": 6},
              {"10L": 60,
              "5L": 34,
              "2L": 15,
              "1L": 9},
              {"10L": 70,
              "5L": 40,
              "2L": 20,
              "1L": 15}]
    coats = int(input("How many coats? "))
    final_area = total_size * coats

    print("What brand of paint would you like for this wall?")
    print(f" 1. GoodHome ", end="")
    print(*[f'| {key}: £{value}' for key, value in prices[0].items()])
    print(f" 2. Dulux ", end="")
    print(*[f'| {key}: £{value}' for key, value in prices[1].items()])
    print(f" 3. Crown ", end="")
    print(*[f'| {key}: £{value}' for key, value in prices[2].items()])
    opt = ""
    while opt not in ['1', '2', '3']:
        opt = input()
    if opt == '1':
        brand = 0
    elif opt == '2':
        brand = 1
    elif opt == '3':
        brand = 2
    else:
        print("Invalid, defualting to medium")

    buckets = bucketsCalc(final_area)

    for bucket in buckets:
        cost += prices[brand][bucket[0]] * bucket[1]

    print(f"Final cost of paint is £{cost}, you will need to buy the following buckets:")
    print("\n".join(f"{bucket[0]}: {bucket[1]}" for bucket in buckets))
    quit()

def menu():
    total_size = 0
    while 1:
        print(f"Size: {total_size}")
        print("**********************")
        print("* 1. Add Wall        *")
        print("* 2. Finish          *")
        print("**********************")
        opt = input()

        if opt == '1':
            total_size += wallSize()
        elif opt == '2':
            finish(total_size)
        else:
            print("Invalid")

if __name__ == '__main__':
    menu()
