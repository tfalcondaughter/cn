import random
import socket as s
import threading as th
import time as t

import pandas as pd

server_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
server_socket.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
host = s.gethostname()
port = 1032
server_socket.bind((host, port))
print('waiting for clients...')

file = pd.read_csv('cn.csv', dtype={'code': 'str', 'name': 'str', 'type': 'str', 'value': 'str'})


def journal(c_idc, c_time, status):
    with open('journal.txt', 'a') as j:
        j.write('client ' + str(c_idc) + ' ' + status + ' on ' + c_time + '\n')


def personal_code(in_code, c_socket):
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
        c_socket.send(new_code.encode('ascii'))
        return None, new_code
    else:
        if not file[file.code == in_code].empty:
            client_set = file[file.code == in_code]
            return client_set, in_code


def commands(server_set, command, in_code, c_socket):
    global file
    if command == 'PRINT':
        c_socket.send('valid command'.encode('ascii'))
        c_print(server_set, c_socket)
    elif command == 'GET_NAMES':
        c_socket.send('valid command'.encode('ascii'))
        c_get(server_set, c_socket)
    elif command == 'CREATE':
        c_socket.send('valid command'.encode('ascii'))
        c_create(in_code, c_socket)
    elif command == 'CHANGE':
        c_socket.send('valid command'.encode('ascii'))
        c_change(in_code, c_socket)
    elif command == 'Who':
        c_socket.send('valid command'.encode('ascii'))
        who(c_socket)
    else:
        if command != 'EXIT' and command != 'EXIT_CLIENT':
            c_socket.send('invalid command'.encode('ascii'))


def c_check_type(c_type, c_value, c_socket):
    check = True
    try:
        if c_type == "int":
            int(c_value)
        elif c_type == "float":
            float(c_value)
        elif c_type == "str":
            str(c_value)
        elif c_type == "bool":
            bool(c_value)
        elif c_type == "complex":
            complex(c_value)
        else:
            check = False
            c_socket.send("server does not support that type".encode('ascii'))
    except ValueError:
        check = False
        c_socket.send("your value does not match the type".encode('ascii'))
    else:
        c_socket.send("fine".encode('ascii'))
    return check


def c_print(server_set, c_socket):
    in_name = c_socket.recv(1024).decode('ascii')
    if not server_set[server_set.name == in_name].empty:
        for i in server_set.itertuples():
            name = ''.join(map(str, i[2]))
            type = ''.join(map(str, i[3]))
            value = ''.join(map(str, i[4]))
            c_socket.send(name.encode('ascii'))
            c_socket.send(type.encode('ascii'))
            c_socket.send(value.encode('ascii'))


def c_get(server_set, c_socket):
    number = len(server_set.index)
    c_socket.send(str(number).encode('ascii'))
    for i in server_set.itertuples():
        name = ''.join(map(str, i[2]))
        c_socket.send(name.encode('ascii'))


def c_create(in_code, c_socket):
    global file
    name = c_socket.recv(1024).decode('ascii')
    type = c_socket.recv(1024).decode('ascii')
    value = c_socket.recv(1024).decode('ascii')
    check = c_check_type(type, value, c_socket)
    if check:
        new_row = pd.DataFrame([[in_code, name, type, value]], columns=['code', 'name', 'type', 'value'])
        file = file.append(new_row, ignore_index=True)


def c_change(in_code, c_socket):
    global file
    in_name = c_socket.recv(1024).decode('ascii')
    file = file[file.name != in_name]
    new_name = c_socket.recv(1024).decode('ascii')
    new_type = c_socket.recv(1024).decode('ascii')
    new_value = c_socket.recv(1024).decode('ascii')
    check = c_check_type(new_type, new_value, c_socket)
    if check:
        new_row = pd.DataFrame([[in_code, new_name, new_type, new_value]], columns=['code', 'name', 'type', 'value'])
        file = file.append(new_row, ignore_index=True)


def who(c_socket):
    c_socket.send('Written by Tetiana Sokolova, K-23. 7: <Name,type,value>.'.encode('ascii'))


def rewrite():
    global file
    with open('cn.csv', 'w') as f:
        f.write('code,name,type,value\n')
        for i in file.itertuples():
            f.write(''.join(map(str, i[1])) + ',' + ''.join(map(str, i[2])) + ',' + ''.join(
                map(str, i[3])) + ',' + ''.join(map(str, i[4])) + '\n')


def client(c_e, c_socket, c_address):
    try:
        journal(c_address, currentTime, 'joined')
        while True:
            input_code = c_socket.recv(1024).decode('ascii')
            new = input_code
            client_set, code = personal_code(input_code, c_socket)
            if (client_set is None) and (new != 'new'):
                c_socket.send("stop".encode('ascii'))
                c_socket.send("There is no such code.".encode('ascii'))
                continue
            else:
                c_socket.send("go".encode('ascii'))
            while c_e != 'EXIT_CLIENT'.encode('ascii'):
                c_e = c_socket.recv(1024)
                if c_e == 'EXIT'.encode('ascii'):
                    rewrite()
                    break
                commands(client_set, c_e.decode('ascii'), code, c_socket)
                client_set = file[file.code == code]
            else:
                c_e = 'new_it'
                c_socket.send("go".encode('ascii'))
            if c_e == 'EXIT'.encode('ascii'):
                break
        journal(c_address, t.ctime(t.time()), 'disconnected')
        c_socket.close()
        print(f'client {c_address} disconnected')
    except ConnectionResetError as c_r_e:
        print('something went wrong:', c_r_e)
    except ConnectionError as c_e_e:
        print('something went wrong:', c_e_e)


while True:
    try:
        server_socket.listen(1)
        e = 'go'
        client_socket, address = server_socket.accept()
        c_id = int(t.time())
        print("Connected with:", address[0], "address:", address[1], "id:", str(c_id))
        currentTime = t.ctime(t.time())
        client_socket.send((currentTime + '\n').encode('ascii'))
        th.Thread(target=client, args=(e, client_socket, c_id)).start()
    except ConnectionResetError as c_r:
        print('something went wrong:', c_r)
    except ConnectionError as c_e:
        print('something went wrong:', c_e)
