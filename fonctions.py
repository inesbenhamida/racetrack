from PIL import Image
from fltk import *
import main 

################ TACHE 1 #################### 

def afficher_piste(piste, trajectoire, options):
    """
    Permet d'afficher la piste et la trajectoire lorsque la voiture avance. Ainsi que les options possibles pour le prochain avancement.
    
    Paramètres:
    - piste : liste de listes représentant le plateau
    - trajectoire : liste de tuples comprenant des couples de coordonnées.
    - options : Liste de tuples des coordonnees des positions possibles pour le prochain choix
    
    Exemple:
    >>>afficher_piste(piste_liste,[(1,1),(2,1)])
    ##########
    #X.....###
    #X!....###
    #.!....##
    #####....#
    ####.....#
    ##......##
    #**...####
    #**...####
    ##########
    """
    
    if len(trajectoire) >= 2:
        for i in range(len(piste)):
            ligne_affichage = ""
            for j in range(len(piste[i])):
                if (i, j) in trajectoire:
                    ligne_affichage += 'X'
                elif (i, j) in options:
                    ligne_affichage += '!'
                else:
                    ligne_affichage += piste[i][j]
            print(ligne_affichage)
    else:
        for ligne in piste:
            print("".join(ligne))
            
            
def position_depart(piste):
     """
    Permet de trouver la position de départ en fonction des différentes maps, place la voiture l'élément ">".
    
    Paramètre :
    - piste : liste comprenant la map.
   
    Returns :
    - couple de tuples : correspond aux coordonnées du point de départ.
    """
     for i in range(len(piste)):
        for j in range(len(piste[i])):
            if piste[i][j] == '>':
                return (i, j)
     return None

def est_valide(piste, position):
    """
    Vérifie si il n'y a pas d'obstacles et si la voiture n'est pas rentrée en collision.
    
    Paramètres:
    - piste : liste de listes représentant le plateau
    - position : coordonnées de la voiture
    
    Exemple :
    >>>est_valide(piste_liste,(4,1))
    False
    """
    i, j = position
    return 0 <= i < len(piste) and 0 <= j < len(piste[0]) and piste[i][j] != '#'


###### NIVEAU 1 ###########

def vitesse(trajectoire):
    """
    Renvoie la vitesse de la voiture, en calculant la différence entre l'avant dernière position et la dernière.
    
    Paramètre :
    - trajectoire : liste de tuples comprenant des couples de coordonnées.
    
    Returns :
    -tuples : représente la vitesse de la voiture.
    
    Exemples :
    >>>vitesse([(1,1)]
    (0,0)
    >>>vitesse([(1, 1), (2, 1)])
    (1,0)
    """
    
    if len(trajectoire) < 2 :
        return (0,0)
    else :
        derniere_pos = trajectoire[-1]
        avant_derniere_pos = trajectoire[-2]
        return (derniere_pos[0] - avant_derniere_pos[0], derniere_pos[1] - avant_derniere_pos[1])
    

def verif_collision(piste,debut, fin):
    """
    Vérifie si il n'y a pas de collision en faisant appel à la fonction "est_valide".
    
    Paramètres :
    - debut : position de départ de la voiture.
    - fin : dernière position de la voiture.
    
    Returns :
    - booléen : True si il n'y a pas de collision, False sinon.
    """
    return est_valide(piste, fin)


def options(trajectoire, piste):
    """
    Donne les 9 positions possibles de déplacement.
    
    Paramètres :
    - trajectoire : liste de tuples comprenant des couples de coordonnées.
    - piste
    
    Returns :
    - liste de tuples : renvoyant la position de départ si la voiture est immobile, ou les 9 positions possible en comptaant la position principale.
    
    Exemples :
    >>>options([(1,1)])
    Options possibles: [(1, 1), (2, 1)]
    """
    if len(trajectoire) == 0:
         pos_depart = [position_depart(piste)]
         return pos_depart

    v = vitesse(trajectoire)
    point_principal = (trajectoire[-1][0] + v[0], trajectoire[-1][1] + v[1])
    
    pos_autorisees = []
    
    for i in range(-1, 2):
        for j in range(-1, 2):
            nouvelle_pos = (point_principal[0] + i, point_principal[1] + j)
            if verif_collision(piste,trajectoire[-1], nouvelle_pos):
                pos_autorisees.append(nouvelle_pos)

    return pos_autorisees
        

################ TACHE 2 ####################

###### NIVEAU 1 ###########

def charger(fichier):
    """
    Charge le fichier correspondant au circuit si il n'est pas vide ou introuvable. On ajoute ensuite le ficher a la liste "piste" pour pouvoir
    l'utiliser.
    
    Paramètre :
    - fichier : nom du fichier
    
    Returns :
    - liste de tuples : renvoie le fichier sous forme de piste.
    """
    try:
        with open(fichier, 'r') as f: 
            lignes = f.readlines()
    except FileNotFoundError:
        print("Le fichier désiré est introuvable ," , fichier)
        return None

    
    if len(lignes) == 0:
        print("Le fichier est vide")
        return None
    
    piste = []

    for ligne in lignes:
        caracteres_autorises = "#.*>"
        if all(caractere in caracteres_autorises for caractere in ligne.strip()):
            piste.append(ligne.strip())
        else:
            print("Le fichier contient un caractère inattendu :", fichier)
            return None
        
        
    return piste



def charger_piste_image(chemin_image):
    """
    Charge l'image de la piste et crée une structure de données représentant la piste.
    
    Paramètres :
    - chemin_image : chemin d'accès de l'image de la piste au format png.
    
    Returns :
    - piste : une liste de listes représentant la piste, où chaque élément correspond à une case de la piste.
    """    
    
    image = Image.open(chemin_image)
    largeur, hauteur = image.size
   
    piste = []

    for y in range(0,hauteur,20):
        ligne_piste = []
        for x in range(0,largeur,20):
            couleur_pixel = image.getpixel((x,y))
            
            if couleur_pixel == (0, 128, 128,255):  # Vert (zone de départ)
                ligne_piste.append('>')
            elif couleur_pixel == (128, 128, 128,255):  # Gris (zone d'arrivée)
                ligne_piste.append('*')
            elif couleur_pixel == (255, 255, 255,255):  # Blanc (piste)
                ligne_piste.append('.')
            else:
                ligne_piste.append('#')  # Autre couleur (obstacle)
        
        piste.append(ligne_piste)
    
    return piste

####TACHE 3############


taille=600

def ecran_accueil(taille):
    """
    Crée la fenêtre d'accueil avec les éléments graphiques.
    Paramètre :
    - taille (int): La taille de la fenêtre carrée en pixels.

    Returns:
    - None
    
    """
    image(300, 300, 'image_menu/course.png', largeur=600, hauteur=600, ancrage='center', tag='titre')
    image(290, 100, 'image_menu/rc.png', largeur=420, hauteur=90, ancrage='center', tag='titre')
    image(300, 300, 'image_menu/play.png', largeur=140, hauteur=55, ancrage='center', tag='jouer')
   

def gestion_clic(x, y):
    """
    Vérifie si le clic est dans la zone du bouton jouer et ouvre une nouvelle fenêtre si c'est le cas.
     
    Paramètres:
    - x (int): La position horizontale du clic.
    - y (int): La position verticale du clic.

    Returns:
    - None"""
    
    if 220 <= x <= 375 and 275 <= y <= 320:
        ouvrir_nouvelle_fenetre()

def ouvrir_nouvelle_fenetre():
    """
    Ouvre une nouvelle fenêtre pour la sélection de la piste.
    Ferme la fenêtre précédente, puis crée une nouvelle fenêtre carrée avec des éléments graphiques pour la sélection de la piste.
    Affiche trois options de pistes avec leurs images et rectangles de sélection.

    Returns:
    - None
    """
    
    ferme_fenetre()
    cree_fenetre(taille,taille)
    image(300, 300, 'image_menu/race-2.png',
          largeur=600, hauteur=600, ancrage='center', tag='titre')
    image(300, 100, 'image_menu/piste1.png',
          largeur=140, hauteur=55, ancrage='center', tag='piste1')
    
    image(300, 200, 'image_menu/piste2.png',
          largeur=140, hauteur=55, ancrage='center', tag='piste2')
    
    image(300, 300, 'image_menu/piste3.png',
          largeur=140, hauteur=55, ancrage='center', tag='piste3')
    
def gestion_clic_menu(x, y):
    """
    Vérifie si le clic est dans la zone d'un des boutons de sélection de piste et ouvre la grille si c'est le cas.
    
    Paramètres:
    - x (int): La position horizontale du clic.
    - y (int): La position verticale du clic.

    Returns:
    - None
    """ 
    ferme_fenetre()
    if 220 <= x <= 375 and 75 <= y <= 120:
        grille("maps-texte/map1.txt")
    elif 220 <= x <= 375 and 175 <= y <= 220:
        grille("maps-texte/map2.txt")
    elif 220 <= x <= 375 and 275 <= y <= 320:
        grille("maps-texte/map3.txt")


   
    
def gestion_clavier(ev, trajectoire):
    """
    Gère les actions du clavier pour annuler le dernier coup ou retourner au menu.
    
    Paramètres:
    - ev (événement): L'événement clavier généré.
    - trajectoire (list): La liste des mouvements effectués.
    
    Returns:
    - None
    """
    tev = touche(ev)
    if tev == 'BackSpace' and len(trajectoire) > 1:
        trajectoire.pop()
    elif tev == 'Escape':
        ferme_fenetre()
        main()  # Retour au menu principal



def grille(chemin):
    """
    Affiche la grille de jeu en fonction du contenu du fichier spécifié par `chemin`.

    Paramètres:
    chemin (str): Le chemin vers le fichier contenant la grille de jeu.

    Returns:
    - None
    """
    with open(chemin, "r") as file:
        lines = file.readlines()

    numero_ligne = len(lines)
    numero_colonne = len(lines[0].strip())

    largeur_fenetre = 600
    hauteur_fenetre = 600
    case = min(largeur_fenetre / numero_colonne, hauteur_fenetre / numero_ligne)
    cree_fenetre(int(numero_colonne * case), int(numero_ligne * case))

    piste = [line.strip() for line in lines]
    trajectoire = [position_depart(piste)]
    options_actuelles = options(trajectoire, piste)
    victoire = False  
    

    def redessiner(victoire):
        """
        Redessine la grille de jeu avec les éléments actuels de la trajectoire et affiche un écran de victoire si nécessaire.

        Parameters:
        victoire (bool): Un booléen indiquant si le joueur a atteint la victoire ou non.

        Returns:
        None
        """
        efface_tout()
        for i, line in enumerate(piste):
            for j, symbole in enumerate(line):
                x = int(j * case)
                y = int(i * case)
                couleur = determine_couleur(symbole)
                rectangle(x, y, x + case, y + case, remplissage=couleur)
                if (i, j) in trajectoire or (i, j) in options_actuelles or couleur == "cyan":
                    cercle(x + case / 2, y + case / 2, case / 4, remplissage="purple")
        for i in range(len(trajectoire) - 1):
                debut = trajectoire[i]
                fin = trajectoire[i + 1]
                vitesse = (fin[0] - debut[0], fin[1] - debut[1])
                couleur_vitesse = calculer_couleur_vitesse(vitesse)
                ligne(int(debut[1] * case + case / 2), int(debut[0] * case + case / 2),
                      int(fin[1] * case + case / 2), int(fin[0] * case + case / 2), couleur=couleur_vitesse, epaisseur = 4)
        if victoire:
            image(300, 200, 'image_menu/victoire.png',
                                  largeur=340, hauteur=80, ancrage='center', tag='victoire')
            image(300, 320, 'image_menu/menu.png',
                                  largeur=170, hauteur=50, ancrage='center', tag='menu')

    redessiner(victoire)

    while True:
        ev = attend_ev()
        tev = type_ev(ev)
        if tev == 'ClicGauche':
            x, y = int(abscisse(ev)), int(ordonnee(ev))
            if victoire and 300 <= x <= 320 and 300 <= y <= 320:
                ferme_fenetre()
                ouvrir_nouvelle_fenetre()  # Retour au menu principal
                break
            else:
                nouvelle_position = (int(y // case),int( x // case))
                if nouvelle_position in options_actuelles and not victoire:
                    trajectoire.append(nouvelle_position)
                    if piste[int(y // case)][int(x // case)] == '*':
                        victoire = True
                        options_actuelles = []  # Aucune option possible après la victoire
                    else:
                        options_actuelles = options(trajectoire, piste)
                    redessiner(victoire)
        elif tev == 'Touche':
            if touche(ev) == 'BackSpace' and len(trajectoire) > 1:
                trajectoire.pop()
                options_actuelles = options(trajectoire, piste)
                redessiner(victoire)
            elif touche(ev) == 'Escape':
                ferme_fenetre()
                main()
                break
        elif tev == 'Quitte':
            break

    ferme_fenetre()


def determine_couleur(symbole):
    """
    Détermine la couleur de remplissage basée sur le caractère.
    
    Paramètre :
    - symbole (str): Le caractère à partir duquel la couleur est déterminée.

    Returns:
    - str: La couleur de remplissage correspondant au caractère.
    """
    
    
    if symbole == '#':
        return 'green'
    elif symbole == '.':
        return 'white'
    elif symbole == '*':
        return 'gray'
    elif symbole == '>':
        return 'cyan'
    else:
        return 'black'  #Affiche noir si un caractère inconnu apparait
   

def calculer_couleur_vitesse(vitesse):
    """
    Calcule la couleur en fonction de la vitesse de la voiture.
    La couleur codée en hexadécimal au format '#RRGGBB', où la couleur rouge (R) 
    diminue et la couleur verte (G) augmente avec l'augmentation de la vitesse.

    La couleur varie du jaune au vert en fonction de la norme de la vitesse :
    - Vitesse faible : couleur jaune (#ffff00)
    - Vitesse élevée : couleur verte (#00ff00)


    Paramètres:

    - vitesse : tuple
        

    Returns :
    - str
    """
    max_vitesse = 4  # Vitesse maximale pour normaliser
    norme_vitesse = min((abs(vitesse[0]) + abs(vitesse[1])) / (2 * max_vitesse), 1)
    r = int(255 * (1 - norme_vitesse))
    g = int(255 * norme_vitesse)
    return f'#{r:02x}{g:02x}00'


###Tache 4####
def solveur(piste, trajectoire, visite):
    """
    Résout le parcours d'un piste en recherchant une trajectoire valide jusqu'à l'arrivée.

    Paramètres :
    - piste : liste de chaînes de caractères représentant le circuit.
    - trajectoire : liste de tuples représentant les positions parcourues.
    - visite : ensemble de tuples représentant les positions et vitesses déjà visitées.

    Return :
    - bool : True si une trajectoire vers l'arrivée est trouvée, sinon False.
    """
    if not trajectoire:
        return False
    
    position_actuelle = trajectoire[-1]
    vitesse_actuelle = vitesse(trajectoire)
    c = (position_actuelle, vitesse_actuelle)
    
    if est_arrivee(position_actuelle, piste):
        print("Trajectoire trouvée:",trajectoire)
        return True
    
    if c in visite :
        return False
    else:
        visite.add(c)
    
    for o in options(trajectoire,piste):
        nouvelle_trajectoire = trajectoire+[o]
        if solveur(piste, nouvelle_trajectoire, visite):
            return True
    return False

def est_arrivee(position, piste):
     if 0 <= position[0] < len(piste) and 0 <= position[1] < len(piste[0]):
        return piste[position[0]][position[1]] == '*'
     return False



piste = charger("maps-texte/map_mini.txt")
trajectoire_initiale = [position_depart(piste)]
visite = set()
if solveur(piste, trajectoire_initiale, visite):
    print("Solution trouvée")
else:
    print("Aucune solution trouvée")
solveur(piste, trajectoire_initiale, visite)


 

########################################

piste_liste = [
    ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
    ['#', '>', '.', '.', '.', '.', '.', '#', '#', '#'],
    ['#', '>', '.', '.', '.', '.', '.', '#', '#', '#'],
    ['#', '.', '.', '.', '.', '.', '.', '.', '#', '#'],
    ['#', '#', '#', '#', '#', '.', '.', '.', '.', '#'],
    ['#', '#', '#', '#', '.', '.', '.', '.', '.', '#'],
    ['#', '#', '.', '.', '.', '.', '.', '.', '#', '#'],
    ['#', '*', '*', '.', '.', '.', '#', '#', '#', '#'],
    ['#', '*', '*', '.', '.', '.', '#', '#', '#', '#'],
    ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#']
]







