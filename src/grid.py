# Imports
import os
import csv
from copy import deepcopy
from PyQt6.QtCore import QPoint, Qt
from bus_dialogs import AddBusDialog, EditBusDialog
from line_dialogs import AddLineDialog
from run_dialogs import RunSimDialog
from theme import DiscordPalette as theme
from PyQt6.QtGui import QColor, QPaintEvent, QPen, QPainter
from PyQt6.QtWidgets import QApplication, QWidget

from trafo_dialogs import AddTrafoDialog

# Grid Gui Handler 
class Grid(QWidget):
    def __init__(self, dist, *args, ** kwargs):
        super().__init__(*args, **kwargs)
        # Style Properties
        self.dist = dist 
        self.gridWidth = 1
        self.txtWidth = 2
        self.lineWidth = 2
        self.lineColor = QColor(100, 100, 100, 100)
        self.dotColor = QColor(125, 125, 125, 125)
        self.connectionColor = QColor(140, 140, 140, 140)
        self.highLightWhite = QColor(255, 255, 255, 255)
        self.txtColor = theme.toQtColor(theme.foreground)
        self.red = theme.toQtColor(theme.red) 
        self.blue = theme.toQtColor(theme.blue) 
        self.yellow = theme.toQtColor(theme.yellow) 
        self.offSet = QPoint(0, 0)
        self.highLightedPoint = None
        self.currentMousePos = None
        self.insertingOrient = '-90'
        self.handActivatedPos = None

        # State Properties
        self.selectMode = False
        self.handMode = False
        self.insertBusMode = False
        self.insertLineMode = False
        self.insertTrafoMode = False

        self.correctNodeSelect = False 
        self.spacePressed = False  # Track the state of the Space key

        # Dialogs
        self.addBusDialog = None
        self.editBusDialog = None
        self.addLineDialog = None
        self.addTrafoDialog = None
        self.runSimDialog = None
        
        # Data Properties
        self.projectPath = None
        self.busCounter = 0
        self.trafoCounter = 0
        self.firstNode = None
        self.busses = {}
        self.trafos = {}
        self.paths = []
        self.tokenBusPorts = []
        self.tokenTrafoHands = []
        self.xDists = []
        self.tempPath = []
        self.orientations = ['-90', '0', '90', '180']
        self.trafoCenters = []

        # Defaults
        self.freq = 50
        self.sBase = 100

        # Mouse Tracking for Hovering
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)  # Enable focus for key events
        self.update()

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
        if self.handMode and self.handActivatedPos is not None:
            xDiff = (self.highLightedPoint.x() - self.handActivatedPos.x())
            yDiff = (self.highLightedPoint.y() - self.handActivatedPos.y())
            print(xDiff, yDiff)
            for bus, (point, capacity, orient, points, id) in self.busses.items():
                newOriginX = point.x() + xDiff 
                newOriginY = point.y() + yDiff 
                newOrigin = QPoint(newOriginX, newOriginY)
                point = self.snap(newOrigin)
                newPoints = []
                for p in points:
                    p = self.snap(QPoint(p.x() + xDiff, p.y() + yDiff))
                    newPoints.append(p)
                bigTuple = (point, capacity, orient, newPoints, id)
                edited = self.editedBusses(bus, bigTuple)
            self.update()
            newPaths = []
            for p in self.paths:
                connection1, connection2, fp, i, tempPath = p
                newTp = []
                for tp in tempPath:
                    tp = self.snap(QPoint(tp.x() + xDiff, tp.y() + xDiff))
                    newTp.append(tp)
                p = connection1, connection2, fp, i, newTp
                newPaths.append(p)
            self.paths = newPaths
            self.update()
            handActivatedPosX = self.handActivatedPos.x() + xDiff
            handActivatedPosY = self.handActivatedPos.y() + yDiff
            newHAP = QPoint(handActivatedPosX, handActivatedPosY)
            self.handActivatedPos = self.snap(newHAP)
        self.update()

    # def keyPressEvent(self, event):
    #     if event.key() == Qt.Key.Key_Space:
    #         self.spacePressed = True
    #         # print('Space pressed!')
    #         self.checkCombo()
    # def keyReleaseEvent(self, event):
    #     if event.key() == Qt.Key.Key_Space:
    #         self.spacePressed = False
    #         # print("Space key released")
    #
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.handMode:
            self.handActivatedPos = None
    #
    # def checkCombo(self):
    #     if self.spacePressed and self.leftMouseHold:
    #         self.comboLocation = deepcopy(self.currentMousePos)
    #         # print('Space + Left Mouse Button pressed!')

    def mousePressEvent(self, event) -> None:
        self.leftMouseHold = True
        if event.button() == Qt.MouseButton.LeftButton:
            self.leftMouseHold = True
            # Placing a bus
            if self.insertBusMode:
                pos = self.snap(event.pos())
                defaultCapacity = 1
                defaultOrientation = '-90'
                self.addBusDialog = AddBusDialog(self)
                self.addBusDialog.busPos = pos
                self.busCounter += 1
                self.addBusDialog.busId = self.busCounter
                self.addBusDialog.projectPath = self.projectPath
                self.addBusDialog.exec()
                busName = self.addBusDialog.nameInput.text()
                id = self.busCounter
                self.setBusDict(busName, pos, defaultCapacity, defaultOrientation, id)

            # Placing a Transformator 
            if self.insertTrafoMode:
                pos = self.snap(event.pos())
                self.addTrafoDialog = AddTrafoDialog(self)
                self.addTrafoDialog.projectPath = self.projectPath
                self.addTrafoDialog.trafoBus = pos
                self.addTrafoDialog.trafoId = self.trafoCounter
                self.addTrafoDialog.exec()
                # busName = self.addBusDialog.nameInput.text()
                self.setTrafoDict(pos)
                self.update()
            
            # Placing Line: First Connection
            if self.insertLineMode and self.firstNode is None:
                self.firstPointPos = self.snap(event.pos())
                for bus, (point, capacity, orient, points, id) in self.busses.items():
                    for i in range(len(points)):
                        if points[i] == self.firstPointPos:
                            if points[i] not in self.tokenBusPorts:
                                self.correctNodeSelect = True
                                self.firstNode = (id, i)
                                # self.tokenBusPorts.append(points[i])
                for trafo, (point, ori, hands) in self.trafos.items():
                    for i in range(len(hands)):
                        if hands[i] == self.firstPointPos:
                            if hands[i] not in self.tokenTrafoHands:
                                self.correctNodeSelect = True
                                self.firstNode = (trafo, i)
                                self.tokenTrafoHands.append(hands[i])

            # Placing second Connection
            elif self.insertLineMode and self.firstNode is not None:
                self.secondPointPos = self.snap(event.pos())
                print('firstNode', self.paths)
                connection1, firstPoint = self.firstNode
                self.tempPath.append(self.secondPointPos)
                # print(self.tempPath)
                # print('Point added: ', self.tempPath)
                for bus, (point, capacity, orient, points, id) in self.busses.items():
                    connection2 = id 
                    for i in range(len(points)):
                        if points[i] == self.secondPointPos and points[i] not in self.tokenBusPorts:
                            if connection1 != connection2 :
                                # Direct Line
                                self.tempPath.pop() 
                                tempPath = deepcopy(self.tempPath)
                                line = (connection1, connection2, firstPoint, i, tempPath) 
                                revLine = (connection2, connection1, firstPoint, i, tempPath)
                                if line not in self.paths and revLine not in self.paths:
                                    self.paths.append(line)
                                    self.firstNode = None
                                    # self.tokenBusPorts.append(points[i])
                                    self.update()
                                    self.addLineDialog = AddLineDialog(self, connection1, connection2)
                                    self.addLineDialog.projectPath = self.projectPath
                                    self.addLineDialog.exec()
                                    self.tempPath.clear() 
                for trafo, (point, ori, hands) in self.trafos.items():
                    connection2 = trafo
                    for i in range(len(hands)):
                        if hands[i] == self.secondPointPos and self.secondPointPos not in self.tokenTrafoHands:
                            if connection1 != connection2 and self.firstPointPos not in self.tokenTrafoHands:
                                self.tempPath.pop() 
                                tempPath = deepcopy(self.tempPath)
                                line = (connection1, connection2, firstPoint, i, tempPath) 
                                revLine = (connection2, connection1, firstPoints, i, tempPath)
                                if line not in self.paths and revLine not in self.paths:
                                    self.tokenTrafoHands.append(hands[i])
                                    self.paths.append(line)
                                    self.firstNode = None
                                    self.update()
                                    self.addLineDialog = AddLineDialog(self, connection1, connection2)
                                    self.addLineDialog.projectPath = self.projectPath
                                    self.addLineDialog.exec()
                                    self.tempPath.clear() 

        # Clicked on an existing bus
        if event.button() == Qt.MouseButton.LeftButton and self.insertBusMode == False and self.insertLineMode == False:
            pos = self.snap(event.pos())
            x = pos.x()
            y = pos.y()
            editedBus = None
            editedTuple = None 
            for bus, bigTuple in self.busses.items():
                point, capacity, orient, points, id = bigTuple
                busX = point.x()
                busY = point.y()
                if orient == '-90':
                    if x == busX and y in range(busY, busY + capacity * self.dist):
                        self.initEditBox(bus, point)
                        editedBus = bus
                        editedTuple = bigTuple
                elif orient == '0':
                    if x in range(busX, busX + capacity * self.dist) and y == busY:
                        self.initEditBox(bus, point)
                        editedBus = bus
                        editedTuple = bigTuple
                elif orient == '90':
                    if x == busX and y in range(busY - capacity * self.dist, busY):
                        self.initEditBox(bus, point)
                        editedBus = bus
                        editedTuple = bigTuple
                elif orient == '180':
                    if x in range(busX - capacity * self.dist, busX) and y == busY:
                        self.initEditBox(bus, point)
                        editedBus = bus
                        editedTuple = bigTuple
            if editedBus is not None:
                print('paths: ',self.paths)
                editedBus = self.editedBusses(editedBus, editedTuple)
                del self.busses[editedBus]
                editedBus = None
                self.update()

        # Hand mode pressed
        if event.button() == Qt.MouseButton.LeftButton and self.handMode:
            self.handActivatedPos = self.snap(event.pos())

        # Left + Alt: Removes Node
        if event.button() == Qt.MouseButton.RightButton and QApplication.keyboardModifiers() == Qt.KeyboardModifier.AltModifier:
            pos = self.snap(event.pos())
            x = pos.x()
            y = pos.y()
            for bus, (point, capacity, orient, points, id) in self.busses.items():
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
                    self.setBusDict(bus, point, capacity, orient, id)
                    self.update()


        if event.button() == Qt.MouseButton.RightButton:
            pos = self.snap(event.pos())
            x = pos.x()
            y = pos.y()
            for bus, (point, capacity, orient, points, id) in self.busses.items():
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
                self.setBusDict(bus, point, capacity, orient, id)
                self.update()

    def withinBounds(self, x, y, busX, busY, dist, capacity, orient):
        if orient == '-90':
            return busX - dist <= x < busX + dist and busY - dist <= y < busY + capacity * dist
        elif orient == '0':
            return busX - dist <= x < busX + capacity * dist and busY - dist <= y < busY + dist
        elif orient == '90':
            return busX - dist <= x < busX + dist and busY - capacity * dist <= y < busY + dist
        elif orient == '180':
            return busX - capacity * dist <= x < busX and busY - dist <= y < busY + dist
        return False

    def wheelEvent(self, event) -> None:
        pos = self.snap(self.currentMousePos)
        x = pos.x()
        y = pos.y()
        for bus, (point, capacity, orient, points, id) in self.busses.items():
            busX, busY = point.x(), point.y()
            if event.angleDelta().y() > 0:  # Scroll up
                nextOrient = self.orientations[(self.orientations.index(orient) + 1) % len(self.orientations)]
            elif event.angleDelta().y() < 0:  # Scroll down
                nextOrient = self.orientations[(self.orientations.index(orient) - 1) % len(self.orientations)]
            else:
                continue

            if self.withinBounds(x, y, busX, busY, self.dist, capacity, orient):
                orient = nextOrient  # Update orientation

                self.setBusDict(bus, point, capacity, orient, id)
                self.update()

        if self.insertTrafoMode or self.insertBusMode:
            if self.insertingOrient == '-90':
                self.insertingOrient = '0'
            else:
                self.insertingOrient = '-90'

        self.update()

    def setOffset(self, offset: QPoint):
        # Sets an offset on the grid to simulate a move.
        self.offSet = QPoint(int(offset.x() % self.dist),
                               int(offset.y() % self.dist))

    def paintEvent(self, event: QPaintEvent) -> None:
        # Set Pen for Grid painting
        gridPen = QPen()
        gridPen.setWidth(self.gridWidth)
        gridPen.setColor(self.lineColor)
        painter = QPainter()
        painter.begin(self)
        painter.setPen(gridPen)

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
        color = QColor(255, 255, 255, int(255 * 0.1))  # with 10% transparency
        symbolPen = QPen()
        symbolPen.setWidth(self.lineWidth)
        symbolPen.setColor(self.blue)
        dotPen = QPen()
        dotPen.setColor(self.highLightWhite)
        dotPen.setWidth(self.txtWidth)
        txtPen = QPen()
        txtPen.setWidth(self.txtWidth)
        txtPen.setColor(color)

        if highLightedPoint is not None:
            xHigh = highLightedPoint.x()
            yHigh = highLightedPoint.y()
            if self.insertBusMode or self.insertTrafoMode:
                painter.setRenderHint(QPainter.RenderHint.Antialiasing)

                # Set the fill color with 20% transparency
                painter.setBrush(color)
                painter.setPen(Qt.PenStyle.NoPen)  # No border for the rectangle   
                painter.drawRect(xHigh - self.dist, yHigh - self.dist, 2 * self.dist, 2 * self.dist)
                painter.setPen(symbolPen)

                if self.insertBusMode:
                    painter.setPen(symbolPen)
                    painter.drawLine(xHigh, yHigh - self.dist, xHigh, yHigh + self.dist)

                    txt = 'Left Click to Drop Bus'
                    textRect = painter.fontMetrics().boundingRect(txt)
                    textWidth = textRect.width()
                    textHeight = textRect.height()
                    txtPointX = xHigh - (textWidth // 2)
                    txtPointY = yHigh + (self.dist) + (textHeight)
                    txtPoint = QPoint(xHigh, yHigh - self.dist)
                    painter.setPen(txtPen)
                    txtPoint = QPoint(txtPointX, txtPointY)
                    painter.drawText(txtPoint, txt)

                if self.insertTrafoMode:
                    gridPen.setColor(self.yellow)
                    painter.setPen(gridPen)
                    if self.insertingOrient == '-90':
                        painter.drawLine(xHigh, yHigh - self.dist, xHigh, yHigh - 20)
                        painter.drawLine(xHigh, yHigh + self.dist, xHigh, yHigh + 20)
                        symbolPen.setColor(self.yellow)
                        painter.setPen(symbolPen)
                        painter.drawEllipse(xHigh - 12, yHigh - 12 - 7, 24, 24)
                        painter.drawEllipse(xHigh - 12, yHigh - 12 + 7, 24, 24)
                        painter.setPen(dotPen)
                        painter.drawEllipse(xHigh - 1, yHigh - self.dist, 2, 2)
                        painter.drawEllipse(xHigh - 1, yHigh + self.dist, 2, 2)
                    else:
                        painter.drawLine(xHigh - self.dist, yHigh, xHigh - 20, yHigh)
                        painter.drawLine(xHigh + self.dist, yHigh, xHigh + 20, yHigh)
                        symbolPen.setColor(self.yellow)
                        painter.setPen(symbolPen)
                        painter.drawEllipse(xHigh - 12 - 7, yHigh - 12, 24, 24)
                        painter.drawEllipse(xHigh - 12 + 7, yHigh - 12, 24, 24)
                        painter.setPen(dotPen)
                        painter.drawEllipse(xHigh - self.dist, yHigh - 1, 2, 2)
                        painter.drawEllipse(xHigh + self.dist, yHigh - 1, 2, 2)

            if not self.insertTrafoMode:
                painter.setPen(dotPen)
                painter.drawEllipse(xHigh - 1, yHigh - 1, 2, 2)

            for bus, (point, capacity, orient, points, _) in self.busses.items():
                if self.highLightedPoint == point or self.highLightedPoint in points:
                    # Set the fill color with 20% transparency
                    painter.setBrush(color)
                    painter.setPen(Qt.PenStyle.NoPen)  # No border for the rectangle   
                    if orient == '-90':
                        painter.drawRect(point.x() - self.dist, point.y() - self.dist,
                                         2 * self.dist, (capacity + 1) * self.dist)
                    elif orient == '0':
                        painter.drawRect(point.x() - self.dist, point.y() - self.dist,
                                         (capacity + 1) * self.dist, 2 * self.dist)
                    elif orient == '90':
                        painter.drawRect(point.x() - self.dist, point.y() - (capacity) * self.dist,
                                         2 * self.dist, (capacity + 1) * self.dist)
                    elif orient == '180':
                        painter.drawRect(point.x() - capacity * self.dist, point.y() - self.dist,
                                         (capacity + 1) * self.dist, 2 * self.dist)
                else:
                    painter.setBrush(Qt.BrushStyle.NoBrush)

            for trafo, (point, ori, hands) in self.trafos.items():
                if self.highLightedPoint == point or self.highLightedPoint in hands:
                    # Set the fill color with 20% transparency
                    painter.setBrush(color)
                    painter.setPen(Qt.PenStyle.NoPen)  # No border for the rectangle   
                    painter.drawRect(point.x() - self.dist, point.y() - self.dist, 2 * self.dist, 2 * self.dist)
                else: 
                    painter.setBrush(Qt.BrushStyle.NoBrush)

        # Drawing all the busbars here
        for bus, (point, capacity, orient, points, _) in self.busses.items():
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
            self.update()

        # Drawing all the transfos here
        for trafo, (point, ori, hands) in self.trafos.items():
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            gridPen.setColor(self.yellow)
            painter.setPen(gridPen)
            traX = point.x()
            traY = point.y()
            gridPen.setColor(self.yellow)
            painter.setPen(gridPen)
            if ori == '-90':
                painter.drawLine(traX, traY - self.dist, traX, traY - 20)
                painter.drawLine(traX, traY + self.dist, traX, traY + 20)
                symbolPen.setColor(self.yellow)
                painter.setPen(symbolPen)
                painter.drawEllipse(traX - 12, traY - 12 - 7, 24, 24)
                painter.drawEllipse(traX - 12, traY - 12 + 7, 24, 24)
                painter.setPen(dotPen)
                painter.drawEllipse(traX - 1, traY - self.dist, 2, 2)
                painter.drawEllipse(traX - 1, traY + self.dist, 2, 2)
            else:
                painter.drawLine(traX - self.dist, traY, traX - 20, traY)
                painter.drawLine(traX + self.dist, traY, traX + 20, traY)
                symbolPen.setColor(self.yellow)
                painter.setPen(symbolPen)
                painter.drawEllipse(traX - 12 - 7, traY - 12, 24, 24)
                painter.drawEllipse(traX - 12 + 7, traY - 12, 24, 24)
                painter.setPen(dotPen)
                painter.drawEllipse(traX - self.dist, traY - 1, 2, 2)
                painter.drawEllipse(traX + self.dist, traY - 1, 2, 2)

        # Drawing Lines
        linePen = QPen()
        linePen.setWidth(self.gridWidth)
        linePen.setColor(self.yellow)
        painter.setPen(linePen)

        if len(self.paths) > 0:
            for line in self.paths:
                connection1, connection2, i1, i2, pathList = line
                firstNode, secondNode = None, None
                for bus, (point, capacity, orient, points, id) in self.busses.items():
                    if connection1 == id:
                        firstNode = points[i1]
                    elif connection2 == id:
                        secondNode = points[i2]
                for trafo, (point, ori, hands) in self.trafos.items():
                    if connection1 == trafo:
                        firstNode = hands[i1]
                    elif connection2 == trafo:
                        secondNode = hands[i2]

                if firstNode is not None and secondNode is not None:
                    self.update()
                    if len(pathList) == 0:
                        painter.drawLine(firstNode.x(), firstNode.y(), secondNode.x(), secondNode.y())
                    else:
                        painter.drawLine(firstNode.x(), firstNode.y(), pathList[0].x(), pathList[0].y())
                        for i in range(len(pathList) - 1):
                            painter.drawLine(pathList[i].x(), pathList[i].y(), pathList[i + 1].x(), pathList[i + 1].y())
                        painter.drawLine(pathList[-1].x(), pathList[-1].y(), secondNode.x(), secondNode.y())

        # Doesn't matter to path finding
        if self.insertLineMode and self.correctNodeSelect:
            if self.firstNode is not None:
                connection, i = self.firstNode
                print(self.firstNode)
                for bus, (point, capacity, orient, points, id) in self.busses.items():
                    if connection == id:
                        firstNode = points[i]
                for trafo, (point, ori, hands) in self.trafos.items():
                    if connection == trafo:
                        firstNode = hands[i]
                mousePos = self.snap(self.currentMousePos)
                pathList = self.tempPath
                if len(pathList) == 0:
                    painter.drawLine(firstNode.x(), firstNode.y(), mousePos.x(), mousePos.y())
                else:
                    painter.drawLine(firstNode.x(), firstNode.y(), pathList[0].x(), pathList[0].y())
                    for i in range(len(pathList) - 1):
                        painter.drawLine(pathList[i].x(), pathList[i].y(), pathList[i + 1].x(), pathList[i + 1].y())
                    painter.drawLine(pathList[-1].x(), pathList[-1].y(), mousePos.x(), mousePos.y())

        else:
            return

        painter.end()

    def setBusDict(self, name: str, pos: QPoint, cap: int, ori: str, id: int):
        points = []
        mainX = pos.x()
        mainY = pos.y()
        for i in range(0, cap):
            if ori == '0':
                newPointX = mainX + (i * self.dist)
                newPointY = mainY
                points.append(QPoint(newPointX, newPointY))
            elif ori == '-90':
                newPointX = mainX 
                newPointY = mainY + (i * self.dist)
                points.append(QPoint(newPointX, newPointY))
            elif ori == '90':
                newPointX = mainX 
                newPointY = mainY - (i * self.dist)
                points.append(QPoint(newPointX, newPointY))
            elif ori == '180':
                newPointX = mainX - (i * self.dist)
                newPointY = mainY
                points.append(QPoint(newPointX, newPointY))
        busTuple = (pos, cap, ori, points, id)
        self.busses[name] = busTuple

    def setTrafoDict(self, pos: QPoint) -> None:
        self.trafoCenters.append(pos)
        x = pos.x()
        y = pos.y()
        self.trafoCounter += 1
        id = self.trafoCounter
        ori = self.insertingOrient
        if ori == '0':
            hands = (QPoint(x - self.dist, y), QPoint(x + self.dist, y))
        else:
            hands = (QPoint(x, y - self.dist), QPoint(x, y + self.dist))
        trafoTuple = (pos, ori, hands)
        self.trafos[id] = trafoTuple
        print(self.trafos)

    def initEditBox(self, busName: str, point: QPoint) -> None:
        csvPath = self.projectPath + '/Buses.csv'
        self.editBusDialog = EditBusDialog(self)
        self.editBusDialog.projectPath = self.projectPath
        with open(csvPath) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if busName == row['name']:
                    self.editBusDialog.busPos = point
                    self.editBusDialog.busId = row['id']
                    self.editBusDialog.nameInput.setText(row['name'])
                    self.editBusDialog.previousName = row['name']
                    self.editBusDialog.vMagInput.setText(row['vMag'])
                    self.editBusDialog.vAngInput.setText(row['vAng'])
                    self.editBusDialog.pInput.setText(row['P'])
                    self.editBusDialog.qInput.setText(row['Q'])
                    self.editBusDialog.exec()

    def editedBusses(self, editedBus: str, bigTuple: tuple) -> None:
        if self.editBusDialog is not None:
            self.busses[self.editBusDialog.nameInput.text()] = bigTuple
            newPaths = []
            for line in self.paths:
                bus1Name, bus2Name, i1, i2, pathList = line
                if bus1Name == editedBus:
                    bus1Name = self.editBusDialog.nameInput.text()
                elif bus2Name == editedBus:
                    bus2Name = self.editBusDialog.nameInput.text()
                line = bus1Name, bus2Name, i1, i2, pathList
                newPaths.append(line)
            self.paths = newPaths
        else:
            self.busses[editedBus] = bigTuple
        return editedBus

    def openRunDialog(self) -> None:
        self.runSimDialog = RunSimDialog(self, self.freq, self.sBase)
        self.runSimDialog.projectPath = self.projectPath
        self.runSimDialog.exec()
