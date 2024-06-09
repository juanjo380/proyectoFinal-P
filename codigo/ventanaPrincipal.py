import pygame
from pygame.locals import *
import random
from entidades import jugador, enemigos, Jefe, anchoPantalla, nuevoAncho, altoPantalla
from menu import Menu

anchoVentana = 800
altoVentana = 800

# Inicializar Pygame
pygame.init()
pygame.mixer.init()
ventana = pygame.display.set_mode((anchoVentana, altoVentana))
pygame.display.set_caption("Space Invaders en POO 😎")
pygame.mixer.music.load('./texturas/soundTrack.mp3')
pygame.mixer.music.set_volume(0.3) 
pygame.mixer.music.play(-1)  # El argumento -1 hace que la música se repita indefinidamente

# Fondo
fondo = pygame.image.load("./texturas/cielo.png").convert()
x = 0

# Instancia del menú
menu = Menu(anchoVentana, altoVentana)

texturas_enemigos = [
    "./texturas/enemigo1.png",
    "./texturas/enemigo2.png",
    "./texturas/enemigo3.png",
    "./texturas/enemigo4.png"
]

# Variables de estado
enMenu = True
en_como_jugar = False
correr = True
puntaje = 0

def mostrarPuntaje(ventana, puntaje):
    fuente = pygame.font.Font(None, 36)
    texto = fuente.render(f"Puntaje: {puntaje}", True, (255, 255, 255))
    ventana.blit(texto, (10, 10))

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

# Variables adicionales
puntajeJefe = 1000  # El puntaje en el que el jefe aparece
jefe = None  # Inicialmente no hay jefe
jefeDerrotado = False
jugador.y = altoVentana - jugador.imagen.get_height() - 20

while correr:
    obtenerMouse = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            correr = False
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
                        en_como_jugar = True
                    elif opcion == "Salir":
                        correr = False
            elif en_como_jugar:
                if event.key == K_RETURN:
                    en_como_jugar = False
                    enMenu = True
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

        ventana.blit(fondo, (0, 0))
        jugador.mover()

        for proyectil in jugador.proyectiles:
            proyectil.mover()
            ventana.blit(proyectil.imagen, (proyectil.x, proyectil.y))
            if proyectil.y < 0:
                jugador.proyectiles.remove(proyectil)
            for enemigo in enemigos:
                if proyectil.colisiona(enemigo):
                    if enemigo.recibirDano(50):
                        enemigos.remove(enemigo)
                        puntaje += 100
                    jugador.proyectiles.remove(proyectil)
                    break

        for enemigo in enemigos:
            enemigo.mover()
            ventana.blit(enemigo.imagen, (enemigo.x, enemigo.y))

        # Comprobar si el puntaje alcanza el valor para aparecer el jefe
        if puntaje >= puntajeJefe and not jefe:
            jefe = Jefe(x=anchoVentana // 2 - nuevoAncho, y=50, imagenPath="./texturas/jefeFinal.png", velocidad=2, vida=500)

        # Mover y dibujar el jefe si está presente
        if jefe and not jefeDerrotado:
            jefe.mover()
            ventana.blit(jefe.imagen, (jefe.x, jefe.y))
            jefe.disparar()  # Asegúrate de que el jefe esté disparando

            for proyectil in jugador.proyectiles:
                if proyectil.colisiona(jefe):
                    if jefe.recibirDano(50):
                        jefe_derrotado = True
                        jefe = None
                    jugador.proyectiles.remove(proyectil)

        # Dibujar el jugador
        ventana.blit(jugador.imagen, (jugador.x, jugador.y))

        # Mostrar el puntaje
        mostrarPuntaje(ventana, puntaje)

    pygame.display.update()

pygame.quit()
