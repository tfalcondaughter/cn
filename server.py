import random
import socket as s
import time as t

import pandas as pd

server_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
host = s.gethostname()
port = 1111
server_socket.bind((host, port))
server_socket.listen(5)

file = pd.read_csv('cn.csv', dtype={'code': 'str', 'name': 'str', 'type': 'str', 'value': 'str'})


def personal_code(in_code):
    code_existence = True
    if in_code == 'new':
        new_code = None
        while code_existence:
            new_code = str(int(random.uniform(0, 9))) + str(int(random.uniform(0, 9))) + str(
                int(random.uniform(0, 9))) + str(int(random.uniform(0, 9))) + str(int(random.uniform(0, 9))) + str(
                int(random.uniform(0, 9)))
            if not file[file.code == new_code].empty:
                code_existence = True
            else:
                code_existence = False
        global code
        code = new_code
        client_socket.send(new_code.encode('ascii'))
    else:
        if not file[file.code == in_code].empty:
            client_set = file[file.code == in_code]
            return client_set


def commands(server_set, command, in_code):
    if command == 'PRINT':
        in_name = client_socket.recv(1024).decode('ascii')
        if not server_set[server_set.name == in_name].empty:
            for i in server_set.itertuples():
                name = ''.join(map(str, i[2]))
                type = ''.join(map(str, i[3]))
                value = ''.join(map(str, i[4]))
                client_socket.send(name.encode('ascii'))
                client_socket.send(type.encode('ascii'))
                client_socket.send(value.encode('ascii'))
    elif command == 'GET_OBJECTS_NAMES':
        number = len(server_set.index)
        client_socket.send(str(number).encode('ascii'))
        for i in server_set.itertuples():
            name = ''.join(map(str, i[2]))
            client_socket.send(name.encode('ascii'))
    elif command == 'CREATE':
        with open('cn.csv', 'a') as f:
            f.write('\n' + in_code + ',' + client_socket.recv(1024).decode('ascii') + ',' +
                    client_socket.recv(1024).decode('ascii') + ',' + client_socket.recv(1024).decode('ascii'))
        f.close()
    elif command == 'CHANGE':
        in_name = client_socket.recv(1024).decode('ascii')
        save_f = file[file.name != in_name]
        with open('cn.csv', 'w') as f:
            f.write('code,name,type,value\n')
            for i in save_f.itertuples():
                f.write(''.join(map(str, i[1])) + ',' + ''.join(map(str, i[2])) + ',' + ''.join(
                    map(str, i[3])) + ',' + ''.join(map(str, i[4])) + '\n')
            f.write(in_code + ',' + in_name + ',' + client_socket.recv(1024).decode(
                'ascii') + ',' + client_socket.recv(
                1024).decode('ascii'))
            f.close()


while True:
    client_socket, address = server_socket.accept()
    print("Connected with:", address[0], "address:", address[1])
    currentTime = t.ctime(t.time()) + '\n'
    client_socket.send(currentTime.encode('ascii'))
    code = client_socket.recv(1024).decode('ascii')
    e = 'go'
    while e != "EXIT".encode('ascii'):
        file = pd.read_csv('cn.csv', dtype={'code': 'str', 'name': 'str', 'type': 'str', 'value': 'str'})
        client_set = personal_code(code)
        if client_set is None:
            client_socket.send("stop".encode('ascii'))
            client_socket.send("There is no such code.".encode('ascii'))
        else:
            client_socket.send("go".encode('ascii'))
            e = client_socket.recv(1024)
            commands(client_set, e.decode('ascii'), code)
    client_socket.close()
