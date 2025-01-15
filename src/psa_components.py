#   Components like Bus, Line and Network...
import csv
import json
from enum import Enum
from termcolor import colored
from PyQt6.QtCore import QPoint

class BusType(Enum):
    SLACK = 'slack'
    PV = 'pv'
    PQ = 'pq'

class Winding(Enum):
    DELTA = 'delta'
    Y = 'Y'
    GY = 'Grounded Y'

class BusBar():
    def __init__(self,
                 pos: QPoint,
                 id: int,
                 name: str,
                 bType: BusType,
                 vMag: float,
                 # vAng: float,
                 # P: float, 
                 # Q: float,
                 capacity: int,
                 orient: str,
                 points: list,
                 ) -> None:
        self.pos = (pos.x(), pos.y())
        self.name = name # just for GUI display
        self.id = id
        self.bType = bType
        self.vMag = vMag
        self.vAng = 'NaN'
        self.P = 'NaN'
        self.Q = 'NaN'
        self.capacity = capacity
        self.orient = orient
        self.points = [] 

        for p in points:
            for pp in p:
                tup = (pp.x(), pp.y())
                self.points.append(tup)

    def log(self) -> None:
        print(colored(
        '''
                                █   █▀█ █▀▀ █▀
                                █▄▄ █▄█ █▄█ ▄█
        '''
        , 'light_blue'))
        print(colored('-' * 80, 'red'))
        print(colored('-> ID:', 'light_blue'), self.id)
        print(colored('-> Name:', 'light_blue'), self.name)
        print(colored('-> Pos:', 'light_blue'), self.pos)
        print(colored('-> Bus Type:', 'light_blue'), self.bType)
        print(colored('-> Voltage Magnitude:', 'light_blue'), self.vMag)
        print(colored('-> Voltage Angle:', 'light_blue'), self.vAng)
        print(colored('-> Active Power:', 'light_blue'), self.P)
        print(colored('-> Passive Power:', 'light_blue'), self.Q)

    def append2CSV(self, path: str) -> None:
        data = {
            'id': self.id,
            'bType': self.bType,
            'vMag': self.vMag,
            'vAng': self.vAng,
            'P': self.P,
            'Q': self.Q,
            'name': self.name,
            'pos': json.dumps(self.pos),
            'capacity': self.capacity,
            'orient': self.orient,
            'points': json.dumps(self.points)
        }
        csvPath = path + '/Buses.csv'
        with open(csvPath, 'a', newline = '') as file:
            writer = csv.DictWriter(file,fieldnames=['id', 'bType', 'vMag', 'vAng',
                                                     'P', 'Q', 'name', 'pos',
                                                     'capacity', 'orient', 'points'])
            writer.writerow(data)
        print(f'-> Bus data appended to {path} successfuly.')

    def editCSV(self, path: str, prevName: str) -> None:
        csvPath = path + '/Buses.csv'
        newBusList = []
        with open(csvPath) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['name'] == prevName:
                    row['id'] = self.id
                    row['bType'] = self.bType
                    row['vMag'] = self.vMag
                    row['vAng'] = self.vAng
                    row['P'] = self.P
                    row['Q'] = self.Q
                    row['name'] = self.name,
                    row['pos'] = json.dumps(self.pos),
                    row['capacity'] = self.capacity,
                    row['orient'] = self.orient,
                    row['points'] = json.dumps(self.points)
                newBusList.append(row)

        with open(csvPath, 'w', newline = '') as file:
            writer = csv.DictWriter(file,fieldnames=['id', 'bType', 'vMag', 'vAng',
                                                     'P', 'Q', 'name', 'pos',
                                                     'capacity', 'orient', 'points'])
            writer.writeheader()
            writer.writerows(newBusList)
            print(f'-> Bus Data edited to {csvPath} successfuly.')

class Line():
    def __init__(self,
                 bus1id: int,
                 bus2id: int,
                 name: str,
                 # R: float,
                 # X: float,
                 len: float,
                 # vBase: float,
                 ) -> None:
        self.name = name
        self.bus1id = bus1id
        self.bus2id = bus2id
        self.R = 'NaN'
        self.X = 'NaN'
        self.len = len
        self.vBase = 'NaN'

    def log(self) -> None:
        print(colored(
        '''
                                █   █▀█ █▀▀ █▀
                                █▄▄ █▄█ █▄█ ▄█
        '''
        , 'light_blue'))
        print(colored('-' * 80, 'red'))
        print(colored('-> First Bus ID:', 'light_blue'), self.bus1id)
        print(colored('-> Second Bus ID:', 'light_blue'), self.bus2id)
        print(colored('-> R:', 'light_blue'), self.R)
        print(colored('-> X:', 'light_blue'), self.X)
        print(colored('-> Length:', 'light_blue'), self.len)
        print(colored('-> V Base:', 'light_blue'), self.vBase)

    def append2CSV(self, path: str) -> None:
        data = {
            'name': self.name,
            'bus1id': self.bus1id, 
            'bus2id': self.bus2id, 
            'R': self.R,
            'X': self.X,
            'len': self.len,
            'vBase': self.vBase,
        }
        csvPath = path + '/Lines.csv'
        with open(csvPath, 'a', newline = '') as file:
            writer = csv.DictWriter(file,fieldnames = ['name', 'bus1id','bus2id','R','X',
                                                     'len', 'vBase'])
            writer.writerow(data)
        print(f'-> Line data appended to {csvPath} successfuly.')

class Transformer():
    def __init__(self,
                 id: int,
                 name: str,
                 hvBus: int,
                 lvBus: int,
                 pos: QPoint,
                 orient: str,
                 hands: list) -> None:
        self.pos = (pos.x(), pos.y())
        self.name = name # just for GUI display
        self.id = id
        self.hvBus = hvBus
        self.lvBus = lvBus
        self.orient = orient
        self.hands = [(h.x(), h.y()) for h in hands]
        self.R = 0 
        self.X = 0 
        self.a = 0
        self.vBase = 0
        self.winding = 0

    def log(self) -> None:
        print(colored(
        '''
                                █   █▀█ █▀▀ █▀
                                █▄▄ █▄█ █▄█ ▄█
        '''
        , 'light_blue'))
        print(colored('-' * 80, 'red'))
        print(colored('-> ID:', 'light_blue'), self.id)
        print(colored('-> Name:', 'light_blue'), self.name)
        print(colored('-> Pos:', 'light_blue'), self.pos)
        print(colored('-> HV Bus:', 'light_blue'), self.hvBus)
        print(colored('-> LV Bus:', 'light_blue'), self.lvBus)
        print(colored('-> Orientation:', 'light_blue'), self.orient)
        print(colored('-> Hands:', 'light_blue'), self.hands)

    def append2CSV(self, path: str) -> None:
        data = {
            'id': self.id,
            'name': self.name,
            'hvBus': self.hvBus,
            'lvBus': self.lvBus,
            'pos': json.dumps(self.pos),
            'orient': self.orient,
            'hands': json.dumps(self.hands)
        }
        csvPath = path + '/Trafos.csv'
        with open(csvPath, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['id', 'name', 'hvBus', 'lvBus', 'pos', 'orient', 'hands'])
            writer.writerow(data)
        print(f'-> Transformer data appended to {path} successfully.')

    def editCSV(self, path: str, prevName: str) -> None:
        csvPath = path + '/Trafos.csv'
        newTransformerList = []
        with open(csvPath) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['name'] == prevName:
                    row['id'] = self.id
                    row['name'] = self.name
                    row['hvBus'] = self.hvBus
                    row['lvBus'] = self.lvBus
                    row['pos'] = json.dumps(self.pos)
                    row['orient'] = self.orient
                    row['hands'] = json.dumps(self.hands)
                newTransformerList.append(row)

        with open(csvPath, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['id', 'name', 'hvBus', 'lvBus', 'pos', 'orient', 'hands'])
            writer.writeheader()
            writer.writerows(newTransformerList)
        print(f'-> Transformer data edited in {csvPath} successfully.')

class Generator():
    def __init__(self,
                 bus: int,
                 name: str,
                 pMW: float,
                 pos: QPoint,
                 orient: str,
                 hand: QPoint,
                 ) -> None:
        self.bus = bus
        self.name = name
        self.pMW = pMW
        self.pos = (pos.x(), pos.y())
        self.orient = orient
        self.hand = (hand.x(), hand.y())

    def append2CSV(self, path: str) -> None:
        data = {
            'bus': self.bus,
            'name': self.name,
            'pMW': self.pMW,
            'pos': json.dumps(self.pos),
            'orient': self.orient,
            'hand': json.dumps(self.hand),
        }
        csvPath = path + '/Gens.csv'
        with open(csvPath, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['bus', 'name', 'pMW', 'pos', 'orient', 'hand'])
            writer.writerow(data)
        print(f'-> Gen data appended to {csvPath} successfully.')

class Load():
    def __init__(self,
                 bus: int,
                 pMW: float,
                 qMW: float,
                 pos: QPoint,
                 orient: str,
                 hand: QPoint,
                 ) -> None:
        self.bus = bus
        self.pMW = pMW
        self.qMW = qMW
        self.pos = (pos.x(), pos.y())
        self.orient = orient
        self.hand = (hand.x(), hand.y())

    def append2CSV(self, path: str) -> None:
        data = {
            'bus': self.bus,
            'pMW': self.pMW,
            'qMW': self.qMW,
            'pos': json.dumps(self.pos),
            'orient': self.orient,
            'hand': json.dumps(self.hand),
        }
        csvPath = path + '/Loads.csv'
        with open(csvPath, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['bus', 'pMW', 'qMW', 'pos', 'orient', 'hand'])
            writer.writerow(data)
        print(f'-> Load data appended to {csvPath} successfully.')

class Slack():
    def __init__(self,
                 bus: int,
                 vmPU: float,
                 pos: QPoint,
                 orient: str,
                 hand: QPoint,
                 ) -> None:
        self.bus = bus
        self.vmPU = vmPU
        self.pos = (pos.x(), pos.y())
        self.orient = orient
        self.hand = (hand.x(), hand.y())

    def append2CSV(self, path: str) -> None:
        data = {
            'bus': self.bus,
            'vmPU': self.vmPU,
            'pos': json.dumps(self.pos),
            'orient': self.orient,
            'hand': json.dumps(self.hand),
        }
        csvPath = path + '/Slacks.csv'
        with open(csvPath, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['bus', 'vmPU', 'pos', 'orient', 'hand'])
            writer.writerow(data)
        print(f'-> Slack data appended to {csvPath} successfully.')
