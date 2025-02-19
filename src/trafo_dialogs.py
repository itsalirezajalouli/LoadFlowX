# Import
from psa_components import Transformer
from PyQt6.QtWidgets import (
    QDialog, QLabel, QWidget, QHBoxLayout, QLineEdit, QVBoxLayout,
    QDialogButtonBox, QMessageBox, QPushButton
)

class AddTrafoDialog(QDialog):
    def __init__(self, parent, bus1, bus2, theme = 'dark') -> None:
        super().__init__(parent)
        self.projectPath = None
        self.trafoPos = None
        self.trafoOrient = None
        self.trafoHands = None
        self.trafoId = None
        self.inputError = False
        self.bus1Id = bus1 
        self.bus2Id = bus2 
        self.canceled = False
        self.setWindowTitle('Add Transformer')

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
        
        self.title = QLabel('Add Transformer to Network')
        self.title.setStyleSheet(f'''
            color: {'#ffffff' if theme == 'dark' else '#000000'};
            font-weight: bold;
            border: 2px solid #7289da;
            border-radius: 5px;
            padding: 10px;
        ''')
        
        # Transformer Name
        self.trafoWidget = QWidget()
        self.trafoHBox = QHBoxLayout()
        self.trafoLabel = QLabel('Name:')
        starLabelName = QLabel('* ')
        starLabelName.setStyleSheet('color: #f04747;')
        self.trafoInput = QLineEdit(self)
        self.trafoInput.setPlaceholderText('Transformer Name')
        
        self.trafoHBox.addWidget(self.trafoLabel)
        self.trafoHBox.addWidget(starLabelName)
        self.trafoHBox.addWidget(self.trafoInput)
        self.trafoWidget.setLayout(self.trafoHBox)
        
        # High Voltage / Low Voltage Showcase
        self.busWidget = QWidget()
        self.busHBox = QHBoxLayout()
        self.busLabel = QLabel('High Voltage Bus:')
        self.hvBusLabel = QLabel(str(self.bus1Id))
        self.hvBusLabel.setStyleSheet('color: #f04747;')
        self.lvBusLabel = QLabel(str(self.bus2Id))
        self.lvBusLabel.setStyleSheet('color: #f04747;')
        self.swapButton = QPushButton('Swap')
        self.swapButton.clicked.connect(self.swapBuses)
        
        self.busHBox.addWidget(self.busLabel)
        self.busHBox.addWidget(self.hvBusLabel)
        self.busHBox.addWidget(QLabel('Low Voltage Bus:'))
        self.busHBox.addWidget(self.lvBusLabel)
        self.busHBox.addWidget(self.swapButton)
        self.busWidget.setLayout(self.busHBox)
        
        # Rated Power and Short-Circuit Voltage
        self.snLabel = QLabel('Rated Power (MVA):')
        starLabelSn = QLabel('* ')
        starLabelSn.setStyleSheet('color: #f04747;')
        self.snInput = QLineEdit(self)
        self.snInput.setPlaceholderText('i.e. 10')
        
        self.vkLabel = QLabel('Short-Circuit Voltage (%):')
        starLabelVk = QLabel('* ')
        starLabelVk.setStyleSheet('color: #f04747;')
        self.vkInput = QLineEdit(self)
        self.vkInput.setPlaceholderText('i.e. 10')
        
        self.snVkHBox = QHBoxLayout()
        self.snVkHBox.addWidget(self.snLabel)
        self.snVkHBox.addWidget(starLabelSn)
        self.snVkHBox.addWidget(self.snInput)
        self.snVkHBox.addWidget(self.vkLabel)
        self.snVkHBox.addWidget(starLabelVk)
        self.snVkHBox.addWidget(self.vkInput)
        self.snVkWidget = QWidget()
        self.snVkWidget.setLayout(self.snVkHBox)
        
        # Resistive Component and Tap Step Percent
        self.vkrLabel = QLabel('Resistive Component (%):')
        starLabelVkr = QLabel('* ')
        starLabelVkr.setStyleSheet('color: #f04747;')
        self.vkrInput = QLineEdit(self)
        self.vkrInput.setPlaceholderText('i.e. 0.5')
        
        self.tapStepLabel = QLabel('Tap Step (%):')
        starLabelTap = QLabel('* ')
        starLabelTap.setStyleSheet('color: #f04747;')
        self.tapStepInput = QLineEdit(self)
        self.tapStepInput.setPlaceholderText('i.e. 2')
        
        self.vkrTapHBox = QHBoxLayout()
        self.vkrTapHBox.addWidget(self.vkrLabel)
        self.vkrTapHBox.addWidget(starLabelVkr)
        self.vkrTapHBox.addWidget(self.vkrInput)
        self.vkrTapHBox.addWidget(self.tapStepLabel)
        self.vkrTapHBox.addWidget(starLabelTap)
        self.vkrTapHBox.addWidget(self.tapStepInput)
        self.vkrTapWidget = QWidget()
        self.vkrTapWidget.setLayout(self.vkrTapHBox)
        
        # Button Box
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.accepted.connect(self.accept)
        
        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.trafoWidget)
        layout.addWidget(self.busWidget)
        layout.addWidget(self.snVkWidget)
        layout.addWidget(self.vkrTapWidget)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

    def swapBuses(self):
        self.bus1Id, self.bus2Id = self.bus2Id, self.bus1Id
        self.hvBusLabel.setText(str(self.bus1Id))
        self.lvBusLabel.setText(str(self.bus2Id))
    
    def accept(self) -> None:
        print(f'bus1:{self.bus1Id}, bus2:{self.bus2Id}')
        inputList = [self.trafoInput.text(), self.snInput.text(), self.vkInput.text(), self.vkrInput.text(), self.tapStepInput.text()]
        if '' in inputList:
            self.inputError = True
            QMessageBox.warning(self, 'Fill all the fields.', 'No field can be empty! Please fill them all.', QMessageBox.StandardButton.Ok)
            return
        else:
            self.inputError = False

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

    def reject(self) -> None:
        self.canceled = True
        super().reject()
