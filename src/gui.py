# Main GUI setup and window management

# Imports
from grid import Grid
from simulator import NetworkCreator
from PyQt6.QtCore import QSize
from start_window import StartUp
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QHBoxLayout, QMainWindow, QStatusBar, QVBoxLayout, QWidget, QToolButton

# Main Window Object
class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle('PSA II Project')
        self.setMinimumSize(800, 700)
        self.projectPath = None
        self.startUp = StartUp(self)
        self.buttSize = 26
        self.grid = None
        self.minZoom = 16
        self.maxZoom = 256
        if self.projectPath is None:
            self.startUp.exec()
            if not self.startUp.nameError:
                self.projectPath = self.startUp.projectPath

        # Menu Bar
        menu = self.menuBar()
        menu.setStyleSheet('''
            background-color: #2c2f33; color: #fff; ''')
        fileMenu = menu.addMenu('&File')
        editMenu = menu.addMenu('&Edit')
        loadFlowMenu = menu.addMenu('&Load Flow')
        viewMenu = menu.addMenu('&View')
        docMenu = menu.addMenu('&Docs')

        # New Project Button
        newButton = QAction('New Project', self)
        newButton.setStatusTip('Make a new project file')
        newButton.triggered.connect(self.makeProject)
        fileMenu.addAction(newButton)
        fileMenu.addSeparator()

        # Save Project Button
        saveProButton = QAction('Save Project', self)
        saveProButton.setStatusTip('Save this project as a file')
        saveProButton.triggered.connect(self.saveProject)
        fileMenu.addAction(saveProButton)
        fileMenu.addSeparator()

        # Open Project Button
        openProButton = QAction('Open Project', self)
        openProButton.setStatusTip('Open previous project files')
        openProButton.triggered.connect(self.openProject)
        fileMenu.addAction(openProButton)
        fileMenu.addSeparator()

        # Open Example Button
        openExButton = QAction('Open IEEE Example', self)
        openExButton .setStatusTip('Open IEEE Example files')
        openExButton.triggered.connect(self.openExample)
        fileMenu.addAction(openExButton)
        fileMenu.addSeparator()

        # Exit Button
        exitButton = QAction('Exit', self)
        exitButton.setStatusTip('Exit the program')
        exitButton.triggered.connect(self.exitProgram)
        fileMenu.addAction(exitButton)
        fileMenu.addSeparator()

        # Undo Button
        undoButton = QAction('Undo', self)
        undoButton.setStatusTip('Undo last action')
        undoButton.triggered.connect(self.undoLastAction)
        editMenu.addAction(undoButton)
        editMenu.addSeparator()

        # Redo Button
        redoButton = QAction('Redo', self)
        redoButton.setStatusTip('Redo last action')
        redoButton.triggered.connect(self.redoLastAction)
        editMenu.addAction(redoButton)
        editMenu.addSeparator()

        # Run Gauss-Siedel Button
        gsButton = QAction('Run Gauss-Siedel Method', self)
        gsButton.setStatusTip('Run Gauss Seidel Method of Load Flow')
        gsButton.triggered.connect(self.gsLoadFlow)
        loadFlowMenu.addAction(gsButton)
        loadFlowMenu.addSeparator()

        # Run Newton-Raphson Button
        nrButton = QAction('Run Newton-Raphson Method', self)
        nrButton.setStatusTip('Run Newton Raphson Method of Load Flow')
        nrButton.triggered.connect(self.nrLoadFlow)
        loadFlowMenu.addAction(nrButton)
        loadFlowMenu.addSeparator()

        # Run Fast-Decoupled Button
        fdButton = QAction('Run Fast-Decoupled Method', self)
        fdButton.setStatusTip('Run Fast-Decoupled Method of Load Flow')
        fdButton.triggered.connect(self.fdLoadFlow)
        loadFlowMenu.addAction(fdButton)
        loadFlowMenu.addSeparator()

        # Layouts
        self.mainLayout = QHBoxLayout()
        
        # View Toolbox
        self.barWidget = QWidget()
        self.barLayout = QVBoxLayout()
        self.barLayout.setSpacing(2)
        self.barWidget.setLayout(self.barLayout)

        self.viewToolbox = QWidget()
        self.viewToolbox.setStyleSheet('''
            background-color: #23272a;
            border: 1px solid #23272a;
            border-radius: 15px;
        ''')
        self.viewToolbox.setFixedWidth(52)
        self.viewToolbox.setFixedHeight(210)
        self.viewBar = QVBoxLayout()
        self.viewBar.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Run Toolbox
        self.runWidget = QWidget()
        self.runLayout = QVBoxLayout()
        self.runWidget.setLayout(self.runLayout)
        self.runWidget.setStyleSheet('''
            background-color: #23272a;
            border: 1px solid #23272a;
            border-radius: 15px;
        ''')
        self.runWidget.setFixedWidth(52)
        self.runWidget.setFixedHeight(55)

        # Symbols Toolbox
        self.symbolsToolbox = QWidget()
        self.toolBoxLayout = QVBoxLayout()
        self.symbolsToolbox.setLayout(self.toolBoxLayout)
        self.symbolsToolbox.setStyleSheet('''
            background-color:#23272a;
            border-radius: 15px;
        ''')
        self.symbolsToolbox.setFixedWidth(52)
        self.symbolsToolbox.setFixedHeight(260)
        self.toolBoxLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.normalStyle = '''
                QToolButton {
                    font-size: 24px;
                    background-color: #3b3e45;
                    border: 1px solid #3b3e45;
                    border-radius: 10px;
                    padding: 2px;
                    color: #ffffff;
                }
                QToolButton:hover {
                    background-color: #3b3e45;
                    border: 1px solid #7289da;
                }
                QToolButton:pressed {
                    background-color: #23272a;
                    border: 1px solid #FAA61A;
                }
                '''
        self.toggledStyle = '''
                QToolButton {
                    font-size: 24px;
                    background-color: #23272a;
                    border: 1px solid #FAA61A;
                    border-radius: 10px;
                    padding: 2px;
                    color: #ffffff;
                }
                QToolButton:hover {
                    background-color: #3b3e45;
                    border: 1px solid #7289da;
                }
                QToolButton:pressed {
                    background-color: #23272a;
                    border: 1px solid #FAA61A;
                }
                '''

        #   Edit button
        self.editGridButton = QToolButton()
        self.editGridButton.setIcon(QIcon('../icons/editGrid.png'))
        self.editGridButton.setIconSize(QSize(self.buttSize, self.buttSize))
        self.editGridButton.clicked.connect(self.setSelectMode)
        self.editGridButton.setStyleSheet(self.normalStyle)
        self.viewBar.addWidget(self.editGridButton)

        # move button
        self.moveButt = QToolButton()
        self.moveButt.setIcon(QIcon('../icons/move.png'))
        self.moveButt.setIconSize(QSize(self.buttSize, self.buttSize))
        self.moveButt.clicked.connect(self.hand)
        self.moveButt.setStyleSheet(self.normalStyle)
        self.viewBar.addWidget(self.moveButt)
        self.viewToolbox.setLayout(self.viewBar)

        #   erase button
        eraseGridButt = QToolButton()
        eraseGridButt.setIcon(QIcon('../icons/eraseGrid.png'))
        eraseGridButt.setIconSize(QSize(self.buttSize, self.buttSize))
        eraseGridButt.setStyleSheet(self.normalStyle)
        self.viewBar.addWidget(eraseGridButt)

        #   Zoom In button
        zoomInButt = QToolButton()
        zoomInButt.setIcon(QIcon('../icons/zoomIn.png'))
        zoomInButt.setIconSize(QSize(self.buttSize, self.buttSize))
        zoomInButt.setStyleSheet(self.normalStyle)
        zoomInButt.clicked.connect(self.zoomIn)
        self.viewBar.addWidget(zoomInButt)

        #   Zoom Out button
        self.zoomOutButt = QToolButton()
        self.zoomOutButt.setIcon(QIcon('../icons/zoomOut.png'))
        self.zoomOutButt.setIconSize(QSize(self.buttSize, self.buttSize))
        self.zoomOutButt.setStyleSheet(self.normalStyle)
        self.zoomOutButt.clicked.connect(self.zoomOut)
        self.viewBar.addWidget(self.zoomOutButt)

        #   Run button
        self.runButton = QToolButton()
        self.runButton.setIcon(QIcon('../icons/run.png'))
        self.runButton.setIconSize(QSize(self.buttSize, self.buttSize))
        self.runButton.setStyleSheet(self.normalStyle)
        self.runButton.clicked.connect(self.run)
        self.runLayout.addWidget(self.runButton)

        #   Add Bus button
        self.addBusButton = QToolButton()
        self.addBusButton.setIcon(QIcon('../icons/bus.png'))
        self.addBusButton.setIconSize(QSize(self.buttSize, self.buttSize))
        self.addBusButton.setStyleSheet(self.normalStyle)
        self.addBusButton.clicked.connect(self.addBus)
        self.toolBoxLayout.addWidget(self.addBusButton)

        self.barLayout.addWidget(self.viewToolbox)
        self.barLayout.addWidget(self.runWidget)
        self.barLayout.addWidget(self.symbolsToolbox)

        #   Add Line button
        self.addLineButton = QToolButton()
        self.addLineButton.setIcon(QIcon('../icons/line.png'))
        self.addLineButton.setIconSize(QSize(self.buttSize, self.buttSize))
        self.addLineButton.setStyleSheet(self.normalStyle)
        self.addLineButton.clicked.connect(self.addLine)
        self.toolBoxLayout.addWidget(self.addLineButton)

        #   Add Transformer button
        self.addTrafoButton = QToolButton()
        self.addTrafoButton.setIcon(QIcon('../icons/transformer.png'))
        self.addTrafoButton.setIconSize(QSize(self.buttSize, self.buttSize))
        self.addTrafoButton.setStyleSheet(self.normalStyle)
        self.addTrafoButton.clicked.connect(self.addTrafo)
        self.toolBoxLayout.addWidget(self.addTrafoButton)

        #   Add Generator button
        self.addGenButton = QToolButton()
        self.addGenButton.setIcon(QIcon('../icons/generator.png'))
        self.addGenButton.setIconSize(QSize(self.buttSize, self.buttSize))
        self.addGenButton.setStyleSheet(self.normalStyle)
        self.addGenButton.clicked.connect(self.addGen)
        self.toolBoxLayout.addWidget(self.addGenButton)

        #   Add Load button
        self.addLoadButton = QToolButton()
        self.addLoadButton.setIcon(QIcon('../icons/load.png'))
        self.addLoadButton.setIconSize(QSize(self.buttSize, self.buttSize))
        self.addLoadButton.setStyleSheet(self.normalStyle)
        self.addLoadButton.clicked.connect(self.addLoad)
        self.toolBoxLayout.addWidget(self.addLoadButton)

        #   Add slack button
        self.addSlackButton = QToolButton()
        self.addSlackButton.setIcon(QIcon('../icons/slack.png'))
        self.addSlackButton.setIconSize(QSize(self.buttSize, self.buttSize))
        self.addSlackButton.setStyleSheet(self.normalStyle)
        self.addSlackButton.clicked.connect(self.addSlack)
        self.toolBoxLayout.addWidget(self.addSlackButton)

        # Grid Layout
        self.grid = Grid(32)
        self.grid.projectPath = self.projectPath
        if self.startUp.loaded:
            self.grid.loadGUI()
        else: 
            self.grid.drawingParams = [20, 12, 7, 24, 1, 2]
        self.mainLayout.addWidget(self.grid, 12)
        self.mainLayout.addWidget(self.barWidget)
        
        # Main Widget
        widget = QWidget()
        widget.setLayout(self.mainLayout)
        widget.setStyleSheet('''
            background-color: #191b1d;
        ''')
        self.setCentralWidget(widget)

        # Status Bar
        statusBar = QStatusBar()
        self.setStatusBar(statusBar)
        statusBar.showMessage(
            'Power System Analysis II Project - Load Flow Methods GUI Simulator')
        statusBar.setStyleSheet('''
            color: #ffffff;
            background-color: #23272a;
        ''')

    def makeProject(self) -> None:
        pass

    def openProject(self) -> None:
        pass

    def saveProject(self) -> None:
        pass

    def openExample(self) -> None:
        pass

    def exitProgram(self) -> None:
        pass

    def undoLastAction(self) -> None:
        pass

    def redoLastAction(self) -> None:
        pass

    def gsLoadFlow(self) -> None:
        pass

    def nrLoadFlow(self) -> None:
        pass

    def fdLoadFlow(self) -> None:
        pass

    def run(self) -> None:
        # Takes chosen method from dialog chosen by user
        method = self.grid.openRunDialog()

        # Passing data csvs to the simulator
        busCsvPath = self.projectPath + '/Buses.csv'
        lineCSV = self.projectPath + '/Lines.csv'
        trafoCSV = self.projectPath + '/Trafos.csv'
        genCSV = self.projectPath + '/Gens.csv'
        loadCSV = self.projectPath + '/Loads.csv'
        slacksCSV = self.projectPath + '/Slacks.csv'

        # Run load flow Simulation
        nMaker = NetworkCreator(self.projectPath,
                                busCsvPath, lineCSV, trafoCSV, genCSV, loadCSV, slacksCSV)

        nMaker.run(method)

        # Save results
        busResultsPath = self.projectPath + '/results_buses.csv'
        lineResultsPath = self.projectPath + '/results_lines.csv'
        trafoResultsPath = self.projectPath + '/results_trafos.csv'
        loadsResultsPath = self.projectPath + '/results_loads.csv'

        # Show results
        paths = {
            'lines': lineResultsPath,
            'buses': busResultsPath,
            'transformers': trafoResultsPath,
            'loads': loadsResultsPath,
        }

        self.grid.viewResultCsv(paths) 

    def addBus(self) -> None:
        self.grid.selectMode = False
        self.grid.insertTrafoMode = False
        self.grid.handMode = False
        self.grid.insertLineMode = False 
        self.grid.insertGenMode = False
        self.grid.insertLoadMode = False
        self.grid.insertSlackMode = False
        self.grid.insertBusMode = not(self.grid.insertBusMode) 
        if not self.grid.insertBusMode:
            self.addBusButton.setStyleSheet(self.normalStyle)
        else:
            self.addBusButton.setStyleSheet(self.toggledStyle)
            self.addLoadButton.setStyleSheet(self.normalStyle)
            self.addSlackButton.setStyleSheet(self.normalStyle)
            self.addTrafoButton.setStyleSheet(self.normalStyle)
            self.addLineButton.setStyleSheet(self.normalStyle)
            self.addGenButton.setStyleSheet(self.normalStyle)
            self.editGridButton.setStyleSheet(self.normalStyle)
            self.moveButt.setStyleSheet(self.normalStyle)
        self.update()

    def addLine(self) -> None:
        self.grid.insertBusMode = False
        self.grid.selectMode = False
        self.grid.insertTrafoMode = False
        self.grid.insertGenMode = False
        self.grid.handMode = False
        self.grid.insertLoadMode = False
        self.grid.insertSlackMode = False
        self.grid.insertLineMode = not(self.grid.insertLineMode) 
        if not self.grid.insertLineMode:
            self.addLineButton.setStyleSheet(self.normalStyle)
        else:
            self.addLineButton.setStyleSheet(self.toggledStyle)
            self.addLoadButton.setStyleSheet(self.normalStyle)
            self.addSlackButton.setStyleSheet(self.normalStyle)
            self.addTrafoButton.setStyleSheet(self.normalStyle)
            self.addGenButton.setStyleSheet(self.normalStyle)
            self.addBusButton.setStyleSheet(self.normalStyle)
            self.editGridButton.setStyleSheet(self.normalStyle)
            self.moveButt.setStyleSheet(self.normalStyle)
        self.update()

    def addTrafo(self) -> None:
        self.grid.insertBusMode = False
        self.grid.insertLineMode = False 
        self.grid.insertGenMode = False
        self.grid.selectMode = False
        self.grid.insertLoadMode = False
        self.grid.insertSlackMode = False
        self.grid.insertTrafoMode = not(self.grid.insertTrafoMode) 
        if not self.grid.insertTrafoMode:
            self.addTrafoButton.setStyleSheet(self.normalStyle)
        else:
            self.addTrafoButton.setStyleSheet(self.toggledStyle)
            self.addSlackButton.setStyleSheet(self.normalStyle)
            self.addLoadButton.setStyleSheet(self.normalStyle)
            self.addLineButton.setStyleSheet(self.normalStyle)
            self.addBusButton.setStyleSheet(self.normalStyle)
            self.addGenButton.setStyleSheet(self.normalStyle)
            self.editGridButton.setStyleSheet(self.normalStyle)
            self.moveButt.setStyleSheet(self.normalStyle)
        self.update()

    def addGen(self) -> None:
        self.grid.insertBusMode = False
        self.grid.insertLineMode = False 
        self.grid.selectMode = False
        self.grid.insertTrafoMode = False
        self.grid.insertLoadMode = False
        self.grid.insertSlackMode = False
        self.grid.insertGenMode = not(self.grid.insertGenMode) 
        if not self.grid.insertGenMode:
            self.addGenButton.setStyleSheet(self.normalStyle)
        else:
            self.addGenButton.setStyleSheet(self.toggledStyle)
            self.addSlackButton.setStyleSheet(self.normalStyle)
            self.addLoadButton.setStyleSheet(self.normalStyle)
            self.addTrafoButton.setStyleSheet(self.normalStyle)
            self.addLineButton.setStyleSheet(self.normalStyle)
            self.addBusButton.setStyleSheet(self.normalStyle)
            self.editGridButton.setStyleSheet(self.normalStyle)
            self.moveButt.setStyleSheet(self.normalStyle)
        self.update()

    def addLoad(self) -> None:
        self.grid.insertBusMode = False
        self.grid.insertLineMode = False 
        self.grid.selectMode = False
        self.grid.insertTrafoMode = False
        self.grid.insertGenMode = False
        self.grid.insertSlackMode = False
        self.grid.insertLoadMode = not(self.grid.insertLoadMode) 
        if not self.grid.insertLoadMode:
            self.addLoadButton.setStyleSheet(self.normalStyle)
        else:
            self.addLoadButton.setStyleSheet(self.toggledStyle)
            self.addSlackButton.setStyleSheet(self.normalStyle)
            self.addTrafoButton.setStyleSheet(self.normalStyle)
            self.addLineButton.setStyleSheet(self.normalStyle)
            self.addBusButton.setStyleSheet(self.normalStyle)
            self.editGridButton.setStyleSheet(self.normalStyle)
            self.moveButt.setStyleSheet(self.normalStyle)
        self.update()

    def addSlack(self) -> None:
        self.grid.insertBusMode = False
        self.grid.insertLineMode = False 
        self.grid.selectMode = False
        self.grid.insertTrafoMode = False
        self.grid.insertGenMode = False
        self.grid.insertLoadMode = False
        self.grid.insertSlackMode = not(self.grid.insertSlackMode) 
        if not self.grid.insertSlackMode:
            self.addSlackButton.setStyleSheet(self.normalStyle)
        else:
            self.addSlackButton.setStyleSheet(self.toggledStyle)
            self.addLoadButton.setStyleSheet(self.normalStyle)
            self.addTrafoButton.setStyleSheet(self.normalStyle)
            self.addLineButton.setStyleSheet(self.normalStyle)
            self.addBusButton.setStyleSheet(self.normalStyle)
            self.editGridButton.setStyleSheet(self.normalStyle)
            self.moveButt.setStyleSheet(self.normalStyle)
        self.update()

    def setSelectMode(self) -> None:
        self.grid.insertLoadMode = False
        self.grid.firstNode = None
        if self.grid.insertLineMode:
            self.grid.tempPath = []
        self.grid.insertBusMode = False
        self.grid.insertLineMode = False
        self.grid.insertTrafoMode = False
        self.grid.insertGenMode = False
        self.grid.insertSlackMode = False
        self.grid.insertLoadMode = False
        self.grid.handMode = False
        self.grid.selectMode = not(self.grid.selectMode) 
        if not self.grid.selectMode:
            self.editGridButton.setStyleSheet(self.normalStyle)
        else:
            self.addTrafoButton.setStyleSheet(self.normalStyle)
            self.editGridButton.setStyleSheet(self.toggledStyle)
            self.addLineButton.setStyleSheet(self.normalStyle)
            self.addBusButton.setStyleSheet(self.normalStyle)
            self.addGenButton.setStyleSheet(self.normalStyle)
            self.addSlackButton.setStyleSheet(self.normalStyle)
            self.addLoadButton.setStyleSheet(self.normalStyle)
            self.moveButt.setStyleSheet(self.normalStyle)
        self.update()

    def hand(self) -> None:
        self.grid.insertLoadMode = False
        self.grid.insertBusMode = False
        self.grid.insertLineMode = False
        self.grid.insertTrafoMode = False
        self.grid.selectMode = False
        self.grid.insertGenMode = False
        self.grid.insertSlackMode = False
        self.grid.insertLoadMode = False
        self.grid.handMode = not(self.grid.handMode) 
        if not self.grid.handMode:
            self.moveButt.setStyleSheet(self.normalStyle)
        else:
            self.moveButt.setStyleSheet(self.toggledStyle)
            self.addTrafoButton.setStyleSheet(self.normalStyle)
            self.addLineButton.setStyleSheet(self.normalStyle)
            self.addBusButton.setStyleSheet(self.normalStyle)
            self.addGenButton.setStyleSheet(self.normalStyle)
            self.addSlackButton.setStyleSheet(self.normalStyle)
            self.addLoadButton.setStyleSheet(self.normalStyle)
            self.editGridButton.setStyleSheet(self.normalStyle)
        self.update()

    def zoomIn(self) -> None:
        newSize = self.grid.dist * 2
        if newSize in range(self.minZoom, self.maxZoom):
            self.grid.dist = newSize
            for bus, (point, capacity, orient, points, id) in self.grid.busses.items():
                newOriginX = point.x() * 2
                newOriginY = point.y() * 2
                newOrigin = QPoint(newOriginX, newOriginY)
                point = self.grid.snap(newOrigin)
                newPoints = []
                for p in points:
                    p = QPoint(p.x() * 2, p.y() * 2)
                    newPoints.append(p)
                bigTuple = (point, capacity, orient, newPoints, id)
                edited = self.grid.editedBusses(bus, bigTuple)

            for trafo, (point, ori, hands, bus1, bus2) in self.grid.trafos.items():
                newOriginX = point.x() * 2
                newOriginY = point.y() * 2
                newOrigin = QPoint(newOriginX, newOriginY)
                point = self.grid.snap(newOrigin)
                newPoints = []
                for h in hands:
                    h = QPoint(h.x() * 2, h.y() * 2)
                    newPoints.append(h)
                bigTuple = (point, ori, hands, bus1, bus2)
                self.grid.trafos.update({trafo: bigTuple})
                self.grid.update()
                self.update()

            newPaths = []
            for p in self.grid.paths:
                connection1, connection2, fp, i, tempPath = p
                newTp = []
                for tp in tempPath:
                    tp = QPoint(tp.x() * 2, tp.y() * 2)
                    newTp.append(tp)
                p = connection1, connection2, fp, i, newTp
                newPaths.append(p)

            self.grid.paths = newPaths
            self.grid.update()
            self.grid.updateGuiElementsCSV()
            self.grid.updateBusCSVGuiParams()

    def zoomOut(self) -> None:
        newSize = self.grid.dist // 2
        if newSize in range(self.minZoom, self.maxZoom):
            self.grid.dist = newSize
            for bus, (point, capacity, orient, points, id) in self.grid.busses.items():
                newOriginX = point.x() // 2
                newOriginY = point.y() // 2
                newOrigin = QPoint(newOriginX, newOriginY)
                point = self.grid.snap(newOrigin)
                newPoints = []
                for p in points:
                    p = QPoint(p.x() // 2, p.y() // 2)
                    newPoints.append(p)
                bigTuple = (point, capacity, orient, newPoints, id)
                edited = self.grid.editedBusses(bus, bigTuple)

            for trafo, (point, ori, hands, bus1, bus2) in self.grid.trafos.items():
                newOriginX = point.x() // 2
                newOriginY = point.y() // 2
                newOrigin = QPoint(newOriginX, newOriginY)
                point = self.grid.snap(newOrigin)
                newPoints = []
                for h in hands:
                    h = QPoint(h.x() // 2, h.y() // 2)
                    newPoints.append(h)
                bigTuple = (point, ori, hands, bus1, bus2)
                self.grid.trafos.update({trafo: bigTuple})
                self.grid.update()
                self.update()

            newPaths = []
            for p in self.grid.paths:
                connection1, connection2, fp, i, tempPath = p
                newTp = []
                for tp in tempPath:
                    tp = QPoint(tp.x() // 2, tp.y() // 2)
                    newTp.append(tp)
                p = connection1, connection2, fp, i, newTp
                newPaths.append(p)

            self.grid.paths = newPaths
            self.grid.update()
            self.grid.updateGuiElementsCSV()
            self.grid.updateBusCSVGuiParams()
