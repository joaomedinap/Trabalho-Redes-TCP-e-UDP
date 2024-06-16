import socket
import threading
import time

class TCPServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.client_socket = None
        self.addr = None
        self.message_count = 0
        self.start_time = None
        self.end_time = None

    def run(self):
        # print("Servidor TCP iniciado, aguardando conexões...")
        while True:
            self.client_socket, self.addr = self.server_socket.accept()
            # print(f"Conexão estabelecida com {self.addr}")
            data = self.client_socket.recv(1024)
            # print(f"{data}")
            response = f"Echo: {data}"
            self.client_socket.send(response.encode("utf-8"))
            
            self.message_count += 1
            if self.message_count == 1:
                self.start_time = time.time_ns()
            if self.message_count == 1000:
                self.end_time = time.time_ns()
                total_time = (self.end_time - self.start_time)/1000000000
                print(f"TCP = Tempo total para receber 1000 mensagens: {total_time:.2f} segundos")
                break
            
        self.client_socket.close()

if __name__ == "__main__":
    server = TCPServer('localhost', 12345)
    server.run()
