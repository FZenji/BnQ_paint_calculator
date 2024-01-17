import math
length = int(input("What is the length of the wall (meters)? "))
width = int(input("What is the width of the wall (meters)? "))
coats = int(input("How many coats? "))


area_per_litre = 13
bucket_size = 5
wall_size = length * width
buckets = ((wall_size * coats) / area_per_litre) / bucket_size

print(f"You need {math.ceil(buckets)} buckets of paint of paint.")
