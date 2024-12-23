#   Components like Bus, Line and Network...
import csv
from enum import Enum
from termcolor import colored

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
                 pos: tuple[float, float],
                 id: int,
                 name: str,
                 bType: BusType,
                 vMag: float,
                 vAng: float,
                 P: float, 
                 Q: float,
                 ) -> None:
        self.pos = pos
        self.name = name # just for GUI display
        self.id = id
        self.bType = bType
        self.vMag = vMag
        self.vAng = vAng
        self.P = P
        self.Q = Q

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
            'name': self.name,
            'pos': self.pos,
            'bType': self.bType,
            'vMag': self.vMag,
            'vAng': self.vAng,
            'P': self.P,
            'Q': self.Q,
        }
        csvPath = path + '/Buses.csv'
        with open(csvPath, 'a', newline = '') as file:
            writer = csv.DictWriter(file,fieldnames=['id','name','pos','bType','vMag',
                                                     'vAng','P','Q'])
            writer.writerow(data)
        print(f'-> Bus data appended to {path} successfuly.')

    def editCSV(self, path: str, prevName: str) -> None:
        csvPath = path + '/Buses.csv'
        newBusList = []
        with open(csvPath) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['name'] == prevName:
                    row['name'] = self.name
                    row['id'] = self.id
                    row['pos'] = self.pos
                    row['bType'] = self.bType
                    row['vMag'] = self.vMag
                    row['vAng'] = self.vAng
                    row['P'] = self.P
                    row['Q'] = self.Q
                newBusList.append(row)

        with open(csvPath, 'w', newline = '') as file:
            writer = csv.DictWriter(file,fieldnames=['id','name','pos','bType','vMag',
                                                     'vAng','P','Q'])
            writer.writeheader()
            writer.writerows(newBusList)
            print(f'-> Bus Data edited to {path} successfuly.')
class Line():
    def __init__(self,
                 bus1id: int,
                 bus2id: int,
                 R: float,
                 X: float,
                 len: float,
                 vBase: float,
                 ) -> None:
        self.bus1id = bus1id
        self.bus2id = bus2id
        self.R = R
        self.X = X
        self.len = len
        self.vBase = vBase

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
            'bus1id': self.bus1id, 
            'bus2id': self.bus2id, 
            'R': self.R,
            'X': self.X,
            'len': self.len,
            'vBase': self.vBase,
        }
        csvPath = path + '/Lines.csv'
        with open(csvPath, 'a', newline = '') as file:
            writer = csv.DictWriter(file,fieldnames=['bus1id','bus2id','R','X','len',
                                                     'vBase'])
            writer.writerow(data)
        print(f'-> Line data appended to {path} successfuly.')

class Transformer():
    def __init__(self,
                 pos: tuple[float, float],
                 id: int,
                 name: str,
                 R: float,
                 X: float,
                 a: float,
                 vBase: float,
                 winding: Winding,
                 ) -> None:
        self.pos = pos
        self.name = name # just for GUI display
        self.id = id
        self.R = R 
        self.X = X 
        self.a = a
        self.vBase = vBase
        self.winding = winding

