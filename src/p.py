import pandas as pd
import pandapower.networks as pn 
import pandapower as pp
 
net = pn.case39()
pp.runpp(net, 'fdbx')
print(net.res_bus)
