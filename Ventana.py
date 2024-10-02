import pygame

class Ventana:
    def __init__(self, ancho, alto):
        pygame.init()
        self.screen = pygame.display.set_mode((ancho, alto))
        pygame.display.set_caption("Nonograma")

    def update(self):
        pygame.display.flip()

