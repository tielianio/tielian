import hashlib
from datetime import datetime
import logging
import time
import sys
from transaction import create_transaction_from_json

class Block:

    def __init__(self, _index, _timestamp, _data, _previous_hash):
        # 区块高度
        self.index = _index

        # 时间戳
        self.timestamp = _timestamp

        # 任意数据
        self.data = _data

        # 上一个区块哈希
        self.previous_hash = _previous_hash

        # 区块哈希
        self.hash = self.calc_hash()

    def calc_hash(self):
        """
        根据区块数据，生成唯一的区块哈希。哈希算法是最最简单的sha256。
        """
        sha = hashlib.sha256()
        sig = "%s%s%s%s" % (self.index, self.timestamp, self.data, self.previous_hash)

        # 因为数据(data)可能会有中文，这里用统一utf8编码
        sha.update(sig.encode('utf8'))

        return sha.hexdigest()

    @property
    def txs(self):
        return map(lambda p: create_transaction_from_json(p), self.data['txs'])

    def to_json(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "hash": self.hash
        }

    def is_valid(self, chain):
        """
        验证区块是否合格

        Dummy实现中[暂时]都是合法的
        """

        return self.previous_hash == chain[-1].hash



def create_genesis_block():
    """
    创建创始区块
    """
    now = int(datetime.now().timestamp())
    return Block(0, now, "Skr! 我是创始区块!", "0")

def load_block(payload):
    """
    将 JSON 格式的新区块变成 Block 类型
    """
    return Block(
        payload['index'],
        payload['timestamp'],
        payload['data'],
        payload['previous_hash']
    )
    



def new_block(last_block, data):
    """
    生成新区块，需要上一个区块的哈希值来连接铁链
    """
    index = last_block.index + 1
    timestamp = datetime.now()
    previous_hash = last_block.hash

    return Block(index, timestamp, data, previous_hash)


def run():
    chain = [create_genesis_block()]

    # 铁链上最新的区块
    current_block = chain[0]

    while True:
        # 广播当前区块
        logging.info("新区块<#%3d, h=%s>加入铁链：%s", current_block.index, current_block.hash, current_block.data)

        # 生成新区块
        data = "你好，我是区块<#%d>" % (current_block.index + 1)
        pending_block = new_block(current_block, data)

        # 矿工挖矿🚧
        # [现在是睡眠挖矿，起床捡钱。之后换成工作量证明]
        time.sleep(1)

        # 新区块加入铁链
        chain.append(pending_block)

        # 更新最新区块指针
        current_block = pending_block

        # [周而复始...↑]

if __name__ == '__main__':
    # 配置日志，打到控制台上
    logging.basicConfig(level=logging.INFO)

    # 铁链甩起来！
    logging.info("区块链？就是...铁链嘛！\n\n")

    try:
        run()
    except KeyboardInterrupt:
        logging.info("铁链断裂[-END-]")
        sys.exit(0)