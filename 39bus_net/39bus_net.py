import pandapower as pp
import pandapower.networks as pn
net = pn.case39()
# pp.plotting.simple_plot(net)
pp.runpp(net)
print(net.res_line)
# pp.plotting.create_bus_collection(net)