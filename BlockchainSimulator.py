from Nodes import Nodes

def is_node_contain(node_id):
    return any(node_id == node.myid for node in nodes_list)

def retrieve_contacts():
    global time
    global time_interval
    global contacts
    c_list = []

    while(contacts):
        if contacts[0][2] >= time+time_interval:
            break
        c_list.append(contacts.pop(0))
    if c_list:
        return c_list
    return None


contacts = [[1, 2, 200],
            [3, 2, 200],
            [3, 2, 600],
            [2, 4, 1000],
            [1, 3, 1500]
            ]

transactions = [[1, 2, 500, 172],
            [3, 2, 700, 200],
            [1, 3, 200, 650],
            [2, 4, 130, 780],
            [4, 1, 50, 1000],
            [3, 1, 100, 1200],
            [4, 3, 600, 1500]]

node_id_list = []
nodes_list = []

time = 0
time_interval = 600


while(time<2000):
    print("time", time)
    current_contact = retrieve_contacts()
    if current_contact:
        for c in current_contact:
            node1_id = c[0]
            node2_id = c[1]
            if(not is_node_contain(node1_id)):
                nodes_list.append(Nodes(node1_id))
            if(not is_node_contain(node2_id)):
                nodes_list.append(Nodes(node2_id))

    time += time_interval

for n in nodes_list:
    print(n.myid)