#! /usr/bin/env python3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json

import matplotlib

print(matplotlib.get_backend())
matplotlib.use("TkAgg")

#TODO -------------#
# --> Add parameters for different costs for AV, teleops, driver_salary, etc
# --> Add flags for teleops and AV for purchase and maintenance costs

# Import vehicle parameters from csv
def read_json(filename):
    PARAM = {}
    try:
        with open(filename, "r") as f:
            data = json.loads(f.read())
            for key, value in data.items():
                PARAM[key] = value
    except FileNotFoundError:
        print("(didn't find parameters.json)")
    return PARAM

class cost_gens:
    def __init__(self, model, assumptions_json='assumptions.json'):
        # Assign model to variable
        self.model = model

        # Get common assumptions
        self.assumptions = read_json(assumptions_json)

        # Define lists to store calculations at each iteration
        self.operation_costs = []
        self.maintenance_costs = []
        self.driver_costs = []

    def get_purchase_cost(self):
        return self.model.purchase

    def get_operation_gen(self, inflation=False):
        years = self.assumptions['years']
        miles = self.assumptions['miles/year']
        if inflation:
            inflate_rate = self.assumptions['inflation_rate']
        else: 
            inflate_rate = 0        
        year = 0
        while year < years:
            this_year_cost = miles*self.model.operation*(1+inflate_rate*year)
            self.operation_costs.append(this_year_cost)            
            YTD_cost = np.sum(self.operation_costs)
            year += 1
            yield YTD_cost, self.operation_costs

    def get_maintenance_gen(self, inflation=False):
        years = self.assumptions['years']
        miles = self.assumptions['miles/year']
        if inflation:
            inflate_rate = self.assumptions['inflation_rate']
        else: 
            inflate_rate = 0        
        year = 0
        while year < years:
            this_year_cost = miles*self.model.maintenance*(1+inflate_rate*year)
            self.maintenance_costs.append(this_year_cost)            
            YTD_cost = np.sum(self.maintenance_costs)
            year += 1
            yield YTD_cost, self.maintenance_costs

    def get_driver_gen(self, inflation=False):
        years = self.assumptions['years']
        miles = self.assumptions['miles/year']
        salary = self.assumptions['salary']
        if inflation:
            inflate_rate = self.assumptions['inflation_rate']
        else: 
            inflate_rate = 0
        year = 0
        while year < years:
            this_year_cost = self.model.driver_rate*salary*(1+inflate_rate*year)
            self.driver_costs.append(this_year_cost)            
            YTD_cost = np.sum(self.driver_costs)
            year += 1
            yield YTD_cost, self.driver_costs        

class model:
    def __init__(self, df, index, assumptions_json='assumptions.json', driver_rate=1.0, inflation=False):
        # Create variables from parameters in dataframe
        self.name = df.vehicle[index]               # name of vehicle model
        self.purchase = df.purchase[index]          # initial purchase cost
        self.maintenance = df.maintenance[index]    # cost per mile
        self.operation = df.operation[index]        # cost per mile
        self.passengers = df.passengers[index]      # passengers
        self.driver_rate = driver_rate              # driver pay rate {"Full AV": 0, "No AV": 1.0, "SD": 1.1, "FM": 1.15}
        
        # Get common assumptions
        self.assumptions = read_json(assumptions_json)
        # Get time array for plotting
        self.time = range(self.assumptions['years'])
        # Get object for model generators
        self.gens = cost_gens(self)

        # Operation cost generator
        self.operation_gen = self.gens.get_operation_gen(inflation=inflation)
    
        # Maintenance cost generator
        self.maintenance_gen = self.gens.get_maintenance_gen(inflation=inflation)

        # Driver cost generator
        self.driver_gen = self.gens.get_driver_gen(inflation=inflation)

    def oper(self):
        for year in range(self.assumptions['years']):
            YTD, history = next(self.operation_gen)   
        return YTD, history

    def maint(self):
        for year in range(self.assumptions['years']):
            YTD, history = next(self.maintenance_gen)   
        return YTD, history

    def driver(self):
        for year in range(self.assumptions['years']):
            YTD, history = next(self.driver_gen)   
        return YTD, history        
        

    ########## Print to console functions ##########
    def get_assumptions(self, filename):
        print(self.assumptions)

    def print_params(self):
        print('''Name: {}
        Passengers: {}
        Purchase Cost: $ {}
        Maintenance Cost: $ {} / mile
        Operation Cost: $ {} / mile
        '''.format(self.name, self.passengers, self.purchase,
                self.maintenance, self.operation))

if __name__ == '__main__':
    vehicles = pd.read_csv('vehicles.csv')
    models_dict = {}
    for index in vehicles.index:
        vehicle = model(vehicles, index, inflation=False)
        models_dict[vehicle.name] = vehicle
        vehicle.print_params()
        #print(vehicle.maint())
    plt.figure()
    ytd, y = models_dict['small'].oper()
    print(y)
    plt.plot(models_dict['small'].time, y)
    plt.show()