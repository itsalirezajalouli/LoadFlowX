from add_element import *
import pandapower as pp
# this is simulation of grid1.jpg
# vbase = 63 kv, sbase = 100mva, zbase = 63*63/100 = 39.69 ohm

net = create_net(network='net1')

add_bus('bt.csv',net)
add_gen('gt.csv',net)
add_line_from_param('lit.csv',net)
add_load('lot.csv',net)
pp.plotting.simple_plot(net)
lf(net)
print(net.res_bus)