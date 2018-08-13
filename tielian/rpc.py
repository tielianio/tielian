import logging

from flask import Flask, jsonify, request

from tielian.block import create_genesis_block, load_block
from tielian.transaction import create_transaction_from_json, trim_pending_txs

app = Flask('TIELIE_RPC_v1')

# 待定交易列表，新提交的交易会被加入到该列表内
pending_txs = []

chain = [create_genesis_block()]


@app.route('/txs', methods=['POST'])
def submit_tx():
    """
    提交交易

    交易将被加入到待打包交易
    """
    payload = request.get_json()
    tx = create_transaction_from_json(payload)

    # 将交易放入待打包交易
    pending_txs.append(tx)

    logging.info('收到新交易：%s，当前待定交易数量：%d', tx, len(pending_txs))

    return jsonify(
        result=tx.to_json(),
        msg='铁链本节点成功收到交易',
    ), 201


@app.route('/txs', methods=['GET'])
def get_pending_txs():
    txs = list(map(lambda x: x.to_json(), pending_txs))
    return jsonify(txs)


@app.route('/blocks', methods=['POST'])
def submit_block():
    """
    提交已打包新区块
    """
    global pending_txs

    block = load_block(request.get_json())

    try:
        current_block = chain[-1]
        block.is_valid(current_block)
    except Exception as e:
        raise Exception('非法区块尝试上链！%s' % e)

    # 把已经打包的交易从待打包交易去掉
    pending_txs = trim_pending_txs(pending_txs, block)

    chain.append(block)
    return "", 201


@app.route('/blocks', methods=['GET'])
def get_all_blocks():
    """
    获取所有区块
    """
    blocks = list(map(lambda x: x.to_json(), chain))
    return jsonify(blocks=blocks)


@app.route('/blocks/latest', methods=['GET'])
def get_latest_block():
    return jsonify(block=chain[-1].to_json())


@app.errorhandler(Exception)
def error_handler(e):
    return jsonify(msg=str(e)), 500


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    # 铁链先甩起来
    app.run(debug=True)
