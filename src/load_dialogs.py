# Imports 
import os
import csv
from psa_components import Load
from PyQt6.QtGui import QDoubleValidator
from PyQt6.QtWidgets import QComboBox, QDialog, QHBoxLayout, QLineEdit, QVBoxLayout, QWidget, QLabel, QDialogButtonBox, QMessageBox

class AddLoadDialog(QDialog):
    def __init__(self, parent, bus) -> None:
        super().__init__(parent)
        self.setWindowTitle('Add Load')
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
        self.title = QLabel('Add Load to Network')
        self.title.setStyleSheet('''
            color: #ffffff;
            border: 2px solid #7289da;
            border-radius: 5px;
            padding: 8px;
        ''')
        self.projectPath = None
        self.inputError = False
        self.bus = bus
        self.loadId = None
        self.loadPos = None
        self.loadOri = None
        self.loadHand = None

        # Active Power (P) Input Box
        self.pWidget = QWidget()
        self.pHBox = QHBoxLayout()
        self.pInputLabel = QLabel('Active Power (P):')
        self.pInputLabel.setStyleSheet('color: #ffffff;')
        self.pLabel = QLabel('P: ')
        self.pInput = QLineEdit(self)
        self.pInput.setPlaceholderText('i.e. 100 MW')
        self.pUnitDropDown = QComboBox(self)
        self.pUnitDropDown.addItem('MW')
        self.pUnitDropDown.addItem('PU')
        self.pUnitDropDown.activated.connect(self.updatePUnit)
        starLabelP = QLabel('*  ')
        starLabelP.setStyleSheet('color: #f04747;')
        self.pHBox.addWidget(self.pLabel)
        self.pHBox.addWidget(starLabelP)
        self.pHBox.addWidget(self.pInput)
        self.pHBox.addWidget(self.pUnitDropDown)
        self.pWidget.setLayout(self.pHBox)

        # Reactive Power (Q) Input Box
        self.qWidget = QWidget()
        self.qHBox = QHBoxLayout()
        self.qInputLabel = QLabel('Reactive Power (Q):')
        self.qInputLabel.setStyleSheet('color: #ffffff;')
        self.qLabel = QLabel('Q: ')
        self.qInput = QLineEdit(self)
        self.qInput.setPlaceholderText('i.e. 20 MVAR')
        self.qUnitDropDown = QComboBox(self)
        self.qUnitDropDown.addItem('MVar')
        self.qUnitDropDown.addItem('PU')
        self.qUnitDropDown.activated.connect(self.updateQUnit)
        starLabelQ = QLabel('*  ')
        starLabelQ.setStyleSheet('color: #f04747;')
        self.qHBox.addWidget(self.qLabel)
        self.qHBox.addWidget(starLabelQ)
        self.qHBox.addWidget(self.qInput)
        self.qHBox.addWidget(self.qUnitDropDown)
        self.qWidget.setLayout(self.qHBox)

        self.pInput.setValidator(QDoubleValidator())
        self.qInput.setValidator(QDoubleValidator())

        # Button Box
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.accepted.connect(self.accept)

        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.pInputLabel)
        layout.addWidget(self.pWidget)
        layout.addWidget(self.qInputLabel)
        layout.addWidget(self.qWidget)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

    def updatePUnit(self, index) -> None:
        if index == 0:  # MW
            self.removePBaseFields()
            self.pInput.setPlaceholderText('i.e. 100 MW')
        elif index == 1:  # PU
            self.addPBaseFields()
            self.pInput.setPlaceholderText('i.e. 1.02 PU')

    def updateQUnit(self, index) -> None:
        if index == 0:  # MVAR
            self.removeQBaseFields()
            self.qInput.setPlaceholderText('i.e. 20 MVAR')
        elif index == 1:  # PU
            self.addQBaseFields()
            self.qInput.setPlaceholderText('i.e. 1.02 PU')

    def addPBaseFields(self) -> None:
        if not hasattr(self, 'pBaseLabel'):
            self.pBaseLabel = QLabel('SBase: ')
            self.pBaseLabel.setStyleSheet('color: #ffffff;')
            self.pBaseStarLabel = QLabel('*  ')
            self.pBaseStarLabel.setStyleSheet('color: #f04747;')
            self.pBaseInput = QLineEdit(self)
            self.pBaseInput.setPlaceholderText('i.e. 100 MVA')
            self.pHBox.addWidget(self.pBaseLabel)
            self.pHBox.addWidget(self.pBaseStarLabel)
            self.pHBox.addWidget(self.pBaseInput)

    def removePBaseFields(self) -> None:
        if hasattr(self, 'pBaseLabel'):
            self.pBaseLabel.deleteLater()
            self.pBaseStarLabel.deleteLater()
            self.pBaseInput.deleteLater()
            del self.pBaseLabel, self.pBaseStarLabel, self.pBaseInput

    def addQBaseFields(self) -> None:
        if not hasattr(self, 'qBaseLabel'):
            self.qBaseLabel = QLabel('SBase: ')
            self.qBaseLabel.setStyleSheet('color: #ffffff;')
            self.qBaseStarLabel = QLabel('*  ')
            self.qBaseStarLabel.setStyleSheet('color: #f04747;')
            self.qBaseInput = QLineEdit(self)
            self.qBaseInput.setPlaceholderText('i.e. 100 MVA')
            self.qHBox.addWidget(self.qBaseLabel)
            self.qHBox.addWidget(self.qBaseStarLabel)
            self.qHBox.addWidget(self.qBaseInput)

    def removeQBaseFields(self) -> None:
        if hasattr(self, 'qBaseLabel'):
            self.qBaseLabel.deleteLater()
            self.qBaseStarLabel.deleteLater()
            self.qBaseInput.deleteLater()
            del self.qBaseLabel, self.qBaseStarLabel, self.qBaseInput

    def accept(self) -> None:
        # Handling Empty Inputs Error
        inputList = [self.pInput.text(), self.qInput.text()]
        if '' in inputList:
            self.inputError = True
            QMessageBox.warning(self, 'Fill all the fields.',
                'No field can be empty! Please fill them all.', QMessageBox.StandardButton.Ok)
            return
        self.inputError = False

        # Convert P and Q to MW and MVAR if in PU
        pValue = float(self.pInput.text())
        qValue = float(self.qInput.text())
        if self.pUnitDropDown.currentIndex() == 1:  # PU
            pValue *= float(self.pBaseInput.text())
        if self.qUnitDropDown.currentIndex() == 1:  # PU
            qValue *= float(self.qBaseInput.text())

        # Creating the Load
        load = Load(
            id=self.loadId,
            bus=self.bus,
            pMW=pValue,
            qMW=qValue,
            pos=self.loadPos,
            orient=self.loadOri,
            hand=self.loadHand,
        )
        load.log()
        load.append2CSV(self.projectPath)
        super().accept()
