import socket
import time

# встановлюємо IP-адресу та порт хоста
host_ip = "192.168.0.177"  # замініть це на IP-адресу свого хоста
port = 12345

# підключаємося до хоста
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host_ip, port))

while True:
    # отримуємо команду та час її надсилання
    command = 0
    client_socket.recv(1024)
    client_socket.send(command)
    command_with_time = client_socket.recv(1024)
    command, timestamp = command_with_time.decode().split()
    timestamp = float(timestamp)

    # виконуємо команду та виводимо час її отримання
    print(f"Command '{command}' received at {time.ctime(timestamp)}")

    response = 22
    timestamp = time.time()
    response_data = f"{response} {timestamp}"
    client_socket.send(response_data.encode())
