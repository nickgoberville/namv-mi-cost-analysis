#! /usr/bin/env python3


#--COST MODEL PARAMETERS----------------------------------------------------------#
# units: 2019 U.S. $, $/mile, $/mile
assumptions =   {"Years": 15,
                 "Miles/year": 15000,
                 "Fleet size": 2,
                 "Salary": 55000,
                 "SO_raise": 1.1,
                 "FM_raise": 1.15,
                 "Autonomous kit": 50000,
                 "teleops": 5000,
                 "Autonomous maintenance": 0.01,
                 "$/kWh": 0.13,
                 "$/gal unlead": 2.6}

km2mi = 1.60934
BEV_bus_power = 0.8*km2mi #kWh/mi
BEV_bus_operation = BEV_bus_power*assumptions['$/kWh']

Devpod_power = 6/30 #kWh/mi
Devpod_operation = Devpod_power*assumptions['$/kWh']

Gas_van_operation = assumptions['$/gal unlead']/15  # 15 mpg
Gas_van_maintenance = 2000/6000

Golfcart_operation = assumptions['$/gal unlead']/25 # 25mpg

Pod12_power = 33/124 #kWh/mi
Pod12_operation = assumptions['$/kWh']*Pod12_power 
vehicle =   {"\nSmall BEV \n(4 seats)": {'Purchase': 96300,     # NEED SOURCE
                        'Maintenance': 0.033,       # Source is ok, can find better
                        'Operation': Devpod_operation,
                        'Passengers': 4},      # Source is ok, can find better

             "\nSmall ICE \n(4 seats)": {'Purchase': 20000,     # NEED SOURCE
                           'Maintenance': 0.033,       # Source is ok, can find better
                           'Operation': Golfcart_operation,
                           'Passengers': 4},     # Source is ok, can find better 

             "\nSmall HEV \n(4 seats)": {'Purchase': 30000,      # NEED SOURCE
                             'Maintenance': 0.035,      # Source is ok, can find better 
                             'Operation': Golfcart_operation*0.75,
                             'Passengers': 4},
                     
             "\nMid-size BEV \n(15 seats)": {'Purchase': 280000,
                      'Maintenance': 0.10,
                      'Operation': Pod12_operation,
                      'Passengers': 13},
             
             #"\nNAVYA \n(15 seats)": {'Purchase': 320000,
             #         'Maintenance': 0.10,
             #         'Operation': Pod12_operation*1.1,
             #         'Passengers': 15},    
             
             "\nMid-size ICE \n(15 seats)": {'Purchase': 55000,
                      'Maintenance': Gas_van_maintenance,
                      'Operation': Gas_van_operation,
                      'Passengers': 15},
                      
             "\nLarge BEV \n(30 seats)": {'Purchase': 350000,
                      'Maintenance': 0.18,
                      'Operation': BEV_bus_operation,
                      'Passengers': 30},
                      
              "\nLarge ICE \n(30 seats)": {'Purchase': 247000,
                      'Maintenance': 0.354,
                      'Operation': 0.35, # from bts.gov
                      'Passengers': 30},                                    # Source is ok, can find better 
              
              "\nLarge HEV \n(30 seats)": {'Purchase': 275000,
                      'Maintenance': 0.44,
                      'Operation': 0.24,
                      'Passengers': 30},#,
                      
              "ICE":    {'Purchase': 25000,
                         'Maintenance': 0.2,
                         'Operation': 0.3,
                         'Passengers': 5},

              "HEV":    {'Purchase': 30000,
                         'Maintenance': 0.3,
                         'Operation': 0.2,
                         'Passengers': 5},

              "BEV":    {'Purchase': 35000,
                         'Maintenance': 0.035,
                         'Operation': 0.05,
                         'Passengers': 5}}

evalu = {"non_AV": {"is_AV": 'N',
                    "teleops": False,
                    "vals": []},

         "AV_SD": {"is_AV": 'S',
                   "teleops": False,
                   "vals": []},

         "AV_FM": {"is_AV": 'Y',
                   "teleops": True,
                   "vals": []},

         "AV_full": {"is_AV": 'Y',
                     "teleops": False,
                     "vals": []}}

cost_calculations = ['Purchase', 'Maintenance', 'Fuel', 'Operator']

#--RIDERSHIP EVALUTATION------------------------------------------------------------#
DPW = 5         #Days per week
WPY = 52        #Weeks per year
HPD = 8         #Hours per day
avg_ride_time = 1/6
avg_mph = assumptions['Miles/year']/(DPW*WPY*HPD)
miles_per_trip = avg_mph*avg_ride_time
rider_percent_per_trip = 0.1
route_data = {'WMU': {'distance': 3,
                      'riders/day': 1000,
                      'trips/hour': 2,
                      'stops': 13,
                      'hours': 17,
                      'miles': 20},
                      
              'low': {'distance': 1.5,
                      'riders/day': 100,
                      'trips/hour': 4,
                      'stops': 5,
                      'hours': 8},
                      
              'OD':  {'distance': 0.5,          # On Demand
                      'riders/day': 300,
                      'trips/hour': 8,
                      'hours': 24,
                      'riders/trip': 2.5}}

#miles_per_rider = {'WMU': }

market_AVs =    {"Aurrigo Devpod":  {"Passengers": 3,
                                     "Purchase Cost": 200000},
                                    
                 "Hypothetic 6":    {"Passengers": 6,
                                     "Purchase Cost": 250000},
                         
                 "Aurrigo Pod12":   {"Passengers": 12,
                                     "Purchase Cost": 300000},
                           
                 "NAVYA AUTONOM":   {"Passengers": 15,
                                     "Purchase Cost": 350000}}

#--PLOT FORMATTING PARAMETERS-------------------------------------------------------#
font = 'Times New Roman'
colors = [(77/255, 148/255, 255/255),
          (255/255, 51/255, 51/255),
          (102/255, 153/255, 0/255),
          (91/255, 91/255, 141/255),
          (80/255, 80/255, 150/255)]

def main():
    for val in enumerate(vehicle):
        i=0
        print('i: {} val: {}'.format(i,val))
        if val == 'ICE':
            print('YUP')
    print(len(vehicle))
    evalu['non_AV']['vals'].append(5)
    print(evalu['non_AV']['vals'])

if __name__ == '__main__':
    main()

