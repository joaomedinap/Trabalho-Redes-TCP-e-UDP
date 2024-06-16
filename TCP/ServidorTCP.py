import socket
import threading

# Função para lidar com a comunicação com um cliente
def handle_client(client_socket):
    while True:
        message = client_socket.recv(1024).decode('utf-8')
        if not message:
            break
        print(f"Mensagem recebida: {message}")
        response = f"Echo: {message}"
        client_socket.send(response.encode('utf-8'))
    client_socket.close()

# Configura e executa o servidor TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("localhost", 12345))
server_socket.listen(5)
print("Servidor TCP aguardando conexões...")

while True:
    client_socket, addr = server_socket.accept()
    print(f"Conexão estabelecida com {addr}")
    threading.Thread(target=handle_client, args=(client_socket,)).start()
