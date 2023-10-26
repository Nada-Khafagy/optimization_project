def objective_func(w1, r_total ,merge_r,sequence_full_info_list,distances_to_merge, min_v,max_v):
    f1 = merge_r/r_total
    sum1 = 0
    sum2 = 0
    sum3 = 0
    sum4 = 0
    for car,i in zip(list(sequence_full_info_list.values()),range(len(sequence_full_info_list))):
        if car.name >= chr(97):
            continue
        sum1 = sum1 + car.traveled_time
        sum2 = sum2 + (distances_to_merge[i]/min_v)
        sum3 = sum3 + (distances_to_merge[i]/max_v)
    
    sum4 = sum2

    f2 = (-sum1+sum2) / (-sum3+sum4)

    w2 = 1 - w1
    value = w1 * f1 + w2 * f2
    
    return value 