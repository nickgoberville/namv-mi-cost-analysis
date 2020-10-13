#! /usr/bin/env python3
import os, sys
namvi_mi_root = os.getcwd()+'/../..'
sys.path.append(namvi_mi_root)
from namv_mi.cost_model.cost_model import *
from namv_mi.utils import process_sim_results as sim
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def YTD_plot(vehicle, fig_YTD, ax_YTD, index, fig_YTD_axes_set, c, label, i):
    if not fig_YTD_axes_set and i==0:    # append new axes if not already set
        ax_YTD.append(fig_YTD.add_subplot(2,2,index+1))
        ax_YTD[index].set_title(vehicle.name_nomode, fontsize=20)
        if index == 0 or index == 2:
            ax_YTD[index].set_ylabel('YTD Cost (USD)', fontsize=20)
        if index == 2 or index == 3:
            ax_YTD[index].set_xlabel('Time (years)', fontsize=20)
   # get vehicle cost model
            # plot YTD cost vs time
    #print("Plotting ytd of {}_{} in axes {}".format(vehicle.name, vehicle.drive_train, index))
    ytd, cash_flow = vehicle.total()
    ax_YTD[index].plot(vehicle.time, ytd, c[i], label=label)#label=label)
    ax_YTD[index].legend(fontsize=10)
    ax_YTD[index].grid(b=True)
    return ytd[-1]

def main():
    # Get modes (normal, AV_SD, AV_FM, AV_full)
    modes = read_json('params/modes.json')     # defined in cost_model.cost_model

    # Define different drivetrains
    drive_trains = ['_EV', '_ICE']

    # Setup figures
    # Year to date plot
    fig_YTD = plt.figure()
    fig_YTD.suptitle('Year-to-Date Cost')
    ax_YTD = []
    fig_YTD_axes_set = False

    # plot line params
    plot_params = {'_EV': ['g', 'g:', 'g--', 'g*-'],
                    '_ICE': ['r', 'r:', 'r--', 'r*-']}

    # loop each drive train
    for drive_train in drive_trains:
        vehicles = pd.read_csv('vehicles/vehicles'+drive_train+'.csv')   # extract vehicle models from csv file
        c = plot_params[drive_train]
        labels_set = False

        # loop each vehicle size (S, M, L, XL)
        for index in vehicles.index:
            sim_results_path = 'sim_runs/scenario_'+str(index+1)+'/sim_results/'+vehicles.vehicle[index]+drive_train+'.csv'
            sim_results_df = pd.read_csv(sim_results_path)   # get simulation results for vehicle
            sim_results = sim.Results(sim_results_df)           # Process simulation results
            yearly_miles = np.sum(sim_results.daily_dist)       # Get yearly miles
            yearly_riders = np.sum(sim_results.daily_rides)     # Get yearly_riders

            # loop each mode
            for i, mode in enumerate(modes):
                label = drive_train+'_'+mode
                label = label[1:]
                # Get vehicle cost model
                vehicle = model(vehicles, index, yearly_miles, yearly_riders, mode=mode, inflation=True)

                final_yr_cost = YTD_plot(vehicle, fig_YTD, ax_YTD, index, fig_YTD_axes_set, c, label, i)       

        fig_YTD_axes_set = True # set axes set to true
    plt.show() # YTD_plot

