#! /usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
from functions import ops, maint, purchase, total
from parameters import *
plt.rcParams['font.family'] = font
f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
t = np.arange(0,9,1)
plt1 = ax1
plt2 = ax2
lw = 3
for i in range(0,3):
    plt1.plot(t, total(V_type[i], D_val[0], t)/1000, color=colors[i], label=V_type[i], linewidth=lw)
plt1.set_title('Not Autonomous', fontsize=30)
plt1.tick_params(labelsize=25)
plt1.set_xticks(range(0,9,2))

ttc = 4

for i in range(0,3):
    plt2.plot(t[0:ttc], total(V_type[i], D_val[1], t[0:ttc])/1000, color=colors[i], label=V_type[i], linewidth=lw)
    plt2.plot([ttc-1,ttc], [total(V_type[i], D_val[1], t[ttc-1])/1000, total(V_type[i], D_val[2], t[ttc], reduction=1)/1000 + total(V_type[i], D_val[1], t[ttc-1])/1000], color=colors[i], label=V_type[i], linestyle='dashdot', linewidth=lw)
    plt2.plot(t[ttc:], total(V_type[i], D_val[2], t[ttc:], reduction=1)/1000 + total(V_type[i], D_val[1], t[ttc-1])/1000, color=colors[i], label=V_type[i], linestyle='dashdot', linewidth=lw)
plt2.set_title('Realistic Autonomous Scenario', fontsize=30)
plt2.plot([ttc-1, ttc-1], [0, 500000/1000], color='k', linestyle='dashed', linewidth=3)
plt2.text(0.5, 50000/1000, 'Safety Driver', fontsize=20)
plt2.text(4, 50000/1000, 'Remote Fleet Manager', fontsize=20)
plt2.tick_params(labelsize=25)
plt2.set_xticks(range(0,9,2))
x = [0, 0]
y1 = [0, total(V_type[2], D_val[0], 0)/1000]
y2 = [0, total(V_type[2], D_val[2], 0)/1000]
plt1.plot(x, y1, color=colors[2], linewidth=lw)
plt2.plot(x, y2, color=colors[2], linewidth=lw)

plt1.grid(linestyle=':')
plt2.grid(linestyle=':')
plt2.grid(linestyle=':')
plt1.legend(fontsize=25)
plt.yticks(np.arange(0, 501, 100), fontsize=30)

plt1.set_xlabel('Time (years)', fontsize=25)
plt2.set_xlabel('Time (years)', fontsize=25)
plt1.set_ylabel('Total Cost ($ in thousands)', fontsize=25)
plt.show()

# ==================================================================

f, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
t = np.arange(0,16,1)
plt1 = ax1
plt2 = ax2
redu = 0.1

for i in range(0,3):
    plt1.plot(t, total(V_type[i], D_val[2], t)/1000, color=colors[i], label=V_type[i], linewidth=lw)
plt1.set_title('Fully Autonomous (Current Prices)', fontsize=25)
plt.yticks(fontsize=20)
plt1.set_ylabel('Total Cost ($ in thousands)', fontsize=25)
plt1.tick_params(labelsize=20)


for i in range(0,2):
    plt2.plot(t, total(V_type[i], D_val[2], t)/1000, color=colors[i], label=V_type[i], linewidth=lw)
plt2.plot(t, total(V_type[2], D_val[2], t, reduction=redu)/1000, color=colors[2], label=V_type[2], linewidth=lw)
plt2.set_title('Fully Autonomous (10% Reduction in EV Price)', fontsize=25)

x = [0, 0]
y1 = [0, total(V_type[2], D_val[2], 0)/1000]
y2 = [0, total(V_type[2], D_val[2], 0, reduction=redu)/1000]
plt1.plot(x, y1, color=colors[2], linewidth=lw)
plt2.plot(x, y2, color=colors[2], linewidth=lw)

plt1.grid(linestyle=':')
plt2.grid(linestyle=':')

plt.xlabel('Time (years)', fontsize=25)
plt.xticks(fontsize=20)
plt.ylabel('Total Cost ($ in thousands)', fontsize=25)
plt.yticks(np.arange(0,81,20), fontsize=20)
plt.legend(fontsize=25)
plt.show()