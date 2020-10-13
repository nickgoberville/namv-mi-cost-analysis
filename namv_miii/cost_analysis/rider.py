import matplotlib.pyplot as plt
import numpy as np
import time

def wait_time(df, name='NULL'):
    '''
    Function to plot wait time of the vehicle. 
     -- df is a pandas DataFrame which must contain "wait_times_list" column
    '''
    bins = {'<30 s': {'bounds': (0,30),
                  'count': 0},
            '30-120 s': {'bounds': (30,120),
                  'count': 0},
            '120-300 s': {'bounds': (120,300),
                  'count': 0},
            '300-600 s': {'bounds': (300,600),
                  'count': 0},
            '>600 s': {'bounds': (600,float('inf')),
                  'count': 0}
           }

    print("Initial {} Bins: {}".format(name, bins))

    times_list = df.wait_times_list
    #print(type(times_list[0])) 
    #print(type(eval(times_list[0])))
    for day in df.index:
        times_list = eval(df.wait_times_list[day])
        for wait_time in times_list:
            #print("\n{} seconds".format(wait_time))
            for key, value in bins.items():
                
                if wait_time >= value['bounds'][0] and wait_time < value['bounds'][1]:
                    value['count'] += 1
                    #print("     place in bin {}".format(key))
    plt.figure()
    plot_vals = []
    y_pos = np.arange(len(bins.keys()))
    for key in bins.keys():
        plot_vals.append(bins[key]['count'])
    plt.bar(y_pos, plot_vals)
    plt.xticks(y_pos, bins.keys())
    plt.ylabel('Riders')
    plt.title(name+' rider wait times')
    plt.show()

    print("Final {} Bins: {}".format(name, bins))
    #time.sleep(10)