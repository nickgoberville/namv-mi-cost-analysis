#! /usr/bin/env python3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json

#TODO -------------#
# --> Add docstrings for everything

# Import vehicle parameters from csv
def read_json(filename):
    PARAM = {}
    try:
        with open(filename, "r") as f:
            data = json.loads(f.read())
            for key, value in data.items():
                PARAM[key] = value
    except FileNotFoundError:
        print("DIDN'T FIND {}!".format(filename))
    return PARAM

class cost_gens:
    def __init__(self, model, assumptions_json='params/assumptions.json'):
        # Assign model to variable
        self.model = model

        # Get common assumptions
        self.assumptions = read_json(assumptions_json)
        # Get miles_per_year
        self.miles_per_year = self.model.miles_per_year

    def get_purchase_cost(self, inflation=False, years_ahead=0):
        # Calculate purchase cost with AV, teleops options
        a_kit = self.assumptions['a-kit_cost']
        teleops_kit = self.assumptions['teleops_cost']
        purchase = self.model.purchase + a_kit*self.model.is_AV + teleops_kit*self.model.is_teleops
        return purchase*(1+inflation*years_ahead)

    def get_operation_gen(self, inflation, time_frame, miles_vect):
        if time_frame == 'years':
            end_t = self.assumptions['years']
            # Define variables for calculation
            self.operation_cash_flow = [0]
            self.operation_YTD = [0]
            
            miles = self.miles_per_year
            if inflation:
                inflate_rate = self.assumptions['inflation_rate']
            else: 
                inflate_rate = 0        
            
            # initialize year
        t = 0

            # Loop generator
        while t < end_t:
            this_year_cost = miles*self.model.operation*(1+inflate_rate*year)
            self.operation_cash_flow.append(this_year_cost)            
            self.operation_YTD.append(np.sum(self.operation_cash_flow))
            t += 1
            yield self.operation_YTD, self.operation_cash_flow

    def get_maintenance_gen(self, inflation):
      # additional maintenance for AV and teleop options
        self.maintenance_cash_flow = [0]
        self.maintenance_YTD = [0]
        years = self.assumptions['years']
        miles = self.miles_per_year
        a_kit = self.assumptions['a-kit_maintenance']
        teleops_kit = self.assumptions['teleops_maintenance']
        if inflation:
            inflate_rate = self.assumptions['inflation_rate']
        else: 
            inflate_rate = 0        
        year = 0
        while year < years:
            maint_AV = a_kit*self.model.is_AV
            maint_teleops = teleops_kit*self.model.is_teleops
            this_year_cost = miles*(self.model.maintenance + maint_AV + maint_teleops)*(1+inflate_rate*year)
            self.maintenance_cash_flow.append(this_year_cost)            
            self.maintenance_YTD.append(np.sum(self.maintenance_cash_flow))
            year += 1
            yield self.maintenance_YTD, self.maintenance_cash_flow

    def get_driver_gen(self, inflation, FM_flag=False):
        self.driver_cash_flow = [0]
        self.driver_YTD = [0]
        years = self.assumptions['years']
        miles = self.miles_per_year
        salary = self.assumptions['salary']
        if inflation:
            inflate_rate = self.assumptions['inflation_rate']
        else: 
            inflate_rate = 0
        year = 0
        while year < years:
            this_year_cost = self.model.driver_rate*salary*(1+inflate_rate*year)
            if FM_flag: this_year_cost /= self.assumptions['fleet_size']
            self.driver_cash_flow.append(this_year_cost)            
            self.driver_YTD.append(np.sum(self.driver_cash_flow))
            year += 1
            yield self.driver_YTD, self.driver_cash_flow        

class model:
    def __init__(self, df, index, miles_per_year=0, riders_per_year=100, assumptions_json='params/assumptions.json', modes_json='params/modes.json', inflation=False, mode='normal', time_period='year'):
        modes = read_json(modes_json)
        self.mode = mode
        # Create variables from parameters in dataframe
        self.name_nomode = df.vehicle[index]
        self.name = df.vehicle[index]+'_'+mode               # name of vehicle model
        self.purchase = df.purchase[index]          # initial purchase cost
        self.maintenance = df.maintenance[index]    # cost per mile
        self.operation = df.operation[index]        # cost per mile
        self.passengers = df.passengers[index]      # passengers
        self.driver_rate = modes[mode]['driver_rate']              # driver pay rate {"Full AV": 0, "No AV": 1.0, "SD": 1.1, "FM": 1.15}
        self.is_AV = modes[mode]['is_AV']
        self.is_teleops = modes[mode]['is_teleops']
        self.miles_per_year = miles_per_year
        self.category = df.category[index]
        self.drive_train = df.drive_train[index]
        self.riders_per_year = riders_per_year

        self.inflation = inflation
        # Get common assumptions
        self.assumptions = read_json(assumptions_json)
        # Get time array for plotting
        self.time = range(self.assumptions['years']+1)
        self.time_period = time_period
        # Get object for model generators
        self.gens = cost_gens(self)

        # Operation cost generator
        self.operation_gen = self.gens.get_operation_gen(inflation=self.inflation)
    
        # Maintenance cost generator
        self.maintenance_gen = self.gens.get_maintenance_gen(inflation=self.inflation)

        # Driver cost generator
        self.driver_gen = self.gens.get_driver_gen(inflation=self.inflation, FM_flag=self.is_teleops)

    def description(self):
        print("{} in driving mode: {}\n".format(self.name, self.mode))

    def oper(self):
        for year in range(self.assumptions[self.time_period]):
            YTD_history, cash_flows = next(self.operation_gen)   
        self.operCosts = []
        self.operCosts.append(YTD_history)
        self.operCosts.append(cash_flows)
        return YTD_history, cash_flows

    def maint(self):
        for year in range(self.assumptions[self.time_period]):
            YTD_history, cash_flows = next(self.maintenance_gen)   
        self.maintCosts = []
        self.maintCosts.append(YTD_history)
        self.maintCosts.append(cash_flows)
        return YTD_history, cash_flows

    def driver(self):
        for year in range(self.assumptions[self.time_period]):
            YTD_history, cash_flows = next(self.driver_gen)   
        self.driverCosts = []
        self.driverCosts.append(YTD_history)
        self.driverCosts.append(cash_flows)
        return YTD_history, cash_flows              

    def purch(self):
        self.purchaseCost = [self.gens.get_purchase_cost(inflation=self.inflation)]
        return self.gens.get_purchase_cost(inflation=self.inflation)

    def run_calcs(self):
        try:
            self.calcs_run
        except:
            self.oper()
            self.maint()
            self.driver()
            self.purch()
            self.calcs_run = True

    def total(self, include_purchase=True):
        self.run_calcs()
        oper_YTD, oper_flow = self.operCosts
        maint_TYD, maint_flow = self.maintCosts
        drive_YTD, drive_flow = self.driverCosts

        cash_flows = np.add(oper_flow, np.add(maint_flow, drive_flow))
        YTD = np.add(oper_YTD, np.add(maint_TYD, drive_YTD))
        
        # If we incl
        if include_purchase:
            cash_flows[0] += self.purch()
            for i in range(len(YTD)):
                YTD[i] += self.purch()
        return YTD, cash_flows
    
    def per_rider(self, include_purchase=True):
        YTD, cash_flows = self.total(include_purchase=include_purchase)
        avg_per_year = np.true_divide(YTD, self.assumptions['years'])
        cost_per_rider = np.true_divide(avg_per_year, self.riders_per_year)

        cash_flows_per_rider = np.true_divide(cash_flows, self.passengers)
        return cost_per_rider, cash_flows_per_rider

    ########## Print to console functions ##########
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
    modes = read_json('modes.json')
    models_dict = {}
    for index in vehicles.index:
        for mode in modes.keys():
            vehicle = model(vehicles, index, 0, inflation=False, mode=mode)
            models_dict[vehicle.name] = vehicle
            vehicle.print_params()
            print("PURCHASE: {}".format(vehicle.purch()))
    #plt.figure()
    #ytd, y = models_dict['small'].oper()
    #print(y)
    #plt.plot(models_dict['small'].time, y)
    #plt.show()