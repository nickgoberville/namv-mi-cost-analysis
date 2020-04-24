#! /usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
from functions import ops, maint, purchase, driver_cost
from parameters import *

plt.rcParams['font.family'] = font
# fontname=font,

EV_1 = (ops(vtype='EV') + maint(vtype='EV') + 
        driver_cost(vtype='EV', drvr='SD') + av_shuttle_costs[0]) / years / (passenger_size[0]*15000)
EV_2 = (ops(vtype='EV') + maint(vtype='EV') + 
        driver_cost(vtype='EV', drvr='SD') + av_shuttle_costs[1]) / years / (passenger_size[1]*15000)
EV_3 = (ops(vtype='EV') + maint(vtype='EV') + 
        driver_cost(vtype='EV', drvr='SD') + av_shuttle_costs[2]) / years / (passenger_size[2]*15000)
EV_4 = (ops(vtype='EV') + maint(vtype='EV') + 
        driver_cost(vtype='EV', drvr='SD') + av_shuttle_costs[3]) / years / (passenger_size[3]*15000)
EV_5 = (ops(vtype='EV') + maint(vtype='EV') + 
        driver_cost(vtype='EV', drvr='ND') + av_shuttle_costs[0]) / years / (passenger_size[0]*15000)
EV_6 = (ops(vtype='EV') + maint(vtype='EV') + 
        driver_cost(vtype='EV', drvr='ND') + av_shuttle_costs[1]) / years / (passenger_size[1]*15000)
EV_7 = (ops(vtype='EV') + maint(vtype='EV') + 
        driver_cost(vtype='EV', drvr='ND') + av_shuttle_costs[2]) / years / (passenger_size[2]*15000)
EV_8 = (ops(vtype='EV') + maint(vtype='EV') + 
        driver_cost(vtype='EV', drvr='ND') + av_shuttle_costs[3]) / years / (passenger_size[3]*15000)

vals_1 = tuple([EV_1, EV_2, EV_3, EV_4])
vals_2 = tuple([EV_5, EV_6, EV_7, EV_8])

N = 4
ind1 = np.arange(0.1, 4.1,1)
ind2 = np.arange(0.2, 4.2,1)
w = 0.1       # the width of the bars: can also be len(x) sequence

# ND Plots
p1 = plt.barh(ind1, vals_1, height=w, edgecolor='k', color='r', label='Safety Driver')
p2 = plt.barh(ind2, vals_2, height=w, edgecolor='k', color='b', label='No Driver')
plt.yticks(np.arange(0.15, 4.15, 1), ('3-person', '6-person', '12-person', '15-person'), fontsize=30)
plt.xticks(fontsize=25)
plt.xlabel('Cost ($/rider)', fontsize=30)
plt.ylabel('Shuttle Size', fontsize=30)
plt.title('Ridership Evaluation', fontsize=35)
plt.legend(fontsize=25)
plt.grid(axis='y', linestyle=':', linewidth=1)
plt.show()