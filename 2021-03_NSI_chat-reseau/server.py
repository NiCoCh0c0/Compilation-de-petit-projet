import socket
import threading
import mysql.connector


class TreadForClient(threading.Thread):
    def __init__(self, connexion):
        threading.Thread.__init__(self)
        self.connexion = connexion
        connexion.send('OK'.encode("Utf8"))
        self.pseudo = self.connexion.recv(1024).decode("utf8")
        print(self.pseudo)

    def run(self):
        while True:
            try:
                data = self.connexion.recv(1024).decode("utf8")
                msg = self.pseudo + '> ' + data
                print(msg)

                request = "INSERT INTO historique (id, utilisateur, message) " \
                          "VALUES (%s, %s, %s)"
                mycursor.execute("SELECT max(id) FROM historique")
                max_id = mycursor.fetchall()
                max_id = max_id[0][0] + 1

                values = (max_id, self.pseudo, data)
                mycursor.execute(request, values)
                mydb.commit()
                print("Message ajouté à la bd")

                if data.upper() == 'FIN':
                    print('deconnexion de ', self.pseudo)
                    break

            except:
                connexion_list.remove(self.connexion)
                connexion.close()
                print("deconnexion")
                break

            for conn in connexion_list:
                try:
                    conn.send(msg.encode("Utf8"))
                except ConnectionAbortedError:
                    connexion_list.remove(conn)
                    connexion.close()
                    print("deconnexion")
                    break


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="chat_en_ligne"
)
mycursor = mydb.cursor()

host, port = '', 5566

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind((host, port))
print('Le serveur est prêt')

connexion_list = []

while True:
    socket.listen()
    connexion, address = socket.accept()
    print('Connexion de :', address)
    connexion_list.append(connexion)
    # print(connexion_list)

    my_thread = TreadForClient(connexion)
    my_thread.start()

socket.close()
