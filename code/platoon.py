import matplotlib.pyplot as plt
import scatter_custom

#animation for the platoon on the main line
def platooning(final_sequence,delta_time,merging_position,desired_distance_bet_cars,alpha,beta,gamma ):
    car_labels = []  # List to store car labels
    #inialize grid
    # Create a 2D grid-like representation
    fig, ax = plt.subplots(figsize=(15, 2))  # Adjust the figsize to make the plot wider
    ax.set_xlim(-50, 100)
    for car in final_sequence.values():
        car_label = ax.text(car.position, 1, car.name, ha='center', va='center')  # Add a label for the car
        car_labels.append(car_label)

    car_markers = ax.scatter([car.position for car in final_sequence.values()], [1] * len(final_sequence), marker=scatter_custom.custom_marker(4,2,0), label=[car.name for car in final_sequence.values()], s=400)
    ax.set_yticks([]) # Remove y-axis ticks
    ax.set_xlabel('Position (m)')
    plt.legend(loc='upper left')

    plt.title('Car Positions on the Highway')
    plt.pause(0.5)  # Initial pause for visualization

    # Simulation loop to update car positions
    for j in range(10000):  # Simulate 1000 time steps

        # Update car positions zip(range(len(final_sequence)),car_labels):
        for i,label in zip(range(len(final_sequence)),car_labels):
            car = list(final_sequence.values())[i] #current car

            #first car has no lead and so we treat it differently
            if i == 0:
                #check if it is in the zone we do cruse control in
                car.update_cruise_control(None,delta_time,merging_position,desired_distance_bet_cars,alpha,beta,gamma) 
                label.set_x(car.position)
                continue
            else: 
                #get its leading car since it has a leader
                lead_car = list(final_sequence.values())[i-1]
                #start platooning   
                car.update_cruise_control(lead_car,delta_time,merging_position,desired_distance_bet_cars,alpha,beta,gamma)   
                label.set_x(car.position)
            print(  "{:.2f}".format(final_sequence['B'].distance_to_lead),"{:.2f}".format(final_sequence['C'].distance_to_lead),
                    "{:.2f}".format(final_sequence['D'].distance_to_lead),"{:.2f}".format(final_sequence['E'].distance_to_lead),
                    "{:.2f}".format(final_sequence['F'].distance_to_lead),"{:.2f}".format(final_sequence['G'].distance_to_lead),
                    "{:.2f}".format(final_sequence['H'].distance_to_lead),"{:.2f}".format(final_sequence['I'].distance_to_lead,))
            
        # Update the scatter plot
        car_markers.set_offsets([(car.position, 1) for car in final_sequence.values()])
        
        plt.pause(0.001)  # Pause for visualization
        j+=1 #why did you add this?

