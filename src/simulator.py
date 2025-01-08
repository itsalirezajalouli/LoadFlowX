# Methods of load flow calculations 

# Imports
import csv
import pandapower as pp 
from termcolor import colored

# Creates the network
class NetworkCreator():

    def __init__(self, busCsv: str, lineCsv: str, trafoCsv: str, genCsv: str) -> None:
        self.net = pp.create_empty_network()
        self.buses = {}
        self.tBuses = {}
        self.trafos = {}
        self.lines = {}
        self.gens = {}
        self.busCounter = 0
        self.trafoBusCounter = 0
        self.trafoCounter = 0
        self.lineCounter = 0
        self.genCounter = 0
        self.busCsv = busCsv
        self.lineCsv = lineCsv
        self.trafoCsv = trafoCsv
        self.genCsv = genCsv

    def addSlack(self, key: str, vmPu: float, vaDeg: float) -> None:
        pp.create_ext_grid(self.net, self.buses[key], vm_pu = vmPu, va_degree = vaDeg)

    def addBusBar(self, vnKv: float, name: str, id: int) -> None:
        self.busCounter += 1
        key = f'Bus{self.busCounter}'
        self.buses[key] = pp.create_bus(self.net, vn_kv = float(vnKv),
                            name = name, index = id, type = 'b')
        print('-> Bus added to simulation:')
        print(f'V: {vnKv}, Name: {name}, Id: {id}')

    def addLine(self, fromBus: int, toBus: int, len: float, name: str) -> None:
        self.lineCounter += 1
        key = f'Line{self.lineCounter}'
        self.lines[key] = pp.create_line(self.net, from_bus = fromBus, to_bus = toBus,
                                         length_km = len, name = 'Line',
                                         std_type = 'NAYY 4x50 SE')
        print('-> Bus added to simulation:')
        print(f'From Bus: {fromBus}, To Bus: {toBus}, Length(KM): {len}, name: {name}')

    def addGen(self, bus: int, name: str, pMW: float) -> None:
        self.genCounter += 1
        key = f'Gen{self.genCounter}'
        self.gens[key] = pp.create_gen(self.net, bus = bus, name = name, p_mw = pMW)
        print('-> Gen added to simulation:')
        print(f'Bus: {bus}, Name: {name}, pMW: {pMW}')

    def addTrafo(self, name: str, id: int, busOne: str, busTwo: str):
        self.trafoCounter += 1
        key = f'Transformer{self.trafoCounter}'
        busOneKey = self.buses[busOne]
        busTwoKey = self.buses[busTwo]
        self.trafos[key] = pp.create_transformer(self.net, busOneKey, busTwoKey,
                                     name = name, std_type = '25 MVA 110/20 kV',
                                                 index = id)
        print('-> Trafo added to simulation:')
        print(f'Bus1: {busOne}, bus2: {busTwo}, id: {id}')

    def log(self):
        print(colored(
        '''
                                █   █▀█ █▀▀ █▀
                                █▄▄ █▄█ █▄█ ▄█
        '''
        , 'light_blue'))
        print(colored('-' * 80, 'red'))
        print(colored('-> Buses:', 'light_blue'), '\n', self.buses)
        print(colored('-> Lines:', 'light_blue'), '\n', self.lines)
        print(colored('-> Tranfo Buses:', 'light_blue'), '\n', self.tBuses)
        print(colored('-> Transformers:', 'light_blue'), '\n', self.trafos)
        print(colored('-' * 80, 'red'))
        print(colored('-> Bus Table:', 'light_blue'), '\n', self.net.bus)
        print(colored('-' * 80, 'red'))
        print(colored('-> External Grid Table:', 'light_blue'), '\n', self.net.ext_grid)
        print(colored('-' * 80, 'red'))
        # print('Transformer Table: \n', self.net.trafo)

    def run(self, method: str):
        self.loadBusBars()
        print('busses', self.buses)
        self.loadLines()
        self.loadGens()
        self.loadTrafos()
        print(colored('-> Buses:', 'light_blue'), '\n', self.buses)
        print(colored('-> Lines:', 'light_blue'), '\n', self.lines)
        print(colored('-> Gens:', 'light_blue'), '\n', self.gens)
        # pp.runpp(self.net, algorithm = method)
        # print(self.net.res_bus)

    def loadBusBars(self) -> None:
        with open(self.busCsv) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # if row['vUnit'] == 'KV':
                self.addBusBar(float(row['vMag']), row['name'], int(row['id']))

    def loadLines(self) -> None:
        with open(self.lineCsv) as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                if row['bus1id'] != row['bus2id']:
                    self.addLine(int(row['bus1id']), int(row['bus2id']), float(row['len']),
                                row['name'])

    def loadGens(self) -> None:
        with open(self.genCsv) as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                self.addGen(int(row['bus']), row['name'], float(row['pMW']))

    def loadTrafos(self) -> None:
        with open(self.trafoCsv) as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                b1id = int(row['hvBus'])
                b1 = str(f'Bus{b1id}')
                b2id = int(row['lvBus'])
                b2 = str(f'Bus{b2id}')
                self.addTrafo(row['name'], int(row['id']), b1, b2)

# nMaker = NetworkCreator()
# nMaker.addBusBar(110, 'Bus1')
# nMaker.addBusBar(20, 'Bus2')
# nMaker.addBusBar(110, 'Bus3')
# nMaker.addTransBus(110, 'TBus1')
# nMaker.addTransBus(20, 'TBus2')
# nMaker.addTransformer('TBus1', 'TBus2', '110kV/20kV transformer',
#                       )
# nMaker.addSlack('Bus1', 1.02, 50)
# nMaker.log()
# nMaker.run('gs')
