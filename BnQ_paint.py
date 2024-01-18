import math

def wallSize():
    '''
    Collects information about the length and width of a wall from the user,
    ensuring valid numerical entries within the range of 0.01 to 500 meters.
    Calculates the total wall size and subtracts the area occupied by obstructions.
    Returns the adjusted wall size.

    Returns:
    float: Adjusted wall size in square meters.
    '''
    while 1:
        try:
            length = float(input("What is the length of the wall (meters)? "))
            assert 0 < length <= 500
        except ValueError:
            print("Not a number.")
        except AssertionError:
            print("Must be between 0m and 500m.")
        else:
            break
    while 1:
        try:
            width = float(input("What is the width of the wall (meters)? "))
            assert 0 < width <= 500
        except ValueError:
            print("Not a number.")
        except AssertionError:
            print("Must be between 0m and 500m.")
        else:
            break
    
    wall_size = float(length) * float(width)
    obs = obstructions(wall_size)
    wall_size_obs = (float(length) * float(width)) - obs

    print(f"Your wall is {wall_size_obs:.2f}m2 large.")

    return wall_size_obs

def obstructions(wall_size):
    '''
    Determines if there are obstructions on a wall, calculates and returns the total area
    occupied by the obstructions. If no obstructions are present, returns 0.

    Parameters:
    wall_size (float): The total size of the wall in square meters.

    Returns:
    float: Total area occupied by obstructions, or 0 if no obstructions are present.
    '''
    c = ""
    while c.lower() not in ["y", "n"]:
        c = input("Are there any obstructions on the wall? (Y/N)")
    if c.lower() == "y":
        obs_area = math.inf
        while obs_area >= wall_size:
            obs_area = 0
            while 1:
                try:
                    nos = int(input("How many obstructions are there on the wall? "))
                    assert 0 < nos <= 10
                except ValueError:
                    print("Not an integer. Try again.")
                except AssertionError:
                    print("Must be between 1 and 10 obstructions.")
                else:
                    break
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
                    while 1:
                        try:
                            width = float(input("What is the width of the obstruction (meters)? "))
                            assert 0 < width <= 500
                        except ValueError:
                            print("Not a number. Try again.")
                        except AssertionError:
                            print("Must be between 0 and 500m.")
                        else:
                            break
                    while 1:
                        try:
                            height = float(input("What is the height of the obstruction (meters)? "))
                            assert 0 < height <= 500
                        except ValueError:
                            print("Not a number. Try again.")
                        except AssertionError:
                            print("Must be between 0 and 500m.")
                        else:
                            break
                    obs_area += width * height
                elif shape == '2':
                    while 1:
                        try:
                            while 1:
                                try:      
                                    a = float(input("Side 1: "))
                                    assert a > 0
                                except ValueError:
                                    print("Not a number. Try again.")
                                except AssertionError:
                                    print("Must be above 0m.")
                                else:
                                    break
                            while 1:
                                try:
                                    b = float(input("Side 2: "))
                                    assert b > 0
                                except ValueError:
                                    print("Not a number. Try again.")
                                except AssertionError:
                                    print("Must be above 0m.")
                                else:
                                    break
                            while 1:
                                try:
                                    c = float(input("Side 3: "))
                                    assert c > 0
                                except ValueError:
                                    print("Not a number. Try again.")
                                except AssertionError:
                                    print("Must be above 0m.")
                                else:
                                    break
                            s = (a + b + c) / 2
                            obs_area += math.sqrt(s * (s - a) * (s - b) * (s - c))
                            assert obs_area > 0
                        except ValueError:
                            print("The sum of two side lengths has to exceed the length of the third side.")
                        except AssertionError:
                            print("The sum of two side lengths has to exceed the length of the third side.")
                        else:
                            break
                elif shape == '3':
                    while 1:
                        try:
                            diameter = float(input("What is the diameter of the circle (meters)? "))
                            assert diameter > 0
                        except ValueError:
                            print("Not a number. Try again.")
                        except AssertionError:
                            print("Must be above 0m.")
                        else:
                            break
                    obs_area += math.pi * ((diameter / 2) ** 2)
                else:
                    print("Invalid, defaulting to rectangle")
                    width = float(input("What is the width of the obstruction (meters)? "))
                    height = float(input("What is the height of the obstruction (meters)? "))
                    obs_area += width * height

            if obs_area >= wall_size:
                print("The obsticles must be smaller than the wall.")
            
        return obs_area
    elif c.lower() == "n":
        return 0
    else:
        print("Invalid, defaulting to no obstructions")
        return 0

def bucketsCalc(final_area):
    '''
    Calculates the number of paint buckets needed to cover a given area,
    considering available bucket sizes (10L, 5L, 2L, and 1L).

    Parameters:
    final_area (float): The total area to be covered in square meters.

    Returns:
    list: A list of lists containing the required paint bucket sizes and their quantities.
          Each inner list has the format [bucket_size, quantity].
    '''
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
    '''
    Calculates the cost and required paint buckets for finishing a wall,
    considering the number of coats, total wall size, and user-selected paint brand.

    Parameters:
    total_size (float): The initial total size of the wall in square meters.

    Returns:
    None
    '''
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
    print(*[f'| {key}: £{value}' for key, value in prices[0].items()], end="")
    print(" || Covers 5 square meters per litre")
    print(f" 2. Dulux ", end="")
    print(*[f'| {key}: £{value}' for key, value in prices[1].items()], end="")
    print(" || Covers 10 square meters per litre")
    print(f" 3. Crown ", end="")
    print(*[f'| {key}: £{value}' for key, value in prices[2].items()], end="")
    print(" || Covers 15 square meters per litre")
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

    buckets = bucketsCalc(final_area / ((brand + 1) * 5))

    for bucket in buckets:
        cost += prices[brand][bucket[0]] * bucket[1]

    print(f"Final cost of paint is £{cost}, you will need to buy the following buckets:")
    print("\n".join(f"{bucket[0]}: {bucket[1]}" for bucket in buckets))
    quit()

def menu():
    total_size = 0
    while 1:
        print(f"Size: {total_size:.2f} m2")
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
