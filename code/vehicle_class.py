#this is a vehicle class that defines a car
class Vehicle:
    
    def __init__(self, name, initial_position, initial_velocity, initial_acceleration):
        self.name = name
        self.position = initial_position
        self.velocity = initial_velocity
        self.acceleration = initial_acceleration
        self.distance_to_lead = 0
        self.distance_to_merge = 0  #difference in position between this vehicle and its leading vehicle
        self.traveled_time = 0



    def update_cruise_control(self, lead_vehicle, delta_time, merging_position,desired_distance, alpha, beta, gamma,decision_flag):
       
        if lead_vehicle is not None:
            self.distance_to_lead = lead_vehicle.position - self.position
            af = alpha * lead_vehicle.acceleration + beta * ( lead_vehicle.velocity-self.velocity) + gamma * (self.distance_to_lead - desired_distance)
        else:
            af = 0

        self.acceleration = af
        self.position += (self.velocity * delta_time) + (0.5 * self.acceleration* (delta_time*delta_time))
        self.velocity += self.acceleration*delta_time

        if (self.position <= merging_position)and (decision_flag==True): 
            self.traveled_time += delta_time

    def update_kinematics(self, delta_time):
        self.position +=  (self.velocity * delta_time) + (0.5 * self.acceleration* (delta_time*delta_time))
        self.velocity += self.acceleration*delta_time
    
    def __str__(self):
        return f"Vehicle: Name = {self.name}, Position = {self.position}, Velocity={self.velocity}, Accelration = {self.acceleration}, Distance to Lead={self.distance_to_lead}, traveled time = {self.traveled_time}"
    
    def check_feasibility (self, min_v, max_v, min_a, max_a):
        if (min_v >= self.velocity) or (self.velocity >= max_v) :
            return False
        if (min_a >= self.acceleration) or (self.acceleration>= max_a) :
            return False
        return True
