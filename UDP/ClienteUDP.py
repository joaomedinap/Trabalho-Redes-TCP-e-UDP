import socket
import time

# Configura e executa o cliente UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ("localhost", 12345)

start_time = time.time()
for i in range(1000):
    message = f"Message {i}"
    client_socket.sendto(message.encode('utf-8'), server_address)
    data, addr = client_socket.recvfrom(1024)
    print(f"Resposta do servidor: {data.decode('utf-8')}")
end_time = time.time()

print(f"Tempo total UDP: {end_time - start_time} segundos")
client_socket.close()
