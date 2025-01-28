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
        # self.canceled = False
        self.vUnit = 'KV'
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
        self.projectName = None
        self.inputError = False
        
        self.busId = None
        self.busPos = None
        self.busType = BusType.SLACK 
        self.capacity = None
        self.orient = None
        self.points = None

        # Bus Name Input Box
        self.nameWidget = QWidget()
        self.nameHBox = QHBoxLayout()
        self.nameInputLabel = QLabel('Bus Name:')
        self.nameInput = QLineEdit(self)
        self.nameInputLabel.setStyleSheet('color: #ffffff;')
        self.nameInput.setPlaceholderText('Set Bus Name')
        self.nameHBox.addWidget(self.nameInputLabel)
        starLabel = QLabel('*  ')
        starLabel.setStyleSheet('color: #f04747;')
        self.nameHBox.addWidget(starLabel)
        self.nameHBox.addWidget(self.nameInput)
        self.nameWidget.setLayout(self.nameHBox)

        # V Magnitude Input Box
        self.vInputLabel = QLabel('Nominal Voltage:')
        self.vInputLabel.setStyleSheet('color: #ffffff;')
        self.vWidget = QWidget()
        self.vHBox = QHBoxLayout()
        self.vMagLabel = QLabel('Vn: ')
        self.vMagInput = QLineEdit(self)
        self.vMagInput.setPlaceholderText('i.e. 345 KV')
        self.vUnitDropDown = QComboBox(self) 
        self.vUnitDropDown.addItem('KV')
        self.vUnitDropDown.addItem('PU')
        self.vUnitDropDown.activated.connect(self.perUnitActivator)
        self.vHBox.addWidget(self.vMagLabel)
        starLabel = QLabel('*  ')
        starLabel.setStyleSheet('color: #f04747;')
        self.vHBox.addWidget(starLabel)
        self.vHBox.addWidget(self.vMagInput)
        self.vHBox.addWidget(self.vUnitDropDown)
        self.vWidget.setLayout(self.vHBox)

        self.vMagInput.setValidator(QDoubleValidator())

        # Zone Input Box
        self.zWidget = QWidget()
        self.zHBox = QHBoxLayout()
        self.zoneLabel = QLabel('Zone: ')
        self.zoneInput = QLineEdit(self)
        self.zoneInput.setPlaceholderText('i.e. 1,...')
        self.zHBox.addWidget(self.zoneLabel)
        self.zHBox.addWidget(self.zoneInput)
        self.zWidget.setLayout(self.zHBox)

        # Button Box
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.accepted.connect(self.accept)

        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.nameWidget)
        layout.addWidget(self.vInputLabel)
        layout.addWidget(self.vWidget)
        layout.addWidget(self.zWidget)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

    # Handling per unit combo box
    def perUnitActivator(self, index) -> None:
        if index == 0: 
            if self.vUnit == 'PU':
                self.vBaseLabel.deleteLater()
                self.vBaseStarLabel.deleteLater()
                self.vBaseInput.deleteLater()
            self.vUnit = 'KV'
            self.vMagInput.setPlaceholderText('i.e. 345 KV')
            self.vWidget.setLayout(self.vHBox)

        elif index == 1:
            self.vUnit = 'PU'
            self.vMagInput.setPlaceholderText('i.e. 1.02 PU')
            self.vBaseLabel = QLabel('Vb: ')
            self.vBaseLabel.setStyleSheet('color: #ffffff;')
            self.vBaseStarLabel = QLabel('*  ')
            self.vBaseStarLabel.setStyleSheet('color: #f04747;')
            self.vBaseInput = QLineEdit(self)
            self.vBaseInput.setPlaceholderText('i.e. 220 KV')
            self.vHBox.addWidget(self.vBaseLabel)
            self.vHBox.addWidget(self.vBaseStarLabel)
            self.vHBox.addWidget(self.vBaseInput)

    def accept(self) -> None:
        # Handling Same Name Bus Names
        csvPath = self.projectPath + '/Buses.csv'
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
        # inputList.append(self.vAngInput.text())
        # inputList.append(self.pInput.text())
        # inputList.append(self.qInput.text())
        if '' in inputList:
            self.inputError = True
            QMessageBox.warning(self, 'Fill all the necessary fields.',
                'No necessary field can be empty! Please fill them.', QMessageBox.StandardButton.Ok)
            return
        else:
            self.inputError = False

        # Zone is not necessary
        zone = self.zoneInput.text()
        if zone == '':
            zone = 0

        # Handling per unit
        vMag = self.vMagInput.text()
        if self.vUnit == 'PU':
            vMag = float(self.vMagInput.text()) * float(self.vBaseInput.text())


        # Creating the BusBar
        bus = BusBar(
            id = self.busId,
            pos = self.busPos,
            name = self.nameInput.text(),
            bType = self.busType, 
            zone = int(zone),
            vMag = float(vMag),
            # P = float(self.pInput.text()),
            # Q = float(self.qInput.text()),
            capacity = self.capacity,
            orient = self.orient,
            points = self.points,
        )
        bus.log()
        bus.append2CSV(self.projectPath)
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

        self.projectPath = None
        self.inputError = False
        self.previousName = None
        
        self.busId = None
        self.busPos = None
        self.busType = BusType.SLACK 
        self.capacity = None
        self.orient = None
        self.points = None

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
        csvPath = self.projectPath + '/Buses.csv'
        if os.path.exists(csvPath):
            with open(csvPath) as csvfile:
                reader = csv.DictReader(csvfile)
                names = [row['name'] for row in reader]
                if self.nameInput.text() != self.previousName:
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
            capacity = self.capacity,
            orient = self.orient,
            points = self.points,
        )
        bus.log()
        bus.editCSV(self.projectPath, self.previousName)
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
            capacity = self.capacity,
            orient = self.orient,
            points = self.points,
        )
        bus.log()
        bus.editCSV(self.projectPath, self.previousName)
        super().reject()
