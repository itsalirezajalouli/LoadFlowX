# Dialogs for lines
from psa_components import Line
from PyQt6.QtWidgets import QDialog, QLabel, QWidget, QHBoxLayout, QLineEdit, QComboBox, QVBoxLayout, QDialogButtonBox, QMessageBox, QCheckBox

class AddLineDialog(QDialog):
    def __init__(self, parent, bus1, bus2, theme='dark') -> None:
        super().__init__(parent)
        self.projectPath = None
        self.inputError = False
        self.bus1Id = bus1
        self.bus2Id = bus2
        self.extraParams = False
        self.canceled = False
        self.setWindowTitle('Add Line')

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

        self.title = QLabel('Add Line to Network')
        self.title.setStyleSheet(f'''
            color: {'#ffffff' if theme == 'dark' else '#000000'};
            font-weight: bold;
            border: 2px solid #7289da;
            border-radius: 5px;
            padding: 10px;
        ''')

        # Line Name Input Box
        self.nameWidget = QWidget()
        self.nameHBox = QHBoxLayout()
        self.nameInputLabel = QLabel('Line Name:')
        self.nameInput = QLineEdit(self)
        self.nameInput.setPlaceholderText('Set a name for the line')
        self.nameInputLabel.setStyleSheet(f'color: {"#ffffff" if theme == "dark" else "#000000"};')
        starLabel = QLabel('*  ')
        starLabel.setStyleSheet('color: #f04747;')
        self.nameHBox.addWidget(self.nameInputLabel)
        self.nameHBox.addWidget(starLabel)
        self.nameHBox.addWidget(self.nameInput)
        self.nameWidget.setLayout(self.nameHBox)

        # Impedance Inputs (R, X)
        self.impedanceLabel = QLabel('Impedance (R, X):')
        self.impedanceLabel.setStyleSheet(f'color: {"#ffffff" if theme == "dark" else "#000000"};')
        self.impedanceWidget = QWidget()
        self.impedanceHBox = QHBoxLayout()

        self.rInput = QLineEdit(self)
        self.rInput.setPlaceholderText('R (Ohm/km)')
        self.xInput = QLineEdit(self)
        self.xInput.setPlaceholderText('X (Ohm/km)')

        self.impedanceHBox.addWidget(self.rInput)
        self.impedanceHBox.addWidget(self.xInput)
        self.impedanceWidget.setLayout(self.impedanceHBox)

        # Length Input Box
        self.lenWidget = QWidget()
        self.lenHBox = QHBoxLayout()
        self.lenLabel = QLabel('Length (km):')
        self.lenLabel.setStyleSheet(f'color: {"#ffffff" if theme == "dark" else "#000000"};')
        starLabel = QLabel('*  ')
        starLabel.setStyleSheet('color: #f04747;')
        self.lenInput = QLineEdit(self)
        self.lenInput.setPlaceholderText('Length of the line (km)')
        self.lenUnitDropDown = QComboBox(self)
        self.lenUnitDropDown.addItem('KM   ')
        self.lenHBox.addWidget(self.lenLabel)
        self.lenHBox.addWidget(starLabel)
        self.lenHBox.addWidget(self.lenInput)
        self.lenHBox.addWidget(self.lenUnitDropDown)
        self.lenWidget.setLayout(self.lenHBox)

        # Capacitance and Max Current Inputs
        self.additionalFieldsLabel = QLabel('Additional Parameters:')
        self.additionalFieldsLabel.setStyleSheet(f'color: {"#ffffff" if theme == "dark" else "#000000"};')
        self.additionalFieldsHBox = QHBoxLayout()

        self.cInput = QLineEdit(self)
        self.cInput.setPlaceholderText('Capacitance (nF/km)')
        self.iMaxInput = QLineEdit(self)
        self.iMaxInput.setPlaceholderText('Max Current (kA)')

        self.additionalFieldsHBox.addWidget(self.cInput)
        self.additionalFieldsHBox.addWidget(self.iMaxInput)
        self.additionalFieldsWidget = QWidget()
        self.additionalFieldsWidget.setLayout(self.additionalFieldsHBox)

        # Checkbox for Extra Parameters
        self.extraParamsCheckBox = QCheckBox('Extra Parameters')
        self.extraParamsCheckBox.setStyleSheet(f'color: {"#ffffff" if theme == "dark" else "#000000"};')
        self.extraParamsCheckBox.stateChanged.connect(self.toggleExtraParameters)

        # Button Box
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.accepted.connect(self.accept)

        # Main Layout
        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.nameWidget)
        layout.addWidget(self.lenWidget)
        layout.addWidget(self.extraParamsCheckBox)
        layout.addWidget(self.impedanceWidget)
        layout.addWidget(self.additionalFieldsLabel)
        layout.addWidget(self.additionalFieldsWidget)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

        # Initially hide extra parameters
        self.toggleExtraParameters()

    def toggleExtraParameters(self):
        #Toggle visibility of extra parameter fields
        self.extraParams = self.extraParamsCheckBox.isChecked()
        self.impedanceWidget.setVisible(self.extraParams)
        self.additionalFieldsLabel.setVisible(self.extraParams)
        self.additionalFieldsWidget.setVisible(self.extraParams)

    def accept(self) -> None:
        inputList = [self.nameInput.text(), self.lenInput.text()]
        if self.extraParams:
            inputList.extend([self.rInput.text(), self.xInput.text(), self.cInput.text(),
                              self.iMaxInput.text()])

        # Check if any input is empty
        if '' in inputList:
            self.inputError = True
            QMessageBox.warning(self, 'Fill all the necessary fields.',
                'No necessary field can be empty! Please fill them.', QMessageBox.StandardButton.Ok)
            return
        else:
            self.inputError = False

        # Create the line object with the provided inputs
        if self.extraParams:
            line = Line(
                bus1id=self.bus1Id,
                bus2id=self.bus2Id,
                name=self.nameInput.text(),
                R=float(self.rInput.text()),
                X=float(self.xInput.text()),
                len=float(self.lenInput.text()),
                c_nf_per_km=float(self.cInput.text()),
                max_i_ka=float(self.iMaxInput.text())
            )
        else:
            line = Line(
                bus1id=self.bus1Id,
                bus2id=self.bus2Id,
                name=self.nameInput.text(),
                len=float(self.lenInput.text())
            )

        line.log()
        line.append2CSV(self.projectPath)
        super().accept()

    def reject(self) -> None:
        self.canceled = True
        super().accept()
