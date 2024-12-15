#   Components like Bus, Line and Network...
import pandas as pd
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

    def makeCSV(self, path) -> None:
        data = {
            'id': [self.id],
            'name': [self.name],
            'pos': [self.pos],
            'bType': [self.bType],
            'vMag': [self.vMag],
            'vAng': [self.vAng],
            'P': [self.P],
            'Q': [self.Q],
        }
        df = pd.DataFrame(data)
        csvPath = path + '/Buses.csv'
        df.to_csv(csvPath, mode = 'a', index = False, header = False)
        print('Data appended successfuly.')

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

class Line():
    def __init__(self,
                 bus1id: int,
                 bus2id: int,
                 R: float,
                 X: float,
                 Length: float,
                 vBase: float,
                 ) -> None:
        self.bus1id = bus1id
        self.bus2id = bus2id
        self.R = R
        self.X = X
        self.Length = Length
        self.vBase = vBase
