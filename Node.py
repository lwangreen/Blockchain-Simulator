from Blockchain import Blockchain
import threading


class Node:
    def __init__(self, id):
        """
        :param id:
        """
        self.id = id
        self.blockchain = Blockchain()
        self.account_balance = 0
        self.mining_thread = None

    def start_mining_thread(self):
        self.blockchain.FLAG_MINING = True
        self.mining_thread = threading.Thread(target = self.blockchain.proof_of_work)
        self.mining_thread.start()

    def stop_mining_thread(self):
        self.blockchain.FLAG_MINING = False
        self.mining_thread.join()

    def broadcast_transactions(self, other_node):
        if other_node.blockchain.incomplete_transactions:
            #print("broadcast", self.id, other_node.id)
            self.stop_mining_thread()

            #print("before", self.blockchain.incomplete_transactions, other_node.blockchain.incomplete_transactions)
            for transaction in other_node.blockchain.incomplete_transactions:
              if not transaction in self.blockchain.incomplete_transactions:

                    self.blockchain.incomplete_transactions.append(transaction)
            #print("after", self.blockchain.incomplete_transactions, other_node.blockchain.incomplete_transactions)
            # reinitialise proof-of-work thread
            self.blockchain.unsolved_block['transactions'] = self.blockchain.incomplete_transactions.copy()
            self.start_mining_thread()
