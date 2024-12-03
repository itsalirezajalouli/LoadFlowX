# Methods of load flow calculations 

# Imports
import pandapower as pp 
from termcolor import colored

# Creates the network
class NetworkCreator():
    def __init__(self) -> None:
        self.net = pp.create_empty_network()
        self.buses = {}
        self.tBuses = {}
        self.trafos = {}
        self.busCounter = 0
        self.trafoBusCounter = 0
        self.trafoCounter = 0

    def addSlack(self, key: str, vmPu: float, vaDeg: float):
        pp.create_ext_grid(self.net, self.buses[key], vm_pu = vmPu, va_degree = vaDeg)

    def addBusBar(self, vnKv: float, name: str):
        self.busCounter += 1
        key = f'Bus{self.busCounter}'
        self.buses[key] = pp.create_bus(self.net, vn_kv = vnKv, name = name, type = 'b')

    def addTransBus(self, vnKv: float, name: str):
        self.trafoBusCounter += 1
        key = f'TBus{self.trafoBusCounter}'
        self.tBuses[key] = pp.create_bus(self.net, vn_kv = vnKv,
                                             name = name, type = 'n')

    def addTransformer(self, busOne: str, busTwo: str, name: str,
                       stdType: str = '25 MVA 110/20 kV'):
        self.trafoCounter += 1
        key = f'Transformer{self.trafoCounter}'
        busOneKey = self.tBuses[busOne]
        busTwoKey = self.tBuses[busTwo]
        self.trafos[key] = pp.create_transformer(self.net, busOneKey, busTwoKey,
                                                 name = name, std_type = stdType)

    def log(self):
        print(colored(
        '''
                                █   █▀█ █▀▀ █▀
                                █▄▄ █▄█ █▄█ ▄█
        '''
        , 'light_blue'))
        print(colored('-' * 80, 'red'))
        print(colored('-> Buses:', 'light_blue'), '\n', self.buses)
        print(colored('-> Tranfo Buses:', 'light_blue'), '\n', self.tBuses)
        print(colored('-> Transformers:', 'light_blue'), '\n', self.trafos)
        print(colored('-' * 80, 'red'))
        print(colored('-> Bus Table:', 'light_blue'), '\n', self.net.bus)
        print(colored('-' * 80, 'red'))
        print(colored('-> External Grid Table:', 'light_blue'), '\n', self.net.ext_grid)
        print(colored('-' * 80, 'red'))
        # print('Transformer Table: \n', self.net.trafo)

    def run(self, method: str):
        pp.runpp(self.net, algorithm = method)
        print(self.net.res_bus)

nMaker = NetworkCreator()
nMaker.addBusBar(110, 'Bus1')
nMaker.addBusBar(20, 'Bus2')
nMaker.addBusBar(110, 'Bus3')
nMaker.addTransBus(110, 'TBus1')
nMaker.addTransBus(20, 'TBus2')
nMaker.addTransformer('TBus1', 'TBus2', '110kV/20kV transformer',
                      )
nMaker.addSlack('Bus1', 1.02, 50)
nMaker.log()
nMaker.run('gs')
