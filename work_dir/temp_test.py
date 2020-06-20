#! /usr/bin/env python3
import os, sys
namvi_mi_root = os.getcwd()+'/..'
sys.path.append(namvi_mi_root)
from namv_mi.cost_model.cost_model import *
from namv_mi.utils import process_sim_results as sim
from namv_mi.plots.templates import barPlot, sub_dim
'''import glob
import pandas as pd
from plot_code import rider, YTD

from cost_model.cost_model import *
import process_sim_results as sim
import numpy as np
import matplotlib.pyplot as plt
from cost_analysis import line_plots
'''
# Get modes (normal, AV_SD, AV_FM, AV_full)
num = 9
index = 1
print(sub_dim(num, index, return_type=int))
#fig = plt.figure()
#fig.add_subplot(sub_dim(num, index, col_size=2, return_type=int))
#plt.show()
bar = barPlot(qty=10)
print(bar.params)
plt.show()