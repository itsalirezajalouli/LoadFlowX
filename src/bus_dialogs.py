# Imports 
import os
from csv import DictReader, DictWriter
from psa_components import BusBar, BusType
from PyQt6.QtGui import QDoubleValidator
from PyQt6.QtWidgets import (QComboBox, QDialog, QHBoxLayout, QLineEdit, 
                           QVBoxLayout, QWidget, QLabel, QDialogButtonBox, 
                           QMessageBox, QCheckBox)

class AddBusDialog(QDialog):
    def __init__(self, parent, theme = 'dark') -> None:
        super().__init__(parent)
        self.setWindowTitle('Add Bus Bar')
        self.vUnit = 'KV'
        self.canceled = False
        self.extraParams = False

        # Apply theme-specific styles
        self.setStyleSheet(f'''
        QDialog {{
            font-size: 14px;
            color: {'#ffffff' if theme == 'dark' else '#000000'};
            border: 2px solid #7289da;
            border-radius: 10px;
            padding: 2px;
        }}
        QLineEdit {{
            font-size: 12px;
            color: {'#ffffff' if theme == 'dark' else '#000000'};
            background-color: {'#d9d9d9' if theme == 'light' else '#23272a'}
        }}
        QLabel {{
            font-size: 14px;
            color: {'#ffffff' if theme == 'dark' else '#000000'};
        }}
        QComboBox {{
            font-size: 12px;
            color: {'#ffffff' if theme == 'dark' else '#000000'};
            background-color: {'#23272a' if theme == 'dark' else '#d9d9d9'};
            border: 1px solid #7289da;
            border-radius: 5px;
        }}
        QCheckBox {{
            font-size: 12px;
            color: {'#ffffff' if theme == 'dark' else '#000000'};
        }}
        QDialogButtonBox QPushButton {{
            font-size: 12px;
            padding: 5px;
            border-radius: 5px;
            border: 1px solid #7289da;
            color: {'#ffffff' if theme == 'dark' else '#000000'};
            border-radius: 5px
        }}
        QDialogButtonBox QPushButton:hover {{
            font-size: 12px;
            background-color: #99aab5;
            padding: 5px;
            color: {'#ffffff' if theme == 'dark' else '#000000'};
            border: 1px solid #7289da;
            border-radius: 5px
        }}
        ''')

        self.title = QLabel('Add Bus Bar to Network')
        self.title.setStyleSheet(f'''
            color: {'#ffffff' if theme == 'dark' else '#000000'};
            font-weight: bold;
            border: 2px solid #7289da;
            border-radius: 5px;
            padding: 10px;
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
        self.nameInputLabel.setStyleSheet(f'color: {"#ffffff" if theme == "dark" else "#000000"};')
        self.nameInput.setPlaceholderText('Set Bus Name')
        self.nameHBox.addWidget(self.nameInputLabel)
        starLabel = QLabel('*  ')
        starLabel.setStyleSheet('color: #f04747;')
        self.nameHBox.addWidget(starLabel)
        self.nameHBox.addWidget(self.nameInput)
        self.nameWidget.setLayout(self.nameHBox)

        # V Magnitude Input Box
        self.vInputLabel = QLabel('Nominal Voltage:')
        self.vInputLabel.setStyleSheet(f'color: {"#ffffff" if theme == "dark" else "#000000"};')
        self.vWidget = QWidget()
        self.vHBox = QHBoxLayout()
        self.vMagLabel = QLabel('Vn: ')
        self.vMagInput = QLineEdit(self)
        self.vMagInput.setPlaceholderText('i.e. 345 KV')
        self.vUnitDropDown = QComboBox(self) 
        self.vUnitDropDown.addItem('KV   ')
        self.vUnitDropDown.addItem('PU   ')
        self.vUnitDropDown.activated.connect(self.perUnitActivator)
        self.vHBox.addWidget(self.vMagLabel)
        starLabel = QLabel('*  ')
        starLabel.setStyleSheet('color: #f04747;')
        self.vHBox.addWidget(starLabel)
        self.vHBox.addWidget(self.vMagInput)
        self.vHBox.addWidget(self.vUnitDropDown)
        self.vWidget.setLayout(self.vHBox)

        self.vMagInput.setValidator(QDoubleValidator())

        # Checkbox for Extra Parameters
        self.extraParamsCheckBox = QCheckBox('Extra Parameters')
        self.extraParamsCheckBox.setStyleSheet(f'color: {"#ffffff" if theme == "dark" else "#000000"};')
        self.extraParamsCheckBox.stateChanged.connect(self.toggleExtraParameters)

        # Additional Parameters Section
        self.additionalFieldsLabel = QLabel('Additional Parameters:')
        self.additionalFieldsLabel.setStyleSheet(f'color: {"#ffffff" if theme == "dark" else "#000000"};')

        # Zone Input Box
        self.zWidget = QWidget()
        self.zHBox = QHBoxLayout()
        self.zoneLabel = QLabel('Zone: ')
        self.zoneInput = QLineEdit(self)
        self.zoneInput.setPlaceholderText('i.e. 1,...')
        self.zHBox.addWidget(self.zoneLabel)
        self.zHBox.addWidget(self.zoneInput)
        self.zWidget.setLayout(self.zHBox)

        # Max and Min Voltage Widget
        self.voltageConstraintsWidget = QWidget()
        self.voltageConstraintsHBox = QHBoxLayout()
        
        self.maxVmInput = QLineEdit(self)
        self.maxVmInput.setPlaceholderText('Max Vm (p.u.)')
        self.maxVmInput.setValidator(QDoubleValidator())
        
        self.minVmInput = QLineEdit(self)
        self.minVmInput.setPlaceholderText('Min Vm (p.u.)')
        self.minVmInput.setValidator(QDoubleValidator())
        
        self.voltageConstraintsHBox.addWidget(self.maxVmInput)
        self.voltageConstraintsHBox.addWidget(self.minVmInput)
        self.voltageConstraintsWidget.setLayout(self.voltageConstraintsHBox)

        # Button Box
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.accepted.connect(self.accept)

        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.nameWidget)
        layout.addWidget(self.vInputLabel)
        layout.addWidget(self.vWidget)
        layout.addWidget(self.extraParamsCheckBox)
        layout.addWidget(self.additionalFieldsLabel)
        layout.addWidget(self.zWidget)
        layout.addWidget(self.voltageConstraintsWidget)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

        # Initially hide extra parameters
        self.toggleExtraParameters()

    def toggleExtraParameters(self):
        """Toggle visibility of extra parameter fields"""
        self.extraParams = self.extraParamsCheckBox.isChecked()
        self.additionalFieldsLabel.setVisible(self.extraParams)
        self.zWidget.setVisible(self.extraParams)
        self.voltageConstraintsWidget.setVisible(self.extraParams)

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
                reader = DictReader(csvfile)
                names = [row['name'] for row in reader]
                if self.nameInput.text() in names:
                    self.inputError = True
                    QMessageBox.warning(self, 'Clone Bus Name',
                        'A bus with the same name already exists.', QMessageBox.StandardButton.Ok)
                    return

        # Handling Empty Inputs Error
        inputList = [self.nameInput.text(), self.vMagInput.text()]
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

        # Default voltage limits if not specified
        maxVm = float(self.maxVmInput.text()) if self.maxVmInput.text() else 1.1  # Default max 1.1 p.u.
        minVm = float(self.minVmInput.text()) if self.minVmInput.text() else 0.9  # Default min 0.9 p.u.

        # Creating the BusBar with additiona l parameters
        bus = BusBar(
            id = self.busId,
            pos = self.busPos,
            name = self.nameInput.text(),
            bType = self.busType, 
            zone = int(zone),
            vMag = float(vMag),
            capacity = self.capacity,
            orient = self.orient,
            points = self.points,
            maxVm = maxVm,
            minVm = minVm
        )
        bus.log()
        bus.append2CSV(self.projectPath)
        super().accept()

    def reject(self) -> None:
        self.canceled = True
        super().accept()

class EditBusDialog(QDialog):
    def __init__(self, parent, projectPath, busName, theme='dark'):
        super().__init__(parent)
        self.setWindowTitle('Edit Bus Bar')
        self.projectPath = projectPath
        self.busName = busName
        self.vUnit = 'KV'
        self.canceled = False
        self.extraParams = False

        # Apply theme-specific styles
        self.setStyleSheet(f'''
        QDialog {{
            font-size: 14px;
            color: {'#ffffff' if theme == 'dark' else '#000000'};
            border: 2px solid #7289da;
            border-radius: 10px;
            padding: 2px;
        }}
        QLineEdit {{
            font-size: 12px;
            color: {'#ffffff' if theme == 'dark' else '#000000'};
            background-color: {'#d9d9d9' if theme == 'light' else '#23272a'}
        }}
        QLabel {{
            font-size: 14px;
            color: {'#ffffff' if theme == 'dark' else '#000000'};
        }}
        QComboBox {{
            font-size: 12px;
            color: {'#ffffff' if theme == 'dark' else '#000000'};
            background-color: {'#23272a' if theme == 'dark' else '#d9d9d9'};
            border: 1px solid #7289da;
            border-radius: 5px;
        }}
        QCheckBox {{
            font-size: 12px;
            color: {'#ffffff' if theme == 'dark' else '#000000'};
        }}
        QDialogButtonBox QPushButton {{
            font-size: 12px;
            padding: 5px;
            border-radius: 5px;
            border: 1px solid #7289da;
            color: {'#ffffff' if theme == 'dark' else '#000000'};
            border-radius: 5px
        }}
        QDialogButtonBox QPushButton:hover {{
            font-size: 12px;
            background-color: #99aab5;
            padding: 5px;
            color: {'#ffffff' if theme == 'dark' else '#000000'};
            border: 1px solid #7289da;
            border-radius: 5px
        }}
        ''')



        self.loadBusData()
        
        # UI Elements
        self.title = QLabel('Edit Bus Bar')
        self.nameInput = QLineEdit(self)
        self.nameInput.setText(self.busData['name'])
        self.nameInput.setReadOnly(True)

        self.vMagInput = QLineEdit(self)
        self.vMagInput.setText(str(self.busData['vMag']))
        self.vMagInput.setValidator(QDoubleValidator())

        self.zoneInput = QLineEdit(self)
        self.zoneInput.setText(str(self.busData['zone']))

        self.maxVmInput = QLineEdit(self)
        self.maxVmInput.setText(str(self.busData['maxVm']))
        self.maxVmInput.setValidator(QDoubleValidator())

        self.minVmInput = QLineEdit(self)
        self.minVmInput.setText(str(self.busData['minVm']))
        self.minVmInput.setValidator(QDoubleValidator())

        # Layouts
        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(QLabel('Bus Name:'))
        layout.addWidget(self.nameInput)
        layout.addWidget(QLabel('Nominal Voltage:'))
        layout.addWidget(self.vMagInput)
        layout.addWidget(QLabel('Zone:'))
        layout.addWidget(self.zoneInput)
        layout.addWidget(QLabel('Max Voltage (p.u.):'))
        layout.addWidget(self.maxVmInput)
        layout.addWidget(QLabel('Min Voltage (p.u.):'))
        layout.addWidget(self.minVmInput)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        layout.addWidget(self.buttonBox)

        self.setLayout(layout)
    
    def loadBusData(self):
        csvPath = os.path.join(self.projectPath, 'Buses.csv')
        self.busData = {}
        if os.path.exists(csvPath):
            with open(csvPath, newline='') as file:
                reader = DictReader(file)
                for row in reader:
                    if row['name'] == self.busName:
                        self.busData = row
                        self.busData['vMag'] = float(row['vMag'])
                        self.busData['zone'] = int(row['zone'])
                        self.busData['maxVm'] = float(row['maxVm'])
                        self.busData['minVm'] = float(row['minVm'])
                        break

    def accept(self):
        csvPath = os.path.join(self.projectPath, 'Buses.csv')
        tempPath = csvPath + '.tmp'
        
        with open(csvPath, 'r', newline='') as infile, open(tempPath, 'w', newline='') as outfile:
            reader = DictReader(infile)
            fieldnames = reader.fieldnames
            writer = DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()

            for row in reader:
                if row['name'] == self.busName:
                    row['name'] = self.nameInput.text()
                    row['vMag'] = self.vMagInput.text()
                    row['zone'] = self.zoneInput.text()
                    row['maxVm'] = self.maxVmInput.text()
                    row['minVm'] = self.minVmInput.text()
                writer.writerow(row)

        os.replace(tempPath, csvPath)
        super().accept()
    
    def reject(self):
        self.canceled = True
        super().reject()
