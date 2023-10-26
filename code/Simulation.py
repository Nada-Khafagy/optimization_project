import matplotlib.pyplot as plt
import scatter_custom

#car labels
car_labels = []  # List to store car labels
car_labels_updates = [] 
#car average velocities
car_avg_velocities = []
car_labels_ramps=[]

#animation for the platoon on the main line
def visualization(main_road,on_ramp,car_sequence,delta_time,decision_position,merging_position,desired_distance_bet_cars,alpha,beta,gamma ):
    #inialize grid
    # Create a 2D grid-like representation
    fig, ax = plt.subplots(figsize=(15, 2))  # Adjust the figsize to make the plot wider
    ax.set_xlim(-50, 100)
    ax.set_ylim(-50,60)

    for car in main_road.values():
        car_label = ax.text(car.position, 30, car.name, ha='center', va='center')  # Add a label for the car
        car_labels.append(car_label)
    for car in on_ramp.values():
        car_label_ramp = ax.text(car.position, 5, car.name, ha='center', va='center')  # Add a label for the car
        car_labels_ramps.append(car_label_ramp)

    for car in car_sequence.values():
        if car in main_road.values():
            car_index = list(main_road.values()).index(car)
            car_labels_updates.append(car_labels[car_index])
        else:
            car_index =list(on_ramp.values()).index(car)
            car_labels_updates.append(car_labels_ramps[car_index])
    car_markers = ax.scatter([car.position for car in main_road.values()], [30] * len(main_road), marker=scatter_custom.custom_marker(4,2,-0), 
                             label=[car.name for car in main_road.values()], s=400)
    car_markers_ramp = ax.scatter([car.position for car in on_ramp.values()], [5] * len(on_ramp),marker=scatter_custom.custom_marker(4,2,0),
                                   label=[car.name for car in on_ramp.values()], s=400)
   
    #ax.set_yticks([])  # Remove y-axis ticks
    ax.set_xlabel('Position (m)')
    plt.legend(loc='upper left')

    plt.title('Car Positions on the Highway')
    plt.pause(0.5)  # Initial pause for visualizaton

    # Simulation loop to update car positions
    for j in range(10000):  # Simulate 1000 time steps
        if list(car_sequence.values())[0].position<decision_position:
            # Update car positions
            for i,label in zip(range(len(main_road)),car_labels):
                car = list(main_road.values())[i] #current car
                
                #first car has no lead and so we treat it differently
                if i == 0:
                    car.update_cruise_control(None,delta_time,merging_position,desired_distance_bet_cars,alpha,beta,gamma,True) 
                    label.set_x(car.position)
                    continue
                
                #check if it is in the zone we do cruse control in
             
                #get its leading car since it has a leader
                lead_car = list(main_road.values())[i-1]
                #start platooning   
                car.update_cruise_control(lead_car,delta_time,merging_position,desired_distance_bet_cars,alpha,beta,gamma,True) 
                label.set_x(car.position)
               
                '''  print(  "{:.2f}".format(main_road['B'].distance_to_lead),"{:.2f}".format(main_road['C'].distance_to_lead),
                    "{:.2f}".format(main_road['D'].distance_to_lead),"{:.2f}".format(main_road['E'].distance_to_lead),
                    "{:.2f}".format(main_road['F'].distance_to_lead),"{:.2f}".format(main_road['G'].distance_to_lead),
                    "{:.2f}".format(main_road['H'].distance_to_lead),"{:.2f}".format(main_road['I'].distance_to_lead,))'''
                
            for r,label_ramp in zip(range(len(on_ramp)),car_labels_ramps):
                car_ramp = list(on_ramp.values())[r]
                car_ramp.update_kinematics(delta_time)
                label_ramp.set_x(car_ramp.position)

            car_markers.set_offsets([(car.position, 30) for car in main_road.values()])
            car_markers_ramp.set_offsets([(car.position, 5) for car in on_ramp.values()])
            
            
        else:
            for i in range(len(car_sequence)):
                car = list(car_sequence.values())[i] #current car
                if i == 0:
                    car.update_cruise_control(None,delta_time,merging_position,desired_distance_bet_cars,alpha,beta,gamma,True) 
                    car_labels_updates[i].set_x(car.position)
                    continue
                
               
                #get its leading car since it has a leader
                lead_car = list(car_sequence.values())[i-1]
                #start platooning   
                car.update_cruise_control(lead_car,delta_time,merging_position,desired_distance_bet_cars,alpha,beta,gamma,True) 
                car_labels_updates[i].set_x(car.position)

            '''for r,label_ramp in zip(range(len(on_ramp)),car_labels_ramps):
                car_ramp = list(on_ramp.values())[r]
                if (car_ramp not in updated_sequence.values()):
                    car_ramp.update_kinematics(delta_time)
                    label_ramp.set_x(car_ramp.position)'''
        
        # Update the scatter plot
            car_markers.set_offsets([(car.position,30) for car in main_road.values()]) 
            car_markers_ramp.set_offsets([(car.position, 5) for car in on_ramp.values()])
        plt.pause(0.001)  # Pause for visualization

    
