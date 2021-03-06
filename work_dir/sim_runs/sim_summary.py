#! /usr/bin/env python3
import glob
import pandas as pd
import json

for scenario in glob.glob('scenario*'):
    for vehicle in glob.glob(scenario+'/sim_results/*.csv'):
        vehicle_data = pd.read_csv(vehicle)
        print('============= {} ============'.format(vehicle))
        print(vehicle_data.describe())
        print('\n')
        