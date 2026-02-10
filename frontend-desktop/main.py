
"""
Chemical Equipment Visualizer - Enhanced Professional Desktop Application
PyQt5 + Matplotlib Frontend with Beautiful Charts - FIXED
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
    QScrollArea, QTextEdit, QFrame, QSizePolicy, QGridLayout, QHeaderView,
    QSpacerItem
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer, pyqtSignal, QSize
from PyQt5.QtGui import QFont, QPalette, QColor, QLinearGradient, QPainter, QBrush, QPen, QIcon


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

INPUT_STYLE = """
    QLineEdit {
        padding: 10px 14px;
        border: 2px solid #e2e8f0;
        border-radius: 8px;
        font-size: 13px;
        background-color: white;
        color: #2d3748;
    }
    QLineEdit:focus {
        border: 2px solid #667eea;
    }
"""

LABEL_STYLE = "color: #4a5568; font-weight: 600; font-size: 12px;"

TABLE_STYLE = """
    QTableWidget {
        background-color: white;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        gridline-color: #edf2f7;
        font-size: 12px;
        selection-background-color: #ebf4ff;
        selection-color: #2d3748;
    }
    QTableWidget::item {
        padding: 8px 12px;
        border-bottom: 1px solid #edf2f7;
    }
    QTableWidget::item:alternate {
        background-color: #f7fafc;
    }
    QHeaderView::section {
        background-color: #667eea;
        color: white;
        padding: 10px 12px;
        font-weight: bold;
        font-size: 12px;
        border: none;
        border-right: 1px solid #5a72d4;
    }
    QHeaderView::section:last {
        border-right: none;
    }
"""

# ─── Global window references to prevent garbage collection ───────────────────
_active_windows = []

def _keep_window(win):
    """Store a reference so the window is not garbage-collected."""
    _active_windows.append(win)

def _release_window(win):
    """Remove the reference when the window is intentionally closed."""
    try:
        _active_windows.remove(win)
    except ValueError:
        pass


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
        url = f"{self.base_url}/auth/login/"
        data = {'username': username, 'password': password}
        response = requests.post(url, json=data)
        return response.status_code, response.json()

    def register(self, user_data):
        url = f"{self.base_url}/auth/register/"
        response = requests.post(url, json=user_data)
        return response.status_code, response.json()

    def upload_csv(self, file_path):
        url = f"{self.base_url}/upload/"
        headers = {'Authorization': f'Token {self.token}'}
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(url, headers=headers, files=files)
        return response.status_code, response.json()

    def list_datasets(self):
        url = f"{self.base_url}/datasets/"
        response = requests.get(url, headers=self.get_headers())
        return response.json()

    def get_dataset(self, dataset_id):
        url = f"{self.base_url}/datasets/{dataset_id}/"
        response = requests.get(url, headers=self.get_headers())
        return response.json()

    def delete_dataset(self, dataset_id):
        url = f"{self.base_url}/datasets/{dataset_id}/delete/"
        response = requests.delete(url, headers=self.get_headers())
        return response.json()

    def generate_report(self, dataset_id, save_path):
        url = f"{self.base_url}/datasets/{dataset_id}/report/"
        response = requests.get(url, headers=self.get_headers())
        with open(save_path, 'wb') as f:
            f.write(response.content)
        return True

    def get_statistics(self):
        url = f"{self.base_url}/statistics/"
        response = requests.get(url, headers=self.get_headers())
        return response.json()


class ProfessionalMatplotlibCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=3, dpi=100):
        plt.style.use('seaborn-v0_8-darkgrid')
        fig = Figure(figsize=(width, height), dpi=dpi, facecolor='white')
        super().__init__(fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def create_pie_chart(self, data_dict, title):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        labels = list(data_dict.keys())
        sizes = list(data_dict.values())
        colors = COLORS['chart_colors'][:len(labels)]
        wedges, texts, autotexts = ax.pie(
            sizes, labels=labels, colors=colors, autopct='%1.1f%%',
            startangle=90, pctdistance=0.85, explode=[0.05] * len(labels),
            shadow=True, textprops={'fontsize': 9, 'weight': 'bold'})
        for text in texts:
            text.set_fontsize(10); text.set_weight('bold')
        for autotext in autotexts:
            autotext.set_color('white'); autotext.set_fontsize(9); autotext.set_weight('bold')
        ax.set_title(title, fontsize=12, weight='bold', pad=15)
        ax.axis('equal')
        self.figure.tight_layout(); self.draw()

    def create_bar_chart(self, labels, values, title, ylabel='Value', colors=None):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        if colors is None:
            colors = COLORS['chart_colors'][:len(labels)]
        x_pos = np.arange(len(labels))
        bars = ax.bar(x_pos, values, color=colors, alpha=0.8, edgecolor='white', linewidth=2)
        for bar, value in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width()/2., bar.get_height(),
                    f'{value:.1f}', ha='center', va='bottom', fontsize=9, weight='bold')
        ax.set_xlabel('Parameters', fontsize=10, weight='bold')
        ax.set_ylabel(ylabel, fontsize=10, weight='bold')
        ax.set_title(title, fontsize=12, weight='bold', pad=15)
        ax.set_xticks(x_pos); ax.set_xticklabels(labels, fontsize=9)
        ax.grid(True, alpha=0.3, linestyle='--'); ax.set_axisbelow(True)
        self.figure.tight_layout(); self.draw()

    def create_grouped_bar_chart(self, equipment_list, title):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        names = [eq['equipment_name'][:12] + '...' if len(eq['equipment_name']) > 12
                 else eq['equipment_name'] for eq in equipment_list]
        flowrates = [eq['flowrate'] for eq in equipment_list]
        pressures = [eq['pressure'] for eq in equipment_list]
        temperatures = [eq['temperature'] for eq in equipment_list]
        x = np.arange(len(names)); width = 0.25
        ax.bar(x - width, flowrates, width, label='Flowrate',
               color=COLORS['chart_colors'][0], alpha=0.8, edgecolor='white', linewidth=1.5)
        ax.bar(x, pressures, width, label='Pressure',
               color=COLORS['chart_colors'][1], alpha=0.8, edgecolor='white', linewidth=1.5)
        ax.bar(x + width, temperatures, width, label='Temperature',
               color=COLORS['chart_colors'][2], alpha=0.8, edgecolor='white', linewidth=1.5)
        ax.set_xlabel('Equipment', fontsize=10, weight='bold')
        ax.set_ylabel('Values', fontsize=10, weight='bold')
        ax.set_title(title, fontsize=12, weight='bold', pad=15)
        ax.set_xticks(x); ax.set_xticklabels(names, rotation=45, ha='right', fontsize=8)
        ax.legend(loc='upper right', fontsize=9, framealpha=0.9, shadow=True)
        ax.grid(True, alpha=0.3, linestyle='--', axis='y'); ax.set_axisbelow(True)
        self.figure.tight_layout(); self.draw()

    def create_line_chart(self, x_data, y_data, title, xlabel, ylabel, label=None):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(x_data, y_data, color=COLORS['primary'], linewidth=2.5,
                marker='o', markersize=8, markerfacecolor=COLORS['secondary'],
                markeredgecolor='white', markeredgewidth=2, label=label)
        ax.set_xlabel(xlabel, fontsize=10, weight='bold')
        ax.set_ylabel(ylabel, fontsize=10, weight='bold')
        ax.set_title(title, fontsize=12, weight='bold', pad=15)
        if label: ax.legend(fontsize=9, framealpha=0.9, shadow=True)
        ax.grid(True, alpha=0.3, linestyle='--'); ax.set_axisbelow(True)
        self.figure.tight_layout(); self.draw()


class GradientWidget(QWidget):
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
    def __init__(self, text, color='primary', parent=None):
        super().__init__(text, parent)
        self.color = color
        self.apply_style()
    def apply_style(self):
        m = {'primary': (COLORS['primary'], '#5568d3'), 'success': (COLORS['success'], '#38a169'),
             'danger': (COLORS['danger'], '#e53e3e'), 'info': (COLORS['info'], '#3182ce')}
        bg, hv = m.get(self.color, (COLORS['info'], '#3182ce'))
        self.setStyleSheet(f"""
            QPushButton {{ background-color:{bg}; color:white; border:none; border-radius:6px;
                padding:6px 14px; font-size:11px; font-weight:bold; min-width:70px; }}
            QPushButton:hover {{ background-color:{hv}; }}
            QPushButton:pressed {{ background-color:{bg}; padding-top:7px; padding-bottom:5px; }}
            QPushButton:disabled {{ background-color:#cbd5e0; color:#a0aec0; }}
        """)


class StatCard(QFrame):
    def __init__(self, title, value, icon="", parent=None):
        super().__init__(parent)
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        self.setFixedHeight(100); self.setMinimumWidth(180)
        self.setStyleSheet("""
            QFrame { background-color:white; border-radius:12px; border:1px solid #e2e8f0; }
            QFrame:hover { border:1px solid #cbd5e0; background-color:#fafbfc; }
        """)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 14, 18, 14); layout.setSpacing(4)
        tl = QLabel(f"{icon}  {title}" if icon else title)
        tl.setStyleSheet("color:#718096; font-size:11px; font-weight:600; letter-spacing:0.5px; background:transparent; border:none;")
        layout.addWidget(tl)
        self.value_label = QLabel(str(value))
        self.value_label.setStyleSheet("color:#2d3748; font-size:28px; font-weight:bold; background:transparent; border:none;")
        layout.addWidget(self.value_label)
        layout.addStretch()
    def update_value(self, value):
        self.value_label.setText(str(value))


def _make_field(parent_layout, label_text, placeholder, is_password=False):
    lbl = QLabel(label_text)
    lbl.setStyleSheet(LABEL_STYLE)
    parent_layout.addWidget(lbl)
    field = QLineEdit()
    field.setPlaceholderText(placeholder)
    field.setStyleSheet(INPUT_STYLE)
    field.setMinimumHeight(40)
    if is_password:
        field.setEchoMode(QLineEdit.Password)
    parent_layout.addWidget(field)
    parent_layout.addSpacing(4)
    return field


def _parse_api_errors(result):
    messages = []
    if isinstance(result, dict):
        for field, errors in result.items():
            if field in ('token', 'user', 'message'):
                continue
            if isinstance(errors, list):
                for e in errors:
                    messages.append(f"{field}: {e}")
            elif isinstance(errors, str):
                messages.append(errors)
    return '\n'.join(messages) if messages else 'An unknown error occurred. Please try again.'


# ─── Application Controller ──────────────────────────────────────────────────
# Single object that owns all windows and manages transitions safely.

class AppController:
    """Manages window lifecycle to prevent garbage-collection crashes."""

    def __init__(self, api_client):
        self.api_client = api_client
        self.login_window = None
        self.register_window = None
        self.main_window = None

    def show_login(self):
        """Show the login window, cleaning up any previous windows."""
        # Close previous windows safely
        if self.main_window:
            self.main_window.close()
            self.main_window = None
        if self.register_window:
            self.register_window.close()
            self.register_window = None

        self.api_client.token = None
        self.login_window = LoginWindow(self.api_client, self)
        _keep_window(self.login_window)
        self.login_window.show()

    def show_register(self):
        """Show the register window."""
        self.register_window = RegisterWindow(self.api_client, self)
        _keep_window(self.register_window)
        self.register_window.show()

    def on_login_success(self, token, user):
        """Called when login or registration succeeds."""
        self.api_client.set_token(token)

        # Close auth windows
        if self.register_window:
            self.register_window.close()
            _release_window(self.register_window)
            self.register_window = None
        if self.login_window:
            self.login_window.close()
            _release_window(self.login_window)
            self.login_window = None

        # Open main window
        self.main_window = MainWindow(self.api_client, user, self)
        _keep_window(self.main_window)
        self.main_window.show()

    def on_logout(self):
        """Called when user logs out."""
        if self.main_window:
            self.main_window.close()
            _release_window(self.main_window)
            self.main_window = None
        self.show_login()


class LoginWindow(QWidget):
    def __init__(self, api_client, controller):
        super().__init__()
        self.api_client = api_client
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Chemical Equipment Visualizer - Login')
        self.setFixedSize(480, 520)
        self.setObjectName("LoginBg")
        self.setStyleSheet("""
            QWidget#LoginBg {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
            }
        """)

        outer = QVBoxLayout(self)
        outer.setAlignment(Qt.AlignCenter)

        card = QFrame(); card.setObjectName("LoginCard"); card.setFixedWidth(380)
        card.setStyleSheet("QFrame#LoginCard { background-color:white; border-radius:16px; }")
        cl = QVBoxLayout(card)
        cl.setContentsMargins(36, 32, 36, 28); cl.setSpacing(0)

        title = QLabel('Chemical Equipment\nVisualizer')
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color:#2d3748; font-size:22px; font-weight:bold; background:transparent; border:none;")
        cl.addWidget(title)

        sub = QLabel('Sign in to your account')
        sub.setAlignment(Qt.AlignCenter)
        sub.setStyleSheet("color:#718096; font-size:13px; margin-bottom:6px; background:transparent; border:none;")
        cl.addWidget(sub); cl.addSpacing(18)

        self.username_input = _make_field(cl, 'Username', 'Enter your username')
        self.password_input = _make_field(cl, 'Password', 'Enter your password', is_password=True)
        cl.addSpacing(10)

        self.login_btn = QPushButton('Sign In')
        self.login_btn.setMinimumHeight(42); self.login_btn.setCursor(Qt.PointingHandCursor)
        self.login_btn.setStyleSheet(f"""
            QPushButton {{ background-color:{COLORS['primary']}; color:white; border:none;
                border-radius:8px; font-size:14px; font-weight:bold; }}
            QPushButton:hover {{ background-color:#5568d3; }}
            QPushButton:pressed {{ background-color:#4c5ec7; }}
            QPushButton:disabled {{ background-color:#cbd5e0; color:#a0aec0; }}
        """)
        self.login_btn.clicked.connect(self.handle_login)
        cl.addWidget(self.login_btn); cl.addSpacing(8)

        reg_btn = QPushButton('Create New Account')
        reg_btn.setMinimumHeight(42); reg_btn.setCursor(Qt.PointingHandCursor)
        reg_btn.setStyleSheet(f"""
            QPushButton {{ background-color:{COLORS['success']}; color:white; border:none;
                border-radius:8px; font-size:14px; font-weight:bold; }}
            QPushButton:hover {{ background-color:#38a169; }}
            QPushButton:pressed {{ background-color:#2f855a; }}
        """)
        reg_btn.clicked.connect(self.controller.show_register)
        cl.addWidget(reg_btn)

        self.message_label = QLabel('')
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setWordWrap(True); self.message_label.hide()
        cl.addSpacing(10); cl.addWidget(self.message_label)

        outer.addWidget(card)
        self.password_input.returnPressed.connect(self.handle_login)
        self.username_input.returnPressed.connect(self.password_input.setFocus)

    def handle_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()
        if not username or not password:
            self.show_message('Please enter both username and password.', 'error')
            return
        try:
            self.login_btn.setEnabled(False); self.login_btn.setText('Signing in...')
            QApplication.processEvents()
            status_code, result = self.api_client.login(username, password)
            if status_code == 200 and 'token' in result:
                self.controller.on_login_success(result['token'], result['user'])
            else:
                self.show_message(result.get('error', 'Invalid username or password.'), 'error')
        except requests.exceptions.ConnectionError:
            self.show_message('Cannot connect to server.\nCheck your internet connection.', 'error')
        except Exception as e:
            self.show_message(f'Error: {str(e)}', 'error')
        finally:
            self.login_btn.setEnabled(True); self.login_btn.setText('Sign In')

    def show_message(self, text, msg_type='error'):
        self.message_label.setText(text)
        if msg_type == 'error':
            self.message_label.setStyleSheet("QLabel { color:#c53030; background-color:#fed7d7; padding:10px 14px; border-radius:8px; font-size:12px; font-weight:500; border:none; }")
        else:
            self.message_label.setStyleSheet("QLabel { color:#22543d; background-color:#c6f6d5; padding:10px 14px; border-radius:8px; font-size:12px; font-weight:500; border:none; }")
        self.message_label.show()


class RegisterWindow(QWidget):
    def __init__(self, api_client, controller):
        super().__init__()
        self.api_client = api_client
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Create New Account')
        self.setFixedSize(480, 660)
        self.setObjectName("RegBg")
        self.setStyleSheet("""
            QWidget#RegBg {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
            }
        """)

        outer = QVBoxLayout(self)
        outer.setAlignment(Qt.AlignCenter)

        card = QFrame(); card.setObjectName("RegCard"); card.setFixedWidth(400)
        card.setStyleSheet("QFrame#RegCard { background-color:white; border-radius:16px; }")
        cl = QVBoxLayout(card)
        cl.setContentsMargins(32, 28, 32, 24); cl.setSpacing(0)

        title = QLabel('Create Account')
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color:#2d3748; font-size:22px; font-weight:bold; background:transparent; border:none;")
        cl.addWidget(title)

        sub = QLabel('Fill in the details below')
        sub.setAlignment(Qt.AlignCenter)
        sub.setStyleSheet("color:#718096; font-size:12px; margin-bottom:4px; background:transparent; border:none;")
        cl.addWidget(sub); cl.addSpacing(14)

        self.reg_username = _make_field(cl, 'Username *', 'Choose a username')
        self.reg_email = _make_field(cl, 'Email *', 'your.email@example.com')

        name_row = QHBoxLayout(); name_row.setSpacing(12)
        left_col = QVBoxLayout(); left_col.setSpacing(2)
        lf = QLabel('First Name'); lf.setStyleSheet(LABEL_STYLE); left_col.addWidget(lf)
        self.reg_first_name = QLineEdit()
        self.reg_first_name.setPlaceholderText('John')
        self.reg_first_name.setStyleSheet(INPUT_STYLE); self.reg_first_name.setMinimumHeight(40)
        left_col.addWidget(self.reg_first_name)

        right_col = QVBoxLayout(); right_col.setSpacing(2)
        ll = QLabel('Last Name'); ll.setStyleSheet(LABEL_STYLE); right_col.addWidget(ll)
        self.reg_last_name = QLineEdit()
        self.reg_last_name.setPlaceholderText('Doe')
        self.reg_last_name.setStyleSheet(INPUT_STYLE); self.reg_last_name.setMinimumHeight(40)
        right_col.addWidget(self.reg_last_name)

        name_row.addLayout(left_col); name_row.addLayout(right_col)
        cl.addLayout(name_row); cl.addSpacing(4)

        self.reg_password = _make_field(cl, 'Password *', 'At least 8 characters', is_password=True)
        self.reg_password_confirm = _make_field(cl, 'Confirm Password *', 'Re-enter password', is_password=True)
        cl.addSpacing(8)

        self.register_btn = QPushButton('Create Account')
        self.register_btn.setMinimumHeight(42); self.register_btn.setCursor(Qt.PointingHandCursor)
        self.register_btn.setStyleSheet(f"""
            QPushButton {{ background-color:{COLORS['success']}; color:white; border:none;
                border-radius:8px; font-size:14px; font-weight:bold; }}
            QPushButton:hover {{ background-color:#38a169; }}
            QPushButton:pressed {{ background-color:#2f855a; }}
            QPushButton:disabled {{ background-color:#cbd5e0; color:#a0aec0; }}
        """)
        self.register_btn.clicked.connect(self.handle_register)
        cl.addWidget(self.register_btn); cl.addSpacing(6)

        back_btn = QPushButton('Back to Sign In')
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.setStyleSheet("QPushButton { background:transparent; color:#667eea; border:none; font-size:12px; font-weight:600; } QPushButton:hover { color:#5568d3; }")
        back_btn.clicked.connect(self.close)
        cl.addWidget(back_btn, 0, Qt.AlignCenter)

        self.message_label = QLabel('')
        self.message_label.setAlignment(Qt.AlignLeft)
        self.message_label.setWordWrap(True); self.message_label.hide()
        cl.addSpacing(8); cl.addWidget(self.message_label)

        outer.addWidget(card)
        self.reg_password_confirm.returnPressed.connect(self.handle_register)

    def handle_register(self):
        username = self.reg_username.text().strip()
        email = self.reg_email.text().strip()
        password = self.reg_password.text()
        password_confirm = self.reg_password_confirm.text()

        if not username or not email or not password:
            self.show_message('Please fill in all required fields (*).', 'error')
            return
        if len(password) < 8:
            self.show_message('Password must be at least 8 characters.', 'error')
            return
        if password != password_confirm:
            self.show_message('Passwords do not match.', 'error')
            return

        user_data = {
            'username': username,
            'email': email,
            'password': password,
            'password_confirm': password_confirm,
            'first_name': self.reg_first_name.text().strip(),
            'last_name': self.reg_last_name.text().strip(),
        }

        try:
            self.register_btn.setEnabled(False); self.register_btn.setText('Creating account...')
            QApplication.processEvents()
            status_code, result = self.api_client.register(user_data)
            if status_code == 201 and 'token' in result:
                # Hand off to controller — it will close windows safely
                self.controller.on_login_success(result['token'], result['user'])
            else:
                error_text = _parse_api_errors(result)
                self.show_message(error_text, 'error')
        except requests.exceptions.ConnectionError:
            self.show_message('Cannot connect to server.\nCheck your internet connection.', 'error')
        except Exception as e:
            self.show_message(f'Error: {str(e)}', 'error')
        finally:
            self.register_btn.setEnabled(True); self.register_btn.setText('Create Account')

    def show_message(self, text, msg_type='error'):
        self.message_label.setText(text)
        if msg_type == 'error':
            self.message_label.setStyleSheet("QLabel { color:#c53030; background-color:#fed7d7; padding:10px 14px; border-radius:8px; font-size:12px; font-weight:500; border:none; }")
        else:
            self.message_label.setStyleSheet("QLabel { color:#22543d; background-color:#c6f6d5; padding:10px 14px; border-radius:8px; font-size:12px; font-weight:500; border:none; }")
        self.message_label.show()


class MainWindow(QMainWindow):
    def __init__(self, api_client, user, controller):
        super().__init__()
        self.api_client = api_client
        self.user = user
        self.controller = controller
        self.current_dataset = None
        self.datasets = []
        self.init_ui()
        self.load_data()

    def init_ui(self):
        self.setWindowTitle(f'Chemical Equipment Visualizer - {self.user["username"]}')
        self.setGeometry(50, 50, 1300, 760)
        self.setMinimumSize(1000, 600)
        self.setStyleSheet("QMainWindow { background-color: #f0f2f5; }")

        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setSpacing(0); root.setContentsMargins(0, 0, 0, 0)

        root.addWidget(self._build_header())

        body = QWidget()
        body.setStyleSheet("background-color: #f0f2f5;")
        body_layout = QVBoxLayout(body)
        body_layout.setContentsMargins(20, 18, 20, 12); body_layout.setSpacing(16)

        stats_row = QHBoxLayout(); stats_row.setSpacing(16)
        self.datasets_card = StatCard('Total Datasets', '0', '📂')
        self.equipment_card = StatCard('Total Equipment', '0', '⚙️')
        self.user_card = StatCard('Logged in as', self.user['username'], '👤')
        stats_row.addWidget(self.datasets_card)
        stats_row.addWidget(self.equipment_card)
        stats_row.addWidget(self.user_card)
        stats_row.addStretch()
        body_layout.addLayout(stats_row)

        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane { border:none; background-color:white; border-radius:12px; }
            QTabBar::tab { padding:12px 28px; font-size:13px; font-weight:500;
                background-color:#e8ecf1; border:none; border-top-left-radius:8px;
                border-top-right-radius:8px; margin-right:3px; color:#718096; }
            QTabBar::tab:selected { background-color:white; color:#667eea; font-weight:bold; }
            QTabBar::tab:hover:!selected { background-color:#f0f4f8; }
        """)

        self.upload_tab = self._build_upload_tab()
        self.datasets_tab = self._build_datasets_tab()
        self.viz_tab = self._build_visualization_tab()
        self.tabs.addTab(self.upload_tab, '📤  Upload Dataset')
        self.tabs.addTab(self.datasets_tab, '📊  My Datasets')
        self.tabs.addTab(self.viz_tab, '📈  Visualizations')
        body_layout.addWidget(self.tabs)
        root.addWidget(body)

    def _build_header(self):
        header = GradientWidget(); header.setFixedHeight(60)
        layout = QHBoxLayout(header); layout.setContentsMargins(24, 0, 24, 0)
        title = QLabel('⚗️  Chemical Equipment Visualizer')
        title.setStyleSheet("color:white; font-size:18px; font-weight:bold; background:transparent;")
        layout.addWidget(title); layout.addStretch()
        ul = QLabel(f'Welcome, {self.user["username"]}')
        ul.setStyleSheet("color:rgba(255,255,255,0.9); font-size:13px; margin-right:12px; background:transparent;")
        layout.addWidget(ul)
        lb = QPushButton('Logout'); lb.setCursor(Qt.PointingHandCursor)
        lb.setStyleSheet("""
            QPushButton { background-color:rgba(255,255,255,0.15); color:white;
                border:1.5px solid rgba(255,255,255,0.6); border-radius:6px;
                padding:6px 20px; font-weight:bold; font-size:12px; }
            QPushButton:hover { background-color:rgba(255,255,255,0.25); }
        """)
        lb.clicked.connect(self.handle_logout)
        layout.addWidget(lb)
        return header

    def _build_upload_tab(self):
        widget = QWidget(); widget.setStyleSheet("background-color:white;")
        layout = QVBoxLayout(widget); layout.setContentsMargins(32, 28, 32, 28); layout.setSpacing(16)
        t = QLabel('Upload New Dataset')
        t.setStyleSheet("font-size:20px; font-weight:bold; color:#2d3748;")
        layout.addWidget(t)
        ins = QLabel('📋  Upload a CSV file with columns: Equipment Name, Type, Flowrate, Pressure, Temperature')
        ins.setWordWrap(True)
        ins.setStyleSheet("font-size:13px; color:#2d6a4f; padding:12px 16px; background-color:#e6fffa; border-radius:8px; border-left:4px solid #48bb78;")
        layout.addWidget(ins)

        zone = QFrame()
        zone.setStyleSheet("""
            QFrame { border:2.5px dashed #cbd5e0; border-radius:12px; background-color:#f7fafc; }
            QFrame:hover { border-color:#667eea; background-color:#eef2ff; }
        """)
        zl = QVBoxLayout(zone); zl.setContentsMargins(40, 36, 40, 36); zl.setAlignment(Qt.AlignCenter)
        ic = QLabel('📁'); ic.setAlignment(Qt.AlignCenter)
        ic.setStyleSheet("font-size:48px; background:transparent; border:none;")
        zl.addWidget(ic)
        ht = QLabel('Click the button below to select a CSV file')
        ht.setAlignment(Qt.AlignCenter)
        ht.setStyleSheet("color:#a0aec0; font-size:13px; margin-bottom:10px; background:transparent; border:none;")
        zl.addWidget(ht)
        self.upload_btn = StyledButton('Choose CSV File', 'success')
        self.upload_btn.setMinimumHeight(42); self.upload_btn.setMinimumWidth(180)
        self.upload_btn.setCursor(Qt.PointingHandCursor)
        self.upload_btn.clicked.connect(self.upload_file)
        zl.addWidget(self.upload_btn, 0, Qt.AlignCenter)
        layout.addWidget(zone)

        self.upload_message = QTextEdit(); self.upload_message.setReadOnly(True)
        self.upload_message.setMaximumHeight(90)
        self.upload_message.setStyleSheet("QTextEdit { border:1px solid #e2e8f0; border-radius:8px; padding:10px; font-size:12px; background-color:#fafbfc; }")
        layout.addWidget(self.upload_message)
        layout.addStretch()
        return widget

    def _build_datasets_tab(self):
        widget = QWidget(); widget.setStyleSheet("background-color:white;")
        layout = QVBoxLayout(widget); layout.setContentsMargins(28, 24, 28, 24); layout.setSpacing(14)
        header = QHBoxLayout()
        t = QLabel('My Datasets'); t.setStyleSheet("font-size:20px; font-weight:bold; color:#2d3748;")
        header.addWidget(t); header.addStretch()
        rb = StyledButton('🔄  Refresh', 'info'); rb.setCursor(Qt.PointingHandCursor)
        rb.clicked.connect(self.load_datasets); header.addWidget(rb)
        layout.addLayout(header)

        self.datasets_table = QTableWidget()
        self.datasets_table.setColumnCount(7)
        self.datasets_table.setHorizontalHeaderLabels([
            'Filename', 'Upload Date', 'Equipment', 'Avg Flowrate', 'Avg Pressure', 'Avg Temp', 'Actions'])
        self.datasets_table.setStyleSheet(TABLE_STYLE)
        self.datasets_table.verticalHeader().setVisible(False)
        self.datasets_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.datasets_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.datasets_table.setAlternatingRowColors(True)
        self.datasets_table.setShowGrid(False)
        hdr = self.datasets_table.horizontalHeader()
        for col in range(6):
            hdr.setSectionResizeMode(col, QHeaderView.Stretch)
        hdr.setSectionResizeMode(6, QHeaderView.Fixed)
        self.datasets_table.setColumnWidth(6, 230)
        layout.addWidget(self.datasets_table)
        return widget

    def _build_visualization_tab(self):
        widget = QWidget(); widget.setStyleSheet("background-color:white;")
        layout = QVBoxLayout(widget); layout.setContentsMargins(28, 24, 28, 24); layout.setSpacing(14)
        t = QLabel('Data Visualizations')
        t.setStyleSheet("font-size:20px; font-weight:bold; color:#2d3748;")
        layout.addWidget(t)
        self.viz_info = QLabel('Select a dataset from "My Datasets" tab to view visualizations')
        self.viz_info.setWordWrap(True)
        self.viz_info.setStyleSheet("font-size:13px; color:#7b6c00; padding:12px 16px; background-color:#fef5e7; border-radius:8px; border-left:4px solid #ed8936;")
        layout.addWidget(self.viz_info)

        scroll = QScrollArea(); scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("QScrollArea { border:none; background-color:white; }")
        self.charts_widget = QWidget(); self.charts_widget.setStyleSheet("background-color:white;")
        self.charts_layout = QVBoxLayout(self.charts_widget); self.charts_layout.setSpacing(20)
        self.charts_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        scroll.setWidget(self.charts_widget)
        layout.addWidget(scroll)
        return widget

    def load_data(self):
        self.load_datasets(); self.load_statistics()

    def load_statistics(self):
        try:
            stats = self.api_client.get_statistics()
            self.datasets_card.update_value(stats.get('total_datasets', 0))
            self.equipment_card.update_value(stats.get('total_equipment', 0))
        except Exception as e:
            print(f"Error loading statistics: {e}")

    def upload_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Select CSV File', '', 'CSV Files (*.csv)')
        if not file_path:
            return
        try:
            self.upload_btn.setEnabled(False); self.upload_btn.setText('Uploading...')
            self.upload_message.setText('📤 Uploading file...'); QApplication.processEvents()
            status_code, result = self.api_client.upload_csv(file_path)
            if status_code == 201:
                ds = result.get('dataset', {})
                self.upload_message.setHtml(f"""
                <div style='color:#22543d; background-color:#c6f6d5; padding:14px; border-radius:8px;'>
                    <b>✅ Upload Successful!</b><br>{result.get('message', 'File uploaded successfully')}<br>
                    <b>Dataset:</b> {ds.get('filename', '')}<br>
                    <b>Equipment Count:</b> {ds.get('total_equipment', 0)}</div>""")
                self.load_datasets(); self.load_statistics()
            else:
                error = result.get('error', 'Upload failed.')
                self.upload_message.setHtml(f"""
                <div style='color:#c53030; background-color:#fed7d7; padding:14px; border-radius:8px;'>
                    <b>❌ Error:</b> {error}</div>""")
        except requests.exceptions.ConnectionError:
            self.upload_message.setHtml("""
            <div style='color:#c53030; background-color:#fed7d7; padding:14px; border-radius:8px;'>
                <b>❌ Error:</b> Cannot connect to server.</div>""")
        except Exception as e:
            self.upload_message.setHtml(f"""
            <div style='color:#c53030; background-color:#fed7d7; padding:14px; border-radius:8px;'>
                <b>❌ Error:</b> {str(e)}</div>""")
        finally:
            self.upload_btn.setEnabled(True); self.upload_btn.setText('Choose CSV File')

    def load_datasets(self):
        try:
            self.datasets = self.api_client.list_datasets()
            self.datasets_table.setRowCount(len(self.datasets))
            for row, dataset in enumerate(self.datasets):
                self.datasets_table.setRowHeight(row, 44)
                self.datasets_table.setItem(row, 0, QTableWidgetItem(dataset['filename']))
                self.datasets_table.setItem(row, 1, QTableWidgetItem(dataset['upload_date'].split('T')[0]))
                eq_item = QTableWidgetItem(str(dataset['total_equipment']))
                eq_item.setTextAlignment(Qt.AlignCenter)
                self.datasets_table.setItem(row, 2, eq_item)
                for col, key in [(3, 'avg_flowrate'), (4, 'avg_pressure'), (5, 'avg_temperature')]:
                    item = QTableWidgetItem(f"{dataset[key]:.1f}")
                    item.setTextAlignment(Qt.AlignCenter)
                    self.datasets_table.setItem(row, col, item)

                action_widget = QWidget()
                action_widget.setStyleSheet("background:transparent; border:none;")
                al = QHBoxLayout(action_widget); al.setContentsMargins(4, 4, 4, 4); al.setSpacing(5)
                vb = StyledButton("View", "primary"); vb.setCursor(Qt.PointingHandCursor)
                vb.clicked.connect(lambda _, d=dataset['id']: self.view_dataset(d))
                pb = StyledButton("PDF", "success"); pb.setCursor(Qt.PointingHandCursor)
                pb.clicked.connect(lambda _, d=dataset['id']: self.generate_report(d))
                db = StyledButton("Delete", "danger"); db.setCursor(Qt.PointingHandCursor)
                db.clicked.connect(lambda _, d=dataset['id']: self.delete_dataset(d))
                al.addWidget(vb); al.addWidget(pb); al.addWidget(db)
                self.datasets_table.setCellWidget(row, 6, action_widget)
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Failed to load datasets:\n{str(e)}')

    def view_dataset(self, dataset_id):
        self.tabs.setCurrentWidget(self.viz_tab)
        while self.charts_layout.count():
            item = self.charts_layout.takeAt(0)
            if item.widget(): item.widget().deleteLater()
        try:
            data = self.api_client.get_dataset(dataset_id)
            self.current_dataset = data
            self.show_visualizations(data)
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def show_visualizations(self, data):
        for i in reversed(range(self.charts_layout.count())):
            w = self.charts_layout.itemAt(i).widget()
            if w: w.setParent(None)

        di = data['dataset']
        self.viz_info.setText(
            f"📊  Dataset: {di['filename']}   |   Equipment: {di['total_equipment']}   |   "
            f"Uploaded: {di['upload_date'].split('T')[0]}")
        self.viz_info.setStyleSheet("font-size:13px; color:#22543d; padding:12px 16px; background-color:#c6f6d5; border-radius:8px; border-left:4px solid #48bb78;")

        charts_grid = QWidget(); charts_grid.setMinimumHeight(400)
        gl = QGridLayout(charts_grid); gl.setSpacing(16)

        if 'type_distribution' in data and data['type_distribution']:
            pf = self._chart_frame(); pl = QVBoxLayout(pf)
            pc = ProfessionalMatplotlibCanvas(pf, width=5, height=3.5)
            pc.create_pie_chart(data['type_distribution'], 'Equipment Type Distribution')
            pl.addWidget(pc); gl.addWidget(pf, 0, 0)

        af = self._chart_frame(); al = QVBoxLayout(af)
        ac = ProfessionalMatplotlibCanvas(af, width=5, height=3.5)
        ac.create_bar_chart(['Flowrate', 'Pressure', 'Temperature'],
                            [di['avg_flowrate'], di['avg_pressure'], di['avg_temperature']],
                            'Average Parameters Comparison', 'Average Value',
                            [COLORS['chart_colors'][0], COLORS['chart_colors'][1], COLORS['chart_colors'][2]])
        al.addWidget(ac); gl.addWidget(af, 0, 1)
        self.charts_layout.addWidget(charts_grid)

        equipment_list = di['equipment'][:10]
        if equipment_list:
            gf = self._chart_frame(); gf.setMinimumHeight(320)
            gfl = QVBoxLayout(gf)
            gc = ProfessionalMatplotlibCanvas(gf, width=10, height=3.5)
            gc.create_grouped_bar_chart(equipment_list, 'Parameter Comparison (First 10 Equipment)')
            gfl.addWidget(gc); self.charts_layout.addWidget(gf)

        tf = self._chart_frame(); tfl = QVBoxLayout(tf)
        tt = QLabel('📋  Equipment Details')
        tt.setStyleSheet("font-size:16px; font-weight:bold; color:#2d3748; margin-bottom:8px; background:transparent; border:none;")
        tfl.addWidget(tt)

        et = QTableWidget(); et.setColumnCount(5)
        et.setHorizontalHeaderLabels(['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature'])
        et.setRowCount(len(di['equipment'])); et.setStyleSheet(TABLE_STYLE)
        et.setShowGrid(False); et.verticalHeader().setVisible(False)
        for i, eq in enumerate(di['equipment']):
            et.setItem(i, 0, QTableWidgetItem(eq['equipment_name']))
            et.setItem(i, 1, QTableWidgetItem(eq['equipment_type']))
            for c, k in [(2, 'flowrate'), (3, 'pressure'), (4, 'temperature')]:
                item = QTableWidgetItem(f"{eq[k]:.1f}")
                item.setTextAlignment(Qt.AlignCenter)
                et.setItem(i, c, item)
        et.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        et.setAlternatingRowColors(True); et.setEditTriggers(QTableWidget.NoEditTriggers)
        tfl.addWidget(et); self.charts_layout.addWidget(tf)

        self.charts_widget.adjustSize(); self.charts_widget.repaint()
        self.charts_widget.update()
        QTimer.singleShot(0, self.charts_widget.adjustSize)

    def _chart_frame(self):
        frame = QFrame()
        frame.setStyleSheet("QFrame { background-color:white; border:1px solid #e2e8f0; border-radius:10px; padding:14px; }")
        frame.setFrameStyle(QFrame.StyledPanel)
        return frame

    def generate_report(self, dataset_id):
        save_path, _ = QFileDialog.getSaveFileName(self, 'Save Report', f'equipment_report_{dataset_id}.pdf', 'PDF Files (*.pdf)')
        if save_path:
            try:
                self.api_client.generate_report(dataset_id, save_path)
                QMessageBox.information(self, 'Success', f'✅ Report generated successfully!\n\nSaved to: {save_path}')
            except Exception as e:
                QMessageBox.warning(self, 'Error', f'Failed to generate report: {str(e)}')

    def delete_dataset(self, dataset_id):
        reply = QMessageBox.question(self, 'Confirm Delete',
                                     'Are you sure you want to delete this dataset?\n\nThis action cannot be undone.',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                self.api_client.delete_dataset(dataset_id)
                QMessageBox.information(self, 'Success', '✅ Dataset deleted successfully!')
                self.load_datasets(); self.load_statistics()
                if self.current_dataset and self.current_dataset['dataset']['id'] == dataset_id:
                    for i in reversed(range(self.charts_layout.count())):
                        w = self.charts_layout.itemAt(i).widget()
                        if w: w.setParent(None)
                    self.current_dataset = None
            except Exception as e:
                QMessageBox.warning(self, 'Error', f'Failed to delete dataset: {str(e)}')

    def handle_logout(self):
        reply = QMessageBox.question(self, 'Confirm Logout', 'Are you sure you want to logout?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.controller.on_logout()


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    font = QFont("Segoe UI", 10)
    font.setStyleStrategy(QFont.PreferAntialias)
    app.setFont(font)

    api_client = APIClient()
    controller = AppController(api_client)
    _keep_window(controller)  # prevent GC of the controller itself
    controller.show_login()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

