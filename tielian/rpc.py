import dataclasses
import logging

from flask import Flask, jsonify, request

from tielian.block import Block, create_genesis_block
from tielian.transaction import Transaction

app = Flask('TIELIAN_RPC_v1')

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
    tx = Transaction(**payload)

    # 将交易放入待打包交易
    pending_txs.append(tx)

    logging.info('收到新交易：%s，当前待定交易数量：%d', tx, len(pending_txs))

    return jsonify(
        result=dataclasses.asdict(tx),
        msg='铁链本节点成功收到交易',
    ), 201


@app.route('/txs', methods=['GET'])
def get_pending_txs():
    """ 获取待打包交易 """
    txs = list(map(lambda tx: dataclasses.asdict(tx), pending_txs))
    return jsonify(txs)


@app.route('/blocks', methods=['POST'])
def submit_block():
    """ 提交已打包新区块 """
    global pending_txs
    payload = request.get_json()
    block = Block(**payload)

    try:
        current_block = chain[-1]
        block.is_valid(current_block)
    except Exception as ex:
        raise Exception(f'非法区块尝试上链！{ex}')

    # 把已经打包的交易从待打包交易去掉
    # TODO: 可以优化这一步
    pending_txs = list(filter(lambda tx: tx in block.txs, pending_txs))

    chain.append(block)
    return '', 201


@app.route('/blocks', methods=['GET'])
def get_all_blocks():
    """ 获取所有区块 """
    blocks = list(map(lambda x: dataclasses.asdict(x), chain))
    return jsonify(blocks=blocks)


@app.route('/blocks/latest', methods=['GET'])
def get_latest_block():
    """ 获取最近得到的区块 """
    return jsonify(block=dataclasses.asdict(chain[-1]))


@app.errorhandler(Exception)
def error_handler(ex):
    logging.exception(ex)
    return jsonify(msg=str(ex)), 500


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    # 铁链先甩起来
    app.run(debug=True)
