# Import
from PyQt6.QtWidgets import QDialog, QLabel, QWidget, QHBoxLayout, QLineEdit, QComboBox, QVBoxLayout, QDialogButtonBox, QMessageBox

# Dialogs to handle user input for running load flow calculation
class RunSimDialog(QDialog):
    def __init__(self, parent, freq, sBase, theme = 'dark') -> None:
        super().__init__(parent)
        self.projectPath = None
        self.freq = freq # frequency of the network
        self.sBase = sBase
        self.activatedMethod = 'nr' # set default load flow method to newton-raphson
        self.maxIter = 1000
        self.canceled = False

        # Styling
        self.setWindowTitle('Run Simulation')

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

        self.title = QLabel('Run Simulation')
        self.title.setStyleSheet(f'''
            color: {'#ffffff' if theme == 'dark' else '#000000'};
            font-weight: bold;
            border: 2px solid #7289da;
            border-radius: 5px;
            padding: 10px;
        ''')
        
        # Method Box
        self.methLabel = QLabel('Method of Calculation:')
        self.methWidget = QWidget()
        self.methHBox = QHBoxLayout()
        self.methDropDown = QComboBox(self) 
        self.methDropDown.addItem('Newton Raphson')
        self.methDropDown.addItem('Gauss Seidel')
        self.methDropDown.addItem('Fast Decoupled')
        self.methDropDown.activated.connect(self.method)
        self.methHBox.addWidget(self.methDropDown)
        self.methWidget.setLayout(self.methHBox)

        # Frequency & S Base input box
        self.fsLabel = QLabel('Network Constant Parameters:')
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
        self.sbUnitDropDown.addItem('MVA   ')
        self.fsHBox.addWidget(self.fLabel)
        self.fsHBox.addWidget(self.freqInput)
        self.fsHBox.addWidget(self.sbLabel)
        self.fsHBox.addWidget(self.sBaseInput)
        self.fsHBox.addWidget(self.sbUnitDropDown)
        self.fsWidget = QWidget()
        self.fsWidget.setLayout(self.fsHBox)

        # Max Iterations input box
        self.maxIterLabel = QLabel('Maximum Iterations:')
        self.maxIterHBox = QHBoxLayout()
        self.maxIterInput = QLineEdit(self)
        self.maxIterInput.setPlaceholderText('Max Iterations')
        self.maxIterInput.setText('1000')  # Default value
        self.maxIterHBox.addWidget(self.maxIterLabel)
        self.maxIterHBox.addWidget(self.maxIterInput)
        self.maxIterWidget = QWidget()
        self.maxIterWidget.setLayout(self.maxIterHBox)

        # Button Box
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.accepted.connect(self.accept)

        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.methLabel)
        layout.addWidget(self.methWidget)
        layout.addWidget(self.fsLabel)
        layout.addWidget(self.fsWidget)
        layout.addWidget(self.maxIterWidget)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

    def accept(self) -> None:
        inputList = []
        inputList.append(self.freqInput.text())
        inputList.append(self.sBaseInput.text())
        inputList.append(self.maxIterInput.text())
        self.freq = float(self.freqInput.text())
        self.sBase = float(self.sBaseInput.text())
        self.maxIter = int(self.maxIterInput.text())
        if '' in inputList:
            self.inputError = True
            QMessageBox.warning(self, 'Fill all the fields.',
                'No field can be empty! Please fill them all.', QMessageBox.StandardButton.Ok)
            return
        else:
            self.inputError = False
        super().accept()

    def method(self, index) -> None:
        # saves the user's choice for calculation of load flow
        if index == 0: 
            self.activatedMethod = 'nr'
        elif index == 1: 
            self.activatedMethod = 'gs'
        elif index == 2:
            self.activatedMethod = 'fdbx'

    def reject(self) -> None:
        self.canceled = True
        super().accept()
