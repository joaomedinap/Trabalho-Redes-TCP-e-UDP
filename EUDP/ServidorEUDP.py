import socket
import threading
import time

# EUDP (Enhanced User Datagram Protocol)
class EUDPServer:
    def __init__(self, address, port):
        # Inicializa o servidor com o endereço e a porta fornecidos
        self.address = address
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((address, port))
        self.expected_seq = 1
        self.recv_buffer = {}
        self.lock = threading.Lock()
        self.message_count = 0
        self.start_time = None
        self.end_time = None

    def run(self):
        # Loop para receber pacotes continuamente
        while True:
            data, addr = self.sock.recvfrom(1024)
            self.handle_packet(data, addr)

    def handle_packet(self, data, addr):
        # Processa o pacote recebido e envia ACK
        with self.lock:
            seq_num, payload = self.parse_packet(data)
            self.message_count += 1
            if self.message_count == 1:
                self.start_time = time.time_ns()

            if seq_num == self.expected_seq:
                # print(f"Recebido: {payload}")
                self.expected_seq += 1
                self.send_ack(addr, seq_num)
                # Processa pacotes que chegaram fora de ordem
                while self.expected_seq in self.recv_buffer:
                    print(f"Recebido (buffer): {self.recv_buffer[self.expected_seq]}")
                    del self.recv_buffer[self.expected_seq]
                    self.expected_seq += 1
            else:
                self.recv_buffer[seq_num] = payload
                self.send_ack(addr, self.expected_seq - 1)
                
            if self.message_count == 1000:
                self.end_time = time.time_ns()
                total_time = (self.end_time - self.start_time)/1000000000
                print(f"EUDP = Tempo total para receber 1000 mensagens: {total_time:.2f} segundos")

    def parse_packet(self, data):
        # Converte o pacote de bytes para uma string e divide em seq_num e payload
        seq_num, payload = data.decode().split('|', 1)
        return int(seq_num), payload

    def send_ack(self, addr, ack_num):
        # Envia um ACK para o cliente
        ack_packet = f"ACK|{ack_num}".encode()
        self.sock.sendto(ack_packet, addr)


if __name__ == "__main__":
    
    # Inicializa e inicia o servidor UDP aprimorado
    server = EUDPServer('localhost', 12345)
    server.run()
