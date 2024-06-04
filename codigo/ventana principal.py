import pygame
from pygame import mixer
from pygame.locals import *
import random
from entidades import jugador,enemigo1,enemigo2,enemigo3,enemigo4 #similar a importar una clase de C++

anchoVentana = 600
altoVentana = 700

#------------------------------------------
# Inicializar Pygame
pygame.init()
pygame.mixer.init()
ventana = pygame.display.set_mode((anchoVentana, altoVentana))
pygame.display.set_caption("Space Invaders en POO 😎")

# Fondo
fondo = pygame.image.load("./texturas/cielo.png").convert()
x = 0

#similar a la funcion main() de C++
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        jugador.disparar()


    ventana.fill((0, 0, 0))

    # Dibujar el fondo
    ventana.blit(fondo, (0, x))

    jugador.mover()

    # Mover y dibujar los proyectiles
    for proyectil in jugador.proyectiles:
        proyectil.mover()
        ventana.blit(proyectil.imagen, (proyectil.x, proyectil.y))
        if proyectil.y < 0:  # Si el proyectil sale de la pantalla
            jugador.proyectiles.remove(proyectil)
            jugador.puedeDisparar = True


    # Dibujar el jugador en la ventana
    ventana.blit(jugador.imagen, (jugador.x, jugador.y))
    ventana.blit(enemigo1.imagen, (enemigo1.x, enemigo1.y))
    ventana.blit(enemigo2.imagen, (enemigo2.x, enemigo2.y))
    ventana.blit(enemigo3.imagen, (enemigo3.x, enemigo3.y))
    ventana.blit(enemigo4.imagen, (enemigo4.x, enemigo4.y))
    pygame.display.update()

pygame.quit()