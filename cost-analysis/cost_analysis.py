#! /usr/bin/env python3
# Add namv_mi package files to path
import os, sys
namvi_mi_root = os.getcwd()+'/..'
sys.path.append(namvi_mi_root)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
from cost_model.cost_model import *     # my module

drive_train = '_EV'
vehicles = pd.read_csv('vehicles'+drive_train+'.csv')
modes = read_json('modes.json')
models_dict = {}

def get_miles(csv_file):
    df = pd.read_csv(csv_file)
    miles_per_year = np.sum(df.daily_dist)
    return miles_per_year

def which_plot(name, vehicle):
    if "maint" in name:
        out = vehicle.maint()
    elif "oper" in name:
        out = vehicle.oper()
    elif "drive" in name:
        out = vehicle.driver()
    elif "rider" in name:
        out = vehicle.per_rider(include_purchase=False)
    elif "tot" in name:
        out = vehicle.total(include_purchase=False)
    else:
        NameError 
        print("COULD NOT FIND PLOT TO MATCH NAME!")
        exit()
    return out

def line_plots(name, miles, cash_flow=True, YTD=True):
    plot_types = []
    sup_title = [name+' '+'YTD', name+' '+'cash_flow']
    if YTD:
        plot_types.append(0)
    if cash_flow:
        plot_types.append(1)

    for plot_type in plot_types:
        fig = plt.figure()
        fig.suptitle(sup_title[plot_type])
        axes_set = False
        for index in vehicles.index:
            label = vehicles.vehicle[index]
            if not axes_set: 
                ax = []
            for i, (key, value) in enumerate(modes.items()):
                vehicle = model(vehicles, index, miles, inflation=True, mode=key)
                y = which_plot(name, vehicle)
                models_dict[vehicle.name] = vehicle
                
                if not axes_set:
                    ax.append(fig.add_subplot(2,2,i+1))
                ax[i].plot(vehicle.time, y[plot_type], label=label)
                ax[i].set_title(key)
                ax[i].legend()
            axes_set=True
        plt.show(block=True)

#to_plot = ['maintenance', 'operation', 'per rider', 'total']
#for item in to_plot:
#    line_plots(item)

#x = get_miles('sim_runs/scenario_1/sim_results/small_normal.csv')
#print(x)

