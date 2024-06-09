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

intervaloDisparo = 500  # Intervalo de tiempo entre disparos en milisegundos

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
        if self.vida <= 0:
            self.vida = 0
            return True
        return False

# Clase Proyectil que hereda de Entidad
class Proyectil(Entidad):
    def __init__(self, x, y):
        super().__init__(x, y, velocidad=7, vida=1)  # Llama al constructor de la clase base
        self.ancho = nuevoAncho // 2
        self.alto = nuevoAlto // 2
        self.imagen = pygame.image.load("./texturas/proyectil1.png")
        self.imagen = pygame.transform.scale(self.imagen, (self.ancho, self.alto))

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
        super().__init__(x=300, y=500, velocidad=4, vida=100)  # Llama al constructor de la clase base
        imagenOriginal = pygame.image.load(imagenPath)
        self.imagen = pygame.transform.scale(imagenOriginal, (nuevoAncho, nuevoAlto))
        self.ancho = self.imagen.get_width()
        self.alto = self.imagen.get_height()
        self.proyectiles = []  # Composición: el jugador tiene una lista de proyectiles
        self.ultimo_disparo = pygame.time.get_ticks()

    def disparar(self):
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.ultimo_disparo > intervaloDisparo:
            proyectil = Proyectil(self.x + self.ancho // 2 - 10, self.y)
            self.proyectiles.append(proyectil)
            self.ultimo_disparo = tiempo_actual
                
    def mover(self):
        teclas = pygame.key.get_pressed()
        if teclas[K_LEFT] and self.x > 0:
            self.x -= self.velocidad
        if teclas[K_RIGHT] and self.x < anchoPantalla - self.ancho:
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
            if self.x < 0:
                self.x = 0
            if self.x + self.ancho > anchoPantalla:
                self.x = anchoPantalla - self.ancho
                
# Clase Jefe que hereda de Entidad
class Jefe(Entidad):
    def __init__(self, x, y, imagenPath, velocidad, vida):
        super().__init__(x, y, velocidad, vida)  # Llama al constructor de la clase base
        imagenOriginal = pygame.image.load(imagenPath)
        self.imagen = pygame.transform.scale(imagenOriginal, (nuevoAncho * 2, nuevoAlto * 2))  # Tamaño mayor
        self.ancho = self.imagen.get_width()
        self.alto = self.imagen.get_height()
        self.direccion = 1  # 1 significa moviéndose a la derecha, -1 significa moviéndose a la izquierda
        self.ultimo_disparo = pygame.time.get_ticks()
        self.intervalo_disparo = 1000  # Intervalo de tiempo entre disparos en milisegundos

    def mover(self):
        self.x += self.velocidad * self.direccion
        if self.x <= 0 or self.x + self.ancho >= anchoPantalla:
            self.direccion *= -1
            self.y += self.alto // 2  # Mueve al jefe hacia abajo cuando cambia de dirección
            if self.x < 0:
                self.x = 0
            if self.x + self.ancho > anchoPantalla:
                self.x = anchoPantalla - self.ancho

    def disparar(self):
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.ultimo_disparo > self.intervalo_disparo:
            # Aquí puedes definir el comportamiento de disparo del jefe, como crear proyectiles
            print("El jefe está disparando")
            self.ultimo_disparo = tiempo_actual


#-------------------------------------------

# Crear una formación de enemigos en cuadrícula
def crearFormacionEnemigos(filas, columnas, imagenPaths):
    enemigos = []
    paddingX = 20  # Aumentar el espacio horizontal entre enemigos
    paddingY = 20  # Aumentar el espacio vertical entre enemigos
    for fila in range(filas):
        for columna in range(columnas):
            x = columna * (nuevoAncho + paddingX)
            y = fila * (nuevoAlto + paddingY)
            index = fila * columnas + columna
            imagen_path = imagenPaths[index % len(imagenPaths)]
            enemigo = Enemigo(x, y, imagen_path, velocidad=1, vida=100)
            enemigos.append(enemigo)
    return enemigos

# Lista de rutas de imágenes de enemigos
tipos_enemigos = [
    "./texturas/enemigo1.png",
    "./texturas/enemigo2.png",
    "./texturas/enemigo3.png",
    "./texturas/enemigo4.png"
]

# Crear la formación de enemigos
enemigos = crearFormacionEnemigos(3, 4, tipos_enemigos)