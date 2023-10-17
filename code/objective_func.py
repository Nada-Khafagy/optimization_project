def objective_func(w1, r, rl, list_main_cars, merging_point_pos, min_v,max_v):
    f1 = (r-rl)/r

    for car in list_main_cars:
        sum1 = sum1 + abs(car.position - merging_point_pos) / car.velocity
        sum2 = sum2 + (car.position/min_v)
        sum3 = sum3 + (car.position/max_v)
    
    sum4 = sum2

    f2 = (-sum1+sum2) / (-sum3+sum4)

    w2 = 1 - w1
    value = w1 * f1 + w2 * f2
    return value 