# Dialogs for Generator
from psa_components import Generator
from PyQt6.QtWidgets import (
    QDialog, QLabel, QWidget, QHBoxLayout, QLineEdit, QComboBox, QVBoxLayout,
    QDialogButtonBox, QMessageBox, QCheckBox
)
from PyQt6.QtGui import QDoubleValidator

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
        QComboBox {
            font-size: 12px;
            color: #ffffff;
        }
        QCheckBox {
            font-size: 12px;
            color: #ffffff;
        }
        ''')
        
        # Title
        self.title = QLabel('Add Generator to Network')
        self.title.setStyleSheet('''
            color: #ffffff;
            border: 2px solid #7289da;
            border-radius: 5px;
            padding: 8px;
        ''')

        # Generator Name Input
        self.nameWidget = QWidget()
        self.nameHBox = QHBoxLayout()
        self.nameLabel = QLabel('Name:')
        starLabelName = QLabel('*  ')
        starLabelName.setStyleSheet('color: #f04747;')
        self.nameInput = QLineEdit(self)
        self.nameInput.setPlaceholderText('i.e. Gen1')
        self.nameHBox.addWidget(self.nameLabel)
        self.nameHBox.addWidget(starLabelName)
        self.nameHBox.addWidget(self.nameInput)
        self.nameWidget.setLayout(self.nameHBox)

        # Active Power and Unit
        self.pWidget = QWidget()
        self.pHBox = QHBoxLayout()
        self.pLabel = QLabel('P:')
        starLabelP = QLabel('*  ')
        starLabelP.setStyleSheet('color: #f04747;')
        self.pInput = QLineEdit(self)
        self.pInput.setPlaceholderText('Active Power')
        self.pInput.setValidator(QDoubleValidator())
        self.pUnitDropDown = QComboBox(self)
        self.pUnitDropDown.addItem('MW')
        self.pUnitDropDown.addItem('PU')
        self.pUnitDropDown.currentIndexChanged.connect(self.updatePUnit)
        self.pHBox.addWidget(self.pLabel)
        self.pHBox.addWidget(starLabelP)
        self.pHBox.addWidget(self.pInput)
        self.pHBox.addWidget(self.pUnitDropDown)
        self.pWidget.setLayout(self.pHBox)

        # Voltage Magnitude and Unit
        self.vmWidget = QWidget()
        self.vmHBox = QHBoxLayout()
        self.vmLabel = QLabel('V:')
        starLabelVm = QLabel('*  ')
        starLabelVm.setStyleSheet('color: #f04747;')
        self.vmInput = QLineEdit(self)
        self.vmInput.setPlaceholderText('Voltage Magnitude')
        self.vmInput.setValidator(QDoubleValidator())
        self.vmUnitDropDown = QComboBox(self)
        self.vmUnitDropDown.addItem('PU')
        self.vmUnitDropDown.addItem('kV')
        self.vmUnitDropDown.currentIndexChanged.connect(self.updateVmUnit)
        self.vmHBox.addWidget(self.vmLabel)
        self.vmHBox.addWidget(starLabelVm)
        self.vmHBox.addWidget(self.vmInput)
        self.vmHBox.addWidget(self.vmUnitDropDown)
        self.vmWidget.setLayout(self.vmHBox)

        # Additional Parameters Checkbox
        self.additionalParamsCheckbox = QCheckBox('Show additional parameters')
        self.additionalParamsCheckbox.setChecked(False)
        self.additionalParamsCheckbox.toggled.connect(self.toggleAdditionalParameters)

        # Reactive Power Range (minQMvar and maxQMvar)
        self.qWidget = QWidget()
        self.qHBox = QHBoxLayout()
        self.minQLabel = QLabel('Min Q:')
        self.minQInput = QLineEdit(self)
        self.minQInput.setPlaceholderText('Min Reactive Power (MVar)')
        self.minQInput.setValidator(QDoubleValidator())
        self.maxQLabel = QLabel('Max Q:')
        self.maxQInput = QLineEdit(self)
        self.maxQInput.setPlaceholderText('Max Reactive Power (MVar)')
        self.maxQInput.setValidator(QDoubleValidator())
        self.qHBox.addWidget(self.minQLabel)
        self.qHBox.addWidget(self.minQInput)
        self.qHBox.addWidget(self.maxQLabel)
        self.qHBox.addWidget(self.maxQInput)
        self.qWidget.setLayout(self.qHBox)

        # Active Power Range (minPMW and maxPMW)
        self.pRangeWidget = QWidget()
        self.pRangeHBox = QHBoxLayout()
        self.minPLabel = QLabel('Min P:')
        self.minPInput = QLineEdit(self)
        self.minPInput.setPlaceholderText('Min Active Power (MW)')
        self.minPInput.setValidator(QDoubleValidator())
        self.maxPLabel = QLabel('Max P:')
        self.maxPInput = QLineEdit(self)
        self.maxPInput.setPlaceholderText('Max Active Power (MW)')
        self.maxPInput.setValidator(QDoubleValidator())
        self.pRangeHBox.addWidget(self.minPLabel)
        self.pRangeHBox.addWidget(self.minPInput)
        self.pRangeHBox.addWidget(self.maxPLabel)
        self.pRangeHBox.addWidget(self.maxPInput)
        self.pRangeWidget.setLayout(self.pRangeHBox)

        # Button Box
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.accepted.connect(self.accept)

        # Main Layout
        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.nameWidget)
        layout.addWidget(self.pWidget)
        layout.addWidget(self.vmWidget)
        layout.addWidget(self.additionalParamsCheckbox)
        layout.addWidget(self.qWidget)
        layout.addWidget(self.pRangeWidget)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

        # Initially hide additional parameters
        self.qWidget.hide()
        self.pRangeWidget.hide()

    def updatePUnit(self, index):
        """Handle active power unit change"""
        if index == 0:  # MW
            self.removePBaseFields()
            self.pInput.setPlaceholderText('i.e. 100 MW')
        else:  # PU
            self.addPBaseFields()
            self.pInput.setPlaceholderText('i.e. 1.02 PU')

    def updateVmUnit(self, index):
        """Handle voltage magnitude unit change"""
        if index == 0:  # PU
            self.removeVmBaseFields()
            self.vmInput.setPlaceholderText('i.e. 1.02 PU')
        else:  # kV
            self.addVmBaseFields()
            self.vmInput.setPlaceholderText('i.e. 400 kV')

    def addPBaseFields(self):
        """Add base power input fields"""
        if not hasattr(self, 'pBaseLabel'):
            self.pBaseLabel = QLabel('SBase:')
            self.pBaseStarLabel = QLabel('*')
            self.pBaseStarLabel.setStyleSheet('color: #f04747;')
            self.pBaseInput = QLineEdit(self)
            self.pBaseInput.setPlaceholderText('i.e. 100 MVA')
            self.pBaseInput.setValidator(QDoubleValidator())
            self.pHBox.addWidget(self.pBaseLabel)
            self.pHBox.addWidget(self.pBaseStarLabel)
            self.pHBox.addWidget(self.pBaseInput)

    def removePBaseFields(self):
        """Remove base power input fields"""
        if hasattr(self, 'pBaseLabel'):
            self.pBaseLabel.deleteLater()
            self.pBaseStarLabel.deleteLater()
            self.pBaseInput.deleteLater()
            del self.pBaseLabel, self.pBaseStarLabel, self.pBaseInput

    def addVmBaseFields(self):
        """Add base voltage input fields"""
        if not hasattr(self, 'vmBaseLabel'):
            self.vmBaseLabel = QLabel('VBase:')
            self.vmBaseStarLabel = QLabel('*')
            self.vmBaseStarLabel.setStyleSheet('color: #f04747;')
            self.vmBaseInput = QLineEdit(self)
            self.vmBaseInput.setPlaceholderText('i.e. 400 kV')
            self.vmBaseInput.setValidator(QDoubleValidator())
            self.vmHBox.addWidget(self.vmBaseLabel)
            self.vmHBox.addWidget(self.vmBaseStarLabel)
            self.vmHBox.addWidget(self.vmBaseInput)

    def removeVmBaseFields(self):
        """Remove base voltage input fields"""
        if hasattr(self, 'vmBaseLabel'):
            self.vmBaseLabel.deleteLater()
            self.vmBaseStarLabel.deleteLater()
            self.vmBaseInput.deleteLater()
            del self.vmBaseLabel, self.vmBaseStarLabel, self.vmBaseInput

    def toggleAdditionalParameters(self, checked):
        """Toggle visibility of additional parameter fields"""
        self.qWidget.setVisible(checked)
        self.pRangeWidget.setVisible(checked)

    def accept(self) -> None:
        """Handle dialog acceptance with proper input validation"""
        # Validate required fields
        if not all([self.nameInput.text(), self.pInput.text(), self.vmInput.text()]):
            QMessageBox.warning(self, 'Required Fields Empty',
                              'Please fill all required fields marked with *',
                              QMessageBox.StandardButton.Ok)
            return

        try:
            # Handle active power conversion
            p_value = float(self.pInput.text())
            if self.pUnitDropDown.currentText() == 'PU':
                if not hasattr(self, 'pBaseInput') or not self.pBaseInput.text():
                    QMessageBox.warning(self, 'Base Power Required',
                                      'Please enter base power value when using PU',
                                      QMessageBox.StandardButton.Ok)
                    return
                p_value *= float(self.pBaseInput.text())

            # Handle voltage magnitude conversion
            vm_value = float(self.vmInput.text())
            if self.vmUnitDropDown.currentText() == 'kV':
                if not hasattr(self, 'vmBaseInput') or not self.vmBaseInput.text():
                    QMessageBox.warning(self, 'Base Voltage Required',
                                      'Please enter base voltage value when using kV',
                                      QMessageBox.StandardButton.Ok)
                    return
                vm_value /= float(self.vmBaseInput.text())

            # Handle additional parameters
            if self.additionalParamsCheckbox.isChecked():
                min_q = float(self.minQInput.text()) if self.minQInput.text() else -1e6
                max_q = float(self.maxQInput.text()) if self.maxQInput.text() else 1e6
                min_p = float(self.minPInput.text()) if self.minPInput.text() else 0.0
                max_p = float(self.maxPInput.text()) if self.maxPInput.text() else 1e6
            else:
                min_q = -1e6
                max_q = 1e6
                min_p = 0.0
                max_p = 1e6

            # Create generator object
            generator = Generator(
                id=self.genId,
                bus=self.bus,
                name=self.nameInput.text(),
                pMW=p_value,
                vmPU=vm_value,
                minQMvar=min_q,
                maxQMvar=max_q,
                minPMW=min_p,
                maxPMW=max_p,
                pos=self.genPos,
                orient=self.genOri,
                hand=self.genHand
            )
            generator.log()
            generator.append2CSV(self.projectPath)
            super().accept()

        except ValueError as e:
            QMessageBox.critical(self, 'Invalid Input',
                               f'Please enter valid numeric values: {str(e)}',
                               QMessageBox.StandardButton.Ok)
        except Exception as e:
            QMessageBox.critical(self, 'Error',
                               f'Failed to create generator: {str(e)}',
                               QMessageBox.StandardButton.Ok)
