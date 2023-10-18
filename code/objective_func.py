def objective_func(w1, r, rl, sequence_car_info, min_v,max_v):
    f1 = (r-rl)/r
    sum1 = 0
    sum2 = 0
    sum3 = 0
    sum4 = 0
    for car in sequence_car_info.values():
        sum1 = sum1 + car.traveled_time
        sum2 = sum2 + (car.position/min_v)
        sum3 = sum3 + (car.position/max_v)
    
    sum4 = sum2

    f2 = (-sum1+sum2) / (-sum3+sum4)

    w2 = 1 - w1
    value = w1 * f1 + w2 * f2
    return value 