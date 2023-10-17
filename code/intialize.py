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
initial_main_velocity = 25 #m/s
initial_main_desired_dist = 3 #m
initial_main_accelration = 3 #m/s^2
delta_time = 0.5 #seconds
desired_distance_bet_cars = 3 #m
alpha = 0.00001
beta = 0.00002
gamma = 0.0001


#cars on main line list
main_cars_platoon = dict() #list of car object
#car labels
car_labels = []  # List to store car labels

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

for c in main_cars_platoon.values():
    print(c)








#animation
car_markers = ax.scatter([car.position for car in main_cars_platoon.values()], [1] * len(main_cars_platoon), marker='o', label=[car.name for car in main_cars_platoon.values()], s=100)
ax.set_yticks([])  # Remove y-axis ticks
ax.set_xlabel('Position (m)')
plt.legend(loc='upper left')

plt.title('Car Positions on the Highway')
plt.pause(0.5)  # Initial pause for visualization


# Simulation loop to update car positions
for _ in range(100):  # Simulate 100 time steps
    # Update car positions (e.g., simple simulation with constant velocity)
    for i,label in zip(range(len(main_cars_platoon)),car_labels):
        car = list(main_cars_platoon.values())[i]    
        if i == 0:
            car.update_kinematics(None,delta_time,desired_distance_bet_cars,alpha,beta,gamma)
            label.set_x(car.position)
            continue
        lead_car = list(main_cars_platoon.values())[i-1]   
        car.update_kinematics(lead_car,delta_time,desired_distance_bet_cars,alpha,beta,gamma)
        if car.name == 'B':
            print(f"B : accelration = {car.acceleration} , position diff = {car.distance_to_lead}")
        label.set_x(car.position)
        
    # Update the scatter plot
    car_markers.set_offsets([(car.position, 1) for car in main_cars_platoon.values()])
    plt.pause(0.5)  # Pause for visualization
