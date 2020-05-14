#! /usr/bin/env python3

import glob
import pandas as pd
from plot_code import rider, YTD
import os, sys
namvi_mi_root = os.getcwd()+'/..'
sys.path.append(namvi_mi_root)
from cost_model.cost_model import * 
import process_sim_results as sim
import numpy as np
import matplotlib.pyplot as plt
from cost_analysis import line_plots

# TODO --------------#
# --> 
# --> for each vehicle, add necessary calculations to all plots
# --> write code for plots in separate code
drive_train = '_EV'
vehicles = pd.read_csv('vehicles'+drive_train+'.csv')
modes = read_json('modes.json')
models_dict = {}
assumptions = read_json('assumptions.json')


import time

c = ['r', 'b', 'g', 'y']

for sim_scenario in glob.glob('sim_runs/scenario_1'):    # loop each simulation scenario
    fig = plt.figure()
    #ax = fig.add_subplot(111)
    axes_set = False

    for mode in modes.keys():
        #label = vehicles.vehicle[index]
        #vehicle = model(vehicles, index, yearly_miles, mode=mode)
        #vehicle.description()

        #if not axes_set:
        #    ax.append(fig.add_subplot(2,2,i+1))
        #ytd, flow = vehicle.total()
        #ax[i].plot(vehicle.time, ytd, color=c[index], label=label)
        #ax[i].set_title(mode)
        #ax[i].legend()
        #time.sleep(0)
        if not axes_set:
            ax = []
        label = mode

        for index in vehicles.index:                        # loop each vehicle in csv file
            i = index
            sim_results_df = pd.read_csv(sim_scenario+'/sim_results/'+vehicles.vehicle[index]+drive_train+'.csv')   # get simulation results for vehicle
            sim_results = sim.Results(sim_results_df)        
            yearly_miles = np.sum(sim_results.daily_dist)       # Probably wrong..
            vehicle = model(vehicles, index, yearly_miles, mode=mode)

            #yearly_riders = np.sum(sim_results.daily_rides)
            #print(yearly_miles)        
            #if not axes_set:
            #    ax = []
            
            #for i, mode in enumerate(modes.keys()):
            #label = vehicles.vehicle[index]
            #    vehicle = model(vehicles, index, yearly_miles, mode=mode)
            #    vehicle.description()

            if not axes_set:
                ax.append(fig.add_subplot(2,2,i+1))
            ytd, flow = vehicle.total()
            ax[i].plot(vehicle.time, ytd, color=c[index], label=label)
            ax[i].set_title(vehicle.name_nomode)
            ax[i].legend()
            print(len(ax))
               # time.sleep(0)
        axes_set = True
    #plt.legend()
    plt.show()

        #TODO: Create new code that processes sim results and creates object for simulation results including:
        # total distance
        # wait_time_bins
        # riders left behind
        # wait time average
        # wait time max        
        #vehicle = model(vehicles, index, )                                                      # Build vehicle model
        #wait_time(sim_results_df, vehicle)              # plot wait time results