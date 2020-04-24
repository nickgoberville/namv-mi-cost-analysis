#! /usr/bin/env python3
import parameters as p

def ops(vtype, t=p.assumptions['Years'], miles=p.assumptions['Miles/year']):
    return (p.vehicle[vtype]['Operation']*miles) * t

def maint(vtype, t=p.assumptions['Years'], miles=p.assumptions['Miles/year']):
    return (p.vehicle[vtype]['Maintenance'] * miles) * t

def purchase(vtype, is_AV, teleops):
    '''
    Total purchase costs after t years calculation.
    drvr options: 'D' = Driver
                   'SD' = Safety Driver
                   'ND' = NO Driver
    vtype options: 'ICE' = Internal Combustion
                  'HEV' = Hybrid Electric
                  'EV' = Electric
    '''
    purchase_val = p.vehicle[vtype]['Purchase']
    if is_AV == 'N':
        pass
    elif is_AV == 'S' or is_AV == 'Y':
        purchase_val += p.assumptions['Autonomous kit']
    elif is_AV == 'Y' and teleops:
        purchase_val += p.assumptions['Autonomous kit'] + p.assumptions['telops']
    return purchase_val

def driver_cost(vtype, drvr, t=p.assumptions['Years'], miles=p.assumptions['Miles/year']):
    '''
    Total operation costs after t years calculation.
    drvr options: 
                   'D' = Driver
                   'SD' = Safety Driver
                   'ND' = NO Driver
    vtype options: 
                  'ICE' = Internal Combustion
                  'HEV' = Hybrid Electric
                  'EV' = Electric
    '''
    if drvr is 'D':
        driver_sal = Driver
    elif drvr == 'SD':
        driver_sal = Safety_Driver
    elif drvr == 'ND':
        driver_sal = No_Driver
    return driver_sal * t

def total(vtype, drvr, t=years, miles=miles_per_year, reduction=0):
    '''
    Calculate Total cost
    '''
    if reduction != 0:
        return purchase(vtype, drvr)*(1-reduction) + maint(vtype, t, miles) + ops(vtype, t, miles) + driver_cost(vtype, drvr, t, miles)
    else:
        return purchase(vtype, drvr) + maint(vtype, t, miles) + ops(vtype, t, miles) + driver_cost(vtype, drvr, t, miles)