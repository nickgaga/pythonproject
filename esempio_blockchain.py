import hashlib
import time

class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        # Crea il blocco di genesi
        genesis_block = Block(0, "0", time.time(), "Blocco di genesi", self.calculate_hash("0"))
        self.chain.append(genesis_block)

    def add_block(self, data):
        # Aggiunge un nuovo blocco alla blockchain
        index = len(self.chain)
        previous_hash = self.chain[-1].hash
        timestamp = time.time()
        hash = self.calculate_hash(str(index) + previous_hash + str(timestamp) + data)
        new_block = Block(index, previous_hash, timestamp, data, hash)
        self.chain.append(new_block)

    def calculate_hash(self, data):
        # Calcola l'hash SHA-256 del blocco
        return hashlib.sha256(data.encode()).hexdigest()
