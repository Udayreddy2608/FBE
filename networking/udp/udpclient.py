import socket

HOST = "127.0.0.1"
PORT = 9999

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.sendto(b"Hello UDAY", (HOST, PORT))

    s.settimeout(2.0)
    
    response, _ = s.recvfrom(1024)

    print(f"Echo: {response.decode()}")