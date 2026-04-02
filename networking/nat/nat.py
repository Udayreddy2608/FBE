import socket
import threading
import time
from collections import namedtuple

NATEntry = namedtuple("NATEntry", ["private_ip", "private_port", "public_port", "dest_ip", "dest_port", "created_at"])

class NATTable:
    def __init__(self):
        self.entries : dict[int, NATEntry] = {}
        self._port_counter = 4000
        self._lock = threading.Lock()
    
    def get_or_create(self, private_ip, private_port, dest_ip, dest_port):
        with self._lock:
            for pub_port, entry in self.entries.items():
                if (entry.private_ip == private_ip and
                    entry.private_port == private_port and
                    entry.dest_ip == dest_ip and
                    entry.dest_port == dest_port):
                    return pub_port
        

            self._port_counter += 1
            pub_port = self._port_counter
            self.entries[pub_port] = NATEntry(
                private_ip= private_ip,
                private_port= private_port,
                public_port = pub_port,
                dest_ip= dest_ip,
                dest_port= dest_port,
                created_at= time.time()
            )
            print(f"  [NAT] New mapping: {private_ip}:{private_port} → PUBLIC:{pub_port} → {dest_ip}:{dest_port}")
            return pub_port
        
    
    def reverse_lookup(self, public_port):
        return self.entries.get(public_port)

    def display(self):
        print(f"\n{'─'*70}")
        print(f"  {'PRIVATE SRC':<25} {'PUBLIC PORT':<15} {'DESTINATION':<25}")
        print(f"{'─'*70}")
        for pub_port, e in self.entries.items():
            print(f"  {e.private_ip}:{e.private_port:<18} {pub_port:<15} {e.dest_ip}:{e.dest_port}")
        print(f"{'─'*70}\n")


nat = NATTable()

dest = ("93.184.216.34", 80)

clients = [
    ("192.168.1.10", 5001),
    ("192.168.1.20", 6001),
    ("192.168.1.30", 7001),
]

print("Clients sending packets through NAT:\n")

for private_ip, private_port in clients:
    pub_port = nat.get_or_create(private_ip,
                                private_port,
                                 *dest)

nat.display()

print("Inbound reply to port 4001:")

entry = nat.reverse_lookup(4001)

if entry:
    print(f"  Forwarding to → {entry.private_ip}:{entry.private_port}\n")