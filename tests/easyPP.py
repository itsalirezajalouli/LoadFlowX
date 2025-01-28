import pandapower as pp
import pandapower.networks as nw

# Import case39
net = nw.case39()
pp.runpp(net, algorithm = 'nr') # Newton-Raphson

# Results
print('Bus Results:')
print(net.res_bus)
print('\nLine Results:')
print(net.res_line)
