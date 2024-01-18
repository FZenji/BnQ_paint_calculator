import math

def wallArea(coats, area_per_litre):
    length = int(input("What is the length of the wall (meters)? "))
    width = int(input("What is the width of the wall (meters)? "))
    coats = int(input("How many coats? "))
    print("What brand of paint would you like for this wall?")
    print(" 1. Cheap | £5 / sqm")
    print(" 2. Medium | £10 / sqm")
    print(" 3. Expensive | £15 / sqm")
    opt = input()
    if opt.lower == 'cheap':
        wallArea()
    elif opt == '2':
        finish()
    else:
        print("Invalid")
    
    obs = obstructions()


    area_per_litre = 13
    # bucket_size = 5
    wall_size = length * width
    litres = (wall_size * coats) / area_per_litre
    # buckets = litres / bucket_size

    # print(f"You need {math.ceil(buckets)} buckets of paint of paint.")

def obstructions():
    c = input("Are there any obstructions on the wall? (Y/N)")
    if c.lower == "y":
        obs_area = 0
        nos = int(input("How many obstructions are there on the wall? "))
        for i in range(nos):
            print(f"Obstruction {i+1}:")
            width = input("What is the width of the obstruction (meters)? ")
            height = input("What is the height of the obstruction (meters)? ")
            obs_area += width * height
        return obs_area
    if c.lower == "n":
        return 0



def finish():
    pass

def menu():
    while 1:
        print("**********************")
        print("* 1. Add Wall        *")
        print("* 2. Finish          *")
        print("**********************")
        opt = input()

        if opt == '1':
            wallArea()
        elif opt == '2':
            finish()
        else:
            print("Invalid")

if __name__ == '__main__':
    print("Enter x to any input to return to menu")
    menu()
