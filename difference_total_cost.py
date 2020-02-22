#! /usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
import parameters as p
import functions as f

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

scale = 1000

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
ax1.set_ylabel('Total Cost ($)', fontsize=25)
ax2.set_ylabel('Total Cost ($)', fontsize=25)
ax2.set_xlabel('Time (years)', fontsize=25)

plt.xlabel('Time (years)', fontsize=25)
plt.show()