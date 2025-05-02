"""
Styling for the Maynooth Paper Prep application.
Provides light and dark themes with easy switching.
"""

class AppTheme:
    """Manages application themes and provides easy access to stylesheets"""
    
    def __init__(self):
        self.current_theme = "light"
    
    def get_stylesheet(self):
        """Returns the current theme's stylesheet"""
        if self.current_theme == "dark":
            return self.dark_theme()
        else:
            return self.light_theme()
    
    def set_theme(self, theme_name):
        """Sets the current theme to either 'light' or 'dark'"""
        if theme_name in ["light", "dark"]:
            self.current_theme = theme_name
    
    def toggle_theme(self):
        """Toggles between light and dark themes"""
        self.current_theme = "dark" if self.current_theme == "light" else "light"
    
    @staticmethod
    def light_theme():
        """Returns the light theme stylesheet"""
        return """
            QMainWindow {
                background-color: #f5f5f5;
            }
            
            QWidget {
                color: #333333;
            }
            
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                border: 1px solid #cccccc;
                border-radius: 5px;
                margin-top: 1.5ex;
                padding-top: 10px;
                background-color: white;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 10px;
                color: #3498db;
            }
            
            QLineEdit {
                border: 1px solid #cccccc;
                border-radius: 4px;
                padding: 6px;
                background-color: #fafafa;
            }
            
            QLineEdit:focus {
                border-color: #3498db;
                background-color: white;
            }
            
            QLabel#fieldLabel {
                font-weight: bold;
                color: #333333;
            }
            
            QPushButton {
                border: 1px solid #cccccc;
                border-radius: 4px;
                padding: 6px 12px;
                background-color: #f8f8f8;
                color: #333333;
            }
            
            QPushButton:hover {
                background-color: #eeeeee;
                border-color: #bbbbbb;
            }
            
            QPushButton:pressed {
                background-color: #dddddd;
            }
            
            QPushButton#startButton {
                background-color: #3498db;
                color: white;
                border: 1px solid #2980b9;
                font-weight: bold;
                min-width: 120px;
                min-height: 30px;
            }
            
            QPushButton#startButton:hover {
                background-color: #2980b9;
            }
            
            QPushButton#startButton:disabled {
                background-color: #95a5a6;
                border-color: #7f8c8d;
            }
            
            QPushButton#browseButton {
                min-width: 80px;
            }
            
            QPushButton#themeButton {
                min-width: 30px;
                min-height: 30px;
                border-radius: 15px;
                padding: 3px;
            }
            
            QCheckBox {
                spacing: 5px;
            }
            
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
            }
            
            QCheckBox::indicator:unchecked {
                border: 1px solid #cccccc;
                background-color: white;
            }
            
            QCheckBox::indicator:checked {
                border: 1px solid #3498db;
                background-color: #3498db;
            }
            
            QStatusBar {
                background-color: #f0f0f0;
                color: #333333;
                border-top: 1px solid #cccccc;
            }
            
            QScrollBar:vertical {
                border: none;
                background: #f0f0f0;
                width: 10px;
                margin: 0px;
            }

            QScrollBar::handle:vertical {
                background: #cccccc;
                min-height: 20px;
                border-radius: 5px;
            }

            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """
    
    @staticmethod
    def dark_theme():
        """Returns the dark theme stylesheet"""
        return """
            QMainWindow {
                background-color: #2c3e50;
            }
            
            QWidget {
                color: #ecf0f1;
            }
            
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                border: 1px solid #34495e;
                border-radius: 5px;
                margin-top: 1.5ex;
                padding-top: 10px;
                background-color: #34495e;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 10px;
                color: #3498db;
            }
            
            QLineEdit {
                border: 1px solid #7f8c8d;
                border-radius: 4px;
                padding: 6px;
                background-color: #1a2530;
                color: #ecf0f1;
            }
            
            QLineEdit:focus {
                border-color: #3498db;
                background-color: #1a2530;
            }
            
            QLabel#fieldLabel {
                font-weight: bold;
                color: #ecf0f1;
            }
            
            QPushButton {
                border: 1px solid #7f8c8d;
                border-radius: 4px;
                padding: 6px 12px;
                background-color: #34495e;
                color: #ecf0f1;
            }
            
            QPushButton:hover {
                background-color: #2c3e50;
                border-color: #95a5a6;
            }
            
            QPushButton:pressed {
                background-color: #1a2530;
            }
            
            QPushButton#startButton {
                background-color: #2980b9;
                color: white;
                border: 1px solid #3498db;
                font-weight: bold;
                min-width: 120px;
                min-height: 30px;
            }
            
            QPushButton#startButton:hover {
                background-color: #3498db;
            }
            
            QPushButton#startButton:disabled {
                background-color: #7f8c8d;
                border-color: #95a5a6;
            }
            
            QPushButton#browseButton {
                min-width: 80px;
            }
            
            QPushButton#themeButton {
                min-width: 30px;
                min-height: 30px;
                border-radius: 15px;
                padding: 3px;
            }
            
            QCheckBox {
                spacing: 5px;
            }
            
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
            }
            
            QCheckBox::indicator:unchecked {
                border: 1px solid #7f8c8d;
                background-color: #2c3e50;
            }
            
            QCheckBox::indicator:checked {
                border: 1px solid #3498db;
                background-color: #3498db;
            }
            
            QStatusBar {
                background-color: #1a2530;
                color: #ecf0f1;
                border-top: 1px solid #34495e;
            }
            
            QScrollBar:vertical {
                border: none;
                background: #2c3e50;
                width: 10px;
                margin: 0px;
            }

            QScrollBar::handle:vertical {
                background: #34495e;
                min-height: 20px;
                border-radius: 5px;
            }

            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """


# Create a singleton instance for easy access
theme = AppTheme()

# Export the theme instance
__all__ = ['theme']