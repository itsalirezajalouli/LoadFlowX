# Main GUI setup and window management

# Imports
from PyQt6.QtGui import QAction 
from PyQt6.QtWidgets import QGridLayout, QHBoxLayout, QMainWindow, QVBoxLayout, QWidget
from guiComponents import Color

# Main Window Object
class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle('DickSilent!')
        self.setFixedSize(1300, 700)

        # Menu Bar
        menu = self.menuBar()
        menu.setStyleSheet('''
            background-color: #2c2f33;
            color: #fff;
        ''')
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
        layout = QHBoxLayout()
        layout.addWidget(Color('red'), 1)
        layout.addWidget(Color('orange'), 12)
        layout.addWidget(Color('blue'), 3)
        widget = QWidget()
        widget.setLayout(layout)
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
