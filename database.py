import sqlite3

DB_NAME = "bank.db"

def create_tables():
    """Veritabanını ve tabloları oluşturur"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Kullanıcılar tablosunu oluştur (tc_kimlik sütunu)
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        isim TEXT NOT NULL,
                        soyisim TEXT NOT NULL,
                        tc_kimlik TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        bakiye REAL DEFAULT 0
                    )''')

    # İşlemler tablosunu oluştur
    cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        islem_turu TEXT,
                        miktar REAL,
                        tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(id)
                    )''')

    conn.commit()
    conn.close()

def register_user(name, surname, tc_kimlik, password):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (isim, soyisim, tc_kimlik, password) VALUES (?, ?, ?, ?)",
                       (name, surname, tc_kimlik, password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False  # TC kimlik numarası zaten kayıtlı

def validate_user(tc_kimlik, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE tc_kimlik = ? AND password = ?", (tc_kimlik, password))
    user = cursor.fetchone()
    conn.close()
    return user[0] if user else None

def get_user_by_id(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT isim, soyisim FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def add_transaction(user_id, transaction_type, amount):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO transactions (user_id, islem_turu, miktar) VALUES (?, ?, ?)",
                   (user_id, transaction_type, amount))
    conn.commit()
    conn.close()

def check_balance(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(miktar) FROM transactions WHERE user_id = ?", (user_id,))
    balance = cursor.fetchone()[0]
    conn.close()
    return balance if balance else 0

def get_transaction_history(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, islem_turu, miktar, tarih FROM transactions WHERE user_id = ? ORDER BY tarih DESC", (user_id,))
    history = cursor.fetchall()
    conn.close()
    return history

def get_user_id_by_tc(tc_kimlik):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE tc_kimlik = ?", (tc_kimlik,))
    user = cursor.fetchone()
    conn.close()
    return user[0] if user else None

def get_balance(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT bakiye FROM users WHERE id = ?", (user_id,))
    balance = cursor.fetchone()
    conn.close()
    return balance[0] if balance else 0
