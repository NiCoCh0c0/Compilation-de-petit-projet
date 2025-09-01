import InitalisationNiveau
import Personnage
import AffichageCarte


# Crée la carte sous format de tableau
niveau = InitalisationNiveau.InitialisationNiveau()
# Crée la partie graphique (tkinter)
mon_app = AffichageCarte.AffichageCarte(640,640, niveau)

# Crée le personnage
mon_perso = Personnage.Personnage(mon_app)

# Lance la boucle infini
mon_app.initEcran()