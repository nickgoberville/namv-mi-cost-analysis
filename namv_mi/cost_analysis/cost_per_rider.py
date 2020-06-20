#! /usr/bin/env python3
import os, sys
namvi_mi_root = os.getcwd()+'/../..'
sys.path.append(namvi_mi_root)
from namv_mi.cost_model.cost_model import *
from namv_mi.utils import process_sim_results as sim
from namv_mi.utils.plot_templates import barPlot, sub_dim

def main():
    # Get modes (normal, AV_SD, AV_FM, AV_full)
    modes = read_json('params/modes.json')     # defined in cost_model.cost_model

    # Define different drivetrains
    drive_trains = ['_EV', '_ICE']        #TODO REMOVE THE COMMENTED PART IN HERE

    # cost per rider plot
    riderbar = barPlot(qty=2, barperVal=4, suptitle="Cost per Rider")

    # plot line params
    colors = [(77/255, 148/255, 255/255),
            (255/255, 51/255, 51/255),
            (102/255, 153/255, 0/255),
            (91/255, 91/255, 141/255),
            (80/255, 80/255, 150/255)]

    #Setup per rider plot
    barWidth = 0.2
    r1 = np.arange(4)      #Spacing for non AV
    r2 = [x + barWidth for x in r1]     #Spacing for AV w/ SD
    r3 = [x + barWidth for x in r2]     #Spacing for AV w/ FM
    r4 = [x + barWidth for x in r3]     #Spacing for AV w/o operator

    legs = []

    # loop each drive train
    for enum, drive_train in enumerate(drive_trains):
        vehicles = pd.read_csv('vehicles/vehicles'+drive_train+'.csv')   # extract vehicle models from csv file
        labels_set = False
        rider_vals = {'normal': [],
                'AV_SD': [],
                'AV_FM': [],
                'AV_full': []}
        # loop each vehicle size (S, M, L, XL)
        for index in vehicles.index:
            sim_results_path = 'sim_runs/scenario_'+str(index+1)+'/sim_results/'+vehicles.vehicle[index]+drive_train+'.csv'
            sim_results_df = pd.read_csv(sim_results_path)   # get simulation results for vehicle
            sim_results = sim.Results(sim_results_df)           # Process simulation results
            yearly_miles = np.sum(sim_results.daily_dist)       # Get yearly miles
            yearly_riders = np.sum(sim_results.daily_rides)     # Get yearly_riders

            # loop each mode
            for i, mode in enumerate(modes):
                if len(legs) != 4:
                    legs.append(mode)
                label = drive_train+'_'+mode
                label = label[1:]
                # Get vehicle cost model
                vehicle = model(vehicles, index, yearly_miles, yearly_riders, mode=mode, inflation=False, assumptions_json="params/assumptions.json", modes_json="params/modes.json")
                # Get ytd & cash flow vectors
                ytd, cash_flow = vehicle.total()
                # Calculate cost per rider vector
                ytd_rider, cash_flow_rider = vehicle.per_rider()
                cost_per_rider = ytd_rider[-1]
                # Append vectors to rider_vals dict
                rider_vals[mode].append(cost_per_rider)

        fig_YTD_axes_set = True # set axes set to true

        riderbar.add_val(rider_vals, enum)
    print(rider_vals)

    riderbar.plot(plot_order=['normal', 'AV_SD', 'AV_FM', 'AV_full'], orientation="Vertical", colors=colors)

    riderbar.format(['Small', 'Medium', 'Large', 'X-Large'], ['EV', 'ICE'], ['normal', 'AV_SD', 'AV_FM', 'AV_full'], label_fsize=20, legend_loc="upper right", axis_label='Cost ($/rider)', orientation="Vertical")

    riderbar.show()