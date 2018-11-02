import Blockchain
from Blockchain import Blockchain
import Threads


class Nodes:
    def __init__(self, myid):
        """

        :param myid:
        """
        self.myid = myid
        self.blockchain = Blockchain()
        self.account_balance = 0
        self.incomplete_transactions = []
        self.mining_thread = Threads.NodeThread("self.blockchain.proof_of_work")

    def add_new_block(self):
        self.blockchain.new_block(self.incomplete_transactions)
        self.incomplete_transactions = []

    def new_transaction(self, sender, recipient, amount):
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
        })

        return self.blockchain.last_block['index'] + 1

    def broadcast_transactions(self, other_node):
        for transaction in self.incomplete_transactions:
            other_node.incompleteTransactions.append(transaction)

