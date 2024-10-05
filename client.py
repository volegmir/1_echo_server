import socket  # Импортируем модуль socket для работы с сетевыми соединениями

# Запрашиваем у пользователя адрес сервера и номер порта
host = input("host:")  # Например, 'localhost' или '127.0.0.1'
port = int(input("port:"))

# Создаем TCP/IP сокет
# socket.AF_INET указывает, что используем IPv4
# socket.SOCK_STREAM указывает, что используем протокол TCP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Устанавливаем блокирующий режим сокета (по умолчанию блокирующий)
# sock.setblocking(1)  # Эта строка необязательна и оставлена для информации

# Устанавливаем соединение с сервером по указанному адресу и порту
sock.connect((host, port))
print("Connected to server")  # пункт 4.i выполнен

# Инициализируем переменную для накопления полученных данных
received_data = ''

# Основной цикл для отправки сообщений на сервер
while True:
    # Запрашиваем у пользователя сообщение для отправки на сервер
    msg = input("Your string (type 'exit' to quit):")
    # Отправляем сообщение серверу, добавляя символ '\n' в конце для обозначения конца сообщения
    sock.send((msg + '\n').encode('utf-8'))
    print("Message sent to server")  # пункт 4.iii выполнен

    # Инициализируем переменную для хранения полного ответа от сервера
    full_response = ''
    # Получаем ответ от сервера
    while True:
        data = sock.recv(1024)
        if not data:
            # Если получили пустые данные, значит соединение закрыто
            break
        # Декодируем полученные байты и добавляем к накопленной строке
        received_data += data.decode('utf-8')
        # Проверяем, есть ли в накопленных данных полный ответ
        if '\n' in received_data:
            # Разделяем данные по символу новой строки '\n'
            line, received_data = received_data.split('\n', 1)
            full_response = line
            break  # Выходим из цикла ожидания ответа
    print("Message received from server")  # пункт 4.iv выполнен
    print(full_response)  # Выводим ответ от сервера

    # Если мы отправили 'exit', завершаем цикл
    if msg.lower() == 'exit':
        break  # Выходим из цикла отправки сообщений

# После выхода из цикла закрываем соединение с сервером
sock.close()
print("Connection closed to server")  # пункт 4.ii выполнен