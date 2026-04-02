import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("127.0.0.1", 9200))
print("Server listening on :9200")

while True:
    data, addr = s.recvfrom(4096)
    print(f"  [SERVER] Got '{data.decode()}' from {addr}")
    s.sendto(b"ACK: " + data, addr)