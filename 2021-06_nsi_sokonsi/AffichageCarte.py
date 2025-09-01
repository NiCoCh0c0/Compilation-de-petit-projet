import tkinter as tk

class AffichageCarte(tk.Tk):
    def __init__(self,X_ecran,Y_ecran, niveau):
        tk.Tk.__init__(self)
        # Initialise les variables
        self.niveau = niveau
        self.tailleX_ecran = X_ecran
        self.tailleY_ecran = Y_ecran

        self.etat_app = False

        self.index_carte = self.niveau.getIndexCarte()
        self.carte = self.niveau.getCarte()
        self.liste_carte = self.niveau.getListeCarte()

        # Calcul de la taille des cases en fonction de la carte
        self.nb_case = 0
        for i in range(len(self.carte)):
            self.nb_case += len(self.carte[i])
        self.tailleX_case = self.tailleX_ecran / len(self.carte[0])
        self.tailleY_case = self.tailleY_ecran / len(self.carte)

        # Calcul du zoom à faire sur les images en fonction de la carte
        coef_zoomX = int(1/(640/len(self.carte[0])/64))
        coef_zoomY = int(1/(640 / len(self.carte)/64))

        # Charge les images
        self.mur = tk.PhotoImage(file="Sprite/mur.png").subsample(coef_zoomX, coef_zoomY)
        self.caisse = tk.PhotoImage(file='Sprite/caisse.png').subsample(coef_zoomX, coef_zoomY)
        self.perso = tk.PhotoImage(file='Sprite/perso.png').subsample(coef_zoomX, coef_zoomY)
        self.perso_sans_fond = tk.PhotoImage(file='Sprite/perso_sans_fond.png').zoom(2)
        self.sol = tk.PhotoImage(file='Sprite/sol.png').subsample(coef_zoomX, coef_zoomY)
        self.checkpoint = tk.PhotoImage(file='Sprite/checkpoint.png').subsample(coef_zoomX, coef_zoomY)
        self.caisse_check = tk.PhotoImage(file='Sprite/caissef.png').subsample(coef_zoomX, coef_zoomY)
        self.teleporteur = tk.PhotoImage(file='Sprite/teleporteur.png').subsample(coef_zoomX, coef_zoomY)
        self.fond_debut = tk.PhotoImage(file='Sprite/bg_debut_modif.png').zoom(10)
        self.fond_fin = tk.PhotoImage(file='Sprite/bg_fin.png').zoom(10)

        # Initialise les éléments de la fenêtre à son état initial
        self.canv = tk.Canvas(self, height=self.tailleY_ecran, width=self.tailleX_ecran, borderwidth=5, relief='groove')
        self.titre = tk.Label(self, fg='red', text='SOKONSI', font=('Algerian', 20))
        self.titre.grid(row=0)
        self.bouton = tk.Button(self, text='Niveau suivant', command=self.changementNiveau)
        self.bouton_recommencer = tk.Button(self, text='Jouer', command=self.commencer)


    def initEcran(self):
        # Affiche l'écran de début
        self.titre.pack()
        self.canv.create_image(self.tailleX_ecran / 2, self.tailleY_ecran / 2, image=self.fond_debut)
        self.canv.create_text(self.tailleX_ecran/2, self.tailleY_ecran/3, text="        Appuyes sur le bouton\npour entrer dans le chateau"\
                              , font=('Algerian', 20), fill='#33FFCC') # CHANGER COULEUR
        self.canv.create_image(self.tailleX_ecran/2 ,self.tailleY_ecran, image=self.perso_sans_fond, anchor='s') # PRENDRE LE BAS DE L'IMAGE
        self.canv.pack()
        self.bouton_recommencer.pack()
        self.mainloop()

    def commencer(self):
        # Change quelques propriétés
        titre_niveau = 'Niveau {}'.format(self.index_carte + 1)
        self.majAffichageObjet()
        self.bouton_recommencer.config(text='Recommencer', command=self.recommencer)
        self.titre.config(text=titre_niveau)




    def majAffichageObjet(self):
        # Evite un bug d'affichage (lorsqu'on appuye sur un déplacement avant de cliquer sur jouer)
        if self.etat_app == False:
            self.etat_app = True
            self.commencer()

        # Gestion de l'affichage des images
        self.carte = self.niveau.getCarte()
        self.canv.delete("all") # Supprime tout les éléments du canvas
        nb_caisse = 0
        for ligne in range(len(self.carte)): # Pour chaque ligne
            maLigne = self.carte[ligne]
            for colonne in range(len(self.carte[ligne])): # Pour chaque colonne de la ligne
                # Si mur
                if maLigne[colonne] == 'X':
                    self.canv.create_image(colonne * self.tailleX_case, ligne * self.tailleY_case, image=self.mur,  anchor='nw')
                # Si perso
                elif maLigne[colonne] == 'P' or maLigne[colonne] == 'Z' or maLigne[colonne] == 'K':
                    self.canv.create_image(colonne * self.tailleX_case, ligne * self.tailleY_case, image=self.perso,  anchor='nw')
                # Si caisse
                elif maLigne[colonne] == 'C':
                    nb_caisse+=1
                    self.canv.create_image(colonne * self.tailleX_case, ligne * self.tailleY_case, image=self.caisse,  anchor='nw')
                # Si checkpoint
                elif maLigne[colonne] == 'A':
                    self.canv.create_image(colonne * self.tailleX_case, ligne * self.tailleY_case, image=self.checkpoint,  anchor='nw')
                # Si caisse sur checkpoint
                elif maLigne[colonne] == 'M':
                    self.canv.create_image(colonne * self.tailleX_case, ligne * self.tailleY_case,
                                                                image=self.caisse_check, anchor='nw')
                # Si téléporteur
                elif maLigne[colonne] == 'T':
                    self.canv.create_image(colonne * self.tailleX_case, ligne * self.tailleY_case,
                                                                image=self.teleporteur, anchor='nw')
                # Si c'est un vide
                else:
                    self.canv.create_image(colonne * self.tailleX_case, ligne * self.tailleY_case, image=self.sol,  anchor='nw')

        if nb_caisse == 0:
            # Si on a fini le niveau
            self.bouton.pack()
            self.bouton_recommencer.pack_forget()  # Retire le bouton
        else:
            try:
                self.bouton.pack_forget() # Retire le bouton
                self.bouton_recommencer.pack()
            except:
                # Si le bouton était déjà retiré
                pass


    def changementNiveau(self):
        self.index_carte+=1
        try:
            # Test si il reste des cartes
            nouveau_texte = 'Niveau {}'.format(self.index_carte +1)
            self.titre.config(text=nouveau_texte)
            carte = self.liste_carte[self.index_carte]

            # Ajustement des images si les dimensions de la carte change
            if len(carte[0]) == 20 and self.tailleX_case != (640/20):
                # Si le format de la carte change
                self.mur = self.mur.subsample(2)
                self.caisse = self.caisse.subsample(2)
                self.perso = self.perso.subsample(2)
                self.sol = self.sol.subsample(2)
                self.checkpoint = self.checkpoint.subsample(2)
                self.caisse_check = self.caisse_check.subsample(2)
                self.teleporteur = self.teleporteur.subsample(2)
                self.tailleX_case = self.tailleX_ecran / len(carte[0])
                self.tailleY_case = self.tailleX_ecran / len(carte)
            self.niveau.setCarte(carte)
            self.majAffichageObjet()


        except: # Quand il y a plus de niveau (fin du jeu), écran de fin
            self.canv.delete('all')
            self.bouton.config(text='Appuyez pour quitter', command=self.destroy)
            self.titre.config(text='SOKONSI', font=('Algerian', 40))
            self.canv.create_image(self.tailleX_ecran / 2, self.tailleY_ecran / 2, image=self.fond_fin)
            self.canv.create_image(self.tailleX_ecran / 2, self.tailleY_ecran, image=self.perso_sans_fond, anchor='s')
            self.canv.create_text(self.tailleX_ecran / 2, self.tailleY_ecran / 2.5, text='BIEN JOUE, TU AS FINI LE JEU',\
                                  font=('Algerian', 20), fill='#33FFCC')
            with open('sauvegarde.txt', 'w') as sauvegarde:
                # Reset de la sauvegarde
                sauvegarde.write('')
        else:
            with open('sauvegarde.txt', 'w') as sauvegarde:
                # Sauvegarde la progression
                sauvegarde.write(str(self.index_carte))

    def recommencer(self):
        # Remmet la carte dans son état initial
        carte = self.niveau.listeCarte()[self.index_carte]
        self.niveau.setCarte(carte)
        self.majAffichageObjet()

    def getEtatApp(self):
        return self.etat_app

    def getNiveau(self):
        return self.niveau