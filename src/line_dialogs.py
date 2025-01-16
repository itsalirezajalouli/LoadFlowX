# Dialogs for lines
from psa_components import Line
from PyQt6.QtWidgets import QDialog, QLabel, QWidget, QHBoxLayout, QLineEdit, QComboBox, QVBoxLayout, QDialogButtonBox, QMessageBox

class AddLineDialog(QDialog):
    def __init__(self, parent, bus1, bus2) -> None:
        super().__init__(parent)
        self.projectPath = None
        self.inputError = False
        self.bus1Id = bus1
        self.bus2Id = bus2
        self.setWindowTitle('Add Line')
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
        self.title = QLabel('Add Line to Network')
        self.title.setStyleSheet('''
            color: #ffffff;
            border: 2px solid #7289da;
            border-radius: 5px;
            padding: 8px;
        ''')
        
        self.lineId = None
        self.R = None
        self.X = None
        self.B = None
        self.Length = None
        self.vBase = None

        # Line Name Input Box
        self.nameInputLabel = QLabel('Line Name:')
        self.nameInputLabel.setStyleSheet('color: #ffffff;')
        self.nameInput = QLineEdit(self)
        self.nameInput.setPlaceholderText('Set a name for the line')

        # Impedance Inputs (R, X, B)
        self.impedanceLabel = QLabel('Impedance (R, X, B):')
        self.impedanceLabel.setStyleSheet('color: #ffffff;')
        self.impedanceWidget = QWidget()
        self.impedanceHBox = QHBoxLayout()

        self.rInput = QLineEdit(self)
        self.rInput.setPlaceholderText('R (Ohm/km)')
        self.xInput = QLineEdit(self)
        self.xInput.setPlaceholderText('X (Ohm/km)')
        self.bInput = QLineEdit(self)
        self.bInput.setPlaceholderText('B (S/km)')

        self.impedanceHBox.addWidget(self.rInput)
        self.impedanceHBox.addWidget(self.xInput)
        self.impedanceHBox.addWidget(self.bInput)
        self.impedanceWidget.setLayout(self.impedanceHBox)

        # Length Input Box
        self.lenLabel = QLabel('Length (km):')
        self.lenLabel.setStyleSheet('color: #ffffff;')
        self.lenHBox = QHBoxLayout()
        self.lenInput = QLineEdit(self)
        self.lenInput.setPlaceholderText('Length of the line (km)')
        self.lenUnitDropDown = QComboBox(self) 
        self.lenUnitDropDown.addItem('KM')
        self.lenHBox.addWidget(self.lenLabel)
        self.lenHBox.addWidget(self.lenInput)
        self.lenHBox.addWidget(self.lenUnitDropDown)
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
        layout.addWidget(self.impedanceWidget)
        layout.addWidget(self.lenWidget)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

    def accept(self) -> None:
        inputList = []
        inputList.append(self.rInput.text())
        inputList.append(self.xInput.text())
        inputList.append(self.bInput.text())
        inputList.append(self.lenInput.text())
        inputList.append(self.nameInput.text())

        # Check if any input is empty
        if '' in inputList:
            self.inputError = True
            QMessageBox.warning(self, 'Fill all the fields.',
                'No field can be empty! Please fill them all.', QMessageBox.StandardButton.Ok)
            return
        else:
            self.inputError = False

        # Create the line object with the provided inputs
        line = Line(
            bus1id=self.bus1Id,
            bus2id=self.bus2Id,
            name=self.nameInput.text(),
            R=float(self.rInput.text()),
            X=float(self.xInput.text()),
            B=float(self.bInput.text()),
            len=float(self.lenInput.text())
        )

        line.log()
        line.append2CSV(self.projectPath)
        super().accept()
