import socket
import time

class TCPClient:
    # Armazena o numero da porta e o endereço do host e cria o socket tcp
    def __init__(self, host, port):
        self.host = host
        self.port = port

    # Realiza a conexão do socket cliente com o servidor e Adiciona o loop que irá iterar 1000x
    def start(self, count, times):
        for i in range(count):
            start_time = time.time()
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
            self.client_socket.send(f"Mensagem {i}".encode("utf-8"))
            response = self.client_socket.recv(1024).decode("utf-8")
            # print(f"Resposta do servidor: {response}")
            self.client_socket.close()
            end_time = time.time()
            times.append(end_time - start_time)

if __name__ == "__main__":
    client = TCPClient('localhost', 12345)
    tcp_times = []
    client.start(1000, tcp_times)
