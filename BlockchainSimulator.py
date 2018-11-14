import threading
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
    cur.execute("select start_time, id1, id2, end_time from contactsrep2 where start_time > %s order by start_time limit 1000;" % (current_time))
    contacts = cur.fetchall()
    return contacts


def retrieve_transaction_from_file(f, end_time):
    transactions = []
    t = f.readline()
    t = t.split()
    while int(t[0]) < end_time:
        transactions.append([int(t[i]) for i in range(len(t))])
        t = f.readline()
        t = t.split()
    transactions.append([int(t[i]) for i in range(len(t))])
    #print("Time concern", end_time, transactions[-1][0])
    return transactions


def retrieve_transaction_records(records, current_time, time_interval):
    c_list = []

    while records:
        if records[0][0] >= current_time+time_interval:
            break
        c_list.append(records.pop(0))
    if c_list:
        return c_list
    return None


def retrieve_contact_records(records, current_time, time_interval):
    c_list = []
    index = 0
    while index < len(records):
        if records[index][0] >= current_time+time_interval:
            break
        if records[index][-1] < current_time+time_interval:
            c_list.append(records.pop(index))
            index -= 1
        else:
            c_list.append(records[index])

        index += 1
    if c_list:
        return c_list


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
        f.write("-------------Incomplete transaction----------------:"+"\n")
        write_transactions_into_file(f, node.blockchain.incomplete_transactions)
        f.write("\n")
        f.write("-------------Blockchain:---------------------------:"+"\n")
        write_blocks_into_file(f, node.blockchain.chain)

        f.write("-------------------------------------------------------------------------------------\n")
        f.write("\n")
    f.close()


def get_end_time(cur):
    cur.execute("select end_time from contactsrep2 order by end_time desc limit 1;")
    d = cur.fetchall()
    return d[0][0]


def main():
    nodes_list = []
    current_contacts = []
    current_transactions = []
    current_time = 0
    time_interval = 600

    cnx = mysql.connector.connect(user='root', database='cambridge')
    cur = cnx.cursor(buffered=True)
    #end_time = 10000
    end_time = get_end_time(cur)
    #print("endtime", end_time)
    f = open(os.getcwd()+"\\Created_data_trace\\transaction.txt", 'r')

    while current_time <= end_time:
        if not current_contacts:
            current_contacts = retrieve_contact_from_data_trace(cur, current_time)
        current_period_end_time = current_contacts[-1][0]

        if not current_transactions:
            current_transactions = retrieve_transaction_from_file(f, current_period_end_time)
        
        current_contacts_within_time_interval = retrieve_contact_records(current_contacts, current_time, time_interval)
        current_transactions_within_time_interval = retrieve_transaction_records(current_transactions, current_time, time_interval)
        #print(current_contacts_within_time_interval)
        #print(current_transactions_within_time_interval)

        if current_transactions_within_time_interval:
            for t in current_transactions_within_time_interval:

                nodes_list = create_node(t[1], nodes_list)
                nodes_list = create_node(t[2], nodes_list)
                node1 = get_node(t[1], nodes_list)
                transaction = {
                    'sender': t[1],
                    'recipient': t[2],
                    'amount': t[3],
                    'timestamp': t[0],
                }
                node1.blockchain.new_transaction(transaction)

        if current_contacts_within_time_interval:
            for c in current_contacts_within_time_interval:

                nodes_list = create_node(c[1], nodes_list)
                nodes_list = create_node(c[2], nodes_list)
                node1 = get_node(c[1], nodes_list)
                node2 = get_node(c[2], nodes_list)

                node1.blockchain.resolve_conflicts(node2.blockchain)
                node2.blockchain.resolve_conflicts(node1.blockchain)
                #node1_resolve_conflict_thread = threading.Thread(target=node1.blockchain.resolve_conflicts, args=[node2.blockchain])
                #node2_resolve_conflict_thread = threading.Thread(target=node2.blockchain.resolve_conflicts, args=[node1.blockchain])
                #node1_resolve_conflict_thread.start()
                #node2_resolve_conflict_thread.start()


                node1.blockchain.broadcast_transactions(node2.blockchain)
                node2.blockchain.broadcast_transactions(node1.blockchain)


        current_time += time_interval
        print(current_time, len(nodes_list))

    print("end")
    #nodes_list.sort()
    write_into_file("BlockchainResult.txt", nodes_list)


if __name__ == "__main__":
    main()
