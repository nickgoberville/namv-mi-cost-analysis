import random

def get_vect(in_array, dt=12):
    output = []
    summer = 0
    for i, val in enumerate(in_array):
        if i>0 and i%dt == 0:
            print("appending {}".format(summer))
            output.append(summer)
            print("reseting: summer --> 0")
            summer = 0
        summer += val
    print("appending {}".format(summer))
    output.append(summer)
    return output
#x = {"one": 1, "two": 2, "three": 3}
#print(*x.values())
#print(get_vect(*x.values()))
vect = [random.randint(0, 10) for _ in range(20)]
print(vect)
print(get_vect(vect, 2))
'''
import numpy as np
import matplotlib.pyplot as plt
x = [1,2,3]
y = [4,5,6]
z = [x, y]
t = np.arange(6)
z2 = np.array(z).reshape(-1,1)

print(np.array(z))

plt.figure()
plt.plot(t, z2)
plt.show()
'''