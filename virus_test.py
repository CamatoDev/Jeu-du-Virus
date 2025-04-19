# -*- coding: utf-8 -*-
"""
Created on Sun Oct 16 05:52:21 2022

@author: pc
"""

import pygame, copy, time, random, sys
from pygame.locals import*
from math import ceil

HAUTEUR_FENETRE = 550
LARGEUR_FENETRE = 550
TAILLE_GRILLE = 7
DECALAGE_X = 100
DECALAGE_Y = 100
TAILLE_CASE = 50
RAYON = 20
ANIMATIONSPEED = 25
FPS = 10

#couleur        R    G    B
WHITE      = (255, 0, 0)
BLACK      = (  0,   255,   0)
RBLACK      = (  0,   0,   0)
BLACK1      = (  255,   255,   255)
GREEN      = (  0, 155,   0)
BRIGHTBLUE = ( 128, 128, 128)
BROWN      = (174,  94,   0)
DEFAUT     = (0, 0, 255)

COULEUR_GRILLE = BLACK
COULEUR_NOIR = BLACK
COULEUR_BLANCHE = WHITE
BACKGROUND_COLOR = DEFAUT
TEXTCOLOR1 = WHITE
TEXTCOLOR2 = BLACK
TEXTCOLOR3 = RBLACK
TEXTCOLOR = BLACK1
TEXTBGCOLOR1 = BRIGHTBLUE

RIEN = 0
PION_NOIR = 1
PION_BLANC = 2
PION_AIDE = 3

# Utiliser uniquement dans les fonctions Min et Max




def main():
    global Surface, continuer, fond_plateau, fond_plateau_rect, clock, FONT,BIGFONT
    
    #Initialisation de pygame
    pygame.init()
    FONT = pygame.font.Font('freesansbold.ttf', 50)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 32)
    Surface = pygame.display.set_mode((LARGEUR_FENETRE, HAUTEUR_FENETRE))
    pygame.display.set_caption('Jeu du Virus')
    clock = pygame.time.Clock()

    # On parametre l'image de fond
    fond_plateau = pygame.image.load('flippybackground.png').convert_alpha()
    fond_plateau.set_alpha(255)
    
    # Use smoothscale() to stretch the board image to fit the entire board:
    fond_plateau = pygame.transform.smoothscale(fond_plateau, (TAILLE_CASE * TAILLE_GRILLE, TAILLE_CASE * TAILLE_GRILLE))
    fond_plateau_rect = fond_plateau.get_rect()
    fond_plateau_rect.topleft = (DECALAGE_X, DECALAGE_Y)

    Surface.fill(BACKGROUND_COLOR)
    # pygame.display.update()
    Surface.blit(fond_plateau, fond_plateau_rect)
    pygame.display.update(fond_plateau_rect)
    # Run the main game.
   
    while True:
        if runGame() == False: 
            break
    
########################## Initialisation général du jeu 
def nouvelleGrille():

    #Initialisation de la grille 
    grille = [[RIEN]*TAILLE_GRILLE for _ in range(TAILLE_GRILLE)]
       
    # Quelle valeurs par defaut
    grille[0][0] = PION_NOIR
    grille[0][6] = PION_BLANC
    grille[6][6] = PION_NOIR
    grille[6][0] = PION_BLANC

    #grille[2][4] = PION_NOIR
    #grille[2][5] = PION_NOIR
    #grille[3][5] = PION_NOIR
    #grille[2][2] = PION_NOIR
    #grille[2][1] = PION_NOIR
    #grille[3][1] = PION_NOIR
    #grille[4][1] = PION_AIDE
    
    
    return grille


def afficheGrille(grille):
    #Affichage de la grille avec les taches
    
    #Affichage de trait en largeur
    x, y = DECALAGE_X, DECALAGE_Y
    for i in range(0,TAILLE_GRILLE+1):
        pygame.draw.rect(Surface, COULEUR_GRILLE, (x, y, 2, HAUTEUR_FENETRE-DECALAGE_X*2))
        x += TAILLE_CASE   
    #Affichage de traits en longueur
    x, y =DECALAGE_X, DECALAGE_Y
    for i in range(0,TAILLE_GRILLE+1):
        pygame.draw.rect(Surface, COULEUR_GRILLE, (x, y, LARGEUR_FENETRE-DECALAGE_Y*2, 2))
        y += TAILLE_CASE
     #Affichage des pions
    x, y = DECALAGE_X, DECALAGE_Y
    for i in range(TAILLE_GRILLE):
        for j in range(TAILLE_GRILLE):
            if grille[i][j] == PION_NOIR:
                pygame.draw.circle(Surface, COULEUR_NOIR, (x+TAILLE_CASE/2, y+TAILLE_CASE/2), RAYON)
            if grille[i][j] == PION_BLANC:
                pygame.draw.circle(Surface, COULEUR_BLANCHE, (x+TAILLE_CASE/2, y+TAILLE_CASE/2), RAYON)
            if grille[i][j] == PION_AIDE:
                pygame.draw.circle(Surface, COULEUR_NOIR, (x+TAILLE_CASE/2, y+TAILLE_CASE/2),RAYON,2) 
            x += TAILLE_CASE
        y += TAILLE_CASE
        x = DECALAGE_X 
  ######################################### 

def affichePion(pos, typePion):
    x, y = transformToCoordonnee(pos[0], pos[1])
    if typePion == PION_NOIR:
        pygame.draw.circle(Surface, COULEUR_NOIR, (x+TAILLE_CASE/2, y+TAILLE_CASE/2), RAYON)
    elif typePion == PION_BLANC:
        pygame.draw.circle(Surface, COULEUR_BLANCHE, (x+TAILLE_CASE/2, y+TAILLE_CASE/2), RAYON)
    else:
        pygame.draw.circle(Surface, COULEUR_NOIR, (x+TAILLE_CASE/2, y+TAILLE_CASE/2),RAYON,2)
    
######################################## Gestion des pions 
def determine_case(position):
    # Prend en entrée une position(de la souris ) et retourne la case sur laquelle elle est
    l, c = 0, 0
    
    # gestion de la ligne
    if position[0]%TAILLE_CASE == 0:
        c = position[0]//TAILLE_CASE - 2*int(TAILLE_CASE/TAILLE_CASE) 
       
        #(Le '-' deux fois car il y'a un décalage de TAILLE_CASE en hauteur et en largeur et les   
        #indices de la liste commence à partir de 0)
    else:
        c = ceil(position[0]/TAILLE_CASE) - 2*int(TAILLE_CASE/TAILLE_CASE) -1 
    # gestion de la colone
    if position[1]%TAILLE_CASE == 0:
        l = position[1]//TAILLE_CASE - 2*int(TAILLE_CASE/TAILLE_CASE) -1 
    else:
        l = ceil(position[1]/TAILLE_CASE) - 2*int(TAILLE_CASE/TAILLE_CASE) -1     
           
    return [l, c]    

def transformToCoordonnee(l, c): 
    return (c*TAILLE_CASE + DECALAGE_X, l*TAILLE_CASE + DECALAGE_X )
    
    
    
def recherche_position_pions(plateau, type_pion):
    # Retourne toutes les positions possibles des pions d'une couleur donné
    positions_poins = [] 
    for x in range(TAILLE_GRILLE):
        for y in range(TAILLE_GRILLE):
            if plateau[x][y] == type_pion:
                positions_poins.append([x,y])
    return positions_poins

def is_possible_to_push(grille,position, couleur_pion):
    # Elle regarde si avant de poser un pion d'un couleur donnée il y'a une couleur de ce type
    #dans les environs
    #on determine la position sur la grille du pion
    l, c  = position
    
    #gestion suivant l'ordonné
    if l+1 <= TAILLE_GRILLE-1 and grille[l+1][c] == couleur_pion:
         return True    
    if l-1 >= 0  and grille[l-1][c] == couleur_pion:
         return True            
    #Gestion suivant l'abscisse
    if c+1 <= TAILLE_GRILLE-1 and grille[l][c+1] == couleur_pion:
        return True 
    if c-1 >= 0  and grille[l][c-1] == couleur_pion:
        return True         
    #Gestion suivant la diagonale
    if c+1 <= TAILLE_GRILLE-1 and l+1 <= TAILLE_GRILLE-1 and grille[l+1][c+1] == couleur_pion:
        return True
        
    if c+1 <= TAILLE_GRILLE-1 and l-1 >= 0 and grille[l-1][c+1] == couleur_pion:
        return True
        
    if c-1 >= 0 and l+1 <= TAILLE_GRILLE-1 and grille[l+1][c-1] == couleur_pion:
        return True
        
    if c-1 >= 0 and l-1 >= 0 and grille[l-1][c-1] == couleur_pion:
        return True
       
    return False

def recherche_des_coups_possibles(plateau, position):
    #Renvoile la liste de coups possibles pour une position donnée
    l, c  = position
    coups_possibles = []
    
    #gestion suivant l'ordonné
    if l+1 <= TAILLE_GRILLE-1 and (plateau[l+1][c] == RIEN or plateau[l+1][c] == PION_AIDE):
         coups_possibles.append([l+1,c])       
    if l-1 >= 0  and plateau[l-1][c] == RIEN:
         coups_possibles.append([l-1, c])
              
    #Gestion suivant l'abscisse
    if c+1 <= TAILLE_GRILLE-1 and (plateau[l][c+1] == RIEN or plateau[l][c+1] == PION_AIDE):
        coups_possibles.append([l,c+1])
    if c-1 >= 0  and plateau[l][c-1] == RIEN:
        coups_possibles.append([l,c-1])
               
    #Gestion suivant la diagonale
    if c+1 <= TAILLE_GRILLE-1 and l+1 <= TAILLE_GRILLE-1 and (plateau[l+1][c+1] == RIEN or plateau[l+1][c+1] == PION_AIDE):
        coups_possibles.append([l+1,c+1])       
    if c+1 <= TAILLE_GRILLE-1 and l-1 >= 0 and (plateau[l-1][c+1] == RIEN or plateau[l-1][c+1] == PION_AIDE):
        coups_possibles.append([l-1,c+1])    
    if c-1 >= 0 and l+1 <= TAILLE_GRILLE-1 and (plateau[l+1][c-1] == RIEN or plateau[l+1][c-1] == PION_AIDE):
        coups_possibles.append([l+1,c-1])  
    if c-1 >= 0 and l-1 >= 0 and (plateau[l-1][c-1] == RIEN or plateau[l-1][c-1] == PION_AIDE):
        coups_possibles.append([l-1,c-1])
       
    #print(f"\nles coups possible a la position {position} sont: {coups_possibles} \n")
    return coups_possibles

def determine_nombre_de_coup(plateau, type_pion):
    # Retourne le nombre total de coup pour un type de joueur
    resultat = 0

    # Tous les pions du joueur appelant
    positions_poins = [] 
    for x in range(len(plateau)):
        for y in range(len(plateau)):
            if plateau[x][y] == type_pion:
                positions_poins.append([x,y])
                
    for i in range(0, len(positions_poins)):
        resultat += len(recherche_des_coups_possibles(plateau, positions_poins[i]))
        
    return resultat   

def contamination(plateau, position, type_pion, allow = True):
    # Contamine si possible les pions voisins
    
    #on determine la position sur la grille du pion
    l, c  = position

    contamines = {}

    #gestion suivant l'ordonné
    if l+1 <= TAILLE_GRILLE-1 and plateau[l+1][c] != RIEN and  plateau[l+1][c] != type_pion and plateau[l+1][c] != PION_AIDE:
        if type_pion == PION_BLANC:
             plateau[l+1][c] = PION_BLANC 
        elif type_pion == PION_NOIR:
            plateau[l+1][c] = PION_NOIR
        contamines[l+1,c] = type_pion      
    if l-1 >= 0  and plateau[l-1][c] != RIEN and  plateau[l-1][c] != type_pion and  plateau[l-1][c] != PION_AIDE:
        if type_pion == PION_BLANC:
            plateau[l-1][c] = PION_BLANC 
        elif type_pion == PION_NOIR:
            plateau[l-1][c] = PION_NOIR
        contamines[l-1,c] = type_pion
                 
    #Gestion suivant l'abscisse
    if c+1 <= TAILLE_GRILLE-1 and plateau[l][c+1] != RIEN and  plateau[l][c+1] != type_pion and plateau[l][c+1] != PION_AIDE:
        if type_pion == PION_BLANC:
            plateau[l][c+1] = PION_BLANC 
        elif type_pion == PION_NOIR:
            plateau[l][c+1] = PION_NOIR
        contamines[l,c+1] = type_pion 
    if c-1 >= 0  and plateau[l][c-1] != RIEN and  plateau[l][c-1]!= type_pion and  plateau[l][c-1]!= PION_AIDE:
        if type_pion == PION_BLANC:
            plateau[l][c-1] = PION_BLANC 
        elif type_pion == PION_NOIR:
            plateau[l][c-1] = PION_NOIR
        contamines[l,c-1] = type_pion
            
    #Gestion suivant la diagonale
    if c+1 <= TAILLE_GRILLE-1 and l+1 <= TAILLE_GRILLE-1 and plateau[l+1][c+1] != RIEN and plateau[l+1][c+1] != type_pion and plateau[l+1][c+1] != PION_AIDE:
        if type_pion == PION_BLANC:
            plateau[l+1][c+1] = PION_BLANC 
        elif type_pion == PION_NOIR:
            plateau[l+1][c+1] = PION_NOIR
        contamines[l+1,c+1] = type_pion
    if c+1 <= TAILLE_GRILLE-1 and l-1 >= 0 and plateau[l-1][c+1] != RIEN and plateau[l-1][c+1] != type_pion and plateau[l-1][c+1] != PION_AIDE:
        if type_pion == PION_BLANC:
            plateau[l-1][c+1] = PION_BLANC 
        elif type_pion == PION_NOIR:
            plateau[l-1][c+1] = PION_NOIR
        contamines[l-1,c+1] = type_pion
    if c-1 >= 0 and l+1 <= TAILLE_GRILLE-1 and plateau[l+1][c-1] != RIEN and plateau[l+1][c-1] != type_pion and plateau[l+1][c-1] != PION_AIDE:
        if type_pion == PION_BLANC:
            plateau[l+1][c-1]= PION_BLANC 
        elif type_pion == PION_NOIR:
            plateau[l+1][c-1] = PION_NOIR
        contamines[l+1,c-1] = type_pion
    if c-1 >= 0 and l-1 >= 0 and plateau[l-1][c-1] != RIEN and  plateau[l-1][c-1] != type_pion and  plateau[l-1][c-1] != PION_AIDE:
        if type_pion == PION_BLANC:
            plateau[l-1][c-1] = PION_BLANC 
        elif type_pion == PION_NOIR:
            plateau[l-1][c-1] = PION_NOIR
        contamines[l-1,c-1] = type_pion
        
    #print(f"{compteur} cases contaminés\n"
    if allow == True:
        affichePion(position, type_pion)
        for key, value in contamines.items():
            animationContamination(key, value)
            
    return contamines
     
def animationContamination(posPionAContamine, typePionVirus):
   # animation du joueur adverse
    for rgbValues in range(0, 255, int(ANIMATIONSPEED * 2.55)):
        if rgbValues > 255:
            rgbValues = 255
        elif rgbValues < 0:
            rgbValues = 0

        if typePionVirus == PION_BLANC:
            color = tuple([rgbValues] * 3) # rgbValues goes from 0 to 255
        elif typePionVirus == PION_NOIR:
            color = tuple([255 - rgbValues] * 3) # rgbValues goes from 255 to 0

        l, c = posPionAContamine
        x, y = transformToCoordonnee(l, c)
        pygame.draw.circle(Surface, color, (x+TAILLE_CASE/2, y+TAILLE_CASE/2), RAYON)
        pygame.display.update()
        clock.tick(FPS)


def pushPion(plateau, position, couleur_pion, allow = True):
    # Fonction qui permet d'ajouter un pion a la grille
    
    l, c = position
            
    if (l >= 0 and l < TAILLE_GRILLE) and (c >= 0 and c < TAILLE_GRILLE):
        if plateau[l][c] != RIEN and plateau[l][c] != PION_AIDE:
            return False
        else:
            # On verifie que l'on ne met le pion que dans les cases voisines 
            if is_possible_to_push(plateau, position, couleur_pion):
                if plateau[l][c] == RIEN or plateau[l][c] == PION_AIDE:
                    if couleur_pion == PION_BLANC:
                        plateau[l][c] = PION_BLANC 
                    if couleur_pion == PION_NOIR:
                        plateau[l][c] = PION_NOIR
                        # on fait la contamination 
                contamination(plateau, position, couleur_pion, allow)
                return True
            else:
                return False
   
    return False
 ########################################

######################################### Gestion du jeu 

def enterPlayerTile():
    # Affiche le message et les options d'initialisations du jeu
    
    # Creation ds text a afficher the text.
    FONT = pygame.font.Font('freesansbold.ttf', 20)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 32)
    
    textSurf = FONT.render('Tu choisis quel couleur ?', True, TEXTCOLOR, TEXTBGCOLOR1)
    textRect = textSurf.get_rect()
    textRect.center = (int(LARGEUR_FENETRE / 2), int(HAUTEUR_FENETRE / 2))

    bSurf = BIGFONT.render('Blanc', True, TEXTCOLOR, TEXTBGCOLOR1)
    bRect = bSurf.get_rect()
    bRect.center = (int(LARGEUR_FENETRE / 2) - 60, int(HAUTEUR_FENETRE / 2) + 40)

    nSurf = BIGFONT.render('Noir', True, TEXTCOLOR, TEXTBGCOLOR1)
    nRect = nSurf.get_rect()
    nRect.center = (int(LARGEUR_FENETRE / 2) + 60, int(HAUTEUR_FENETRE / 2) + 40)
    
    global continuer
    while True:
        # Keep looping until the player has clicked on a color.
        for event in pygame.event.get(): # event handling loop
            if event.type == pygame.MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if bRect.collidepoint( (mousex, mousey) ):
                    return [PION_BLANC, PION_NOIR]
                elif nRect.collidepoint( (mousex, mousey) ):
                    return [PION_NOIR, PION_BLANC]   
    
        # Draw the screen.
    Surface.blit(textSurf, textRect)
    Surface.blit(bSurf, bRect)
    Surface.blit(nSurf, nRect)
    clock.tick(FPS)
       # MAINCLOCK.tick(FPS)


# Fonction qui gère le jeu du joueur 
def playerGame(plateau, position):
    l, c = determine_case(position)
    return pushPion(plateau, [l,c], PION_NOIR)
    
# Fonction qui gère le jeu de l'IA                                   
def iaGame(plateau):
    position = choix_miniMax(plateau, 2)
    return pushPion(plateau, position, PION_BLANC)
    
def getScores(plateau):
    bScore = 0
    nScore = 0
    for x in range(TAILLE_GRILLE):
        for y in range(TAILLE_GRILLE):
            if plateau[x][y] == PION_BLANC:
                bScore += 1
            if plateau[x][y] == PION_NOIR:
                nScore += 1
                
    return [bScore, nScore]
   
def afficheInfoJeu(plateau):
    # les scores
    FONT = pygame.font.Font('freesansbold.ttf', 20)
    scores = getScores(plateau)
    scoreSurf_j = FONT.render("Joueur Score: %s " % (str(scores[1])), True, COULEUR_NOIR)
    scoreRect_j = scoreSurf_j.get_rect()
    scoreRect_j.topleft = (10,  5)
    Surface.blit(scoreSurf_j, scoreRect_j)

    
    scoreSurf_m = FONT.render("Machine Score: %s " % (str(scores[0])), True, TEXTCOLOR1)
    scoreRect_m = scoreSurf_m.get_rect()
    scoreRect_m.topright = (LARGEUR_FENETRE-10,  5)
    Surface.blit(scoreSurf_m, scoreRect_m)

    
def jeuEnCour(plateau):
    #Verifie le jeu doit continuer ou pas 
    
    # Possibilité 1: le nombre de coup d'un joueur est null
    if determine_nombre_de_coup(plateau, PION_BLANC) == 0:
        return False
    if determine_nombre_de_coup(plateau, PION_NOIR) == 0:
        return False
    
    #Possibilité 2: 

    return True

def aide(plateau):
    # Fonction qui affiche de l'aide à la demande du joueur
    pos_pions = recherche_position_pions(plateau, PION_NOIR)
    for i in range(0, len(pos_pions)):
        coup_possibe = recherche_des_coups_possibles(plateau, pos_pions[i])
        t = len(coup_possibe)
        if t != 0:
            for j in range(0, t):
                l,c = coup_possibe[j]
                plateau[l][c] = PION_AIDE
 
def cleanHint(plateau):
    print("clean hint")
    for x in range(TAILLE_GRILLE):
        for y in range(TAILLE_GRILLE):
            if plateau[x][y] == PION_AIDE:
                plateau[x][y] = RIEN    
                
def sauvegarderPlateau(plateau):
    # Elle duplique le plateau et renvoi le tableau dupliqué
    copie_plateau = copy.deepcopy(plateau)
    return copie_plateau


#####################################    

#####################################  Gestion de l'IA

# Algorithme minimax 
          
def evaluation(plateau):
    # Fonction d'évaluation: C'est la différence entre le nombre de pions que j'ai mangé et 
    # celui de l'adversaire
    ia_pions_contamines = 0
    adversaire_pions_contamines = 0
    for x in range(TAILLE_GRILLE):
        for y in range(TAILLE_GRILLE):
            if plateau[x][y] == PION_BLANC:
                ia_pions_contamines += 1
            elif plateau[x][y] == PION_NOIR:
                adversaire_pions_contamines += 1
   
    #print("evaluation", ia_pions_contamines -  adversaire_pions_contamines)
    return ia_pions_contamines -  adversaire_pions_contamines
     
# Algorithme pour le max   
def Max(plateau, coup_a_jouer, profondeur):
    #C'est une fonction récursive en fait il y'aura une recursibité mutuelle 
    # entre elle et la fonction Min
    # NB: le coup à jour est la position de la case ou on souhairte placer le pion
    #print(f"**** Max à la profondeur {profondeur}")
    #Condition d'arret 
    
    debut = time.time()
    if profondeur == 0:
        return evaluation(plateau)
    
    #Valeur temporaire du max
    m_max = float('-inf')

    
    # On sauvegarde le plateau
    copie_plateau = sauvegarderPlateau(plateau)
    
    # Simulation du jeu coté adversaire
    pushPion(copie_plateau, coup_a_jouer, PION_NOIR, False)

    # Etape 1: On repère tous les pions de l'IA sur le plateau
    pos_ia = recherche_position_pions(copie_plateau, PION_BLANC)
    random.shuffle(pos_ia)
    # Etape 2
    # Etape 2-1: Pour chaque pion, on determine les coups possibles à joueur
    for j in range(len(pos_ia)) : 
        fils = recherche_des_coups_possibles(copie_plateau, pos_ia[j])
        t = len(fils)
        if t != 0:
            # Etape 2-2: Pour chaque coup, on fait jouer l'adversaire et on évalue la position
            # puis on s'arrage a prendre le max de ces évaluations et le coup qui le donne 
            for i in range(0,t):
                m_value = Min(copie_plateau, fils[i], profondeur)
                if  m_value >= m_max:
                    m_max = m_value    

    #print("max:",m_max)
    fin = time.time()
    print(f"Fonction max. Le temps mis {fin - debut}")
    return m_max
    
# Algorithme pour le min    
def Min(plateau, coup_a_jouer, profondeur):
    #C'est une fonction récursive en fait il y'aura une recursibité mutuelle 
    # entre elle et la fonction Min
    # NB: le coup à jour est la position de la case ou l'ia place son pion;
    #     En min c'est a l'adversaire de jouer apres le tour de l'IA   
    if profondeur == 0:
        return evaluation(plateau)
    
    #Valeur temporaire du min
    m_min = float('inf')

    # On sauvegarde le plateau
    copie_plateau = sauvegarderPlateau(plateau)
    
    # Simulation du jeu côté IA sur le tableau copié
    pushPion(copie_plateau, coup_a_jouer, PION_BLANC, False)
    
    # Simulation du jeu  côté adversaire sur le tableau copié
    pos_adverse = recherche_position_pions(copie_plateau, PION_NOIR)
    random.shuffle(pos_adverse)
    for i in range(0, len(pos_adverse)):
        fils = recherche_des_coups_possibles(copie_plateau, pos_adverse[i])
        t = len(fils) 
        if t != 0:
            for j in range(0,t):
                tmp_min = Max(copie_plateau, fils[j], profondeur-1)
                if tmp_min <= m_min:
                    m_min = tmp_min
    return m_min

# Recherche  Minimax
def choix_miniMax(plateau, profondeur):
    debut = time.time()
    
    choix_coup = None
    tmp_value = float('-inf')
    
    #  Etape 1: On repère tous les pions de l'IA sur le plateau
    positions_poins = recherche_position_pions(plateau, PION_BLANC)
    
    print("position des pions IA",positions_poins)
    
    # Etape 2
    for i in range(len(positions_poins)):
        # Etape 2-1: Pour chaque pion, on determine les coups possibles à joueur
        fils = recherche_des_coups_possibles(plateau, positions_poins[i])
        t = len(fils)
        if t != 0:
            #print("fils de",positions_poins[i]," ",fils)
            # Etape 2-2: Pour chaque coup, on fait jouer l'adversaire et on évalue la position
            # puis on s'arrage a prendre le max de ces évaluations et le coup qui le donne 
            for j in range(0, t):
                m_value = Min(plateau, fils[j], profondeur)
                if  m_value >= tmp_value:
                    tmp_value = m_value
                    choix_coup = fils[j]
        else:
            print(positions_poins[i],": pas de fils possible")
        #print("############################################################""")

    
    
    
    print(f"Position choisi {choix_coup} et l'évaluation est' : {tmp_value}")
    fin = time.time() 
    print(f"Fonction choix_minimax. Le temps mis {fin - debut}")
    return choix_coup
#####################################
def checkForQuit():
    for event in pygame.event.get((pygame.QUIT, pygame.KEYUP)): # event handling loop
        if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()
def end_of_game (plateau) :
    # Display the final score.
   afficheGrille(plateau)
   scores = getScores(plateau)

   # texte en fin de partie
   if scores[1] > scores[0]:
       text = 'YOU WON:) %s points! Felicitations !' % \
              (scores[1] - scores[0])
   elif scores[1] < scores[0]:
       text = 'YOU LOST :( %s points.' % \
              (scores[0] - scores[1])
   else:
       text = 'GAME OVER!'

   textSurf = FONT.render(text, True, TEXTCOLOR1, TEXTBGCOLOR1)
   textRect = textSurf.get_rect()
   textRect.center = (int(LARGEUR_FENETRE / 2), int(HAUTEUR_FENETRE / 3))
   

   # rejouer?
   text2Surf = BIGFONT.render('Rejouer?', True, TEXTCOLOR3, TEXTBGCOLOR1)
   text2Rect = text2Surf.get_rect()
   text2Rect.center = (int(LARGEUR_FENETRE / 2), int(HAUTEUR_FENETRE / 2+50))
   

   # si oui
   yesSurf = BIGFONT.render('Oui', True, TEXTCOLOR, TEXTBGCOLOR1)
   yesRect = yesSurf.get_rect()
   yesRect.center = (int(LARGEUR_FENETRE / 2) - 60, int(HAUTEUR_FENETRE / 2) + 200)
   

   # sinon
   noSurf = BIGFONT.render('Non', True, TEXTCOLOR, TEXTBGCOLOR1)
   noRect = noSurf.get_rect()
   noRect.center = (int(LARGEUR_FENETRE / 2) + 60, int(HAUTEUR_FENETRE / 2) + 200)
   while True:
        # boucle du jeu
        checkForQuit()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if yesRect.collidepoint( (mousex, mousey) ):
                    runGame()
                elif noRect.collidepoint( (mousex, mousey) ):
                    pygame.quit()
                    sys.exit()
        Surface.blit(textSurf, textRect)
        Surface.blit(text2Surf, text2Rect)
        Surface.blit(yesSurf, yesRect)
        Surface.blit(noSurf, noRect)
        pygame.display.flip()
   
  
def runGame(): # A revoir 
    
    # Initialisation de la grille et du jeu
    grille = nouvelleGrille()
    global sauvegarde_grille
    sauvegarde_grille = grille 
    
    j_trait = 'Humain'
                # , 'Machine'])
    
    
    checkForQuit()
    while jeuEnCour(grille):
        Surface.fill(BACKGROUND_COLOR)
        Surface.blit(fond_plateau, fond_plateau_rect)
        afficheGrille(grille)
        afficheInfoJeu(grille)
        # pion= enterPlayerTile()
        
        if j_trait == 'Humain':
            if determine_nombre_de_coup(grille, PION_NOIR) == 0:
                #le joueur ne peut plus joueur
                end_of_game(grille)
                break;
            afficheGrille(grille)
            afficheInfoJeu(grille)
            
            clock.tick(FPS)
            pygame.display.update()
            
            for event in pygame.event.get():
               if event.type == pygame.MOUSEBUTTONDOWN:
                   sauvegarde_grille = sauvegarderPlateau(grille)
                   if playerGame(grille, event.pos) : 
                       if determine_nombre_de_coup(grille, PION_NOIR) != 0:
                           j_trait = "Machine"
               if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE :
                   aide(grille)    
        else:  
            if determine_nombre_de_coup(grille, PION_NOIR) == 0:
                #la machine ne peut plus poser de pions
                end_of_game(grille)
                break   
            
            afficheGrille(grille)
            afficheInfoJeu(grille)
            
            # On ralenti un peut le temps de jeu de l'IA comme s'il recfléchissait.
            pauseUntil = time.time() + random.randint(5, 15) * 0.1
            while time.time() < pauseUntil:
                pygame.display.update()
                
            iaGame(grille)
            
            if determine_nombre_de_coup(grille, PION_NOIR) != 0:
                j_trait = "Humain"
    end_of_game(grille)                       
    afficheGrille(grille) 
    checkForQuit() 
    
        
    return False



main()
