# Import
from psa_components import Transformer
from PyQt6.QtWidgets import QDialog, QLabel, QWidget, QHBoxLayout, QLineEdit, QComboBox, QVBoxLayout, QDialogButtonBox, QMessageBox

# Dialogs Related to Trafo 
class AddTrafoDialog(QDialog):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.projectPath = None
        self.trafoPos = None
        self.trafoOrient = None
        self.trafoHands = None
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

        # Trafo Name
        self.trafoLabel = QLabel('Name:')
        self.trafoLabel.setStyleSheet('color: #ffffff;')
        self.trafoInput = QLineEdit(self)
        self.trafoInput.setPlaceholderText('Transformer Name')

        # Rated Power (sn_mva) and Short-Circuit Voltage (vk_percent)
        self.snLabel = QLabel('Rated Power (MVA):')
        self.snLabel.setStyleSheet('color: #ffffff;')
        self.snInput = QLineEdit(self)
        self.snInput.setPlaceholderText('i.e. 10')

        self.vkLabel = QLabel('Short-Circuit Voltage (%):')
        self.vkLabel.setStyleSheet('color: #ffffff;')
        self.vkInput = QLineEdit(self)
        self.vkInput.setPlaceholderText('i.e. 10')

        self.snVkHBox = QHBoxLayout()
        self.snVkHBox.addWidget(self.snLabel)
        self.snVkHBox.addWidget(self.snInput)
        self.snVkHBox.addWidget(self.vkLabel)
        self.snVkHBox.addWidget(self.vkInput)
        self.snVkWidget = QWidget()
        self.snVkWidget.setLayout(self.snVkHBox)

        # Resistive Component (vkr_percent) and Tap Step Percent (tap_step_percent)
        self.vkrLabel = QLabel('Resistive Component (%):')
        self.vkrLabel.setStyleSheet('color: #ffffff;')
        self.vkrInput = QLineEdit(self)
        self.vkrInput.setPlaceholderText('i.e. 0.5')

        self.tapStepLabel = QLabel('Tap Step (%):')
        self.tapStepLabel.setStyleSheet('color: #ffffff;')
        self.tapStepInput = QLineEdit(self)
        self.tapStepInput.setPlaceholderText('i.e. 2')

        self.vkrTapHBox = QHBoxLayout()
        self.vkrTapHBox.addWidget(self.vkrLabel)
        self.vkrTapHBox.addWidget(self.vkrInput)
        self.vkrTapHBox.addWidget(self.tapStepLabel)
        self.vkrTapHBox.addWidget(self.tapStepInput)
        self.vkrTapWidget = QWidget()
        self.vkrTapWidget.setLayout(self.vkrTapHBox)

        # Button Box
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.accepted.connect(self.accept)

        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.trafoLabel)
        layout.addWidget(self.trafoInput)
        layout.addWidget(self.snVkWidget)
        layout.addWidget(self.vkrTapWidget)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

    def accept(self) -> None:
        print(f'bus1:{self.bus1Id}, bus2:{self.bus2Id}')
        inputList = [self.trafoInput.text(), self.snInput.text(), self.vkInput.text(), self.vkrInput.text(), self.tapStepInput.text()]
        if '' in inputList:
            self.inputError = True
            QMessageBox.warning(self, 'Fill all the fields.',
                                 'No field can be empty! Please fill them all.', QMessageBox.StandardButton.Ok)
            return
        else:
            self.inputError = False

        # Creating the Transformer
        trafo = Transformer(
            name=self.trafoInput.text(),
            id=self.trafoId,
            hvBus=self.bus1Id,
            lvBus=self.bus2Id,
            pos=self.trafoPos,
            orient=self.trafoOrient,
            hands=self.trafoHands,
            sn_mva=float(self.snInput.text()),
            vk_percent=float(self.vkInput.text()),
            vkr_percent=float(self.vkrInput.text()),
            tap_step_percent=float(self.tapStepInput.text()),
        )
        trafo.log()
        trafo.append2CSV(self.projectPath)
        super().accept()
