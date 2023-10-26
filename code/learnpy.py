import vehicle_class
#this file is to test some cocepts in python 
dict_of_cars = dict()

car_one = vehicle_class.Vehicle("A",0,4,0.3)
car_two = vehicle_class.Vehicle("B",5,3,0.2)
car_three = vehicle_class.Vehicle("C",10,2,0.5)

dict_of_cars['A'] = car_one
dict_of_cars['B'] = car_two
dict_of_cars['C'] = car_three

list_of_cars = dict_of_cars.values()

for car in dict_of_cars.values():
    car.position = 30

print(car_one)
