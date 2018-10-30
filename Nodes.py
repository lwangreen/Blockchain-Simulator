import Blockchain
import hashlib

class Nodes:
    def __init__(self, myid):
        """

        :param myid:
        """
        self.myid = myid
        self.blockchain = Blockchain.Blockchain()
        self.incompleteTransactions = []

    def proof_of_work(self, lastBlock):
        """

        :param lastBlock:
        :return:
        """



