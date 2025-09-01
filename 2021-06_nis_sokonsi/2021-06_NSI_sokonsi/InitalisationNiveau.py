"""
La carte se présente sous un format de tableau (liste dans des listes)
Chaque caractère correspond à un élément précis:
    - P : le personnage
    - Z : le personnage sur un checkpoint
    - K : le personnage sur un téléporteur

    - C : une caisse
    - M : une caisse sur un checkpoint

    - X : un mur
    - ' '(un espace) : du vide (plancher)
    - A : un checkpoint
    - T : un téléporteur

IMPORTANT : les caisses ne peuvent pas utiliser les téléporteurs (le déplacement est rendu impossible)

Il y a 8 types de déplacements :
    - Sans pousser de caisse :
        - gauche
        - droite
        - haut
        - bas
    - En poussant une caisse:
        - droite_caisse
        - gauche_caisse
        - haut_caisse
        - bas_caisse
Chacun prends en compte tout les scénarios dans lesquels on peut se confronter (seulement si le déplacement est possible)

Le système de sauvegarde est implémenté dans cette classe car la progression est définie par rapport au niveau
La sauvegarde se résume au fichier 'sauvegarde.txt' qui contient UNIQUEMENT l'index de la dernière carte jouée

Pour le stockage des cartes, il existe deux fichiers (modification possible dans la fonction listeCarte()) :
    - 'CarteTest.txt' : qui test toute les collisions possible
    - 'SauvegardeCarte.txt' : qui est le fichier contenant les cartes du jeu
!!! Une carte ne doit comprendre UNIQUEMENT DEUX téléporteurs

Les cartes peuvent être en (10*10) ou (20*20)
A la fin de la carte, il faut mettre une ligne avec au moins un tiret (-)
"""
class InitialisationNiveau:

    def __init__(self):

        self.liste_carte = self.listeCarte()

        try:
            # Essaye de lire le fichier sauvegarde (il se peut qu'il ne soit pas crée ou qu'il soit vide)
            with open('sauvegarde.txt', 'r') as sauvegarde:
                num_niveau = int(sauvegarde.read())
                self.carte = self.liste_carte[num_niveau]
                self.index_carte = num_niveau
        except:
            # Commence depuis le début
            self.carte = self.liste_carte[0]
            self.index_carte = 0


    # Mise à jour de la carte lors d'un déplacement du personnage
    def majCarte(self, carte, deplacement):
        utilisation_tp = False
        coordonnee_tp = []
        mouvement_P = False # Permet d'éviter des boucles infinies pour le déplacement vers le bas
        nouvelle_carte = []
        # Récupération des lignes de la carte pour avoir son "ordonnée" sur la carte (de haut en bas)
        for ligne in range(len(carte)):
            ma_ligne = carte[ligne]
            ma_ligne_liste = list(ma_ligne) # Comme une string ne peut être modifié, il faut la transformer en liste

            for colonne in range(len(ma_ligne)): # Récupération de la colonne pour avoir son "abscisse" sur la carte (de gauche à droite)
                if ma_ligne[colonne] == 'T':
                    coordonnee_tp.append([ligne, colonne])
                if deplacement == 'gauche':
                    # Si trouve le joueur sans être sur un checkpoint
                    if ma_ligne[colonne] == 'P':
                        # Si la case où il se rend est un check point
                        if ma_ligne[colonne-1] == 'A':
                            ma_ligne_liste[colonne] = ' '
                            ma_ligne_liste[colonne - 1] = 'Z'
                        elif ma_ligne[colonne-1] == 'T':
                            ma_ligne_liste[colonne] = ' '
                            ma_ligne_liste[colonne - 1] = 'T'
                            utilisation_tp = True
                            coordonnee_perso = (ligne, colonne-1)
                        else:
                            ma_ligne_liste[colonne] = ' '
                            ma_ligne_liste[colonne - 1] = 'P'
                    # Si trouve le joueur sans être sur un checkpoint
                    elif ma_ligne[colonne] == 'Z':
                        if ma_ligne[colonne-1] == 'A':
                            ma_ligne_liste[colonne] = 'A'
                            ma_ligne_liste[colonne - 1] = 'Z'
                        elif ma_ligne[colonne - 1] == 'T':
                            ma_ligne_liste[colonne] = 'A'
                            ma_ligne_liste[colonne - 1] = 'T'
                            utilisation_tp = True
                            coordonnee_perso = (ligne, colonne - 1)
                        else:
                            ma_ligne_liste[colonne] = 'A'
                            ma_ligne_liste[colonne - 1] = 'P'
                    # Si trouve le joueur sur un tp
                    elif ma_ligne[colonne] == 'K':
                        if ma_ligne[colonne - 1] == 'A':
                            ma_ligne_liste[colonne] = 'T'
                            ma_ligne_liste[colonne - 1] = 'Z'
                        elif ma_ligne[colonne - 1] == 'T':
                            ma_ligne_liste[colonne] = 'T'
                            ma_ligne_liste[colonne - 1] = 'K'
                        else:
                            ma_ligne_liste[colonne] = 'T'
                            ma_ligne_liste[colonne - 1] = 'P'

                    ma_ligne = ''.join(ma_ligne_liste) # Transforme la liste en string


                elif deplacement == 'droite':
                    # On raisonne avec -colonne pour éviter des problèmes (on raisonne de droite à gauche)
                    # Même chose que pour gauche (cf. au dessus)
                    if ma_ligne[-colonne] == 'P':
                        if ma_ligne[-colonne+1] == 'A':
                            ma_ligne_liste[-colonne] = ' '
                            ma_ligne_liste[-colonne + 1] = 'Z'
                        elif ma_ligne[-colonne+1] == 'T':
                            ma_ligne_liste[-colonne] = ' '
                            ma_ligne_liste[-colonne + 1] = 'T'
                            utilisation_tp = True
                            coordonnee_perso = (ligne, len(ma_ligne)-colonne + 1)
                        else:
                            ma_ligne_liste[-colonne] = ' '
                            ma_ligne_liste[-colonne+1] = 'P'

                    elif ma_ligne[-colonne] == 'Z':
                        if ma_ligne[-colonne + 1] == 'A':
                            ma_ligne_liste[-colonne] = 'A'
                            ma_ligne_liste[-colonne + 1] = 'Z'
                        elif ma_ligne[-colonne + 1] == 'T':
                            ma_ligne_liste[-colonne] = 'A'
                            ma_ligne_liste[-colonne + 1] = 'T'
                            utilisation_tp = True
                            coordonnee_perso = (ligne, len(ma_ligne)-colonne + 1)
                        else:
                            ma_ligne_liste[-colonne] = 'A'
                            ma_ligne_liste[-colonne + 1] = 'P'
                    elif ma_ligne[-colonne] == 'K':
                        if ma_ligne[-colonne + 1] == 'A':
                            ma_ligne_liste[-colonne] = 'T'
                            ma_ligne_liste[-colonne + 1] = 'Z'
                        elif ma_ligne[-colonne + 1] == 'T':
                            ma_ligne_liste[-colonne] = 'T'
                            ma_ligne_liste[-colonne + 1] = 'K'
                        else:
                            ma_ligne_liste[-colonne] = 'T'
                            ma_ligne_liste[-colonne + 1] = 'P'

                    ma_ligne = ''.join(ma_ligne_liste)




                elif deplacement == 'haut':
                    try:
                        # Le try teste le cas de l'index error
                        ligne_dessus = list(nouvelle_carte[ligne - 1])
                    except:
                        # Si une exception est levée on ne fait rien
                        pass
                    else:
                        # Si le try est "réussi"
                        # Même chose que pour gauche/droite mais avec un raisonnement sur les lignes et non plus sur les colonnes
                        if ma_ligne[colonne] == 'P':
                            if ligne_dessus[colonne] == 'A':
                                ma_ligne_liste[colonne] = ' '
                                ligne_dessus[colonne] = 'Z'
                            elif ligne_dessus[colonne] == 'T':
                                ma_ligne_liste[colonne] = ' '
                                ligne_dessus[colonne] = 'T'
                                utilisation_tp = True
                                coordonnee_perso = (ligne-1, colonne)
                            else:
                                ma_ligne_liste[colonne] = ' '
                                ligne_dessus[colonne] = 'P'
                            ligne_dessus = ''.join(ligne_dessus)
                            # Modification de ligne-1
                            nouvelle_carte.pop()
                            nouvelle_carte.append(ligne_dessus)

                        elif ma_ligne[colonne] == 'Z':
                            if ligne_dessus[colonne] == 'A':
                                ma_ligne_liste[colonne] = 'A'
                                ligne_dessus[colonne] = 'Z'
                            elif ligne_dessus[colonne] == 'T':
                                ma_ligne_liste[colonne] = 'A'
                                ligne_dessus[colonne] = 'T'
                                utilisation_tp = True
                                coordonnee_perso = (ligne-1, colonne)
                            else:
                                ma_ligne_liste[colonne] = 'A'
                                ligne_dessus[colonne] = 'P'
                            ligne_dessus = ''.join(ligne_dessus)
                            # Modification de ligne-1
                            nouvelle_carte.pop()
                            nouvelle_carte.append(ligne_dessus)

                        elif ma_ligne[colonne] == 'K':
                            if ligne_dessus[colonne] == 'A':
                                ma_ligne_liste[colonne] = 'T'
                                ligne_dessus[colonne] = 'Z'
                            elif ligne_dessus[colonne] == 'T':
                                ma_ligne_liste[colonne] = 'T'
                                ligne_dessus[colonne] = 'K'
                            else:
                                ma_ligne_liste[colonne] = 'T'
                                ligne_dessus[colonne] = 'P'
                            ligne_dessus = ''.join(ligne_dessus)
                            # Modification de ligne-1
                            nouvelle_carte.pop()
                            nouvelle_carte.append(ligne_dessus)

                        ma_ligne = ''.join(ma_ligne_liste)

                elif deplacement == 'bas':
                    try:
                        # Le try évite l'index error
                        ligne_dessous = list(carte[ligne + 1])
                    except:
                        # Si une exception est levée on ne fait rien
                        pass
                    else:
                        # Si aucune exception levée
                        if mouvement_P == False:
                            if ma_ligne[colonne] == 'P' :
                                if ligne_dessous[colonne] == 'A':
                                    ma_ligne_liste[colonne] = ' '
                                    ligne_dessous[colonne] = 'Z'
                                elif ligne_dessous[colonne] == 'T':
                                    ma_ligne_liste[colonne] = ' '
                                    ligne_dessous[colonne] = 'T'
                                    utilisation_tp = True
                                    coordonnee_perso = (ligne + 1, colonne)
                                else:
                                    ma_ligne_liste[colonne] = ' '
                                    ligne_dessous[colonne] = 'P'
                                ligne_dessous = ''.join(ligne_dessous)
                                # Modification de la ligne suivante
                                carte[ligne+1] = ligne_dessous
                                ma_ligne = ''.join(ma_ligne_liste)
                                mouvement_P = True

                            elif ma_ligne[colonne] == 'Z':
                                if ligne_dessous[colonne] == 'A':
                                    ma_ligne_liste[colonne] = 'A'
                                    ligne_dessous[colonne] = 'Z'
                                elif ligne_dessous[colonne] == 'T':
                                    ma_ligne_liste[colonne] = 'A'
                                    ligne_dessous[colonne] = 'T'
                                    utilisation_tp = True
                                    coordonnee_perso = (ligne + 1, colonne)
                                else:
                                    ma_ligne_liste[colonne] = 'A'
                                    ligne_dessous[colonne] = 'P'
                                ligne_dessous = ''.join(ligne_dessous)
                                # Modification de la ligne suivante
                                carte[ligne+1] = ligne_dessous
                                ma_ligne = ''.join(ma_ligne_liste)
                                mouvement_P = True

                            elif ma_ligne[colonne] == 'K':
                                if ligne_dessous[colonne] == 'A':
                                    ma_ligne_liste[colonne] = 'T'
                                    ligne_dessous[colonne] = 'Z'
                                elif ligne_dessous[colonne] == 'T':
                                    ma_ligne_liste[colonne] = 'T'
                                    ligne_dessous[colonne] = 'K'
                                else:
                                    ma_ligne_liste[colonne] = 'T'
                                    ligne_dessous[colonne] = 'P'
                                ligne_dessous = ''.join(ligne_dessous)
                                # Modification de la ligne suivante
                                carte[ligne+1] = ligne_dessous
                                ma_ligne = ''.join(ma_ligne_liste)
                                mouvement_P = True




                elif deplacement == 'droite_caisse':
                    # Si le déplacement est droite MAIS en poussant une caisse
                    if ma_ligne[-colonne-1] == 'P' or ma_ligne[-colonne-1] == 'Z' or ma_ligne[-colonne-1] == 'K':
                        # Si on trouve le Personnage
                        if ma_ligne[-colonne] == 'C':
                            # Si la caisse à pousser n'est pas sur un check point
                            if ma_ligne[-colonne-1] == 'Z':
                                if ma_ligne[-colonne+1] == 'A':
                                    ma_ligne_liste[-colonne - 1] = 'A'
                                    ma_ligne_liste[-colonne] = 'P'
                                    ma_ligne_liste[-colonne + 1] = 'M'
                                else:
                                    ma_ligne_liste[-colonne-1] = 'A'
                                    ma_ligne_liste[-colonne] = 'P'
                                    ma_ligne_liste[-colonne + 1] = 'C'
                            elif ma_ligne[-colonne-1] == 'K':
                                if ma_ligne[-colonne+1] == 'A':
                                    ma_ligne_liste[-colonne - 1] = 'T'
                                    ma_ligne_liste[-colonne] = 'P'
                                    ma_ligne_liste[-colonne + 1] = 'M'
                                else:
                                    ma_ligne_liste[-colonne-1] = 'T'
                                    ma_ligne_liste[-colonne] = 'P'
                                    ma_ligne_liste[-colonne + 1] = 'C'
                            else:
                                if ma_ligne[-colonne+1] == 'A':
                                    ma_ligne_liste[-colonne - 1] = ' '
                                    ma_ligne_liste[-colonne] = 'P'
                                    ma_ligne_liste[-colonne + 1] = 'M'
                                else:
                                    ma_ligne_liste[-colonne-1] = ' '
                                    ma_ligne_liste[-colonne] = 'P'
                                    ma_ligne_liste[-colonne + 1] = 'C'

                        elif ma_ligne[-colonne] == 'M':
                            # Si la caisse à pousser est sur un check point
                            if ma_ligne[-colonne-1] == 'Z':
                                if ma_ligne[-colonne+1] == 'A':
                                    ma_ligne_liste[-colonne - 1] = 'A'
                                    ma_ligne_liste[-colonne] = 'Z'
                                    ma_ligne_liste[-colonne + 1] = 'M'
                                else:
                                    ma_ligne_liste[-colonne-1] = 'A'
                                    ma_ligne_liste[-colonne] = 'Z'
                                    ma_ligne_liste[-colonne + 1] = 'C'
                            elif ma_ligne[-colonne-1] == 'K':
                                if ma_ligne[-colonne+1] == 'A':
                                    ma_ligne_liste[-colonne - 1] = 'T'
                                    ma_ligne_liste[-colonne] = 'Z'
                                    ma_ligne_liste[-colonne + 1] = 'M'
                                else:
                                    ma_ligne_liste[-colonne-1] = 'T'
                                    ma_ligne_liste[-colonne] = 'Z'
                                    ma_ligne_liste[-colonne + 1] = 'C'
                            else:
                                if ma_ligne[-colonne+1] == 'A':
                                    ma_ligne_liste[-colonne - 1] = ' '
                                    ma_ligne_liste[-colonne] = 'Z'
                                    ma_ligne_liste[-colonne + 1] = 'M'
                                else:
                                    ma_ligne_liste[-colonne-1] = ' '
                                    ma_ligne_liste[-colonne] = 'Z'
                                    ma_ligne_liste[-colonne + 1] = 'C'

                        ma_ligne = ''.join(ma_ligne_liste)


                elif deplacement == 'gauche_caisse':
                    if ma_ligne[colonne] == 'P' or ma_ligne[colonne] == 'Z' or ma_ligne[colonne] == 'K':
                        # Si on trouve le personnage
                        if ma_ligne[colonne - 1] == 'C':
                            # Si la caisse à pousser n'est pas sur un check point
                            if ma_ligne[colonne] == 'Z':
                                if ma_ligne[colonne - 2] == 'A':
                                    ma_ligne_liste[colonne] = 'A'
                                    ma_ligne_liste[colonne - 1] = 'P'
                                    ma_ligne_liste[colonne - 2] = 'M'
                                else:
                                    ma_ligne_liste[colonne] = 'A'
                                    ma_ligne_liste[colonne - 1] = 'P'
                                    ma_ligne_liste[colonne - 2] = 'C'
                            elif ma_ligne[colonne] == 'K':
                                if ma_ligne[colonne - 2] == 'A':
                                    ma_ligne_liste[colonne] = 'T'
                                    ma_ligne_liste[colonne - 1] = 'P'
                                    ma_ligne_liste[colonne - 2] = 'M'
                                else:
                                    ma_ligne_liste[colonne] = 'T'
                                    ma_ligne_liste[colonne - 1] = 'P'
                                    ma_ligne_liste[colonne - 2] = 'C'
                            else:
                                if ma_ligne[colonne - 2] == 'A':
                                    ma_ligne_liste[colonne] = ' '
                                    ma_ligne_liste[colonne - 1] = 'P'
                                    ma_ligne_liste[colonne - 2] = 'M'
                                else:
                                    ma_ligne_liste[colonne] = ' '
                                    ma_ligne_liste[colonne - 1] = 'P'
                                    ma_ligne_liste[colonne - 2] = 'C'

                        elif ma_ligne[colonne - 1] == 'M':
                            # Si la caisse à pousser est pas un check point
                            if ma_ligne[colonne] == 'Z':
                                if ma_ligne[colonne - 2] == 'A':
                                    ma_ligne_liste[colonne] = 'A'
                                    ma_ligne_liste[colonne - 1] = 'Z'
                                    ma_ligne_liste[colonne - 2] = 'M'
                                else:
                                    ma_ligne_liste[colonne] = 'A'
                                    ma_ligne_liste[colonne - 1] = 'Z'
                                    ma_ligne_liste[colonne - 2] = 'C'
                            elif ma_ligne[colonne] == 'K':
                                if ma_ligne[colonne - 2] == 'A':
                                    ma_ligne_liste[colonne] = 'T'
                                    ma_ligne_liste[colonne - 1] = 'Z'
                                    ma_ligne_liste[colonne - 2] = 'M'
                                else:
                                    ma_ligne_liste[colonne] = 'T'
                                    ma_ligne_liste[colonne - 1] = 'Z'
                                    ma_ligne_liste[colonne - 2] = 'C'
                            else:
                                if ma_ligne[colonne - 2] == 'A':
                                    ma_ligne_liste[colonne] = ' '
                                    ma_ligne_liste[colonne - 1] = 'Z'
                                    ma_ligne_liste[colonne - 2] = 'M'
                                else:
                                    ma_ligne_liste[colonne] = ' '
                                    ma_ligne_liste[colonne - 1] = 'Z'
                                    ma_ligne_liste[colonne - 2] = 'C'
                        ma_ligne = ''.join(ma_ligne_liste)


                elif deplacement == 'haut_caisse':
                    try:
                        # Permet de tester un index error (PEUT ETRE A SUPPR)
                        ligne_dessus = list(nouvelle_carte[ligne - 1])
                        ligne_dessus_deux = list(nouvelle_carte[ligne - 2])
                    except:
                        # Si il y a une erreur on ne fait rien
                        pass
                    else:
                        # Si pas d'erreur
                        if ma_ligne[colonne] == 'P' or ma_ligne[colonne] == 'Z' or ma_ligne[colonne] == 'K':
                            # Si on trouve le Personnage
                            if carte[ligne-1][colonne] == 'C':
                                # Si la caisse à pousser n'est pas sur un check point
                                if ma_ligne[colonne] == 'Z':
                                    if carte[ligne-2][colonne] == 'A':
                                        ma_ligne_liste[colonne] = 'A'
                                        ligne_dessus[colonne] = 'P'
                                        ligne_dessus_deux[colonne] = 'M'
                                    else:
                                        ma_ligne_liste[colonne] = 'A'
                                        ligne_dessus[colonne] = 'P'
                                        ligne_dessus_deux[colonne] = 'C'
                                elif ma_ligne[colonne] == 'K':
                                    if carte[ligne-2][colonne] == 'A':
                                        ma_ligne_liste[colonne] = 'T'
                                        ligne_dessus[colonne] = 'P'
                                        ligne_dessus_deux[colonne] = 'M'
                                    else:
                                        ma_ligne_liste[colonne] = 'T'
                                        ligne_dessus[colonne] = 'P'
                                        ligne_dessus_deux[colonne] = 'C'
                                else:
                                    if carte[ligne-2][colonne] == 'A':
                                        ma_ligne_liste[colonne] = ' '
                                        ligne_dessus[colonne] = 'P'
                                        ligne_dessus_deux[colonne] = 'M'
                                    else:
                                        ma_ligne_liste[colonne] = ' '
                                        ligne_dessus[colonne] = 'P'
                                        ligne_dessus_deux[colonne] = 'C'

                            elif carte[ligne-1][colonne] == 'M':
                                # Si la caisse à pousser est sur un check point
                                if ma_ligne[colonne] == 'Z':
                                    if carte[ligne - 2][colonne] == 'A':
                                        ma_ligne_liste[colonne] = 'A'
                                        ligne_dessus[colonne] = 'Z'
                                        ligne_dessus_deux[colonne] = 'M'
                                    else:
                                        ma_ligne_liste[colonne] = 'A'
                                        ligne_dessus[colonne] = 'Z'
                                        ligne_dessus_deux[colonne] = 'C'
                                elif ma_ligne[colonne] == 'K':
                                    if carte[ligne-2][colonne] == 'A':
                                        ma_ligne_liste[colonne] = 'T'
                                        ligne_dessus[colonne] = 'Z'
                                        ligne_dessus_deux[colonne] = 'M'
                                    else:
                                        ma_ligne_liste[colonne] = 'T'
                                        ligne_dessus[colonne] = 'Z'
                                        ligne_dessus_deux[colonne] = 'C'
                                else:
                                    if carte[ligne-2][colonne] == 'A':
                                        ma_ligne_liste[colonne] = ' '
                                        ligne_dessus[colonne] = 'Z'
                                        ligne_dessus_deux[colonne] = 'M'
                                    else:
                                        ma_ligne_liste[colonne] = ' '
                                        ligne_dessus[colonne] = 'Z'
                                        ligne_dessus_deux[colonne] = 'C'

                            # Modification de ligne-1 et ligne-2
                            ligne_dessus = ''.join(ligne_dessus)
                            ligne_dessus_deux = ''.join(ligne_dessus_deux)
                            nouvelle_carte.pop()
                            nouvelle_carte.pop()
                            nouvelle_carte.append(ligne_dessus_deux)
                            nouvelle_carte.append(ligne_dessus)

                            ma_ligne = ''.join(ma_ligne_liste)


                elif deplacement == 'bas_caisse':
                    if mouvement_P == False:
                        try:
                            # Le try évite l'index error
                            ligne_dessous = list(carte[ligne + 1])
                            ligne_dessous_deux = list(carte[ligne + 2])

                        except:
                            pass
                        else:
                            if ma_ligne[colonne] == 'P' or ma_ligne[colonne] == 'Z' or ma_ligne[colonne] == 'K':
                                mouvement_P = True
                                if carte[ligne + 1][colonne] == 'C':
                                    if ma_ligne[colonne] == 'Z':
                                        if carte[ligne + 2][colonne] == 'A':
                                            ma_ligne_liste[colonne] = 'A'
                                            ligne_dessous[colonne] = 'P'
                                            ligne_dessous_deux[colonne] = 'M'
                                        else:
                                            ma_ligne_liste[colonne] = 'A'
                                            ligne_dessous[colonne] = 'P'
                                            ligne_dessous_deux[colonne] = 'C'
                                    elif ma_ligne[colonne] == 'K':
                                        if carte[ligne + 2][colonne] == 'A':
                                            ma_ligne_liste[colonne] = 'T'
                                            ligne_dessous[colonne] = 'P'
                                            ligne_dessous_deux[colonne] = 'M'
                                        else:
                                            ma_ligne_liste[colonne] = 'T'
                                            ligne_dessous[colonne] = 'P'
                                            ligne_dessous_deux[colonne] = 'C'
                                    else:
                                        if carte[ligne + 2][colonne] == 'A':
                                            ma_ligne_liste[colonne] = ' '
                                            ligne_dessous[colonne] = 'P'
                                            ligne_dessous_deux[colonne] = 'M'
                                        else:
                                            ma_ligne_liste[colonne] = ' '
                                            ligne_dessous[colonne] = 'P'
                                            ligne_dessous_deux[colonne] = 'C'


                                elif carte[ligne + 1][colonne] == 'M':

                                    # Si la caisse à pousser est sur un check point
                                    if ma_ligne[colonne] == 'Z':
                                        if carte[ligne + 2][colonne] == 'A':
                                            ma_ligne_liste[colonne] = 'A'
                                            ligne_dessous[colonne] = 'Z'
                                            ligne_dessous_deux[colonne] = 'M'
                                        else:
                                            ma_ligne_liste[colonne] = 'A'
                                            ligne_dessous[colonne] = 'Z'
                                            ligne_dessous_deux[colonne] = 'C'
                                    elif ma_ligne[colonne] == 'K':
                                        if carte[ligne + 2][colonne] == 'A':
                                            ma_ligne_liste[colonne] = 'T'
                                            ligne_dessous[colonne] = 'Z'
                                            ligne_dessous_deux[colonne] = 'M'
                                        else:
                                            ma_ligne_liste[colonne] = 'T'
                                            ligne_dessous[colonne] = 'Z'
                                            ligne_dessous_deux[colonne] = 'C'
                                    else:
                                        if carte[ligne + 2][colonne] == 'A':
                                            ma_ligne_liste[colonne] = ' '
                                            ligne_dessous[colonne] = 'Z'
                                            ligne_dessous_deux[colonne] = 'M'
                                        else:
                                            ma_ligne_liste[colonne] = ' '
                                            ligne_dessous[colonne] = 'Z'
                                            ligne_dessous_deux[colonne] = 'C'


                            ligne_dessous = ''.join(ligne_dessous)
                            ligne_dessous_deux = ''.join(ligne_dessous_deux)
                            # Modification de la ligne suivante
                            carte[ligne+1] = ligne_dessous
                            carte[ligne+2] = ligne_dessous_deux
                            ma_ligne = ''.join(ma_ligne_liste)


            nouvelle_carte.append(ma_ligne) # Ajout de la nouvelle ligne (modifié ou non)

        if utilisation_tp == True:
            # Si le téléporteur a été utilisé
            for y, x in coordonnee_tp: # Crée un tupple qui correspond aux coordonnées des deux téléporteurs
                if (y,x) != coordonnee_perso:
                    # Modifie la carte
                    ligne = list(nouvelle_carte[y])
                    ligne[x] = 'K'
                    ma_ligne = ''.join(ligne)
                    nouvelle_carte[y] = ma_ligne
        self.carte = nouvelle_carte


    # Get/Set
    def getCarte(self):
        return self.carte
    def setCarte(self, nouvelle_carte):
        self.carte = nouvelle_carte
    def getListeCarte(self):
        return self.liste_carte
    def getIndexCarte(self):
        return self.index_carte


    def listeCarte(self): # Récupère l'ensemble des cartes
        liste_carte = []
        carte = []
        with open('SauvegardeCarte.txt', 'r') as cartes: # CarteTest.txt
            nb_ligne = 0
            nb_carte = 0
            for ligne in cartes:
                nb_ligne += 1
                if ligne[0] == '-':
                    nb_carte += 1
            cartes.seek(0)
            continuer = True
            for i in range(nb_carte):
                while continuer:
                    contenue_ligne = cartes.readline()[0:-1]
                    if contenue_ligne[0] == '-':
                        continuer = False
                    else:
                        carte.append(contenue_ligne)
                liste_carte.append(carte)
                carte = []
                continuer = True
        return liste_carte