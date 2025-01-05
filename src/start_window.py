# Imports 
import os
import csv
from os.path import isdir
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QLineEdit, QListWidget, QListWidgetItem, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QMessageBox, QWidget, QScrollBar

# Other Main Project Dialogs
class StartUp(QDialog):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.projectName = None
        self.nameError = False
        self.usrPath = './user_data/'
        self.exPath = './examples/'
        self.projectPath = None
        self.busCSV = None
        self.guiCSV = None
        self.lineCSV = None
        self.loaded = False

        # Making the necessary folders if not there
        if not isdir(self.usrPath):
            os.mkdir(self.usrPath)
        if not isdir(self.exPath):
            os.mkdir(self.exPath)

        self.usrProList = os.listdir(self.usrPath)
        self.exProList = os.listdir(self.exPath)
        print('User projects path:', self.usrProList)
        print('Example projects path:', self.exProList)

        # Here's the window
        self.setWindowTitle('New Project')
        self.setFixedSize(620, 400)
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
        self.title = QLabel('Welcome to BADSILENT (Biblically Accurate DigSilent!)')
        self.title.setStyleSheet('''
            color: #ffffff;
            border: 2px solid #7289da;
            border-radius: 5px;
            padding: 8px;
        ''')
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # New Project
        self.newProjectWidget = QWidget()
        self.newProjectLayout = QHBoxLayout()
        self.nameInputLabel = QLabel('New Project Name:')
        self.nameInputLabel.setStyleSheet('color: #ffffff;')
        self.nameInput = QLineEdit(self)
        self.nameInput.setStyleSheet('''
            color: #ffffff;
            background-color: #3b3e45;
            border: 1px solid #7289da;
            border-radius: 5px;
            padding: 6px;
        ''')
        self.nameInput.setPlaceholderText('Pick a name for your Network')

        # Button Box
        buttonStr = 'Start New Project'
        self.newProButton = QPushButton()
        self.newProButton.setText(buttonStr)
        self.newProButton.clicked.connect(self.startProject)
        self.newProButton.setStyleSheet('''
            color: #ffffff;
            background-color: #3b3e45;
            border: 1px solid #7289da;
            border-radius: 5px;
            padding: 7px;
        ''')

        self.newProjectLayout.addWidget(self.nameInput,6)
        self.newProjectLayout.addWidget(self.newProButton, 2)
        self.newProjectWidget.setLayout(self.newProjectLayout)

        # Load Box
        self.loadWidget = QWidget()
        self.loadBox = QHBoxLayout()
        self.loadWidget.setStyleSheet('''
        QLabel {
            color: #ffffff;
        }
        QListWidget {
            color: #dddddd;
            background-color: #3b3e45;
            border: 1px solid #7289da;
            border-radius: 10px;
            padding: 2px;
        }
        QScrollBar {
            color: #ffffff;
            background-color: #3b3e45;
        }
        ''')

        # Load User Projects Scorllable 
        self.userProWidget = QWidget()
        self.userProBox = QVBoxLayout()
        self.loaderLabel = QLabel('Load User Projects:')
        self.loaderLabel.setStyleSheet('color: #ffffff;')
        self.projectBoxList = QListWidget(self)
        for path in self.usrProList:
            item = QListWidgetItem(path)
            self.projectBoxList.addItem(item)
        self.projectBoxList.setGeometry(0, 0, 420, 300)
        self.proBoxScrollBar = QScrollBar(self)
        self.projectBoxList.setVerticalScrollBar(self.proBoxScrollBar)
        self.projectBoxList.activated.connect(self.usrNameChanger)
        self.userProBox.addWidget(self.loaderLabel)
        self.userProBox.addWidget(self.projectBoxList)
        self.userProWidget.setLayout(self.userProBox)

        # Example Projects Scorllable 
        self.exProWidget = QWidget()
        self.exampleBox = QVBoxLayout()
        self.exLoaderLabel = QLabel('Load IEEE Examples:')
        self.exLoaderLabel.setStyleSheet('color: #ffffff;')
        self.exBoxList = QListWidget(self)
        for path in self.exProList:
            item = QListWidgetItem(path)
            self.exBoxList.addItem(item)
        self.exBoxList.setGeometry(0, 0, 420, 300)
        self.exBoxScrollBar = QScrollBar(self)
        self.exBoxList.setVerticalScrollBar(self.exBoxScrollBar)
        self.exBoxList.activated.connect(self.exNameChanger)
        self.exampleBox.addWidget(self.exLoaderLabel)
        self.exampleBox.addWidget(self.exBoxList)
        self.exProWidget.setLayout(self.exampleBox)
        self.loadBox.addWidget(self.userProWidget)
        self.loadBox.addWidget(self.exProWidget)
        self.loadWidget.setLayout(self.loadBox)
        
        # self.loadLabel = QLabel('or Select & Load a Project:')
        # self.loadLabel.setStyleSheet('color: #ffffff;')

        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.nameInputLabel)
        layout.addWidget(self.newProjectWidget)
        # layout.addWidget(self.loadLabel)
        layout.addWidget(self.loadWidget)
        self.setLayout(layout)

    def exNameChanger(self, index) -> None:
        self.projectName = self.exProList[index.row()]
        self.projectPath = os.path.join(self.exPath, self.projectName)
        self.load()
        print(self.projectPath)

    def usrNameChanger(self, index) -> None:
        self.projectName = self.usrProList[index.row()]
        self.projectPath = os.path.join(self.usrPath, self.projectName)
        self.load()
        print(self.projectPath)

    def load(self) -> None:
        if self.projectPath is not None:
            self.nameError = False
            self.loaded = True
            self.accept()
        else:
            QMessageBox.warning(self, 'No Project Loaded',
                'You need to select a project', QMessageBox.StandardButton.Ok)
            self.nameError = True

    def startProject(self) -> None:
        self.projectName = self.nameInput.text()
        self.projectPath = os.path.join(self.usrPath, self.projectName)

        if self.projectName == '':
            QMessageBox.warning(self, 'Name Error',
                'You need to type in a name.', QMessageBox.StandardButton.Ok)
            self.nameError = True

        else:
            self.nameError = False

        if not self.nameError:
            if os.path.isdir(self.projectPath):
                QMessageBox.warning(self, 'Project Exists',
                    'A Project with the same name exists.', QMessageBox.StandardButton.Ok)
                self.nameError = True

            else:
                self.nameError = False
                os.mkdir(self.projectPath)
                self.accept()

        # Adding Headers and Making CSVs
        if not self.nameError:
            self.busCSV = self.usrPath + self.projectName + '/Buses.csv'
            self.lineCSV = self.usrPath + self.projectName + '/Lines.csv'
            self.guiCSV = self.usrPath + self.projectName + '/GUI.csv'
            with open(self.guiCSV, 'a', newline = '') as file:
                writer = csv.DictWriter(file,fieldnames=['dist','paths'])
                writer.writeheader()
            print(f'-> GUI header appended to {self.lineCSV} successfuly.')
            with open(self.busCSV, 'a', newline = '') as file:
                writer = csv.DictWriter(file,fieldnames=['id', 'bType', 'vMag', 'vAng',
                                                         'P', 'Q', 'name', 'pos',
                                                         'capacity', 'orient', 'points'])
                writer.writeheader()
            print(f'-> Bus header appended to {self.busCSV} successfuly.')
            with open(self.lineCSV, 'a', newline = '') as file:
                writer = csv.DictWriter(file,fieldnames=['bus1id','bus2id','R','X','len',
                                                         'vBase'])
                writer.writeheader()
            print(f'-> Line header appended to {self.lineCSV} successfuly.')

