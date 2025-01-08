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

        # Trafo
        self.trafoLabel = QLabel('Name:')
        self.trafoLabel.setStyleSheet('color: #ffffff;')
        self.trafoHBox = QHBoxLayout()
        self.trafoInput = QLineEdit(self)
        self.trafoInput.setPlaceholderText('Name')
        # self.vBaseInput = QLineEdit(self)
        # self.vBaseInput.setPlaceholderText('V Base')
        # self.lenUnitDropDown = QComboBox(self) 
        # self.lenUnitDropDown.addItem('KM')
        # self.lenUnitDropDown.addItem('Miles (Not Implemented)')
        # self.vbUnitDropDown = QComboBox(self) 
        # self.vbUnitDropDown.addItem('PU')
        # self.vbUnitDropDown.addItem('KV')
        self.trafoHBox.addWidget(self.trafoLabel)
        self.trafoHBox.addWidget(self.trafoInput)
        # self.lenHBox.addWidget(self.lenUnitDropDown)
        # self.lenHBox.addWidget(self.vBaseInput)
        # self.lenHBox.addWidget(self.vbUnitDropDown)
        self.trafoWidget = QWidget()
        self.trafoWidget.setLayout(self.trafoHBox)

        # Button Box
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.accepted.connect(self.accept)

        layout = QVBoxLayout()
        layout.addWidget(self.title)
        # layout.addWidget(self.trafoHBox)
        # layout.addWidget(self.nameInput)
        # layout.addWidget(self.zWidget)
        layout.addWidget(self.trafoWidget)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)
        
        # Button Box
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.accepted.connect(self.accept)

    def accept(self) -> None:
        print(f'bus1:{self.bus1Id}, bus2:{self.bus2Id}')
        inputList = []
        # inputList.append(self.rInput.text())
        # inputList.append(self.xInput.text())
        # inputList.append(self.aInput.text())
        inputList.append(self.trafoInput.text())
        if '' in inputList:
            self.inputError = True
            QMessageBox.warning(self, 'Fill all the fields.',
                'No field can be empty! Please fill them all.', QMessageBox.StandardButton.Ok)
            return
        else:
            self.inputError = False
        # Creating the Trafo
        trafo = Transformer(
            name = self.trafoInput.text(),
            id = self.trafoId,
            hvBus = self.bus1Id,
            lvBus = self.bus2Id,
        )
        # bus.log()
        trafo.append2CSV(self.projectPath)
        super().accept()

        super().accept()
