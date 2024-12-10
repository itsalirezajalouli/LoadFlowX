# Imports
import os
# from os.path import isdir
from PyQt6.QtCore import QPoint, Qt
from psa_components import BusBar, BusType
from theme import DiscordPalette as theme
from PyQt6.QtGui import QColor, QPalette, QPaintEvent, QPen, QPainter, QBrush
from PyQt6.QtWidgets import QComboBox, QDialog, QHBoxLayout, QLineEdit, QPushButton, QVBoxLayout, QWidget, QLabel, QDialogButtonBox, QMessageBox

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
        self.gridWidth = 1
        self.txtWidth = 2
        self.lineWidth = 2
        self.lineColor = QColor(100, 100, 100, 100)
        self.dotColor = QColor(125, 125, 125, 125)
        self.highLightWhite = QColor(255, 255, 255, 255)
        self.txtColor = theme.toQtColor(theme.foreground)
        self.red = theme.toQtColor(theme.red) 
        self.blue = theme.toQtColor(theme.blue) 
        self.purple = theme.toQtColor(theme.purple) 
        self.offSet = QPoint(0, 0)
        self.insertBusMode = False
        self.projectName = None
        self.busCounter = 0
        self.busses = {}
        self.highLightedPoint = None
        # Mouse Tracking for Hovering
        self.setMouseTracking(True)

    def snap(self, pos: QPoint) -> QPoint:
        # To escape repetition of code i created this function it's gonna be very useful
        x = pos.x()
        y = pos.y()
        xmod = x % self.dist
        ymod = y % self.dist
        if xmod < (self.dist / 2):
            x -= xmod
        else: 
            x += (self.dist - xmod)
        if ymod < (self.dist / 2):
            y -= ymod
        else: 
            y += (self.dist - ymod)
        return QPoint(x, y)

    def mouseMoveEvent(self, event) -> None:
        self.highLightedPoint = self.snap(event.pos())
        self.update()

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            if self.insertBusMode:
                pos = self.snap(event.pos())
                defaultCapacity = 1
                busTuple = (pos, defaultCapacity)
                self.addBusDialog = AddBusDialog(self)
                self.addBusDialog.busPos = pos
                self.busCounter += 1
                self.addBusDialog.busId = self.busCounter
                self.addBusDialog.projectName = self.projectName
                self.addBusDialog.exec()
                self.busses[self.addBusDialog.nameInput.text()] = busTuple
                self.update()
                self.insertBusMode = False

        if event.button() == Qt.MouseButton.RightButton:
            pos = self.snap(event.pos())
            x = pos.x()
            y = pos.y()
            for bus, (point, capacity) in self.busses.items():
                busX = point.x()
                busY = point.y()
                if x == busX and y in range(busY, busY + capacity * self.dist):
                    capacity += 1
                    busTuple = (point, capacity)
                    self.busses[bus] = busTuple

    def insertBus(self) -> None:
        pass

    def setOffset(self, offset):
        # Sets an offset on the grid to simulate a move.
        self.offSet = QPoint(int(offset.x() % self.dist),
                               int(offset.y() % self.dist))

    def paintEvent(self, event: QPaintEvent) -> None:
        # Set Pen for Grid painting
        pen = QPen()
        pen.setWidth(self.gridWidth)
        pen.setColor(self.lineColor)
        painter = QPainter()
        painter.begin(self)
        painter.setPen(pen)

        # Horizontal lines
        startH = QPoint(0, int(self.offSet.y()))
        endH = QPoint(int(self.width()), int(self.offSet.y()))
        distanceH = QPoint(0, int(self.dist))

        # Vertical lines
        startV = QPoint(int(self.offSet.x()), 0)
        endV = QPoint(int(self.offSet.x()), int(self.height()))
        distanceV = QPoint(int(self.dist), 0)

        while startH.y() < self.height():
            painter.drawLine(startH, endH)
            startH += distanceH
            endH += distanceH

        while startV.x() < self.width():
            painter.drawLine(startV, endV)
            startV += distanceV
            endV += distanceV

        startH = QPoint(0, int(self.offSet.y()))
        startV = QPoint(int(self.offSet.x()), 0)

        # Drawing little dots on the collision
        x = 0
        y = 0
        while y < self.height():
            while x < self.width():
                dotPen = QPen()
                dotPen.setColor(self.dotColor)
                painter.setPen(dotPen)
                painter.drawEllipse(x - 1, y - 1, 2, 2)
                x += self.dist
            y += self.dist
            x = 0

        # Drawing where the mouse is pointing to drop the item
        highLightedPoint = self.highLightedPoint
        if highLightedPoint is not None:
            dotPen = QPen()
            dotPen.setColor(self.highLightWhite)
            dotPen.setWidth(self.txtWidth)
            painter.setPen(dotPen)
            xHigh = highLightedPoint.x()
            yHigh = highLightedPoint.y()
            painter.drawEllipse(xHigh - 1, yHigh - 1, 2, 2)

        # Drawing all the busbars here
        for bus, (point, capacity) in self.busses.items():
            # Get the points
            busX = point.x()
            busY = point.y()
            # Create Symbol
            symbolPen = QPen()
            symbolPen.setWidth(self.lineWidth)
            symbolPen.setColor(self.purple)
            painter.setPen(symbolPen)
            painter.drawLine(busX, busY - self.dist, busX, busY + ( capacity * self.dist))
            # Create Text
            txtPen = QPen()
            txtPen.setWidth(self.txtWidth)
            txtPen.setColor(self.txtColor)
            # Calculate text dimensions
            textRect = painter.fontMetrics().boundingRect(bus)
            textWidth = textRect.width()
            textHeight = textRect.height()
            # Center text horizontally and vertically relative to the bus line
            txtPointX = busX - (textWidth // 2)
            txtPointY = busY - (self.dist) - (textHeight // 2)
            txtPoint = QPoint(txtPointX, txtPointY)
            painter.setPen(txtPen)
            txtPoint = QPoint(txtPointX, txtPointY)
            painter.drawText(txtPoint, bus)
            # Create the Connection Capacities
            painter.setPen(Qt.PenStyle.NoPen)
            brush = QBrush(self.txtColor)  
            painter.setBrush(brush)
            for _ in range(0, capacity):
                painter.drawEllipse(busX - 2, busY - 2, 4, 4)
                busY += self.dist

        painter.end()

class GetProjectNameDialog(QDialog):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.projectName = None
        self.setWindowTitle('New Project')
        self.setStyleSheet('''
        QDialog {
            font-size: 24px;
            color: #ffffff;
            background-color: #3b3e45;
            border: 2px solid #7289da;
            border-radius: 10px;
            padding: 2px;
        }
        ''')
        self.title = QLabel('New Load Flow Project')
        self.title.setStyleSheet('''
            color: #ffffff;
            border: 2px solid #7289da;
            border-radius: 5px;
            padding: 8px;
        ''')
        self.nameInputLabel = QLabel('Project Name:')
        self.nameInputLabel.setStyleSheet('color: #ffffff;')
        self.nameInput = QLineEdit(self)
        self.nameInput.setPlaceholderText('Pick a name for your Network')

        # Button Box
        self.startProjectButton = QPushButton()
        self.startProjectButton.setText('Start Project')
        self.startProjectButton.clicked.connect(self.startProject)

        layout = QVBoxLayout()
        layout.addWidget(self.nameInputLabel)
        layout.addWidget(self.nameInput)
        layout.addWidget(self.startProjectButton)
        self.setLayout(layout)

    def startProject(self) -> None:
        self.accept()
        self.projectName = self.nameInput.text()
        if not os.path.isdir('./user_data'):
            os.mkdir('./user_data')
        projectPath = os.path.join('./user_data/', self.projectName)
        if os.path.isdir(projectPath):
            QMessageBox.warning(self, 'Project Exists',
                'A Project with the same name exists.', QMessageBox.StandardButton.Ok)
        else:
            os.mkdir(projectPath)

class AddBusDialog(QDialog):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setWindowTitle('Add Bus Bar')
        self.setStyleSheet('''
        QDialog {
            font-size: 24px;
            color: #ffffff;
            background-color: #3b3e45;
            border: 2px solid #7289da;
            border-radius: 10px;
            padding: 2px;
        }
        ''')
        self.title = QLabel('Add Bus Bar to Network')
        self.title.setStyleSheet('''
            color: #ffffff;
            border: 2px solid #7289da;
            border-radius: 5px;
            padding: 8px;
        ''')
        
        self.busId = None
        self.busPos = None
        self.busType = BusType.SLACK 
        self.projectName = None

        # Bus Name Input Box
        self.nameInputLabel = QLabel('Bus Name:')
        self.nameInputLabel.setStyleSheet('color: #ffffff;')
        self.nameInput = QLineEdit(self)
        self.nameInput.setPlaceholderText('Set Your Bus Name')

        # Bus Type Combo Box
        self.typeInputLabel = QLabel('Bus Type:')
        self.typeInputLabel.setStyleSheet('color: #ffffff;')
        self.busTypeDropDown = QComboBox(self) 
        self.busTypeDropDown.addItem('SLACK')
        self.busTypeDropDown.addItem('PV')
        self.busTypeDropDown.addItem('PQ')
        self.busTypeDropDown.activated.connect(self.busTypeActivator)

        # V Magnitude & Angle Input Box
        self.vInputLabel = QLabel('Voltage (|V|∠δ):')
        self.vInputLabel.setStyleSheet('color: #ffffff;')
        self.vWidget = QWidget()
        self.vHBox = QHBoxLayout()
        self.vMagInput = QLineEdit(self)
        self.vMagInput.setPlaceholderText('|V|')
        self.vAngInput = QLineEdit(self)
        self.vAngInput.setPlaceholderText('δ')
        self.vUnitDropDown = QComboBox(self) 
        self.vUnitDropDown.addItem('PU')
        self.vUnitDropDown.addItem('KV')
        self.vUnitDropDown.addItem('V')
        self.vDegreeTypeDropDown = QComboBox(self) 
        self.vDegreeTypeDropDown.addItem('Deg')
        self.vDegreeTypeDropDown.addItem('Rad')
        self.vHBox.addWidget(self.vMagInput)
        self.vHBox.addWidget(self.vUnitDropDown)
        self.vHBox.addWidget(self.vAngInput)
        self.vHBox.addWidget(self.vDegreeTypeDropDown)
        self.vWidget.setLayout(self.vHBox)

        # P & Q Input Box
        self.pqInputLabel = QLabel('Active & Passive Power:')
        self.pqInputLabel.setStyleSheet('color: #ffffff;')
        self.pqWidget = QWidget()
        self.pqHBox = QHBoxLayout()
        self.pInput = QLineEdit(self)
        self.pInput.setPlaceholderText('P')
        self.qInput = QLineEdit(self)
        self.qInput.setPlaceholderText('Q')
        self.pUnitDropDown = QComboBox(self) 
        self.pUnitDropDown.addItem('PU')
        self.pUnitDropDown.addItem('KW')
        self.qUnitDropDown = QComboBox(self) 
        self.qUnitDropDown.addItem('PU')
        self.qUnitDropDown.addItem('KVA')
        self.pqHBox.addWidget(self.pInput)
        self.pqHBox.addWidget(self.pUnitDropDown)
        self.pqHBox.addWidget(self.qInput)
        self.pqHBox.addWidget(self.qUnitDropDown)
        self.pqWidget.setLayout(self.pqHBox)

        # Button Box
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.nameInputLabel)
        layout.addWidget(self.nameInput)
        layout.addWidget(self.typeInputLabel)
        layout.addWidget(self.busTypeDropDown)
        layout.addWidget(self.vInputLabel)
        layout.addWidget(self.vWidget)
        layout.addWidget(self.pqInputLabel)
        layout.addWidget(self.pqWidget)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

    def busTypeActivator(self, index) -> None:
        if index == 0: 
            self.busType = BusType.SLACK
        elif index == 1:
            self.busType = BusType.PV
        elif index == 2:
            self.busType = BusType.PQ

    def accept(self) -> None:
        bus = BusBar(
            id = self.busId,
            pos = self.busPos,
            name = self.nameInput.text(),
            bType = self.busType, 
            vAng = float(self.vAngInput.text()),
            vMag = float(self.vMagInput.text()),
            P = float(self.pInput.text()),
            Q = float(self.qInput.text()),
        )
        bus.log()
        projectPath = os.path.join('./user_data/', self.projectName)
        bus.makeCSV(projectPath)
        super().accept()

