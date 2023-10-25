

#parameters to update kinematics
decision_position = 40#m, position where we apply cruse control
merging_position = 140 #m, position of point of merging
delta_time = 0.01 #seconds, sampling time
desired_distance_bet_cars = 6#m
alpha = 1
beta = 1.2
gamma = 0.5


def platooning(updated_sequence, delta_time):
    #flag = True
    #distances_to_merge=[]
    for i in range(len(updated_sequence)):
        car = list(updated_sequence.values())[i] #current car
        #first car has no lead car
        
        if i == 0:
            #print(car.position)
            #if car.position > decision_position:
            #        flag = False
            car.update_cruise_control(None,delta_time,merging_position,desired_distance_bet_cars,alpha,beta,gamma,True) 
            
        #Not first car
        #get its leading car since it has a leader
        else:
            lead_car = list(updated_sequence.values())[i-1]
            #start platooning   
            car.update_cruise_control(lead_car,delta_time,merging_position,desired_distance_bet_cars,alpha,beta,gamma,True) 
        #if flag==True:
         #       distances_to_merge.append(car.distance_to_merge)
                #print("true")
        #print(car)
    '''for r,label_ramp in zip(range(len(on_ramp)),car_labels_ramps):
        car_ramp = list(on_ramp.values())[r]
        if (car_ramp not in updated_sequence.values()):
            car_ramp.update_kinematics(delta_time)
            label_ramp.set_x(car_ramp.position)'''
    #return distances_to_merge
    # Update the scatter plot
    