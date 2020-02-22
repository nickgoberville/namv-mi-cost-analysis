#! /usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
import parameters as p
import functions as f
from itertools import chain
fig = plt.figure()
plt.rcParams['font.family'] = p.font
ax1 = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2)
t = np.arange(p.assumptions['Years']+1)
c1 = p.colors[0]
c2 = p.colors[1]
c3 = p.colors[2]
c4 = p.colors[3]
c5 = p.colors[4]
year = 3
lw = 3
#a_1 = np.zeros(len(t), 5)


#for i in range(year):
# Non AV
#ax1.plot(t, f.total('BEV', 'N', False, t), linewidth=lw)
plots = []
def plotax1(fm, year, c1, scale=1000):
    ax1.plot(t[:year+1], (f.total('BEV', 'N', False, t[:year+1]) -f.total('BEV', 'N', False, t[:year+1]))/scale , color=c1, linewidth=lw)
    ax1.plot([year,year+1], [(f.total('BEV', 'N', False, t[year]) -f.total('BEV', 'N', False, t[year]))/scale , (f.total('BEV', 'Y', True, t[year+1], fm=fm) -f.total('BEV', 'N', False, t[year+1])+f.total('BEV', 'N',False,t[year-1]))/scale], color=c1, linewidth=lw)
    plots.append(ax1.plot(t[year+1:], (f.total('BEV', 'Y', True, t[year+1:], fm=fm) -f.total('BEV', 'N', False, t[year+1:])+f.total('BEV', 'N',False,t[year-1]))/scale, color=c1, linewidth=lw))#+ f.total('BEV', 'N', False, year))

def plotax2(fm, year, c1, scale=1000):
    ax2.plot(t[:year+1], (f.total('BEV', 'N', False, t[:year+1]) -f.total('BEV', 'N', False, t[:year+1]))/scale, color=c1, linewidth=lw)
    ax2.plot([year,year+1], [(f.total('BEV', 'N', False, t[year]) - f.total('BEV', 'N', False, t[year]))/scale, (f.total('BEV', 'Y', True, t[year+1], fm=fm)+f.total('BEV', 'N',False,t[year-1]) -f.total('BEV', 'N', False, t[year+1]) )/scale], color=c1, linewidth=lw)
    plots.append(ax2.plot(t[year+1:], (f.total('BEV', 'Y', True, t[year+1:], fm=fm)+f.total('BEV', 'N',False,t[year-1]) -f.total('BEV', 'N', False, t[year+1:]) )/scale, color=c1, linewidth=lw))#+ f.total('BEV', 'N', False, year))

def ax1_npv_calc(fm, year, scale=1000, rate=0.08):
    ax1_vals1 = f.total('BEV', 'N', False, t[:year+1]) -f.total('BEV', 'N', False, t[:year+1])
    ax1_vals2 = [(f.total('BEV', 'N', False, t[year]) -f.total('BEV', 'N', False, t[year]))/scale , (f.total('BEV', 'Y', True, t[year+1], fm=fm) -f.total('BEV', 'N', False, t[year+1])+f.total('BEV', 'N',False,t[year-1]))/scale]
    ax1_vals3 = (f.total('BEV', 'Y', True, t[year+1:], fm=fm) -f.total('BEV', 'N', False, t[year+1:])+f.total('BEV', 'N',False,t[year-1]))/scale
    full_ax1 = list(chain(ax1_vals1, ax1_vals2, ax1_vals3))
    NPV = np.npv(rate, full_ax1)
    print("# FMs = {}; Years = {}; NPV = {}".format(fm, year, NPV))

def ax2_npv_calc(fm, year, scale=1000, rate=0.08):
    ax2_vals1 = (f.total('BEV', 'N', False, t[:year+1]) -f.total('BEV', 'N', False, t[:year+1]))/scale 
    ax2_vals2 = [(f.total('BEV', 'N', False, t[year]) - f.total('BEV', 'N', False, t[year]))/scale, (f.total('BEV', 'Y', True, t[year+1], fm=fm)+f.total('BEV', 'N',False,t[year-1]) -f.total('BEV', 'N', False, t[year+1]) )/scale] 
    ax2_vals3 = (f.total('BEV', 'Y', True, t[year+1:], fm=fm) -f.total('BEV', 'N', False, t[year+1:])+f.total('BEV', 'N',False,t[year-1]))/scale 
    full_ax2 = list(chain(ax2_vals1, ax2_vals2, ax2_vals3))
    NPV = np.npv(rate, full_ax2) 
    print("# FMs = {}; Years = {}; NPV = {}".format(fm, year, NPV)) 

fms = [2, 3, 5, 10]
years = [2, 3, 5, 8]

for i in fms:
    ax1_npv_calc(i, years[1])

for i in years:
    ax2_npv_calc(fms[2], i)
scale = 1000

ax1.plot([0,t[-1]],[0,0], linestyle='--', linewidth=lw, color='k')
ax2.plot([0,t[-1]],[0,0], linestyle='--', linewidth=lw, color='k')
plotax1(2,3, c1)
fm2 = plots[0]

plotax1(3,3, c2)
fm3 = plots[1]

plotax1(5,3, c3)
fm5 = plots[2]

plotax1(10, 3, c4)
fm10 = plots[3]
#FM = 2

ax1.legend((fm2[0], fm3[0], fm5[0], fm10[0]), ['Fleet Size: 2', 'Fleet Size: 3', 'Fleet Size: 5','Fleet Size: 10'], fontsize=15)
ax1.grid()

#Subplot 2
#l1 = ax2.plot(t, (f.total('BEV', 'N', False, t))/scale, linewidth=lw)

#year = 2
fm=5
year=2

plots = []
plotax2(5, 2, c1)
y2 = plots[0]

plotax2(5, 3, c2)
y3 = plots[1]

plotax2(5, 5, c3)
y5 = plots[2]

plotax2(5,8,c4)
y8 = plots[3]

ax2.legend((y2[0], y3[0], y5[0], y8[0]), ['2 years', '3 years', '5 years','8 years'], fontsize=15)
#ax2.legend()
ax2.grid()
ax1.ticklabel_format(style='sci', axis='both')
ax1.set_ylabel('Total Cost (thousands of $)', fontsize=20)
ax2.set_ylabel('Total Cost (thousands of $)', fontsize=20)
ax2.set_xlabel('Time (years)', fontsize=25)
#ax1.set_yticklabels(np.arange(-600, 200, 100), fontsize=20)
ax2.set_yticklabels(np.arange(-600, 200, 100), fontsize=20)
plt.xlabel('Time (years)', fontsize=25)
plt.show()