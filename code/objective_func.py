def objective_func(w1, r_total ,merge_r,sequence_full_info_list,distances_to_merge, min_v_main,max_v_main):
    f1 = merge_r/r_total
    sum1 = 0
    sum2 = 0
    sum3 = 0
    sum4 = 0

    for car,i in zip(list(sequence_full_info_list.values()),range(len(sequence_full_info_list))):
        if car.name >= chr(97):
            continue
        sum1 = sum1 + car.traveled_time
        #if distances_to_merge[i] < 0:
            #print('Sum2 is negative !!!!!!!')

        sum2 = sum2 + (distances_to_merge[i]/min_v_main)
        sum3 = sum3 + (distances_to_merge[i]/max_v_main)

    print("value of sum1 :",sum1)
    print("distance to merge :",distances_to_merge[i])
    print("value of sum2 :",sum2)
    print("value of sum3 :",sum3)

    if sum1 == 0: #no main line cars on solution, maybe we change this later
        f2 = 0
    else:
        f2 = (sum2-sum1) / (sum2-sum3)

    w2 = 1 - w1
    value = (w1 * f1) + (w2 * f2)
    
        


    print("value of F1 :",f1)
    print("value of F2 :",f2)
    print("cost ", value)

    return value