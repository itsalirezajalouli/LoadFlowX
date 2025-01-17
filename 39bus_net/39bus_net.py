import pandapower as pp
import pandapower.networks as pn
import csv
net = pn.case39()
# pp.plotting.simple_plot(net)
line_before_pf = dict(net.line)
with open('line_before_pf.csv',"w") as file:
    writer = csv.DictWriter(file,fieldnames=['to_bus', 'length_km', 'max_i_ka', 'x_ohm_per_km', 'max_loading_percent', 'from_bus', 'r_ohm_per_km', 
'c_nf_per_km', 'parallel', 'df', 'type', 'name', 'g_us_per_km', 'std_type', 'in_service'])
    writer.writeheader()
    writer.writerow(line_before_pf)



pp.runpp(net)
# pp.plotting.create_bus_collection(net)



line_after_pf = dict(net.line)
with open('line_after_pf.csv',"w") as file:
    writer = csv.DictWriter(file,fieldnames=['to_bus', 'length_km', 'max_i_ka', 'x_ohm_per_km', 'max_loading_percent', 'from_bus', 'r_ohm_per_km', 
'c_nf_per_km', 'parallel', 'df', 'type', 'name', 'g_us_per_km', 'std_type', 'in_service'])
    writer.writeheader()
    writer.writerow(line_after_pf)