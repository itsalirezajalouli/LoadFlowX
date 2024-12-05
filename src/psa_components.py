#   Components like Bus, Line and Network...

class BusBar():
    def __init__(self,
                 id: int,
                 name: str,
                 bType: str,
                 vMag: float,
                 vAng: float,
                 P: float, 
                 Q: float,
                 ) -> None:
        self.name = name # just for GUI display
        self.id = id
        self.bType = bType
        self.vMag = vMag
        self.vAng = vAng
        self.P = P
        self.Q = Q

class Transformer():
    def __init__(self,
                 R: float,
                 X: float,
                 ) -> None:
       self.R = R 
       self.X = X 
