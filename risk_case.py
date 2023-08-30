from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)

# Simula um banco de dados para histórico de transações
chargebacks = set()
transaction_history = {}

@app.route('/anti_fraud', methods=['POST'])
def anti_fraud():
    transaction = request.json
    
    transaction_id = transaction["transaction_id"]
    user_id = transaction["user_id"]
    transaction_amount = transaction["transaction_amount"]
    transaction_date = datetime.datetime.fromisoformat(transaction["transaction_date"])

    # Verificar se o ch ja teve cbk
    if user_id in chargebacks:
        return jsonify({"transaction_id": transaction_id, "recommendation": "deny"})
    
    # Verificar transações consecutivas
    if user_id in transaction_history:
        last_transaction_date = transaction_history[user_id]
        if (transaction_date - last_transaction_date).seconds < 10:  # menos de 10 segundos desde a última transação
            return jsonify({"transaction_id": transaction_id, "recommendation": "deny"})
    
    # Verificar valor da transação
    if transaction_amount > 1000:  # limite arbitrário
        return jsonify({"transaction_id": transaction_id, "recommendation": "deny"})
    
    # Se passar em todas as verificações, a transação pode ser aprovada
    transaction_history[user_id] = transaction_date
    return jsonify({"transaction_id": transaction_id, "recommendation": "approve"})

if __name__ == '__main__':
    app.run(debug=True)