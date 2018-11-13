import random
import mysql.connector
import os


def get_nodes_from_data_trace():
    nodes_list = []
    cur.execute("select distinct id1 from contactsrep2;")
    d = cur.fetchall()
    for i in d:
        nodes_list.append(int(i[0]))

    cur.execute("select distinct id2 from contactsrep2;")
    d = cur.fetchall()
    for i in d:
        if i[0] not in nodes_list:
            nodes_list.append(int(i[0]))
    nodes_list.sort()
    return nodes_list


def choose_nodes(nodes_list):
    node1 = random.randint(0, len(nodes_list))
    node2 = random.randint(0, len(nodes_list))
    while node2 == node1:
        node2 = random.randint(0, len(nodes_list))
    return node1, node2


def get_end_time(cur):
    global end
    cur.execute("select end_time from contactsrep2 order by end_time desc limit 1;")
    d = cur.fetchall()
    return d[0][0]


def write_into_file(f, transaction_time, node1, node2, transaction_amount):
    f.write(str(transaction_time)+" "+str(node1)+" "+str(node2)+" "+str(transaction_amount)+"\n")


def generate_nodes_transaction():
    node1, node2 = choose_nodes(nodes_list)
    transaction_amount = random.randint(0, 9999)
    return node1, node2, transaction_amount


dur = 600       # Time flows by 600 secs a time
endtime = 0
time = 0
count = 0

file_path = os.getcwd() + "\\Created_data_trace\\"
if not os.path.exists(file_path):
    os.makedirs(file_path)

f = open(file_path+"transaction.txt", 'w+')

cnx = mysql.connector.connect(user='root', database='cambridge')
cur = cnx.cursor(buffered=True)
endtime = get_end_time(cur)
nodes_list = get_nodes_from_data_trace()
count = 0

while time < endtime:
    time_elapse = random.randint(0, 600)
    time += time_elapse

    node1, node2, transaction_amount = generate_nodes_transaction()
    write_into_file(f, time, node1, node2, transaction_amount)
    repeat = random.random()
    count += 1

    while repeat > 0.9:
        node1, node2, transaction_amount = generate_nodes_transaction()
        write_into_file(f, time, node1, node2, transaction_amount)
        repeat = random.random()
        count += 1

f.close()
print(count)
