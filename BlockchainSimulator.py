import time
import os
import mysql.connector
from Node import Node


def is_node_contain(node_id, nodes_list):
    return any(node_id == node.id for node in nodes_list)


def get_node(node_id, nodes_list):
    for node in nodes_list:
        if node.id == node_id:
            return node


def create_node(node_id, nodes_list):
    if not is_node_contain(node_id, nodes_list):
        nodes_list.append(Node(node_id))
    return nodes_list


def retrieve_contact_from_data_trace(cur, current_time):
    cur.execute("select start_time, id1, id2, end_time from contactsrep2 where start_time > %d order by start_time limit 1000;", current_time)
    contacts = cur.fetchall()
    return contacts


def retrieve_records(records, current_time, time_interval):
    c_list = []

    while records:
        if records[0][0] >= current_time+time_interval:
            break
        c_list.append(records.pop(0))
    if c_list:
        return c_list
    return None


def write_transactions_into_file(f, transactions):
    for t in transactions:
        f.write(str(t) + "\n")


def write_blocks_into_file(f, blocks):
    """
    Write each block of a node into file
    :param f: file instance
    :param blocks: the blockchain of a node
    :return: None
    """
    for block in blocks:
        for keyword in block:
            if keyword != 'transactions':
                f.write(keyword+": "+str(block[keyword])+"\n")
            else:
                write_transactions_into_file(f, block['transactions'])
        f.write("\n")


def write_into_file(filename, nodes_list):
    """
    Write final blockchain information of all nodes into a file
    :param filename: the name of the file that blockchain information is stored into
    :param nodes_list: all nodes
    :return: None
    """
    file_path = os.getcwd()+"\\Log\\"
    if not os.path.exists(file_path):
        os.makedirs(file_path)

    f = open(file_path+filename, 'w+')
    for node in nodes_list:
        f.write("Node ID:"+str(node.id)+"\n")
        f.write("Incomplete transaction:"+"\n")
        write_transactions_into_file(f, node.blockchain.incomplete_transactions)
        f.write("\n")
        f.write("Blockchain:"+"\n")
        write_blocks_into_file(f, node.blockchain.chain)

        f.write("\n")
    f.close()


def get_end_time(cur):
    cur.execute("select end_time from contactsrep2 order by end_time desc limit 1;")
    d = cur.fetchall()
    return d[0][0]


def main():
    # # node1, node2, time
    # contacts = [[1, 2, 200],
    #         [3, 2, 200],
    #         [3, 2, 600],
    #         [2, 4, 1000],
    #         [1, 3, 1500]
    #         ]
    #
    # # payer, payee, transaction amount, time
    # transactions = [[1, 2, 500, 172],
    #             [3, 2, 700, 200],
    #             [1, 3, 200, 650],
    #             [2, 4, 130, 780],
    #             [4, 1, 50, 1000],
    #             [3, 1, 100, 1200],
    #             [4, 3, 600, 1500]]
    nodes_list = []
    current_time = 0
    time_interval = 600

    end_time = get_end_time(cur)

    cnx = mysql.connector.connect(user='root', database='cambridge')
    cur = cnx.cursor(buffered=True)

    while current_time < end_time:
        current_contacts = retrieve_contact_from_data_trace(current_time)

        
        current_contacts = retrieve_records(current_contacts, current_time, time_interval)
        current_transactions = retrieve_records(transactions, current_time, time_interval)

        if current_transactions:
            for t in current_transactions:
                nodes_list = create_node(t[0], nodes_list)
                nodes_list = create_node(t[1], nodes_list)
                node1 = get_node(t[0], nodes_list)
                transaction = {
                    'sender': t[0],
                    'recipient': t[1],
                    'amount': t[2],
                    'timestamp': t[3],
                }
                node1.blockchain.new_transaction(transaction)

        if current_contacts:
            for c in current_contacts:
                nodes_list = create_node(c[0], nodes_list)
                nodes_list = create_node(c[1], nodes_list)
                node1 = get_node(c[0], nodes_list)
                node2 = get_node(c[1], nodes_list)
                node1.blockchain.resolve_conflicts(node2.blockchain)
                node2.blockchain.resolve_conflicts(node1.blockchain)

                node1.broadcast_transactions(node2)
                node2.broadcast_transactions(node1)

        time.sleep(1)

        current_time += time_interval

    print("end")

    write_into_file("testresult.txt", nodes_list)


if __name__ == "__main__":
    main()
