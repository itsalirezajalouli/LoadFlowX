# Import
from psa_components import Transformer
from PyQt6.QtWidgets import QDialog, QLabel, QWidget, QHBoxLayout, QLineEdit, QComboBox, QVBoxLayout, QDialogButtonBox, QMessageBox

# Dialogs Related to Trafo 
class AddTrafoDialog(QDialog):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.projectPath = None
        self.trafoPos = None
        self.trafoId = None
        self.inputError = False
        self.bus1Id = None
        self.bus2Id = None 
        self.setWindowTitle('Add Transformer')
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
        self.title = QLabel('Add Transformer to Network')
        self.title.setStyleSheet('''
            color: #ffffff;
            border: 2px solid #7289da;
            border-radius: 5px;
            padding: 8px;
        ''')
        
        # Trafo Z Input Box
        self.zLabel = QLabel('Impedances:')
        self.zLabel.setStyleSheet('color: #ffffff;')
        self.zWidget = QWidget()
        self.zHBox = QHBoxLayout()
        self.rInput = QLineEdit(self)
        self.rInput.setPlaceholderText('R')
        self.xInput = QLineEdit(self)
        self.xInput.setPlaceholderText('X')
        self.rUnitDropDown = QComboBox(self) 
        self.rUnitDropDown.addItem('PU')
        self.rUnitDropDown.addItem('Kohm')
        self.xUnitDropDown = QComboBox(self) 
        self.xUnitDropDown.addItem('PU')
        self.xUnitDropDown.addItem('Kohm')
        self.zHBox.addWidget(self.rInput)
        self.zHBox.addWidget(self.rUnitDropDown)
        self.zHBox.addWidget(self.xInput)
        self.zHBox.addWidget(self.xUnitDropDown)
        self.zWidget.setLayout(self.zHBox)

        # A & V Base
        self.vLabel = QLabel('Voltages:')
        self.vLabel.setStyleSheet('color: #ffffff;')
        self.aHBox = QHBoxLayout()
        self.aInput = QLineEdit(self)
        self.aInput.setPlaceholderText('a (N1 / N2 or V1 / V2)')
        self.vBaseInput = QLineEdit(self)
        self.vBaseInput.setPlaceholderText('V Base')
        self.vbUnitDropDown = QComboBox(self) 
        self.vbUnitDropDown.addItem('PU')
        self.vbUnitDropDown.addItem('KV')
        self.aHBox.addWidget(self.aInput)
        self.aHBox.addWidget(self.vBaseInput)
        self.aHBox.addWidget(self.vbUnitDropDown)
        self.aWidget = QWidget()
        self.aWidget.setLayout(self.aHBox)

        # Button Box
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.accepted.connect(self.accept)

        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.zLabel)
        layout.addWidget(self.zWidget)
        layout.addWidget(self.vLabel)
        layout.addWidget(self.aWidget)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

    def accept(self) -> None:
        inputList = []
        inputList.append(self.rInput.text())
        inputList.append(self.xInput.text())
        inputList.append(self.aInput.text())
        inputList.append(self.vBaseInput.text())
        if '' in inputList:
            self.inputError = True
            QMessageBox.warning(self, 'Fill all the fields.',
                'No field can be empty! Please fill them all.', QMessageBox.StandardButton.Ok)
            return
        else:
            self.inputError = False
        super().accept()
