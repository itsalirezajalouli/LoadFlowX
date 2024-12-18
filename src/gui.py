# Main GUI setup and window management

# Imports
from PyQt6.QtCore import Qt
from PyQt6.QtCore import QSize
from grid import Grid
from other_dialogs import GetProjectNameDialog, LoadProject
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QHBoxLayout, QMainWindow, QStatusBar, QVBoxLayout, QWidget, QToolButton

# Main Window Object
class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle('DickSilent!')
        self.setMinimumSize(800, 700)
        self.projectName = None
        self.getProjectNameDialog = GetProjectNameDialog(self)
        self.loadProject = LoadProject(self)

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
        self.mainLayout.setSpacing(10)
        self.toolBox = QWidget()
        self.toolBoxLayout = QVBoxLayout()
        self.toolBox.setLayout(self.toolBoxLayout)
        self.toolBox.setStyleSheet('''
            background-color: #23272a;
            border-radius: 12px;
        ''')

        #   Select button
        selectButton = QToolButton()
        selectButton.setIcon(QIcon('../icons/select.png'))
        selectButton.setIconSize(QSize(28, 28))
        selectButton.clicked.connect(self.setSelectMode)
        selectButton.setStyleSheet('''
        QToolButton {
            font-size: 24px;
            background-color: #3b3e45;
            border: 2px solid #7289da;
            border-radius: 10px;
            padding: 2px;
            color: #ffffff;
        }
        QToolButton:hover {
            background-color: #3b3e45;
            border: 2px solid #99aab5;
        }
        QToolButton:pressed {
            background-color: #23272a;
            border: 2px solid #7289da;
        }
        ''')
        self.toolBoxLayout.addWidget(selectButton)

        #   Add Bus button
        addBusButton = QToolButton()
        addBusButton.setText('B')
        addBusButton.setStyleSheet('''
        QToolButton {
            font-size: 24px;
            background-color: #3b3e45;
            border: 2px solid #7289da;
            border-radius: 10px;
            padding: 2px;
            color: #ffffff;
        }
        QToolButton:hover {
            background-color: #3b3e45;
            border: 2px solid #99aab5;
        }
        QToolButton:pressed {
            background-color: #23272a;
            border: 2px solid #7289da;
        }
        ''')
        addBusButton.clicked.connect(self.addBus)
        self.toolBoxLayout.addWidget(addBusButton)

        self.mainLayout.addWidget(self.toolBox)

        #   Add Line button
        addLineButton = QToolButton()
        addLineButton.setText('Li')
        addLineButton.setStyleSheet('''
        QToolButton {
            font-size: 24px;
            background-color: #3b3e45;
            border: 2px solid #7289da;
            border-radius: 10px;
            padding: 2px;
            color: #ffffff;
        }
        QToolButton:hover {
            background-color: #3b3e45;
            border: 2px solid #99aab5;
        }
        QToolButton:pressed {
            background-color: #23272a;
            border: 2px solid #7289da;
        }
        ''')
        addLineButton.clicked.connect(self.addLine)
        self.toolBoxLayout.addWidget(addLineButton)

        #   Add Generator button
        addGenButton = QToolButton()
        addGenButton.setText('G')
        addGenButton.setStyleSheet('''
        QToolButton {
            font-size: 24px;
            background-color: #3b3e45;
            border: 2px solid #7289da;
            border-radius: 10px;
            padding: 2px;
            color: #ffffff;
        }
        QToolButton:hover {
            background-color: #3b3e45;
            border: 2px solid #99aab5;
        }
        QToolButton:pressed {
            background-color: #23272a;
            border: 2px solid #7289da;
        }
        ''')
        self.toolBoxLayout.addWidget(addGenButton)

        #   Add Transformer button
        addTrafoButton = QToolButton()
        addTrafoButton.setText('T')
        addTrafoButton.setStyleSheet('''
        QToolButton {
            font-size: 24px;
            background-color: #3b3e45;
            border: 2px solid #7289da;
            border-radius: 10px;
            padding: 2px;
            color: #ffffff;
        }
        QToolButton:hover {
            background-color: #3b3e45;
            border: 2px solid #99aab5;
        }
        QToolButton:pressed {
            background-color: #23272a;
            border: 2px solid #7289da;
        }
        ''')
        self.toolBoxLayout.addWidget(addTrafoButton)

        #   Add Load button
        addLoadButton = QToolButton()
        addLoadButton.setText('Lo')
        addLoadButton.setStyleSheet('''
        QToolButton {
            font-size: 24px;
            background-color: #3b3e45;
            border: 2px solid #7289da;
            border-radius: 10px;
            padding: 2px;
            color: #ffffff;
        }
        QToolButton:hover {
            background-color: #3b3e45;
            border: 2px solid #99aab5;
        }
        QToolButton:pressed {
            background-color: #23272a;
            border: 2px solid #7289da;
        }
        ''')
        self.toolBoxLayout.addWidget(addLoadButton)

        # Grid Layout
        self.grid = Grid(32)
        self.mainLayout.addWidget(self.grid, 10)
        
        # Main Widget
        widget = QWidget()
        widget.setLayout(self.mainLayout)
        widget.setStyleSheet('''
            background-color: #23272a
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
        self.loadProject.exec()

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
        if self.projectName is None:
            self.getProjectNameDialog.exec()
            if not self.getProjectNameDialog.nameError:
                self.projectName = self.getProjectNameDialog.projectName
        self.grid.projectName = self.projectName
        self.grid.insertBusMode = True
        self.update()

    def addLine(self) -> None:
        self.grid.insertBusMode = False
        self.grid.insertLineMode = True
        self.update()

    def setSelectMode(self) -> None:
        self.grid.insertBusMode = False
        self.grid.insertLineMode = False
        self.update()

