import sequence
def fitness(w1, ramp_cars_total_num, obj_sequence, cc_paramters, road):
    #just to make sure everything is correct
    for car in obj_sequence:
        car.return_to_initial_conditions()

    distances_to_merge = sequence.get_distance_to_merge_list(obj_sequence, cc_paramters)
    
    if not sequence.check_feasibility( obj_sequence, road, cc_paramters):
        return -1


    ramp_cars_used=0
    for car in obj_sequence:
        if car.name >= chr(97):
            ramp_cars_used+=1

    f1 = ramp_cars_used / ramp_cars_total_num
    sum1 = 0
    sum2 = 0
    sum3 = 0

    for car, distance in zip(obj_sequence,distances_to_merge):
        if car.name >= chr(97):
            continue
        sum1 = sum1 + car.traveled_time
        #if distances_to_merge[i] < 0:
            #print('Sum2 is negative !!!!!!!')

        sum2 = sum2 + (distance/road.min_v_main)
        sum3 = sum3 + (distance/road.max_v_main)

    if sum2 == sum3: #no main line cars on solution, maybe we change this later
        f2 = 0
    else:
        f2 = (sum2-sum1) / (sum2-sum3)

    w2 = 1 - w1
    value = (w1 * f1) + (w2 * f2)

    '''print("value of sum1 :", sum1)
    print("value of sum2 :", sum2)
    print("value of sum3 :", sum3)
    print("value of F1 :", f1)
    print("value of F2 :", f2)
    print("cost ", value)'''

    return value
