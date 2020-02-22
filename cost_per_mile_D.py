#! /usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
from functions import ops, maint, purchase, driver_cost
from parameters import *
import matplotlib.font_manager as fm
fm._rebuild()
# Font & color values
plt.rcParams['font.family'] = font
c1 = (77/255, 148/255, 255/255)
c2 = (255/255, 51/255, 51/255)
c3 = (102/255, 153/255, 0/255)
c4 = (196/255, 77/255, 255/255)

# Initiating plot with grid
plt.figure()
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

driver_vals = []
for drive_val in D_val:
    for vehicle in V_type:
        driver_vals.append(driver_cost(vtype=vehicle, drvr=drive_val)/(miles_per_year*years))

# Splitting lists into D, SD, and ND
D_operation = tuple(op_vals[0:3])
D_maintenance = tuple(maint_vals[0:3])
D_purchase = tuple(purch_vals[0:3])
D_driver = tuple(driver_vals[0:3])

SD_operation = tuple(op_vals[3:6])
SD_maintenance = tuple(maint_vals[3:6])
SD_purchase = tuple(purch_vals[3:6])
SD_driver = tuple(driver_vals[3:6])

ND_operation = tuple(op_vals[6:9])
ND_maintenance = tuple(maint_vals[6:9])
ND_purchase = tuple(purch_vals[6:9])
ND_driver = tuple(driver_vals[6:9])
print(SD_driver)
print(ND_driver)

# Bar graph spacing
N = 3
ind1 = np.arange(N) - 0.15   # the x locations for the groups
ind2 = np.arange(N)
ind3 = np.arange(N) + 0.15
h = 0.1       # the width of the bars: can also be len(x) sequence

# ND Plots
p1 = plt.barh(ind1, ND_purchase, height=h, edgecolor='k', color=c1)     # Operations
p2 = plt.barh(ind1, ND_maintenance, height=h,
             left=ND_purchase, edgecolor='k', color=c2)                     # Purchase
p3 = plt.barh(ind1, ND_operation, height=h,
             left=tuple(map(sum,zip(ND_purchase, ND_maintenance))), 
             edgecolor='k', color=c3)
p4 = plt.barh(ind1, ND_driver, height=h,
             left=tuple(map(sum, zip(ND_maintenance, ND_purchase, ND_operation))), 
             edgecolor='k', color=c4)

# SD Plots
p5 = plt.barh(ind2, SD_purchase, height=h, edgecolor='k', color=c1)      # Operations
p6 = plt.barh(ind2, SD_maintenance, height=h,
             left=SD_purchase, edgecolor='k', color=c2)                     # Purchase
p7 = plt.barh(ind2, SD_operation, height=h,
             left=tuple(map(sum,zip(SD_maintenance, SD_purchase))), 
             edgecolor='k', color=c3)
p8 = plt.barh(ind2, SD_driver, height=h,
             left=tuple(map(sum, zip(SD_maintenance, SD_purchase, SD_operation))), 
             edgecolor='k', color=c4)

# D Plots
p9 = plt.barh(ind3, D_purchase, height=h, edgecolor='k', color=c1)      # Operations
p10 = plt.barh(ind3, D_maintenance, height=h,
             left=D_purchase, edgecolor='k', color=c2)                     # Purchase
p11 = plt.barh(ind3, D_operation, height=h,
             left=tuple(map(sum,zip(D_maintenance, D_purchase))), 
             edgecolor='k', color=c3)
p12 = plt.barh(ind3, D_driver, height=h,
             left=tuple(map(sum, zip(D_maintenance, D_purchase, D_operation))), 
             edgecolor='k', color=c4)
          
# Text annotations
plt.annotate('  Not Autonomous', xy=(6.2, 0.15), xytext=(7.2, 0.13),
            arrowprops=dict(facecolor='grey'), fontsize=25)
plt.annotate('  Autonomous w/ Safety Driver', xy=(6.8, 0), xytext=(7.2, -0.02),
            arrowprops=dict(facecolor='grey'), fontsize=25)
plt.annotate('  Autonomous w/o Safety Driver', xy=(0.8, -0.15), xytext=(7.2, -0.18),
            arrowprops=dict(facecolor='grey'), fontsize=25)

# Plot labelling
plt.xlabel('Cost per mile ($/mile)', fontsize=30)
plt.title('Purchase, Maintenance, and Operation Costs (with driver cost)', fontsize=35)
plt.yticks(ind2, ('ICE', 'HEV', 'EV'), fontsize=30)
plt.xticks(np.arange(0, 12, 1), fontsize=25)
plt.legend((p1[0], p2[0], p3[0], p4[0]), ('Purchase', 'Maintenance', 'Operation', 'Driver'), fontsize=25)

plt.show()