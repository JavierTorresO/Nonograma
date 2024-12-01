import unittest
import pygame
from src.main import Main
from src.Tablero import Tablero
from src.Ventana import Ventana
from src.menu import mostrar_menu_size

# Tamaños
CELDA_SIZE = 30
MARGIN = 40

# Colores
NEGRO = (0, 0, 0)
GRIS = (200, 200, 200)
GRIS_OSCURO = (150, 150, 150)
ROJO = (255, 0, 0)
BEIGE = (160, 121, 95)

class TestMain(unittest.TestCase):

    def setUp(self):
        pygame.init()
        self.game = Main()

    def tearDown(self):
        pygame.quit()

    def test_initialization(self):
        """Probar que la inicialización del juego es correcta."""
        self.assertIsInstance(self.game.board, Tablero)
        self.assertIsInstance(self.game.window, Ventana)
        self.assertTrue(self.game.running)
        self.assertIsNone(self.game.win_time)
        self.assertFalse(self.game.win_sound_played)

    def test_handle_events_quit(self):
        """Probar que el evento QUIT detiene el juego."""
        pygame.event.post(pygame.event.Event(pygame.QUIT))
        self.game.handle_events()
        self.assertFalse(self.game.running)

    def test_handle_events_click_izquierdo(self):
        """Probar que el clic izquierdo del mouse maneja correctamente las celdas."""
        pos = (MARGIN + 100 + CELDA_SIZE // 2, MARGIN + 100 + CELDA_SIZE // 2)
        pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=pos))
        self.game.handle_events()
        cell = self.game.board.get_cell((0, 0))
        self.assertTrue(cell.is_painted)

    def test_handle_events_click_derecho(self):
        """Probar que el clic derecho del mouse alterna la 'X' en la celda."""
        pos = (MARGIN + 100 + CELDA_SIZE // 2, MARGIN + 100 + CELDA_SIZE // 2)
        pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=3, pos=pos))
        self.game.handle_events()
        cell = self.game.board.get_cell((0, 0))
        self.assertTrue(cell.is_x)

    def test_handle_events_escape(self):
        """Probar que presionar Escape vuelve al menú."""
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE))
        self.game.handle_events()
        self.assertIsInstance(self.game.board, Tablero)
        self.assertIsInstance(self.game.window, Ventana)

    def test_run(self):
        """Probar que el método run se ejecuta sin errores."""
        self.game.running = False  # Detener el bucle después de una iteración
        try:
            self.game.run()
        except Exception as e:
            self.fail(f"El método run lanzó una excepción: {e}")

    def test_return_to_menu(self):
        """Probar que return_to_menu reinicia el juego correctamente."""
        self.game.return_to_menu()
        self.assertIsNone(self.game.win_time)
        self.assertFalse(self.game.win_sound_played)
        self.assertIsInstance(self.game.board, Tablero)
        self.assertIsInstance(self.game.window, Ventana)

if __name__ == '__main__':
    unittest.main()