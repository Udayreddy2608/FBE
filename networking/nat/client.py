import socket, time, threading

def client(name, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("127.0.0.1", port))
    for i in range(3):
        msg = f"{name}-packet-{i}".encode()
        s.sendto(msg, ("127.0.0.1", 9000))
        data, _ = s.recvfrom(4096)
        print(f"  [{name}] Reply: {data.decode()}")
        time.sleep(0.5)

threading.Thread(target=client, args=("ClientA", 5001)).start()
threading.Thread(target=client, args=("ClientB", 6001)).start()