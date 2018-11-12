import random
import mysql.connector
import datetime as dt
import os


def choose_nodes(start, end):
    active = []
    i1 = ''
    i2 = ''
    ##    cur.execute("select distinct device_oid from devicespan where ((endtime<'%s' and endtime>='%s') or (starttime<'%s' and endtime>'%s')) group by device_oid order by count(*) desc limit 20;"  % (end, start, end, end))
    cur.execute(
        "select distinct id1 from contact where ((end_time<'%s' and end_time>='%s') or (start_time<'%s' and end_time>'%s'));" % (
        end, start, end, end))
    d = cur.fetchall()

    for i in d:
        active.append(i[0])
    # print(active)
    if (len(active) > 0):
        i1 = active[random.randint(0, len(active) - 1)]
        # print(i1)
        cur.execute("select distinct id2 from contactsrep2 where \
((end_time<'%s' and end_time>='%s') or (start_time<'%s' and end_time>'%s'));" % (
        end, start, end, end))
        d = cur.fetchall()

        for i in d:
            active.append(i[0])
        # print(len(active))
        i2 = active[random.randint(0, len(active) - 1)]
        while (i1 == i2):
            i1 = active[random.randint(0, len(active) - 1)]
            i2 = active[random.randint(0, len(active) - 1)]
            # print(i1, i2)
    return i1, i2


def get_end_time(cur):
    global end
    cur.execute("select end_time from contactsrep2 order by end_time desc limit 1;")
    d = cur.fetchall()
    return d[0][0]


def write_into_file(filename, nodes_list):
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


dur = 600       #Time flows by 600 secs a time
endtime = 0
time = 0
count = 0

cnx = mysql.connector.connect(user='root', database='cambridge')
cur = cnx.cursor(buffered=True)
endtime = get_end_time(cur)

while time < endtime:

    i1, i2 = choose_nodes(start, finish)