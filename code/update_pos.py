#assume that dist is the distance from the center of the car to another + 1 meter for spacing
def update_position(main_cars_dict, ramp_cars_dict, new_pos_list, dist):
    for i in new_pos_list:
        name = new_pos_list[i]
        if name in main_cars_dict:
            main_cars_dict[name]['position'] = i * dist
        else :
            ramp_cars_dict[name]['position'] = i * dist