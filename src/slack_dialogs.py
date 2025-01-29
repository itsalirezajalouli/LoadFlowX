# Dialogs for slack
from psa_components import Slack
from PyQt6.QtWidgets import QDialog, QLabel, QWidget, QHBoxLayout, QLineEdit, QComboBox, QVBoxLayout, QDialogButtonBox, QMessageBox
from PyQt6.QtGui import QDoubleValidator

class AddSlackDialog(QDialog):
    def __init__(self, parent, bus, theme = 'dark') -> None:
        super().__init__(parent)
        self.projectPath = None
        self.inputError = False
        self.bus = bus
        self.slackId = None 
        self.slackPos = None
        self.slackOri = None
        self.slackHand = None
        self.setWindowTitle('Add Bus')

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
            background-color: {'#d9d9d9' if theme == 'light' else '#23272a'};
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
        }}
        QDialogButtonBox QPushButton:hover {{
            font-size: 12px;
            background-color: #99aab5;
            padding: 5px;
            color: {'#ffffff' if theme == 'dark' else '#000000'};
            border: 1px solid #7289da;
        }}
        ''')

        self.title = QLabel('Add Slack to Network')
        self.title.setStyleSheet(f'''
            color: {'#ffffff' if theme == 'dark' else '#000000'};
            font-weight: bold;
            border: 2px solid #7289da;
            border-radius: 5px;
            padding: 10px;
        ''')

        # Bus Name Input Box
        self.nameInputLabel = QLabel('Slack Name:')
        self.nameInput = QLineEdit(self)
        self.nameInput.setPlaceholderText('Set a name for the grid')

        # Voltage Magnitude Input
        self.vMagHBox = QHBoxLayout()
        self.vMagLabel = QLabel('|V|:')
        self.vMagInput = QLineEdit(self)
        self.vMagInput.setPlaceholderText('i.e. 1.02 p.u')
        self.vMagInput.setValidator(QDoubleValidator())
        self.vMagUnitDropDown = QComboBox(self)
        self.vMagUnitDropDown.addItem('PU   ')
        self.vMagUnitDropDown.addItem('KV   ')
        self.vMagUnitDropDown.activated.connect(self.handleVoltageUnitChange)
        self.vBaseLabel = QLabel('Vb: ')
        self.vBaseInput = QLineEdit(self)
        self.vBaseInput.setPlaceholderText('Base Voltage (KV)')
        self.vBaseInput.setValidator(QDoubleValidator())
        self.vBaseLabel.hide()
        self.vBaseInput.hide()

        self.vMagHBox.addWidget(self.vMagLabel)
        self.vMagHBox.addWidget(self.vMagInput)
        self.vMagHBox.addWidget(self.vMagUnitDropDown)
        self.vMagHBox.addWidget(self.vBaseLabel)
        self.vMagHBox.addWidget(self.vBaseInput)

        # Voltage Angle Input
        self.vAngHBox = QHBoxLayout()
        self.vangLabel = QLabel('δ:')
        self.vangInput = QLineEdit(self)
        self.vangInput.setPlaceholderText('i.e. 0')
        self.vangInput.setValidator(QDoubleValidator())
        self.vangUnitDropDown = QComboBox(self)
        self.vangUnitDropDown.addItem('DEG   ')
        self.vangUnitDropDown.addItem('RAD   ')
        self.vangUnitDropDown.activated.connect(self.handleAngleUnitChange)

        self.vAngHBox.addWidget(self.vangLabel)
        self.vAngHBox.addWidget(self.vangInput)
        self.vAngHBox.addWidget(self.vangUnitDropDown)

        # Button Box
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.accepted.connect(self.accept)

        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.nameInputLabel)
        layout.addWidget(self.nameInput)
        layout.addLayout(self.vMagHBox)
        layout.addLayout(self.vAngHBox)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

    def handleVoltageUnitChange(self, index):
        if index == 0:  # PU selected
            self.vBaseLabel.hide()
            self.vBaseInput.hide()
            self.vMagInput.setPlaceholderText('i.e. 1.02 p.u')
        elif index == 1:  # KV selected
            self.vBaseLabel.show()
            self.vBaseInput.show()
            self.vMagInput.setPlaceholderText('i.e. 345 KV')

    def handleAngleUnitChange(self, index):
        if index == 0:  # Degrees selected
            self.vangInput.setPlaceholderText('i.e. 0')
        elif index == 1:  # Radians selected
            self.vangInput.setPlaceholderText('i.e. 0.785')

    def accept(self) -> None:
        inputList = [self.vMagInput.text(), self.nameInput.text()]
        if '' in inputList:
            self.inputError = True
            QMessageBox.warning(self, 'Fill all the fields.',
                'No field can be empty! Please fill them all.', QMessageBox.StandardButton.Ok)
            return
        else:
            self.inputError = False

        # Convert KV to PU if required
        vMag = float(self.vMagInput.text())
        if self.vMagUnitDropDown.currentText() == 'KV':
            vBase = float(self.vBaseInput.text())
            vMag = vMag / vBase  # Convert to PU

        # Convert radians to degrees if required
        vang = float(self.vangInput.text())
        if self.vangUnitDropDown.currentText() == 'rad':
            vang = vang * (180 / 3.141592653589793)  # Convert to degrees

        slack = Slack(
            id=self.slackId,
            bus=self.bus,
            vmPU=vMag,
            vaD=vang,
            pos=self.slackPos,
            orient=self.slackOri,
            hand=self.slackHand,
        )
        slack.log()
        slack.append2CSV(self.projectPath)
        super().accept()
