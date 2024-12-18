# Dialogs for lines
from PyQt6.QtWidgets import QDialog, QLabel, QWidget, QHBoxLayout, QLineEdit, QComboBox, QVBoxLayout, QDialogButtonBox

class AddLineDialog(QDialog):
    def __init__(self, parent) -> None:
        super().__init__(parent)
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
        self.bus1Id = None
        self.bus2Id = None
        self.R = None
        self.X = None
        self.Length = None
        self.vBase = None

        # Line Z Input Box
        self.zLabel = QLabel('Impedances:')
        self.zLabel.setStyleSheet('color: #ffffff;')
        self.zWidget = QWidget()
        self.zHBox = QHBoxLayout()
        self.rInput = QLineEdit(self)
        self.rInput.setPlaceholderText('R')
        self.xInput = QLineEdit(self)
        self.xInput.setPlaceholderText('X')
        self.rUnitDropDown = QComboBox(self) 
        self.rUnitDropDown.addItem('PU')
        self.rUnitDropDown.addItem('Kohm')
        self.xUnitDropDown = QComboBox(self) 
        self.xUnitDropDown.addItem('PU')
        self.xUnitDropDown.addItem('Kohm')
        self.zHBox.addWidget(self.rInput)
        self.zHBox.addWidget(self.rUnitDropDown)
        self.zHBox.addWidget(self.xInput)
        self.zHBox.addWidget(self.xUnitDropDown)
        self.zWidget.setLayout(self.zHBox)

        # Length & V Base
        self.lenHBox = QHBoxLayout()
        self.lenInput = QLineEdit(self)
        self.lenInput.setPlaceholderText('Line Length')
        self.vBaseInput = QLineEdit(self)
        self.vBaseInput.setPlaceholderText('V Base')
        self.lenUnitDropDown = QComboBox(self) 
        self.lenUnitDropDown.addItem('KM')
        self.lenUnitDropDown.addItem('Miles')
        self.vbUnitDropDown = QComboBox(self) 
        self.vbUnitDropDown.addItem('PU')
        self.vbUnitDropDown.addItem('KV')
        self.lenHBox.addWidget(self.lenInput)
        self.lenHBox.addWidget(self.lenUnitDropDown)
        self.lenHBox.addWidget(self.vBaseInput)
        self.lenHBox.addWidget(self.vbUnitDropDown)
        self.lenWidget = QWidget()
        self.lenWidget.setLayout(self.lenHBox)

        # Button Box
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.accepted.connect(self.accept)

        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.zLabel)
        layout.addWidget(self.zWidget)
        layout.addWidget(self.lenWidget)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)
