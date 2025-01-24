# Dialogs for lines
from psa_components import Generator
from PyQt6.QtWidgets import QDialog, QLabel, QWidget, QHBoxLayout, QLineEdit, QVBoxLayout, QDialogButtonBox, QMessageBox

class AddGenDialog(QDialog):
    def __init__(self, parent, bus) -> None:
        super().__init__(parent)
        self.projectPath = None
        self.inputError = False
        self.bus = bus
        self.genId = None
        self.genPos = None
        self.genOri = None
        self.genHand = None
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
        ''')
        self.title = QLabel('Add Generator to Network')
        self.title.setStyleSheet('''
            color: #ffffff;
            border: 2px solid #7289da;
            border-radius: 5px;
            padding: 8px;
        ''')

        # Generator Name Input
        self.nameInputLabel = QLabel('Generator Name:')
        self.nameInputLabel.setStyleSheet('color: #ffffff;')
        self.nameInput = QLineEdit(self)
        self.nameInput.setPlaceholderText('i.e. Gen1')

        # Active Power and Voltage Magnitude (pMW and vmPU)
        self.pHBox = QHBoxLayout()
        self.pInput = QLineEdit(self)
        self.pInput.setPlaceholderText('Active Power (MW)')
        self.vmInput = QLineEdit(self)
        self.vmInput.setPlaceholderText('Voltage Magnitude (PU)')
        self.pHBox.addWidget(QLabel('Active Power:'))
        self.pHBox.addWidget(self.pInput)
        self.pHBox.addWidget(QLabel('Voltage Magnitude:'))
        self.pHBox.addWidget(self.vmInput)
        self.pWidget = QWidget()
        self.pWidget.setLayout(self.pHBox)

        # Reactive Power Range (minQMvar and maxQMvar)
        self.qHBox = QHBoxLayout()
        self.minQInput = QLineEdit(self)
        self.minQInput.setPlaceholderText('Min Reactive Power (MVar)')
        self.maxQInput = QLineEdit(self)
        self.maxQInput.setPlaceholderText('Max Reactive Power (MVar)')
        self.qHBox.addWidget(QLabel('Min Q (MVar):'))
        self.qHBox.addWidget(self.minQInput)
        self.qHBox.addWidget(QLabel('Max Q (MVar):'))
        self.qHBox.addWidget(self.maxQInput)
        self.qWidget = QWidget()
        self.qWidget.setLayout(self.qHBox)

        # Active Power Range (minPMW and maxPMW)
        self.pRangeHBox = QHBoxLayout()
        self.minPInput = QLineEdit(self)
        self.minPInput.setPlaceholderText('Min Active Power (MW)')
        self.maxPInput = QLineEdit(self)
        self.maxPInput.setPlaceholderText('Max Active Power (MW)')
        self.pRangeHBox.addWidget(QLabel('Min P (MW):'))
        self.pRangeHBox.addWidget(self.minPInput)
        self.pRangeHBox.addWidget(QLabel('Max P (MW):'))
        self.pRangeHBox.addWidget(self.maxPInput)
        self.pRangeWidget = QWidget()
        self.pRangeWidget.setLayout(self.pRangeHBox)

        # Button Box
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.accepted.connect(self.accept)

        # Main Layout
        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.nameInputLabel)
        layout.addWidget(self.nameInput)
        layout.addWidget(self.pWidget)
        layout.addWidget(self.qWidget)
        layout.addWidget(self.pRangeWidget)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

    def accept(self) -> None:
        """Handles acceptance of the dialog."""
        inputList = [
            self.pInput.text(),
            self.vmInput.text(),
            self.minQInput.text(),
            self.maxQInput.text(),
            self.minPInput.text(),
            self.maxPInput.text(),
            self.nameInput.text()
        ]

        # Check for empty inputs
        if '' in inputList:
            self.inputError = True
            QMessageBox.warning(self, 'Fill all the fields.',
                'No field can be empty! Please fill them all.', QMessageBox.StandardButton.Ok)
            return
        else:
            self.inputError = False

        # Create generator object
        generator = Generator(
            id = self.genId,
            bus=self.bus, 
            name=self.nameInput.text(),
            pMW=float(self.pInput.text()),
            vmPU=float(self.vmInput.text()),
            minQMvar=float(self.minQInput.text()),
            maxQMvar=float(self.maxQInput.text()),
            minPMW=float(self.minPInput.text()),
            maxPMW=float(self.maxPInput.text()),
            pos=self.genPos,
            orient=self.genOri, 
            hand=self.genHand
        )

        generator.append2CSV(self.projectPath)
        super().accept()

