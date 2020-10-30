import pygame
from pygame.locals import *
from math import *

def afficheScore(s1, s2):
    """ Affiche les scores du joueur 1 et 2"""
    fenetre.blit(haut, (0,0))
    font=pygame.font.Font(pygame.font.match_font('arcade'), 140, bold=True)
    text = font.render(str(s1),True,(79, 129, 183))
    l,h = font.size(str(s1))
    fenetre.blit(text, (250-l//2,80-h//2))
    text = font.render(str(s2),True,(202, 72, 66))
    l,h = font.size(str(s2))
    fenetre.blit(text, (750-l//40,80-h//2))
    font = pygame.font.Font(pygame.font.match_font('videogames'), 100)
    text = font.render("z", True, (202, 72, 66))
    fenetre.blit(text, (0, 0 ))


def enfoncee(key):
    """
    Fonction qui est déclenchée lorsque on appuie sur
    une touche. On met à  jour la liste Touches
    """
    if not key in Touches:
        Touches.append(key)

def relachee(key):
    """
    Fonction qui est déclenchée lorsque on relâche une
    touche. On met à  jour la liste Touches
    """
    if key in Touches:
        Touches.remove(key)

def place(D):
    """
    Cette fonction place le 'sprite' du dictionnaire D
    aux coordonnées (X,Y)
    :param D: Un dictionnaire J1,J2 ou balle
    :return: rien
    """
    fenetre.blit(D['sprite'],(D['X']-D['L']//2,D['Y']-D['H']//2))

def raquetteUP(J):
    if  (not J['Y'] - J['H']//2 < 130) :
        J['Y'] -= 3

def raquetteDOWN(J):
    if (not J['Y'] + J['H'] // 2 > 570):
        J['Y'] += 3

def rebond(x, y, e):
    l = sqrt(x**2 + y**2)
    alpha = degrees( asin(y/l) )
    beta = alpha + e
    beta = min(max(-60, beta), 60) #bornage pour éviter les angles trop grands

    return -copysign(1.1,x)*l*cos(radians(beta)), l*sin(radians(beta))

def arrivee(b, coup):
    x, y, vx, vy = b['X'], b['Y'], b['VX'], b['VY']
    c = 0
    while x < 900 - 34 and c < coup:
        x, y = x + vx, y + vy
        c += 1
        if y < 130 + 16 or y > 570 - 16 :
            vy = -vy
    return int(y)


pygame.init()
fenetre = pygame.display.set_mode((1000,600))

# Déclaration des variables globales
continuer = True
coup = 0
Touches = []

# Chargement des images
haut = pygame.image.load("haut.png").convert()
fenetre.blit(haut, (0,0))
gauche = pygame.image.load("bordjeux.png").convert()
fenetre.blit(gauche, (0,100))
terrain = pygame.image.load("centre.png").convert()
fenetre.blit(terrain, (100,100))
droite = pygame.image.load("bordjeux.png").convert()
fenetre.blit(droite, (900,100))

balle = {'X':300, 'Y':300, 'VX':3, 'VY':3, 'L':32, 'H':32}
balle['sprite'] = pygame.image.load("balle.png").convert_alpha()
J1 = {'X': 110, 'Y':350, 'L':16, 'H':100, 'score':0}
J1['sprite'] = pygame.image.load("R1.png").convert_alpha()
J2 = {'X': 890, 'Y':350, 'L':16, 'H':100, 'score':0}
J2['sprite'] = pygame.image.load("R2.png").convert_alpha()
clock = pygame.time.Clock()

while continuer:
    clock.tick(100)
    # fenetre.blit(terrain, (100, 100))

    for event in pygame.event.get():
        if event.type == QUIT :
            continuer = False
        elif event.type == KEYDOWN :
            enfoncee(event.key)
        elif event.type == KEYUP :
            relachee(event.key)

    if K_s in Touches : raquetteUP(J1)
    if K_x in Touches : raquetteDOWN(J1)

    #if K_UP in Touches: raquetteUP(J2)
    #if K_DOWN in Touches: raquetteDOWN(J2)

    # Deplacement Joueur 2 IA
    if balle['VX'] > 0 : # La balle vient vers le joueur
        cible =  arrivee(balle, coup)
    else: # la balle va vers l'autre joueur
        cible = 350 # milieu du terrain

    if J2['Y'] < cible :
        raquetteDOWN(J2)
    elif J2['Y'] > cible :
        raquetteUP(J2)

    # ici on réalise l'animation
    fenetre.blit(terrain, (100,100))
    place(balle)
    place(J1)
    place(J2)

    # Mise à jour des coordonnées
    balle['X'] += balle['VX']
    balle['Y'] += balle['VY']

    # Rebonds
    if balle['Y'] <= 130 + balle['L']//2 or balle['Y'] >= 570 - balle['L']//2 :
        balle['VY'] = - balle['VY']

    # Buts et score
    if balle['X'] > 900 - balle['L']//2 or balle['X'] < 100 + balle['L']//2:
        if balle['VX'] > 0:
            J1['score'] += 1
            balle['VX'] = -3
            balle['VY'] = -3
            coup += 2
        else:
            J2['score'] += 1
            balle['VX'] = 3
            balle['VY'] = 3
            if coup > 2 :
                coup -= 2

        balle['X'] = 500
        balle['Y'] = 350

    afficheScore(J1['score'], J2['score'])

    # Rebonds raquettes

    # Raquette1
    if J1['X']+8 <= balle['X'] <= J1['X']+24 and J1['Y']-50 <= balle['Y']<=J1['Y']+50 :
        balle['VX'], balle['VY'] = rebond( balle['VX'], balle['VY'], balle['Y']-J1['Y'] )

    # Raquette2
    if J2['X']-24 <= balle['X'] <= J2['X'] - 8 and J2['Y'] - 50 <= balle['Y'] <= J2['Y'] + 50:
        balle['VX'], balle['VY'] = rebond( balle['VX'], balle['VY'], balle['Y']-J2['Y'] )

    # Mise à jour de l'écran
    pygame.display.flip()

print('Fin')
pygame.quit()