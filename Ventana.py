import pygame


class Ventana:
    def __init__(self, rows, cols, MARGIN, CELDA_SIZE):
        pygame.init()
        self.crearVentana(rows, cols, MARGIN, CELDA_SIZE)

        
    def update(self):
        pygame.display.flip()

    def calcularTamañoVentana(self, rows, cols, MARGIN, CELDA_SIZE):
        ancho = MARGIN + 120 + (cols * CELDA_SIZE) + MARGIN
        alto = MARGIN + 70 + (rows * CELDA_SIZE) + MARGIN
        return (ancho, alto)
        
    def crearVentana(self, rows, cols, MARGIN, CELDA_SIZE):
        self.screen = pygame.display.set_mode(self.calcularTamañoVentana(rows, cols, MARGIN, CELDA_SIZE))
        pygame.display.set_caption("Nonograma")
        return self.screen