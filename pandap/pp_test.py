from add_element import add_bus,add_gen,add_line_from_param,add_load,create_net
import pandapower as pp
# this is simulation of grid1.jpg
# vbase = 63 kv, sbase = 100mva, zbase = 63*63/100 = 39.69 ohm

net = create_net(network='net1')

add_bus('bt.csv',net)
add_gen('gt.csv',net)
add_line_from_param('lit.csv',net)
add_load('lot.csv',net)
# pp.plotting.simple_plot(net)
pp.runpp(net)
print(net.res_bus)