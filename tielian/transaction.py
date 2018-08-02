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


def create_transaction_from_json(payload):
    return Transaction(payload['sender'], payload['to'], payload['value'])

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