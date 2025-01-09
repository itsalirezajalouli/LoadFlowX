from PyQt6.QtWidgets import (QDialog, QTableWidget, QTableWidgetItem, 
    QVBoxLayout, QWidget, QLabel, QHeaderView, QMainWindow, QDialogButtonBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPalette, QColor
import csv

class CsvViewer(QDialog):
    def __init__(self, parent, csvPath: str = None):
        super(CsvViewer, self).__init__(parent)
        self.setWindowTitle('CSV Data')
        self.setMinimumSize(800, 600)
        
        # Create layout
        mainLayout = QVBoxLayout(self)
        
        # Create table
        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.table.verticalHeader().setVisible(False)
        
        # Style the table and dialog
        self.styleTable()
        self.styleDialog()

        # Button Box
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.accepted.connect(self.accept)
        
        mainLayout.addWidget(self.table)
        mainLayout.addWidget(self.buttonBox)

        
        # Set window modality
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        
        # Load CSV if path is provided
        if csvPath:
            self.loadCsv(csvPath)
    
    def styleDialog(self):
        self.setStyleSheet('''
            QDialog {
                color: #ffffff;
                background-color: #2c2f33;
            }
            QTableWidget {
                color: #ffffff;
                background-color: #2c2f33;
                border: 1px solid #dddddd;
                border-radius: 4px;
            }
        ''')
    
    def styleTable(self):
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor('#3b3e45'))
        self.table.setPalette(palette)
        
        headerStyle = '''
            QHeaderView::section {
                color: #ffffff;
                background-color: #2c2f33;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        '''
        self.table.horizontalHeader().setStyleSheet(headerStyle)
    
    def loadCsv(self, csvPath):
        try:
            with open(csvPath, 'r') as file:
                csvReader = csv.reader(file)
                headers = next(csvReader)
                data = list(csvReader)
            
            self.table.setColumnCount(len(headers))
            self.table.setRowCount(len(data))
            self.table.setHorizontalHeaderLabels(headers)
            
            # Populate table
            for i, row in enumerate(data):
                for j, value in enumerate(row):
                    item = QTableWidgetItem(value)
                    item.setTextAlignment(int(Qt.AlignmentFlag.AlignCenter))
                    self.table.setItem(i, j, item)
            
            # Auto-adjust columns
            self.table.resizeColumnsToContents()
            
        except Exception as e:
            print(f'Error loading CSV: {str(e)}')
