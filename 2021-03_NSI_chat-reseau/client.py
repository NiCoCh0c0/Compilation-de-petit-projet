import socket
import interface


mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

screen = interface.Interface(mySocket)
screen.start()