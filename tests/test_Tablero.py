import unittest
from src.Tablero import Tablero, seleccionar_nanograma
from src.Celda import Celda
import pygame

class TestTablero(unittest.TestCase):

    def setUp(self):
        self.rows = 5
        self.cols = 5
        self.tipo = 1
        self.tablero = Tablero(self.rows, self.cols, self.tipo)

    def test_inicializacion(self):
        """Probar que el tablero se inicializa correctamente."""
        self.assertEqual(self.tablero.rows, self.rows)
        self.assertEqual(self.tablero.cols, self.cols)
        self.assertEqual(self.tablero.tipo, self.tipo)
        self.assertEqual(len(self.tablero.cells), self.rows)
        self.assertEqual(len(self.tablero.cells[0]), self.cols)
        self.assertIsInstance(self.tablero.cells[0][0], Celda)

    def test_seleccionar_nanograma(self):
        """Probar que seleccionar_nanograma devuelve las pistas y la solución correctas."""
        hints, solution = seleccionar_nanograma(self.rows, self.cols, self.tipo)
        self.assertEqual(hints, self.tablero.hints)
        self.assertEqual(solution, self.tablero.solution)

    def test_draw(self):
        """Probar que el método draw no lanza excepciones."""
        screen = pygame.Surface((300, 300))
        try:
            self.tablero.draw(screen)
        except Exception as e:
            self.fail(f"El método draw lanzó una excepción: {e}")

    def test_get_cell(self):
        """Probar que get_cell devuelve la celda correcta."""
        cell = self.tablero.get_cell((0, 0))
        self.assertIsInstance(cell, Celda)
        self.assertEqual(cell.position, (0, 0))

        cell = self.tablero.get_cell((self.cols - 1, self.rows - 1))
        self.assertIsInstance(cell, Celda)
        self.assertEqual(cell.position, (self.cols - 1, self.rows - 1))

        cell = self.tablero.get_cell((self.cols, self.rows))
        self.assertIsNone(cell)

    def test_check_win(self):
        """Probar que check_win devuelve False para un tablero no resuelto."""
        self.assertFalse(self.tablero.check_win())

        # Pintar el tablero según la solución para probar que check_win devuelve True
        for i in range(self.rows):
            for j in range(self.cols):
                self.tablero.cells[i][j].is_painted = self.tablero.solution[i][j]
        self.assertTrue(self.tablero.check_win())

if __name__ == '__main__':
    unittest.main()