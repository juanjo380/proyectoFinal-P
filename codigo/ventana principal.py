import pygame
from pygame import mixer
from pygame.locals import *
import random
from entidades import jugador, enemigos
from menu import Menu  # Asegúrate de importar la clase Menu

anchoVentana = 600
altoVentana = 700

# Inicializar Pygame
pygame.init()
pygame.mixer.init()
ventana = pygame.display.set_mode((anchoVentana, altoVentana))
pygame.display.set_caption("Space Invaders en POO 😎")

# Fondo
fondo = pygame.image.load("./texturas/cielo.png").convert()
x = 0

# Instancia del menú
menu = Menu(anchoVentana, altoVentana)

# Variables de estado
enMenu = True
correr = True

# similar a la funcion main() de C++
correrCodigo = True
while correrCodigo:
    obtenerMouse = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            correr = False
            correrCodigo = False  # Asegúrate de salir del bucle principal
        elif event.type == KEYDOWN:
            if enMenu:
                if event.key == K_UP:
                    menu.mover_seleccion(-1)
                elif event.key == K_DOWN:
                    menu.mover_seleccion(1)
                elif event.key == K_RETURN:
                    opcion = menu.obtener_opcion()
                    if opcion == "Iniciar Juego":
                        enMenu = False
                    elif opcion == "Cómo Jugar":
                        print("Mostrar pantalla de cómo jugar")  # Implementar según se desee
                    elif opcion == "Salir":
                        run = False
                        correrCodigo = False  # Asegúrate de salir del bucle principal
            else:
                if event.key == K_SPACE:
                    jugador.disparar()

    if enMenu:
        menu.dibujar(ventana)
    else:
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
            for enemigo in enemigos:
                if proyectil.colisiona(enemigo):
                    if enemigo.recibirDano(10):
                        enemigos.remove(enemigo)
                    jugador.proyectiles.remove(proyectil)
                    break

        # Mover enemigos
        for enemigo in enemigos:
            enemigo.mover()

        # Dibujar todo
        ventana.blit(fondo, (0, 0))
        jugador.y = altoVentana - jugador.imagen.get_height() - 20
        ventana.blit(jugador.imagen, (jugador.x, jugador.y))
        for proyectil in jugador.proyectiles:
            ventana.blit(proyectil.imagen, (proyectil.x, proyectil.y))
        for enemigo in enemigos:
            ventana.blit(enemigo.imagen, (enemigo.x, enemigo.y))

    pygame.display.update()

pygame.quit()
