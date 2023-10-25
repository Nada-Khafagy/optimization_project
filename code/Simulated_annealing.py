import numpy as np
import objective_func
import randomize_sequence
import math
import Simulation
import initialization
import merged_platoon
import matplotlib.pyplot as plt

SA_temprature_List = []
SA_obj_func_List = []

def simulated_annealing(delta_time,merging_position,
                        initial_temperature, final_temperature, cooling_rate,linear,
                        min_v,max_v,min_a,max_a,min_v_ramp,max_v_ramp,min_a_ramp,max_a_ramp,
                        w1, cars_ramp_no,cars_ramp_merged_no,merged_sequence_size,distances_to_merge):
    #the second to last argument is wrong 
    
    