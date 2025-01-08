# Dialogs for lines
from psa_components import Generator
from PyQt6.QtWidgets import QDialog, QLabel, QWidget, QHBoxLayout, QLineEdit, QComboBox, QVBoxLayout, QDialogButtonBox, QMessageBox

class AddGenDialog(QDialog):
    def __init__(self, parent, bus) -> None:
        super().__init__(parent)
        self.projectPath = None
        self.inputError = False
        self.bus = bus
        self.setWindowTitle('Add Generator')
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
        self.title = QLabel('Add Generator to Network')
        self.title.setStyleSheet('''
            color: #ffffff;
            border: 2px solid #7289da;
            border-radius: 5px;
            padding: 8px;
        ''')
        
        # Bus Name Input Box
        self.nameInputLabel = QLabel('Generator Name:')
        self.nameInputLabel.setStyleSheet('color: #ffffff;')
        self.nameInput = QLineEdit(self)
        self.nameInput.setPlaceholderText('i.e. Gen1')

        # P
        self.pLabel = QLabel('Active Power:')
        self.pLabel.setStyleSheet('color: #ffffff;')
        self.pHBox = QHBoxLayout()
        self.pInput = QLineEdit(self)
        self.pInput.setPlaceholderText('i.e. 80 MW')
        self.pUnitDropDown = QComboBox(self) 
        self.pUnitDropDown.addItem('MW')
        self.pUnitDropDown.addItem('PU (Not Implemented)')
        self.pHBox.addWidget(self.pLabel)
        self.pHBox.addWidget(self.pInput)
        self.pHBox.addWidget(self.pUnitDropDown)
        self.pWidget = QWidget()
        self.pWidget.setLayout(self.pHBox)

        # Button Box
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.accepted.connect(self.accept)

        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.nameInputLabel)
        layout.addWidget(self.nameInput)
        layout.addWidget(self.pWidget)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

    def accept(self) -> None:
        inputList = []
        inputList.append(self.pInput.text())
        inputList.append(self.nameInput.text())
        print('intputList', inputList)
        if '' in inputList:
            self.inputError = True
            QMessageBox.warning(self, 'Fill all the fields.',
                'No field can be empty! Please fill them all.', QMessageBox.StandardButton.Ok)
            return
        else:
            self.inputError = False
        generator = Generator(
            bus = self.bus, 
            name = inputList[1],
            pMW = inputList[0],
        )
        generator.append2CSV(self.projectPath)
        super().accept()
