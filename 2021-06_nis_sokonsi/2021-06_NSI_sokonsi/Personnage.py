class Personnage:
    def __init__(self, app):
        self.app = app
        self.niveau = self.app.getNiveau()
        self.initCoordonee() # Récupère les coordonnées du personnage
        self.controle() # Définition des touches



    def initCoordonee(self):
        # Cherche les coordonnées du perso sur la carte
        carte =self.niveau.getCarte()
        for ligne in range(len(carte)): # Parcours de chaque ligne
            ma_ligne = carte[ligne]
            for colonne in range(len(carte[ligne])): # Parcours de chaque colonne
                if ma_ligne[colonne] == 'P' or ma_ligne[colonne] == 'Z' or ma_ligne[colonne] == 'K': # Si le personnage est trouvé
                    self.colonne, self.ligne = colonne, ligne

    def controle(self):
        # Définit les touches
        self.app.canv.focus_force()
        self.app.bind('<z>', self.haut)
        self.app.bind('<q>', self.gauche)
        self.app.bind('<s>', self.bas)
        self.app.bind('<d>', self.droite)



    # Déplacement à droite du personnage
    def droite(self, touche):
        self.initCoordonee()
        carte = self.niveau.getCarte()
        # Vérification de savoir si il peut aller à droite
        ligne_perso_carte = carte[self.ligne]

        # Si on peut avancer sans caisse ni mur
        if ligne_perso_carte[self.colonne + 1] == ' ' or ligne_perso_carte[self.colonne + 1] == 'A' or ligne_perso_carte[self.colonne + 1] == 'T':
            self.niveau.majCarte(carte, 'droite') # Met la carte à jour
            self.app.majAffichageObjet()

        # Si on peut avancer mais avec une caisse
        elif (ligne_perso_carte[self.colonne + 1] == 'C' or ligne_perso_carte[self.colonne + 1] == 'M') and (ligne_perso_carte[self.colonne + 2] == ' ' or ligne_perso_carte[self.colonne + 2] == 'A'):
            self.niveau.majCarte(carte, 'droite_caisse')
            self.app.majAffichageObjet()



    # Déplacement à gauche du personnage
    def gauche(self, touche):
        self.initCoordonee()
        carte = self.niveau.getCarte()
        # Vérification de savoir si il peut aller à gauche
        ligne_perso_carte = carte[self.ligne]

        if ligne_perso_carte[self.colonne-1] == ' ' or ligne_perso_carte[self.colonne-1] == 'A' or ligne_perso_carte[self.colonne-1] == 'T':
            self.niveau.majCarte(carte, 'gauche') # Met la carte à jour
            self.app.majAffichageObjet()

        elif (ligne_perso_carte[self.colonne-1]=='C' or ligne_perso_carte[self.colonne-1]=='M') and (ligne_perso_carte[self.colonne-2]==' ' or ligne_perso_carte[self.colonne-2]=='A'):
            self.niveau.majCarte(carte, 'gauche_caisse')
            self.app.majAffichageObjet()


    # Déplacement en haut du personnage
    def haut(self, touche):
        self.initCoordonee()
        carte = self.niveau.getCarte()
        # Vérification de savoir si il peut monter
        try:
            ligne_dessus = carte[self.ligne - 1]
            ligne_dessus_deux = carte[self.ligne - 2]
            case_verif = ligne_dessus[self.colonne]
            case_verif_deux = ligne_dessus_deux[self.colonne]

            if case_verif == ' ' or case_verif == 'A' or case_verif == 'T':
                self.niveau.majCarte(carte, 'haut') # Met la carte à jour
                self.app.majAffichageObjet()

            elif (case_verif == 'C' or case_verif == 'M') and (case_verif_deux == ' ' or case_verif_deux == 'A'):
                self.niveau.majCarte(carte, 'haut_caisse')  # Met la carte à jour
                self.app.majAffichageObjet()
        except:
            # Test le IndexError
            pass

    # Déplacement en bas du personnage
    def bas(self, touche):
        self.initCoordonee()
        carte = self.niveau.getCarte()
        # Vérification de savoir si il peut descendre
        try :
            ligne_dessous = carte[self.ligne+1]
            ligne_dessous_deux = carte[self.ligne+2]
            case_verif = ligne_dessous[self.colonne]
            case_verif_deux = ligne_dessous_deux[self.colonne]

            # Le personnage descent
            if case_verif == ' ' or case_verif == 'A' or case_verif == 'T':
                self.niveau.majCarte(carte, 'bas') # Met la carte à jour
                self.app.majAffichageObjet()

            elif (case_verif == 'C' or case_verif == 'M') and (case_verif_deux == ' ' or case_verif_deux == 'A'):
                self.niveau.majCarte(carte, 'bas_caisse')  # Met la carte à jour
                self.app.majAffichageObjet()
        except IndexError:
            # Test le IndexError
            pass

    # Get Set des coordonées du perso
    def getCoordonnee(self):
        return self.colonne, self.ligne
    def setCoordonee(self, nouvelle_coordonee):
        self.colonne, self.ligne = nouvelle_coordonee