class DiscordPalette:
    '''Discord Color Palette for PyQt6
    Provides both hex and RGB representations for easy use.
    '''
    # Base Colors
    background = '#2C2F33'  # Discord's dark mode background
    foreground = '#FFFFFF'  # White text
    
    # Accent Colors
    red = '#F04747'      # Red for destructive actions or errors
    green = '#43B581'    # Green for success or online
    yellow = '#FAA61A'   # Yellow for warnings or away
    blue = '#7289DA'     # Discord's brand blue
    purple = '#9B59B6'   # Purple for custom highlights
    cyan = '#00BFFF'     # Cyan for information or subtle highlights

    # Grayscale
    commentGrey = '#99AAB5'  # Subtle text or placeholders
    lightGrey = '#36393F'    # Input field background
    darkGrey = '#23272A'     # Deeper background elements

    @classmethod
    def stylesheet(cls):
        '''Returns a complete stylesheet using the Discord palette'''
        return f''' 
QWidget {{ background-color: {cls.background}; color: {cls.foreground}; selection-background-color: {cls.blue}; selection-color: {cls.background}; }}
QLineEdit, QTextEdit {{ background-color: {cls.darkGrey}; color: {cls.foreground}; border: 1px solid {cls.lightGrey}; }}
QPushButton {{ background-color: {cls.lightGrey}; color: {cls.foreground}; border: none; padding: 5px; }}
QPushButton:hover {{ background-color: {cls.blue}; }} '''

    @classmethod
    def toQtColor(cls, hexColor):
        '''Converts hex color to QColor'''
        from PyQt6.QtGui import QColor
        return QColor(hexColor)
