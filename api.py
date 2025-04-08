from flask import Flask, request, jsonify
from flask_cors import CORS
import database

app = Flask(__name__)
CORS(app)



@app.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data.get("name")
    surname = data.get("surname")
    tc = data.get("tc")
    password = data.get("password")

    if database.register_user(name, surname, tc, password):
        return jsonify({"success": True, "message": "Kayıt başarılı!"}), 201
    else:
        return jsonify({"success": False, "message": "Bu TC Kimlik Numarası zaten kayıtlı!"}), 409

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    tc = data.get("tc")
    password = data.get("password")

    user_id = database.validate_user(tc, password)
    if user_id:
        return jsonify({"success": True, "user_id": user_id}), 200
    else:
        return jsonify({"success": False, "message": "Geçersiz TC veya şifre!"}), 401

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = database.get_user_by_id(user_id)
    if user:
        return jsonify({"name": user[0], "surname": user[1]}), 200
    return jsonify({"error": "Kullanıcı bulunamadı."}), 404

@app.route('/balance/<int:user_id>', methods=['GET'])
def get_balance(user_id):
    balance = database.check_balance(user_id)
    return jsonify({"balance": balance}), 200

@app.route('/deposit', methods=['POST'])
def deposit():
    data = request.json
    user_id = data.get("user_id")
    amount = data.get("amount")
    if user_id is None or amount is None:
        return jsonify({"error": "Eksik veri."}), 400

    database.add_transaction(user_id, "Yatırma", amount)
    return jsonify({"message": f"{amount} TL yatırıldı."}), 200

@app.route('/withdraw', methods=['POST'])
def withdraw():
    data = request.json
    user_id = data.get("user_id")
    amount = data.get("amount")
    if user_id is None or amount is None:
        return jsonify({"error": "Eksik veri."}), 400

    balance = database.check_balance(user_id)
    if balance >= amount:
        database.add_transaction(user_id, "Çekme", -amount)
        return jsonify({"message": f"{amount} TL çekildi."}), 200
    else:
        return jsonify({"error": "Yetersiz bakiye."}), 400

@app.route('/transfer', methods=['POST'])
def transfer():
    data = request.json
    sender_id = data.get("sender_id")
    receiver_tc = data.get("receiver_tc")
    amount = data.get("amount")

    receiver_id = database.get_user_id_by_tc(receiver_tc)
    if not receiver_id:
        return jsonify({"error": "Alıcı bulunamadı."}), 404

    balance = database.check_balance(sender_id)
    if balance >= amount:
        database.add_transaction(sender_id, "Transfer (Gönderilen)", -amount)
        database.add_transaction(receiver_id, "Transfer (Alınan)", amount)
        return jsonify({"message": f"{amount} TL transfer edildi."}), 200
    else:
        return jsonify({"error": "Yetersiz bakiye."}), 400

@app.route('/history/<int:user_id>', methods=['GET'])
def get_history(user_id):
    history = database.get_transaction_history(user_id)
    formatted_history = [
        {"id": h[0], "type": h[1], "amount": h[2], "date": h[3]} for h in history
    ]
    return jsonify({"history": formatted_history}), 200



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
