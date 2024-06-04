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
        super().__init__(x, y, velocidad=10, vida=1)  # Llama al constructor de la clase base
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

# Clase Jugador que hereda de Entidad
class Jugador(Entidad):
    def __init__(self, imagenPath):
        super().__init__(x=300, y=600, velocidad=2, vida=100)  # Llama al constructor de la clase base
        imagenOriginal = pygame.image.load(imagenPath)
        self.imagen = pygame.transform.scale(imagenOriginal, (nuevoAncho, nuevoAlto))
        self.ancho = self.imagen.get_width()
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

# Clase Enemigo que hereda de Entidad
class Enemigo(Entidad):
    def __init__(self, imagenPath, ancho, alto):
        super().__init__(x=random.randint(0, anchoPantalla - ancho), y=0, velocidad=5, vida=100)  # Llama al constructor de la clase base
        imagenOriginal = pygame.image.load(imagenPath)
        self.imagen = pygame.transform.scale(imagenOriginal, (ancho, alto))
        self.rect = self.imagen.get_rect()
        self.rect.x = random.randrange(anchoPantalla - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.velocidady = random.randrange(1, 10)

    def mover(self):
        self.rect.y += self.velocidady

# Instancias de enemigos
enemigo1 = Enemigo("./texturas/enemigo1.png", 100, 100)
enemigo2 = Enemigo("./texturas/enemigo2.png", 150, 150)
enemigo3 = Enemigo("./texturas/enemigo3.png", 150, 150)
enemigo4 = Enemigo("./texturas/enemigo4.png", 150, 150)

enemigo1.vida = 100
enemigo2.vida = 70
enemigo3.vida = 50
enemigo4.vida = 90