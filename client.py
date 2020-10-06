import socket as s

S = s.socket(s.AF_INET, s.SOCK_STREAM)
host = s.gethostname()
port = 1111
S.connect((host, port))
print("Connected to server on:%s" % S.recv(1024).decode('ascii'))
S.close()
