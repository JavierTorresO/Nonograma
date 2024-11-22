import unittest
import pygame

from src.Tablero import Tablero


class TestX(unittest.TestCase):
    def setUp(self):
        #crear una instancia del tablero.
        pygame.init()
        self.tablero = Tablero(rows=5, cols=5, tipo="normal")
        self.screen = pygame.display.set_mode((800, 600))

    def test_mark_x_on_cell(self):
        # Simular un clic derecho en una celda (ejemplo, (2, 3)).
        pos = (2, 3)
        self.tablero.handle_right_click(pos)  # Método que debería marcar la "X"

        # Verificar que la celda se marcó con una "X".
        self.assertTrue(self.tablero.cells[2][3].is_x)

    def test_prevent_paint_over_x(self):
        # Simular un clic derecho en una celda (ejemplo, (2, 3)) y marcar "X".
        pos = (2, 3)
        self.tablero.handle_right_click(pos)
        self.assertTrue(self.tablero.cells[2][3].is_x)

        # Intentar pintar sobre la celda marcada con "X".
        self.tablero.handle_left_click(pos)  # Método para pintar la celda
        self.assertFalse(self.tablero.cells[2][3].is_painted)  # Asegurarse de que no se pintó

if __name__ == '__main__':
    unittest.main()

