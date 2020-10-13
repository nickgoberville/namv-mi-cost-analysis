#! /usr/bin/env python3
import os, sys
namvi_mi_root = os.getcwd()+'/../..'
sys.path.append(namvi_mi_root)
from namv_mi.cost_model.cost_model import *
from namv_mi.utils import process_sim_results as sim
from namv_mi.utils.plot_templates import sub_dim
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def YTD_plot(vehicle, fig_YTD, ax_YTD, index, fig_YTD_axes_set, c, label, i):
    if not fig_YTD_axes_set and i==0:    # append new axes if not already set
        ax_YTD.append(fig_YTD.add_subplot(sub_dim(2, index, return_type=int)))
        ax_YTD[index].set_title(vehicle.name_nomode)
        if index == 0 or index == 2:
            ax_YTD[index].set_ylabel('YTD Cost (USD)')
        if index == 2 or index == 3:
            ax_YTD[index].set_xlabel('Time (years)')
   # get vehicle cost model
            # plot YTD cost vs time
    #print("Plotting ytd of {}_{} in axes {}".format(vehicle.name, vehicle.drive_train, index))
    ytd, cash_flow = vehicle.total()
    ax_YTD[index].plot(vehicle.time, ytd, c[i], label=label)#label=label)
    ax_YTD[index].legend()
    return ytd[-1]

def deployment_ytd_vect(mode_vehicles, AV_upgrade=2, Teleop_upgrade=4, Full_upgrade=6):
    mode_flows = {}
    for mode in mode_vehicles.keys():
        ytds, cash_flows = mode_vehicles[mode].total()
        mode_flows[mode] = cash_flows
    #print(mode_flows)
    year = 0
    normal_flows = mode_flows['normal'][0:AV_upgrade+1]
    normal_flows[-1] += mode_vehicles['normal'].assumptions['a-kit_cost']
    sd_flows = mode_flows['AV_SD'][AV_upgrade+1:Teleop_upgrade+1]
    try:
        sd_flows[-1] += mode_vehicles['normal'].assumptions['teleops_cost']
    except:
        normal_flows[-1] += mode_vehicles['normal'].assumptions['teleops_cost']
    fm_flows = mode_flows['AV_FM'][Teleop_upgrade+1:Full_upgrade+1]
    full_flows = mode_flows['AV_full'][Full_upgrade+1:mode_vehicles['normal'].time[-1]]

    #print(type(normal_flows))
    #print("Normal: {}\nSD: {}\nFM: {}\nfull:{}".format(normal_flows, sd_flows, fm_flows, full_flows))
    total_flow = np.concatenate((normal_flows, sd_flows, fm_flows, full_flows), axis=None)
    #print(total_flow)
    total_ytd = []
    for i in range(len(total_flow)):
        if i == 0:
            prev = 0
        else:
            prev = total_ytd[i-1]
        total_ytd.append(total_flow[i]+prev)        
        print("{} --> total_flow: {}\n\ntotal_ytd: {}\n\nprev: {}".format(i, total_flow, total_ytd, prev))

    
    return total_ytd, total_flow

    for t in mode_vehicles['normal'].time:
        # initial purchase
        x = 1



def main():
    # Get modes (normal, AV_SD, AV_FM, AV_full)
    modes = read_json('params/modes.json')     # defined in cost_model.cost_model

    # Define different drivetrains
    drive_trains = ['_EV', '_ICE']

    # Setup figures
    # Year to date plot
    figs = {'Small': plt.figure(),
            'Medium': plt.figure(),
            'Large': plt.figure(),
            'X-Large': plt.figure()}
    for key, val in figs.items():
        figs[key].suptitle(key)
    ax = {'Small': [],
          'Medium': [],
          'Large': [],
          'X-Large': []}

    for key, val in figs.items():
        ax[key].append(figs[key].add_subplot(121))
        ax[key].append(figs[key].add_subplot(122))

    fig_YTD_axes_set = False

    # plot line params
    plot_params = {'_EV': ['g', 'g:', 'g--', 'g*-'],
                    '_ICE': ['r', 'r:', 'r--', 'r*-']}

    # loop each drive train
    for ax_num, drive_train in enumerate(drive_trains):
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
            mode_vehicles = {}

            # loop each mode
            for i, mode in enumerate(modes):
                # Get cash flows for each mode
                vehicle = model(vehicles, index, yearly_miles, yearly_riders, mode=mode, inflation=True)
                mode_vehicles[mode] = vehicle
                
                #label = drive_train+'_'+mode
                #label = label[1:]
                # Get vehicle cost model
                #vehicle = model(vehicles, index, yearly_miles, yearly_riders, mode=mode, inflation=True)

                #final_yr_cost = YTD_plot(vehicle, fig_YTD, ax_YTD, index, fig_YTD_axes_set, c, label, i)       

            # ENTER MAIN PLOT FUNCTION HERE TO PLOT FOR EACH VEHICLE IN OWN FIGURE
            #print("{} {} --> {}".format(drive_train, vehicles.vehicle[index], mode_vehicles))
            total_ytd1, total_flow1 = deployment_ytd_vect(mode_vehicles, AV_upgrade=2, Teleop_upgrade=4, Full_upgrade=6) 
            total_ytd2, total_flow2 = deployment_ytd_vect(mode_vehicles, AV_upgrade=0, Teleop_upgrade=2, Full_upgrade=5)
            total_ytd3, total_flow3 = deployment_ytd_vect(mode_vehicles, AV_upgrade=0, Teleop_upgrade=0, Full_upgrade=3)


            print("YTD: {}\n\nFlow: {}\n".format(total_ytd1, total_flow1))
            ax[vehicles.vehicle[index]][ax_num].plot(vehicle.time[0:-1], total_flow1, label="Scenario 1")
            ax[vehicles.vehicle[index]][ax_num].plot(vehicle.time[0:-1], total_flow2, label="Scenario 2")
            ax[vehicles.vehicle[index]][ax_num].plot(vehicle.time[0:-1], total_flow3, label="Scenario 3")
            ax[vehicles.vehicle[index]][ax_num].set_xlabel("Time (years)", fontsize=20)
            ax[vehicles.vehicle[index]][0].set_ylabel("Cost (USD)", fontsize=20)
            ax[vehicles.vehicle[index]][ax_num].set_title(drive_train[1:], fontsize=20)
            ax[vehicles.vehicle[index]][ax_num].legend(fontsize=20)
            ax[vehicles.vehicle[index]][ax_num].grid()     

        #if ax_num == 1: 
        plt.savefig("plots/"+vehicles.vehicle[index])
        fig_YTD_axes_set = True # set axes set to true
    plt.show() # YTD_plot

