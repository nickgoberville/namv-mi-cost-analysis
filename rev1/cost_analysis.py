#! /usr/bin/env python3
import matplotlib as mpl
print(mpl.get_backend())
mpl.use("TkAgg")
print(mpl.get_backend())
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
from cost_model import *

#plt.ion()

vehicles = pd.read_csv('vehicles.csv')
modes = read_json('modes.json')
models_dict = {}

def maintenance_plots(cash_flow=True, YTD=True):
    plot_types = []
    sup_title = ['YTD', 'cash_flow']
    if YTD:
        plot_types.append(0)
    if cash_flow:
        plot_types.append(1)

    for plot_type in plot_types:
        fig = plt.figure()
        fig.suptitle(sup_title[plot_type])
        axes_set = False
        for index in vehicles.index:
            label = vehicles.vehicle[index]
            if not axes_set: 
                ax = []
            for i, (key, value) in enumerate(modes.items()):
                vehicle = model(vehicles, index, inflation=True, mode=key)
                models_dict[vehicle.name] = vehicle
                
                if not axes_set:
                    ax.append(fig.add_subplot(2,2,i+1))
                ax[i].plot(vehicle.time, vehicle.maint()[plot_type], label=label)
                ax[i].set_title(key)
                ax[i].legend()
            axes_set=True
        plt.show(block=True)

def operation_plots(cash_flow=True, YTD=True):
    plot_types = []
    sup_title = ['YTD', 'cash_flow']
    if YTD: plot_types.append(0)
    if cash_flow: plot_types.append(1)

    for plot_type in plot_types:
        fig = plt.figure()
        fig.suptitle(sup_title[plot_type])
        axes_set = False

        for index in vehicles.index:
            label = vehicles.vehicle[index]
            if not axes_set: 
                ax = []

            for i, (key, value) in enumerate(modes.items()):
                vehicle = model(vehicles, index, inflation=True, mode=key)
                models_dict[vehicle.name] = vehicle 
                if not axes_set:
                    ax.append(fig.add_subplot(2,2,i+1))
                ax[i].plot(vehicle.time, vehicle.oper()[plot_type], label=label)
                ax[i].set_title(key)
                ax[i].legend()

            axes_set=True
        plt.show(block=True)

def total_plots(cash_flow=True, YTD=True):
    plot_types = []
    sup_title = ['YTD', 'cash_flow']
    if YTD: plot_types.append(0)
    if cash_flow: plot_types.append(1)

    for plot_type in plot_types:
        fig = plt.figure()
        fig.suptitle(sup_title[plot_type])
        axes_set = False

        for index in vehicles.index:
            label = vehicles.vehicle[index]
            if not axes_set: 
                ax = []

            for i, (key, value) in enumerate(modes.items()):
                vehicle = model(vehicles, index, inflation=True, mode=key)
                models_dict[vehicle.name] = vehicle 
                if not axes_set:
                    ax.append(fig.add_subplot(2,2,i+1))
                ax[i].plot(vehicle.time, vehicle.total()[plot_type], label=label)
                ax[i].set_title(key)
                ax[i].legend()

            axes_set=True
        plt.show(block=True)

def per_rider_plots(cash_flow=True, YTD=True):
    plot_types = []
    sup_title = ['YTD', 'cash_flow']
    if YTD: plot_types.append(0)
    if cash_flow: plot_types.append(1)

    for plot_type in plot_types:
        fig = plt.figure()
        fig.suptitle(sup_title[plot_type])
        axes_set = False

        for index in vehicles.index:
            label = vehicles.vehicle[index]
            if not axes_set: 
                ax = []

            for i, (key, value) in enumerate(modes.items()):
                vehicle = model(vehicles, index, inflation=True, mode=key)
                models_dict[vehicle.name] = vehicle 
                if not axes_set:
                    ax.append(fig.add_subplot(2,2,i+1))
                ax[i].plot(vehicle.time, vehicle.per_rider()[plot_type], label=label)
                ax[i].set_title(key)
                ax[i].legend()

            axes_set=True
        plt.show(block=True)
#maintenance_plots(cash_flow=False)
per_rider_plots()
#operation_plots()