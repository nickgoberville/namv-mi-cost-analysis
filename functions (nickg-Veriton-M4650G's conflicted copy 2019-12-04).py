#! /usr/bin/env python3
import parameters as p
import matplotlib.pyplot as plt
import numpy as np

#--COST MODEL FUNCTIONS----------------------------------------------------------------------#

def purchase(vtype, is_AV, teleops):
    purchase_val = p.vehicle[vtype]['Purchase']
    if is_AV == 'N':
        pass
    elif is_AV == 'S' or is_AV == 'Y':
        purchase_val += p.assumptions['Autonomous kit']
    elif is_AV == 'Y' and teleops:
        purchase_val += p.assumptions['Autonomous kit'] + p.assumptions['telops']
    return purchase_val

def operation(vtype, is_AV, teleops, t=p.assumptions['Years'], miles=p.assumptions['Miles/year']):
    operation_val = p.vehicle[vtype]['Operation']
    return miles*operation_val*t

def maintenance(vtype, is_AV, teleops, t=p.assumptions['Years'], miles=p.assumptions['Miles/year']):
    av_maint = 0
    if is_AV == 'Y' or is_AV == 'S':
        av_maint = p.assumptions['Autonomous maintenance']
    if teleops:
        av_maint*=1.05        
    maintenance_val = p.vehicle[vtype]['Maintenance'] + av_maint
    return miles*maintenance_val*t

def operator(is_AV, teleops, t=p.assumptions['Years'], fm=p.assumptions['Fleet size']):
    '''is_AV: 'N' = not autonomous
              'S' = semi-autonomous (Has safety operator)
              'Y' = fully-autonomous (No safety operator in vehicle)

        teleops are either True (Using teleops) or False (not using teleops)
    '''
    if is_AV == 'N':
        #print('is_AV is N')
        promo = 1         #10% raise for AV Operator
    elif is_AV == 'S':
        promo = p.assumptions['SO_raise']
    elif is_AV == 'Y' and teleops:
        promo = p.assumptions['FM_raise'] / fm
    elif is_AV == 'Y':
        promo = 0
    return p.assumptions['Salary']*promo*t

def total(vtype, is_AV, teleops, t=p.assumptions['Years'], fm=p.assumptions['Fleet size'], miles=p.assumptions['Miles/year']):
    return purchase(vtype, is_AV, teleops) + operation(vtype, is_AV, teleops, t, miles) + maintenance(vtype, is_AV, teleops, t, miles) + operator(is_AV, teleops, t=t, fm=fm)

def cost_per_mile(vtype, is_AV, teleops, which_cost='total', t=p.assumptions['Years'], miles=p.assumptions['Miles/year']):
    divi = miles*t
    if which_cost == 'total':
        return total(vtype, is_AV, teleops, t, miles=miles) / divi
    elif which_cost == p.cost_calculations[0]:
        return purchase(vtype, is_AV, teleops) / divi
    elif which_cost == p.cost_calculations[1]:
        return maintenance(vtype, is_AV, teleops, t, miles) / divi
    elif which_cost == p.cost_calculations[2]:
        return operation(vtype, is_AV, teleops, t, miles) / divi
    elif which_cost == p.cost_calculations[3]:
        return operator(is_AV, teleops) / divi

def net_pres_val(vtype, is_AV, teleops, t=p.assumptions['Years'], fm=p.assumptions['Fleet size'], miles=p.assumptions['Miles/year']):
    vals = [purchase(vtype, is_AV, teleops)]
    for i in range(t-1):
        flow = maintenance(vtype, 1, miles) + operation(vtype, 1, miles) + operator(is_AV, teleops, 1, fm)
        vals.append(flow)
    return vals

#--RIDERSHIP EVALUATION-------------------------------------------------------#
def vehicle_need(vtype, site):
    dset = p.route_data[site]
    trips_per_day = dset['hours']*dset['trips/hour']
    riders_per_trip = dset['riders/day']/trips_per_day
    num_vehicles = 1
    while num_vehicles*p.vehicle[vtype]['Passengers'] < riders_per_trip:
        num_vehicles+=1
    return num_vehicles

def rider_miles(site):
    dist = p.route_data[site]['distance']
    trp_pr_hr = p.route_data[site]['trips/hour']
    hours = p.route_data[site]['hours']
    return dist*trp_pr_hr*hours*p.DPW*p.WPY

def cost_per_rider(vtype, is_AV, teleops, time=p.assumptions['Years']):
    if is_AV == 'N' or is_AV == 'S':
        cost_per_year = total(vtype, is_AV, teleops, time)/p.assumptions['Years']
        riders_per_year = p.rider_percent_per_trip*p.vehicle[vtype]['Passengers']*p.avg_mph*p.assumptions['Miles/year']/p.miles_per_trip
    elif is_AV =='Y':
        cost_per_year = total(vtype, is_AV, teleops, time)/p.assumptions['Years']
        riders_per_year = p.rider_percent_per_trip*(p.vehicle[vtype]['Passengers']+1)*p.avg_mph*p.assumptions['Miles/year']/p.miles_per_trip 
    return cost_per_year/riders_per_year

def riders_per_mile(vtype, site):
    dset = p.route_data[site]
    trips_per_day = dset['hours']*dset['trips/hour']
    try:
        riders_per_trip = dset['riders/trip']
    except:
        riders_per_trip = dset['riders/day']/trips_per_day
    return riders_per_trip/dset['distance']

def cost_per_rider2(vtype, is_AV, teleops, site, which_cost='total', time=p.assumptions['Years']):
    miles = rider_miles(site)
    return vehicle_need(vtype, site) * cost_per_mile(vtype, is_AV, teleops, which_cost, time, miles=miles)/riders_per_mile(vtype, site)


#--PLOT FORMATTING FUNCTIONS--------------------------------------------------#
'''
def init_plot():
    plt.rcParams['font.family'] = p.font
    global c1, c2, c3, fig
    c1 = p.c1
    c2 = p.c2
    c3 = p.c3
    fig = plt.figure()
    ax = fig.gca()
'''

#--MAIN-----------------------------------------------------------------------#

def main():
    l = ['N','S','Y']
    tele = [True, False]
    for j, item in enumerate(p.vehicle):
        print('==========================================')
        for i in l:
            for k in tele:
                if item == 'ICE' or item == 'HEV' or item == 'BEV':
                    pass
                else:
                    value = net_pres_val(item, i, teleops=k)
                    netpresval = np.npv(0.08, value)
                    print('\nVtype =  {}; Safe_Op = {}; Teleop = {}; NPV = {}\n'.format(item, i, k, netpresval))
        
    
if __name__ == '__main__':
    main()
