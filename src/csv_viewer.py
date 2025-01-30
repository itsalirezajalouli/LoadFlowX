from PyQt6.QtWidgets import (QDialog, QTableWidget, QTableWidgetItem, 
    QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QLabel, QHeaderView, QTabWidget)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor
import csv

class CsvViewer(QDialog):
    def __init__(self, parent: QWidget = None, csvPaths: dict = None, time = 0, theme: str = 'dark'):
        super(CsvViewer, self).__init__(parent)
        
        self.theme = theme
        self.colors = {
            'dark': {
                'text': '#ffffff',
                'background': '#2c2f33',
                'border': '#7289da',
                'alternate': '#3b3e45',
                'button': '#23272a',
                'button_hover': '#99aab5'
            },
            'light': {
                'text': '#000000',
                'background': '#ffffff',
                'border': f'{QColor(30, 144, 255).name()}',
                'alternate': '#d9d9d9',
                'button': '#d9d9d9',
                'button_hover': '#99aab5'
            }
        }
        
        self.setWindowTitle('Simulation Results')
        self.setMinimumSize(1000, 700)
        
        # Create main layout
        mainLayout = QVBoxLayout(self)
        
        # Create execution time label
        self.exeTimeLabel = QLabel(f'Load flow calculations took {time:.4f} seconds')
        self.exeTimeLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        # Create tab widget
        self.tabWidget = QTabWidget()
        self.tabWidget.setTabPosition(QTabWidget.TabPosition.North)
        self.tabWidget.setMovable(True)
        
        # Create OK button
        self.okButton = QPushButton('OK')
        self.okButton.clicked.connect(self.accept)
        
        # Create button layout
        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch()
        buttonLayout.addWidget(self.okButton)
        
        # Add widgets to main layout
        mainLayout.addWidget(self.exeTimeLabel)
        mainLayout.addWidget(self.tabWidget)
        mainLayout.addLayout(buttonLayout)
        
        # Style the dialog
        self.styleDialog()
        
        # Set window modality
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        
        # Load CSVs if paths are provided
        if csvPaths:
            self.loadCsvs(csvPaths)

    def styleDialog(self):
        c = self.colors['dark'] if self.theme == 'dark' else self.colors['light']
        
        self.setStyleSheet(f'''
            QDialog {{
                font-size: 14px;
                color: {c['text']};
                background-color: {c['background']};
                border-radius: 10px;
                padding: 2px;
            }}
            
            QLabel {{
                font-size: 14px;
                color: {c['text']};
                padding: 5px;
                background-color: {c['background']};
                border: 1px solid {c['border']};
                border-radius: 3px;
                font-family: monospace;
            }}
            
            QTableWidget {{
                color: {c['text']};
                border-radius: 4px;
                background-color: {c['background']};
            }}
            
            QTabWidget::pane {{
                color: {c['text']};
                border: 1px solid {c['border']};
                border-radius: 4px;
            }}
            
            QTabBar::tab {{
                color: {c['text']};
                border: 1px solid {c['border']};
                background-color: {c['background']};
                padding: 8px 12px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }}
            
            QTabBar::tab:selected {{
                background: {c['background']};
                border-bottom-color: {c['border']};
            }}
            
            QTabBar::tab:hover {{
                color: {c['text']};
                background: {c['alternate']};
            }}
            
            QPushButton {{
                background-color: {c['button']};
                color: {c['text']};
                border: 1px solid {c['border']};
                border-radius: 5px;
                padding: 5px 15px;
                font-size: 12px;
            }}
            
            QPushButton:hover {{
                background-color: {c['button_hover']};
            }}
            
            QPushButton:pressed {{
                background-color: {c['alternate']};
            }}
        ''')
    
    def createTable(self):
        table = QTableWidget()
        table.setAlternatingRowColors(True)
        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        table.verticalHeader().setVisible(False)
        
        # Style the table
        c = self.colors['dark'] if self.theme == 'dark' else self.colors['light']
        palette = table.palette()
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(c['alternate']))
        table.setPalette(palette)
        
        headerStyle = f'''
            QHeaderView::section {{
                color: {c['text']};
                background-color: {c['background']};
                padding: 8px;
                border: none;
                border-right: 1px solid {c['border']};
                font-weight: bold;
            }}
        '''
        table.horizontalHeader().setStyleSheet(headerStyle)
        return table

    # Rest of the class implementation remains the same
    def loadCsvs(self, csvPaths: dict):
        for tabName, path in csvPaths.items():
            try:
                table = self.createTable()
                
                with open(path, 'r') as file:
                    csvReader = csv.reader(file)
                    headers = next(csvReader)
                    data = list(csvReader)
                
                table.setColumnCount(len(headers))
                table.setRowCount(len(data))
                table.setHorizontalHeaderLabels(headers)
                
                for i, row in enumerate(data):
                    for j, value in enumerate(row):
                        item = QTableWidgetItem(value)
                        item.setTextAlignment(int(Qt.AlignmentFlag.AlignCenter))
                        table.setItem(i, j, item)
                
                table.resizeColumnsToContents()
                self.tabWidget.addTab(table, tabName)
                
            except Exception as e:
                print(f'Error loading CSV for {tabName}: {str(e)}')
                errorWidget = QWidget()
                errorLayout = QVBoxLayout(errorWidget)
                errorLabel = QLabel(f'Error loading data: {str(e)}')
                errorLabel.setStyleSheet('color: red;')
                errorLayout.addWidget(errorLabel)
                self.tabWidget.addTab(errorWidget, tabName)
