#! /usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import functions as f
import parameters as p

iters = len(p.vehicle)

# Font and color values
plt.rcParams['font.family'] = 'Times New Roman'
c1 = p.colors[0]
c2 = p.colors[1]
c3 = p.colors[2]
c4 = p.colors[3]

# Initialize plot
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.set_xlabel('Time')
ax.set_ylabel('Cost')
ax.set_title('Cost per Mile')
xlabels = ['AV', 'SO', 'FM', 'FA']


# Setting up bar graph
barWidth = 0.2
r1 = np.arange(len(p.vehicle))      #Spacing for non AV
r2 = [x + barWidth for x in r1]     #Spacing for AV w/ SD
r3 = [x + barWidth for x in r2]     #Spacing for AV w/ FM
r4 = [x + barWidth for x in r3]     #Spacing for AV w/o operator
all = np.append(r1,np.append(r2,np.append(r3,r4)))
ax.set_xticks(all)
xlabels = ['non-AV','non-AV','non-AV', 'AV w/ SO','AV w/ SO','AV w/ SO', 'AV w/ FM','AV w/ FM','AV w/ FM', 'Fully AV', 'Fully AV', 'Fully AV']
ax.set_xticklabels(xlabels)
#ax.set_xticklabels((r1, r2, r3, r4), xlabels)
for k in p.cost_calculations:
    for i, key in enumerate(p.evalu):
        for j, item in enumerate(p.vehicle):
        #for k in p.cost_calculations:
            is_AV_val = p.evalu[key]['is_AV']
            teleops_val = p.evalu[key]['teleops']
            #vals_list = p.evalu[key]['vals']
            p.evalu[key]['vals'].append(f.cost_per_mile(item, is_AV_val, teleops_val, which_cost=k))

print(p.evalu['non_AV']['vals'])
non_AV = tuple(p.evalu['non_AV']['vals'])     # is_AV='N', teleops=False
AV_SD = tuple(p.evalu['AV_SD']['vals'])      # is_AV='S', teleops=False
AV_FM = tuple(p.evalu['AV_FM']['vals'])      # is_AV='Y', teleops=True
AV_full = tuple(p.evalu['AV_full']['vals'])   # is_AV='Y', teleops=False

print(non_AV[0:3])

p1 = ax.bar(r1, non_AV[0:3], width=barWidth-.05, color=c1, label='Purchase')
p2 = ax.bar(r1, non_AV[3:6], width=barWidth-.05, color=c2, label='Maintenance', bottom=non_AV[0:3])
p3 = ax.bar(r1, non_AV[6:9], width=barWidth-.05, color=c3, label='Operation', bottom=tuple(map(sum,zip(non_AV[0:3], non_AV[3:6]))))
p4 = ax.bar(r1, non_AV[9:12], width=barWidth-.05, color=c4, label='Operator', bottom=tuple(map(sum,zip(non_AV[0:3], non_AV[3:6]), non_AV[6:9])))

p5 = ax.bar(r2, AV_SD[0:3], width=barWidth-.05, color=c1, label='Purchase')
p6 = ax.bar(r2, AV_SD[3:6], width=barWidth-.05, color=c2, label='Maintenance', bottom=AV_SD[0:3])
p7 = ax.bar(r2, AV_SD[6:9], width=barWidth-.05, color=c3, label='Operation', bottom=tuple(map(sum,zip(AV_SD[0:3], AV_SD[3:6]))))
p8 = ax.bar(r2, AV_SD[9:12], width=barWidth-.05, color=c4, label='Operator', bottom=tuple(map(sum,zip(AV_SD[0:3], AV_SD[3:6]), AV_SD[6:9])))

p9  = ax.bar(r3, AV_FM[0:3], width=barWidth-.05, color=c1, label='Purchase')
p10 = ax.bar(r3, AV_FM[3:6], width=barWidth-.05, color=c2, label='Maintenance', bottom=AV_FM[0:3])
p11 = ax.bar(r3, AV_FM[6:9], width=barWidth-.05, color=c3, label='Operation', bottom=tuple(map(sum,zip(AV_FM[0:3], AV_FM[3:6]))))
p12 = ax.bar(r3, AV_FM[9:12], width=barWidth-.05, color=c4, label='Operator', bottom=tuple(map(sum,zip(AV_FM[0:3], AV_FM[3:6]), AV_FM[6:9])))

p13 = ax.bar(r4, AV_full[0:3], width=barWidth-.05, color=c1, label='Purchase')
p14 = ax.bar(r4, AV_full[3:6], width=barWidth-.05, color=c2, label='Maintenance', bottom=AV_full[0:3])
p15 = ax.bar(r4, AV_full[6:9], width=barWidth-.05, color=c3, label='Operation', bottom=tuple(map(sum,zip(AV_full[0:3], AV_full[3:6]))))
p16 = ax.bar(r4, AV_full[9:12], width=barWidth-.05, color=c4, label='Operator', bottom=tuple(map(sum,zip(AV_full[0:3], AV_full[3:6]), AV_full[6:9])))
ax.legend((p1[0],p2[0],p3[0],p4[0]), p.cost_calculations)
plt.show()