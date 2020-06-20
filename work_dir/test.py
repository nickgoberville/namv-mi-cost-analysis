import os, sys
namvi_mi_root = os.getcwd()+'/..'
sys.path.append(namvi_mi_root)
from namv_mi.cost_analysis import cost_per_mile, cost_per_rider, ytd_plot, deployment_scenarios_ytd, deployment_scenarios_flows

# Generating cost per mile plot
#cost_per_mile.main()
#cost_per_rider.main()
#ytd_plot.main()
#deployment_scenarios_ytd.main()
deployment_scenarios_flows.main()

#TODO:
#       3 --> Wait times plots for appendix