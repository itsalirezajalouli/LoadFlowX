# Imports 
import os
import csv
from os.path import isdir
from PyQt6.QtWidgets import QDialog, QLineEdit, QPushButton, QVBoxLayout, QLabel, QMessageBox 

# Other Main Project Dialogs
class GetProjectNameDialog(QDialog):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.projectName = None
        self.nameError = False
        self.root = './user_data/'
        self.busCSV = None

        if not isdir(self.root):
            os.mkdir(self.root)

        self.setWindowTitle('New Project')
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
        self.title = QLabel('New Load Flow Project')
        self.title.setStyleSheet('''
            color: #ffffff;
            border: 2px solid #7289da;
            border-radius: 5px;
            padding: 8px;
        ''')
        self.nameInputLabel = QLabel('Project Name:')
        self.nameInputLabel.setStyleSheet('color: #ffffff;')
        self.nameInput = QLineEdit(self)
        self.nameInput.setPlaceholderText('Pick a name for your Network')

        # Button Box
        self.startProjectButton = QPushButton()
        self.startProjectButton.setText('Start Project')
        self.startProjectButton.clicked.connect(self.startProject)

        layout = QVBoxLayout()
        layout.addWidget(self.nameInputLabel)
        layout.addWidget(self.nameInput)
        layout.addWidget(self.startProjectButton)
        self.setLayout(layout)

    def startProject(self) -> None:
        self.projectName = self.nameInput.text()
        projectPath = os.path.join(self.root, self.projectName)

        if not isdir('./user_data'):
            os.mkdir('./user_data')
        if os.path.isdir(projectPath):
            QMessageBox.warning(self, 'Project Exists',
                'A Project with the same name exists.', QMessageBox.StandardButton.Ok)
            self.nameError = True
        else:
            self.nameError = False
            os.mkdir(projectPath)
            self.accept()

        # Adding Headers and Making CSVs
        self.busCSV = self.root + self.projectName + '/Buses.csv'
        with open(self.busCSV, 'a', newline = '') as file:
            writer = csv.DictWriter(file,fieldnames=['id','name','pos','bType','vMag',
                                                     'vAng','P','Q'])
            writer.writeheader()

        print(f'header succefully added to {self.busCSV}')

class LoadProject(QDialog):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setWindowTitle('Load Project')
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
        self.nameInputLabel = QLabel('Project Name:')
        self.nameInputLabel.setStyleSheet('color: #ffffff;')
        self.root = './user_data/'
        if not isdir(self.root):
            os.mkdir(self.root)
        # TODO!: Make a scroller

