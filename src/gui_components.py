# Imports
import os
from sys import settrace
import typing
import pandas as pd
from os.path import isdir
from PyQt6.QtCore import QPoint, Qt
from dialogs import GetProjectNameDialog, AddBusDialog
from theme import DiscordPalette as theme
from PyQt6.QtGui import QColor, QPalette, QPaintEvent, QPen, QPainter, QBrush, QDoubleValidator, QKeyEvent
from PyQt6.QtWidgets import QApplication, QComboBox, QDialog, QHBoxLayout, QLineEdit, QPushButton, QVBoxLayout, QWidget, QLabel, QDialogButtonBox, QMessageBox

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
        self.yellow = theme.toQtColor(theme.yellow) 
        self.offSet = QPoint(0, 0)
        self.insertBusMode = False
        self.projectName = None
        self.addBusDialog = None
        self.busCounter = 0
        self.busses = {}
        self.highLightedPoint = None
        self.currentMousePos = None
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
        self.currentMousePos = event.pos()
        self.highLightedPoint = self.snap(event.pos())
        self.update()

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            if self.insertBusMode:
                pos = self.snap(event.pos())
                defaultCapacity = 1
                defaultOrientation = '-90'
                busTuple = (pos, defaultCapacity, defaultOrientation)
                self.addBusDialog = AddBusDialog(self)
                self.addBusDialog.busPos = pos
                self.busCounter += 1
                self.addBusDialog.busId = self.busCounter
                self.addBusDialog.projectName = self.projectName
                self.addBusDialog.exec()
                self.busses[self.addBusDialog.nameInput.text()] = busTuple
                self.update()
            
        # Clicked on an existing bus
        if event.button() == Qt.MouseButton.LeftButton and self.insertBusMode == False:
            pos = self.snap(event.pos())
            x = pos.x()
            y = pos.y()
            for bus, (point, capacity, orient) in self.busses.items():
                busX = point.x()
                busY = point.y()
                self.editBusDialog = EditBusDialog(self)
                self.editBusDialog.busPos = point
                projectPath = os.path.join('./user_data/', self.projectName)
                csvPath = projectPath + '/Buses.csv'
                df = pd.read_csv(csvPath)
                if orient == '-90':
                    if x == busX and y in range(busY, busY + capacity * self.dist):
                        matchedRow = df[df['pos'] == str(point)]
                        if not matchedRow.empty:
                            self.editBusDialog
                            self.editBusDialog.nameInput.setText(str(matchedRow['name'].item()))
                            self.editBusDialog.vMagInput.setText(str(matchedRow['vMag'].item()))
                            self.editBusDialog.vAngInput.setText(str(matchedRow['vAng'].item()))
                            self.editBusDialog.pInput.setText(str(matchedRow['P'].item()))
                            self.exitBusDialog.qInput.setText(str(matchedRow['Q'].item()))
                            self.editBusDialog.exec()
                # elif orient == '0':
                #     if x in range(busX, busX + capacity * self.dist) and y == busY:
                # elif orient == '90':
                #     if x == busX and y in range(busY - capacity * self.dist, busY):
                # elif orient == '180':
                #     if x in range(busX - capacity * self.dist, busX) and y == busY:
                self.update()

        if event.button() == Qt.MouseButton.RightButton and QApplication.keyboardModifiers() == Qt.KeyboardModifier.AltModifier:
            pos = self.snap(event.pos())
            x = pos.x()
            y = pos.y()
            for bus, (point, capacity, orient) in self.busses.items():
                busX = point.x()
                busY = point.y()
                if capacity > 2:
                    if orient == '-90':
                        if x == busX and y in range(busY, busY + capacity * self.dist):
                            capacity -= 2
                    elif orient == '0':
                        if x in range(busX, busX + capacity * self.dist) and y == busY:
                            capacity -= 2
                    elif orient == '90':
                        if x == busX and y in range(busY - capacity * self.dist, busY):
                            capacity -= 2
                    elif orient == '180':
                        if x in range(busX - capacity * self.dist, busX) and y == busY:
                            capacity -= 2
                    busTuple = (point, capacity, orient)
                    self.busses[bus] = busTuple
                    self.update()

        if event.button() == Qt.MouseButton.RightButton:
            pos = self.snap(event.pos())
            x = pos.x()
            y = pos.y()
            for bus, (point, capacity, orient) in self.busses.items():
                busX = point.x()
                busY = point.y()
                if orient == '-90':
                    if x == busX and y in range(busY, busY + capacity * self.dist):
                        capacity += 1
                elif orient == '0':
                    if x in range(busX, busX + capacity * self.dist) and y == busY:
                        capacity += 1
                elif orient == '90':
                    if x == busX and y in range(busY - capacity * self.dist, busY):
                        capacity += 1
                elif orient == '180':
                    if x in range(busX - capacity * self.dist, busX) and y == busY:
                        capacity += 1
                busTuple = (point, capacity, orient)
                self.busses[bus] = busTuple
                self.update()

    def wheelEvent(self, event) -> None:
        pos = self.currentMousePos
        pos = self.snap(pos)
        x = pos.x()
        y = pos.y()
        for bus, (point, capacity, orient) in self.busses.items():
            busX = point.x()
            busY = point.y()
            if orient == '-90':
                if x == busX and y in range(busY, busY + capacity * self.dist):
                    orient = '0'
            elif orient == '0':
                if x in range(busX, busX + capacity * self.dist) and y == busY:
                    orient = '90'
            elif orient == '90':
                if x == busX and y in range(busY - capacity * self.dist, busY):
                    orient = '180'
            elif orient == '180':
                if x in range(busX - capacity * self.dist, busX) and y == busY:
                    orient = '-90'
            busTuple = (point, capacity, orient)
            self.busses[bus] = busTuple
            self.update()

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
        if self.addBusDialog is not None and not self.addBusDialog.inputError:
            for bus, (point, capacity, orient) in self.busses.items():
                # Get the points
                busX = point.x()
                busY = point.y()
                # Create Symbol
                symbolPen = QPen()
                symbolPen.setWidth(self.lineWidth)
                symbolPen.setColor(self.blue)
                painter.setPen(symbolPen)
                if orient == '-90':
                    painter.drawLine(busX, busY - self.dist, busX,
                                     busY + ( capacity * self.dist))
                elif orient == '0':
                    painter.drawLine(busX - self.dist, busY, busX + ( capacity * self.dist),
                                     busY)
                elif orient == '90':
                    painter.drawLine(busX, busY + self.dist, busX,
                                     busY - ( capacity * self.dist))
                elif orient == '180':
                    painter.drawLine(busX + self.dist, busY, busX - ( capacity * self.dist),
                                     busY)
                # Create Text
                txtPen = QPen()
                txtPen.setWidth(self.txtWidth)
                txtPen.setColor(self.yellow)
                # Calculate text dimensions
                textRect = painter.fontMetrics().boundingRect(bus)
                textWidth = textRect.width()
                textHeight = textRect.height()
                # Center text horizontally and vertically relative to the bus line
                txtPointX = busX - (textWidth // 2)
                txtPointY = busY - (self.dist) - (textHeight // 2)
                if orient == '-90':
                    txtPointX = busX - (textWidth // 2)
                    txtPointY = busY - (self.dist) - (textHeight)
                elif orient == '90':
                    txtPointX = busX - (textWidth // 2)
                    txtPointY = busY + (self.dist) + (textHeight)
                elif orient == '0':
                    txtPointX = busX + (((capacity - 1) * self.dist) // 2) - textWidth // 2
                    txtPointY = busY + (self.dist) + (textHeight // 2)
                elif orient == '180':
                    txtPointX = busX - (((capacity - 1) * self.dist) // 2) - textWidth // 2
                    txtPointY = busY - (self.dist) - (textHeight // 2) 
                txtPoint = QPoint(txtPointX, txtPointY)
                painter.setPen(txtPen)
                txtPoint = QPoint(txtPointX, txtPointY)
                painter.drawText(txtPoint, bus)
                # Create the Connection Capacities
                dotPen = QPen()
                dotPen.setColor(self.highLightWhite)
                dotPen.setWidth(self.txtWidth)
                painter.setPen(dotPen)
                if orient == '-90':
                    for _ in range(0, capacity):
                        painter.drawEllipse(busX - 1, busY - 1, 2, 2)
                        busY += self.dist
                elif orient == '0':
                    for _ in range(0, capacity):
                        painter.drawEllipse(busX - 1, busY - 1, 2, 2)
                        busX += self.dist
                elif orient == '90':
                    for _ in range(0, capacity):
                        painter.drawEllipse(busX - 1, busY - 1, 2, 2)
                        busY -= self.dist
                elif orient == '180':
                    for _ in range(0, capacity):
                        painter.drawEllipse(busX - 1, busY - 1, 2, 2)
                        busX -= self.dist

        painter.end()

