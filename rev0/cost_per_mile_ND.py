#! /usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
from functions import ops, maint, purchase, driver_cost
from parameters import *

# Font & color values
plt.rcParams['font.family'] = p.font
c1 = p.c1
c2 = p.c2
c3 = p.c3

# Initiating plot with grid
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.set
plt.grid(axis='x', linestyle=':', linewidth=1)

# Calculating operation, maintenance, & purchase costs into lists
op_vals = []
for drive_val in D_val:
    for vehicle in V_type:
        op_vals.append(ops(vtype=vehicle)/(miles_per_year*years))

maint_vals = []
for drive_val in D_val:
    for vehicle in V_type:
        maint_vals.append(maint(vtype=vehicle)/(miles_per_year*years))

purch_vals = []
for drive_val in D_val:
    for vehicle in V_type:
        purch_vals.append(purchase(vtype=vehicle, drvr=drive_val)/(miles_per_year*years))

# Splitting lists into D, SD, and ND
D_operation = tuple(op_vals[0:3])
D_maintenance = tuple(maint_vals[0:3])
D_purchase = tuple(purch_vals[0:3])

SD_operation = tuple(op_vals[3:6])
SD_maintenance = tuple(maint_vals[3:6])
SD_purchase = tuple(purch_vals[3:6])

ND_operation = tuple(op_vals[6:9])
ND_maintenance = tuple(maint_vals[6:9])
ND_purchase = tuple(purch_vals[6:9])

# Bar graph spacing
N = 3
ind1 = np.arange(N) - 0.15   # the x locations for the groups
ind2 = np.arange(N)
ind3 = np.arange(N) + 0.15
h = 0.2      # the width of the bars: can also be len(x) sequence

# ND Plots
p1 = plt.barh(ind1, ND_purchase, height=h, edgecolor='k', color=c1)     # Operations
p2 = plt.barh(ind1, ND_maintenance, height=h,
             left=ND_purchase, edgecolor='k', color=c2)                     # Purchase
p3 = plt.barh(ind1, ND_operation, height=h,
             left=tuple(map(sum,zip(ND_purchase, ND_maintenance))), 
             edgecolor='k', color=c3)

# D Plots
p7 = plt.barh(ind3, D_purchase, height=h, edgecolor='k', color=c1)      # Operations
p8 = plt.barh(ind3, D_maintenance, height=h,
             left=D_purchase, edgecolor='k', color=c2)                     # Purchase
p9 = plt.barh(ind3, D_operation, height=h,
             left=tuple(map(sum,zip(D_maintenance, D_purchase))), 
             edgecolor='k', color=c3)
          
# Text annotations
plt.annotate('  Not Autonomous', xy=(0.5, 0.15), xytext=(0.8, 0.13),
            arrowprops=dict(facecolor='grey'), fontsize=25)
#plt.annotate('  Safety Driver', xy=(0.6, 0), xytext=(0.8, -0.02),
#            arrowprops=dict(facecolor='grey'), fontsize=25)
plt.annotate('  Autonomous', xy=(0.6, -0.15), xytext=(0.8, -0.18),
            arrowprops=dict(facecolor='grey'), fontsize=25)
# Plot labelling
plt.xlabel('Cost per mile ($/mile)', fontsize=30)
plt.title('Purchase, Maintenance, and Operation Costs (without driver cost)', fontsize=35)
plt.yticks(ind2, ('ICE', 'HEV', 'EV'), fontsize=30)
plt.xticks(np.arange(0, 1.3, 0.1), fontsize=20)
plt.legend((p1[0], p2[0], p3[0]), ('Purchase', 'Maintenance', 'Operation'), fontsize=25)

plt.show()