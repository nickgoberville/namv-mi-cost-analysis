import matplotlib.pyplot as plt
import random

def plot(x, y, ax):
    ax.plot(x,y, label='one')
    ax.legend()
    return ax

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
x1 = [random.randint(x, x+1) for x in range(5)]
y1 = [random.randint(x, x+1) for x in range(5)]

x2 = [random.randint(x, x+1) for x in range(5)]
y2 = [random.randint(x, x+1) for x in range(5)]

ax = plot(x1, y1, ax)
#plt.show()
ax = plot(x2, y2, ax)
plt.show()