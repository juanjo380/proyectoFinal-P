import pygame
from pygame import mixer
from pygame.locals import *
import random
from entidades import jugador,enemigos

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

    obtenerMouse = pygame.mouse.get_pos
    #menuTexto = g


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

    # Mover enemigos
    for enemigo in enemigos:
        enemigo.mover()

        # Dibujar todo
    ventana.blit(fondo,(0,0))
    ventana.blit(jugador.imagen, (jugador.x, jugador.y))
    for proyectil in jugador.proyectiles:
        ventana.blit(proyectil.imagen, (proyectil.x, proyectil.y))
    for enemigo in enemigos:
        ventana.blit(enemigo.imagen, (enemigo.x, enemigo.y))
    # Variables para la posición inicial de los enemigos y el espacio entre ellos

    pygame.display.update()

pygame.quit()