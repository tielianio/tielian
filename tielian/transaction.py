import dataclasses


@dataclasses.dataclass
class Transaction:
    """ 交易 """
    sender: str
    to: str
    value: str
    # TODO 考虑 tx 加入 timestamp


def create_transaction_from_json(payload):
    """ 将传入的JSON转化成交易对象，若JSON是列表，就返回一个交易对象列表 """
    if isinstance(payload, list):
        return [create_transaction_from_json(_) for _ in payload]
    elif isinstance(payload, dict):
        return Transaction(**payload)
    else:
        raise Exception('错误的负载类型')
