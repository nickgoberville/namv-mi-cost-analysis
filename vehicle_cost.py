#! /usr/bin/env python3
import numpy as np
import parameters as p

t = np.arange(2036-2018)
battery_cost = {'Base': {'initial': 197,    # 2018
                         'rate_1': 0.07,    # 2020-2028
                         'rate_2': 0.03},   # 2028+
                         
                'Optimistic': {'initial': 161,  # 2018
                               'rate_1': 0.083, # 2019-2030
                               'rate_2': 0.03}, # 2030+
                              
                'Conservative': {'initial': 220, # 2018
                                 'rate_1': 0.05, # 2020-2025, no reduction 2025-2028
                                 'rate_2': 0.01}}# 2028+

def base_price():
    base_price = [battery_cost['Base']['initial']]  # 2018 price
    base_price.append(base_price[0])                   # 2019 price
    for i in range(len(base_price)-1, len(base_price) + 8):                      # 2020-2028 price
        base_price.append(base_price[i]*(1 - battery_cost['Base']['rate_1']))

    for i in range(len(base_price)-1, len(base_price)+ 6):               # 2020-2028 price
        base_price.append(base_price[i]*(1 - battery_cost['Base']['rate_2']))
    return base_price

def optimistic_price():
    opt_price = [battery_cost['Optimistic']['initial']]  # 2018 price
    opt_price.append(opt_price[0])                   # 2019 price
    for i in range(len(opt_price)-1, len(opt_price) + 10):                      # 2020-2028 price
        opt_price.append(opt_price[i]*(1 - battery_cost['Base']['rate_1']))

    for i in range(len(opt_price)-1, len(opt_price)+ 4):               # 2020-2028 price
        opt_price.append(opt_price[i]*(1 - battery_cost['Base']['rate_2']))
    return opt_price

print(base_price())
print(optimistic_price())
print(len(base_price()))
print(len(optimistic_price()))
print(len(t))
