import socket as s

# 7. Контейнер іменованих об'єктів.
# На сервері зберігаються іменовані об'єкти клієнтів: цілі числа, символьні рядки тощо. Для зберігання/зміни на сервері
# об'єкта потрібно передати трійку <Ім'я; Тип; Значення>. Для зчитування потрібне лише ім'я, а сервер має дати відповідь
# трійкою <Ім'я; Тип; Значення>. Клієнт може зчитати, змінити та отримати перелік імен об'єктів.

S = s.socket(s.AF_INET, s.SOCK_STREAM)
host = s.gethostname()
port = 1111
S.connect((host, port))
print("Connected to server on:", S.recv(1024).decode('ascii'))

code = input("Enter your personal code or write 'new' if you don't have one: ")
S.send(code.encode('ascii'))
if code == 'new':
    print("Your new code is now: ", end='')
    print(S.recv(1024).decode('ascii'))

if S.recv(1024).decode('ascii') == "stop":
    print(S.recv(1024).decode('ascii'))
    S.close()

command = input("Enter a command: ")
S.send(command.encode('ascii'))
if command == 'PRINT':
    name = input("Enter name: ")
    S.send(name.encode('ascii'))
    a = S.recv(1024)
    b = S.recv(1024)
    c = S.recv(1024)
    print(a.decode('ascii'), ';', b.decode('ascii'), ';', c.decode('ascii'))
elif command == 'GET_OBJECTS_NAMES':
    number = int(S.recv(1024).decode('ascii'))
    for i in range(number):
        print(S.recv(1024).decode('ascii'))
elif command == 'CREATE':
    name = input("Enter name: ")
    S.send(name.encode('ascii'))
    type = input("Enter type: ")
    S.send(type.encode('ascii'))
    value = input("Enter value: ")
    S.send(value.encode('ascii'))
S.close()
