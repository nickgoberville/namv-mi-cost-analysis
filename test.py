import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as tick
import glob
import numpy as np

from namv_mi import vehicle_model
from namv_mi import helpers
from namv_mi import simulation
from namv_mi import cost_model

def get_vect(in_array, dt=12, inflation=False):
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

def reduction(a, b):
    return (a-b)/b*100

@tick.FuncFormatter
def reformat_large_tick_values(tick_val, pos):
    """
    Turns large tick values (in the billions, millions and thousands) such as 4500 into 4.5K and also appropriately turns 4000 into 4K (no zero after the decimal).
    """
    if tick_val >= 1000000000:
        val = round(tick_val/1000000000, 1)
        new_tick_format = '{:}B'.format(val)
    elif tick_val >= 1000000:
        val = round(tick_val/1000000, 1)
        new_tick_format = '{:}M'.format(val)
    elif tick_val >= 1000:
        val = round(tick_val/1000, 1)
        new_tick_format = '{:}K'.format(val)
    elif tick_val < 1000:
        new_tick_format = round(tick_val, 1)
    else:
        new_tick_format = tick_val

    # make new_tick_format into a string value
    new_tick_format = str(new_tick_format)
    
    # code below will keep 4.5M as is but change values such as 4.0M to 4M since that zero after the decimal isn't needed
    index_of_decimal = new_tick_format.find(".")
    
    if index_of_decimal != -1:
        value_after_decimal = new_tick_format[index_of_decimal+1]
        if value_after_decimal == "0":
            # remove the 0 after the decimal point since it's not needed
            new_tick_format = new_tick_format[0:index_of_decimal] + new_tick_format[index_of_decimal+2:]
            
    return new_tick_format

def sumitup(in_vect):
    x = 0
    new_vect = []
    for i in in_vect:
        x+=i
        new_vect.append(x)
    return new_vect


data_files = glob.glob("output_data/costs/*")
filtered_data = []

fig = plt.figure()
ax = fig.add_subplot(111)
drivetrain = "EV"
size = "XLarge"
# baseline plot
df = pd.read_csv("output_data/costs/{}_{}-scenario_0-baseline.csv".format(size, drivetrain))
baseline = sumitup(get_vect(df.total))
ax.plot(range(15), baseline)#np.zeros((15,1)))
totals = []
for data in data_files:
    if (size in data) and ("C" == data[-5]):# and ("XLarge" not in data):# and ("B" != data[-5]) and ("C" != data[-5]) and ("baseline" in data): #"Large" in data or "Medium" in data or "XLarge" in data:# and "EV" in data and "scenario_0-A" in data:
        
        filtered_data.append(data)
        df = pd.read_csv(data)
        #print(df)
        name = data.split('/')[-1][:-4]
        print(name)
        y = sumitup(get_vect(df.total))
        totals.append(y[-1])
        print(y[-1])
        print('\n')
        ax.plot(range(15), y)
        
        #ax.plot(range(15), -np.array(sumitup(get_vect(df.total))) + np.array(baseline))


print(totals[-1]-totals[0])
print("EV '%' reduction: {}".format(reduction(totals[-1], baseline[-1])))
print("ICE '%' reduction: {}".format(reduction(totals[0], baseline[-1])))
y_formatter = tick.ScalarFormatter(useOffset=True)
ax.yaxis.set_major_formatter(reformat_large_tick_values)
#print(filtered_data)



plt.show()
'''
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
vehicles_path = "src/resources/vehicles.csv"
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

        for vehicle_mode in vehicle_modes:
            for dep_scenario in deployment_scenarios:
                deployment_scenario = deployment_scenarios_full[dep_scenario]
                
                vehicle_mode_params = vehicle_modes_full[vehicle_mode]
                cm = cost_model.costModel(vehicle, sim_results_df, sim_params, 
                            cost_model_assumptions, vehicle_mode_params, deployment_scenario)
                cm.mode_name = vehicle_mode
                cm.sim_scenario = sim_scenario
                cm.dep_scenario = dep_scenario

                cm._total_dict()

                df = pd.DataFrame(cm.costs_dict)
                df.to_csv("output_data/costs/{}.csv".format(cm.get_run_name()))

                
                plt.figure()

                t = range(180)

                total = cm.costs_dict["total"]
                purch = cm.costs_dict["purchase"]
                maint = cm.costs_dict["maintenance"]
                oper = cm.costs_dict["operation"]
                plt.plot(t, total, t, purch, t, maint, t, oper)

                plt.show()
                
                #cm.summary()
            # Calculate costs with cost model
'''
