import socket
import threading

NAT_LISTEN_HOST = "127.0.0.1"
NAT_LISTEN_PORT = 9000
NAT_PUBLIC_PORT = 9100
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 9200

nat_table: dict[tuple, socket.socket] = {}
reverse_table: dict[int, tuple] = {}      
lock = threading.Lock()

def handle_reply(pub_sock: socket.socket, private_in: socket.socket):
    while True:
        data, _ = pub_sock.recvfrom(4096)
        pub_port = pub_sock.getsockname()[1]

        with lock:
            client_addr = reverse_table.get(pub_port)
        
        if client_addr:
            print(f"  [NAT ←] Reply to {client_addr} via public port {pub_port}")
            private_in.sendto(data, client_addr)


def nat_proxy():
    private_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    private_sock.bind((NAT_LISTEN_HOST, NAT_LISTEN_PORT))
    print(f"NAT proxy listening on private side: {NAT_LISTEN_HOST}:{NAT_LISTEN_PORT}")

    while True:
        data, client_addr = private_sock.recvfrom(4096)
        print(f"  [NAT →] Packet from {client_addr}: {data.decode()}")

        with lock:
            if client_addr not in nat_table:
                pub_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                pub_sock.bind((NAT_LISTEN_HOST, 0))
                pub_port = pub_sock.getsockname()[1]

                nat_table[client_addr] = pub_sock
                reverse_table[pub_port] = client_addr

                print(f"  [NAT]  Mapped {client_addr} → public port {pub_port}")

                t = threading.Thread(target=handle_reply, args=(pub_sock, private_sock), daemon=True)
                t.start()

            pub_sock = nat_table[client_addr]

        pub_sock.sendto(data, (SERVER_HOST, SERVER_PORT))

if __name__ == "__main__":
    nat_proxy()