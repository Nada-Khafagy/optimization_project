class cruise_control_parameters:
    def __init__(self, decision_position, merging_position, sampling_time, desired_distance, alpha, beta, gamma):
        self.decision_position = decision_position
        self.sampling_time = sampling_time
        self.merging_position = merging_position
        self.desired_distance = desired_distance
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma

#update all cars positions
def cruise_control(vehicle_objects_sequence,cc_parameters):
    for i, car in zip(range(len(vehicle_objects_sequence)),vehicle_objects_sequence):
        #get the car's leading car  
        if i == 0:
            car.update_cruise_control(None,cc_parameters)            
        else:
            lead_car = vehicle_objects_sequence[i-1]  
            car.update_cruise_control(lead_car,cc_parameters)
    

         
    '''for r,label_ramp in zip(range(len(on_ramp)),car_labels_ramps):
        car_ramp = list(on_ramp.values())[r]
        if (car_ramp not in updated_sequence.values()):
            car_ramp.update_kinematics(delta_time)
            label_ramp.set_x(car_ramp.position)'''

    