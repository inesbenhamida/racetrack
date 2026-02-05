# 🏎️ Race Track - Projet de Licence 1 (L1)

**Race Track** (ou Vector Race) est un projet de simulation de course automobile réalisé en **mai 2024** dans le cadre de ma première année de Licence informatique. Ce jeu, inspiré des classiques sur papier quadrillé, repose sur des concepts physiques d'inertie et de vecteurs.

##  Auteure
* **Inès Benhamida**

## 🎮 Concept du Jeu
Le but est de franchir la ligne d'arrivée le plus vite possible sans sortir de la piste. La particularité du gameplay est que le mouvement de la voiture est régi par son vecteur vitesse précédent. 

Chaque tour, le joueur choisit une accélération parmi les cases adjacentes, ce qui modifie son vecteur de déplacement actuel.

## 🛠️ Aspects Techniques de L1
Ce projet de début de cursus m'a permis de mettre en pratique les fondamentaux de la programmation :
* **Logique de Jeu** : Gestion des collisions avec les bords de la piste et détection du franchissement de la ligne d'arrivée.
* **Algorithmique** : Implémentation d'un "solveur" capable de calculer automatiquement une trajectoire pour terminer la course.
* **Interface Graphique** : Utilisation du module `fltk.py` pour l'affichage dynamique et la gestion des événements souris/clavier.
* **Modularité** : Organisation du code en plusieurs fichiers pour séparer la logique (`fonctions.py`), l'affichage et l'exécution (`main.py`).

## 📂 Contenu du dépôt
* `main.py` : Le point d'entrée du programme.
* `fonctions.py` : Contient toute la logique des déplacements et du solveur.
* `fltk.py` : La bibliothèque graphique nécessaire au fonctionnement du jeu.
* `RAPPORT_ZIACH_BENHAMIDA.pdf` : Le document expliquant la conception et les choix techniques.

## 💻 Lancement
Assurez-vous d'avoir Python 3 installé sur votre machine. Pour lancer le jeu, exécutez la commande suivante dans le dossier du projet :
```bash
python3 main.py
