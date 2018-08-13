import dataclasses


@dataclasses.dataclass
class Transaction:
    """ 交易 """
    sender: str
    to: str
    value: str


def create_transaction_from_json(payload):
    """ 将传入的JSON转化成交易对象，若JSON是列表，就返回一个交易对象列表 """
    if isinstance(payload, list):
        return [create_transaction_from_json(_) for _ in payload]
    elif isinstance(payload, dict):
        return Transaction(**payload)
    else:
        raise Exception('错误的负载类型')


def trim_pending_txs(pending_txs, block):
    """
    将已经打包的交易从待打包交易去掉

    现在的时间复杂度是 O(n^2)，因为要同时遍历 pending_txs 和 block 中的交易
    """
    # TODO 考虑 tx 加入 timestamp
    block_txs = block.txs

    return list(filter(lambda tx: tx in block_txs, pending_txs))
