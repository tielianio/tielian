import dataclasses
import logging
import time
from typing import List

import requests

from tielian.block import Block
from tielian.transaction import Transaction


class MiningJob:
    """ CPU挖矿的一个工作 """

    def __init__(self, previous_block: Block, pending_txs: List[Transaction]):
        self.previous_block = previous_block
        self.pending_txs = pending_txs

        data = {
            'txs': [dataclasses.asdict(_) for _ in self.pending_txs],
        }

        self.block = Block(
            index=self.previous_block.index + 1,
            timestamp=int(time.time()),
            data=data,
            previous_hash=self.previous_block.hash,
            nonce=self.previous_block.nonce + 1,
        )

        self.is_mined = False

    def validate_difficulty(self):
        """
        若验证难度通过，返回True；否则返回False

        Block中同样的函数会抛出异常，为了本类中`mine`方法的简洁性，这里不抛出异常。
        反正应该只要检测是否找到nonce即可，不需要再判断lineage。
        """
        try:
            self.block.validate_difficulty()
            return True
        except Exception:
            return False

    def mine(self):
        """ 打包 """
        # 总归能找到，所以不会是一个死循环。
        # 可以考虑是否增加一个超时或者停止条件
        while not self.validate_difficulty():
            # 找下一个nonce
            self.block.nonce += 1

        return self.block


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    base_url = 'http://localhost:5000'

    # 准备数据
    previous_block_payload = requests.get(base_url + '/blocks/latest').json()['block']
    logging.debug(previous_block_payload)
    previous_block = Block(**previous_block_payload)

    pending_txs_payload = requests.get(base_url + '/txs').json()
    logging.debug(pending_txs_payload)
    pending_txs = [Transaction(**payload) for payload in pending_txs_payload]

    # 准备工作
    job = MiningJob(previous_block, pending_txs)

    # 跑起来
    block = job.mine()
    logging.info('找到合法区块：%s', block.to_json())
