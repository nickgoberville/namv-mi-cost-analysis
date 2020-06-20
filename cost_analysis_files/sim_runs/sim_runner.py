#! /usr/bin/env python3

import os, sys
root = os.getcwd()+'/../..'
sys.path.append(root)
cost_analysis_root = root + '/cost-analysis/'
from random import randint, gauss
from cost_model.cost_model import *
from simulation.rider_sim import *
import pandas as pd
import time
import argparse
import glob

def data_to_year_csv(week_list, output_filename):
    df_dict = {'riders_left': [],
                'daily_dist': [],
                'completed_rides': [],
                'wait_times_list': []}

    for day in week_list:
        for data in day:
            df_dict['riders_left'].append(data["riders_left_behind"])
            df_dict['daily_dist'].append(data["distance"])
            df_dict['completed_rides'].append(data["completed_rides"])
            df_dict['wait_times_list'].append(data["wait times"])

    df = pd.DataFrame(df_dict, columns=df_dict.keys())
    df.to_csv(output_filename, index=True, header=True)

if __name__ == '__main__':
    #parser defined in simulation.rider_sim
    #parser.add_argument('-d', '--drive_train', help='Identify drive train to run simulations with.', action='store_true', default=False)    
    #parser.add_argument('run_number', help='Identify which simulation scenario to run.', type=int)
    #args = parser.parse_args()
    #run_num = args.run_number
    #verbose = args.verbose
    
    # Uncomment which drive train to run simulations with
    #vehicles = pd.read_csv(cost_analysis_root+'vehicles_EV.csv')
    #vehicles = pd.read_csv(cost_analysis_root+'vehicles_ICE.csv')
    

    modes = read_json(cost_analysis_root+'modes.json')
    models_dict = {}

    types = ['Small', 'Medium', 'Large', 'X-Large']
    #for j, scenario in enumerate(glob.glob('scenario*')):


    for i in range(2):
        if i == 0:
            vehicles = pd.read_csv(cost_analysis_root+'vehicles_EV.csv')
        else:
            vehicles = pd.read_csv(cost_analysis_root+'vehicles_ICE.csv') 
            #for index in vehicles.index:
        vehicle = model(vehicles, run_num-1, inflation=False, assumptions_json=cost_analysis_root+'assumptions.json', modes_json=cost_analysis_root+'modes.json')
        week_list = main(vehicle, real_time=False, verbose=verbose)
        name = vehicle.name[0:-6]   # remove "_normal" from vehicle name
        output_filename = "scenario_" + str(run_num) + "/sim_results/" + name + vehicle.drive_train + ".csv"
        data_to_year_csv(week_list, output_filename)