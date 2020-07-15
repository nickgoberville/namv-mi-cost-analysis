#! /usr/bin/env python3
import os, sys
namvi_mi_root = os.getcwd()+'/../..'
sys.path.append(namvi_mi_root)
from namv_mi.cost_model.cost_model import *
from namv_mi.utils import process_sim_results as sim
from namv_mi.utils.plot_templates import barPlot, sub_dim

# Get all daily ride data into a csv file for drivetrain, vehicle size, and deployment type scenario

def main():
    # Get modes (normal, AV_SD, AV_FM, AV_full)
    modes = read_json('params/modes.json')     # defined in cost_model.cost_model

    # Define different drivetrains
    drive_trains = ['_EV', '_ICE']        #TODO REMOVE THE COMMENTED PART IN HERE

    # loop each drive train
    for enum, drive_train in enumerate(drive_trains):
        vehicles = pd.read_csv('vehicles/vehicles'+drive_train+'.csv')   # extract vehicle models from csv file
        rider_vals = {'normal': [],
                'AV_SD': [],
                'AV_FM': [],
                'AV_full': []}
        # loop each vehicle size (S, M, L, XL)
        for index in vehicles.index:
            sim_results_path = 'sim_runs/scenario_'+str(index+1)+'/sim_results/'+vehicles.vehicle[index]+drive_train+'.csv'
            sim_results_df = pd.read_csv(sim_results_path)   # get simulation results for vehicle
            sim_results = sim.Results(sim_results_df)           # Process simulation results
            print(sim_results.show())
            yearly_miles = np.sum(sim_results.daily_dist)       # Get yearly miles
            yearly_riders = np.sum(sim_results.daily_rides)     # Get yearly_riders

            # loop each mode
            for i, mode in enumerate(modes):
                # Get vehicle cost model
                vehicle = model(vehicles, index, yearly_miles, yearly_riders, mode=mode, inflation=False, assumptions_json="params/assumptions.json", modes_json="params/modes.json")
                # Get ytd & cash flow vectors
                ytd, cash_flow = vehicle.total()
                # Calculate cost per mile vector
                cost_per_mile = ytd[-1]/((vehicle.miles_per_year)*vehicle.time[-1])
                # Append vectors to rider_vals dict
                rider_vals[mode].append(cost_per_mile)
