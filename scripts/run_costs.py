import pandas as pd
import matplotlib.pyplot as plt
import time
from namv_mi import vehicle_model
from namv_mi import helpers
from namv_mi import simulation
from namv_mi import cost_model

def get_vect(in_array, dt=12):
    output = []
    summer = 0
    for i, val in enumerate(in_array):
        if i>0 and i%dt == 0:
            #print("appending {}".format(summer))
            output.append(summer)
            #print("reseting: summer --> 0")
            summer = 0
        summer += val
    #print("appending {}".format(summer))
    output.append(summer)
    return output

##### THINGS TO ADD TO ARGUMENT PARSER !!!!!!
output_directory = "output_data/simulation/"

# define vehicles csv path
vehicles_path = "src/resources/vehicles_general.csv"
# Get vehicle info from csv file
vehicles_df = pd.read_csv(vehicles_path)

# read sim_params
sim_params_path = "src/resources/simulation_assumptions.json"
sim_params_full = helpers.read_json(sim_params_path)
sim_scenarios = sim_params_full.keys()

# read cost model assumptions
cost_model_assumptions_path = "src/resources/cost_model_assumptions.json"
cost_model_assumptions = helpers.read_json(cost_model_assumptions_path)

# read vehicle modes
vehicle_modes_path = "src/resources/vehicle_modes.json"
vehicle_modes_full = helpers.read_json(vehicle_modes_path)
vehicle_modes = vehicle_modes_full.keys()

# read deployment scenarios
deployment_scenarios_path = "src/resources/deployment_scenarios.json"
deployment_scenarios_full = helpers.read_json(deployment_scenarios_path)
deployment_scenarios = deployment_scenarios_full.keys()


for _, vehicle in vehicles_df.iterrows():
    for sim_scenario in sim_scenarios:
        sim_params = sim_params_full[sim_scenario]

        # Get sim_results
        sim_results = simulation.main(vehicle, sim_params)
        sim_results_df = simulation.data_to_df(sim_results)
        #print(sim_results_df) 

        #for vehicle_mode in vehicle_modes:
        for dep_scenario in deployment_scenarios:
            deployment_scenario = deployment_scenarios_full[dep_scenario]
            
            #vehicle_mode_params = vehicle_modes_full[vehicle_mode]
            cm = cost_model.costModel(vehicle, sim_results_df, sim_params, 
                        cost_model_assumptions, deployment_scenario)#vehicle_mode_params, d)
            #cm.mode_name = vehicle_mode
            cm.sim_scenario = sim_scenario
            cm.dep_scenario = dep_scenario

            cost_dict = cm._total_dict()
            #print("\n{} total cost = {}".format(cm.get_run_name(), sum(cost_dict["total"])))
            #time.sleep(2)
            #print(sum(cost_dict["total"]))
            df = pd.DataFrame(cost_dict)
            df.to_csv("output_data/costs/{}.csv".format(cm.get_run_name()))

            '''
            plt.figure()

            t = range(180)

            total = cm.costs_dict["total"]
            purch = cm.costs_dict["purchase"]
            maint = cm.costs_dict["maintenance"]
            oper = cm.costs_dict["operation"]
            plt.plot(t, total, t, purch, t, maint, t, oper)

            plt.show()
            '''
            #cm.summary()
        # Calculate costs with cost model
