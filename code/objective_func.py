<<<<<<< HEAD
def objective_func(w1, r, rl, car_sequence_info, min_v ,max_v):
    f1 = (r-rl)/r
=======
def objective_func(w1, r_total,merge_r, sequence_car_info,distances_to_merge, min_v,max_v):
    f1 = merge_r/r_total
>>>>>>> 09b59ae10f44911fdb9f1cd5189a69571bd6f117
    sum1 = 0
    sum2 = 0
    sum3 = 0
    sum4 = 0
<<<<<<< HEAD
    for car in car_sequence_info.values():
=======
    for car,i in zip(sequence_car_info.values(),range(len(sequence_car_info.values()))):
        if car.distance_to_merge<0:
            car.distance_to_merge=0
>>>>>>> 09b59ae10f44911fdb9f1cd5189a69571bd6f117
        sum1 = sum1 + car.traveled_time
        sum2 = sum2 + (distances_to_merge[i]/min_v)
        sum3 = sum3 + (distances_to_merge[i]/max_v)
    
    sum4 = sum2

    f2 = (-sum1+sum2) / (-sum3+sum4)

    w2 = 1 - w1
    value = w1 * f1 + w2 * f2
    return value 