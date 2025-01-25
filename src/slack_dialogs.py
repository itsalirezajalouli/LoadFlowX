# Dialogs for slack
from psa_components import Slack
from PyQt6.QtWidgets import QDialog, QLabel, QWidget, QHBoxLayout, QLineEdit, QComboBox, QVBoxLayout, QDialogButtonBox, QMessageBox

class AddSlackDialog(QDialog):
    def __init__(self, parent, bus) -> None:
        super().__init__(parent)
        self.projectPath = None
        self.inputError = False
        self.bus = bus
        self.slackId = None 
        self.slackPos = None
        self.slackOri = None
        self.slackHand = None
        self.setWindowTitle('Add Bus')
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
        self.title = QLabel('Add Slack to Network')
        self.title.setStyleSheet('''
            color: #ffffff;
            border: 2px solid #7289da;
            border-radius: 5px;
            padding: 8px;
        ''')
        
        self.vmPU = None

        # Bus Name Input Box
        self.nameInputLabel = QLabel('Slack Name:')
        self.nameInputLabel.setStyleSheet('color: #ffffff;')
        self.nameInput = QLineEdit(self)
        self.nameInput.setPlaceholderText('Set a name for the grid')

        # Length & V Base
        self.vMagLabel = QLabel('|V|:')
        self.vMagLabel.setStyleSheet('color: #ffffff;')
        self.vHBox = QHBoxLayout()
        self.vMagInput = QLineEdit(self)
        self.vMagInput.setPlaceholderText('i.e. 1.02 p.u')
        self.vangLabel = QLabel('δ:')
        self.vangInput = QLineEdit(self)
        self.vangInput.setPlaceholderText('i.e. 0')
        self.vMagUnitDropDown = QComboBox(self) 
        self.vMagUnitDropDown.addItem('PU')
        self.vangUnitDropDown = QComboBox(self) 
        self.vangUnitDropDown.addItem('deg')
        self.vHBox.addWidget(self.vMagLabel)
        self.vHBox.addWidget(self.vMagInput)
        self.vHBox.addWidget(self.vMagUnitDropDown)
        self.vHBox.addWidget(self.vangLabel)
        self.vHBox.addWidget(self.vangInput)
        self.vHBox.addWidget(self.vangUnitDropDown)
        self.lenWidget = QWidget()
        self.lenWidget.setLayout(self.vHBox)

        # Button Box
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.accepted.connect(self.accept)

        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.nameInputLabel)
        layout.addWidget(self.nameInput)
        # layout.addWidget(self.zWidget)
        layout.addWidget(self.lenWidget)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

    def accept(self) -> None:
        inputList = []
        # inputList.append(self.rInput.text())
        # inputList.append(self.xInput.text())
        inputList.append(self.vMagInput.text())
        inputList.append(self.nameInput.text())
        if '' in inputList:
            self.inputError = True
            QMessageBox.warning(self, 'Fill all the fields.',
                'No field can be empty! Please fill them all.', QMessageBox.StandardButton.Ok)
            return
        else:
            self.inputError = False
        slack = Slack(
            id = self.slackId,
            bus = self.bus,
            vmPU = float(self.vMagInput.text()),
            vaD = float(self.vangInput.text()),
            pos = self.slackPos,
            orient = self.slackOri,
            hand = self.slackHand,
        )
        slack.append2CSV(self.projectPath)
        super().accept()
