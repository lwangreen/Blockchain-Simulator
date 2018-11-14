from Blockchain import Blockchain


class Node:
    def __init__(self, id):
        """
        :param id:
        """
        self.id = id
        self.blockchain = Blockchain(id)
        self.account_balance = 0



