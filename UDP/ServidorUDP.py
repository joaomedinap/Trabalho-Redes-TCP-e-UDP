import socket

# Configura e executa o servidor UDP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('localhost', 12345))
print("Servidor UDP aguardando mensagens...")

while True:
    message, addr = server_socket.recvfrom(1024)
    print(f"Mensagem recebida de {addr}: {message.decode('utf-8')}")
    response = f"Echo: {message.decode('utf-8')}"
    server_socket.sendto(response.encode('utf-8'), addr)
