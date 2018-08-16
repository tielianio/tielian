import dataclasses


@dataclasses.dataclass
class Transaction:
    """ 交易 """
    sender: str
    to: str
    value: str
    # TODO 考虑 tx 加入 timestamp
