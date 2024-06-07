import pygame
from pygame.locals import *
import random

# Inicializar Pygame
pygame.init()

# Constantes

nuevoAncho = 100
nuevoAlto = 100
anchoPantalla = 800
altoPantalla = 600

#-------------------------------------------
# Clase base Entidad
class Entidad(pygame.sprite.Sprite):
    def __init__(self, x, y, velocidad, vida):
        super().__init__()  # Inicializa la clase base de pygame.sprite.Sprite
        self.x = x
        self.y = y
        self.velocidad = velocidad
        self.vida = vida

    def recibirDano(self, cantidad):
        self.vida -= cantidad
        if self.vida < 0:
            self.vida = 0

# Clase Proyectil que hereda de Entidad
class Proyectil(Entidad):
    def __init__(self, x, y):
        super().__init__(x, y, velocidad=7, vida=1)  # Llama al constructor de la clase base
        self.ancho = nuevoAncho
        self.alto = nuevoAlto
        self.imagen = pygame.image.load("./texturas/proyectil1.png")
        self.ancho = self.imagen.get_width()

    def mover(self):
        self.y -= self.velocidad

    def colisiona(self, enemigo):
        proyectilRect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        enemigoRect = pygame.Rect(enemigo.x, enemigo.y, enemigo.ancho, enemigo.alto)
        return proyectilRect.colliderect(enemigoRect)

#-------------------------------------------

# Clase Jugador que hereda de Entidad
class Jugador(Entidad):
    def __init__(self, imagenPath):
        super().__init__(x=300, y=500, velocidad=2, vida=100)  # Llama al constructor de la clase base
        imagenOriginal = pygame.image.load(imagenPath)
        self.imagen = pygame.transform.scale(imagenOriginal, (nuevoAncho, nuevoAlto))
        self.ancho = self.imagen.get_width()
        self.alto = self.imagen.get_height()
        self.proyectiles = []  # Composición: el jugador tiene una lista de proyectiles
        self.puedeDisparar = True

    def disparar(self):
        if self.puedeDisparar:
            proyectil = Proyectil(self.x + 20, self.y)
            self.proyectiles.append(proyectil)
            self.puedeDisparar = False
                
    def mover(self):
        teclas = pygame.key.get_pressed()
        if teclas[K_LEFT]:
            self.x -= self.velocidad
        if teclas[K_RIGHT]:
            self.x += self.velocidad

# Instancia del jugador
jugador = Jugador("./texturas/nave.png")
jugador.vida = 150

#-------------------------------------------

# Clase Enemigo que hereda de Entidad
class Enemigo(Entidad):
    def __init__(self, x, y, imagenPath, velocidad, vida):
        super().__init__(x, y, velocidad, vida)  # Llama al constructor de la clase base
        imagenOriginal = pygame.image.load(imagenPath)
        self.imagen = pygame.transform.scale(imagenOriginal, (nuevoAncho, nuevoAlto))
        self.ancho = self.imagen.get_width()
        self.alto = self.imagen.get_height()
        self.direccion = 1  # 1 significa moviéndose a la derecha, -1 significa moviéndose a la izquierda

    def mover(self):
        self.x += self.velocidad * self.direccion
        if self.x <= 0 or self.x + self.ancho >= anchoPantalla:
            self.direccion *= -1
            self.y += self.alto  # Mueve al enemigo hacia abajo cuando cambia de dirección

#-------------------------------------------

# Crear una formación de enemigos en cuadrícula
def crearFormacionEnemigos(filas, columnas, imagenPath):
    enemigos = []
    paddingX = 3
    paddingY = 3
    for fila in range(filas):
        for columna in range(columnas):
            x = columna * (nuevoAncho + paddingX)
            y = fila * (nuevoAlto + paddingY)
            enemigo = Enemigo(x, y, imagenPath, velocidad=1, vida=100)
            enemigos.append(enemigo)
    return enemigos

# Crear la formación de enemigos
enemigos = crearFormacionEnemigos(3, 4, "./texturas/enemigo1.png",)
