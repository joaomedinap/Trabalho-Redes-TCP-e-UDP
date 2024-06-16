import time
import threading
import EUDP.ClienteEUDP
import EUDP.ServidorEUDP
import TCP.ClienteTCP
import TCP.ServidorTCP
import matplotlib.pyplot as plt
import UDP.ClienteUDP
import UDP.ServidorUDP

def main():
    message_count = 1000
    
    # Instancia TCP
    tcp_server = TCP.ServidorTCP.TCPServer('localhost', 12345)
    tcp_client = TCP.ClienteTCP.TCPClient('localhost', 12345)
    tcp_times = []
    
    # Instancia UDP
    udp_server = UDP.ServidorUDP.UDPServer('localhost', 12346)
    udp_client = UDP.ClienteUDP.UDPClient('localhost', 12346)
    udp_times = []
    
    # # Instancia EUDP
    eudp_server = EUDP.ServidorEUDP.EUDPServer('localhost', 12347)
    eudp_client = EUDP.ClienteEUDP.EUDPClient('localhost', 54321, 'localhost', 12347)
    eudp_times = []
    
    # Iniciando os Servidores separadamente
    threading.Thread(target=tcp_server.run, daemon=True).start()
    threading.Thread(target=udp_server.run, daemon=True).start()
    threading.Thread(target=eudp_server.run, daemon=True).start()

    # Espera para garantir que os servidores estejam prontos
    time.sleep(3)
    
    # Executando os clientes e medindo o tempo
    threading.Thread(target=tcp_client.start, args=(message_count, tcp_times)).start()
    threading.Thread(target=udp_client.start, args=(message_count, udp_times)).start()
    threading.Thread(target=eudp_client.start, args=(message_count, eudp_times)).start()
    
    # Espera para garantir que terminem a execução
    time.sleep(6)
    
    # Calculando tempos totais e médios
    total_tcp_time = sum(tcp_times)
    total_udp_time = sum(udp_times)
    total_eudp_time = sum(eudp_times)
    avg_tcp_time = total_tcp_time / message_count
    avg_udp_time = total_udp_time / message_count
    avg_eudp_time = total_eudp_time / message_count
    
    # Plotando os gráficos
    plt.figure(figsize=(20, 8))
    
    # Tempo total
    plt.subplot(1, 2, 1)
    plt.bar(['TCP', 'UDP', 'EUDP'], [total_tcp_time, total_udp_time, total_eudp_time], color=['green', 'blue', 'red'])
    plt.title('Tempo Total de Comunicação')
    plt.ylabel('Tempo (s)')
    
    # Tempo médio
    plt.subplot(1, 2, 2)
    plt.bar(['TCP', 'UDP', 'EUDP'], [avg_tcp_time, avg_udp_time, avg_eudp_time], color=['green', 'blue', 'red'])
    plt.title('Tempo Médio de Comunicação')
    plt.ylabel('Tempo (s)')
    
    plt.tight_layout()
    plt.show()
    
if __name__ == "__main__":
    main()