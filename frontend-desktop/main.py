"""
Chemical Equipment Visualizer - Enhanced Professional Desktop Application
PyQt5 + Matplotlib Frontend with Beautiful Charts - FIXED SIZING
"""

import sys
import os
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from functools import partial
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import patches
import matplotlib.patches as mpatches
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QFileDialog, QMessageBox, QTabWidget, QGroupBox, QFormLayout,
    QScrollArea, QTextEdit, QFrame, QSizePolicy, QGridLayout, QHeaderView
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer, pyqtSignal
from PyQt5.QtGui import QFont, QPalette, QColor, QLinearGradient, QPainter, QBrush, QPen


# API Configuration
API_BASE_URL = "https://chemical-equipment-backend-bjfj.onrender.com/api"

# Professional Color Palette
COLORS = {
    'primary': '#667eea',
    'secondary': '#764ba2',
    'success': '#48bb78',
    'danger': '#f56565',
    'warning': '#ed8936',
    'info': '#4299e1',
    'light': '#f7fafc',
    'dark': '#2d3748',
    'gradient_start': '#667eea',
    'gradient_end': '#764ba2',
    'chart_colors': ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#43e97b',
                     '#fa709a', '#feca57', '#ff6348', '#48dbfb', '#ee5a6f'],
}


class APIClient:
    """Client for interacting with Django REST API"""

    def __init__(self):
        self.base_url = API_BASE_URL
        self.token = None

    def set_token(self, token):
        self.token = token

    def get_headers(self):
        headers = {'Content-Type': 'application/json'}
        if self.token:
            headers['Authorization'] = f'Token {self.token}'
        return headers

    def login(self, username, password):
        """Login user"""
        url = f"{self.base_url}/auth/login/"
        data = {'username': username, 'password': password}
        response = requests.post(url, json=data)
        return response.json()

    def register(self, user_data):
        """Register new user"""
        url = f"{self.base_url}/auth/register/"
        response = requests.post(url, json=user_data)
        return response.json()

    def upload_csv(self, file_path):
        """Upload CSV file"""
        url = f"{self.base_url}/upload/"
        headers = {'Authorization': f'Token {self.token}'}
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(url, headers=headers, files=files)
        return response.json()

    def list_datasets(self):
        """List all datasets"""
        url = f"{self.base_url}/datasets/"
        response = requests.get(url, headers=self.get_headers())
        return response.json()

    def get_dataset(self, dataset_id):
        """Get dataset details"""
        url = f"{self.base_url}/datasets/{dataset_id}/"
        response = requests.get(url, headers=self.get_headers())
        return response.json()

    def delete_dataset(self, dataset_id):
        """Delete dataset"""
        url = f"{self.base_url}/datasets/{dataset_id}/delete/"
        response = requests.delete(url, headers=self.get_headers())
        return response.json()

    def generate_report(self, dataset_id, save_path):
        """Generate and download PDF report"""
        url = f"{self.base_url}/datasets/{dataset_id}/report/"
        response = requests.get(url, headers=self.get_headers())
        with open(save_path, 'wb') as f:
            f.write(response.content)
        return True

    def get_statistics(self):
        """Get user statistics"""
        url = f"{self.base_url}/statistics/"
        response = requests.get(url, headers=self.get_headers())
        return response.json()


class ProfessionalMatplotlibCanvas(FigureCanvas):
    """Enhanced Matplotlib canvas with professional styling"""

    def __init__(self, parent=None, width=5, height=3, dpi=100):
        # Set professional style
        plt.style.use('seaborn-v0_8-darkgrid')

        fig = Figure(figsize=(width, height), dpi=dpi, facecolor='white')
        super().__init__(fig)
        self.setParent(parent)

        # Configure for better rendering
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def create_pie_chart(self, data_dict, title):
        """Create professional pie chart"""
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        labels = list(data_dict.keys())
        sizes = list(data_dict.values())
        colors = COLORS['chart_colors'][:len(labels)]

        # Create pie chart with enhanced styling
        wedges, texts, autotexts = ax.pie(
            sizes,
            labels=labels,
            colors=colors,
            autopct='%1.1f%%',
            startangle=90,
            pctdistance=0.85,
            explode=[0.05] * len(labels),
            shadow=True,
            textprops={'fontsize': 9, 'weight': 'bold'}
        )

        # Enhance text styling
        for text in texts:
            text.set_fontsize(10)
            text.set_weight('bold')

        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(9)
            autotext.set_weight('bold')

        ax.set_title(title, fontsize=12, weight='bold', pad=15)
        ax.axis('equal')

        self.figure.tight_layout()
        self.draw()

    def create_bar_chart(self, labels, values, title, ylabel='Value', colors=None):
        """Create professional bar chart"""
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        if colors is None:
            colors = COLORS['chart_colors'][:len(labels)]

        x_pos = np.arange(len(labels))
        bars = ax.bar(x_pos, values, color=colors, alpha=0.8, edgecolor='white', linewidth=2)

        # Add value labels on top of bars
        for i, (bar, value) in enumerate(zip(bars, values)):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{value:.1f}',
                    ha='center', va='bottom', fontsize=9, weight='bold')

        ax.set_xlabel('Parameters', fontsize=10, weight='bold')
        ax.set_ylabel(ylabel, fontsize=10, weight='bold')
        ax.set_title(title, fontsize=12, weight='bold', pad=15)
        ax.set_xticks(x_pos)
        ax.set_xticklabels(labels, fontsize=9)

        # Style the grid
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.set_axisbelow(True)

        self.figure.tight_layout()
        self.draw()

    def create_grouped_bar_chart(self, equipment_list, title):
        """Create professional grouped bar chart"""
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        # Prepare data
        equipment_names = [eq['equipment_name'][:12] + '...' if len(eq['equipment_name']) > 12
                           else eq['equipment_name'] for eq in equipment_list]
        flowrates = [eq['flowrate'] for eq in equipment_list]
        pressures = [eq['pressure'] for eq in equipment_list]
        temperatures = [eq['temperature'] for eq in equipment_list]

        x = np.arange(len(equipment_names))
        width = 0.25

        # Create bars with professional styling
        bars1 = ax.bar(x - width, flowrates, width, label='Flowrate',
                       color=COLORS['chart_colors'][0], alpha=0.8, edgecolor='white', linewidth=1.5)
        bars2 = ax.bar(x, pressures, width, label='Pressure',
                       color=COLORS['chart_colors'][1], alpha=0.8, edgecolor='white', linewidth=1.5)
        bars3 = ax.bar(x + width, temperatures, width, label='Temperature',
                       color=COLORS['chart_colors'][2], alpha=0.8, edgecolor='white', linewidth=1.5)

        # Customize axes
        ax.set_xlabel('Equipment', fontsize=10, weight='bold')
        ax.set_ylabel('Values', fontsize=10, weight='bold')
        ax.set_title(title, fontsize=12, weight='bold', pad=15)
        ax.set_xticks(x)
        ax.set_xticklabels(equipment_names, rotation=45, ha='right', fontsize=8)

        # Enhanced legend
        ax.legend(loc='upper right', fontsize=9, framealpha=0.9, shadow=True)

        # Grid
        ax.grid(True, alpha=0.3, linestyle='--', axis='y')
        ax.set_axisbelow(True)

        self.figure.tight_layout()
        self.draw()

    def create_line_chart(self, x_data, y_data, title, xlabel, ylabel, label=None):
        """Create professional line chart"""
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        ax.plot(x_data, y_data, color=COLORS['primary'], linewidth=2.5,
                marker='o', markersize=8, markerfacecolor=COLORS['secondary'],
                markeredgecolor='white', markeredgewidth=2, label=label)

        ax.set_xlabel(xlabel, fontsize=10, weight='bold')
        ax.set_ylabel(ylabel, fontsize=10, weight='bold')
        ax.set_title(title, fontsize=12, weight='bold', pad=15)

        if label:
            ax.legend(fontsize=9, framealpha=0.9, shadow=True)

        ax.grid(True, alpha=0.3, linestyle='--')
        ax.set_axisbelow(True)

        self.figure.tight_layout()
        self.draw()


class GradientWidget(QWidget):
    """Widget with gradient background"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.start_color = QColor(COLORS['gradient_start'])
        self.end_color = QColor(COLORS['gradient_end'])

    def paintEvent(self, event):
        painter = QPainter(self)
        gradient = QLinearGradient(0, 0, self.width(), 0)
        gradient.setColorAt(0, self.start_color)
        gradient.setColorAt(1, self.end_color)
        painter.fillRect(self.rect(), gradient)


class StyledButton(QPushButton):
    """Professional styled button"""

    def __init__(self, text, color='primary', parent=None):
        super().__init__(text, parent)
        self.color = color
        self.apply_style()

    def apply_style(self):
        if self.color == 'primary':
            bg_color = COLORS['primary']
            hover_color = '#5568d3'
        elif self.color == 'success':
            bg_color = COLORS['success']
            hover_color = '#38a169'
        elif self.color == 'danger':
            bg_color = COLORS['danger']
            hover_color = '#e53e3e'
        else:
            bg_color = COLORS['info']
            hover_color = '#3182ce'

        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg_color};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 11px;
                font-weight: bold;
                min-width: 70px;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
            QPushButton:pressed {{
                background-color: {bg_color};
                padding-top: 7px;
                padding-bottom: 5px;
            }}
            QPushButton:disabled {{
                background-color: #cbd5e0;
                color: #a0aec0;
            }}
        """)


class StatCard(QFrame):
    """Professional statistics card widget"""

    def __init__(self, title, value, parent=None):
        super().__init__(parent)
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                border: 1px solid #e2e8f0;
                padding: 15px;
            }
            QFrame:hover {
                border: 1px solid #cbd5e0;
                background-color: #f7fafc;
            }
        """)

        layout = QVBoxLayout(self)

        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            QLabel {
                color: #718096;
                font-size: 12px;
                font-weight: 500;
            }
        """)
        layout.addWidget(title_label)

        # Value
        self.value_label = QLabel(str(value))
        self.value_label.setStyleSheet("""
            QLabel {
                color: #2d3748;
                font-size: 28px;
                font-weight: bold;
            }
        """)
        layout.addWidget(self.value_label)

        layout.addStretch()

    def update_value(self, value):
        """Update the value displayed"""
        self.value_label.setText(str(value))


class LoginWindow(QWidget):
    """Enhanced professional login window"""

    login_success = pyqtSignal(str, dict)

    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Chemical Equipment Visualizer - Login')
        self.setGeometry(100, 100, 500, 550)
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
            }
        """)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Login card container
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 20px;
                padding: 35px;
            }
        """)
        card.setMaximumWidth(400)
        card_layout = QVBoxLayout(card)

        # Logo/Title
        title = QLabel('Chemical Equipment\nVisualizer')
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                color: #2d3748;
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 8px;
            }
        """)
        card_layout.addWidget(title)

        subtitle = QLabel('Desktop Application')
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("""
            QLabel {
                color: #718096;
                font-size: 13px;
                margin-bottom: 25px;
            }
        """)
        card_layout.addWidget(subtitle)

        # Login form
        form_layout = QFormLayout()
        form_layout.setSpacing(12)

        # Username
        username_label = QLabel('Username')
        username_label.setStyleSheet("color: #2d3748; font-weight: 500; font-size: 13px;")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Enter your username')
        self.username_input.setStyleSheet("""
            QLineEdit {
                padding: 10px 14px;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                font-size: 13px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 2px solid #667eea;
            }
        """)
        form_layout.addRow(username_label, self.username_input)

        # Password
        password_label = QLabel('Password')
        password_label.setStyleSheet("color: #2d3748; font-weight: 500; font-size: 13px;")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Enter your password')
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("""
            QLineEdit {
                padding: 10px 14px;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                font-size: 13px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 2px solid #667eea;
            }
        """)
        form_layout.addRow(password_label, self.password_input)

        card_layout.addLayout(form_layout)

        # Login button
        self.login_btn = StyledButton('Sign In', 'primary')
        self.login_btn.clicked.connect(self.handle_login)
        self.login_btn.setMinimumHeight(40)
        card_layout.addWidget(self.login_btn)

        # Register button
        self.register_btn = StyledButton('Create New Account', 'success')
        self.register_btn.clicked.connect(self.show_register_form)
        self.register_btn.setMinimumHeight(40)
        card_layout.addWidget(self.register_btn)

        # Message label
        self.message_label = QLabel('')
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setStyleSheet("""
            QLabel {
                color: #f56565;
                font-weight: bold;
                margin-top: 12px;
                padding: 8px;
                background-color: #fed7d7;
                border-radius: 6px;
            }
        """)
        self.message_label.hide()
        card_layout.addWidget(self.message_label)

        layout.addWidget(card)
        self.setLayout(layout)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            self.show_message('Please enter username and password', 'error')
            return

        try:
            self.login_btn.setEnabled(False)
            self.login_btn.setText('Signing in...')
            result = self.api_client.login(username, password)
            if 'token' in result:
                self.api_client.set_token(result['token'])
                self.login_success.emit(result['token'], result['user'])
                self.close()
            else:
                self.show_message('Login failed', 'error')
        except Exception as e:
            self.show_message(f'Error: {str(e)}', 'error')
        finally:
            self.login_btn.setEnabled(True)
            self.login_btn.setText('Sign In')

    def show_message(self, text, msg_type='error'):
        self.message_label.setText(text)
        if msg_type == 'error':
            self.message_label.setStyleSheet("""
                QLabel {
                    color: #c53030;
                    background-color: #fed7d7;
                    padding: 10px;
                    border-radius: 8px;
                    font-weight: bold;
                }
            """)
        else:
            self.message_label.setStyleSheet("""
                QLabel {
                    color: #22543d;
                    background-color: #c6f6d5;
                    padding: 10px;
                    border-radius: 8px;
                    font-weight: bold;
                }
            """)
        self.message_label.show()

    def show_register_form(self):
        register_window = RegisterWindow(self.api_client)
        register_window.register_success.connect(self.handle_register_success)
        register_window.show()

    def handle_register_success(self, token, user):
        self.api_client.set_token(token)
        self.login_success.emit(token, user)
        self.close()


class RegisterWindow(QWidget):
    """Enhanced registration window"""

    register_success = pyqtSignal(str, dict)

    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Create New Account')
        self.setGeometry(150, 150, 500, 650)
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
            }
        """)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Card container
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 20px;
                padding: 35px;
            }
        """)
        card.setMaximumWidth(400)
        card_layout = QVBoxLayout(card)

        # Title
        title = QLabel('Create Account')
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                color: #2d3748;
                font-size: 22px;
                font-weight: bold;
                margin-bottom: 25px;
            }
        """)
        card_layout.addWidget(title)

        # Form
        form_layout = QFormLayout()
        form_layout.setSpacing(10)

        input_style = """
            QLineEdit {
                padding: 10px 14px;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 2px solid #667eea;
            }
        """

        label_style = "color: #2d3748; font-weight: 500; font-size: 12px;"

        self.reg_username = QLineEdit()
        self.reg_username.setPlaceholderText('Choose a username')
        self.reg_username.setStyleSheet(input_style)
        username_label = QLabel('Username *')
        username_label.setStyleSheet(label_style)
        form_layout.addRow(username_label, self.reg_username)

        self.reg_email = QLineEdit()
        self.reg_email.setPlaceholderText('your.email@example.com')
        self.reg_email.setStyleSheet(input_style)
        email_label = QLabel('Email *')
        email_label.setStyleSheet(label_style)
        form_layout.addRow(email_label, self.reg_email)

        self.reg_first_name = QLineEdit()
        self.reg_first_name.setPlaceholderText('John')
        self.reg_first_name.setStyleSheet(input_style)
        first_label = QLabel('First Name')
        first_label.setStyleSheet(label_style)
        form_layout.addRow(first_label, self.reg_first_name)

        self.reg_last_name = QLineEdit()
        self.reg_last_name.setPlaceholderText('Doe')
        self.reg_last_name.setStyleSheet(input_style)
        last_label = QLabel('Last Name')
        last_label.setStyleSheet(label_style)
        form_layout.addRow(last_label, self.reg_last_name)

        self.reg_password = QLineEdit()
        self.reg_password.setPlaceholderText('At least 8 characters')
        self.reg_password.setEchoMode(QLineEdit.Password)
        self.reg_password.setStyleSheet(input_style)
        pass_label = QLabel('Password *')
        pass_label.setStyleSheet(label_style)
        form_layout.addRow(pass_label, self.reg_password)

        self.reg_password_confirm = QLineEdit()
        self.reg_password_confirm.setPlaceholderText('Re-enter password')
        self.reg_password_confirm.setEchoMode(QLineEdit.Password)
        self.reg_password_confirm.setStyleSheet(input_style)
        confirm_label = QLabel('Confirm Password *')
        confirm_label.setStyleSheet(label_style)
        form_layout.addRow(confirm_label, self.reg_password_confirm)

        card_layout.addLayout(form_layout)

        # Register button
        self.register_btn = StyledButton('Create Account', 'success')
        self.register_btn.clicked.connect(self.handle_register)
        self.register_btn.setMinimumHeight(40)
        card_layout.addWidget(self.register_btn)

        # Message
        self.message_label = QLabel('')
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setWordWrap(True)
        self.message_label.hide()
        card_layout.addWidget(self.message_label)

        layout.addWidget(card)
        self.setLayout(layout)

    def handle_register(self):
        username = self.reg_username.text()
        email = self.reg_email.text()
        password = self.reg_password.text()
        password_confirm = self.reg_password_confirm.text()

        if not username or not email or not password:
            self.show_message('Please fill in required fields', 'error')
            return

        if password != password_confirm:
            self.show_message('Passwords do not match', 'error')
            return

        user_data = {
            'username': username,
            'email': email,
            'password': password,
            'password_confirm': password_confirm,
            'first_name': self.reg_first_name.text(),
            'last_name': self.reg_last_name.text(),
        }

        try:
            self.register_btn.setEnabled(False)
            self.register_btn.setText('Creating account...')
            result = self.api_client.register(user_data)
            if 'token' in result:
                self.register_success.emit(result['token'], result['user'])
                self.close()
            else:
                self.show_message('Registration failed', 'error')
        except Exception as e:
            self.show_message(f'Error: {str(e)}', 'error')
        finally:
            self.register_btn.setEnabled(True)
            self.register_btn.setText('Create Account')

    def show_message(self, text, msg_type='error'):
        self.message_label.setText(text)
        if msg_type == 'error':
            self.message_label.setStyleSheet("""
                QLabel {
                    color: #c53030;
                    background-color: #fed7d7;
                    padding: 10px;
                    border-radius: 8px;
                }
            """)
        else:
            self.message_label.setStyleSheet("""
                QLabel {
                    color: #22543d;
                    background-color: #c6f6d5;
                    padding: 10px;
                    border-radius: 8px;
                }
            """)
        self.message_label.show()


class MainWindow(QMainWindow):
    """Enhanced professional main window with beautiful charts"""

    def __init__(self, api_client, user):
        super().__init__()
        self.api_client = api_client
        self.user = user
        self.current_dataset = None
        self.datasets = []
        self.init_ui()
        self.load_data()

    def init_ui(self):
        self.setWindowTitle(f'Chemical Equipment Visualizer - {self.user["username"]}')
        self.setGeometry(50, 50, 1280, 720)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f7fafc;
            }
        """)

        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main Layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Header
        header = self.create_header()
        main_layout.addWidget(header)

        # Content area
        content = QWidget()
        content.setStyleSheet("background-color: #f7fafc;")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(15, 15, 15, 15)

        # Statistics Cards
        self.stats_container = QWidget()
        self.stats_layout = QHBoxLayout(self.stats_container)
        self.stats_layout.setSpacing(15)

        self.datasets_card = StatCard('Total Datasets', '0')
        self.equipment_card = StatCard('Total Equipment', '0')

        self.stats_layout.addWidget(self.datasets_card)
        self.stats_layout.addWidget(self.equipment_card)
        self.stats_layout.addStretch()

        content_layout.addWidget(self.stats_container)

        # Tabs
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background-color: white;
                border-radius: 12px;
            }
            QTabBar::tab {
                padding: 12px 25px;
                font-size: 13px;
                font-weight: 500;
                background-color: white;
                border: none;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                margin-right: 5px;
                color: #718096;
            }
            QTabBar::tab:selected {
                background-color: white;
                color: #667eea;
                font-weight: bold;
            }
            QTabBar::tab:hover {
                background-color: #f7fafc;
            }
        """)

        # Create tabs
        self.upload_tab = self.create_upload_tab()
        self.datasets_tab = self.create_datasets_tab()
        self.viz_tab = self.create_visualization_tab()

        self.tabs.addTab(self.upload_tab, '📤 Upload Dataset')
        self.tabs.addTab(self.datasets_tab, '📊 My Datasets')
        self.tabs.addTab(self.viz_tab, '📈 Visualizations')

        content_layout.addWidget(self.tabs)

        main_layout.addWidget(content)
        central_widget.setLayout(main_layout)

    def create_header(self):
        """Create professional header"""
        header = GradientWidget()
        header.setFixedHeight(65)

        layout = QHBoxLayout(header)
        layout.setContentsMargins(25, 0, 25, 0)

        # Title
        title = QLabel('Chemical Equipment Visualizer')
        title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 20px;
                font-weight: bold;
            }
        """)
        layout.addWidget(title)

        layout.addStretch()

        # User info
        user_label = QLabel(f"👤 Welcome, {self.user['username']}!")
        user_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 13px;
                margin-right: 15px;
            }
        """)
        layout.addWidget(user_label)

        # Logout button
        logout_btn = QPushButton('Logout')
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.2);
                color: white;
                border: 2px solid white;
                border-radius: 6px;
                padding: 6px 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.3);
            }
        """)
        logout_btn.clicked.connect(self.handle_logout)
        layout.addWidget(logout_btn)

        return header

    def create_upload_tab(self):
        """Create enhanced upload tab"""
        widget = QWidget()
        widget.setStyleSheet("background-color: white;")
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        # Title
        title = QLabel('Upload New Dataset')
        title.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: #2d3748;
                margin-bottom: 8px;
            }
        """)
        layout.addWidget(title)

        # Instructions
        instructions = QLabel('Upload a CSV file with columns: Equipment Name, Type, Flowrate, Pressure, Temperature')
        instructions.setStyleSheet("""
            QLabel {
                font-size: 13px;
                color: #718096;
                padding: 12px;
                background-color: #e6fffa;
                border-radius: 8px;
                border-left: 4px solid #48bb78;
            }
        """)
        instructions.setWordWrap(True)
        layout.addWidget(instructions)

        # Upload area
        upload_container = QFrame()
        upload_container.setStyleSheet("""
            QFrame {
                border: 3px dashed #cbd5e0;
                border-radius: 12px;
                background-color: #f7fafc;
                padding: 40px;
            }
            QFrame:hover {
                border-color: #667eea;
                background-color: #edf2f7;
            }
        """)
        upload_layout = QVBoxLayout(upload_container)

        upload_icon = QLabel('📁')
        upload_icon.setAlignment(Qt.AlignCenter)
        upload_icon.setStyleSheet("font-size: 56px; margin-bottom: 15px;")
        upload_layout.addWidget(upload_icon)

        self.upload_btn = StyledButton('Choose CSV File', 'success')
        self.upload_btn.setMinimumHeight(42)
        self.upload_btn.setMinimumWidth(150)
        self.upload_btn.clicked.connect(self.upload_file)
        upload_layout.addWidget(self.upload_btn, 0, Qt.AlignCenter)

        layout.addWidget(upload_container)

        # Message area
        self.upload_message = QTextEdit()
        self.upload_message.setReadOnly(True)
        self.upload_message.setMaximumHeight(100)
        self.upload_message.setStyleSheet("""
            QTextEdit {
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 12px;
                font-size: 12px;
                background-color: white;
            }
        """)
        layout.addWidget(self.upload_message)

        layout.addStretch()
        return widget

    def create_datasets_tab(self):
        """Create enhanced datasets tab"""
        widget = QWidget()
        widget.setStyleSheet("background-color: white;")
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(30, 30, 30, 30)

        # Header
        header_layout = QHBoxLayout()

        title = QLabel('My Datasets')
        title.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: #2d3748;
            }
        """)
        header_layout.addWidget(title)

        header_layout.addStretch()

        refresh_btn = StyledButton('🔄 Refresh', 'info')
        refresh_btn.clicked.connect(self.load_datasets)
        header_layout.addWidget(refresh_btn)

        layout.addLayout(header_layout)

        # Table
        self.datasets_table = QTableWidget()
        self.datasets_table.setColumnCount(7)
        self.datasets_table.setHorizontalHeaderLabels([
            'Filename', 'Upload Date', 'Equipment',
            'Avg Flowrate', 'Avg Pressure', 'Avg Temp', 'Actions'
        ])

        header = self.datasets_table.horizontalHeader()

        # Stretch only data columns
        for col in range(6):
            header.setSectionResizeMode(col, QHeaderView.Stretch)

        # Actions column must be fixed width
        header.setSectionResizeMode(6, QHeaderView.Fixed)
        self.datasets_table.setColumnWidth(6, 220)

        self.datasets_table.verticalHeader().setVisible(False)
        self.datasets_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.datasets_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.datasets_table.setAlternatingRowColors(True)
        layout.addWidget(self.datasets_table)

        return widget

    def create_visualization_tab(self):
        """Create enhanced visualization tab with beautiful charts"""
        widget = QWidget()
        widget.setStyleSheet("background-color: white;")
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(30, 30, 30, 30)

        # Title
        title = QLabel('Data Visualizations')
        title.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: #2d3748;
                margin-bottom: 15px;
            }
        """)
        layout.addWidget(title)

        # Info label
        self.viz_info = QLabel('Select a dataset from "My Datasets" tab to view visualizations')
        self.viz_info.setStyleSheet("""
            QLabel {
                font-size: 13px;
                color: #718096;
                padding: 12px;
                background-color: #fef5e7;
                border-radius: 8px;
                border-left: 4px solid #ed8936;
            }
        """)
        self.viz_info.setWordWrap(True)
        layout.addWidget(self.viz_info)

        # Charts container with scroll
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: white;
            }
        """)

        self.charts_widget = QWidget()
        self.charts_widget.setStyleSheet("background-color: white;")
        self.charts_layout = QVBoxLayout(self.charts_widget)
        self.charts_layout.setSpacing(20)

        scroll.setWidget(self.charts_widget)
        layout.addWidget(scroll)
        self.charts_widget.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Preferred
        )

        return widget

    def load_data(self):
        """Load initial data"""
        self.load_datasets()
        self.load_statistics()

    def load_statistics(self):
        """Load and display statistics"""
        try:
            stats = self.api_client.get_statistics()
            self.datasets_card.update_value(stats['total_datasets'])
            self.equipment_card.update_value(stats['total_equipment'])
        except Exception as e:
            print(f"Error loading statistics: {e}")

    def upload_file(self):
        """Handle file upload"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 'Select CSV File', '', 'CSV Files (*.csv)'
        )

        if file_path:
            try:
                self.upload_btn.setEnabled(False)
                self.upload_btn.setText('Uploading...')
                self.upload_message.setText('📤 Uploading file...')

                result = self.api_client.upload_csv(file_path)

                success_msg = f"""
                <div style='color: #22543d; background-color: #c6f6d5; padding: 12px; border-radius: 8px;'>
                    <strong>✅ Success!</strong><br>
                    {result.get('message', 'File uploaded successfully')}<br>
                    <strong>Dataset:</strong> {result.get('dataset', {}).get('filename', '')}<br>
                    <strong>Equipment Count:</strong> {result.get('dataset', {}).get('total_equipment', 0)}
                </div>
                """
                self.upload_message.setHtml(success_msg)

                self.load_datasets()
                self.load_statistics()

            except Exception as e:
                error_msg = f"""
                <div style='color: #c53030; background-color: #fed7d7; padding: 12px; border-radius: 8px;'>
                    <strong>❌ Error:</strong><br>
                    {str(e)}
                </div>
                """
                self.upload_message.setHtml(error_msg)
            finally:
                self.upload_btn.setEnabled(True)
                self.upload_btn.setText('Choose CSV File')

    def load_datasets(self):
        try:
            self.datasets = self.api_client.list_datasets()
            self.datasets_table.setRowCount(len(self.datasets))

            for row, dataset in enumerate(self.datasets):
                self.datasets_table.setRowHeight(row, 42)

                self.datasets_table.setItem(row, 0, QTableWidgetItem(dataset['filename']))
                self.datasets_table.setItem(row, 1, QTableWidgetItem(dataset['upload_date'].split('T')[0]))
                self.datasets_table.setItem(row, 2, QTableWidgetItem(str(dataset['total_equipment'])))
                self.datasets_table.setItem(row, 3, QTableWidgetItem(f"{dataset['avg_flowrate']:.1f}"))
                self.datasets_table.setItem(row, 4, QTableWidgetItem(f"{dataset['avg_pressure']:.1f}"))
                self.datasets_table.setItem(row, 5, QTableWidgetItem(f"{dataset['avg_temperature']:.1f}"))

                # ACTION BUTTONS
                action_widget = QWidget()
                layout = QHBoxLayout(action_widget)
                layout.setContentsMargins(2, 2, 2, 2)
                layout.setSpacing(4)

                view_btn = StyledButton("View", "primary")
                view_btn.clicked.connect(lambda _, d=dataset['id']: self.view_dataset(d))

                pdf_btn = StyledButton("PDF", "success")
                pdf_btn.clicked.connect(lambda _, d=dataset['id']: self.generate_report(d))

                del_btn = StyledButton("Delete", "danger")
                del_btn.clicked.connect(lambda _, d=dataset['id']: self.delete_dataset(d))

                layout.addWidget(view_btn)
                layout.addWidget(pdf_btn)
                layout.addWidget(del_btn)

                self.datasets_table.setCellWidget(row, 6, action_widget)

        except Exception as e:
            QMessageBox.warning(
                self,
                'Error',
                f'Failed to load datasets:\n{str(e)}'
            )

    def view_dataset(self, dataset_id):
        self.tabs.setCurrentWidget(self.viz_tab)

        # Clear previous charts
        while self.charts_layout.count():
            item = self.charts_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        try:
            data = self.api_client.get_dataset(dataset_id)
            self.current_dataset = data
            self.show_visualizations(data)

        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def show_visualizations(self, data):
        """Display beautiful professional charts"""

        # Clear previous charts
        for i in reversed(range(self.charts_layout.count())):
            widget = self.charts_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        dataset_info = data['dataset']

        # Update info label
        self.viz_info.setText(
            f"📊 Dataset: {dataset_info['filename']} | "
            f"Equipment: {dataset_info['total_equipment']} | "
            f"Upload Date: {dataset_info['upload_date'].split('T')[0]}"
        )
        self.viz_info.setStyleSheet("""
            QLabel {
                font-size: 13px;
                color: #22543d;
                padding: 12px;
                background-color: #c6f6d5;
                border-radius: 8px;
                border-left: 4px solid #48bb78;
            }
        """)

        # Create charts grid
        charts_grid = QWidget()
        charts_grid.setMinimumHeight(550)
        grid_layout = QGridLayout(charts_grid)
        grid_layout.setSpacing(15)

        # Chart 1: Equipment Type Distribution (Pie Chart)
        if 'type_distribution' in data and data['type_distribution']:
            pie_frame = self.create_chart_frame()
            pie_layout = QVBoxLayout(pie_frame)

            pie_canvas = ProfessionalMatplotlibCanvas(pie_frame, width=5, height=3.5)
            pie_canvas.create_pie_chart(
                data['type_distribution'],
                'Equipment Type Distribution'
            )
            pie_layout.addWidget(pie_canvas)

            grid_layout.addWidget(pie_frame, 0, 0)

        # Chart 2: Average Parameters (Bar Chart)
        avg_frame = self.create_chart_frame()
        avg_layout = QVBoxLayout(avg_frame)

        avg_canvas = ProfessionalMatplotlibCanvas(avg_frame, width=5, height=3.5)
        avg_canvas.create_bar_chart(
            ['Flowrate', 'Pressure', 'Temperature'],
            [dataset_info['avg_flowrate'], dataset_info['avg_pressure'], dataset_info['avg_temperature']],
            'Average Parameters Comparison',
            'Average Value',
            [COLORS['chart_colors'][0], COLORS['chart_colors'][1], COLORS['chart_colors'][2]]
        )
        avg_layout.addWidget(avg_canvas)

        grid_layout.addWidget(avg_frame, 0, 1)

        self.charts_layout.addWidget(charts_grid)

        # Chart 3: Equipment Parameters Comparison (Grouped Bar Chart)
        equipment_list = dataset_info['equipment'][:10]
        if equipment_list:
            grouped_frame = self.create_chart_frame()
            grouped_frame.setMinimumHeight(320)
            grouped_layout = QVBoxLayout(grouped_frame)

            grouped_canvas = ProfessionalMatplotlibCanvas(grouped_frame, width=10, height=3.5)
            grouped_canvas.create_grouped_bar_chart(
                equipment_list,
                'Parameter Comparison (First 10 Equipment)'
            )
            grouped_layout.addWidget(grouped_canvas)

            self.charts_layout.addWidget(grouped_frame)

        # Equipment Data Table
        table_frame = self.create_chart_frame()
        table_layout = QVBoxLayout(table_frame)

        table_title = QLabel('📋 Equipment Details')
        table_title.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #2d3748;
                margin-bottom: 12px;
            }
        """)
        table_layout.addWidget(table_title)

        equipment_table = QTableWidget()
        equipment_table.setColumnCount(5)
        equipment_table.setHorizontalHeaderLabels([
            'Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature'
        ])
        equipment_table.setRowCount(len(dataset_info['equipment']))

        equipment_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #e2e8f0;
                gridline-color: #e2e8f0;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QHeaderView::section {
                background-color: #667eea;
                color: white;
                padding: 8px;
                font-weight: bold;
                border: none;
            }
        """)

        for i, eq in enumerate(dataset_info['equipment']):
            equipment_table.setItem(i, 0, QTableWidgetItem(eq['equipment_name']))
            equipment_table.setItem(i, 1, QTableWidgetItem(eq['equipment_type']))
            equipment_table.setItem(i, 2, QTableWidgetItem(f"{eq['flowrate']:.1f}"))
            equipment_table.setItem(i, 3, QTableWidgetItem(f"{eq['pressure']:.1f}"))
            equipment_table.setItem(i, 4, QTableWidgetItem(f"{eq['temperature']:.1f}"))

        equipment_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        equipment_table.setAlternatingRowColors(True)
        equipment_table.setEditTriggers(QTableWidget.NoEditTriggers)

        table_layout.addWidget(equipment_table)
        self.charts_layout.addWidget(table_frame)

        self.charts_widget.adjustSize()
        self.charts_widget.repaint()
        self.charts_widget.update()
        QTimer.singleShot(0, self.charts_widget.adjustSize)

    def create_chart_frame(self):
        """Create styled frame for charts"""
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #e2e8f0;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        frame.setFrameStyle(QFrame.StyledPanel)
        return frame

    def generate_report(self, dataset_id):
        """Generate PDF report"""
        save_path, _ = QFileDialog.getSaveFileName(
            self, 'Save Report', f'equipment_report_{dataset_id}.pdf', 'PDF Files (*.pdf)'
        )

        if save_path:
            try:
                self.api_client.generate_report(dataset_id, save_path)
                QMessageBox.information(
                    self,
                    'Success',
                    f'✅ Report generated successfully!\n\nSaved to: {save_path}'
                )
            except Exception as e:
                QMessageBox.warning(self, 'Error', f'Failed to generate report: {str(e)}')

    def delete_dataset(self, dataset_id):
        """Delete dataset"""
        reply = QMessageBox.question(
            self,
            'Confirm Delete',
            'Are you sure you want to delete this dataset?\n\nThis action cannot be undone.',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            try:
                self.api_client.delete_dataset(dataset_id)
                QMessageBox.information(self, 'Success', '✅ Dataset deleted successfully!')
                self.load_datasets()
                self.load_statistics()

                # Clear visualizations if viewing deleted dataset
                if self.current_dataset and self.current_dataset['dataset']['id'] == dataset_id:
                    for i in reversed(range(self.charts_layout.count())):
                        widget = self.charts_layout.itemAt(i).widget()
                        if widget:
                            widget.setParent(None)
                    self.current_dataset = None

            except Exception as e:
                QMessageBox.warning(self, 'Error', f'Failed to delete dataset: {str(e)}')

    def handle_logout(self):
        """Handle logout"""
        reply = QMessageBox.question(
            self,
            'Confirm Logout',
            'Are you sure you want to logout?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.close()
            login_window = LoginWindow(self.api_client)
            login_window.login_success.connect(lambda token, user: MainWindow(self.api_client, user).show())
            login_window.show()


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)

    # Set application style
    app.setStyle('Fusion')

    # Set application font
    font = QFont("Segoe UI", 9)
    app.setFont(font)

    # Create API client
    api_client = APIClient()

    # Show login window
    login_window = LoginWindow(api_client)

    def on_login_success(token, user):
        main_window = MainWindow(api_client, user)
        main_window.show()

    login_window.login_success.connect(on_login_success)
    login_window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()