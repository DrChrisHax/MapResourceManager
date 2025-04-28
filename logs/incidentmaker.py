import random

def create(time: int, address, description):
    f = open(f"{time}.txt", "w")
    f.write(f"--- INCIDENT START ---\nAddress: {address}\nTime: {time}\nDescription: {description}\n--- INCIDENT END ---")
    print(f"File created succesfully: {time}")

h = random.randint(1,24)
m = random.randint(10, 59)

time = (h * 100) + m
address = random.randint (1, 9)

description = "An armed assault was reported outside the shopping mall entrance."
create(time, address, description)