import time

import socket

main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
main_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
main_socket.bind(("localhost", 10000))
main_socket.setblocking(False)
main_socket.listen(10)
print("Socket")
players = []
while True:
    try:
        new_socket = main_socket.accept()[0]
        addr = main_socket.accept()[1]
        print("Connected to:", addr)
        new_socket.setblocking(False)
        players.append(addr)
    except BlockingIOError:
        pass
    for sock in players:
        try:
            sock.send("ready".encode())
        except:
            players.remove(sock)
            sock.close()
            print("Closed")
    #time.sleep(1)
