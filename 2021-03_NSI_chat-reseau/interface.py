import tkinter as tk
import tkinter.font as tkFont
import threading
import sys
import SQL

class ThreadForRead(threading.Thread):
    """
    A VOIR POUR LE RENDRE + PROPRE MAIS OK
    """
    def __init__(self, socket, screen):
        threading.Thread.__init__(self)
        self.socket = socket
        self.screen = screen


    def run(self):
        while True:
            msgServeur = self.socket.recv(1024).decode("Utf8")

            if self.screen.historic_indice == 0:
                self.screen.hystoric.append(msgServeur)
                self.screen.hystoric.pop(0)

            else:
                self.screen.historic_indice += 1
                print(self.screen.historic_indice)

            for i in range(len(self.screen.list_label)):
                label = self.screen.list_label[i]
                label.config(text=self.screen.hystoric[i])
                label.pack()

            print(msgServeur)
            if msgServeur.upper() == 'FIN':
                break


class Interface(tk.Tk):
    """
    FAIRE EN SORTE DE TRANSFORMER UN MAX EN SOUS FONCTION
    """
                    
    def __init__(self, socket):
        tk.Tk.__init__(self)
        self.socket = socket
        self.ignore = False

        self.font = tkFont.Font(family="Helvetica", size=12)

        self.gridConfig()
        self.createFrame()
        self.createLabel()
        self.createButton()
        self.createEntry()



    def gridConfig(self):
        """
        Initialise la taille des lignes et les colonnes
        """
        self.bind("<Configure>", self.on_configure)
        self.columnconfigure(0, weight=1)
        for i in range(4):
            if i == 0 or i == 3:
                self.rowconfigure(i, weight=1)
            else:
                self.rowconfigure(i, weight=3)

    def createFrame(self):
        """
        Création des Frames
        """
        self.title_frame = tk.Frame(self)
        self.frame1 = tk.Frame(self)
        self.frame2 = tk.Frame(self)
        self.frame3 = tk.Frame(self)
        self.frame4 = tk.Frame(self)

    def createEntry(self):
        """
        Création des Entry
        """
        self.list_entry = []
        self.entry1 = tk.Entry(self.frame1, textvariable=tk.StringVar(),
                               width=50, justify='center', font=self.font)
        self.entry2 = tk.Entry(self.frame2, textvariable=tk.StringVar(),
                               width=50, justify='center', font=self.font)
        self.entry3 = tk.Entry(self.frame3, textvariable=tk.StringVar(),
                               width=50, justify='center', font=self.font)
        self.list_entry.append(self.entry1)
        self.list_entry.append(self.entry2)
        self.list_entry.append(self.entry3)


    def modifEntry(self, width):
        """
        Modifie la taille des Entry
        Parametres:
          - width : largeur (en pixel)
          - height : hauteru (en pixel)
        """
        self.entry1.config(width=width)
        self.entry2.config(width=width)
        self.entry3.config(width=width)

    def createLabel(self):
        self.title = tk.Label(self.title_frame, text="FACEBOCK", fg="blue")
        self.label1 = tk.Label(self.frame1, text="HOST", fg="blue", font=self.font)
        self.label2 = tk.Label(self.frame2, text="PORT", fg="blue", font=self.font)
        self.label3 = tk.Label(self.frame3, text="Confirm Password", fg="blue", font=self.font)

        self.hystoric = [''] * 10
        self.historic_indice = 0
        self.list_label = []
        for i in range(10):
            self.list_label.append(tk.Label(self.frame1, text='', wraplength=300, font=self.font))


    def createButton(self):
        self.button = tk.Button(self.frame3, text="Valider", font=self.font, command=self.getServerInfo)
        self.button2 = tk.Button(self.frame4, text="Create account", font=self.font, command=self.createAccount)

    def modifButton(self, width, height):
        """
        Modifie la taille des Buttons
        Parametres:
          - width : largeur (en pixel)
          - height : hauteru (en pixel)
        """
        self.button.config(width=width, height=height)
        self.button2.config(width=width, height=height)



    def on_configure(self, event):
        """
        Fonction qui change la taille des éléments dès que la fenêtre change de taille
        """
        sizew = self.winfo_width()
        sizeh = self.winfo_height()
        if self.ignore:
            self.ignore = False
        else:
            """
            TOUT REDIMENTIONNER (FONT, WIDGETS)
            """
            self.font.config(size=int(sizew/50))
            self.modifEntry(int(sizew/10))# A VOIR
            self.modifButton(int(sizew/30), int(sizeh/250))
            #frame.config(height=sizeh, width=sizew)
            self.ignore = True









    def start(self):
        self.focus_force()

        self.title.pack()
        self.label1.pack()
        self.entry1.pack()
        self.label2.pack()
        self.entry2.pack()
        self.button.pack()

        self.title_frame.grid(row=0)
        self.frame1.grid(row=1)
        self.frame2.grid(row=2)
        self.frame3.grid(row=3)

        self.geometry("400x400")
        self.bind('<Return>', self.getServerInfo)
        self.mainloop()

    def getServerInfo(self, key=0):
        HOST = self.entry1.get()
        PORT = int(self.entry2.get())
        self.entry1.delete(0, tk.END)
        self.entry2.delete(0, tk.END)
        try:
            self.socket.connect((HOST, PORT))
            msgServeur = self.socket.recv(1024).decode("Utf8")
            if msgServeur != 'OK':
                print('Erreur')
                sys.exit()
            print("Connexion établie avec le serveur.")
            self.loginPage()

        except:
            """
            METTRE UN LABEL POUR ERREUR
            """
            print("La connexion a échoué.")

    def loginPage(self, key=0):
        self.label1.config(text="Login")
        self.label2.config(text="Password")
        self.rowconfigure(4, weight=1)
        self.frame4.grid(row=4)
        self.button2.pack()
        self.bind('<Return>', self.getPseudo)
        self.button.config(command=self.getPseudo)

    def getPseudo(self, key=0):
        pseudo, password = self.getEntry(2)


        logins = SQL.select(("login", "password"), "login")
        etat_connexion = False
        for login in logins:
            if login == (pseudo, password):
                etat_connexion = True


        if etat_connexion:
            """
            FAIRE UNE FONCTION POUR METTRE EN PLACE LA PAGE
            """
            self.label1.pack_forget()
            self.label2.pack_forget()
            self.entry1.pack_forget()

            for i in range(10):
                label = self.list_label[i]
                label.config(text=self.hystoric[i])
                label.pack()

            for i in range(4):
                if i == 0 or i == 2:
                    self.rowconfigure(i, weight=1)
                elif i == 3:
                    self.rowconfigure(i, weight=0)
                else:
                    self.rowconfigure(i, weight=8)

            self.socket.send(pseudo.encode("Utf8"))
            self.initHistoric()
            self.button.config(text="Envoyer", command=self.getMessage)
            self.bind('<Return>', self.getMessage)
            self.bind("<Up>", self.initHistoric)
            self.bind("<Down>", self.initHistoric)
            self.startThreadRead()
        else:
            """
            METTRE UN MESSAGE D'ERREUR
            """
            self.label1.config(text="Login inconnu", fg="red")


    def getEntry(self, nb):
        values = []
        for i in range(nb):
            values.append(self.list_entry[i].get())
            self.list_entry[i].delete(0, tk.END)
        return values


    def getMessage(self, key=0):
        msg = self.entry2.get()
        self.entry2.delete(0, tk.END)
        self.socket.send(msg.encode("Utf8"))


    def startThreadRead(self):
        self.thread_read = ThreadForRead(self.socket, self)
        self.thread_read.start()


    def initHistoric(self, key=0):
        max_id = SQL.select("max(id)", "historique")[0]

        if key == 0:
            pass
        elif key.keysym == 'Up' and self.historic_indice+9 < max_id:
            self.historic_indice += 1
        elif key.keysym == 'Down' and self.historic_indice > 0:
            self.historic_indice -= 1


        values = max_id - self.historic_indice - 9, max_id - self.historic_indice
        where = "id BETWEEN {} AND {} ORDER BY id DESC".format(values[0], values[1])

        msg = SQL.select("*", "historique", where=where)
        msg = msg[::-1]

        for i in msg:
            auteur = i[1]
            msg_temp = i[2]
            final = f'{auteur}> {msg_temp}'
            self.hystoric.append(final)
            self.hystoric.pop(0)

        for i in range(len(self.list_label)):
            label = self.list_label[i]
            label.config(text=self.hystoric[i])
            label.pack()





    def createAccount(self):
        self.rowconfigure(3, weight=3)
        self.label3.pack()
        self.button.pack_forget()
        self.entry3.pack()
        self.button2.config(command=self.getNewAccount)
        self.bind('<Return>', self.getNewAccount)

    def getNewAccount(self, key=0):
        condition = True
        pseudo = self.entry1.get()
        password = self.entry2.get()
        password_confirm = self.entry3.get()



        pseudos = SQL.select("login", "login")

        for ps in pseudos:
            if ps == pseudo:
                condition = False

        if (password == password_confirm) and (condition == True):

            max_id = SQL.select("max(id)", "login")
            max_id += 1

            SQL.insert("login", ("id", "login", "password"), (max_id, pseudo, password))


            self.bind('<Return>', self.getPseudo)
            self.button.config(command=self.getPseudo)
            self.entry3.pack_forget()
            self.label3.pack_forget()
            self.loginPage()
