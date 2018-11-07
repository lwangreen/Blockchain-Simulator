import hashlib
import json



class Blockchain:
    def __init__(self):
        self.chain = []
        self.nonce = 0
        self.incomplete_transactions = []
        self.FLAG_MINING = True
        self.create_unsolved_block([], None)

    def reinitialise_for_next_block(self):
        self.nonce = 0
        self.unsolved_block = {}
        self.create_unsolved_block([], self.hash(self.chain[-1]))

    def create_unsolved_block(self, incomplete_transactions, previous_hash):
        self.unsolved_block = {
            'index': len(self.chain) + 1,
            'transactions': incomplete_transactions,
            'proof': self.nonce,
            'previous_hash': previous_hash,
        }

    def new_block(self):
        """
        Create a new Block in the Blockchain
        :param previous_hash: (Optional) <str> Hash of previous Block
        :return: <dict> New Block
        """

        self.chain.append(self.unsolved_block)
        self.reinitialise_for_next_block()

    def hash(self, block):
        """
        Creates a SHA-256 hash of a Block
        :param block: <dict> Block
        :return: <str>
        """

        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def new_transaction(self, sender, recipient, amount, timestamp):
        """
        Creates a new transaction to go into the next mined Block
        :param sender: <str> Address of the Sender
        :param recipient: <str> Address of the Recipient
        :param amount: <int> Amount
        :return: <int> The index of the Block that will hold this transaction
        """

        self.incomplete_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
            'timestamp': timestamp,
        })
        self.unsolved_block['transactions'] = self.incomplete_transactions.copy()
    def proof_of_work(self):
        """
        Simple Proof of Work Algorithm:
         - Find a number p' such that hash(pp') contains leading 4 zeroes, where p is the previous p'
         - p is the previous proof, and p' is the new proof
        :param last_proof: <int>
        :return: <int>
        """

        while self.FLAG_MINING:
            while self.valid_proof(self.unsolved_block) is False:
                self.nonce += 1
                self.unsolved_block['proof'] = self.nonce
            if self.FLAG_MINING:
                self.new_block()
                self.reinitialise_for_next_block()
                self.incomplete_transactions = []

    def valid_proof(self, block):
        """
        Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeroes?
        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :return: <bool> True if correct, False if not.
        """

        return self.hash(block)[:4] == "0000"

    def valid_chain(self):
        """
        Determine if a given blockchain is valid
        :param chain: <list> A blockchain
        :return: <bool> True if valid, False if not
        """

        previous_block = self.chain[0]
        current_index = 0

        while current_index < len(self.chain):
            block = self.chain[current_index]
            print(f'{previous_block}')
            print(f'{block}')
            print("\n-----------\n")
            # Check that the hash of the block is correct

            if current_index != 0:
                if block['previous_hash'] != self.hash(previous_block):
                    return False

            # Check that the Proof of Work is correct
            if not self.valid_proof(block):
                return False

            previous_block = block
            current_index += 1

        return True

    def resolve_conflicts(self, other_node):
        """
        This is our Consensus Algorithm, it resolves conflicts
        by replacing our chain with the longest one in the network.
        :return: <bool> True if our chain was replaced, False if not
        """

        # Check if the length is longer and the chain is valid
        if len(other_node.chain) > len(self.chain) and self.valid_chain(other_node.chain):
            self.chain = other_node.chain.copy()
            return True

        return False
