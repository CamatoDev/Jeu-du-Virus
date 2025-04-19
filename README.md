# 🦠 Jeu du Virus – Contrôle de territoire avec IA MinMax

## 🎯 Objectif

Développer un jeu stratégique en 2D où deux adversaires (le joueur et l'IA) s’affrontent pour le **contrôle du territoire** sur une grille, en contaminant les pions adverses. L'IA repose sur l’algorithme **MinMax**.

## ⚙️ Technologies

| Outil        | Utilisation |
|--------------|-------------|
| Python       | Langage principal |
| Pygame       | Interface graphique et logique de jeu |
| MinMax       | Intelligence artificielle pour stratégie de jeu |

## 🕹️ Principe du jeu

- **Grille** : Jeu sur une grille carrée de taille variable
- **Pions** : Deux joueurs avec des pions de couleurs différentes
- **Contamination** : Lorsqu’un pion est placé à côté d’un ou plusieurs pions adverses, ces derniers sont convertis
- **Placement** : Possible uniquement à proximité d’un pion de la même couleur

## 🧠 Intelligence Artificielle

L’adversaire est contrôlé par une IA basée sur l’algorithme **MinMax**, qui évalue les coups possibles à chaque tour pour maximiser ses chances de victoire.

## 📌 Statut

✅ **Prototype terminé**  
🕹️ IA fonctionnelle avec logique de contamination  
⏸️ Développement suspendu (optimisation et refonte UI à envisager plus tard)

## 🗂️ Structure du projet

- `virus_GAme.py` : Lancement du jeu
- `intégrale.py` : Gestion de la grille et des règles
