#! /usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import functions as f
import parameters as p

veh_num = len(p.vehicle) - 3

# Font and color values
plt.rcParams['font.family'] = p.font
c1 = p.colors[0]
c2 = p.colors[1]
c3 = p.colors[2]
c4=p.colors[3]
# Initialize plot
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
#ax.set_xlabel('Time', fontsize=30)
ax.set_ylabel('Cost per mile ($/mile)', fontsize=30)
#ax.set_title('Cost per mile', fontsize=30)
#xlabels = ['AV', 'SO', 'FM', 'FA']
ax.set_yticklabels(np.arange(0, 7, 1), fontsize=20)

# Setting up bar graph
barWidth = 0.2
r1 = np.arange(veh_num)      #Spacing for non AV
r2 = [x + barWidth for x in r1]     #Spacing for AV w/ SD
r3 = [x + barWidth for x in r2]     #Spacing for AV w/ FM
r4 = [x + barWidth for x in r3]     #Spacing for AV w/o operator
all = np.append(r1,np.append(r2,np.append(r3,r4)))
ax.set_xticks(all)
labels = ['non-AV','AV w/ Safety Operator','AV w/ Fleet Manager', 'Fully AV']

ticks = (np.asarray(r2) + np.asarray(r3)) / 2
ax.set_xticks(ticks)
xlabels = []
for i, key in enumerate(p.vehicle):
    xlabels.append(key)
ax.set_xticklabels(xlabels, fontsize=20)

# MAIN DATA BLOCK 
for k in p.cost_calculations:
    for i, key in enumerate(p.evalu):
        for j, item in enumerate(p.vehicle):
            if item == 'ICE' or item == 'HEV' or item == 'BEV':
                pass
            else:
                is_AV_val = p.evalu[key]['is_AV']
                teleops_val = p.evalu[key]['teleops']
                p.evalu[key]['vals'].append(f.cost_per_mile(item, is_AV_val, teleops_val, which_cost=k))

# Data manipulation for plotting
non_AV = tuple(p.evalu['non_AV']['vals'])     # is_AV='N', teleops=False
AV_SD = tuple(p.evalu['AV_SD']['vals'])      # is_AV='S', teleops=False
AV_FM = tuple(p.evalu['AV_FM']['vals'])      # is_AV='Y', teleops=True
AV_full = tuple(p.evalu['AV_full']['vals'])   # is_AV='Y', teleops=False

a = veh_num
b = 2*veh_num
c = 3*veh_num
d = 4*veh_num

p1 = ax.bar(r1, non_AV[0:a], width=barWidth-.05, color=c1, edgecolor='k', label='Purchase')
p2 = ax.bar(r1, non_AV[a:b], width=barWidth-.05, color=c2, edgecolor='k',label='Maintenance', bottom=non_AV[0:a])
p3 = ax.bar(r1, non_AV[b:c], width=barWidth-.05, color=c3, edgecolor='k',label='Fuel', bottom=tuple(map(sum,zip(non_AV[0:a], non_AV[a:b]))))
p4 = ax.bar(r1, non_AV[c:d], width=barWidth-.05, color=c4, edgecolor='k',label='Operator', bottom=tuple(map(sum,zip(non_AV[0:a], non_AV[a:b]), non_AV[b:c])))

p5 = ax.bar(r2, AV_SD[0:a], width=barWidth-.05, color=c1, edgecolor='k',label='Purchase')
p6 = ax.bar(r2, AV_SD[a:b], width=barWidth-.05, color=c2, edgecolor='k',label='Maintenance', bottom=AV_SD[0:a])
p7 = ax.bar(r2, AV_SD[b:c], width=barWidth-.05, color=c3, edgecolor='k',label='Operation', bottom=tuple(map(sum,zip(AV_SD[0:a], AV_SD[a:b]))))
p8 = ax.bar(r2, AV_SD[c:d], width=barWidth-.05, color=c4, edgecolor='k',label='Operator', bottom=tuple(map(sum,zip(AV_SD[0:a], AV_SD[a:b]), AV_SD[b:c])))

p9  = ax.bar(r3, AV_FM[0:a], width=barWidth-.05, color=c1, edgecolor='k',label='Purchase')
p10 = ax.bar(r3, AV_FM[a:b], width=barWidth-.05, color=c2, edgecolor='k',label='Maintenance', bottom=AV_FM[0:a])
p11 = ax.bar(r3, AV_FM[b:c], width=barWidth-.05, color=c3, edgecolor='k',label='Operation', bottom=tuple(map(sum,zip(AV_FM[0:a], AV_FM[a:b]))))
p12 = ax.bar(r3, AV_FM[c:d], width=barWidth-.05, color=c4, edgecolor='k',label='Operator', bottom=tuple(map(sum,zip(AV_FM[0:a], AV_FM[a:b]), AV_FM[b:c])))

p13 = ax.bar(r4, AV_full[0:a], width=barWidth-.05, color=c1, edgecolor='k',label='Purchase')
p14 = ax.bar(r4, AV_full[a:b], width=barWidth-.05, color=c2, edgecolor='k',label='Maintenance', bottom=AV_full[0:a])
p15 = ax.bar(r4, AV_full[b:c], width=barWidth-.05, color=c3, edgecolor='k',label='Operation', bottom=tuple(map(sum,zip(AV_full[0:a], AV_full[a:b]))))
p16 = ax.bar(r4, AV_full[c:d], width=barWidth-.05, color=c4, edgecolor='k',label='Operator', bottom=tuple(map(sum,zip(AV_full[0:a], AV_full[a:b]), AV_full[b:c])))
legs = [p.cost_calculations[0], p.cost_calculations[1], p.cost_calculations[2], p.cost_calculations[3]]
ax.legend((p1[0],p2[0],p3[0],p4[0]), legs, fontsize=20)
ax.annotate('ICE', xy = (0.1,-0.1), fontsize=20)
ax.yaxis.grid(linestyle=':', color='k', linewidth=2)
plt.show()