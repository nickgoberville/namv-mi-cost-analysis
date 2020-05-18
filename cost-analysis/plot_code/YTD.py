import matplotlib.pyplot as plt


def plot(vehicle, fig_YTD, ax_YTD, index, fig_YTD_axes_set, c, label, i):
    if not fig_YTD_axes_set and i==0:    # append new axes if not already set
        ax_YTD.append(fig_YTD.add_subplot(2,2,index+1))
        ax_YTD[index].set_title(vehicle.name_nomode)
        if index == 0 or index == 2:
            ax_YTD[index].set_ylabel('YTD Cost (USD)')
        if index == 2 or index == 3:
            ax_YTD[index].set_xlabel('Time (years)')
   # get vehicle cost model
            # plot YTD cost vs time
    print("Plotting ytd of {}_{} in axes {}".format(vehicle.name, vehicle.drive_train, index))
    ytd, cash_flow = vehicle.total()
    ax_YTD[index].plot(vehicle.time, ytd, c[i], label=label)#label=label)
    ax_YTD[index].legend()
#fig = plt.figure()
#ax = fig.add_subplot(111)