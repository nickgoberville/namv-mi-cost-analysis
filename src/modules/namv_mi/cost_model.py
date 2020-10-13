import numpy as np
import time

class costModel():
    mode_name = ''
    sim_scenario = ''
    dep_scenario = ''
    def __init__(self, vehicle, sim_results_df, sim_params, 
            cost_model_assumptions, vehicle_mode_params, deployment_scenario):
        self.vehicle = vehicle
        self.sim_results_df = sim_results_df
        self.sim_params = sim_params
        self.cost_model_assumptions = cost_model_assumptions
        self.vehicle_mode_params = vehicle_mode_params
        self.deployment_scenario = deployment_scenario

        self.monthly_payments = {}
        self.remaining_payments = {}

        self._calculate_daily()

    def _calculate_daily(self):
        self.costs_dict = {"purchase": [],
                      "maintenance": [],
                      "operation": [],
                      "driver": [],
                      "total": []}
        for year_i in range(self.cost_model_assumptions["years"]):
            # purchase costs
            self.costs_dict.append(self._purchase_cost(year_i))
            # maintenance costs
            ##
            # operation costs
            ##
            # driver costs
            ##

    def _purchase_cost(self, year_i, rate=0.05, loan_t=5, n_compounded=12):
        compounded_rate = rate/n_compounded#(1+rate)**(1/n_compounded) - 1

        if year_i == self.deployment_scenario["AV_upgrade"]:
            a_kit_cost = self.cost_model_assumptions["a-kit_cost"]
            a_kit_payment = -1*np.pmt(compounded_rate, loan_t*n_compounded, a_kit_cost)
            self.monthly_payments["a-kit"] = a_kit_payment
            self.remaining_payments["a-kit"] = loan_t*n_compounded
        elif year_i > self.deployment_scenario["AV_upgrade"]:
            self.remaining_payments["a-kit"] -= n_compounded
            if self.remaining_payments["a-kit"] <= 0:
                self.monthly_payments["a-kit"] = 0
        
        if year_i == self.deployment_scenario["teleop_upgrade"]:
            teleop_cost = self.cost_model_assumptions["teleops_cost"]
            teleop_payment = -1*np.pmt(compounded_rate, loan_t*n_compounded, teleop_cost)
            self.monthly_payments["teleop"] = teleop_payment
            self.remaining_payments["teleop"] = loan_t*n_compounded
        elif year_i > self.deployment_scenario["teleop_upgrade"]:
            self.remaining_payments["teleop"] -= n_compounded
            if self.remaining_payments["teleop"] <= 0:
                self.monthly_payments["teleop"] = 0       
        
        if year_i == 0:
            shuttle_cost = self.vehicle.purchase_cost#self.cost_model_assumptions["teleops_cost"]
            shuttle_payment = -1*np.pmt(compounded_rate, loan_t*n_compounded, shuttle_cost)
            self.monthly_payments["shuttle"] = shuttle_payment
            self.remaining_payments["shuttle"] = loan_t*n_compounded
        elif year_i > 0:
            self.remaining_payments["shuttle"] -= n_compounded
            if self.remaining_payments["shuttle"] <= 0:
                self.monthly_payments["shuttle"] = 0  

        #teleops_cost = self.cost_model_assumptions["teleops_cost"]
        #purchase_cost = self.vehicle.purchase_cost

        #total_purchase = a_kit_cost + teleops_cost + purchase_cost
        
        self.total_monthly_payment = np.sum(list(self.monthly_payments.values()))#-1*np.pmt(compounded_rate, loan_t*n_compounded, total_purchase)
        #print("Monthly: {}".format(self.total_monthly_payment))
        #self.daily_payment = self.total_monthly_payment * n_compounded * 1/len(self.sim_results_df)#(self.sim_params["days/week"]*self.sim_params["weeks/year"])
        #print("Daily: {}".format(self.daily_payment))
        #this_year_array = [self.daily_payment for i in range(len(self.sim_results_df))]
        this_year_array = [self.total_monthly_payment for i in range(12)]#len(self.sim_results_df))]
        #print(this_year_array)
        #print(len(this_year_array))
        #if year_i >=6: time.sleep(5)
        #print(monthly_payment)
        #time.sleep(5)
        #return total_purchase
        return this_year_array

    def _driver_cost(self, year_i):
        pass

    def summary(self, time_interval=""):
        print("\n+++++++++++++++++++++++++++++")
        print("{}.{}.{}.{}".format(self.vehicle.vehicle_name, self.mode_name, self.sim_scenario, self.dep_scenario))
        print(self.monthly_payments)
        time.sleep(2)