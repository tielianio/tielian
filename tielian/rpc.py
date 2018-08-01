from flask import Flask, request, jsonify
from transaction import create_transaction_from_json


app = Flask("TIELIE_RPC_v1")

pending_txs = []

@app.route('/tx', methods=['POST'])
def submit_tx():
    payload = request.get_json()
    tx = create_transaction_from_json(payload)

    pending_txs.append(tx)

    return jsonify(result=tx.to_json()), 201


if __name__ == '__main__':
    app.run(debug=True)