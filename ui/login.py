from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
import requests
from ui.register import RegisterScreen
from ui.home import HomeScreen

API_URL = "http://192.168.2.108:5000"
  # Flask API adresi

class LoginScreen(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Giriş Yap")
        self.setGeometry(400, 200, 300, 200)
        self.setStyleSheet("""  # <-- BURASI
            QWidget {
                background-color: #f5f7fa;
                font-family: 'Segoe UI';
                font-size: 14px;
            }
            QLabel {
                font-size: 16px;
                font-weight: bold;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 6px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3e8e41;
            }
        """)
        

        layout = QVBoxLayout()

        self.tc_input = QLineEdit(self)
        self.tc_input.setPlaceholderText("TC Kimlik No")
        self.tc_input.setMaxLength(11)
        self.tc_input.setValidator(QRegExpValidator(QRegExp("^[0-9]{11}$")))
        layout.addWidget(self.tc_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Şifre (6 Haneli)")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMaxLength(6)
        self.password_input.setValidator(QRegExpValidator(QRegExp("^[0-9]{6}$")))
        layout.addWidget(self.password_input)

        self.login_button = QPushButton("Giriş Yap", self)
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        self.register_button = QPushButton("Kayıt Ol", self)
        self.register_button.clicked.connect(self.open_register)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def login(self):
        tc = self.tc_input.text()
        password = self.password_input.text()

        if len(tc) != 11 or not tc.isdigit():
            QMessageBox.warning(self, "Hata", "TC Kimlik Numarası 11 haneli ve yalnızca rakamlardan oluşmalıdır!")
            return

        if len(password) != 6 or not password.isdigit():
            QMessageBox.warning(self, "Hata", "Şifre 6 haneli ve yalnızca rakamlardan oluşmalıdır!")
            return

        try:
            response = requests.post(f"{API_URL}/login", json={"tc": tc, "password": password})
            if response.status_code == 200 and response.json().get("success"):
                user_id = response.json().get("user_id")
                QMessageBox.information(self, "Başarılı", "Giriş başarılı!")
                self.home_window = HomeScreen(user_id)
                self.home_window.show()
                self.close()
            else:
                msg = response.json().get("message", "Giriş başarısız!")
                QMessageBox.warning(self, "Hata", msg)
        except Exception as e:
            QMessageBox.critical(self, "Bağlantı Hatası", f"Sunucuya bağlanılamadı!\n\n{str(e)}")

    def open_register(self):
        self.register_window = RegisterScreen()
        self.register_window.show()
