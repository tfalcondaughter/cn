import socket as s
import time as t

server_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
host = s.gethostname()
port = 1111
server_socket.bind((host, port))
server_socket.listen(5)

my_set = {('cat_weight', 'int', 5), ('dog_weight', 'int', 10), ('elephant_weight', 'int', 500)}


def commands(server_set, client_text, command):
    if command == 'PRINT':
        for set_list in server_set:
            if client_text == set_list[0]:
                client_socket.send(set_list[0].encode('ascii'))
                client_socket.send(set_list[1].encode('ascii'))
                client_socket.send(str(set_list[2]).encode('ascii'))
    elif command == 'GET_OBJECTS_NAMES':
        for set_list in server_set:
            print(set_list[0])


e = b'no'
while e.decode('ascii') != 'exit':
    client_socket, address = server_socket.accept()
    print("Connected with:", address[0], "address:", address[1])
    currentTime = t.ctime(t.time()) + '\n'
    client_socket.send(currentTime.encode('ascii'))
    e = client_socket.recv(1024)
    text = client_socket.recv(1024)
    commands(my_set, text.decode('ascii'), e.decode('ascii'))
    client_socket.close()
