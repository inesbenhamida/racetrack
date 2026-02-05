from PIL import Image


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
    - couple de tuples : correspond aux coordonnées du point de départ ou None s'il n y en a pas.
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
    - position : coordonnées de la voNouveau dossieriture
    
    Exemple :
    >>>est_valide(piste_liste,(4,1))
    False
    """
    i, j = position
    if 0 <= i < len(piste) and 0 <= j < len(piste[0]):
        return piste[i][j] != '#'
    return False
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
    
    if len(trajectoire) < 2:
        return (0, 0)
    else:
        derniere_pos = trajectoire[-1]
        avant_derniere_pos = trajectoire[-2]
        return (derniere_pos[0] - avant_derniere_pos[0], derniere_pos[1] - avant_derniere_pos[1])


def verif_collision(piste,debut, fin):
    """
    Vérifie si il n'y a pas de collision en faisant appel à la fonction "est_valide".
    
    Paramètres :
    - piste : liste de listes représentant le plateau
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
        pos_depart = []
        for i in range(len(piste)):
            for j in range(len(piste[0])):
                        if piste[i][j] == '>':
                           pos_depart.append((i, j))
        return pos_depart
    
    v = vitesse(trajectoire)
    point_principal = (trajectoire[-1][0] + v[0], trajectoire[-1][1] + v[1])
    
    pos_autorisees = []
    
    for i in range(-1, 2):
        for j in range(-1, 2):
            nouvelle_pos = (point_principal[0] + i, point_principal[1] + j)
            if est_valide(piste, nouvelle_pos):
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


###### NIVEAU 2 ###########
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
            
            if couleur_pixel == (0, 128, 128,255):  # Vert 
                ligne_piste.append('>')
            elif couleur_pixel == (128, 128, 128,255):  # Gris 
                ligne_piste.append('*')
            elif couleur_pixel == (255, 255, 255,255):  # Blanc 
                ligne_piste.append('.')
            else:
                ligne_piste.append('#')  # Autre couleur (obstacle)
        
        piste.append(ligne_piste)
    
    return piste





 

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




piste_image = charger_piste_image("maps-image\\map.png")
piste_chargee = charger("maps-texte\\map2.txt")
trajectoire = [position_depart(piste_image)]
while True:
    options_possibles = options(trajectoire, piste_image)
    afficher_piste(piste_image, trajectoire, options_possibles)
    print("Trajectoire actuelle:", trajectoire)
    print("Options possibles:", options_possibles)
    print("Vitesse actuelle:", vitesse(trajectoire))
    x = int(input("Entrez la coordonnée x de la prochaine position: "))
    y = int(input("Entrez la coordonnée y de la prochaine position: "))
    nouvelle_position = (x, y)
    
    deplacement_reussi = verif_collision(piste_image,trajectoire[-1], nouvelle_position)
    
    if not deplacement_reussi:
        print("Déplacement invalide! Veuillez choisir une autre position.")
        continue
    
    trajectoire.append(nouvelle_position)
    
    if piste_image[nouvelle_position[0]][nouvelle_position[1]] == '*':
        print("Félicitations! Vous avez atteint la zone d'arrivée.")
        break






