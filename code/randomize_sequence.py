import random

def randomize_sequence():
    sequence_car_info = [1]*10
    ramp_Cars_no = random.randint(1,5)
    for i in range(1,ramp_Cars_no):
        j = random.randint(0,9)
        sequence_car_info[j] = 0