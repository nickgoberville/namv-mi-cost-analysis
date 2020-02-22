#! /usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import functions as f
import parameters as p

def bar_plot(func):
    veh_num = len(p.vehicle) - 3

    # Font and color values
    plt.rcParams['font.family'] = 'Times New Roman'
    c1 = p.colors[0]
    c2 = p.colors[1]
    c3 = p.colors[2]
    c4=p.colors[3]
    # Initialize plot
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    #ax.set_xlabel('Time', fontsize=30)
    ax.set_ylabel('Cost per Rider ($/rider)', fontsize=30)
    #ax.set_title('Cost per Mile', fontsize=30)
    #xlabels = ['AV', 'SO', 'FM', 'FA']


    # Setting up bar graph
    barWidth = 0.2
    r1 = np.arange(veh_num)      #Spacing for non AV
    r2 = [x + barWidth for x in r1]     #Spacing for AV w/ SD
    r3 = [x + barWidth for x in r2]     #Spacing for AV w/ FM
    r4 = [x + barWidth for x in r3]     #Spacing for AV w/o operator
    #all = np.append(r1,np.append(r2,np.append(r3,r4)))
    ticks = (np.asarray(r2) + np.asarray(r3)) / 2
    #print(ticks)
    ax.set_xticks(ticks)
    #labels = ['non-AV','AV w/ SO','AV w/ FM', 'Fully AV']
    xlabels = []
    for i, key in enumerate(p.vehicle):
        xlabels.append(key)
    ax.set_xticklabels(xlabels, fontsize=20)
    #ax.set_xticklabels((r1, r2, r3, r4), xlabels)

    for i, key in enumerate(p.evalu):
        for j, item in enumerate(p.vehicle):
            is_AV_val = p.evalu[key]['is_AV']
            teleops_val = p.evalu[key]['teleops']
            p.evalu[key]['vals'].append(func(item, is_AV_val, teleops_val))

    #print(p.evalu['non_AV']['vals'])
    non_AV = tuple(p.evalu['non_AV']['vals'])     # is_AV='N', teleops=False
    AV_SD = tuple(p.evalu['AV_SD']['vals'])      # is_AV='S', teleops=False
    AV_FM = tuple(p.evalu['AV_FM']['vals'])      # is_AV='Y', teleops=True
    AV_full = tuple(p.evalu['AV_full']['vals'])   # is_AV='Y', teleops=False

    #print(non_AV[0:3])
    a = veh_num

    p1 = ax.bar(r1, non_AV[0:a], width=barWidth-.05, color=c1, edgecolor='k', label='Purchase')
    p2 = ax.bar(r2, AV_SD[0:a], width=barWidth-.05, color=c2, edgecolor='k',label='Purchase')
    p3  = ax.bar(r3, AV_FM[0:a], width=barWidth-.05, color=c3, edgecolor='k',label='Purchase')
    p4 = ax.bar(r4, AV_full[0:a], width=barWidth-.05, color=c4, edgecolor='k',label='Purchase')

    legs = ['Non-AV', 'AV w/ Safety Operator', 'AV w/ Fleet Manager', 'Full AV']
    ax.legend((p1[0],p2[0],p3[0],p4[0]), legs, fontsize=30)
    ax.annotate('ICE', xy = (0.1,-0.1), fontsize=20)
    ax.yaxis.grid(linestyle=':', color='k', linewidth=2)
    plt.show()

def main():
    bar_plot(f.cost_per_rider)

if __name__ == '__main__':
    main()