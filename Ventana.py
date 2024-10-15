import pygame


class Ventana:
    def __init__(self, rows, cols, MARGIN, CELDA_SIZE):
        pygame.init()
        self.screen = pygame.display.set_mode(self.calcularTamañoVentana(rows, cols, MARGIN, CELDA_SIZE))
        pygame.display.set_caption("Nonograma")
        
    def update(self):
        pygame.display.flip()

    def calcularTamañoVentana(self, rows, cols, MARGIN, CELDA_SIZE):
        ancho = MARGIN + 100 + (cols * CELDA_SIZE) + MARGIN
        alto = MARGIN + 50 + (rows * CELDA_SIZE) + MARGIN
        return (ancho, alto)