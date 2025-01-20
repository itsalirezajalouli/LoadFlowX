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
                 zone: int,
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
        self.zone = zone
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
        print(colored('-> Voltage Magnitude:', 'light_blue'), self.vMag)
        print(colored('-> Zone:', 'light_blue'), self.zone)

    def append2CSV(self, path: str) -> None:
        data = {
            'id': self.id,
            'bType': self.bType,
            'vMag': self.vMag,
            'zone': self.zone,
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
            writer = csv.DictWriter(file,fieldnames=['id', 'bType', 'vMag', 'zone', 'vAng',
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


class Line:
    def __init__(self,
                 bus1id: int,
                 bus2id: int,
                 name: str,
                 R: float,
                 X: float,
                 len: float,
                 c_nf_per_km: float,
                 max_i_ka: float) -> None:
        self.name = name
        self.bus1id = bus1id
        self.bus2id = bus2id
        self.R = R
        self.X = X
        self.len = len
        self.c_nf_per_km = c_nf_per_km
        self.max_i_ka = max_i_ka

    def log(self) -> None:
        """Logs the line parameters in a formatted and colored manner."""
        print(colored(
        '''
                                █   █▀█ █▀▀ █▀
                                █▄▄ █▄█ █▄█ ▄█
        ''', 'light_blue'))
        print(colored('-' * 80, 'red'))
        print(colored('-> First Bus ID:', 'light_blue'), self.bus1id)
        print(colored('-> Second Bus ID:', 'light_blue'), self.bus2id)
        print(colored('-> Name:', 'light_blue'), self.name)
        print(colored('-> R (Ohm/km):', 'light_blue'), self.R)
        print(colored('-> X (Ohm/km):', 'light_blue'), self.X)
        print(colored('-> Length (km):', 'light_blue'), self.len)
        print(colored('-> Capacitance (nF/km):', 'light_blue'), self.c_nf_per_km)
        print(colored('-> Max Current (kA):', 'light_blue'), self.max_i_ka)

    def append2CSV(self, path: str) -> None:
        data = {
            'name': self.name,
            'bus1id': self.bus1id,
            'bus2id': self.bus2id,
            'R': self.R,
            'X': self.X,
            'len': self.len,
            'c_nf_per_km': self.c_nf_per_km,
            'max_i_ka': self.max_i_ka
        }
        csvPath = f'{path}/Lines.csv'
        with open(csvPath, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=[
                'name', 'bus1id', 'bus2id', 'R', 'X', 
                'len', 'c_nf_per_km', 'max_i_ka'
            ])
            # Write header if file is empty
            if file.tell() == 0:
                writer.writeheader()
            writer.writerow(data)
        print(f'-> Line data appended to {csvPath} successfully.')


class Transformer():
    def __init__(self,
                 id: int,
                 name: str,
                 hvBus: int,
                 lvBus: int,
                 pos: QPoint,
                 orient: str,
                 hands: list,
                 sn_mva: float = 0.0,
                 vk_percent: float = 0.0,
                 vkr_percent: float = 0.0,
                 tap_step_percent: float = 0.0) -> None:
        self.id = id
        self.name = name  # just for GUI display
        self.hvBus = hvBus
        self.lvBus = lvBus
        self.pos = (pos.x(), pos.y())
        self.orient = orient
        self.hands = [(h.x(), h.y()) for h in hands]
        self.sn_mva = sn_mva
        self.vk_percent = vk_percent
        self.vkr_percent = vkr_percent
        self.tap_step_percent = tap_step_percent

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
        print(colored('-> Rated Power (sn_mva):', 'light_blue'), self.sn_mva)
        print(colored('-> Short-Circuit Voltage (vk_percent):', 'light_blue'), self.vk_percent)
        print(colored('-> Resistive Component (vkr_percent):', 'light_blue'), self.vkr_percent)
        print(colored('-> Tap Step (tap_step_percent):', 'light_blue'), self.tap_step_percent)

    def append2CSV(self, path: str) -> None:
        data = {
            'id': self.id,
            'name': self.name,
            'hvBus': self.hvBus,
            'lvBus': self.lvBus,
            'pos': json.dumps(self.pos),
            'orient': self.orient,
            'hands': json.dumps(self.hands),
            'sn_mva': self.sn_mva,
            'vk_percent': self.vk_percent,
            'vkr_percent': self.vkr_percent,
            'tap_step_percent': self.tap_step_percent
        }
        csvPath = path + '/Trafos.csv'
        with open(csvPath, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=[
                'id', 'name', 'hvBus', 'lvBus', 'pos', 'orient', 'hands', 
                'sn_mva', 'vk_percent', 'vkr_percent', 'tap_step_percent'
            ])
            writer.writerow(data)
        print(f'-> Transformer data appended to {csvPath} successfully.')

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
                    row['sn_mva'] = self.sn_mva
                    row['vk_percent'] = self.vk_percent
                    row['vkr_percent'] = self.vkr_percent
                    row['tap_step_percent'] = self.tap_step_percent
                newTransformerList.append(row)

        with open(csvPath, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=[
                'id', 'name', 'hvBus', 'lvBus', 'pos', 'orient', 'hands', 
                'sn_mva', 'vk_percent', 'vkr_percent', 'tap_step_percent'
            ])
            writer.writeheader()
            writer.writerows(newTransformerList)
        print(f'-> Transformer data edited in {csvPath} successfully.')

class Generator():
    def __init__(self,
                 bus: int,
                 name: str,
                 pMW: float,
                 vmPU: float,
                 minQMvar: float,
                 maxQMvar: float,
                 minPMW: float,
                 maxPMW: float,
                 pos: QPoint,
                 orient: str,
                 hand: QPoint
                 ) -> None:
        self.bus = bus
        self.name = name
        self.pMW = pMW
        self.vmPU = vmPU
        self.minQMvar = minQMvar
        self.maxQMvar = maxQMvar
        self.minPMW = minPMW
        self.maxPMW = maxPMW
        self.pos = (pos.x(), pos.y())
        self.orient = orient
        self.hand = (hand.x(), hand.y())

    def append2CSV(self, path: str) -> None:
        data = {
            'bus': self.bus,
            'name': self.name,
            'pMW': self.pMW,
            'vmPU': self.vmPU,
            'minQMvar': self.minQMvar,
            'maxQMvar': self.maxQMvar,
            'minPMW': self.minPMW,
            'maxPMW': self.maxPMW,
            'pos': json.dumps(self.pos),
            'orient': self.orient,
            'hand': json.dumps(self.hand),
        }
        csvPath = path + '/Gens.csv'
        with open(csvPath, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=[
                'bus', 'name', 'pMW', 'vmPU', 'minQMvar', 'maxQMvar', 
                'minPMW', 'maxPMW', 'pos', 'orient', 'hand'
            ])
            if file.tell() == 0:  # Check if the file is empty to write headers
                writer.writeheader()
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
                 vaD: float,
                 pos: QPoint,
                 orient: str,
                 hand: QPoint,
                 ) -> None:
        self.bus = bus
        self.vmPU = vmPU
        self.vaD = vaD 
        self.pos = (pos.x(), pos.y())
        self.orient = orient
        self.hand = (hand.x(), hand.y())

    def append2CSV(self, path: str) -> None:
        data = {
            'bus': self.bus,
            'vmPU': self.vmPU,
            'vaD': self.vaD,
            'pos': json.dumps(self.pos),
            'orient': self.orient,
            'hand': json.dumps(self.hand),
        }
        csvPath = path + '/Slacks.csv'
        with open(csvPath, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['bus', 'vmPU', 'vaD', 'pos', 'orient', 'hand'])
            writer.writerow(data)
        print(f'-> Slack data appended to {csvPath} successfully.')
