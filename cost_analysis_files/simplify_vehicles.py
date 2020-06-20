import pandas as pd
import numpy as np
import math

vehicles_full = pd.read_csv('vehicles_full.csv')
EV_dict = {'vehicle': ['Small', 'Medium', 'Large', 'X-Large'],
             'drive_train': ['EV', 'EV', 'EV', 'EV'],
             'category': ['S', 'M', 'L', 'XL'],
             'purchase': [],
             'operation': [],
             'maintenance': [],
             'passengers': []}

ICE_dict = {'vehicle': ['Small', 'Medium', 'Large', 'X-Large'],
             'drive_train': ['ICE', 'ICE', 'ICE', 'ICE'],
             'category': ['S', 'M', 'L', 'XL'],
             'purchase': [],
             'operation': [],
             'maintenance': [],
             'passengers': []}

EV_indexes = []
ICE_indexes = []
for index in vehicles_full.index:
    if vehicles_full.drive_train[index] == 'EV':
        EV_indexes.append(index)
    else:
        ICE_indexes.append(index)
count = 0

for drive in [EV_indexes, ICE_indexes]:
    S_purch = []
    M_purch = []
    L_purch = []
    XL_purch = []
    S_maint = []
    M_maint = []
    L_maint = []
    XL_maint = []
    S_op = []
    M_op = []
    L_op = []
    XL_op = []
    S_pass = []
    M_pass = []
    L_pass = []
    XL_pass = []
    for index in drive:
        vehicle = vehicles_full.loc[index]
        print(vehicle.category)
        if vehicle.category == 'S':
            S_purch.append(vehicle.purchase)
            S_maint.append(vehicle.maintenance)
            S_op.append(vehicle.operation)
            S_pass.append(vehicle.passengers)
        elif vehicle.category == 'M':
            M_purch.append(vehicle.purchase)
            M_maint.append(vehicle.maintenance)
            M_op.append(vehicle.operation)
            M_pass.append(vehicle.passengers)
        elif vehicle.category == 'L':
            L_purch.append(vehicle.purchase)
            L_maint.append(vehicle.maintenance)
            L_op.append(vehicle.operation)
            L_pass.append(vehicle.passengers)
        elif vehicle.category == 'XL':
            XL_purch.append(vehicle.purchase)
            XL_maint.append(vehicle.maintenance)
            XL_op.append(vehicle.operation)
            XL_pass.append(vehicle.passengers)
    #print(S_pass)
    if count == 0: # EV
        EV_dict['purchase'].append(np.average(np.array(S_purch)))
        EV_dict['purchase'].append(np.average(np.array(M_purch)))
        EV_dict['purchase'].append(np.average(np.array(L_purch)))   
        EV_dict['purchase'].append(np.average(np.array(XL_purch)))
        EV_dict['maintenance'].append(np.average(np.array(S_maint)))
        EV_dict['maintenance'].append(np.average(np.array(M_maint)))
        EV_dict['maintenance'].append(np.average(np.array(L_maint)))   
        EV_dict['maintenance'].append(np.average(np.array(XL_maint)))
        EV_dict['operation'].append(np.average(np.array(S_op)))
        EV_dict['operation'].append(np.average(np.array(M_op)))
        EV_dict['operation'].append(np.average(np.array(L_op)))   
        EV_dict['operation'].append(np.average(np.array(XL_op)))
        EV_dict['passengers'].append(math.ceil(np.average(np.array(S_pass))))
        EV_dict['passengers'].append(math.ceil(np.average(np.array(M_pass))))
        EV_dict['passengers'].append(math.ceil(np.average(np.array(L_pass))))   
        EV_dict['passengers'].append(math.ceil(np.average(np.array(XL_pass))))
    else:
        ICE_dict['purchase'].append(np.average(np.array(S_purch)))
        ICE_dict['purchase'].append(np.average(np.array(M_purch)))
        ICE_dict['purchase'].append(np.average(np.array(L_purch)))   
        ICE_dict['purchase'].append(np.average(np.array(XL_purch)))
        ICE_dict['maintenance'].append(np.average(np.array(S_maint)))
        ICE_dict['maintenance'].append(np.average(np.array(M_maint)))
        ICE_dict['maintenance'].append(np.average(np.array(L_maint)))   
        ICE_dict['maintenance'].append(np.average(np.array(XL_maint)))
        ICE_dict['operation'].append(np.average(np.array(S_op)))
        ICE_dict['operation'].append(np.average(np.array(M_op)))
        ICE_dict['operation'].append(np.average(np.array(L_op)))   
        ICE_dict['operation'].append(np.average(np.array(XL_op)))
        ICE_dict['passengers'].append(math.ceil(np.average(np.array(S_pass))))
        ICE_dict['passengers'].append(math.ceil(np.average(np.array(M_pass))))
        ICE_dict['passengers'].append(math.ceil(np.average(np.array(L_pass))))   
        ICE_dict['passengers'].append(math.ceil(np.average(np.array(XL_pass))))
    count+=1

EV_df = pd.DataFrame(EV_dict, columns=EV_dict.keys())
EV_df.to_csv('vehicles_EV.csv')

ICE_df = pd.DataFrame(ICE_dict, columns=ICE_dict.keys())
ICE_df.to_csv('vehicles_ICE.csv')