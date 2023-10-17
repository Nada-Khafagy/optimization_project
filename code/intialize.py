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
distance_to_merging = 20
delta_time = 0.01 #seconds
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

# Create a 2D grid-like representation
fig, ax = plt.subplots(figsize=(10, 2))  # Adjust the figsize to make the plot wider
ax.set_xlim(-50, 200)

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
    car_label = ax.text(car.position, 1, car.name, ha='center', va='center')  # Add a label for the car
    car_labels.append(car_label)

#print created main cars
for c in main_cars_platoon.values():
    print(c)
def get_main_cars_list():
    return main_cars_platoon

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

def get_ramp_cars_list():
    return ramp_cars


#animation for the platoon on the main line
def platooning():
    car_markers = ax.scatter([car.position for car in main_cars_platoon.values()], [1] * len(main_cars_platoon), marker='o', label=[car.name for car in main_cars_platoon.values()], s=100)
    ax.set_yticks([])  # Remove y-axis ticks
    ax.set_xlabel('Position (m)')
    plt.legend(loc='upper left')

    plt.title('Car Positions on the Highway')
    plt.pause(0.5)  # Initial pause for visualization

    # Simulation loop to update car positions
    for _ in range(1000):  # Simulate 100 time steps
        sum = 0
        num = 0   

        # Update car positions
        for i,label in zip(range(len(main_cars_platoon)),car_labels):
            car = list(main_cars_platoon.values())[i] 

            if i == 0:
                car.update_kinematics(None,delta_time,desired_distance_bet_cars,alpha,beta,gamma)
                label.set_x(car.position)
                continue
            lead_car = list(main_cars_platoon.values())[i-1]   
            car.update_kinematics(lead_car,delta_time,desired_distance_bet_cars,alpha,beta,gamma) #update kinematics of the car each iteration

            if car.position <= distance_to_merging:
                sum += car.position
                num += 1
            else:
                print()
                car_avg_velocities.append(sum/num)
            
            #for debugging 
            #if car.name == 'B':
            #    print(f"B : accelration = {car.acceleration} , position diff = {car.distance_to_lead}")

            label.set_x(car.position)
            
        # Update the scatter plot
        car_markers.set_offsets([(car.position, 1) for car in main_cars_platoon.values()])
        plt.pause(0.1)  # Pause for visualization

    

platooning()