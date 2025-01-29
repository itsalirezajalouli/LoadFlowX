# Main GUI setup and window management

# Imports
import csv
from time import perf_counter
from grid import Grid
from simulator import runLoadFlow 
from PyQt6.QtCore import QSize
from start_window import StartUp
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QAction, QIcon, QCursor, QPixmap
from PyQt6.QtWidgets import QHBoxLayout, QMainWindow, QStatusBar, QVBoxLayout, QWidget, QToolButton

# Main Window Object
class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle('PSA II Project')
        self.setMinimumSize(800, 700)
        self.isThemeLight = False
        self.THEMES = {
            'dark': {
                'background': '#2c2f33',
                'secondaryBackground': '#23272a',
                'buttonBackground': '#3b3e45',
                'buttonBorder': '#3b3e45',
                'buttonHoverBorder': '#7289da',
                'buttonPressedBorder': '#FAA61A',
                'text': '#ffffff'
            },
            'light': {
                'background': '#f0f0f0',  # Light grey background
                'secondaryBackground': '#e0e0e0',  # Lighter secondary
                'buttonBackground': '#d9d9d9',  # Light button background
                'buttonBorder': '#d9d9d9',
                'buttonHoverBorder': '#4b6cb7',  # Soft blue for hover
                'buttonPressedBorder': '#ff9800',  # Orange highlight
                'text': '#333333'  # Dark text for contrast
            }
        }
        self.projectPath = None
        self.startUp = StartUp(self)
        self.buttSize = 26
        if self.projectPath is None:
            self.startUp.exec()
            if not self.startUp.nameError:
                self.projectPath = self.startUp.projectPath

        # Layouts
        self.mainLayout = QHBoxLayout()

        # Grid Layout
        self.grid = Grid(32)
        self.grid.projectPath = self.projectPath
        if self.startUp.loaded:
            self.grid.loadGUI()
        else: 
            self.grid.drawingParams = [20, 12, 7, 24, 1, 2]
        self.mainLayout.addWidget(self.grid, 12)

        # Menu Bar
        self.menu = self.menuBar()
        self.menu.setStyleSheet('''
            background-color: #2c2f33; color: #fff; ''')
        fileMenu = self.menu.addMenu('&File')
        editMenu = self.menu.addMenu('&Edit')
        loadFlowMenu = self.menu.addMenu('&Load Flow')
        viewMenu = self.menu.addMenu('&View')
        docMenu = self.menu.addMenu('&Docs')

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
        self.viewToolbox.setFixedHeight(260)
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
        self.runWidget.setFixedHeight(100)

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

        # Dark Mode Styles
        self.normalStyle4dark = '''
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

        self.toggledStyle4dark = '''
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
        # Light Mode Styles
        self.normalStyle4light = '''
            QToolButton {
                font-size: 24px;
                background-color: #d9d9d9; /* Updated background color */
                border: 1px solid #d9d9d9;
                border-radius: 10px;
                padding: 2px;
                color: #333333;
            }
            QToolButton:hover {
                background-color: #e0e0e0;
                border: 1px solid #4b6cb7;
            }
            QToolButton:pressed {
                background-color: #d9d9d9;
                border: 1px solid #ff9800;
            }
        '''

        self.toggledStyle4light = '''
            QToolButton {
                font-size: 24px;
                background-color: #d9d9d9; /* Updated background color */
                border: 1px solid #ff9800;
                border-radius: 10px;
                padding: 2px;
                color: #333333;
            }
            QToolButton:hover {
                background-color: #e0e0e0;
                border: 1px solid #4b6cb7;
            }
            QToolButton:pressed {
                background-color: #d9d9d9;
                border: 1px solid #4b6cb7;
            }
        '''

        self.normalStyle = self.normalStyle4dark
        self.toggledStyle = self.toggledStyle4dark

        #   Edit button
        self.editGridButton = QToolButton()
        self.editGridButton.setIcon(QIcon('../icons/editGrid.png'))
        self.editGridButton.setIconSize(QSize(self.buttSize, self.buttSize))
        self.editGridButton.clicked.connect(self.setSelectMode)
        self.editGridButton.setStyleSheet(self.normalStyle)
        self.viewBar.addWidget(self.editGridButton)

        #   Move button
        self.moveButt = QToolButton()
        self.moveButt.setIcon(QIcon('../icons/move.png'))
        self.moveButt.setIconSize(QSize(self.buttSize, self.buttSize))
        self.moveButt.clicked.connect(self.moveFunc)
        self.moveButt.setStyleSheet(self.normalStyle)
        self.viewBar.addWidget(self.moveButt)

        # Hand button
        self.handButt = QToolButton()
        self.handButt.setIcon(QIcon('../icons/hand.png'))
        self.handButt.setIconSize(QSize(self.buttSize, self.buttSize))
        self.handButt.clicked.connect(self.hand)
        self.handButt.setStyleSheet(self.normalStyle)
        self.viewBar.addWidget(self.handButt)
        self.viewToolbox.setLayout(self.viewBar)

        #   erase button
        self.eraseButt = QToolButton()
        self.eraseButt.setIcon(QIcon('../icons/eraseGrid.png'))
        self.eraseButt.setIconSize(QSize(self.buttSize, self.buttSize))
        self.eraseButt.setStyleSheet(self.normalStyle)
        self.eraseButt.clicked.connect(self.erase)
        self.viewBar.addWidget(self.eraseButt)

        #   Zoom In button
        self.zoomInButt = QToolButton()
        self.zoomInButt.setIcon(QIcon('../icons/zoomIn.png'))
        self.zoomInButt.setIconSize(QSize(self.buttSize, self.buttSize))
        self.zoomInButt.setStyleSheet(self.normalStyle)
        if self.grid is not None:
            self.zoomInButt.clicked.connect(self.grid.zoomIn)
        self.viewBar.addWidget(self.zoomInButt)

        #   Zoom Out button
        self.zoomOutButt = QToolButton()
        self.zoomOutButt.setIcon(QIcon('../icons/zoomOut.png'))
        self.zoomOutButt.setIconSize(QSize(self.buttSize, self.buttSize))
        self.zoomOutButt.setStyleSheet(self.normalStyle)
        if self.grid is not None:
            self.zoomOutButt.clicked.connect(self.grid.zoomOut)
        self.viewBar.addWidget(self.zoomOutButt)

        #   Run button
        self.runButton = QToolButton()
        self.runButton.setIcon(QIcon('../icons/run.png'))
        self.runButton.setIconSize(QSize(self.buttSize, self.buttSize))
        self.runButton.setStyleSheet(self.normalStyle)
        self.runButton.clicked.connect(self.run)
        self.runLayout.addWidget(self.runButton)

        #   theme button
        self.themeButton = QToolButton()
        self.themeButton.setIcon(QIcon('../icons/lightMode.png'))
        self.themeButton.setIconSize(QSize(self.buttSize, self.buttSize))
        self.themeButton.setStyleSheet(self.normalStyle)
        self.themeButton.clicked.connect(self.toggleTheme)
        self.runLayout.addWidget(self.themeButton)

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
        
        # Main Widget
        self.mainLayout.addWidget(self.barWidget)
        self.widget = QWidget()
        self.widget.setLayout(self.mainLayout)
        self.widget.setStyleSheet('''
            background-color: #191b1d;
        ''')
        self.setCentralWidget(self.widget)

        # Status Bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage(
            'Power System Analysis II Project - Load Flow Methods GUI Simulator')
        self.statusBar.setStyleSheet('''
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
        self.grid.afterRun = True
        method, maxIter = self.grid.openRunDialog()
        # Passing data csvs to the simulator
        busCsvPath = self.projectPath + '/Buses.csv'
        lineCSV = self.projectPath + '/Lines.csv'
        trafoCSV = self.projectPath + '/Trafos.csv'
        genCSV = self.projectPath + '/Gens.csv'
        loadCSV = self.projectPath + '/Loads.csv'
        slacksCSV = self.projectPath + '/Slacks.csv'
        # Run load flow Simulation
        startTime = perf_counter()
        success, error_msg = runLoadFlow(self.projectPath,
                            busCsvPath, lineCSV, trafoCSV, genCSV, loadCSV, slacksCSV,
                            method, maxIter)
        executionTime = perf_counter() - startTime
        print(f'Function took {executionTime:.4f} seconds')
        # Show results
        busResultsPath = self.projectPath + '/results_buses.csv'
        lineResultsPath = self.projectPath + '/results_lines.csv'
        trafoResultsPath = self.projectPath + '/results_trafos.csv'
        loadsResultsPath = self.projectPath + '/results_loads.csv'
        paths = {
            'lines': lineResultsPath,
            'buses': busResultsPath,
            'transformers': trafoResultsPath,
            'loads': loadsResultsPath,
        }
        if success:
            self.grid.viewResultCsv(paths, executionTime) 
        else:
            self.grid.showError(error_msg)

    def addBus(self) -> None:
        self.unsetCursor()

        self.grid.selectMode = False
        self.grid.insertTrafoMode = False
        self.grid.handMode = False
        self.grid.insertLineMode = False 
        self.grid.insertGenMode = False
        self.grid.insertLoadMode = False
        self.grid.insertSlackMode = False
        self.grid.moveMode = False
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
            self.handButt.setStyleSheet(self.normalStyle)
            self.moveButt.setStyleSheet(self.normalStyle)
        self.update()

    def addLine(self) -> None:
        # change cursor
        if self.isThemeLight:
            icon = QPixmap('../icons/lightMode/line.png')
        else:
            icon = QPixmap('../icons/line.png')
        scaledIcon = icon.scaled(QSize(32, 32))  
        cursor = QCursor(scaledIcon)
        self.setCursor(cursor)

        self.grid.insertBusMode = False
        self.grid.selectMode = False
        self.grid.insertTrafoMode = False
        self.grid.insertGenMode = False
        self.grid.handMode = False
        self.grid.insertLoadMode = False
        self.grid.insertSlackMode = False
        self.grid.moveMode = False
        self.grid.eraseMode = False
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
            self.handButt.setStyleSheet(self.normalStyle)
            self.moveButt.setStyleSheet(self.normalStyle)
            self.eraseButt.setStyleSheet(self.normalStyle)
        self.update()

    def addTrafo(self) -> None:
        self.unsetCursor()
        self.grid.insertBusMode = False
        self.grid.insertLineMode = False 
        self.grid.insertGenMode = False
        self.grid.selectMode = False
        self.grid.insertLoadMode = False
        self.grid.insertSlackMode = False
        self.grid.moveMode = False
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
            self.handButt.setStyleSheet(self.normalStyle)
            self.moveButt.setStyleSheet(self.normalStyle)
        self.update()

    def addGen(self) -> None:
        self.unsetCursor()
        self.grid.insertBusMode = False
        self.grid.insertLineMode = False 
        self.grid.selectMode = False
        self.grid.insertTrafoMode = False
        self.grid.insertLoadMode = False
        self.grid.insertSlackMode = False
        self.grid.moveMode = False
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
            self.handButt.setStyleSheet(self.normalStyle)
            self.moveButt.setStyleSheet(self.normalStyle)
        self.update()

    def addLoad(self) -> None:
        self.unsetCursor()

        self.grid.insertBusMode = False
        self.grid.insertLineMode = False 
        self.grid.selectMode = False
        self.grid.insertTrafoMode = False
        self.grid.insertGenMode = False
        self.grid.insertSlackMode = False
        self.grid.moveMode = False
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
            self.handButt.setStyleSheet(self.normalStyle)
            self.moveButt.setStyleSheet(self.normalStyle)
        self.update()

    def addSlack(self) -> None:
        self.unsetCursor()

        self.grid.insertBusMode = False
        self.grid.insertLineMode = False 
        self.grid.selectMode = False
        self.grid.insertTrafoMode = False
        self.grid.insertGenMode = False
        self.grid.insertLoadMode = False
        self.grid.moveMode = False
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
            self.handButt.setStyleSheet(self.normalStyle)
            self.moveButt.setStyleSheet(self.normalStyle)
        self.update()

    def setSelectMode(self) -> None:
        self.unsetCursor()
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
            self.handButt.setStyleSheet(self.normalStyle)
            self.moveButt.setStyleSheet(self.normalStyle)
        self.update()

    def hand(self) -> None:
        # change cursor
        if self.isThemeLight:
            icon = QPixmap('../icons/lightMode/hand.png')
        else:
            icon = QPixmap('../icons/hand.png')
        scaledIcon = icon.scaled(QSize(32, 32))  
        cursor = QCursor(scaledIcon)
        self.setCursor(cursor)

        self.grid.insertLoadMode = False
        self.grid.insertBusMode = False
        self.grid.insertLineMode = False
        self.grid.insertTrafoMode = False
        self.grid.selectMode = False
        self.grid.insertGenMode = False
        self.grid.insertSlackMode = False
        self.grid.insertLoadMode = False
        self.grid.moveMode = False
        self.grid.handMode = not(self.grid.handMode) 
        if not self.grid.handMode:
            self.handButt.setStyleSheet(self.normalStyle)
        else:
            self.handButt.setStyleSheet(self.toggledStyle)
            self.addTrafoButton.setStyleSheet(self.normalStyle)
            self.addLineButton.setStyleSheet(self.normalStyle)
            self.addBusButton.setStyleSheet(self.normalStyle)
            self.addGenButton.setStyleSheet(self.normalStyle)
            self.addSlackButton.setStyleSheet(self.normalStyle)
            self.addLoadButton.setStyleSheet(self.normalStyle)
            self.editGridButton.setStyleSheet(self.normalStyle)
            self.moveButt.setStyleSheet(self.normalStyle)
        self.update()

    def moveFunc(self) -> None:
        # change cursor
        if self.isThemeLight:
            icon = QPixmap('../icons/lightMode/move.png')
        else:
            icon = QPixmap('../icons/move.png')
        scaledIcon = icon.scaled(QSize(32, 32))  
        cursor = QCursor(scaledIcon)
        self.setCursor(cursor)

        self.grid.insertLoadMode = False
        self.grid.insertBusMode = False
        self.grid.insertLineMode = False
        self.grid.insertTrafoMode = False
        self.grid.selectMode = False
        self.grid.insertGenMode = False
        self.grid.insertSlackMode = False
        self.grid.insertLoadMode = False
        self.grid.handMode = False
        self.grid.moveMode = not(self.grid.moveMode) 
        if not self.grid.moveMode:
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
            self.handButt.setStyleSheet(self.normalStyle)
        self.update()

    def erase(self) -> None:
        # change cursor
        if self.isThemeLight:
            icon = QPixmap('../icons/lightMode/eraseGrid.png')
        else:
            icon = QPixmap('../icons/eraseGrid.png')
        scaledIcon = icon.scaled(QSize(32, 32))  
        cursor = QCursor(scaledIcon)
        self.setCursor(cursor)

        self.grid.insertLoadMode = False
        self.grid.insertBusMode = False
        self.grid.insertLineMode = False
        self.grid.insertTrafoMode = False
        self.grid.selectMode = False
        self.grid.insertGenMode = False
        self.grid.insertSlackMode = False
        self.grid.insertLoadMode = False
        self.grid.handMode = False
        self.grid.moveMode = False
        self.grid.eraseMode = not(self.grid.eraseMode) 
        if not self.grid.eraseMode:
            self.eraseButt.setStyleSheet(self.normalStyle)
        else:
            self.eraseButt.setStyleSheet(self.toggledStyle)
            self.moveButt.setStyleSheet(self.normalStyle)
            self.addTrafoButton.setStyleSheet(self.normalStyle)
            self.addLineButton.setStyleSheet(self.normalStyle)
            self.addBusButton.setStyleSheet(self.normalStyle)
            self.addGenButton.setStyleSheet(self.normalStyle)
            self.addSlackButton.setStyleSheet(self.normalStyle)
            self.addLoadButton.setStyleSheet(self.normalStyle)
            self.editGridButton.setStyleSheet(self.normalStyle)
            self.handButt.setStyleSheet(self.normalStyle)
        self.update()

    def clear(self) -> None:

        # Clearing all the data
        self.grid.busCounter = 0
        self.grid.trafoCounter = 0
        self.grid.genCounter = 0
        self.grid.loadCounter = 0
        self.grid.slackCounter = 0
        self.grid.firstNode = None
        self.grid.busses = {}
        self.grid.trafos = {}
        self.grid.gens = {}
        self.grid.loads = {}
        self.grid.slacks = {}
        self.grid.paths = []
        self.grid.tokenBusPorts = []
        self.grid.tokenTrafoHands = []
        self.grid.tokenGenHands = []
        self.grid.tokenLoadHands = []
        self.grid.tokenSlackHands = []
        self.grid.xDists = []
        self.grid.tempPath = []
        self.grid.firstType = None
        self.grid.update()

        self.busCSV = self.projectPath + '/Buses.csv'
        self.lineCSV = self.projectPath + '/Lines.csv'
        self.guiCSV = self.projectPath + '/GUI.csv'
        self.genCSV = self.projectPath + '/Gens.csv'
        self.trafoCSV = self.projectPath + '/Trafos.csv'
        self.loadCSV = self.projectPath + '/Loads.csv'
        self.slackCSV = self.projectPath + '/Slacks.csv'

        with open(self.guiCSV, 'w', newline = '') as file:
            writer = csv.DictWriter(file,fieldnames=['dist','paths'])
            writer.writeheader()
        print(f'-> GUI header cleared to {self.lineCSV} successfuly.')

        with open(self.busCSV, 'w', newline = '') as file:
            writer = csv.DictWriter(file,fieldnames=['id', 'bType', 'vMag', 'zone', 'vAng',
                                                     'P', 'Q', 'name', 'pos',
                                                     'capacity', 'orient', 'points'])
            writer.writeheader()
        print(f'-> Bus header cleared to {self.busCSV} successfuly.')

        with open(self.lineCSV, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=[
                'name', 'bus1id', 'bus2id', 'R', 'X',
                'len', 'c_nf_per_km', 'max_i_ka'
            ])
            writer.writeheader()
        print(f'-> Line header cleared to {self.lineCSV} successfuly.')

        with open(self.genCSV, 'w', newline = '') as file:
            writer = csv.DictWriter(file, fieldnames=[
                'id', 'bus', 'name', 'pMW', 'vmPU', 'minQMvar', 'maxQMvar', 
                'minPMW', 'maxPMW', 'pos', 'orient', 'hand'
            ])
            writer.writeheader()
        print(f'-> Gen header cleared to {self.genCSV} successfuly.')

        with open(self.trafoCSV, 'w', newline = '') as file:
            writer = csv.DictWriter(file, fieldnames=[
                'id', 'name', 'hvBus', 'lvBus', 'pos', 'orient', 'hands', 
                'sn_mva', 'vk_percent', 'vkr_percent', 'tap_step_percent'
            ])
            writer.writeheader()
        print(f'-> Trafo header cleared to {self.trafoCSV} successfuly.')

        with open(self.loadCSV, 'w', newline = '') as file:
            writer = csv.DictWriter(file, fieldnames=['id','bus', 'vmPU', 'vaD',
                                                          'pos', 'orient', 'hand'])
            writer.writeheader()
        print(f'-> Load header cleared to {self.loadCSV} successfuly.')

        with open(self.slackCSV, 'w', newline = '') as file:
            writer = csv.DictWriter(file, fieldnames=['id','bus', 'vmPU', 'vaD',
                                                          'pos', 'orient', 'hand'])
            writer.writeheader()
        print(f'-> Slack header cleared to {self.slackCSV} successfuly.')

    def toggleTheme(self) -> None:
        self.grid.insertLoadMode = False
        self.grid.insertBusMode = False
        self.grid.insertLineMode = False
        self.grid.insertTrafoMode = False
        self.grid.selectMode = False
        self.grid.insertGenMode = False
        self.grid.insertSlackMode = False
        self.grid.insertLoadMode = False
        self.grid.handMode = False
        self.grid.moveMode = False
        self.grid.eraseMode = False
        if self.isThemeLight:
            self.themeButton.setIcon(QIcon('../icons/lightMode.png'))
            self.widget.setStyleSheet('''
                background-color: #191b1d;
            ''')
            self.applyGeneralStyle(widget = self.menu, theme = 'dark')
            self.applyGeneralStyle(widget = self.statusBar,theme = 'dark')
            self.applyGeneralStyle(widget = self.viewToolbox, theme = 'dark')
            self.applyGeneralStyle(widget = self.symbolsToolbox, theme = 'dark')
            self.applyGeneralStyle(widget = self.runWidget, theme = 'dark')
            self.editGridButton.setIcon(QIcon('../icons/editGrid.png'))
            self.moveButt.setIcon(QIcon('../icons/move.png'))
            self.handButt.setIcon(QIcon('../icons/hand.png'))
            self.eraseButt.setIcon(QIcon('../icons/eraseGrid.png'))
            self.zoomInButt.setIcon(QIcon('../icons/zoomIn.png'))
            self.zoomOutButt.setIcon(QIcon('../icons/zoomOut.png'))
            self.runButton.setIcon(QIcon('../icons/run.png'))
            self.themeButton.setIcon(QIcon('../icons/lightMode.png'))
            self.addBusButton.setIcon(QIcon('../icons/bus.png'))
            self.addLineButton.setIcon(QIcon('../icons/line.png'))
            self.addTrafoButton.setIcon(QIcon('../icons/transformer.png'))
            self.addGenButton.setIcon(QIcon('../icons/generator.png'))
            self.addLoadButton.setIcon(QIcon('../icons/load.png'))
            self.addSlackButton.setIcon(QIcon('../icons/slack.png'))

            self.normalStyle = self.normalStyle4dark
            self.toggledStyle = self.toggledStyle4dark

            self.addTrafoButton.setStyleSheet(self.normalStyle)
            self.addLineButton.setStyleSheet(self.normalStyle)
            self.addBusButton.setStyleSheet(self.normalStyle)
            self.addGenButton.setStyleSheet(self.normalStyle)
            self.addSlackButton.setStyleSheet(self.normalStyle)
            self.addLoadButton.setStyleSheet(self.normalStyle)
            self.editGridButton.setStyleSheet(self.normalStyle)
            self.handButt.setStyleSheet(self.normalStyle)
            self.zoomInButt.setStyleSheet(self.normalStyle)
            self.zoomOutButt.setStyleSheet(self.normalStyle)
            self.moveButt.setStyleSheet(self.normalStyle)
            self.runButton.setStyleSheet(self.normalStyle)
            self.themeButton.setStyleSheet(self.normalStyle)
            self.eraseButt.setStyleSheet(self.normalStyle)
            self.grid.toggleGridColors('dark')
        else:
            self.themeButton.setIcon(QIcon('../icons/darkMode.png'))
            self.applyGeneralStyle(widget = self.widget, theme = 'light')
            self.applyGeneralStyle(widget = self.menu, theme = 'light')
            self.applyGeneralStyle(widget = self.statusBar,theme = 'light')
            self.applyContainerStyle(widget = self.viewToolbox, theme = 'light')
            self.applyContainerStyle(widget = self.symbolsToolbox, theme = 'light')
            self.applyContainerStyle(widget = self.runWidget, theme = 'light')
            self.editGridButton.setIcon(QIcon('../icons/lightMode/editGrid.png'))
            self.moveButt.setIcon(QIcon('../icons/lightMode/move.png'))
            self.handButt.setIcon(QIcon('../icons/lightMode/hand.png'))
            self.eraseButt.setIcon(QIcon('../icons/lightMode/eraseGrid.png'))
            self.zoomInButt.setIcon(QIcon('../icons/lightMode/zoomIn.png'))
            self.zoomOutButt.setIcon(QIcon('../icons/lightMode/zoomOut.png'))
            self.runButton.setIcon(QIcon('../icons/lightMode/run.png'))
            self.themeButton.setIcon(QIcon('../icons/lightMode/lightMode.png'))
            self.addBusButton.setIcon(QIcon('../icons/lightMode/bus.png'))
            self.addLineButton.setIcon(QIcon('../icons/lightMode/line.png'))
            self.addTrafoButton.setIcon(QIcon('../icons/lightMode/transformer.png'))
            self.addGenButton.setIcon(QIcon('../icons/lightMode/generator.png'))
            self.addLoadButton.setIcon(QIcon('../icons/lightMode/load.png'))
            self.addSlackButton.setIcon(QIcon('../icons/lightMode/slack.png'))

            self.normalStyle = self.normalStyle4light
            self.toggledStyle = self.toggledStyle4light

            self.addTrafoButton.setStyleSheet(self.normalStyle)
            self.addLineButton.setStyleSheet(self.normalStyle)
            self.addBusButton.setStyleSheet(self.normalStyle)
            self.addGenButton.setStyleSheet(self.normalStyle)
            self.addSlackButton.setStyleSheet(self.normalStyle)
            self.addLoadButton.setStyleSheet(self.normalStyle)
            self.editGridButton.setStyleSheet(self.normalStyle)
            self.handButt.setStyleSheet(self.normalStyle)
            self.zoomInButt.setStyleSheet(self.normalStyle)
            self.zoomOutButt.setStyleSheet(self.normalStyle)
            self.moveButt.setStyleSheet(self.normalStyle)
            self.runButton.setStyleSheet(self.normalStyle)
            self.themeButton.setStyleSheet(self.normalStyle)
            self.eraseButt.setStyleSheet(self.normalStyle)

            self.grid.toggleGridColors('light')

        self.isThemeLight = not(self.isThemeLight) 

    def applyGeneralStyle(self, widget, theme: str):
        colors = self.THEMES[theme]
        widget.setStyleSheet(f'''
            background-color: {colors['background']};
            color: {colors['text']};
            border-radius: 15px;
        ''')

    def applyContainerStyle(self, widget, theme: str):
        colors = self.THEMES[theme]
        widget.setStyleSheet(f'''
            background-color: {colors['secondaryBackground']};
            color: {colors['text']};
            border-radius: 15px;
        ''')

