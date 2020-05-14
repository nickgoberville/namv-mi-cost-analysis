import matplotlib.pyplot as plt


def plot(vehicle, sim_results, ax):
    x = vehicle.time
    y = vehicle.total()
    ax.plot(x,y)
    yield ax
#fig = plt.figure()
#ax = fig.add_subplot(111)