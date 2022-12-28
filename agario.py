
import pygame as pg
from random import randint
import numpy as np
import os


def main():
    clock = pg.time.Clock()

    # on initialise pygame et on crée une fenêtre de 640x640 pixels
    pg.init()
    screen = pg.display.set_mode((640, 640))

    # On donne un titre à la fenetre
    pg.display.set_caption("agario")

    # La boucle du jeu
    done = False
    centre=pg.math.Vector2(320,320)

    #manger1:
    #fruits=[]
    rayon=20
    fruit=(randint(0,639),randint(0,639))
    random_color = (randint(0, 255), randint(0, 255), randint(0, 255))
    pg.draw.circle(screen,random_color,fruit,10)

    #On choisit la couleur du blop avant de commencer le jeu
    print('Quelle est la couleur du blop souhaitée?')

    couleur = input('Saisir une couleur :')

    print('Quelle est la couleur du fond?')
    couleur_fond = input('Saisir une couleur:')

    print('Quel est le nom de l utilisateur?')

    nom = input('Saisir un nom:')

    #Création du bot ( juste le rayon+couleur):
    print('Quelle est la couleur du bot?')
    couleur_bot = input('Saisir une couleur:')
    rayon_bot = 20
    position_random = pg.math.Vector2(randint(0,639),randint(0,639))





    while not done:
        clock.tick(50)
         
        screen.fill(couleur_fond)
        
        x=np.linspace(0,641,17)
        y=np.linspace(0,641,17)

        for k in x:
            pg.draw.line(screen,'black',(k,y[0]),(k,y[-1]))
        for k in y:
            pg.draw.line(screen,'black',(x[0],k),(x[-1],k))       

        #Creation du bot(Déplacements...):
        pg.draw.circle(screen,couleur_bot,position_random,rayon_bot)
        #centre = centre + 

        pg.draw.circle(screen,couleur,centre,rayon)
    
        
        souris=pg.math.Vector2(pg.mouse.get_pos())
        

        direction = souris - centre
        #direction.normalize()


        # Pour le terme d'inertie , on choisir le fait que si la surface du blop est multipliée par 10 , sa vitesse est divisée par 2
        surface = 3.14*rayon**2
        inertie = 1/2**(np.log10(surface))
        centre = centre + direction*0.1*inertie
        
        #manger:
        if pg.math.Vector2.distance_to(pg.Vector2(fruit),centre)<10+rayon:
           surface+=3.14*100
           rayon = np.sqrt(surface/3.14)
           fruit=(randint(0,639),randint(0,639))
        pg.draw.circle(screen,'red',fruit,10)

        
        # enfin on met à jour la fenêtre avec tous les changements
        pg.display.update()

        # on itère sur tous les évênements qui ont eu lieu depuis le précédent appel
        # ici donc tous les évènements survenus durant la seconde précédente
        for event in pg.event.get():
            # chaque évênement à un type qui décrit la nature de l'évênement
            # un type de pg.QUIT signifie que l'on a cliqué sur la "croix" de la fenêtre
            if event.type == pg.QUIT:
                done = True
            # un type de pg.KEYDOWN signifie que l'on a appuyé une touche du clavier
            elif event.type == pg.KEYDOWN:
                # si la touche est "Q" on veut quitter le programme
                if event.key == pg.K_q:
                    done = True

    pg.quit()


# if python says run, then we should run
if __name__ == "__main__":
    main()

