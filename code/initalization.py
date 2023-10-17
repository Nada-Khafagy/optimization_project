import random

#constraints
min_v = 60 * (5/18) #m/s
max_v = 120 * (5/18) #m/s
min_a = -6 #m/s^2
max_a = 5 #m/s^2
min_a_ramp = -3 #m/s^2
max_a_ramp = 3 #m/s^2
cars_main_line_no = 10
cars_ramp_no = 5

#cars on main line 
list_main_cars = dict() #list of dictionaries

#generate an inital value for all cars on the main line for accerlation and velocity
initial_main_velocity = round(random.uniform(min_v, max_v),2)
initial_main_accelration = round(random.uniform(min_a, max_a),2)

for i in range(cars_main_line_no):
    car = dict()
    car['name'] = chr(65+i) # A
    car['position'] =  -5 * (i) #starts with 0
    car['velocity'] = initial_main_velocity
    car['accelration'] = initial_main_accelration
    list_main_cars[str(chr(65+i))]= car

print("Initially:")
print("Main line cars")
for c in list_main_cars.items():
    print(c)

#cars on ramp
list_ramp_cars = dict()

#generate an inital value for all cars on the main line for accerlation and velocity
initial_ramp_velocity = round(random.uniform(min_v, max_v),2)
initial_ramp_accelration = round(random.uniform(min_a, max_a),2)



for i in range(cars_ramp_no):
    car = dict()
    car['name'] = chr(97+i)
    car['position'] =  -5 * (i)
    car['velocity'] = initial_ramp_velocity
    car['accelration'] = initial_ramp_accelration
    list_ramp_cars[str(chr(97+i))] = car

print("Ramp cars")
for c in list_ramp_cars.items():
    print(c)

iterations_num = 2
#code for doing iterations
#for i in range(iterations_num):

print("After doing iteration")

# this is only a test of one iteration where we feed a certain decsision 
list_initial = ['A','a','b','B','C','c','D','E','F','d','G','H','I','J']

#update positions based on last list
for i in range(len(list_initial)):
    name = list_initial[i] 
    if name in list_main_cars:
        list_main_cars[name] = i * 5
    else:
        list_ramp_cars[name] = i * 5



#Move a point on a grid after giving it an intial accelration and velocity
# agrid is a matrix so we can represent it in 
