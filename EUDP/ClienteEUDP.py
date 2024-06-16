import socket
import threading
import time

# EUDP (Enhanced User Datagram Protocol)
class EUDPClient:
    def __init__(self, local_address, local_port, remote_address, remote_port):
        # Inicializa o cliente com os endereços e portas fornecidos
        self.local_address = local_address
        self.local_port = local_port
        self.remote_address = remote_address
        self.remote_port = remote_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((local_address, local_port))
        self.seq_num = 0
        self.ack_num = -1
        self.window_size = 5
        self.cwnd = 1
        self.ssthresh = 64
        self.send_buffer = {}
        self.lock = threading.Lock()

    def send_packet(self, data):
        # Envia um pacote para o servidor
        with self.lock:
            packet = self.create_packet(data)
            self.sock.sendto(packet.encode(), (self.remote_address, self.remote_port))
            self.start_timer(packet)

    def create_packet(self, data):
        # Cria um pacote no formato seq_num|data
        return f"{self.seq_num}|{data}"

    def start_timer(self, packet):
        # Inicia um temporizador para retransmitir o pacote em caso de timeout
        seq_num, _ = self.parse_packet(packet.encode())
        threading.Timer(1.0, self.retransmit_packet, args=(seq_num,)).start()

    def retransmit_packet(self, seq_num):
        # Retransmite o pacote se não houver recebido ACK
        with self.lock:
            if seq_num > self.ack_num:
                packet = self.create_packet(self.send_buffer[seq_num])
                self.sock.sendto(packet.encode(), (self.remote_address, self.remote_port))
                self.start_timer(packet)

    def parse_packet(self, data):
        # Converte o pacote de bytes para uma string e divide em seq_num e payload
        seq_num, payload = data.decode().split('|', 1)
        return int(seq_num), payload

    def receive_ack(self):
        # Loop para receber ACKs continuamente
        while True:
            self.data, self.addr = self.sock.recvfrom(1024)
            self.handle_ack(self.data)

    def handle_ack(self, data):
        # Processa o ACK recebido e ajusta a janela de congestionamento
        ack_type, ack_num = data.decode().split('|')
        if ack_type == "ACK":
            ack_num = int(ack_num)
            with self.lock:
                if ack_num > self.ack_num:
                    self.ack_num = ack_num
                    # Ajusta a janela de congestionamento (cwnd)
                    if self.cwnd < self.ssthresh:
                        self.cwnd *= 2
                    else:
                        self.cwnd += 1

    def start(self, count, times):
        # Envia 1000 mensagens para o servidor
        threading.Thread(target=self.receive_ack).start()
        for i in range(count):
            start_time = time.time()
            message = f"Mensagem {i}"
            with self.lock:
                self.seq_num += 1
                self.send_buffer[self.seq_num] = message
            self.send_packet(message)
            # print(f"Enviada {message}")
            end_time = time.time()
            times.append(end_time - start_time)
        # self.sock.close()

if __name__ == "__main__":
    # Inicializa e executa o cliente EUDP
    client = EUDPClient('localhost', 54321, 'localhost', 12345)
    eudp_times = []
    client.start(1000, eudp_times)
