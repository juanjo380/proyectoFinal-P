import pygame
from pygame import mixer
from pygame.locals import *
import random
from entidades import jugador, enemigos
from menu import Menu

anchoVentana = 800
altoVentana = 800

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
en_como_jugar = False
correr = True

# Función para mostrar la pantalla de "Cómo Jugar"
def mostrarComoJugar(ventana):
    ventana.fill((0, 0, 0))
    fuente = pygame.font.Font(None, 40)
    instrucciones = [
        "Como Jugar Space Invaders:",
        "1. Usa las flechas izquierda y derecha para mover tu nave.",
        "2. Presiona la barra espaciadora para disparar.",
        "3. Destruye a los enemigos antes de que lleguen a la parte inferior.",
        "4. Evita los proyectiles enemigos.",
        "",
        "Presiona Enter para volver al menú principal."
    ]
    for i, linea in enumerate(instrucciones):
        texto = fuente.render(linea, True, (255, 255, 255))
        rect = texto.get_rect(center=(anchoVentana / 2, 100 + i * 40))
        ventana.blit(texto, rect)
    pygame.display.update()

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
                    menu.moverSeleccion(-1)
                elif event.key == K_DOWN:
                    menu.moverSeleccion(1)
                elif event.key == K_RETURN:
                    opcion = menu.obtenerOpcion()
                    if opcion == "Iniciar Juego":
                        enMenu = False
                    elif opcion == "Cómo Jugar":
                        enMenu = False
                        en_como_jugar = True  # Cambia al estado de "Cómo Jugar"
                    elif opcion == "Salir":
                        run = False
                        correrCodigo = False  # Asegúrate de salir del bucle principal
            elif en_como_jugar:
                if event.key == K_RETURN:
                    en_como_jugar = False
                    enMenu = True  # Vuelve al menú principal
            else:
                if event.key == K_SPACE:
                    jugador.disparar()

    ventana.fill((0, 0, 0))  # Limpiar la ventana
    if enMenu:
        menu.dibujar(ventana)
    elif en_como_jugar:
        mostrarComoJugar(ventana)
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
                    if enemigo.recibirDano(50):
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
