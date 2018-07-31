from hashlib import hasher

class Block:

    def __init__(self, _index, _previous_hash, _timestamp, _data):
        # 区块高度
        self.index = _index

        # 上一个区块哈希
        self.previous_hash = _previous_hash

        # 时间戳
        self.timestamp = _timestamp

        # 任意数据
        self.data = _data

        # 区块哈希
        self.hash = self.calc_hash()

    def calc_hash(self):
        sha = hasher.sha256()
        sig = "%s%s%s%s" % (self.index, self.timestamp, self.data, self.previous_hash)
        sha.update(sig)

        return sha.hexdigest()

    