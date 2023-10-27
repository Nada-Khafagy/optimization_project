import random

#returns list of sequence ['A','B']
def randomize_sequence(merged_sequence_size, cars_ramp_num):
    sequence_car_info = [1] * merged_sequence_size
    ramp_Cars_no = random.randint(1, cars_ramp_num)
    for _ in range(ramp_Cars_no):
        while True:
            j = random.randint(0, merged_sequence_size-1)
            if sequence_car_info[j] == 1:
                sequence_car_info[j] = 0
                break  # Exit the inner loop
    current_sequence = []
    r = 0
    m = 0
    for i in range(merged_sequence_size):
        if sequence_car_info[i] == 1:
            current_sequence.append(chr(65+m))
            m+=1
        else:
            current_sequence.append(chr(97+r))
            r+=1
    
    print("Randomized Sequence is: ", [0 if letter>=chr(97) else 1 for letter in current_sequence])
    return current_sequence,r



