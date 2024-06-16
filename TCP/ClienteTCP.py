import socket
import time

# Configura e executa o cliente TCP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("localhost", 12345))

start_time = time.time()
for i in range(1000):
    message = f"Message {i}"
    client_socket.send(message.encode('utf-8'))
    response = client_socket.recv(1024)
    print(f"Resposta do servidor: {response.decode('utf-8')}")
end_time = time.time()

print(f"Tempo total TCP: {end_time - start_time} segundos")
client_socket.close()
