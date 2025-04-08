from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
import requests

API_URL = "http://192.168.2.108:5000"
  # Flask API adresi

class RegisterScreen(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Kayıt Ol")
        self.setGeometry(400, 200, 300, 300)

        layout = QVBoxLayout()

        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("İsim")
        self.name_input.setValidator(QRegExpValidator(QRegExp("^[A-Za-zıİşŞğĞüÜçÇöÖçÇ ]+$")))
        self.name_input.textChanged.connect(self.convert_to_upper)
        layout.addWidget(self.name_input)

        self.surname_input = QLineEdit(self)
        self.surname_input.setPlaceholderText("Soyisim")
        self.surname_input.setValidator(QRegExpValidator(QRegExp("^[A-Za-zıİşŞğĞüÜçÇöÖçÇ ]+$")))
        self.surname_input.textChanged.connect(self.convert_to_upper)
        layout.addWidget(self.surname_input)

        self.tc_input = QLineEdit(self)
        self.tc_input.setPlaceholderText("TC Kimlik No (11 Hane)")
        self.tc_input.setMaxLength(11)
        self.tc_input.setValidator(QRegExpValidator(QRegExp("^[0-9]{11}$")))
        layout.addWidget(self.tc_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Şifre (6 Haneli)")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setValidator(QRegExpValidator(QRegExp("^[0-9]{6}$")))
        layout.addWidget(self.password_input)

        self.confirm_password_input = QLineEdit(self)
        self.confirm_password_input.setPlaceholderText("Şifreyi Tekrar Girin (6 Haneli)")
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setValidator(QRegExpValidator(QRegExp("^[0-9]{6}$")))
        layout.addWidget(self.confirm_password_input)

        self.register_button = QPushButton("Kaydol", self)
        self.register_button.clicked.connect(self.register)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def convert_to_upper(self):
        sender = self.sender()
        sender.setText(sender.text().upper())

    def register(self):
        name = self.name_input.text()
        surname = self.surname_input.text()
        tc = self.tc_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()

        if len(tc) != 11 or not tc.isdigit():
            QMessageBox.warning(self, "Hata", "TC Kimlik Numarası 11 haneli ve sadece rakamlardan oluşmalıdır!")
            return

        if not name or not surname or not password or not confirm_password:
            QMessageBox.warning(self, "Hata", "Lütfen tüm alanları doldurun!")
            return

        if password != confirm_password:
            QMessageBox.warning(self, "Hata", "Şifreler uyuşmuyor!")
            return

        try:
            response = requests.post(f"{API_URL}/register", json={
                "name": name,
                "surname": surname,
                "tc": tc,
                "password": password
            })
            data = response.json()
            if response.status_code == 201:
                QMessageBox.information(self, "Başarılı", data.get("message", "Kayıt başarılı!"))
                self.close()
            else:
                QMessageBox.warning(self, "Hata", data.get("message", "Kayıt başarısız!"))
        except Exception as e:
            print(str(e))  # Hatanın detayını terminalde gör
            QMessageBox.critical(self, "Bağlantı Hatası", f"Sunucuya bağlanılamadı!\n\n{str(e)}")

