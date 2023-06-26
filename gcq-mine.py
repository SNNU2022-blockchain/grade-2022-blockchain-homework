import hashlib
import time
from collections import defaultdict


# 区块类
class Block:
    def __init__(self, index, timestamp, data, previous_hash, uncle_blocks=None):
        """
        区块类的构造函数。
        index: 区块索引
        timestamp: 区块时间戳
        data: 区块数据
        previous_hash: 前一个区块的哈希值
        uncle_blocks: 叔父区块列表，默认为None
        """
        self.index = index
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.timestamp = timestamp
        self.hash = self.calculate_hash()
        self.finishTimestamp = timestamp
        self.uncle_blocks = uncle_blocks if uncle_blocks is not None else []

    def calculate_hash(self):
        """
        计算区块的哈希值。
        """
        data = str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash) + str(self.nonce)
        return hashlib.sha256(data.encode()).hexdigest()

    def mine_block(self, difficulty):
        """
        挖矿函数，通过不断调整nonce值计算满足难度要求的哈希值。
        difficulty: 挖矿的难度值
        """
        while self.hash[:difficulty] != '0' * difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()
        self.finishTimestamp = time.time()


    def print_block(self):
        """
        打印区块的信息。
        """
        print("Block #", self.index)
        print("Timestamp:", self.timestamp)
        print("Data:", self.data)
        print("Previous Hash:", self.previous_hash)
        print("Hash:", self.hash)
        print("finishTimestamp:", self.finishTimestamp)
        print("Nonce:", self.nonce)
        print("Uncle Blocks:", [uncle.index for uncle in self.uncle_blocks])
        print()


# 交易类
class Transaction:
    def __init__(self, sender, recipient, amount):
        """
        交易类的构造函数。
        sender: 交易发送者
        recipient: 交易接收者
        amount: 交易金额
        """
        self.sender = sender
        self.recipient = recipient
        self.amount = amount


# 区块链类
class Blockchain:
    def __init__(self):
        """
        区块链类的构造函数。
        """
        self.chain = [self.create_genesis_block()]  # 存储区块的列表
        self.difficulty = 2  # 初始难度值
        self.pending_transactions = []  # 待处理的交易列表
        self.uncle_blocks = defaultdict(list)  # 叔父区块的字典，存储每个区块的叔父区块列表

    def create_genesis_block(self):
        """
        创建创世区块。
        """
        return Block(0, time.time(), "Genesis Block", "0")

    def get_latest_block(self):
        """
        获取最新的区块。
        """
        return self.chain[-1]

    def add_transaction(self, transaction):
        """
        添加待处理的交易。
        transaction: 待处理的交易对象
        """
        self.pending_transactions.append(transaction)

    def mine_pending_transactions(self, miner_address):
        """
        挖掘待处理的交易并生成新的区块。
        miner_address: 矿工的地址
        """
        block = Block(len(self.chain), time.time(), self.pending_transactions, self.get_latest_block().hash)
        block.mine_block(self.difficulty)
        print("Block mined!")
        self.chain.append(block)

        self.pending_transactions = []
        self.adjust_difficulty()

        # 奖励矿工
        reward_transaction = Transaction("System", miner_address, 1.0)
        self.pending_transactions.append(reward_transaction)

        # 添加叔父区块
        if len(self.chain) > 1:
            uncle_block = self.chain[-2]
            self.uncle_blocks[block.hash].append(uncle_block)

        block.print_block()
        self.mine_pending_transactions(miner_address)

        # if len(self.chain) > 1:
        #     for uncle in self.uncle_blocks[block.hash]:
        #         uncle.print_block()

    def adjust_difficulty(self):
        """
        根据挖矿的速度调整难度值。
        """
        if len(self.chain) > 1:
            block_timestamp = self.chain[-1].finishTimestamp
            previous_timestamp = self.chain[-2].finishTimestamp
            time_difference = block_timestamp - previous_timestamp
            print('区块时间间隔', time_difference)
            if time_difference >= 5:
                self.difficulty -= 1
                print("调整当前难度值为：", self.difficulty)
            else:
                self.difficulty += 1
                print("调整当前难度值为：", self.difficulty)

    def print_chain(self):
        """
        打印区块链的信息。
        """
        for block in self.chain:
            block.print_block()


# 创建区块链对象
blockchain = Blockchain()

# 定义挖矿函数
def mine_transactions(miner_address):
    if len(blockchain.pending_transactions) > 0:
        blockchain.mine_pending_transactions(miner_address)

# 模拟生成1000笔交易
for i in range(50):
    sender = "Sender{}".format(i)
    recipient = "Recipient{}".format(i)
    amount = i + 0.5
    transaction = Transaction(sender, recipient, amount)
    blockchain.add_transaction(transaction)

mine_transactions("Miner{}".format(0))

# 打印区块链信息
blockchain.print_chain()
