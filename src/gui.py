# Main GUI setup and window management

# Imports
from PyQt6.QtCore import QSize
from guiComponents import Color,Grid
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QGridLayout, QHBoxLayout, QMainWindow, QVBoxLayout, QWidget, QToolButton

# Main Window Object
class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle('DickSilent!')
        self.setMinimumSize(800, 700)

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
        selectButton.setStyleSheet('''
        QToolButton {
            background-color: #3b3e45;
            border-radius: 10px;
            padding: 2px;
            color: #ffffff;
        }
        QToolButton:hover {
            background-color: #3b3e45;
        }
        QToolButton:pressed {
            background-color: #23272a;
        }
        ''')
        self.toolBoxLayout.addWidget(selectButton)

        #   Add Generator button
        addGenButton = QToolButton()
        addGenButton.setText('G')
        addGenButton.setStyleSheet('''
        QToolButton {
            font-size: 24px;
            background-color: #3b3e45;
            border-radius: 10px;
            padding: 2px;
            color: #ffffff;
        }
        QToolButton:hover {
            background-color: #3b3e45;
        }
        QToolButton:pressed {
            background-color: #23272a;
        }
        ''')
        self.toolBoxLayout.addWidget(addGenButton)

        #   Add Bus button
        addBusButton = QToolButton()
        addBusButton.setText('B')
        addBusButton.setStyleSheet('''
        QToolButton {
            font-size: 24px;
            background-color: #3b3e45;
            border-radius: 10px;
            padding: 2px;
            color: #ffffff;
        }
        QToolButton:hover {
            background-color: #3b3e45;
        }
        QToolButton:pressed {
            background-color: #23272a;
        }
        ''')
        self.toolBoxLayout.addWidget(addBusButton)

        self.mainLayout.addWidget(self.toolBox)

        # Grid Layout
        self.grid = Grid(30)
        # self.gridLayout = QVBoxLayout()
        # self.grid.setLayout(self.gridLayout)
        # self.grid.setStyleSheet('''
        #     background-color: #3b3e45;
        #     border-radius: 12px;
        # ''')
        self.mainLayout.addWidget(self.grid, 10)
        
        # Main Widget
        widget = QWidget()
        widget.setLayout(self.mainLayout)
        widget.setStyleSheet('''
            background-color: #23272a
        ''')
        self.setCentralWidget(widget)

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

    def gsLoadFlow(self) -> None:
        pass

    def nrLoadFlow(self) -> None:
        pass

    def fdLoadFlow(self) -> None:
        pass
