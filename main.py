import tkinter as tk
from fltk import *
from fonctions import *



def main():
    """
    Fonction principale du programme.

    Crée une fenêtre carrée, affiche l'écran d'accueil, puis attend les événements.
    Si un clic gauche est détecté, la fonction `gestion_clic` est appelée avec les coordonnées du clic.
    Si un clic droit est détecté, la fonction `gestion_clic_menu` est appelée avec les coordonnées du clic.
    La boucle continue jusqu'à ce qu'un événement de fermeture de fenêtre soit détecté.

    Returns:
    - None
    """

    
    cree_fenetre(taille, taille)
    ecran_accueil(taille)

    while True:
        ev = attend_ev()
        tev = type_ev(ev)
        if tev == 'Quitte':
            break  
        elif tev == 'ClicGauche':
            x, y = abscisse(ev), ordonnee(ev)
            gestion_clic(x, y)
   
        elif tev == 'ClicDroit':
             x, y = abscisse(ev), ordonnee(ev)
             gestion_clic_menu(x, y)
    ferme_fenetre()



if __name__ == '__main__':
    main()























