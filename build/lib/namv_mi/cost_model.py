import numpy as np
import time

def get_dep_vect(x, y, z, time=15):
    out_vector = []

    for t in range(time):
        if t<x:
            out_vector.append(0)
        elif t>=x and t<y:
            out_vector.append(1)
        elif t>=y and t<z:
            out_vector.append(2)
        elif t>=z:
            out_vector.append(3)
    
    return out_vector

def simplify(vector):
    simplified_vector = []
    for i in vector:
        if type(i) == list:
            if type(i[0]) == list:
                new = simplify(i)
            else:
                new = i
            simplified_vector += new
        else:
            simplified_vector.append(i)
    return simplified_vector
        

class costModel():
    #mode_name = ''
    sim_scenario = ''
    dep_scenario = ''
    def __init__(self, vehicle, sim_results_df, sim_params, 
            cost_model_assumptions, deployment_scenario, vehicle_mode_params=None):
        self.vehicle = vehicle
        self.sim_results_df = sim_results_df
        self.sim_params = sim_params
        self.cost_model_assumptions = cost_model_assumptions
        #self.vehicle_mode_params = vehicle_mode_params
        self.deployment_scenario = deployment_scenario
        self.deployment_scenario_vector = get_dep_vect(*self.deployment_scenario.values())
        self.yearly_miles = np.sum(self.sim_results_df.daily_dist)

        self.monthly_payments = {}
        self.remaining_payments = {}
        
        self._calculate_daily()

    def _calculate_daily(self):
        self.costs_dict = {"purchase": [],
                      "maintenance": [],
                      "operation": [],
                      "miles": [],
                      "total": []}
        for year_i in range(self.cost_model_assumptions["years"]):
            # purchase costs
            self.costs_dict["purchase"].append(self._purchase_cost(year_i))
            self.costs_dict["maintenance"].append(self._maintenance_cost(year_i))
            self.costs_dict["operation"].append(self._operation_cost(year_i))
            for _ in range(12):
                self.costs_dict["miles"].append(self.yearly_miles/12)
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
        dep_scen = self.deployment_scenario_vector[year_i]
        base_salary = self.cost_model_assumptions["salary"]

        if dep_scen == 0:        
            driver_salary = base_salary
        elif dep_scen == 1:
            driver_salary = base_salary*self.cost_model_assumptions["safety_raise"]
        elif dep_scen == 2:
            driver_salary = base_salary*self.cost_model_assumptions["FM_raise"]/self.cost_model_assumptions["fleet_size"]
        elif dep_scen == 3:
            driver_salary = 0
        #print(driver_salary)
        #time.sleep(1)
        monthly_pay_vect = []
        for _ in range(12):
            monthly_pay_vect.append(driver_salary/12)

        return monthly_pay_vect

    def _maintenance_cost(self, year_i):
        base_rate = self.vehicle.maintenance_cost
        dep_scen = self.deployment_scenario_vector[year_i]
        if dep_scen >= 1:
            base_rate += self.cost_model_assumptions["a-kit_maintenance"]
        elif dep_scen >= 2:
            base_rate += self.cost_model_assumptions["teleops_maintenance"]

        year_cost = base_rate*self.yearly_miles

        monthly_pmt = []
        for _ in range(12):
            monthly_pmt.append(year_cost/12)

        return monthly_pmt

    def _operation_cost(self, year_i):
        rate = self.vehicle.operation_cost

        year_cost = rate*self.yearly_miles

        monthly_pmt = []
        for _ in range(12):
            monthly_pmt.append(year_cost/12)

        val = self._driver_cost(year_i)
        #print(monthly_pmt, val)
        output = np.array(monthly_pmt) + np.array(val)
        return list(output)

    def _total_dict(self):
        years = []
        for i in range(len(self.costs_dict["purchase"])):
            year = []
            for j in range(len(self.costs_dict["purchase"][0])):
                total = self.costs_dict["purchase"][i][j] + self.costs_dict["maintenance"][i][j] + self.costs_dict["operation"][i][j]
                year.append(total)
            years.append(year)
        self.costs_dict["total"] = years
        for key, val in self.costs_dict.items():

            self.costs_dict[key] = simplify(self.costs_dict[key])#list(np.array(val, dtype=float).reshape(-1,1))

            #print("{} len(): {} len(len()): {}".format(key, len(val), len(val[0])))
        return self.costs_dict

    def get_run_name(self):
        return "{}-{}-{}".format(self.vehicle.vehicle_name, self.sim_scenario, self.dep_scenario)

    def summary(self, time_interval=""):
        print("\n+++++++++++++++++++++++++++++")
        print(self.get_run_name())
        self._total_dict()
        print(self.costs_dict)
        time.sleep(2)