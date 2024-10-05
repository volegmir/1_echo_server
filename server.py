import socket  # Импортируем модуль socket для работы с сетевыми соединениями

# Запрашиваем у пользователя номер порта, на котором будет работать сервер
port = int(input("port:"))

# Создаем TCP/IP сокет
# socket.AF_INET означает, что будем использовать сетевой протокол IPv4
# socket.SOCK_STREAM означает, что будем использовать протокол TCP (потоковый)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Устанавливаем опцию сокета SO_REUSEADDR
# Это позволяет повторно использовать локальный адрес при повторном запуске сервера
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Привязываем сокет к указанному адресу и порту
# Пустая строка '' или '0.0.0.0' как адрес означает, что сервер будет принимать соединения на всех сетевых интерфейсах
sock.bind(('', port))

print("Server is starting")  # пункт 2.i выполнен

# Начинаем прослушивание входящих соединений
# Параметр 1 определяет максимальное число подключений в очереди (backlog)
sock.listen(1)
print("Port", port, "is listening")  # пункт 2.ii выполнен

# Метод accept() блокирует выполнение программы до установления входящего соединения
# После установления соединения возвращает новый сокет conn для общения с клиентом и адрес клиента addr
conn, addr = sock.accept()
print("Client is accepted")  # пункт 2.iii выполнен
print("Client address:", addr[0])  # Выводим IP-адрес клиента
print("Client port:", addr[1])     # Выводим порт клиента

# Инициализируем переменную msg для накопления полученных данных
msg = ''

# Основной цикл работы с клиентом
while True:
    # Получаем данные от клиента
    data = conn.recv(1024)
    if not data:
        # Если метод recv() вернул пустые данные, это означает, что клиент закрыл соединение
        print("All data is accepted")  # пункт 2.iv выполнен
        break
    # Декодируем полученные байты в строку
    msg += data.decode('utf-8')
    # Проверяем, есть ли в накопленных данных полное сообщение
    while '\n' in msg:
        # Разделяем данные по символу новой строки '\n'
        line, msg = msg.split('\n', 1)
        print(f"Received from client: {line}")  # Выводим полное сообщение от клиента
        if line.lower() == 'exit':
            # Если клиент отправил команду 'exit', завершаем работу с клиентом
            print("Exit command received. Closing connection.")
            # Отправляем подтверждение клиенту перед закрытием соединения
            conn.send("Server closing connection.\n".encode('utf-8'))
            break
        else:
            # Обрабатываем полученное сообщение
            # Для примера переведем строку в верхний регистр
            response = line.upper()
            # Отправляем ответ клиенту, добавляя символ '\n' в конце
            conn.send((response + '\n').encode('utf-8'))
            print("Response sent to client")  # Подтверждаем отправку ответа
    if line.lower() == 'exit':
        # Если была получена команда 'exit', выходим из внешнего цикла
        break

# После выхода из цикла закрываем соединение с клиентом
conn.close()
print("Connection is closed. Client is off")  # пункт 2.vi выполнен

# Закрываем главный серверный сокет
sock.close()
print("Server is off")  # пункт 2.vii выполнен