import socket
import time

# Armazena o numero da porta e o endereço do host e cria o socket udp (datagrama)
class UDPClient: 
    def __init__(self, host, port): 
        self.host = host  
        self.port = port  
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  

# Função de envio de mensagens e loop que irá iterar 1000x e envia a mensagem formatada para o servidor no endereço (host, port)
    def start(self, count, times): 
        for i in range(count):  
            start_time = time.time()
            self.client_socket.sendto(f"Mensagem {i}".encode(), (self.host, self.port))
            self.client_socket.recvfrom(1024)
            end_time = time.time()
            times.append(end_time - start_time)
        self.client_socket.close()

# Cria a instancia do UDP e chama o metodo para envio das mensagens
if __name__ == "__main__":  
    client = UDPClient('localhost', 12345) 
    udp_times = []
    client.start(1000, udp_times)
