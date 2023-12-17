#this is a vehicle class that defines a vehicle
class Vehicle:
    def __init__(self, name, initial_position, initial_velocity, initial_acceleration):
        self.name = name
        self.initial_position = initial_position
        self.initial_velocity = initial_velocity
        self.initial_acceleration = initial_acceleration

        self.position = self.initial_position
        self.velocity = self.initial_velocity
        self.acceleration = self.initial_acceleration

        self.distance_to_lead = 0
        self.distance_to_merge = 0  #difference in position between this vehicle and its leading vehicle
        self.traveled_time = 0
        self.lead_vehicle = None #for crusie control
        self.initial_lead_vehicle = None #lead car before switching lanes


    def update_cruise_control(self, lead_vehicle, cc_parameters): 
        self.lead_vehicle = lead_vehicle

        if lead_vehicle is not None:
            self.distance_to_lead = lead_vehicle.position - self.position
            af = cc_parameters.alpha * lead_vehicle.acceleration + cc_parameters.beta * ( lead_vehicle.velocity-self.velocity) + cc_parameters.gamma * (self.distance_to_lead - cc_parameters.desired_distance)
        else:
            af = 0
        self.acceleration = af
        self.position += (self.velocity * cc_parameters.sampling_time) + (0.5 * self.acceleration* (cc_parameters.sampling_time**2))
        self.velocity += self.acceleration*cc_parameters.sampling_time
        
        if (self.position <= cc_parameters.merging_position):
            self.traveled_time += cc_parameters.sampling_time


    def update_kinematics(self, cc_parameters):
        self.position +=  (self.velocity * cc_parameters.sampling_time) + (0.5 * self.acceleration* (cc_parameters.sampling_time**2))
        self.velocity += self.acceleration*cc_parameters.sampling_time
    
    def __str__(self):
        return f"Vehicle: Name = {self.name}, Position = {self.position}, Velocity={self.velocity}, Accelration = {self.acceleration}, Distance to Lead={self.distance_to_lead}, traveled time = {self.traveled_time}"
    
    def follows_road_rules(self, road, cc_parameters):
        #first check constraints
        #if it is a main car, use main constraints
        if self.name < chr(97):
            min_v = road.min_v_main
            max_v = road.max_v_main
            min_a = road.min_a_main
            max_a = road.max_a_main
        else:
            min_v = road.min_v_ramp
            max_v = road.max_v_ramp
            min_a = road.min_a_ramp
            max_a = road.max_a_ramp

        if (min_v >= self.velocity) or (self.velocity >= max_v):
            return False
        if (min_a >= self.acceleration) or (self.acceleration >= max_a) :
            return False
        
        #check collision

        #before merging check with intial leading cars
        if self.position < cc_parameters.merging_position :
            if self.initial_lead_vehicle is not None :
                if ((self.initial_lead_vehicle.position - self.position ) < 5):
                    print(f"collision!!! between {self.name} and {self.initial_lead_vehicle.name}", (self.initial_lead_vehicle.position - self.position ) )
                return ((self.initial_lead_vehicle.position - self.position ) >= 5)
        #after merging check with leading car in the solution
        else:
            if self.lead_vehicle is not None :
                if ((self.lead_vehicle.position - self.position ) < 5):
                    print(f"collision!!! between {self.name} and {self.lead_vehicle.name}", (self.lead_vehicle.position - self.position ) )
                return ((self.lead_vehicle.position - self.position ) >= 5)

               
        return True
    
    def return_to_initial_conditions(self):
        self.position = self.initial_position
        self.velocity = self.initial_velocity
        self.acceleration = self.initial_acceleration
        self.distance_to_lead = 0
        self.distance_to_merge = 0  
        self.traveled_time = 0
