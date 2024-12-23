# Imports 
import os
import csv
from psa_components import BusBar, BusType
from PyQt6.QtGui import QDoubleValidator
from PyQt6.QtWidgets import QComboBox, QDialog, QHBoxLayout, QLineEdit, QVBoxLayout, QWidget, QLabel, QDialogButtonBox, QMessageBox

# Dialogs Related to Bus Objects
class AddBusDialog(QDialog):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setWindowTitle('Add Bus Bar')
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
        self.title = QLabel('Add Bus Bar to Network')
        self.title.setStyleSheet('''
            color: #ffffff;
            border: 2px solid #7289da;
            border-radius: 5px;
            padding: 8px;
        ''')
        
        self.busId = None
        self.busPos = None
        self.busType = BusType.SLACK 
        self.projectName = None
        self.inputError = False

        # Bus Name Input Box
        self.nameInputLabel = QLabel('Bus Name:')
        self.nameInputLabel.setStyleSheet('color: #ffffff;')
        self.nameInput = QLineEdit(self)
        self.nameInput.setPlaceholderText('Set Your Bus Name')

        # Bus Type Combo Box
        self.typeInputLabel = QLabel('Bus Type:')
        self.typeInputLabel.setStyleSheet('color: #ffffff;')
        self.busTypeDropDown = QComboBox(self) 
        self.busTypeDropDown.addItem('SLACK')
        self.busTypeDropDown.addItem('PV')
        self.busTypeDropDown.addItem('PQ')
        self.busTypeDropDown.activated.connect(self.busTypeActivator)

        # V Magnitude & Angle Input Box
        self.vInputLabel = QLabel('Voltage (|V|∠δ):')
        self.vInputLabel.setStyleSheet('color: #ffffff;')
        self.vWidget = QWidget()
        self.vHBox = QHBoxLayout()
        self.vMagInput = QLineEdit(self)
        self.vMagInput.setPlaceholderText('|V|')
        self.vAngInput = QLineEdit(self)
        self.vAngInput.setPlaceholderText('δ')
        self.vUnitDropDown = QComboBox(self) 
        self.vUnitDropDown.addItem('PU')
        self.vUnitDropDown.addItem('KV')
        self.vUnitDropDown.addItem('V')
        self.vUnitDropDown.activated.connect(self.vMagUnitActivator)
        self.vDegreeTypeDropDown = QComboBox(self) 
        self.vDegreeTypeDropDown.addItem('Deg')
        self.vDegreeTypeDropDown.addItem('Rad')
        self.vHBox.addWidget(self.vMagInput)
        self.vHBox.addWidget(self.vUnitDropDown)
        self.vHBox.addWidget(self.vAngInput)
        self.vHBox.addWidget(self.vDegreeTypeDropDown)
        self.vWidget.setLayout(self.vHBox)

        # P & Q Input Box
        self.pqInputLabel = QLabel('Active & Passive Power:')
        self.pqInputLabel.setStyleSheet('color: #ffffff;')
        self.pqWidget = QWidget()
        self.pqHBox = QHBoxLayout()
        self.pInput = QLineEdit(self)
        self.pInput.setPlaceholderText('P')
        self.qInput = QLineEdit(self)
        self.qInput.setPlaceholderText('Q')
        self.pUnitDropDown = QComboBox(self) 
        self.pUnitDropDown.addItem('PU')
        self.pUnitDropDown.addItem('KW')
        self.qUnitDropDown = QComboBox(self) 
        self.qUnitDropDown.addItem('PU')
        self.qUnitDropDown.addItem('KVA')
        self.pqHBox.addWidget(self.pInput)
        self.pqHBox.addWidget(self.pUnitDropDown)
        self.pqHBox.addWidget(self.qInput)
        self.pqHBox.addWidget(self.qUnitDropDown)
        self.pqWidget.setLayout(self.pqHBox)

        self.vMagInput.setValidator(QDoubleValidator())
        self.vAngInput.setValidator(QDoubleValidator())
        self.qInput.setValidator(QDoubleValidator())
        self.pInput.setValidator(QDoubleValidator())

        # Button Box
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.accepted.connect(self.accept)

        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.nameInputLabel)
        layout.addWidget(self.nameInput)
        layout.addWidget(self.typeInputLabel)
        layout.addWidget(self.busTypeDropDown)
        layout.addWidget(self.vInputLabel)
        layout.addWidget(self.vWidget)
        layout.addWidget(self.pqInputLabel)
        layout.addWidget(self.pqWidget)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

    # Handling bus type combo box
    def busTypeActivator(self, index) -> None:
        if index == 0: 
            self.busType = BusType.SLACK
        elif index == 1:
            self.busType = BusType.PV
        elif index == 2:
            self.busType = BusType.PQ

    def vMagUnitActivator(self, index) -> None:
        pass

    def accept(self) -> None:
        # Handling Same Name Bus Names
        projectPath = os.path.join('./user_data/', self.projectName)
        csvPath = projectPath + '/Buses.csv'
        if os.path.exists(csvPath):
            with open(csvPath) as csvfile:
                reader = csv.DictReader(csvfile)
                names = [row['name'] for row in reader]
                if self.nameInput.text() in names:
                    self.inputError = True
                    QMessageBox.warning(self, 'Clone Bus Name',
                        'A bus with the same name already exists.', QMessageBox.StandardButton.Ok)
                    return

        # Handling Empty Inputs Error
        inputList = []
        inputList.append(self.nameInput.text())
        inputList.append(self.vMagInput.text())
        inputList.append(self.vAngInput.text())
        inputList.append(self.pInput.text())
        inputList.append(self.qInput.text())
        if '' in inputList:
            self.inputError = True
            QMessageBox.warning(self, 'Fill all the fields.',
                'No field can be empty! Please fill them all.', QMessageBox.StandardButton.Ok)
            return
        else:
            self.inputError = False
        # Creating the BusBar
        bus = BusBar(
            id = self.busId,
            pos = self.busPos,
            name = self.nameInput.text(),
            bType = self.busType, 
            vAng = float(self.vAngInput.text()),
            vMag = float(self.vMagInput.text()),
            P = float(self.pInput.text()),
            Q = float(self.qInput.text()),
        )
        bus.log()
        projectPath = os.path.join('./user_data/', self.projectName)
        bus.append2CSV(projectPath)
        super().accept()

class EditBusDialog(QDialog):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setWindowTitle('Edit Bus Bar')
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
        self.title = QLabel('Edit Selected Bus Bar')
        self.title.setStyleSheet('''
            color: #ffffff;
            border: 2px solid #7289da;
            border-radius: 5px;
            padding: 8px;
        ''')
        
        self.busId = None
        self.busPos = None
        self.busType = BusType.SLACK 
        self.projectName = None
        self.inputError = False
        self.previousName = None

        # Bus Name Input Box
        self.nameInputLabel = QLabel('Bus Name:')
        self.nameInputLabel.setStyleSheet('color: #ffffff;')
        self.nameInput = QLineEdit(self)
        self.nameInput.setPlaceholderText('Set Your Bus Name')

        # Bus Type Combo Box
        self.typeInputLabel = QLabel('Bus Type:')
        self.typeInputLabel.setStyleSheet('color: #ffffff;')
        self.busTypeDropDown = QComboBox(self) 
        self.busTypeDropDown.addItem('SLACK')
        self.busTypeDropDown.addItem('PV')
        self.busTypeDropDown.addItem('PQ')
        self.busTypeDropDown.activated.connect(self.busTypeActivator)

        # V Magnitude & Angle Input Box
        self.vInputLabel = QLabel('Voltage (|V|∠δ):')
        self.vInputLabel.setStyleSheet('color: #ffffff;')
        self.vWidget = QWidget()
        self.vHBox = QHBoxLayout()
        self.vMagInput = QLineEdit(self)
        self.vMagInput.setPlaceholderText('|V|')
        self.vAngInput = QLineEdit(self)
        self.vAngInput.setPlaceholderText('δ')
        self.vUnitDropDown = QComboBox(self) 
        self.vUnitDropDown.addItem('PU')
        self.vUnitDropDown.addItem('KV')
        self.vUnitDropDown.addItem('V')
        self.vDegreeTypeDropDown = QComboBox(self) 
        self.vDegreeTypeDropDown.addItem('Deg')
        self.vDegreeTypeDropDown.addItem('Rad')
        self.vHBox.addWidget(self.vMagInput)
        self.vHBox.addWidget(self.vUnitDropDown)
        self.vHBox.addWidget(self.vAngInput)
        self.vHBox.addWidget(self.vDegreeTypeDropDown)
        self.vWidget.setLayout(self.vHBox)

        # P & Q Input Box
        self.pqInputLabel = QLabel('Active & Passive Power:')
        self.pqInputLabel.setStyleSheet('color: #ffffff;')
        self.pqWidget = QWidget()
        self.pqHBox = QHBoxLayout()
        self.pInput = QLineEdit(self)
        self.pInput.setPlaceholderText('P')
        self.qInput = QLineEdit(self)
        self.qInput.setPlaceholderText('Q')
        self.pUnitDropDown = QComboBox(self) 
        self.pUnitDropDown.addItem('PU')
        self.pUnitDropDown.addItem('KW')
        self.qUnitDropDown = QComboBox(self) 
        self.qUnitDropDown.addItem('PU')
        self.qUnitDropDown.addItem('KVA')
        self.pqHBox.addWidget(self.pInput)
        self.pqHBox.addWidget(self.pUnitDropDown)
        self.pqHBox.addWidget(self.qInput)
        self.pqHBox.addWidget(self.qUnitDropDown)
        self.pqWidget.setLayout(self.pqHBox)

        self.vMagInput.setValidator(QDoubleValidator())
        self.vAngInput.setValidator(QDoubleValidator())
        self.qInput.setValidator(QDoubleValidator())
        self.pInput.setValidator(QDoubleValidator())

        # Button Box
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.accepted.connect(self.accept)

        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.nameInputLabel)
        layout.addWidget(self.nameInput)
        layout.addWidget(self.typeInputLabel)
        layout.addWidget(self.busTypeDropDown)
        layout.addWidget(self.vInputLabel)
        layout.addWidget(self.vWidget)
        layout.addWidget(self.pqInputLabel)
        layout.addWidget(self.pqWidget)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

    def busTypeActivator(self, index) -> None:
        if index == 0: 
            self.busType = BusType.SLACK
        elif index == 1:
            self.busType = BusType.PV
        elif index == 2:
            self.busType = BusType.PQ

    def accept(self) -> None:
        # Handling Same Name Bus Names
        projectPath = os.path.join('./user_data/', self.projectName)
        csvPath = projectPath + '/Buses.csv'
        if os.path.exists(csvPath):
            with open(csvPath) as csvfile:
                reader = csv.DictReader(csvfile)
                names = [row['name'] for row in reader]
                if self.nameInput.text() in names:
                    self.inputError = True
                    QMessageBox.warning(self, 'Clone Bus Name',
                        'A bus with the same name already exists.', QMessageBox.StandardButton.Ok)
                    return

        # Handling Empty Inputs Error
        inputList = []
        inputList.append(self.nameInput.text())
        inputList.append(self.vMagInput.text())
        inputList.append(self.vAngInput.text())
        inputList.append(self.pInput.text())
        inputList.append(self.qInput.text())
        if '' in inputList:
            self.inputError = True
            QMessageBox.warning(self, 'Fill all the fields.',
                'No field can be empty! Please fill them all.', QMessageBox.StandardButton.Ok)
            return
        else:
            self.inputError = False

        # Edit the BusBar
        bus = BusBar(
            id = self.busId,
            pos = self.busPos,
            name = self.nameInput.text(),
            bType = self.busType, 
            vAng = float(self.vAngInput.text()),
            vMag = float(self.vMagInput.text()),
            P = float(self.pInput.text()),
            Q = float(self.qInput.text()),
        )
        bus.log()
        projectPath = os.path.join('./user_data/', self.projectName)
        bus.editCSV(projectPath, self.previousName)
        super().accept()

    def reject(self) -> None:
        # Edit the BusBar
        bus = BusBar(
            id = self.busId,
            pos = self.busPos,
            name = self.nameInput.text(),
            bType = self.busType, 
            vAng = float(self.vAngInput.text()),
            vMag = float(self.vMagInput.text()),
            P = float(self.pInput.text()),
            Q = float(self.qInput.text()),
        )
        bus.log()
        projectPath = os.path.join('./user_data/', self.projectName)
        bus.editCSV(projectPath, self.previousName)
        super().reject()
