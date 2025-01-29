import pandapower.networks as nw
import pandapower as pp

net = nw.four_loads_with_branches_out()
print(net.bus)
print()
print(net.line)
print()
print(net.gen)
print()
print(net.load)
print()
print(net.trafo)
print()
print(net.ext_grid)

pp.runpp(net)
print(net.res_bus)
print(net.res_trafo)
