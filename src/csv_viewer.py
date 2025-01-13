from PyQt6.QtWidgets import (QDialog, QTableWidget, QTableWidgetItem, 
    QVBoxLayout, QWidget, QLabel, QHeaderView, QTabWidget)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPalette, QColor
import csv

class CsvViewer(QDialog):
    def __init__(self, parent: QWidget = None, csvPaths: dict = None):
        super(CsvViewer, self).__init__(parent)
        
        self.setWindowTitle('Simulation Results')
        self.setMinimumSize(1000, 700)
        
        # Create main layout
        mainLayout = QVBoxLayout(self)
        
        # Create tab widget
        self.tabWidget = QTabWidget()
        self.tabWidget.setTabPosition(QTabWidget.TabPosition.North)
        self.tabWidget.setMovable(True)  # Allow reordering tabs
        
        # Add to main layout
        mainLayout.addWidget(self.tabWidget)
        
        # Style the dialog
        self.styleDialog()
        
        # Set window modality
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        
        # Load CSVs if paths are provided
        if csvPaths:
            self.loadCsvs(csvPaths)


    def styleDialog(self):
        self.setStyleSheet('''
            QDialog {
                color: #dddddd;
                background-color: #2c2f33;
            }
            QTableWidget {
                color: #dddddd;
                border: 1px solid #3b3e45;
                border-radius: 4px;
                background-color: #2c2f33;
            }
            QTabWidget::pane {
                color: #dddddd;
                border: 1px solid #3b3e45;
                border-radius: 4px;
            }
            QTabBar::tab {
                color: #dddddd;
                border: 1px solid #3b3e45;
                background-color: #2c2f33;
                padding: 8px 12px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                color: #dddddd;
                background: #2c2f33;
                border-bottom-color:#3b3e45;
            }
            QTabBar::tab:hover {
                color: #ffffff;
                background: #3b3e45;
            }
        ''')
    
    def createTable(self):
        table = QTableWidget()
        table.setAlternatingRowColors(True)
        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        table.verticalHeader().setVisible(False)
        
        # Style the table
        palette = table.palette()
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor('#3b3e45'))
        table.setPalette(palette)
        
        headerStyle = '''
            QHeaderView::section {
                color: #dddddd;
                background-color: #2c2f33;
                padding: 8px;
                border: none;
                border-right: 1px solid #3b3e45;
                font-weight: bold;
            }
        '''
        table.horizontalHeader().setStyleSheet(headerStyle)
        return table
    
    def loadCsvs(self, csvPaths: dict):
        # Load CSVs into tabs
        for tabName, path in csvPaths.items():
            try:
                # Create new table for this tab
                table = self.createTable()
                
                with open(path, 'r') as file:
                    csvReader = csv.reader(file)
                    headers = next(csvReader)
                    data = list(csvReader)
                
                table.setColumnCount(len(headers))
                table.setRowCount(len(data))
                table.setHorizontalHeaderLabels(headers)
                
                # Populate table
                for i, row in enumerate(data):
                    for j, value in enumerate(row):
                        item = QTableWidgetItem(value)
                        item.setTextAlignment(int(Qt.AlignmentFlag.AlignCenter))
                        table.setItem(i, j, item)
                
                # Auto-adjust columns
                table.resizeColumnsToContents()
                
                # Add table to new tab
                self.tabWidget.addTab(table, tabName)
                
            except Exception as e:
                print(f'Error loading CSV for {tabName}: {str(e)}')
                
                # Create error tab
                errorWidget = QWidget()
                errorLayout = QVBoxLayout(errorWidget)
                errorLabel = QLabel(f'Error loading data: {str(e)}')
                errorLabel.setStyleSheet('color: red;')
                errorLayout.addWidget(errorLabel)
                self.tabWidget.addTab(errorWidget, tabName)
