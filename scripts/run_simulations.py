import pandas as pd
import argparse
import matplotlib.pyplot as plt

from namv_mi import vehicle_model
from namv_mi import helpers
from namv_mi import simulation

##### THINGS TO ADD TO ARGUMENT PARSER !!!!!!
output_directory = "output_data/simulation/"

def main():
    # define vehicles csv path
    vehicles_path = "src/resources/vehicles.csv"
    # Get vehicle info from csv file
    vehicles_df = pd.read_csv(vehicles_path)

    # read sim_params
    sim_params_path = "src/resources/simulation_assumptions.json"
    sim_params_full = helpers.read_json(sim_params_path)
    scenarios = sim_params_full.keys()

    for _, vehicle in vehicles_df.iterrows():
        for scenario in scenarios:
            sim_params = sim_params_full[scenario]

            # Get sim_results
            sim_results = simulation.main(vehicle, sim_params)
            sim_results_df = simulation.data_to_df(sim_results) 

            # Export results
            sim_results_output_path = output_directory+"{}-{}.csv".format(vehicle.vehicle_name, scenario)
            sim_results_df.to_csv(sim_results_output_path, index=True, header=True) 


if __name__ == '__main__':
    main()