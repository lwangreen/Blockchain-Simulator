from Blockchain import Blockchain

class Node:
    def __init__(self, id):
        """
        :param id:
        """
        self.id = id
        self.blockchain = Blockchain(id)
        self.account_balance = 0


    def broadcast_transactions(self, other_node):
        if other_node.blockchain.incomplete_transactions:
            # print("before", self.blockchain.incomplete_transactions, other_node.blockchain.incomplete_transactions)
            for transaction in other_node.blockchain.incomplete_transactions:
              if not transaction in self.blockchain.incomplete_transactions:

                    self.blockchain.new_transaction(transaction)
            # print("after", self.blockchain.incomplete_transactions, other_node.blockchain.incomplete_transactions)
            # reinitialise proof-of-work thread
