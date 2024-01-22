import time
import socket
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import declarative_base, sessionmaker
import psycopg2
import pygame

pygame.init()
main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
main_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
main_socket.bind(("localhost", 10000))
main_socket.setblocking(False)
main_socket.listen(10)
WIDHT_ROOM, HEIGHT_ROOM = 4000, 4000
WIDHT_SERVER, HEIGHT_SERVER = 300, 300
screen = pygame.display.set_mode([WIDHT_SERVER, HEIGHT_SERVER])

engine = create_engine("postgresql+psycopg2://postgres:igor33igor@localhost:5432/base_test")
Session = sessionmaker(bind=engine)
Base = declarative_base()
s = Session()


class Players(Base):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30))
    adres = Column(String)
    x = Column(Integer, default=50)
    y = Column(Integer, default=50)
    size = Column(Integer, default=50)
    errors = Column(Integer, default=0)
    abs_speed = Column(Integer, default=1)
    speed_x = Column(Integer, default=0)
    speed_y = Column(Integer, default=0)

    def __init__(self, adres, name):
        self.name = name
        self.adres = adres


class LocalPlayer():
    def __init__(self, id, name, socket, addr):
        self.id = id
        self.db = s.get(Players, self.id)
        self.sock = main_socket
        self.name = name
        self.addres = addr
        self.x = 500
        self.y = 500
        self.size = 50
        self.errors = 0
        self.abs_speed = 1
        self.speed_x = 0
        self.speed_y = 0


run = True
players = {}
timer = pygame.time.Clock()
print("Настройка завершена")

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    try:
        # проверяем желающих войти в игру
        new_socket, addr = main_socket.accept()  # принимаем входящие
        print('Подключился', addr)
        new_socket.setblocking(False)
        new_player = Players(new_socket, addr)
        s.merge(new_player)
        s.commit()
        addr = f'({addr[0]},{addr[1]})'
        data = s.query(Players).filter(Players.adres == addr)
        for user in data:
            player = LocalPlayer(user.id, new_socket, new_socket, addr)
            players[user.id] = player

    except BlockingIOError as e:
        print(e)

    # Считываем команды игроков
    for id in list(players):
        try:
            data = players[id].sock.recv(1024).decode()
            print("Получил", data)
        except:
            pass
    # Отправляем статус игрового поля
    for id in list(players):
        try:
            players[id].sock.send("Игра".encode())
        except:
            players[id].sock.close()
            del players[id]
            s.query(Players).filter(Players.id == id).delete()
            s.commit()
            print("Сокет закрыт")
    timer.tick(60)
    pygame.display.update()
    time.sleep(1)
pygame.quit()
