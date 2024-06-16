import socket 
import time  

# Classe que representa um servidor UDP
class UDPServer:  
    def __init__(self, host, port): 
        self.host = host 
        self.port = port  
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Cria um socket UDP (Datagram) para comunicação.
        self.server_socket.bind((self.host, self.port)) # Associa o socket ao endereço e porta especificados.
        self.message_count = 0  
        self.start_time = None
        self.end_time = None

    # Função que inicia o servidor.
    def run(self):  
        # print("Servidor UDP iniciado, aguardando conexões...")
        while True:  # loop infinito que recebe as mensagens.
            self.data, self.addr = self.server_socket.recvfrom(1024) # Recebe dados do cliente. O buffer é de 1024 bytes.
            # print(f"{self.data}")  # Imprime a mensagem recebida.
            self.server_socket.sendto(self.data, self.addr)
            self.message_count += 1  # Incrementa o contador de mensagens.
            if self.message_count == 1:
                self.start_time = time.time_ns()
                # Registra o tempo de início e de término da mensagem
            if self.message_count == 1000:
                self.end_time = time.time_ns()
                total_time = (self.end_time - self.start_time) / 1000000000
                print(f"UDP = Tempo total para receber 1000 mensagens: {total_time:.2f} segundos")  
                break  

# Cria uma instância do UDPServer e chama o run para iniciar o servidor
if __name__ == "__main__":
    server = UDPServer('localhost', 12345)
    server.run()  
