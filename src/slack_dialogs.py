# Dialogs for slack
from psa_components import Slack
from PyQt6.QtWidgets import QDialog, QLabel, QWidget, QHBoxLayout, QLineEdit, QComboBox, QVBoxLayout, QDialogButtonBox, QMessageBox

class AddSlackDialog(QDialog):
    def __init__(self, parent, bus) -> None:
        super().__init__(parent)
        self.projectPath = None
        self.inputError = False
        self.bus = bus
        self.setWindowTitle('Add Bus')
        self.setStyleSheet('''
        QDialog {
            font-size: 24px;
            color: #ffffff;
            border: 2px solid #7289da;
            border-radius: 10px;
            padding: 2px;
        }
        QLineEdit {
            font-size: 12px;
            color: #ffffff;
        }
        QLabel {
            font-size: 12px;
            color: #ffffff;
        }
        QComboBox {
            font-size: 12px;
            color: #ffffff;
        }
        ''')
        self.title = QLabel('Add Slack to Network')
        self.title.setStyleSheet('''
            color: #ffffff;
            border: 2px solid #7289da;
            border-radius: 5px;
            padding: 8px;
        ''')
        
        self.vmPU = None

        # Bus Name Input Box
        self.nameInputLabel = QLabel('Slack Name:')
        self.nameInputLabel.setStyleSheet('color: #ffffff;')
        self.nameInput = QLineEdit(self)
        self.nameInput.setPlaceholderText('Set a name for the grid')

        # Line Z Input Box
        # self.zLabel = QLabel('Impedances:')
        # self.zLabel.setStyleSheet('color: #ffffff;')
        # self.zWidget = QWidget()
        # self.zHBox = QHBoxLayout()
        # self.rInput = QLineEdit(self)
        # self.rInput.setPlaceholderText('R')
        # self.xInput = QLineEdit(self)
        # self.xInput.setPlaceholderText('X')
        # self.rUnitDropDown = QComboBox(self) 
        # self.rUnitDropDown.addItem('PU')
        # self.rUnitDropDown.addItem('Kohm')
        # self.xUnitDropDown = QComboBox(self) 
        # self.xUnitDropDown.addItem('PU')
        # self.xUnitDropDown.addItem('Kohm')
        # self.zHBox.addWidget(self.rInput)
        # self.zHBox.addWidget(self.rUnitDropDown)
        # self.zHBox.addWidget(self.xInput)
        # self.zHBox.addWidget(self.xUnitDropDown)
        # self.zWidget.setLayout(self.zHBox)

        # Length & V Base
        self.lenLabel = QLabel('Voltage:')
        self.lenLabel.setStyleSheet('color: #ffffff;')
        self.lenHBox = QHBoxLayout()
        self.lenInput = QLineEdit(self)
        self.lenInput.setPlaceholderText('i.e. 1.02 p.u')
       # self.vBaseInput = QLineEdit(self)
        # self.vBaseInput.setPlaceholderText('V Base')
        self.lenUnitDropDown = QComboBox(self) 
        self.lenUnitDropDown.addItem('PU')
        # self.vbUnitDropDown = QComboBox(self) 
        # self.vbUnitDropDown.addItem('PU')
        # self.vbUnitDropDown.addItem('KV')
        self.lenHBox.addWidget(self.lenLabel)
        self.lenHBox.addWidget(self.lenInput)
        self.lenHBox.addWidget(self.lenUnitDropDown)
        # self.lenHBox.addWidget(self.vBaseInput)
        # self.lenHBox.addWidget(self.vbUnitDropDown)
        self.lenWidget = QWidget()
        self.lenWidget.setLayout(self.lenHBox)

        # Button Box
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.accepted.connect(self.accept)

        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.nameInputLabel)
        layout.addWidget(self.nameInput)
        # layout.addWidget(self.zWidget)
        layout.addWidget(self.lenWidget)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

    def accept(self) -> None:
        inputList = []
        # inputList.append(self.rInput.text())
        # inputList.append(self.xInput.text())
        inputList.append(self.lenInput.text())
        inputList.append(self.nameInput.text())
        if '' in inputList:
            self.inputError = True
            QMessageBox.warning(self, 'Fill all the fields.',
                'No field can be empty! Please fill them all.', QMessageBox.StandardButton.Ok)
            return
        else:
            self.inputError = False
        slack = Slack(
            bus = self.bus,
            vmPU = float(self.lenInput.text()),
        )
        slack.append2CSV(self.projectPath)
        super().accept()
