import os, sys
namvi_mi_root = os.getcwd()+'/..'
sys.path.append(namvi_mi_root)
from namv_mi.cost_analysis import cost_per_mile, cost_per_rider, ytd_plot, deployment_scenarios_ytd, deployment_scenarios_flows, get_results

#TODO   1) Write script in namv_mi.cost_analysis that exports all cost results to a csv
#       2) rewrite plot scripts to take the csv file as the input
#       3) Make it more general (EX: line 51 in cost_analysis.cost_per_mile)

# Generating cost per mile plot
cost_per_mile.main()
#get_results.main()
#cost_per_rider.main(costs.csv)
#ytd_plot.main(costs.csv)
#deployment_scenarios_ytd.main(costs.csv)
#deployment_scenarios_flows.main()

#TODO:
#       3 --> Wait times plots for appendix