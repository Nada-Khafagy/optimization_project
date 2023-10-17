#assume that dist is the distance from the center of the car to another + 1 meter for spacing
def update_position(cars_dict, new_pos_list, dist):
    for i in new_pos_list:
        cars_dict[new_pos_list[i]]['position'] = i * dist