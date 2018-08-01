from flask import Flask, request, jsonify
from transaction import create_transaction_from_json

import logging


app = Flask("TIELIE_RPC_v1")

# 待定交易列表，新提交的交易会被加入到该列表内
pending_txs = []

@app.route('/tx', methods=['POST'])
def submit_tx():
    """
    提交交易
    
    交易将被加入到待定列表
    """
    payload = request.get_json()
    tx = create_transaction_from_json(payload)

    # 将交易放入待定列表
    pending_txs.append(tx)

    logging.info('收到新交易：%s，当前待定交易数量：%d', tx, len(pending_txs))

    return jsonify(
        result=tx.to_json(), 
        msg="铁链本节点成功收到交易",
    ), 201


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(debug=True)