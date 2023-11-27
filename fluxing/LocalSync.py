import socket
import time

# отримуємо IP-адресу хоста
host_ip = socket.gethostbyname(socket.gethostname())
print("Host IP address:", host_ip)

# створюємо сокет та встановлюємо його для прослуховування
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host_ip, 12345))
server_socket.listen(2)

print("Waiting for connections...")

# очікуємо на підключення першого клієнта
client1_socket, client1_address = server_socket.accept()
print("Client 1 connected from", client1_address)

# очікуємо на підключення другого клієнта
client2_socket, client2_address = server_socket.accept()
print("Client 2 connected from", client2_address)

# відправляємо команду "True" та час її надсилання обом клієнтам
while True:
    command = '0'
    sendtime = time.time()
    client1_socket.sendall(command.encode())
    data1 = client1_socket.recv(1024)
    gettime = time.time()
    print(f"PC1 ping '{(gettime-sendtime)}'")
    sendtime = time.time()
    sendtime = time.time()
    client2_socket.sendall(command.encode())
    data2 = client2_socket.recv(1024)
    gettime = time.time()
    print(f"PC2 ping '{(gettime - sendtime)}'")
    command = input("Enter command (True/False): ")
    command_with_time = f"{command}".encode()
    client1_socket.sendall(command_with_time)
    client2_socket.sendall(command_with_time)
    print(f"Command '{command}' sent to both clients")
    data1 = client1_socket.recv(1024)
    data2 = client2_socket.recv(1024)
    command = data1.decode()


    # виконуємо команду та виводимо час її отримання
    print(f"Command '{command}' received")
    command = data2.decode()

    # виконуємо команду та виводимо час її отримання
    print(f"Command '{command}' received")
