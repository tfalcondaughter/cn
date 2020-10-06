import socket as s
import time as t

server_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
host = s.gethostname()
port = 1111
server_socket.bind((host, port))
server_socket.listen()

if True:
    client_socket, address = server_socket.accept()
    print("Connected with[address],[port]%s" % str(address))
    currentTime = t.ctime(t.time()) + "\r\n"
    client_socket.send(currentTime.encode('ascii'))
    client_socket.close()
