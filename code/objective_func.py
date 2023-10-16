def objective_func(r,rl,list_main_cars,merging_point_pos):
    f1 = (r-rl)/r

    for car in list_main_cars:
        sum = sum + abs(car['position'] - merging_point_pos) / car['velocity']

    return 