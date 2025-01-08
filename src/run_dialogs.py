# Import
from PyQt6.QtWidgets import QDialog, QLabel, QWidget, QHBoxLayout, QLineEdit, QComboBox, QVBoxLayout, QDialogButtonBox, QMessageBox

# Dialogs Related to Trafo 
class RunSimDialog(QDialog):
    def __init__(self, parent, freq, sBase) -> None:
        super().__init__(parent)
        self.projectPath = None
        self.freq = freq
        self.sBase = sBase
        self.activatedMethod = 'Newton Raphson'
        self.setWindowTitle('Run Simulation')
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
        self.title = QLabel('Run Load Flow Simulation')
        self.title.setStyleSheet('''
            color: #ffffff;
            border: 2px solid #7289da;
            border-radius: 5px;
            padding: 8px;
        ''')
        
        # Method Box
        self.methLabel = QLabel('Method of Calculation:')
        self.methLabel.setStyleSheet('color: #ffffff;')
        self.methWidget = QWidget()
        self.methHBox = QHBoxLayout()
        self.methDropDown = QComboBox(self) 
        self.methDropDown.addItem('Newton Raphson')
        self.methDropDown.addItem('Gauss Seidel')
        self.methDropDown.addItem('Fast Decoupled')
        self.methDropDown.activated.connect(self.method)
        self.methHBox.addWidget(self.methDropDown)
        self.methWidget.setLayout(self.methHBox)

        # Frequency & S Base
        self.fsLabel = QLabel('Network Constant Parameters:')
        self.fsLabel.setStyleSheet('color: #ffffff;')
        self.fsHBox = QHBoxLayout()
        self.freqInput = QLineEdit(self)
        self.fLabel = QLabel('f (Hz) : ')
        self.freqInput.setPlaceholderText('Frequency')
        self.freqInput.setText(str(self.freq))
        self.sbLabel = QLabel('S (Base) : ')
        self.sBaseInput = QLineEdit(self)
        self.sBaseInput.setPlaceholderText('S Base')
        self.sBaseInput.setText(str(self.sBase))
        self.sbUnitDropDown = QComboBox(self) 
        self.sbUnitDropDown.addItem('PU')
        self.sbUnitDropDown.addItem('KV')
        self.fsHBox.addWidget(self.fLabel)
        self.fsHBox.addWidget(self.freqInput)
        self.fsHBox.addWidget(self.sbLabel)
        self.fsHBox.addWidget(self.sBaseInput)
        self.fsHBox.addWidget(self.sbUnitDropDown)
        self.aWidget = QWidget()
        self.aWidget.setLayout(self.fsHBox)

        # Button Box
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.accepted.connect(self.accept)

        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.methLabel)
        layout.addWidget(self.methWidget)
        layout.addWidget(self.fsLabel)
        layout.addWidget(self.aWidget)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

    def accept(self) -> None:
        inputList = []
        inputList.append(self.freqInput.text())
        inputList.append(self.sBaseInput.text())
        if '' in inputList:
            self.inputError = True
            QMessageBox.warning(self, 'Fill all the fields.',
                'No field can be empty! Please fill them all.', QMessageBox.StandardButton.Ok)
            return
        else:
            self.inputError = False
        super().accept()

    def method(self, index) -> None:
        if index == 0: 
            self.activatedMethod = 'nr'
        elif index == 1: 
            self.activatedMethod = 'gs'
        elif index == 2:
            self.activatedMethod = 'fd'
