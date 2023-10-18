import random
import matplotlib.pyplot as plt
import vehicle_class

#constraints
min_v = 60 * (5/18) #m/s
max_v = 120 * (5/18) #m/s
min_a = -6 #m/s^2
max_a = 5 #m/s^2
min_a_ramp = -3 #m/s^2
max_a_ramp = 3 #m/s^2

# intlizing parameters
cars_main_line_no = 10
cars_ramp_no = 5
initial_main_velocity = 60  * 5/18  #m/s
initial_main_accelration = 3 #m/s^2

initial_ramp_velocity = 20 * 5/18 #m/s
initial_ramp_accelration = 0 #m/s^2

#parameters to update kinematics
decision_position = 5#m, position where we apply cruse control
merging_position = 20 #m, position of point of merging
delta_time = 0.01 #seconds, sampling time
desired_distance_bet_cars = 6 #m
alpha = 0.000001
beta = 0.000002
gamma = 0.000001


#cars on main line list
main_cars_platoon = dict() #list of car object
ramp_cars = [] #i want to mak the main line a list as well but to edit that i have no time at the moment

#car labels
car_labels = []  # List to store car labels

#car average velocities
car_avg_velocities = []

def initalize_cars():

    for i in range(cars_main_line_no):
        name = chr(65+i) # starts from A
        if i == 0:
            position = 0 #starts with 0
        else:
            position = main_cars_platoon[chr(65+i-1)].position - round(random.uniform(3, 6))

        velocity = initial_main_velocity
        accelration = initial_main_accelration
        
        car = vehicle_class.Vehicle(name, position, velocity, accelration)
        main_cars_platoon[name]= car

    #print created main cars
    for c in main_cars_platoon.values():
        print(c)

    #initalize cars on ramp
    for i in range(cars_ramp_no):
        name = chr(97+i) # starts from A
        if i == 0:
            position = 0 #starts with 0
        else:
            position = ramp_cars[i-1].position - round(random.uniform(3, 6))

        velocity = initial_ramp_velocity
        accelration = initial_ramp_accelration
        
        car = vehicle_class.Vehicle(name, position, velocity, accelration)
        ramp_cars.append(car)

    #print created ramp cars
    for c in ramp_cars:
        print(c)
    return (main_cars_platoon,ramp_cars)



#animation for the platoon on the main line
def platooning(final_sequence):
    #inialize grid
    # Create a 2D grid-like representation
    fig, ax = plt.subplots(figsize=(15, 2))  # Adjust the figsize to make the plot wider
    ax.set_xlim(-50, 100)
    for car in final_sequence.values():
        car_label = ax.text(car.position, 1, car.name, ha='center', va='center')  # Add a label for the car
        car_labels.append(car_label)

    car_markers = ax.scatter([car.position for car in final_sequence.values()], [1] * len(final_sequence), marker='o', label=[car.name for car in final_sequence.values()], s=100)
    ax.set_yticks([])  # Remove y-axis ticks
    ax.set_xlabel('Position (m)')
    plt.legend(loc='upper left')

    plt.title('Car Positions on the Highway')
    plt.pause(0.5)  # Initial pause for visualization

    # Simulation loop to update car positions
    for _ in range(1000):  # Simulate 1000 time steps

        # Update car positions
        for i,label in zip(range(len(final_sequence)),car_labels):
            car = list(final_sequence.values())[i] #current car

            #first car has no lead and so we treat it differently
            in_cruise_control = False
            if i == 0:
                #check if it is in the zone we do cruse control in
                if decision_position <= car.position <= merging_position:
                    in_cruise_control = True #put flag so following cars start cruise control as well 
                    car.update_cruise_control(None,delta_time,merging_position,desired_distance_bet_cars,alpha,beta,gamma) 
                else:
                    #update kinematics normally with no cruise control each iteration
                    car.update_kinematics(delta_time)

                label.set_x(car.position)
                continue
            
            #check if it is in the zone we do cruse control in
            if in_cruise_control :
                #get its leading car since it has a leader
                lead_car = list(final_sequence.values())[i-1]
                #start platooning   
                car.update_cruise_control(lead_car,delta_time,merging_position,desired_distance_bet_cars,alpha,beta,gamma) 
            else:
                #update kinematics normally with no cruise control each iteration
                car.update_kinematics(delta_time)   
            
            #for debugging 
            #if car.name == 'B':
            #    print(f"B : accelration = {car.acceleration} , position diff = {car.distance_to_lead}")

            label.set_x(car.position)
            
        # Update the scatter plot
        car_markers.set_offsets([(car.position, 1) for car in final_sequence.values()])
        plt.pause(0.1)  # Pause for visualization

    
