# Imports
from PyQt6.QtCore import QPoint
from PyQt6.QtGui import QColor, QPalette, QPaintEvent, QPen, QPainter
from PyQt6.QtWidgets import QWidget

class Color(QWidget):
    def __init__(self, color: str) -> None:
        super().__init__()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)

class Grid(QWidget):
    def __init__(self, dist, *args, ** kwargs):
        super().__init__(*args, **kwargs)
        self.dist = dist 
        self.penWidth = 1
        self.lineColor = QColor(100, 100, 100, 100)
        self.offSet = QPoint(0, 0)

        # Disable the widgets to ignore all events
        # Widget should not become mousegrabber
        self.setDisabled(True)

    def set_offset(self, offset):
        '''
        Sets an offset on the grid to simulate a move.
        '''
        self.offSet = QPoint(int(offset.x() % self.dist),
                               int(offset.y() % self.dist))

    def paintEvent(self, event: QPaintEvent) -> None:
        pen = QPen()
        pen.setWidth(self.penWidth)
        pen.setColor(self.lineColor)
        painter = QPainter()
        painter.begin(self)
        painter.setPen(pen)

        # Horizontal lines
        startH = QPoint(0, int(self.offSet.y()))
        endH = QPoint(int(self.width()), int(self.offSet.y()))
        distance_h = QPoint(0, int(self.dist))

        # Vertical lines
        startV = QPoint(int(self.offSet.x()), 0)
        endV = QPoint(int(self.offSet.x()), int(self.height()))
        distanceV = QPoint(int(self.dist), 0)

        while startH.y() < self.height():
            painter.drawLine(startH, endH)
            startH += distance_h
            endH += distance_h

        while startV.x() < self.width():
            painter.drawLine(startV, endV)
            startV += distanceV
            endV += distanceV

        painter.end()
