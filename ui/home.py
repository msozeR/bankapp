from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QInputDialog
import requests

API_URL = "http://192.168.2.108:5000"

isim="numannn"
class HomeScreen(QWidget):
    def __init__(self, user_id):
        super().__init__()

        self.user_id = user_id
        self.setWindowTitle("Ana Sayfa")
        self.setGeometry(400, 200, 300, 300)

        layout = QVBoxLayout()

        self.welcome_label = QLabel(f"Hoş geldiniz, {self.get_user_name()}!")
        layout.addWidget(self.welcome_label)

        self.balance_label = QLabel(f"Bakiye: {self.get_balance()} TL")
        layout.addWidget(self.balance_label)

        self.deposit_button = QPushButton("Para Yatır", self)
        self.deposit_button.clicked.connect(self.deposit_money)
        layout.addWidget(self.deposit_button)

        self.withdraw_button = QPushButton("Para Çek", self)
        self.withdraw_button.clicked.connect(self.withdraw_money)
        layout.addWidget(self.withdraw_button)

        self.transfer_button = QPushButton("Para Transferi", self)
        self.transfer_button.clicked.connect(self.transfer_money)
        layout.addWidget(self.transfer_button)

        self.history_button = QPushButton("İşlem Geçmişi", self)
        self.history_button.clicked.connect(self.view_history)
        layout.addWidget(self.history_button)

        self.setLayout(layout)

    def get_user_name(self):
        try:
            response = requests.get(f"{API_URL}/user/{self.user_id}")
            if response.status_code == 200:
                user = response.json()
                return f"{user['name']} {user['surname']}"
            else:
                return "Bilinmeyen Kullanıcı"
        except:
            return "Sunucu Hatası"

    def get_balance(self):
        try:
            response = requests.get(f"{API_URL}/balance/{self.user_id}")
            if response.status_code == 200:
                return response.json()["balance"]
            else:
                return "Hata"
        except:
            return "Bağlantı Yok"

    def deposit_money(self):
        amount, ok = QInputDialog.getDouble(self, "Para Yatır", "Miktarı girin:", 0, 0, 200000, 2)
        if ok:
            try:
                response = requests.post(f"{API_URL}/deposit", json={
                    "user_id": self.user_id,
                    "amount": amount
                })
                if response.status_code == 200:
                    self.update_balance_label()
                    QMessageBox.information(self, "Başarılı", f"{amount} TL yatırıldı!")
                else:
                    QMessageBox.warning(self, "Hata", "İşlem başarısız!")
            except:
                QMessageBox.critical(self, "Bağlantı Hatası", "Sunucuya bağlanılamadı!")

    def withdraw_money(self):
        amount, ok = QInputDialog.getDouble(self, "Para Çek", "Miktarı girin:", 0, 0, 200000, 2)
        if ok:
            try:
                response = requests.post(f"{API_URL}/withdraw", json={
                    "user_id": self.user_id,
                    "amount": amount
                })
                if response.status_code == 200:
                    self.update_balance_label()
                    QMessageBox.information(self, "Başarılı", f"{amount} TL çekildi!")
                else:
                    QMessageBox.warning(self, "Hata", response.json().get("error", "İşlem başarısız!"))
            except:
                QMessageBox.critical(self, "Bağlantı Hatası", "Sunucuya bağlanılamadı!")

    def transfer_money(self):
        tc, ok = QInputDialog.getText(self, "Para Transferi", "Alıcı TC Kimlik No:")
        if ok and tc:
            if not (tc.isdigit() and len(tc) == 11):
                QMessageBox.warning(self, "Geçersiz Giriş", "TC Kimlik numarası 11 haneli ve sadece rakamlardan oluşmalıdır.")
                return

        amount, ok2 = QInputDialog.getDouble(self, "Para Transferi", "Miktarı girin:", 0, 0, 200000, 2)
        if ok2:
            try:
                response = requests.post(f"{API_URL}/transfer", json={
                    "sender_id": self.user_id,
                    "receiver_tc": tc,
                    "amount": amount
                })
                if response.status_code == 200:
                    self.update_balance_label()
                    QMessageBox.information(self, "Başarılı", f"{amount} TL {tc} numaralı kişiye gönderildi!")
                else:
                    QMessageBox.warning(self, "Hata", response.json().get("error", "Transfer başarısız!"))
            except:
                QMessageBox.critical(self, "Bağlantı Hatası", "Sunucuya bağlanılamadı!")


    def view_history(self):
        try:
            response = requests.get(f"{API_URL}/history/{self.user_id}")
            if response.status_code == 200:
                history = response.json()["history"]
                if history:
                    history_text = "\n".join([f"{item['type']}: {item['amount']} TL ({item['date']})" for item in history])
                    QMessageBox.information(self, "İşlem Geçmişi", history_text)
                else:
                    QMessageBox.information(self, "İşlem Geçmişi", "Henüz işlem yapılmamış!")
            else:
                QMessageBox.warning(self, "Hata", "İşlem geçmişi alınamadı.")
        except:
            QMessageBox.critical(self, "Bağlantı Hatası", "Sunucuya bağlanılamadı!")

    def update_balance_label(self):
        self.balance_label.setText(f"Bakiye: {self.get_balance()} TL")
