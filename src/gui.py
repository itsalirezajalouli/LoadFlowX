# Main GUI setup and window management

# Imports
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtCore import QSize
from grid import Grid
from start_window import StartUp
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QHBoxLayout, QMainWindow, QStatusBar, QVBoxLayout, QWidget, QToolButton

# Main Window Object
class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle('DickSilent!')
        self.setMinimumSize(800, 700)
        self.projectPath = None
        self.startUp = StartUp(self)
        self.buttSize = 26
        self.grid = None
        self.minZoom = 8 
        self.maxZoom = 512
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

        # Symbols Toolbox
        self.symbolsToolbox = QWidget()
        self.toolBoxLayout = QVBoxLayout()
        self.symbolsToolbox.setLayout(self.toolBoxLayout)
        self.symbolsToolbox.setStyleSheet('''
            background-color:#23272a;
            border-radius: 15px;
        ''')
        self.symbolsToolbox.setFixedWidth(52)
        self.symbolsToolbox.setFixedHeight(210)
        self.toolBoxLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        #   Edit button
        self.editGridButton = QToolButton()
        self.editGridButton.setIcon(QIcon('../icons/editGrid.png'))
        self.editGridButton.setIconSize(QSize(self.buttSize, self.buttSize))
        self.editGridButton.clicked.connect(self.setSelectMode)
        self.editGridButton.setStyleSheet('''
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
        ''')
        self.viewBar.addWidget(self.editGridButton)

        # move button
        moveButt = QToolButton()
        moveButt.setIcon(QIcon('../icons/move.png'))
        moveButt.setIconSize(QSize(self.buttSize, self.buttSize))
        moveButt.clicked.connect(self.hand)
        moveButt.setStyleSheet('''
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
        ''')
        self.viewBar.addWidget(moveButt)
        self.viewToolbox.setLayout(self.viewBar)

        #   erase button
        eraseGridButt = QToolButton()
        eraseGridButt.setIcon(QIcon('../icons/eraseGrid.png'))
        eraseGridButt.setIconSize(QSize(self.buttSize, self.buttSize))
        eraseGridButt.setStyleSheet('''
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
        ''')
        self.viewBar.addWidget(eraseGridButt)

        #   Zoom In button
        zoomInButt = QToolButton()
        zoomInButt.setIcon(QIcon('../icons/zoomIn.png'))
        zoomInButt.setIconSize(QSize(self.buttSize, self.buttSize))
        zoomInButt.setStyleSheet('''
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
        ''')
        zoomInButt.clicked.connect(self.zoomIn)
        self.viewBar.addWidget(zoomInButt)

        #   Zoom Out button
        zoomOutButt = QToolButton()
        zoomOutButt.setIcon(QIcon('../icons/zoomOut.png'))
        zoomOutButt.setIconSize(QSize(self.buttSize, self.buttSize))
        zoomOutButt.setStyleSheet('''
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
        ''')
        zoomOutButt.clicked.connect(self.zoomOut)
        self.viewBar.addWidget(zoomOutButt)

        #   Add Bus button
        addBusButton = QToolButton()
        addBusButton.setIcon(QIcon('../icons/bus.png'))
        addBusButton.setIconSize(QSize(self.buttSize, self.buttSize))
        addBusButton.setStyleSheet('''
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
        ''')
        addBusButton.clicked.connect(self.addBus)
        self.toolBoxLayout.addWidget(addBusButton)

        self.barLayout.addWidget(self.viewToolbox)
        self.barLayout.addWidget(self.symbolsToolbox)

        #   Add Line button
        addLineButton = QToolButton()
        addLineButton.setIcon(QIcon('../icons/line.png'))
        addLineButton.setIconSize(QSize(self.buttSize, self.buttSize))
        addLineButton.setStyleSheet('''
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
        ''')
        addLineButton.clicked.connect(self.addLine)
        self.toolBoxLayout.addWidget(addLineButton)

        #   Add Transformer button
        addTrafoButton = QToolButton()
        addTrafoButton.setIcon(QIcon('../icons/transformer.png'))
        addTrafoButton.setIconSize(QSize(self.buttSize, self.buttSize))
        addTrafoButton.setStyleSheet('''
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
        ''')
        addTrafoButton.clicked.connect(self.addTrafo)
        self.toolBoxLayout.addWidget(addTrafoButton)

        #   Add Generator button
        addGenButton = QToolButton()
        addGenButton.setIcon(QIcon('../icons/generator.png'))
        addGenButton.setIconSize(QSize(self.buttSize, self.buttSize))
        addGenButton.setStyleSheet('''
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
        ''')
        self.toolBoxLayout.addWidget(addGenButton)

        #   Add Load button
        addLoadButton = QToolButton()
        addLoadButton.setIcon(QIcon('../icons/load.png'))
        addLoadButton.setIconSize(QSize(self.buttSize, self.buttSize))
        addLoadButton.setStyleSheet('''
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
        ''')
        self.toolBoxLayout.addWidget(addLoadButton)

        # Grid Layout
        self.grid = Grid(32)
        self.grid.projectPath = self.projectPath
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

    def addBus(self) -> None:
        self.grid.selectMode = False
        self.grid.insertTrafoMode = False
        self.grid.insertLineMode = False 
        self.grid.insertBusMode = True
        self.update()

    def addLine(self) -> None:
        self.grid.insertBusMode = False
        self.grid.selectMode = False
        self.grid.insertTrafoMode = False
        self.grid.insertLineMode = True
        self.update()

    def addTrafo(self) -> None:
        print('Adding Trafo')
        self.grid.insertBusMode = False
        self.grid.insertLineMode = False 
        self.grid.selectMode = False
        self.grid.insertTrafoMode = True
        self.update()

    def setSelectMode(self) -> None:
        self.grid.insertBusMode = False
        self.grid.insertLineMode = False
        self.grid.insertTrafoMode = False
        self.grid.selectMode = True 
        self.update()

    def hand(self) -> None:
        if not self.grid.handMode: 
            self.grid.handMode = True
        else: 
            self.grid.handMode = False 

    def zoomIn(self) -> None:
        newSize = self.grid.dist * 2
        if newSize in range(self.minZoom, self.maxZoom):
            self.grid.dist = newSize
            for bus, (point, capacity, orient, points) in self.grid.busses.items():
                newOriginX = point.x() * 2
                newOriginY = point.y() * 2
                newOrigin = QPoint(newOriginX, newOriginY)
                point = self.grid.snap(newOrigin)
                bigTuple = (point, capacity, orient, points)
                edited = self.grid.editedBusses(bus, bigTuple)
                # for p in points:
                #     p.x() * 2
                #     p.y() * 2
            self.grid.update()

    def zoomOut(self) -> None:
        newSize = self.grid.dist // 2
        if newSize in range(self.minZoom, self.maxZoom):
            self.grid.dist = newSize
            for bus, (point, capacity, orient, points) in self.grid.busses.items():
                newOriginX = point.x() // 2
                newOriginY = point.y() // 2
                newOrigin = QPoint(newOriginX, newOriginY)
                point = self.grid.snap(newOrigin)
                bigTuple = (point, capacity, orient, points)
                edited = self.grid.editedBusses(bus, bigTuple)
            self.grid.update()
