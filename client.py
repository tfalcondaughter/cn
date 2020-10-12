import socket as s

# Контейнер іменованих об'єктів.
# На сервері зберігаються іменовані об'єкти клієнтів: цілі числа, символьні рядки тощо. Для зберігання/зміни на сервері
# об'єкта потрібно передати трійку <Ім'я; Тип; Значення>. Для зчитування потрібне лише ім'я, а сервер має дати відповідь
# трійкою <Ім'я; Тип; Значення>. Клієнт може зчитати, змінити та отримати перелік імен об'єктів.

S = s.socket(s.AF_INET, s.SOCK_STREAM)
host = s.gethostname()
port = 1111
S.connect((host, port))
print("Connected to server on:", S.recv(1024).decode('ascii'))

command = input("Enter a command: ")
S.send(command.encode('ascii'))
if command == 'PRINT':
    text = input("Which object: ")
    S.send(text.encode('ascii'))
    a = S.recv(1024)
    b = S.recv(1024)
    c = S.recv(1024)
    print(a.decode('ascii'), ';', b.decode('ascii'), ';', c.decode('ascii'))

S.close()
