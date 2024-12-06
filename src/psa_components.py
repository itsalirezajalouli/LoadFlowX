#   Components like Bus, Line and Network...
from enum import Enum

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
