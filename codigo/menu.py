import pygame
from pygame.locals import *

# Clase Menu
class Menu:
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.opciones = ["Iniciar Juego", "Cómo Jugar", "Salir"]
        self.seleccionado = 0
        self.fuente = pygame.font.Font(None, 40)
        self.color_fondo = (0, 0, 0)
        self.color_texto = (255, 255, 255)
        self.color_seleccionado = (255, 0, 0)

    def dibujar(self, ventana):
        ventana.fill(self.color_fondo)
        for i, opcion in enumerate(self.opciones):
            if i == self.seleccionado:
                color = self.color_seleccionado
            else:
                color = self.color_texto
            texto = self.fuente.render(opcion, True, color)
            rect = texto.get_rect(center=(self.ancho / 2, self.alto / 2 + i * 60))
            ventana.blit(texto, rect)

    def mover_seleccion(self, direccion):
        self.seleccionado += direccion
        if self.seleccionado < 0:
            self.seleccionado = len(self.opciones) - 1
        elif self.seleccionado >= len(self.opciones):
            self.seleccionado = 0

    def obtener_opcion(self):
        return self.opciones[self.seleccionado]
