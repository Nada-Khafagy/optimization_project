import random

#returns list of sequence ['A','B']
def randomize(merged_sequence_size):
    sequence_car_info = [1] * merged_sequence_size
    ramp_Cars_no = random.randint(1, 5)
    for _ in range(ramp_Cars_no): # Use an underscore for an unused loop variable
        while True:
            j = random.randint(0, merged_sequence_size-1)
            if sequence_car_info[j] == 1:
                sequence_car_info[j] = 0
                
                break  # Exit the inner loop
    current_sequence = []
    r = 0
    m = 0
    for i in range(len(sequence_car_info)):
        if sequence_car_info[i] == 1:
            current_sequence.append(chr(65+m))
            m+=1
        else:
            current_sequence.append(chr(97+r))
            r+=1

    #print(sequence_car_info)
    print("Randomized Sequence is: ", current_sequence)
    return current_sequence,r



