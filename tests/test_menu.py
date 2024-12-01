import unittest
import pygame
from src.menu import mostrar_menu_size, seleccionar_opcion

class TestMenu(unittest.TestCase):

    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))

    def tearDown(self):
        pygame.quit()

    def test_mostrar_menu_size(self):
        """Probar que mostrar_menu_size devuelve el tamaño correcto del tablero."""
        # Simular eventos de teclado para seleccionar la opción '5x5'
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN))
        size = mostrar_menu_size(self.screen)
        self.assertEqual(size, (5, 5, 1))

        # Simular eventos de teclado para seleccionar la opción '10x10'
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN))
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN))
        size = mostrar_menu_size(self.screen)
        self.assertEqual(size, (10, 10, 1))

        # Simular eventos de teclado para seleccionar la opción '15x15'
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN))
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN))
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN))
        size = mostrar_menu_size(self.screen)
        self.assertEqual(size, (15, 15, 1))

        # Simular eventos de teclado para seleccionar la opción '20x20'
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN))
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN))
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN))
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN))
        size = mostrar_menu_size(self.screen)
        self.assertEqual(size, (20, 20, 1))

        # Simular eventos de teclado para seleccionar la opción 'Salir'
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN))
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN))
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN))
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN))
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN))
        with self.assertRaises(SystemExit):
            mostrar_menu_size(self.screen)

if __name__ == '__main__':
    unittest.main()