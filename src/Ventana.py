import pygame
import os


class Ventana:
    def __init__(self, rows, cols, mode, MARGIN, CELDA_SIZE):
        os.environ['SDL_VIDEO_CENTERED'] = '1'  # Establece la variable de entorno para centrar la ventana y la centra
        pygame.init()
        self.screen = pygame.display.set_mode(self.calcularTamañoVentana(rows, cols, mode, MARGIN, CELDA_SIZE))
        pygame.display.set_caption("Nonograma")

        
    def update(self):
        pygame.display.flip()

    def calcularTamañoVentana(self, rows, cols, mode, MARGIN, CELDA_SIZE):
        if mode == "clasico":
            ancho = MARGIN + 90 + (cols * CELDA_SIZE) + MARGIN
            alto = MARGIN + 90 + (rows * CELDA_SIZE) + MARGIN
            return (ancho, alto)
        elif mode == "dos_colores":
            ancho = MARGIN + 100 + (cols * CELDA_SIZE) + MARGIN
            alto = MARGIN + 140 + (rows * CELDA_SIZE) + MARGIN
            return (ancho, alto)
        