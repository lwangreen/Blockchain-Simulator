from Node import Node
import time

global current_time

def is_node_contain(node_id):
    return any(node_id == node.id for node in nodes_list)


def get_node(node_id):
    for node in nodes_list:
        if node.id == node_id:
            return node


def create_node(node_id):
    global nodes_list

    if not is_node_contain(node_id):
        nodes_list.append(Node(node_id))


def retrieve_records(records):
    global current_time
    global time_interval
    c_list = []

    while(records):
        if records[0][-1] >= current_time+time_interval:
            break
        c_list.append(records.pop(0))
    if c_list:
        return c_list
    return None


# node1, node2, time
contacts = [[1, 2, 200],
            [3, 2, 200],
            [3, 2, 600],
            [2, 4, 1000],
            [1, 3, 1500]
            ]

# node1, node2, transaction amount, time
transactions = [[1, 2, 500, 172],
            [3, 2, 700, 200],
            [1, 3, 200, 650],
            [2, 4, 130, 780],
            [4, 1, 50, 1000],
            [3, 1, 100, 1200],
            [4, 3, 600, 1500]]

nodes_list = []

current_time = 0
time_interval = 600


while current_time < 2000:
    print("time", current_time)
    current_contacts = retrieve_records(contacts)
    current_transactions = retrieve_records(transactions)
    print("contact", current_contacts)
    print("transactions", current_transactions)
    if current_transactions:
        for t in current_transactions:
            print(t)
            create_node(t[0])
            create_node(t[1])
            node1 = get_node(t[0])
            node1.blockchain.new_transaction(t[0], t[1], t[2], t[3])

    if current_contacts:
        for c in current_contacts:
            create_node(c[0])
            create_node(c[1])
            node1 = get_node(c[0])
            node2 = get_node(c[1])
            node1.broadcast_transactions(node2)
            node2.broadcast_transactions(node1)

    time.sleep(1)

    current_time += time_interval

for node in nodes_list:
    print('ID:', node.id, node.blockchain.incomplete_transactions)
    print(node.blockchain.chain)