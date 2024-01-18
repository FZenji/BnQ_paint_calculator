import math

def setup():
    area_per_litre = 10
    coats = int(input("How many coats? "))
    print("What brand of paint would you like for this wall?")
    print(" 1. Cheap | £5 / sqm")
    print(" 2. Medium | £10 / sqm")
    print(" 3. Expensive | £15 / sqm")
    opt = input()
    if opt.lower() == 'cheap' or opt == '1':
        area_per_litre = 5
    elif opt.lower() == 'medium' or opt == '2':
        area_per_litre = 10
    elif opt.lower() == 'expensive' or opt == '3':
        area_per_litre = 15
    else:
        print("Invalid, defualting to medium")

    return coats, area_per_litre

def wallSize():
    # paint_type = {5: "Cheap",
    #               10: "Medium",
    #               15: "Expensive"}

    length = float(input("What is the length of the wall (meters)? "))
    width = float(input("What is the width of the wall (meters)? "))
    # coats = int(input("How many coats? "))
    # print("What brand of paint would you like for this wall?")
    # print(" 1. Cheap | £5 / sqm")
    # print(" 2. Medium | £10 / sqm")
    # print(" 3. Expensive | £15 / sqm")
    # opt = input()
    # if opt.lower() == 'cheap' or opt == '1':
    #     area_per_litre = 5
    # elif opt.lower() == 'medium' or opt == '2':
    #     area_per_litre = 10
    # elif opt.lower() == 'expensive' or opt == '3':
    #     area_per_litre = 15
    # else:
    #     print("Invalid, defualting to medium")
    
    obs = obstructions()

    wall_size = (length * width) - obs
    # litres = (wall_size * coats) / area_per_litre

    # print(f"You need {litres} litres of {paint_type[area_per_litre]} paint for this wall.")
    print(f"Your wall is {wall_size}m large.")

    return wall_size

def obstructions():
    c = input("Are there any obstructions on the wall? (Y/N)")
    if c.lower() == "y":
        obs_area = 0
        nos = int(input("How many obstructions are there on the wall? "))
        for i in range(nos):
            print(f"Obstruction {i+1}:")
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
    area_per_litre = 10
    coats = int(input("How many coats? "))
    final_area = total_size * coats

    print("What brand of paint would you like for this wall?")
    print(f" 1. Cheap | £5 / sqm | £{final_area * 5}")
    print(f" 2. Medium | £10 / sqm | £{final_area * 10}")
    print(f" 3. Expensive | £15 / sqm | £{final_area * 15}")
    opt = input()
    if opt.lower() == 'cheap' or opt == '1':
        area_per_litre = 5
        cost = final_area * 5
    elif opt.lower() == 'medium' or opt == '2':
        area_per_litre = 10
        cost = final_area * 10
    elif opt.lower() == 'expensive' or opt == '3':
        area_per_litre = 15
        cost = final_area * 15
    else:
        print("Invalid, defualting to medium")
        cost = final_area * 10

    buckets = bucketsCalc(final_area)

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

        # if total_litres == 0:
        #     coats, area_per_litre = setup()
        if opt == '1':
            total_size += wallSize()
        elif opt == '2':
            finish(total_size)
        else:
            print("Invalid")

if __name__ == '__main__':
    menu()
