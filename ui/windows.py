import sys
import re
import threading
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QCheckBox, QFileDialog,
    QGroupBox, QGridLayout, QMessageBox, QFrame, QSizePolicy,
    QSpacerItem, QStatusBar
)
from PySide6.QtGui import QIcon, QFont, QPixmap, QColor
from PySide6.QtCore import Qt, Signal, Slot, QThread

import scraper
from .styles import theme

class ScraperWorker(QThread):
    """Worker thread to run the scraper without blocking the UI"""
    finished = Signal(bool, str)
    
    def __init__(self, username, password, module_code, output_folder):
        super().__init__()
        self.username = username
        self.password = password
        self.module_code = module_code
        self.output_folder = output_folder
        self.scraper = scraper.Scraper()
        
    def run(self):
        result = self.scraper.start(
            self.username, 
            self.password, 
            self.module_code.upper(), 
            self.output_folder
        )
        
        # Signal the result
        if result is True:
            self.finished.emit(True, "Success")
        else:
            self.finished.emit(False, str(result))


class MainWindow(QMainWindow):
    """Main application window for the Maynooth Paper Prep application"""
    
    def __init__(self):
        super().__init__()
        
        # Window settings
        self.setWindowTitle("Maynooth Paper Scraper")
        self.setGeometry(100, 100, 600, 400)
        
        # Application variables
        self.output_folder = "./papers"  # Default output folder
        
        # Set up the UI
        self.setup_ui()
        self.apply_theme()
        
    def setup_ui(self):
        """Set up the user interface"""
        # Main widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Header with theme toggle
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 10)
        
        title_label = QLabel("Maynooth Paper Scraper")
        title_label.setObjectName("titleLabel")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        
        self.theme_button = QPushButton("Toggle Theme")
        self.theme_button.setObjectName("themeButton")
        self.theme_button.setToolTip("Toggle Dark/Light Theme")
        self.theme_button.clicked.connect(self.toggle_theme)
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.theme_button)
        
        main_layout.addLayout(header_layout)
        
        # Login section
        login_group = QGroupBox("Login Information")
        login_layout = QGridLayout()
        login_group.setLayout(login_layout)
        
        # Username
        username_label = QLabel("Username:")
        username_label.setObjectName("fieldLabel")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Student ID (e.g. 12345678)")
        login_layout.addWidget(username_label, 0, 0)
        login_layout.addWidget(self.username_input, 0, 1)
        
        # Password
        password_label = QLabel("Password:")
        password_label.setObjectName("fieldLabel")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Your Maynooth account password")
        login_layout.addWidget(password_label, 1, 0)
        login_layout.addWidget(self.password_input, 1, 1)
        
        main_layout.addWidget(login_group)
        
        # Paper Info section
        paper_group = QGroupBox("Paper Information")
        paper_layout = QGridLayout()
        paper_group.setLayout(paper_layout)
        
        # Module Code
        module_label = QLabel("Module Code:")
        module_label.setObjectName("fieldLabel")
        self.module_input = QLineEdit()
        self.module_input.setPlaceholderText("E.g. CS101")
        paper_layout.addWidget(module_label, 0, 0)
        paper_layout.addWidget(self.module_input, 0, 1)
        
        # Output Directory
        output_label = QLabel("Output Directory:")
        output_label.setObjectName("fieldLabel")
        output_layout = QHBoxLayout()
        self.output_display = QLineEdit(self.output_folder)
        self.output_display.setReadOnly(True)
        output_btn = QPushButton("Browse...")
        output_btn.setObjectName("browseButton")
        output_btn.clicked.connect(self.select_output_folder)
        output_layout.addWidget(self.output_display)
        output_layout.addWidget(output_btn)
        paper_layout.addWidget(output_label, 1, 0)
        paper_layout.addLayout(output_layout, 1, 1)
        
        main_layout.addWidget(paper_group)
        
        # AI Settings section
        ai_group = QGroupBox("AI Settings (Note generation currently unavailable)")
        ai_layout = QGridLayout()
        ai_group.setLayout(ai_layout)
        
        # API Key
        api_label = QLabel("GPT API Key:")
        api_label.setObjectName("fieldLabel")
        self.api_input = QLineEdit()
        self.api_input.setPlaceholderText("Enter your OpenAI API key")
        ai_layout.addWidget(api_label, 0, 0)
        ai_layout.addWidget(self.api_input, 0, 1, 1, 4)
        
        # Options
        options_label = QLabel("Options:")
        options_label.setObjectName("fieldLabel")
        ai_layout.addWidget(options_label, 1, 0)
        
        # Checkboxes
        self.study_plan_cb = QCheckBox("Create Study Plan")
        self.questions_cb = QCheckBox("Create Sample Questions")
        self.flashcards_cb = QCheckBox("Create Flashcards")
        self.lolcat_cb = QCheckBox("lolcat")
        
        ai_layout.addWidget(self.study_plan_cb, 1, 1)
        ai_layout.addWidget(self.questions_cb, 1, 2)
        ai_layout.addWidget(self.flashcards_cb, 1, 3)
        ai_layout.addWidget(self.lolcat_cb, 1, 4)
        
        main_layout.addWidget(ai_group)
        
        # Start button
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        self.start_button = QPushButton("Start")
        self.start_button.setObjectName("startButton")
        self.start_button.clicked.connect(self.start_scraper)
        button_layout.addWidget(self.start_button)
        button_layout.addStretch()
        
        main_layout.addLayout(button_layout)
        
        # Add stretch to push everything to the top
        main_layout.addStretch()
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
    def apply_theme(self):
        """Apply the current theme to the application"""
        self.setStyleSheet(theme.get_stylesheet())
        
    def toggle_theme(self):
        """Toggle between light and dark themes"""
        theme.toggle_theme()
        self.apply_theme()
        
        # Update status bar with theme info
        current_theme = "Dark" if theme.current_theme == "dark" else "Light"
        self.status_bar.showMessage(f"{current_theme} theme applied")
    
    def select_output_folder(self):
        """Open a dialog to select the output folder"""
        folder_path = QFileDialog.getExistingDirectory(
            self, 
            "Select Output Folder",
            str(Path(self.output_folder).absolute())
        )
        if folder_path:
            self.output_folder = folder_path
            self.output_display.setText(folder_path)
    
    def start_scraper(self):
        """Validate inputs and start the scraping process"""
        # Validate inputs
        if not re.search(r"[0-9]{8}", self.username_input.text()):
            QMessageBox.critical(
                self, 
                "Error", 
                "Invalid username format. Use your student ID (e.g., 12345678)"
            )
            return
            
        if not self.password_input.text():
            QMessageBox.critical(self, "Error", "Password cannot be empty")
            return
            
        if not self.module_input.text():
            QMessageBox.critical(self, "Error", "Module code cannot be empty")
            return
            
        if not self.output_folder:
            QMessageBox.critical(self, "Error", "Output folder cannot be empty")
            return
        
        # Disable the start button and change its text
        self.start_button.setEnabled(False)
        self.start_button.setText("Scraping...")
        self.status_bar.showMessage("Scraping in progress...")
        
        # Start the scraper in a separate thread
        self.worker = ScraperWorker(
            self.username_input.text(),
            self.password_input.text(),
            self.module_input.text(),
            self.output_folder
        )
        self.worker.finished.connect(self.on_scraper_finished)
        self.worker.start()
    
    def on_scraper_finished(self, success, message):
        """Handle the completion of the scraper thread"""
        # Re-enable the start button
        self.start_button.setEnabled(True)
        self.start_button.setText("Start")
        
        if success:
            print("Generating Notes...")
            self.status_bar.showMessage("Scraping completed successfully!")
            QMessageBox.information(self, "Success", "Scraping completed successfully!")
        else:
            self.status_bar.showMessage("Error: Scraping failed")
            QMessageBox.critical(self, "Error", message)


def run_app():
    """Run the application"""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())