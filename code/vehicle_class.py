#this is a vehicle class that defines a car
class Vehicle:
    
    def __init__(self, name, initial_position, initial_velocity, initial_acceleration):
        self.name = name
        self.position = initial_position
        self.velocity = initial_velocity
        self.acceleration = initial_acceleration
        self.distance_to_lead = 0 #difference in position between this vehicle and its leading vehicle


    def update_kinematics(self, lead_vehicle, delta_time, desired_distance, alpha, beta, gamma):
       
        if lead_vehicle is not None:
            self.distance_to_lead = lead_vehicle.position - self.position
            af = alpha * lead_vehicle.acceleration + beta * (self.velocity - lead_vehicle.velocity) + gamma * (self.distance_to_lead - desired_distance)
        else:
            af = 5

        self.acceleration = af
        self.position +=  (self.velocity * delta_time) + (0.5 * self.acceleration* (delta_time*delta_time))
        self.velocity += self.acceleration*delta_time



    def __str__(self):
        return f"Vehicle: Name = {self.name}, Position = {self.position}, Velocity={self.velocity}, Accelration = {self.acceleration}, Distance to Lead={self.distance_to_lead}"