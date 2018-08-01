class Transaction:

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


def create_transaction_from_json(payload):
    return Transaction(payload['sender'], payload['to'], payload['value'])
