#! /usr/bin/env python3

import glob
import pandas as pd
from plot_code.rider import wait_time
import os, sys
namvi_mi_root = os.getcwd()+'/..'
sys.path.append(namvi_mi_root)
from cost_model.cost_model import * 
import process_sim_results as sim
import numpy as np

# TODO --------------#
# --> 
# --> for each vehicle, add necessary calculations to all plots
# --> write code for plots in separate code
vehicles = pd.read_csv('vehicles.csv')
modes = read_json('modes.json')
models_dict = {}
assumptions = read_json('assumptions.json')


import time
for sim_scenario in glob.glob('sim_runs/scenario*'):    # loop each simulation scenario
    for index in vehicles.index:                        # loop each vehicle in csv file
        sim_results_df = pd.read_csv(sim_scenario+'/sim_results/'+vehicles.vehicle[index]+'_normal.csv')   # get simulation results for vehicle
        sim_results = sim.Results(sim_results_df)        
        yearly_miles = np.sum(sim_results.daily_dist)       # Probably wrong..
        yearly_riders = np.sum(sim_results.daily_rides)        
        for mode in modes.keys():
            vehicle = model(vehicles, index, yearly_miles, mode=mode)
            vehicle.description()
            time.sleep(0)

        #TODO: Create new code that processes sim results and creates object for simulation results including:
        # total distance
        # wait_time_bins
        # riders left behind
        # wait time average
        # wait time max        
        #vehicle = model(vehicles, index, )                                                      # Build vehicle model
        #wait_time(sim_results_df, vehicle)              # plot wait time results