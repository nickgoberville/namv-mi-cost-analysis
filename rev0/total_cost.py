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
ax1.plot(t, f.total('BEV', 'N', False, t), linewidth=lw)

#FM = 2
fm=2
ax1.plot(t[:year+1], f.total('BEV', 'N', False, t[:year+1]), color=c1, linewidth=lw)
ax1.plot([year,year+1], [f.total('BEV', 'N', False, t[year]), f.total('BEV', 'Y', True, t[year+1], fm=fm)+f.total('BEV', 'N',False,t[year-1])], color=c1, linewidth=lw)
fm2 = ax1.plot(t[year+1:], f.total('BEV', 'Y', True, t[year+1:], fm=fm)+f.total('BEV', 'N',False,t[year-1]), color=c1, linewidth=lw)#+ f.total('BEV', 'N', False, year))

#FM=3
fm=3
ax1.plot(t[:year+1], f.total('BEV', 'N', False, t[:year+1]), color=c3, linewidth=lw)
ax1.plot([year,year+1], [f.total('BEV', 'N', False, t[year]), f.total('BEV', 'Y', True, t[year+1], fm=fm)+f.total('BEV', 'N',False,t[year-1])], color=c2, linewidth=lw)
fm3 = ax1.plot(t[year+1:], f.total('BEV', 'Y', True, t[year+1:], fm=fm)+f.total('BEV', 'N',False,t[year-1]), color=c2, linewidth=lw)#+ f.total('BEV', 'N', False, year))
#

#FM = 5
fm = 5
ax1.plot(t[:year+1], f.total('BEV', 'N', False, t[:year+1]), color=c3, linewidth=lw)
ax1.plot([year,year+1], [f.total('BEV', 'N', False, t[year]), f.total('BEV', 'Y', True, t[year+1], fm=fm)+f.total('BEV', 'N',False,t[year-1])], color=c3, linewidth=lw)
fm5 = ax1.plot(t[year+1:], f.total('BEV', 'Y', True, t[year+1:], fm=fm)+f.total('BEV', 'N',False,t[year-1]), color=c3, linewidth=lw)#+ f.total('BEV', 'N', False, year))
#ax1.plot([year+1,t[-1]], f.total)

#FM=10
fm=10
ax1.plot(t[:year+1], f.total('BEV', 'N', False, t[:year+1]), color=c4, linewidth=lw)
ax1.plot([year,year+1], [f.total('BEV', 'N', False, t[year]), f.total('BEV', 'Y', True, t[year+1], fm=fm)+f.total('BEV', 'N',False,t[year-1])], color=c4, linewidth=lw)
fm10 = ax1.plot(t[year+1:], f.total('BEV', 'Y', True, t[year+1:], fm=fm)+f.total('BEV', 'N',False,t[year-1]), color=c4, linewidth=lw)#+ f.total('BEV', 'N', False, year))

ax1.legend((fm2[0], fm3[0], fm5[0], fm10[0]), ['Fleet Size: 2', 'Fleet Size: 3', 'Fleet Size: 5','Fleet Size: 10'], fontsize=15)
ax1.grid()

#Subplot 2
l1 = ax2.plot(t, f.total('BEV', 'N', False, t), linewidth=lw)

#year = 2
fm=5
year=2
ax2.plot(t[:year+1], f.total('BEV', 'N', False, t[:year+1]), color=c1, linewidth=lw)
ax2.plot([year,year+1], [f.total('BEV', 'N', False, t[year]), f.total('BEV', 'Y', True, t[year+1], fm=fm)+f.total('BEV', 'N',False,t[year-1])], color=c1, linewidth=lw)
y2 = ax2.plot(t[year+1:], f.total('BEV', 'Y', True, t[year+1:], fm=fm)+f.total('BEV', 'N',False,t[year-1]), color=c1, linewidth=lw)#+ f.total('BEV', 'N', False, year))

#year=3
year=3
ax2.plot(t[:year+1], f.total('BEV', 'N', False, t[:year+1]), color=c3, linewidth=lw)
ax2.plot([year,year+1], [f.total('BEV', 'N', False, t[year]), f.total('BEV', 'Y', True, t[year+1], fm=fm)+f.total('BEV', 'N',False,t[year-1])], color=c2, linewidth=lw)
y3 = ax2.plot(t[year+1:], f.total('BEV', 'Y', True, t[year+1:], fm=fm)+f.total('BEV', 'N',False,t[year-1]), color=c2, linewidth=lw)#+ f.total('BEV', 'N', False, year))
#

#year = 5
year = 5
ax2.plot(t[:year+1], f.total('BEV', 'N', False, t[:year+1]), color=c3, linewidth=lw)
ax2.plot([year,year+1], [f.total('BEV', 'N', False, t[year]), f.total('BEV', 'Y', True, t[year+1], fm=fm)+f.total('BEV', 'N',False,t[year-1])], color=c3, linewidth=lw)
y5 = ax2.plot(t[year+1:], f.total('BEV', 'Y', True, t[year+1:], fm=fm)+f.total('BEV', 'N',False,t[year-1]), color=c3, linewidth=lw)#+ f.total('BEV', 'N', False, year))
#ax1.plot([year+1,t[-1]], f.total)

#year=10
year=8
ax2.plot(t[:year+1], f.total('BEV', 'N', False, t[:year+1]), color=c4, linewidth=lw)
ax2.plot([year,year+1], [f.total('BEV', 'N', False, t[year]), f.total('BEV', 'Y', True, t[year+1], fm=fm)+f.total('BEV', 'N',False,t[year-1])], color=c4, linewidth=lw)
y8 = ax2.plot(t[year+1:], f.total('BEV', 'Y', True, t[year+1:], fm=fm)+f.total('BEV', 'N',False,t[year-1]), color=c4, linewidth=lw)#+ f.total('BEV', 'N', False, year))


ax2.legend((y2[0], y3[0], y5[0], y8[0]), ['2 years', '3 years', '5 years','8 years'], fontsize=15)
#ax2.legend()
ax2.grid()

ax1.set_ylabel('Total Cost ($)', fontsize=25)
ax2.set_ylabel('Total Cost ($)', fontsize=25)
ax2.set_xlabel('Time (years)', fontsize=25)
plt.xlabel('Time (years)', fontsize=25)
plt.show()