class Road:
    def __init__(self,min_v_main,max_v_main,min_v_ramp,max_v_ramp,min_a_main,max_a_main,min_a_ramp, max_a_ramp, position_lower_limit, position_upper_limit):
        self.min_v_main = min_v_main
        self.max_v_main = max_v_main
        self.min_v_ramp = min_v_ramp
        self.max_v_ramp = max_v_ramp
        self.min_a_main = min_a_main
        self.max_a_main = max_a_main
        self.min_a_ramp = min_a_ramp
        self.max_a_ramp = max_a_ramp
        self.position_lower_limit = position_lower_limit
        self.position_upper_limit = position_upper_limit

    

