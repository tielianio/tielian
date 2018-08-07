class Transaction:
    """
    交易
    """

    def __init__(self, _from, _to, _value):
        self.sender = _from
        self.to = _to
        self.value = _value

    def to_json(self):
        return {
            'sender': self.sender,
            'to': self.to,
            'value': self.value
        }

    def __str__(self):
        return 'Transaction<sender=%s, to=%s, value=%s>' % (self.sender, self.to, self.value)


def _create_transaction_from_json(payload):
    return Transaction(payload['sender'], payload['to'], payload['value'])

def create_transaction_from_json(payload):
    """
    将传入的JSON转化成交易对象，若JSON是列表，就返回一个交易对象列表
    """
    if type(payload) is list:
        return [_create_transaction_from_json(obj) for obj in payload]
    elif type(payload) is dict:
        return _create_transaction_from_json(payload)
    else:
        raise Exception('错误的负载类型')

def dump_transactions(txs):
    return [tx.to_json() for tx in txs]


def _contains_tx(tx, txs):
    """
    判断 txs 是否包含 tx
    """
    for t in txs:
        if t.sender == tx.sender and t.to == tx.to and t.value == tx.value:
            return True
    return False

def trim_pending_txs(pending_txs, block):
    """
    将已经打包的交易从待打包交易去掉

    现在的时间复杂度是 O(n^2)，因为要同时遍历 pending_txs 和 block 中的交易
    """
    block_txs = block.txs

    return list(filter(lambda tx: _contains_tx(tx, block_txs), pending_txs))