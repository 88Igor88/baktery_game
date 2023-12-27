import socket
import pygame
import math
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
sock.connect(("localhost", 10000))
pygame.init()
x = 800
y = 600
radius = 50
BLACK = (0, 0, 0)
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("baktery")
run = True
old_vector = (0, 0)
center = (x//2, y//2)
while run:
    for event in pygame.event.get():
        if event == pygame.QUIT:
            run = False
            pygame.quit()
    if pygame.mouse.get_focused():
        pos = pygame.mouse.get_pos()
        vector = pos[0] - center[0], pos[1] - center[1]
        len_ = math.sqrt(vector[0]**2+vector[1]**2)
        if len_ <= radius:
            vector = 0, 0
        if vector != old_vector:
            old_vector = vector
            message = "<{},{}>".format(vector[0], vector[1])
            sock.send(message.encode())
    screen.fill(BLACK)
    pygame.draw.circle(screen, (0, 255, 0), center, radius)
    pygame.display.update()
    data = sock.recv(1024).decode()
    print("Получено: ", data)
pygame.quit()

