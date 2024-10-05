import socket  # Импортируем модуль socket для работы с сетевыми соединениями

# Функция для безопасного ввода адреса хоста с значением по умолчанию
def get_host():
    host_input = input("Введите адрес хоста [по умолчанию 'localhost']: ")
    if not host_input.strip():
        return 'localhost'
    else:
        return host_input

# Функция для безопасного ввода номера порта с значением по умолчанию
def get_port():
    while True:
        try:
            port_input = input("Введите номер порта [по умолчанию 12345]: ")
            if not port_input.strip():
                port = 12345
            else:
                port = int(port_input)
            if 1 <= port <= 65535:
                return port
            else:
                print("Пожалуйста, введите номер порта от 1 до 65535.")
        except ValueError:
            print("Некорректный ввод. Пожалуйста, введите числовое значение номера порта.")

# Получаем адрес хоста и порт от пользователя
host = get_host()
port = get_port()

# Создаем TCP/IP сокет
# socket.AF_INET означает, что будем использовать протокол IPv4
# socket.SOCK_STREAM означает, что будем использовать протокол TCP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Устанавливаем блокирующий режим сокета (по умолчанию он уже блокирующий)
# sock.setblocking(1)  # Эта строка необязательна и оставлена для информации

# Устанавливаем соединение с сервером по указанному адресу и порту
try:
    sock.connect((host, port))
    print("Connected to server")  # пункт 4.i выполнен
except ConnectionRefusedError:
    print(f"Не удалось подключиться к серверу {host}:{port}. Проверьте адрес и порт.")
    sock.close()
    exit()

# Инициализируем переменную для накопления полученных данных
received_data = ''

# Основной цикл для отправки сообщений на сервер
while True:
    # Запрашиваем у пользователя сообщение для отправки на сервер
    msg = input("Your string (type 'exit' to quit):")
    # Отправляем сообщение серверу, добавляя символ '\n' в конце для обозначения конца сообщения
    try:
        sock.send((msg + '\n').encode('utf-8'))
        print("Message sent to server")  # пункт 4.iii выполнен
    except BrokenPipeError:
        print("Соединение с сервером было потеряно.")
        break

    # Инициализируем переменную для хранения полного ответа от сервера
    full_response = ''
    # Получаем ответ от сервера
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                # Если получили пустые данные, значит соединение закрыто
                print("Сервер закрыл соединение.")
                sock.close()
                exit()
            # Декодируем полученные байты и добавляем к накопленной строке
            received_data += data.decode('utf-8')
            # Проверяем, есть ли полный ответ (наличие '\n' в received_data)
            if '\n' in received_data:
                # Разделяем данные по символу новой строки '\n'
                line, received_data = received_data.split('\n', 1)
                full_response = line
                break  # Выходим из цикла ожидания ответа
        except ConnectionResetError:
            print("Соединение было разорвано сервером.")
            sock.close()
            exit()
    print("Message received from server")  # пункт 4.iv выполнен
    print(full_response)  # Выводим ответ от сервера

    # Если мы отправили 'exit', завершаем цикл
    if msg.lower() == 'exit':
        break  # Выходим из цикла отправки сообщений

# После выхода из цикла закрываем соединение с сервером
sock.close()
print("Connection closed to server")  # пункт 4.ii выполнен