import pandapower.networks as nw
import pandapower as pp

net = nw.case39()
print('bus' + 100 * '-' + '\n', net.bus)
print('line' + 100 * '-' + '\n', net.line)
print('trafo' + 100 * '-' + '\n', net.trafo)
print('ext' + 100 * '-' + '\n', net.ext_grid)
print('load' + 100 * '-' + '\n', net.load)
print('gen' + 100 * '-' + '\n', net.gen)

pp.runpp(net)
print('res_bus' + 100 * '-' + '\n', net.res_bus)
print('res_gen' + 100 * '-' + '\n', net.res_gen)
print('res_line' + 100 * '-' + '\n', net.res_line)
