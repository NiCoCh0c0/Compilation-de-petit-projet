import threading

class ThreadForRead(threading.Thread):
    def __init__(self, socket):
        threading.Thread.__init__(self)
        self.socket = socket

    def run(self):
        while True:
            msgServeur = self.socket.recv(1024).decode("Utf8")
            print(msgServeur)
            if msgServeur.upper() == 'FIN':
                break