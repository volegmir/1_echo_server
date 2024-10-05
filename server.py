import socket  # Импортируем модуль socket для работы с сетевыми соединениями

# Запрашиваем у пользователя номер порта и преобразуем его в целое число
port = int(input("port:"))

# Создаем новый сокет
sock = socket.socket()

# Устанавливаем опцию сокета SO_REUSEADDR, чтобы можно было повторно использовать адрес
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Привязываем сокет к указанному порту на всех доступных интерфейсах (пустая строка означает любой доступный адрес)
sock.bind(('', port))

print("Server is starting") # пункт 2.i выполнен

# Начинаем прослушивание входящих соединений (0 означает максимально возможное количество соединений)
sock.listen(0)
print("Port", port, "is listing") # пункт 2.ii выполнен

# Принимаем входящее соединение. conn - новый сокет для общения с клиентом, addr - адрес клиента
conn, addr = sock.accept()
print("Client is accepted") # пункт 2.iii выполнен
print("Client adress:", addr[0])  # Выводим IP-адрес клиента
print("Client port:", addr[1])    # Выводим порт клиента

msg = ''  # Инициализируем пустую строку для хранения полученного сообщения

while True:
    # Получаем данные от клиента (не более 1024 байт за раз)
    data = conn.recv(1024)
    if not data:   # Если данных больше нет, выходим из цикла
        print("All data is accepted") # пункт 2.iv выполнен
        break
    msg += data.decode()  # Декодируем полученные данные и добавляем к сообщению
    # Отправляем обратно клиенту полученное сообщение в верхнем регистре
    conn.send(msg.upper().encode())
    print("Message to client is sent") # пункт 2.v выполнен

print(msg)  # Выводим полное полученное сообщение

conn.close()  # Закрываем соединение с клиентом
print("Connection is closed. Client is off") # пункт 2.vi выполнен
print("Server is off") # пункт 2.vii выполнен
