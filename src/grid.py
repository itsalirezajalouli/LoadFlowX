# Imports
import os
import csv
import json
import math
from copy import deepcopy
from PyQt6.QtCore import QPoint, Qt, QEvent
from bus_dialogs import AddBusDialog, EditBusDialog
from line_dialogs import AddLineDialog
from gen_dialogs import AddGenDialog
from load_dialogs import AddLoadDialog
from slack_dialogs import AddSlackDialog
from run_dialogs import RunSimDialog
from theme import DiscordPalette as theme
from PyQt6.QtGui import QColor, QPaintEvent, QPen, QPainter, QBrush, QPolygon
from PyQt6.QtWidgets import QApplication, QWidget
from trafo_dialogs import AddTrafoDialog
from csv_viewer import CsvViewer

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
        self.currentMousePos = QPoint(400, 400)
        self.insertingOrient = '-90'
        self.handActivatedPos = None

        # State Properties
        self.selectMode = False
        self.handMode = False

        self.insertBusMode = False
        self.insertLineMode = False
        self.insertTrafoMode = False
        self.insertGenMode = False
        self.insertLoadMode = False
        self.insertSlackMode = False 

        self.correctNodeSelect = False 
        self.spacePressed = False  # Track the state of the Space key

        # Dialogs
        self.addBusDialog = None
        self.editBusDialog = None
        self.addLineDialog = None
        self.addTrafoDialog = None
        self.runSimDialog = None
        self.csvViewer = None
        
        # Data Properties
        self.projectPath = None
        self.busCsvPath = None
        self.guiCsvPath = None
        self.busCounter = 0
        self.trafoCounter = 0
        self.genCounter = 0
        self.loadCounter = 0
        self.slackCounter = 0
        self.firstNode = None
        self.busses = {}
        self.trafos = {}
        self.gens = {}
        self.loads = {}
        self.slacks = {}
        self.paths = []
        self.tokenBusPorts = []
        self.tokenTrafoHands = []
        self.tokenGenHands = []
        self.tokenLoadHands = []
        self.tokenSlackHands = []
        self.xDists = []
        self.tempPath = []
        self.firstType = None
        self.drawingParams = None

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
            newPaths = []
            for p in self.paths:
                connection1, connection2, fp, i, tempPath, firstNodeType, secNodeType = p
                newTp = []
                for tp in tempPath:
                    tp = self.snap(QPoint(tp.x() + xDiff, tp.y() + yDiff))
                    newTp.append(tp)
                p = connection1, connection2, fp, i, newTp, firstNodeType, secNodeType
                newPaths.append(p)
            self.paths = newPaths
            self.updateBusCSVGuiParams()
            self.updateGuiElementsCSV()
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
        if event.button() == Qt.MouseButton.LeftButton:
            self.leftMouseHold = True
            # Placing a bus
            if self.insertBusMode:
                pos = self.snap(event.pos())
                defaultCapacity = 1
                self.addBusDialog = AddBusDialog(self)
                self.addBusDialog.busPos = pos
                self.busCounter += 1
                self.addBusDialog.busId = self.busCounter
                self.addBusDialog.projectPath = self.projectPath
                self.addBusDialog.orient = self.insertingOrient 
                self.addBusDialog.capacity = defaultCapacity 
                self.addBusDialog.points = [] 
                self.addBusDialog.exec()
                busName = self.addBusDialog.nameInput.text()
                id = self.busCounter
                self.setBusDict(busName, pos, defaultCapacity, self.insertingOrient, id)

            # Placing a Transformator 
            if self.insertTrafoMode:
                pos = self.snap(event.pos())
                self.trafoCounter += 1
                ori = self.insertingOrient
                id = self.trafoCounter
                self.setTrafoDict(pos, ori, id, 0, 0)
                self.update()

            # Placing a gen 
            if self.insertGenMode:
                pos = self.snap(event.pos())
                self.genCounter += 1
                ori = self.insertingOrient
                id = self.genCounter
                self.setGenDict(id, pos, ori)
                self.update()

            # Placing a load 
            if self.insertLoadMode:
                pos = self.snap(event.pos())
                self.loadCounter += 1
                ori = self.insertingOrient
                id = self.loadCounter
                self.setLoadDict(id, pos, ori)
                self.update()

            # Placing a slack 
            if self.insertSlackMode:
                pos = self.snap(event.pos())
                self.slackCounter += 1
                ori = self.insertingOrient
                id = self.slackCounter
                self.setSlackDict(id, pos, ori)
                self.update()
            
            # Placing Line: First Connection
            if self.insertLineMode and self.firstNode is None:
                # from a bus
                self.firstPointPos = self.snap(event.pos())
                for bus, (point, capacity, orient, points, id) in self.busses.items():
                    for i in range(len(points)):
                        if points[i] == self.firstPointPos:
                            if points[i] not in self.tokenBusPorts:
                                self.correctNodeSelect = True
                                self.firstNode = (id, i, 'bus')
                                # self.tokenBusPorts.append(points[i])

                # from a transformer 
                for trafo, (point, ori, hands, bus1, bus2) in self.trafos.items():
                    for i in range(len(hands)):
                        if hands[i] == self.firstPointPos:
                            if hands[i] not in self.tokenTrafoHands:
                                self.correctNodeSelect = True
                                self.firstNode = (trafo, i, 'trafo')
                                self.tokenTrafoHands.append(hands[i])

                # from a generator
                for gen, (point, ori, hand) in self.gens.items():
                    if hand == self.firstPointPos:
                        if hand not in self.tokenGenHands:
                            self.correctNodeSelect = True
                            self.firstNode = (gen, 0, 'gen')
                            self.tokenGenHands.append(hand)

                # from a load 
                for load, (point, ori, hand) in self.loads.items():
                    if hand == self.firstPointPos:
                        if hand not in self.tokenLoadHands:
                            self.correctNodeSelect = True
                            self.firstNode = (load, 0, 'load')
                            self.tokenLoadHands.append(hand)

                # from a slack 
                for slack, (point, ori, hand) in self.slacks.items():
                    if hand == self.firstPointPos:
                        if hand not in self.tokenSlackHands:
                            self.correctNodeSelect = True
                            self.firstNode = (slack, 0, 'slack')
                            self.tokenSlackHands.append(hand)

            # Placing second Connection
            elif self.insertLineMode and self.firstNode is not None:
                self.secondPointPos = self.snap(event.pos())
                connection1, firstPoint, firstNodeType = self.firstNode
                self.tempPath.append(self.secondPointPos)
                # print(self.tempPath)
                print('Point added: ', self.secondPointPos)
                # to a bus
                for bus, (point, capacity, orient, points, id) in self.busses.items():
                    for i in range(len(points)):
                        if points[i] == self.secondPointPos and points[i] not in self.tokenBusPorts:
                            connection2 = id 
                            # Direct Line
                            self.tempPath.pop() 
                            tempPath = deepcopy(self.tempPath)
                            line = (connection1, connection2, firstPoint, i, tempPath,
                                    firstNodeType, 'bus') 
                            revLine = (connection2, connection1, firstPoint, i, tempPath,
                                       firstNodeType, 'bus')
                            if firstNodeType == 'bus':
                                if line not in self.paths and revLine not in self.paths:
                                    self.paths.append(line)
                                    self.firstNode = None
                                    # self.tokenBusPorts.append(points[i])
                                    self.update()
                                    self.addLineDialog = AddLineDialog(self, connection1, connection2)
                                    self.addLineDialog.projectPath = self.projectPath
                                    self.addLineDialog.exec()
                                    self.updateGuiElementsCSV()
                                    self.tempPath.clear() 

                            if firstNodeType == 'trafo':
                                for trafo, (point, ori, hands, bus1, bus2) in self.trafos.items():
                                    if bus1 == 0:
                                        if connection1 == trafo:
                                            self.paths.append(line)
                                            self.firstNode = None
                                            # self.tokenBusPorts.append(points[i])
                                            trafoTuple = (point, ori, hands, connection2, 0)
                                            self.trafos.update({connection1: trafoTuple})
                                            self.update()
                                    else:
                                        if connection1 == trafo:
                                            self.paths.append(line)
                                            self.firstNode = None
                                            # self.tokenBusPorts.append(points[i])
                                            trafoTuple = (point, ori, hands, bus1, connection2)
                                            self.trafos.update({connection1: trafoTuple})
                                            self.update()
                                            print(self.trafos)
                                            self.addTraffoDialog = AddTrafoDialog(self)
                                            self.addTraffoDialog.trafoPos = point
                                            self.addTraffoDialog.trafoId = trafo
                                            self.addTraffoDialog.bus1Id = bus1
                                            self.addTraffoDialog.bus2Id = connection2
                                            self.addTraffoDialog.projectPath = self.projectPath
                                            self.addTraffoDialog.exec()
                                            self.update()

                            if firstNodeType == 'gen':
                                self.tokenGenHands.append(self.firstPointPos)
                                self.paths.append(line)
                                self.firstNode = None
                                self.update()
                                self.addGenDialog = AddGenDialog(self, connection1)
                                self.addGenDialog.projectPath = self.projectPath
                                self.addGenDialog.exec()
                                self.updateGuiElementsCSV()
                                self.tempPath.clear() 

                            if firstNodeType == 'load':
                                self.tokenLoadHands.append(self.firstPointPos)
                                self.paths.append(line)
                                self.firstNode = None
                                self.update()
                                self.addLoadDialog = AddLoadDialog(self, connection1)
                                self.addLoadDialog.projectPath = self.projectPath
                                self.addLoadDialog.exec()
                                self.updateGuiElementsCSV()
                                self.tempPath.clear() 

                            if firstNodeType == 'slack':
                                self.tokenSlackHands.append(self.firstPointPos)
                                self.paths.append(line)
                                self.firstNode = None
                                self.update()
                                self.addSlackDialog = AddSlackDialog(self, connection1)
                                self.addSlackDialog.projectPath = self.projectPath
                                self.addSlackDialog.exec()
                                self.updateGuiElementsCSV()
                                self.tempPath.clear() 

                # to a transformer 
                updates = []
                for trafo, (point, ori, hands, bus1, bus2) in self.trafos.items():
                    for i in range(len(hands)):
                        if hands[i] == self.secondPointPos and self.secondPointPos not in self.tokenTrafoHands:
                            connection2 = trafo
                            self.tempPath.pop() 
                            tempPath = deepcopy(self.tempPath)
                            line = (connection1, connection2, firstPoint, i, tempPath,
                                    firstNodeType, 'trafo') 
                            revLine = (connection2, connection1, firstPoint, i, tempPath,
                                       firstNodeType, 'trafo')

                            if line not in self.paths and revLine not in self.paths:
                                print(line)
                                self.tokenTrafoHands.append(hands[i])
                                if firstNodeType == 'bus':
                                    if bus1 == 0:
                                        print('fuck')
                                        if connection2 == trafo:
                                            self.paths.append(line)
                                            self.firstNode = None
                                            self.tokenTrafoHands.append(hands[i])
                                            trafoTuple = (point, ori, hands, connection1, 0)
                                            updates.append((trafo, trafoTuple))  # Add to updates
                                            self.update()
                                    else:
                                        print('shit fuck')
                                        if connection2 == trafo:
                                            self.paths.append(line)
                                            self.firstNode = None
                                            # self.tokenBusPorts.append(hands[i])
                                            trafoTuple = (point, ori, hands, bus1, connection1)
                                            updates.append((trafo, trafoTuple))  # Add to updates
                                            self.update()
                                            print(self.trafos)
                                            self.addTraffoDialog = AddTrafoDialog(self)
                                            self.addTraffoDialog.trafoPos = point
                                            self.addTraffoDialog.trafoId = trafo
                                            self.addTraffoDialog.bus1Id = bus1
                                            self.addTraffoDialog.bus2Id = connection1
                                            self.addTraffoDialog.projectPath = self.projectPath
                                            self.addTraffoDialog.exec()
                                            self.update()
                                self.updateGuiElementsCSV()
                                self.firstNode = None
                                self.tempPath.clear() 
                if len(updates) > 0:
                    for key, value in updates:
                        self.trafos[key] = value

                # to a generator 
                for gen, (point, ori, hand) in self.gens.items():
                    if hand == self.secondPointPos and hand not in self.tokenGenHands:
                        if firstNodeType == 'bus':
                            connection2 = gen
                            self.tempPath.pop() 
                            tempPath = deepcopy(self.tempPath)
                            line = (connection1, connection2, firstPoint, 0, tempPath,
                                    firstNodeType, 'gen') 
                            revLine = (connection2, connection1, firstPoint, 0, tempPath,
                                       firstNodeType, 'gen')
                            if line not in self.paths and revLine not in self.paths:
                                self.tokenGenHands.append(hand)
                                self.paths.append(line)
                                self.firstNode = None
                                self.update()
                                self.addGenDialog = AddGenDialog(self, connection1)
                                self.addGenDialog.projectPath = self.projectPath
                                self.addGenDialog.exec()
                                self.updateGuiElementsCSV()
                                self.tempPath.clear() 

        # Double Clicked on an existing bus
        if event.type() == QEvent.Type.MouseButtonDblClick and event.button() == Qt.MouseButton.LeftButton and self.selectMode:
            pos = self.snap(event.pos())
            x = pos.x()
            y = pos.y()
            editedBus = None
            editedTuple = None 
            for bus, bigTuple in self.busses.items():
                point, capacity, orient, points, id = bigTuple
                busX = point.x()
                busY = point.y()
                if self.withinBounds(x, y, busX, busY, self.dist, capacity, orient):
                    self.initEditBox(bus, point)
                    editedBus = bus
                    editedTuple = bigTuple
            if editedBus is not None:
                # print('paths: ',self.paths)
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
                if self.withinBounds(x, y, busX, busY, self.dist, capacity, orient):
                    if (capacity - 2) != 0:
                        capacity -= 2
                self.setBusDict(bus, point, capacity, orient, id)
            self.update()
            self.updateBusCSVGuiParams()


        if event.button() == Qt.MouseButton.RightButton:
            pos = self.snap(event.pos())
            x = pos.x()
            y = pos.y()
            for bus, (point, capacity, orient, points, id) in self.busses.items():
                busX = point.x()
                busY = point.y()
                if self.withinBounds(x, y, busX, busY, self.dist, capacity, orient):
                    capacity += 1
                self.setBusDict(bus, point, capacity, orient, id)
                self.update()
            self.updateBusCSVGuiParams()

    def withinBounds(self, x, y, busX, busY, dist, capacity, orient):
        if x == busX and y == busY:
            return True
        elif orient == '-90':
            return busX - dist <= x < busX + dist and busY - dist <= y < busY + capacity * dist
        elif orient == '0':
            return busX - dist <= x < busX + capacity + dist and busY - dist <= y < busY + dist
        elif orient == '90':
            return busX - dist <= x < busX + dist and busY - capacity * dist <= y < busY + dist
        elif orient == '180':
            return busX - capacity * dist <= x < busX and busY - dist <= y < busY + dist
        return False

    def wheelEvent(self, event) -> None:
        '''
        Handles mouse wheel events for rotating components (busbars, transformers, generators)
        '''
        # Define orientations once as a class constant if not already defined
        ORIENTATIONS = ['-90', '0', '90', '180']
        
        pos = self.snap(self.currentMousePos)
        x, y = pos.x(), pos.y()
        
        # Helper function to get next orientation
        def getNextOrientation(currentOrient: str, scrollUp: bool) -> str:
            currentIndex = ORIENTATIONS.index(currentOrient)
            if scrollUp:
                return ORIENTATIONS[(currentIndex + 1) % len(ORIENTATIONS)]
            return ORIENTATIONS[(currentIndex - 1) % len(ORIENTATIONS)]
        
        # Handle component rotation
        componentUpdated = False
        
        # Check busbars
        for bus, (point, capacity, orient, points, id) in self.busses.items():
            busX, busY = point.x(), point.y()
            if self.withinBounds(x, y, busX, busY, self.dist, capacity, orient):
                newOrient = getNextOrientation(orient, event.angleDelta().y() > 0)
                self.setBusDict(bus, point, capacity, newOrient, id)
                componentUpdated = True
                self.updateBusCSVGuiParams()
                break
        
        # Check transformers
        if not componentUpdated:
            for trafo, (point, ori, hands, bus1, bus2) in self.trafos.items():
                trafX, trafY = point.x(), point.y()
                if x == trafX and y == trafY:
                    newOrient = getNextOrientation(ori, event.angleDelta().y() > 0)
                    self.setTrafoDict(pos, newOrient, trafo, bus1, bus2)
                    componentUpdated = True
                    break
        
        # Check generators
        if not componentUpdated:
            for gen, (point, orient, hand) in self.gens.items():
                genX, genY = point.x(), point.y()
                if x == genX and y == genY:
                    newOrient = getNextOrientation(orient, event.angleDelta().y() > 0)
                    self.setGenDict(gen, pos, newOrient)
                    componentUpdated = True
                    break

        # Check loads
        if not componentUpdated:
            for load, (point, orient, hand) in self.loads.items():
                ldX, ldY = point.x(), point.y()
                if x == ldX and y == ldY:
                    newOrient = getNextOrientation(orient, event.angleDelta().y() > 0)
                    self.setLoadDict(load, pos, newOrient)
                    componentUpdated = True
                    break

        # Check slacks 
        if not componentUpdated:
            for slack, (point, orient, hand) in self.slacks.items():
                slX, slY = point.x(), point.y()
                if x == slX and y == slY:
                    newOrient = getNextOrientation(orient, event.angleDelta().y() > 0)
                    self.setLoadDict(slack, pos, newOrient)
                    componentUpdated = True
                    break
        
        # Handle insertion mode orientation changes
        if self.insertTrafoMode or self.insertBusMode or self.insertGenMode or self.insertLoadMode \
            or self.insertSlackMode:
            self.insertingOrient = getNextOrientation(self.insertingOrient, event.angleDelta().y() > 0)
            print(self.insertingOrient)
        
        self.update()

    def setOffset(self, offset: QPoint):
        # Sets an offset on the grid to simulate a move.
        self.offSet = QPoint(int(offset.x() % self.dist),
                               int(offset.y() % self.dist))

    def paintEvent(self, event: QPaintEvent) -> None:
        # Set Pen for Grid painting
        self.gridPen = QPen()
        self.gridPen.setWidth(self.gridWidth)
        self.gridPen.setColor(self.lineColor)
        painter = QPainter()
        painter.begin(self)
        painter.setPen(self.gridPen)

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
                self.dotPen = QPen()
                self.dotPen.setColor(self.dotColor)
                painter.setPen(self.dotPen)
                painter.drawEllipse(x - 1, y - 1, 2, 2)
                x += self.dist
            y += self.dist
            x = 0

        # Drawing where the mouse is pointing to drop the item
        highLightedPoint = self.highLightedPoint
        color = QColor(255, 255, 255, int(255 * 0.1))  # with 10% transparency
        self.symbolPen = QPen()
        self.symbolPen.setWidth(self.lineWidth)
        self.symbolPen.setColor(self.blue)
        self.dotPen = QPen()
        self.dotPen.setColor(self.highLightWhite)
        self.dotPen.setWidth(self.txtWidth)
        self.txtPen = QPen()
        self.txtPen.setWidth(self.txtWidth)
        self.txtPen.setColor(color)

        if highLightedPoint is not None:
            xHigh = highLightedPoint.x()
            yHigh = highLightedPoint.y()
            if self.insertBusMode or self.insertTrafoMode or self.insertGenMode or self.insertLoadMode \
                or self.insertSlackMode:
                painter.setRenderHint(QPainter.RenderHint.Antialiasing)

                # Set the fill color with 20% transparency
                painter.setBrush(color)
                painter.setPen(Qt.PenStyle.NoPen)  # No border for the rectangle   
                painter.drawRect(xHigh - self.dist, yHigh - self.dist, 2 * self.dist, 2 * self.dist)
                painter.setPen(self.symbolPen)

                # Before Placing Bus
                if self.insertBusMode:
                    painter.setPen(self.symbolPen)
                    self.drawBusbar(painter, '', xHigh, yHigh, 1, self.insertingOrient)
                    # painter.drawLine(xHigh, yHigh - self.dist, xHigh, yHigh + self.dist)

                    txt = 'Left Click to Drop Bus'
                    textRect = painter.fontMetrics().boundingRect(txt)
                    textWidth = textRect.width()
                    textHeight = textRect.height()
                    txtPointX = xHigh - (textWidth // 2)
                    txtPointY = yHigh + (self.dist) + (textHeight)
                    txtPoint = QPoint(xHigh, yHigh - self.dist)
                    painter.setPen(self.txtPen)
                    txtPoint = QPoint(txtPointX, txtPointY)
                    painter.drawText(txtPoint, txt)

                # Before Placing Transformator 
                if self.insertTrafoMode:
                    self.gridPen.setColor(self.yellow)
                    painter.setPen(self.gridPen)
                    txt = 'Left Click to Drop Transformer'
                    textRect = painter.fontMetrics().boundingRect(txt)
                    textWidth = textRect.width()
                    textHeight = textRect.height()
                    txtPointX = xHigh - (textWidth // 2)
                    txtPointY = yHigh + (self.dist) + (textHeight)
                    txtPoint = QPoint(xHigh, yHigh - self.dist)
                    painter.setPen(self.txtPen)
                    txtPoint = QPoint(txtPointX, txtPointY)
                    painter.drawText(txtPoint, txt)

                    self.drawTrafo(painter, xHigh, yHigh, self.insertingOrient)
                    
                # before inserting generator
                if self.insertGenMode:
                    self.gridPen.setColor(self.blue)
                    painter.setPen(self.gridPen)
                    txt = 'Left Click to Drop Generator'
                    textRect = painter.fontMetrics().boundingRect(txt)
                    textWidth = textRect.width()
                    textHeight = textRect.height()
                    txtPointX = xHigh - (textWidth // 2)
                    txtPointY = yHigh - (self.dist) - (textHeight)
                    txtPoint = QPoint(xHigh, yHigh - self.dist)
                    painter.setPen(self.txtPen)
                    txtPoint = QPoint(txtPointX, txtPointY)
                    painter.drawText(txtPoint, txt)
                    self.drawGenerator(painter, xHigh, yHigh, self.insertingOrient)

                # before inserting load
                if self.insertLoadMode:
                    self.gridPen.setColor(self.blue)
                    painter.setPen(self.gridPen)
                    txt = 'Left Click to Drop Load'
                    textRect = painter.fontMetrics().boundingRect(txt)
                    textWidth = textRect.width()
                    textHeight = textRect.height()
                    txtPointX = xHigh - (textWidth // 2)
                    txtPointY = yHigh - (self.dist) - (textHeight)
                    txtPoint = QPoint(xHigh, yHigh - self.dist)
                    painter.setPen(self.txtPen)
                    txtPoint = QPoint(txtPointX, txtPointY)
                    painter.drawText(txtPoint, txt)
                    self.drawLoad(painter, xHigh, yHigh, self.insertingOrient)

                # before inserting slack
                if self.insertSlackMode:
                    self.gridPen.setColor(self.blue)
                    painter.setPen(self.gridPen)
                    txt = 'Left Click to Drop Slack'
                    textRect = painter.fontMetrics().boundingRect(txt)
                    textWidth = textRect.width()
                    textHeight = textRect.height()
                    txtPointX = xHigh - (textWidth // 2)
                    txtPointY = yHigh + (self.dist) + (textHeight)
                    txtPoint = QPoint(xHigh, yHigh - self.dist)
                    painter.setPen(self.txtPen)
                    txtPoint = QPoint(txtPointX, txtPointY)
                    painter.drawText(txtPoint, txt)

                    self.drawSlack(painter, xHigh, yHigh, self.insertingOrient)

            if not self.insertTrafoMode and not self.insertGenMode:
                painter.setPen(self.dotPen)
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

            for trafo, (point, ori, hands, bus1, bus2) in self.trafos.items():
                if self.highLightedPoint == point or self.highLightedPoint in hands:
                    # Set the fill color with 20% transparency
                    painter.setBrush(color)
                    painter.setPen(Qt.PenStyle.NoPen)  # No border for the rectangle   
                    painter.drawRect(point.x() - self.dist, point.y() - self.dist, 2 * self.dist, 2 * self.dist)
                else: 
                    painter.setBrush(Qt.BrushStyle.NoBrush)

        # Drawing all the busbars here
        for bus, (point, capacity, orient, points, _) in self.busses.items():
            self.drawBusbar(painter, bus, point.x(), point.y(), capacity, orient)
            self.update()

        # Drawing all the transfos here
        for trafo, (point, ori, hands, bus1, bus2) in self.trafos.items():
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            self.drawTrafo(painter, point.x(), point.y(), ori)

        # Drawing all the generators here
        for generator, (pos, ori, hand) in self.gens.items():
            self.drawGenerator(painter, pos.x(), pos.y(), ori)

        # Drawing all the loads here
        for load, (pos, ori, hand) in self.loads.items():
            self.drawLoad(painter, pos.x(), pos.y(), ori)

        # Drawing all the loads here
        for slack, (pos, ori, hand) in self.slacks.items():
            self.drawSlack(painter, pos.x(), pos.y(), ori)

        # Drawing all the lines
        linePen = QPen()
        linePen.setWidth(self.gridWidth)
        linePen.setColor(self.yellow)
        painter.setPen(linePen)

        if len(self.paths) > 0:
            for line in self.paths:
                connection1, connection2, i1, i2, pathList, firstNodeType, secNodeType = line
                firstNode, secondNode = None, None

                # from and to bus
                for bus, (point, capacity, orient, points, id) in self.busses.items():
                    # from bus
                    if firstNodeType == 'bus' and connection1 == id:
                        firstNode = points[i1]
                    # to bus
                    if secNodeType == 'bus' and connection2 == id:
                        if i2 == 0:
                            secondNode = point
                        else:
                            secondNode = points[i2]

                # from and to trafo
                for trafo, (point, ori, hands, bus1, bus2) in self.trafos.items():
                    # from trafo
                    if firstNodeType == 'trafo' and connection1 == trafo:
                        firstNode = hands[i1]
                    # to trafo
                    if secNodeType == 'trafo' and connection2 == trafo:
                        secondNode = hands[i2]

                # from and to gen
                for gen, (point, ori, hand) in self.gens.items():
                    # from gen
                    if firstNodeType == 'gen' and connection1 == gen:
                        firstNode = hand
                    # to gen
                    if secNodeType == 'gen' and connection2 == gen:
                        secondNode = hand

                # from and to load 
                for load, (point, ori, hand) in self.loads.items():
                    # from load 
                    if firstNodeType == 'load' and connection1 == load:
                        firstNode = hand 
                    # to load 
                    if secNodeType == 'load' and connection2 == load:
                        secondNode = hand

                # from and to slack 
                for slack, (point, ori, hand) in self.slacks.items():
                    # from slack 
                    if firstNodeType == 'slack' and connection1 == slack:
                        firstNode = hand 
                    # to slack 
                    if secNodeType == 'slack' and connection2 == slack:
                        secondNode = hand

                # Now that we know what are the connections from and to
                if firstNode is not None and secondNode is not None:
                    if len(pathList) == 0:
                        painter.drawLine(firstNode.x(), firstNode.y(), secondNode.x(),
                                         secondNode.y())
                    else:
                        painter.drawLine(firstNode.x(), firstNode.y(), pathList[0].x(),
                                         pathList[0].y())
                        for i in range(len(pathList) - 1):
                            painter.drawLine(pathList[i].x(), pathList[i].y(),
                                             pathList[i + 1].x(), pathList[i + 1].y())
                        painter.drawLine(pathList[-1].x(), pathList[-1].y(),
                                         secondNode.x(), secondNode.y())

        # still not chosen the destination of the line 
        if self.insertLineMode and self.correctNodeSelect:
            if self.firstNode is not None:
                connection, i, firstNodeType = self.firstNode
                # draw start connection from bus
                if firstNodeType == 'bus':
                    for bus, (point, capacity, orient, points, id) in self.busses.items():
                        if connection == id:
                            firstNode = points[i]

                # draw start connection from trafo
                if firstNodeType == 'trafo':
                    for trafo, (point, ori, hands, bus1, bus2) in self.trafos.items():
                        if connection == trafo:
                            firstNode = hands[i]

                # draw start connection from gen
                if firstNodeType == 'gen':
                    for gen, (pos, ori, hand) in self.gens.items():
                        if connection == gen:
                            firstNode = hand

                # draw start connection from load
                if firstNodeType == 'load':
                    for load, (pos, ori, hand) in self.loads.items():
                        if connection == load:
                            firstNode = hand

                # draw start connection from slack
                if firstNodeType == 'slack':
                    for slack, (pos, ori, hand) in self.slacks.items():
                        if connection == slack:
                            firstNode = hand

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

    def setTrafoDict(self, pos: QPoint, ori: str, id: int, bus1: int, bus2: int) -> None:
        x = pos.x()
        y = pos.y()
        if ori == '0':
            hands = (QPoint(x - self.dist, y), QPoint(x + self.dist, y))
        elif ori == '180':
            hands = (QPoint(x + self.dist, y), QPoint(x - self.dist, y))
        elif ori == '-90':
            hands = (QPoint(x, y - self.dist), QPoint(x, y + self.dist))
        elif ori == '90':
            hands = (QPoint(x, y + self.dist), QPoint(x, y - self.dist))
        trafoTuple = (pos, ori, hands, bus1, bus2)
        self.trafos[id] = trafoTuple
        # print(self.trafos)

    def setGenDict(self, id: int, pos: QPoint, ori: str) -> None:
        x = pos.x()
        y = pos.y()
        if ori == '0':
            hand = QPoint(x + self.dist, y) 
        elif ori == '180':
            hand = QPoint(x - self.dist, y)
        elif ori == '-90':
            hand = QPoint(x, y + self.dist)
        elif ori == '90':
            hand = QPoint(x, y - self.dist)
        genTuple = (pos, ori, hand)
        print(genTuple)
        self.gens[id] = genTuple

    def setLoadDict(self, id, pos, orient):
        self.loads[id] = (pos, orient, pos)

    def setSlackDict(self, id, pos, orient):
        self.slacks[id] = (pos, orient, pos)

    def initEditBox(self, busName: str, point: QPoint) -> None:
        self.editBusDialog = EditBusDialog(self)
        self.editBusDialog.projectPath = self.projectPath
        self.busCsvPath = self.projectPath + '/Buses.csv'
        with open(self.busCsvPath) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if busName == row['name']:
                    print(busName)
                    print(row['name'])
                    posList = json.loads(row['pos'].strip())
                    x, y = map(int, posList)
                    pos = QPoint(x, y)
                    pointsList = []
                    pointsArray = json.loads(row['points'].strip())
                    for px, py in pointsArray:
                        print(px, py)
                        point = QPoint(int(px), int(py))
                        pointsList.append(point)
                    print(pointsList)
                    self.editBusDialog.busPos = pos 
                    self.editBusDialog.busId = row['id']
                    self.editBusDialog.nameInput.setText(row['name'])
                    self.editBusDialog.previousName = row['name']
                    self.editBusDialog.vMagInput.setText(row['vMag'])
                    self.editBusDialog.vAngInput.setText(row['vAng'])
                    self.editBusDialog.pInput.setText(row['P'])
                    self.editBusDialog.qInput.setText(row['Q'])
                    self.editBusDialog.capacity = row['capacity'],
                    self.editBusDialog.orient = row['orient'],
                    self.editBusDialog.points = pointsList,
                    self.editBusDialog.exec()
                    self.updateBusCSVGuiParams()
                    self.update()

    def editedBusses(self, editedBus: str, bigTuple: tuple) -> str:
        if self.editBusDialog is not None:
            self.busses[self.editBusDialog.nameInput.text()] = bigTuple
            newPaths = []
            for line in self.paths:
                connection1, connection2, i1, i2, pathList, firstNodeType, secNodeType = line
                bus1Name, bus2Name, i1, i2, pathList, firstNodeType, secNodeType = line
                if connection1 == editedBus:
                    bus1Name = self.editBusDialog.nameInput.text()
                elif connection2 == editedBus:
                    bus2Name = self.editBusDialog.nameInput.text()
                line = bus1Name, bus2Name, i1, i2, pathList, firstNodeType, secNodeType
                newPaths.append(line)
            self.paths = newPaths
        else:
            self.busses[editedBus] = bigTuple
        return editedBus

    def updateBusCSVGuiParams(self) -> None:
        self.busCsvPath = self.projectPath + '/Buses.csv'
        if os.path.exists(self.busCsvPath):
            newBusList = []
            with open(self.busCsvPath) as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    for bus, (point, capacity, orient, points, id) in self.busses.items():
                        if row['name'] == bus:
                            row['pos'] = json.dumps((point.x(), point.y()))
                            row['capacity'] = capacity 
                            row['orient'] = orient
                            pointsList = []
                            for p in points:
                                tup = (p.x(), p.y())
                                pointsList.append(tup)
                            row['points'] = json.dumps(pointsList)
                    newBusList.append(row)

            with open(self.busCsvPath, 'w', newline = '') as file:
                writer = csv.DictWriter(file,fieldnames=['id', 'bType', 'vMag', 'vAng',
                                                         'P', 'Q', 'name', 'pos',
                                                         'capacity', 'orient', 'points'])
                writer.writeheader()
                writer.writerows(newBusList)
                print(f'-> Bus Data edited to {self.busCsvPath} successfuly.')

    def updateGuiElementsCSV(self) -> None:
        self.guiCsvPath = self.projectPath + '/GUI.csv'
        if os.path.exists(self.guiCsvPath):
            newPaths = []
            for p in self.paths:
                connection1, connection2, i1, i2, pathList, firstNodeType, secNodeType = p 
                newTp = []
                for p in pathList:
                    p = (p.x(), p.y())
                    newTp.append(p)
                bigTuple = connection1, connection2, i1, i2, newTp, firstNodeType, secNodeType 
                newPaths.append(bigTuple)
            data = {
                'dist': self.dist,
                'paths': json.dumps(newPaths)
            }
            with open(self.guiCsvPath, 'w', newline = '') as file:
                writer = csv.DictWriter(file, fieldnames=['dist','paths'])
                writer.writeheader()
                writer.writerow(data)
                print(f'-> GUI Data edited to {self.guiCsvPath} successfuly.')
            self.setDrawingParams()

    def loadGUI(self) -> None:
        self.busCsvPath = self.projectPath + '/Buses.csv'
        self.guiCsvPath = self.projectPath + '/GUI.csv'
        with open(self.busCsvPath) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                posList = json.loads(row['pos'].strip())
                x, y = map(int, posList)
                pos = QPoint(x, y)
                pointsList = []
                pointsArray = json.loads(row['points'].strip())
                for px, py in pointsArray:
                    pointsList.append(QPoint(int(px), int(py)))
                bigTuple = (pos, int(row['capacity']), row['orient'],
                            pointsList, int(row['id']))
                self.busses[row['name']] = bigTuple
                print('pa', pointsArray)
            print('-> busses: ',self.busses)
            self.update()

        with open(self.guiCsvPath) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.dist = int(row['dist'])
                pathArray = json.loads(row['paths'].strip())
                paths = []
                for p in pathArray:
                    connection1, connection2, i1, i2, pathList, firstNodeType, secNodeType = p 
                    newTp = []
                    for px, py in pathList:
                        p = QPoint(px, py)
                        newTp.append(p)
                    bigTuple = connection1, connection2, i1, i2, newTp, firstNodeType, secNodeType
                    paths.append(bigTuple)
                self.paths = paths
            self.setDrawingParams()
            self.update()

    def openRunDialog(self) -> str:
        self.runSimDialog = RunSimDialog(self, self.freq, self.sBase)
        self.runSimDialog.projectPath = self.projectPath
        self.runSimDialog.exec()
        return self.runSimDialog.activatedMethod

    def setDrawingParams(self) -> None:
        if self.dist == 16:
            self.drawingParams = [10, 6, 3, 12, 1, 1]
        elif self.dist == 32:
            self.drawingParams = [20, 12, 7, 24, 1, 2]
        elif self.dist == 64:
            self.drawingParams = [40, 24, 14, 48, 2, 4]
        elif self.dist == 128:
            self.drawingParams = [80, 48, 28, 96, 4, 8]
        elif self.dist == 256:
            self.drawingParams = [160, 96, 56, 192, 8, 16]

    def drawBusbar(self, painter, bus, x, y, capacity, orient):

        # Draw the main bus line
        self.symbolPen = QPen()
        self.symbolPen.setWidth(self.lineWidth)
        self.symbolPen.setColor(self.blue)
        painter.setPen(self.symbolPen)
        
        # Draw lines based on orientation
        if orient == '-90':
            painter.drawLine(x, y - self.dist, x, y + (capacity * self.dist))
        elif orient == '0':
            painter.drawLine(x - self.dist, y, x + (capacity * self.dist), y)
        elif orient == '90':
            painter.drawLine(x, y + self.dist, x, y - (capacity * self.dist))
        elif orient == '180':
            painter.drawLine(x + self.dist, y, x - (capacity * self.dist), y)

        # Draw the bus text label
        self.txtPen = QPen()
        self.txtPen.setWidth(self.txtWidth)
        self.txtPen.setColor(self.yellow)
        painter.setPen(self.txtPen)
        
        # Calculate text dimensions
        textRect = painter.fontMetrics().boundingRect(bus)
        textWidth = textRect.width()
        textHeight = textRect.height()
        
        # Position text based on orientation
        txtPointX = x - (textWidth // 2)
        txtPointY = y - self.dist - (textHeight // 2)
        
        if orient == '-90':
            txtPointY = y - self.dist - textHeight
        elif orient == '90':
            txtPointY = y + self.dist + textHeight
        elif orient == '0':
            txtPointX = x + ((capacity - 1) * self.dist // 2) - textWidth // 2
            txtPointY = y + self.dist + (textHeight // 2)
        elif orient == '180':
            txtPointX = x - ((capacity - 1) * self.dist // 2) - textWidth // 2
            txtPointY = y - self.dist - (textHeight // 2)
        
        txtPoint = QPoint(txtPointX, txtPointY)
        painter.drawText(txtPoint, bus)
        
        # Draw connection points
        self.dotPen = QPen()
        self.dotPen.setColor(self.highLightWhite)
        self.dotPen.setWidth(self.txtWidth)
        painter.setPen(self.dotPen)
        
        currentX, currentY = x, y
        
        # Draw dots based on orientation
        for _ in range(capacity):
            painter.drawEllipse(currentX - 1, currentY - 1, 2, 2)
            if orient == '-90':
                currentY += self.dist
            elif orient == '0':
                currentX += self.dist
            elif orient == '90':
                currentY -= self.dist
            elif orient == '180':
                currentX -= self.dist

    def drawGenerator(self, painter, x, y, orient):

        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        # Get drawing parameters
        lineOffset = self.drawingParams[0]
        ellipseRadius = self.drawingParams[1]
        ellipseYOffset = self.drawingParams[2]
        ellipseSize = self.drawingParams[3]
        dotRadius = self.drawingParams[4]
        dotSize = self.drawingParams[5]

        # Draw main ellipse
        self.symbolPen.setWidth(2)
        self.symbolPen.setColor(self.blue)
        painter.setPen(self.symbolPen)
        painter.drawEllipse(x - ellipseSize, y - ellipseSize, 2 * ellipseSize, 2 * ellipseSize)

        # Draw sine wave
        self.gridPen.setColor(self.yellow)
        self.gridPen.setWidth(1)
        painter.setPen(self.gridPen)
        waveWidth = ellipseSize
        waveHeight = ellipseYOffset
        waveSteps = 660
        stepSize = waveWidth / waveSteps
        sinePoints = []
        
        for i in range(waveSteps + 1):
            px = x - waveWidth // 2 + int(i * stepSize)
            py = y + int(math.sin(- 2 * math.pi * i / waveSteps) * waveHeight)
            sinePoints.append((px, py))
        
        for i in range(len(sinePoints) - 1):
            painter.drawLine(sinePoints[i][0], sinePoints[i][1], 
                            sinePoints[i + 1][0], sinePoints[i + 1][1])

        # Draw connection line and dot based on orientation
        self.symbolPen.setColor(self.blue)
        painter.setPen(self.symbolPen)
        
        lineLength = lineOffset // 2 - 4
        
        # Calculate line and dot positions based on orientation
        if orient == '-90':  # Bottom connection
            lineStartX = x
            lineStartY = y + ellipseSize
            lineEndX = x
            lineEndY = lineStartY + lineLength
            dotX = x - dotRadius
            dotY = lineEndY - dotRadius
            
        elif orient == '0':  # Right connection
            lineStartX = x + ellipseSize
            lineStartY = y
            lineEndX = lineStartX + lineLength
            lineEndY = y
            dotX = lineEndX - dotRadius
            dotY = y - dotRadius
            
        elif orient == '90':  # Top connection
            lineStartX = x
            lineStartY = y - ellipseSize
            lineEndX = x
            lineEndY = lineStartY - lineLength
            dotX = x - dotRadius
            dotY = lineEndY - dotRadius
            
        elif orient == '180':  # Left connection
            lineStartX = x - ellipseSize
            lineStartY = y
            lineEndX = lineStartX - lineLength
            lineEndY = y
            dotX = lineEndX - dotRadius
            dotY = y - dotRadius

        # Draw the connection line
        painter.drawLine(lineStartX, lineStartY, lineEndX, lineEndY)

        # Draw the connection dot
        self.dotPen.setWidth(4)
        painter.setPen(self.dotPen)
        painter.drawEllipse(dotX, dotY, dotSize, dotSize)

    def drawLoad(self, painter, x, y, orient):
        # Get drawing parameters
        triangleSize = self.drawingParams[3] # Using same size as generator ellipse
        lineLength = self.drawingParams[0] * 2 # Using same offset as generator
        dotSize = self.drawingParams[5]
        dotRadius = self.drawingParams[4]

        # Draw the connection dot first (at the main x,y point)
        self.dotPen.setWidth(4)
        painter.setPen(self.dotPen)
        dotX = x - dotRadius
        dotY = y - dotRadius
        painter.drawEllipse(dotX, dotY, dotSize, dotSize)

        # Set up triangle brush and pen
        # triangleBrush = QBrush(self.yellow)
        self.symbolPen.setWidth(2)
        self.symbolPen.setColor(self.yellow)
        painter.setPen(self.symbolPen)
        # painter.setBrush(triangleBrush)

        # Calculate positions based on orientation
        if orient == '-90':  # Triangle below dot
            lineStartX, lineStartY = x, y
            lineEndX, lineEndY = x, y + lineLength
            trianglePoints = [
                QPoint(x, lineEndY + triangleSize),  # Bottom point
                QPoint(x - triangleSize, lineEndY),  # Top left
                QPoint(x + triangleSize, lineEndY)   # Top right
            ]
            
        elif orient == '0':  # Triangle right of dot
            lineStartX, lineStartY = x, y
            lineEndX, lineEndY = x + lineLength, y
            trianglePoints = [
                QPoint(lineEndX + triangleSize, y),  # Right point
                QPoint(lineEndX, y - triangleSize),  # Top left
                QPoint(lineEndX, y + triangleSize)   # Bottom left
            ]
            
        elif orient == '90':  # Triangle above dot
            lineStartX, lineStartY = x, y
            lineEndX, lineEndY = x, y - lineLength
            trianglePoints = [
                QPoint(x, lineEndY - triangleSize),  # Top point
                QPoint(x - triangleSize, lineEndY),  # Bottom left
                QPoint(x + triangleSize, lineEndY)   # Bottom right
            ]
            
        elif orient == '180':  # Triangle left of dot
            lineStartX, lineStartY = x, y
            lineEndX, lineEndY = x - lineLength, y
            trianglePoints = [
                QPoint(lineEndX - triangleSize, y),  # Left point
                QPoint(lineEndX, y - triangleSize),  # Top right
                QPoint(lineEndX, y + triangleSize)   # Bottom right
            ]

        # Draw the connection line
        painter.drawLine(lineStartX, lineStartY, lineEndX, lineEndY)

        # Draw the triangle
        triangle = QPolygon(trianglePoints)
        painter.drawPolygon(triangle)

        # Reset the brush
        painter.setBrush(Qt.BrushStyle.NoBrush)

    def drawSlack(self, painter, x, y, orient):

        # Get drawing parameters
        rectSize = self.drawingParams[3]  # Using same size as generator ellipse
        lineLength = self.drawingParams[0] // 2 - 4  # Using same offset as generator
        dotSize = self.drawingParams[5]
        dotRadius = self.drawingParams[4]
        # Set up rectangle pen and brush
        self.symbolPen.setWidth(2)
        self.symbolPen.setColor(self.blue)
        painter.setPen(self.symbolPen)

        # Create diagonal pattern brush
        pattern = QBrush(self.yellow, Qt.BrushStyle.BDiagPattern)  # Diagonal pattern
        painter.setBrush(pattern)

        # Calculate positions based on orientation
        if orient == '-90':  # Rectangle below dot
            lineStartX, lineStartY = x, y
            lineEndX, lineEndY = x, y + lineLength
            rectX = x - rectSize
            rectY = lineEndY
            
        elif orient == '0':  # Rectangle right of dot
            lineStartX, lineStartY = x, y
            lineEndX, lineEndY = x + lineLength, y
            rectX = lineEndX
            rectY = y - rectSize
            
        elif orient == '90':  # Rectangle above dot
            lineStartX, lineStartY = x, y
            lineEndX, lineEndY = x, y - lineLength
            rectX = x - rectSize
            rectY = lineEndY - 2 * rectSize
            
        elif orient == '180':  # Rectangle left of dot
            lineStartX, lineStartY = x, y
            lineEndX, lineEndY = x - lineLength, y
            rectX = lineEndX - 2 * rectSize
            rectY = y - rectSize

        # Draw the connection line
        painter.drawLine(lineStartX, lineStartY, lineEndX, lineEndY)

        # Draw the rectangle
        painter.drawRect(rectX, rectY, 2 * rectSize, 2 * rectSize)

        # Draw the connection dot first (at the main x,y point)
        self.dotPen.setWidth(4)
        painter.setPen(self.dotPen)
        dotX = x - dotRadius
        dotY = y - dotRadius
        painter.drawEllipse(dotX, dotY, dotSize, dotSize)


        # Reset the brush
        painter.setBrush(Qt.BrushStyle.NoBrush)

    def drawTrafo(self, painter, x, y, orient):

        # Draw transformer based on orientation
        if orient in ['-90', '90']:
            self.symbolPen.setColor(self.yellow)
            painter.setPen(self.symbolPen)
            # Vertical lines
            painter.drawLine(x, y - self.dist, x, y - self.drawingParams[0])
            painter.drawLine(x, y + self.dist, x, y + self.drawingParams[0])
            
            # Circles
            painter.drawEllipse(
                x - self.drawingParams[1], y - self.drawingParams[1] - self.drawingParams[2], 
                self.drawingParams[3], self.drawingParams[3]
            )
            painter.drawEllipse(
                x - self.drawingParams[1], y - self.drawingParams[1] + self.drawingParams[2], 
                self.drawingParams[3], self.drawingParams[3]
            )
            
            # Dots
            painter.setPen(self.dotPen)
            painter.drawEllipse(
                x - self.drawingParams[4], y - self.dist, 
                self.drawingParams[5], self.drawingParams[5]
            )
            painter.drawEllipse(
                x - self.drawingParams[4], y + self.dist, 
                self.drawingParams[5], self.drawingParams[5]
            )
        
        elif orient in ['0', '180']:
            self.symbolPen.setColor(self.yellow)
            painter.setPen(self.symbolPen)
            # Horizontal lines
            painter.drawLine(x - self.dist, y, x - self.drawingParams[0], y)
            painter.drawLine(x + self.dist, y, x + self.drawingParams[0], y)
            
            # Circles
            painter.drawEllipse(
                x - self.drawingParams[1] - self.drawingParams[2], y - self.drawingParams[1], 
                self.drawingParams[3], self.drawingParams[3]
            )
            painter.drawEllipse(
                x - self.drawingParams[1] + self.drawingParams[2], y - self.drawingParams[1], 
                self.drawingParams[3], self.drawingParams[3]
            )
            
            # Dots
            painter.setPen(self.dotPen)
            painter.drawEllipse(
                x - self.dist, y - self.drawingParams[4], 
                self.drawingParams[5], self.drawingParams[5]
            )
            painter.drawEllipse(
                x + self.dist, y - self.drawingParams[4], 
                self.drawingParams[5], self.drawingParams[5]
            )

    def viewResultCsv(self, path: str) -> None:
        self.csvViewer = CsvViewer(self, path)
        self.csvViewer.exec()
