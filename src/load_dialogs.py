# Imports 
import os
import csv
from psa_components import Load
from PyQt6.QtGui import QDoubleValidator
from PyQt6.QtWidgets import QComboBox, QDialog, QHBoxLayout, QLineEdit, QVBoxLayout, QWidget, QLabel, QDialogButtonBox, QMessageBox

# Dialogs Related to Bus Objects
class AddLoadDialog(QDialog):
    def __init__(self, parent, bus) -> None:
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
        self.projectName = None
        self.inputError = False
        self.bus = bus 
        self.loadPos = None
        self.loadOri = None
        self.loadHand = None

        # Bus Name Input Box
        # self.nameInputLabel = QLabel('Load Name:')
        # self.nameInputLabel.setStyleSheet('color: #ffffff;')
        # self.nameInput = QLineEdit(self)
        # self.nameInput.setPlaceholderText('Set Your Bus Name')

        # Bus Type Combo Box
        # self.typeInputLabel = QLabel('Bus Type:')
        # self.typeInputLabel.setStyleSheet('color: #ffffff;')
        # self.busTypeDropDown = QComboBox(self) 
        # self.busTypeDropDown.addItem('SLACK')
        # self.busTypeDropDown.addItem('PV')
        # self.busTypeDropDown.addItem('PQ')
        # self.busTypeDropDown.activated.connect(self.busTypeActivator)
        #
        # V Magnitude & Angle Input Box
        self.pInputLabel = QLabel('Load:')
        self.pInputLabel.setStyleSheet('color: #ffffff;')
        self.pWidget = QWidget()
        self.pHBox = QHBoxLayout()
        self.pLabel = QLabel('P: ')
        self.pInput = QLineEdit(self)
        self.pInput.setPlaceholderText('i.e. 100 MW')
        self.pUnitDropDown = QComboBox(self) 
        self.pUnitDropDown.addItem('MW')
        # self.pUnitDropDown.addItem('PU (Not Implemented)')
        self.qWidget = QWidget()
        self.qHBox = QHBoxLayout()
        self.qLabel = QLabel('Q: ')
        self.qInput = QLineEdit(self)
        self.qInput.setPlaceholderText('i.e. 20 MVAR')
        self.qUnitDropDown = QComboBox(self) 
        self.qUnitDropDown.addItem('MW')
        # self.qUnitDropDown.addItem('PU (Not Implemented)')
        # self.vUnitDropDown.addItem('V')
        # self.vUnitDropDown.activated.connect(self.vMagUnitActivator)
        # self.vDegreeTypeDropDown = QComboBox(self) 
        # self.vDegreeTypeDropDown.addItem('Deg')
        # self.vDegreeTypeDropDown.addItem('Rad')
        self.pHBox.addWidget(self.pLabel)
        self.pHBox.addWidget(self.pInput)
        self.pHBox.addWidget(self.pUnitDropDown)
        self.qHBox.addWidget(self.qLabel)
        self.qHBox.addWidget(self.qInput)
        self.qHBox.addWidget(self.qUnitDropDown)
        # self.vHBox.addWidget(self.vAngLabel)
        # self.vHBox.addWidget(self.vAngInput)
        # self.vHBox.addWidget(self.vDegreeTypeDropDown)
        self.pWidget.setLayout(self.pHBox)
        self.qWidget.setLayout(self.qHBox)

        # P & Q Input Box
        # self.pqInputLabel = QLabel('Active & Passive Power:')
        # self.pqInputLabel.setStyleSheet('color: #ffffff;')
        # self.pqWidget = QWidget()
        # self.pqHBox = QHBoxLayout()
        # self.pInput = QLineEdit(self)
        # self.pInput.setPlaceholderText('P')
        # self.qInput = QLineEdit(self)
        # self.qInput.setPlaceholderText('Q')
        # self.pUnitDropDown = QComboBox(self) 
        # self.pUnitDropDown.addItem('PU')
        # self.pUnitDropDown.addItem('KW')
        # self.qUnitDropDown = QComboBox(self) 
        # self.qUnitDropDown.addItem('PU')
        # self.qUnitDropDown.addItem('KVA')
        # self.pqHBox.addWidget(self.pInput)
        # self.pqHBox.addWidget(self.pUnitDropDown)
        # self.pqHBox.addWidget(self.qInput)
        # self.pqHBox.addWidget(self.qUnitDropDown)
        # self.pqWidget.setLayout(self.pqHBox)

        self.pInput.setValidator(QDoubleValidator())
        self.qInput.setValidator(QDoubleValidator())
        # self.vAngInput.setValidator(QDoubleValidator())
        # self.qInput.setValidator(QDoubleValidator())
        # self.pInput.setValidator(QDoubleValidator())

        # Button Box
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.accepted.connect(self.accept)

        layout = QVBoxLayout()
        layout.addWidget(self.title)
        # layout.addWidget(self.typeInputLabel)
        # layout.addWidget(self.busTypeDropDown)
        layout.addWidget(self.pInputLabel)
        layout.addWidget(self.pWidget)
        layout.addWidget(self.qWidget)
        # layout.addWidget(self.pqInputLabel)
        # layout.addWidget(self.pqWidget)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

    def accept(self) -> None:
        # Handling Empty Inputs Error
        inputList = []
        inputList.append(self.pInput.text())
        inputList.append(self.qInput.text())
        # inputList.append(self.vAngInput.text())
        # inputList.append(self.pInput.text())
        # inputList.append(self.qInput.text())
        if '' in inputList:
            self.inputError = True
            QMessageBox.warning(self, 'Fill all the fields.',
                'No field can be empty! Please fill them all.', QMessageBox.StandardButton.Ok)
            return
        else:
            self.inputError = False
        # Creating the Load
        load = Load(
            bus = self.bus,
            pMW = float(self.pInput.text()),
            qMW = float(self.qInput.text()),
            pos = self.loadPos,
            orient = self.loadOri,
            hand = self.loadHand,
        )
        load.append2CSV(self.projectPath)
        super().accept()
