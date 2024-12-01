import unittest
from src.Ventana import Ventana
import pygame

class TestVentana(unittest.TestCase):

    def setUp(self):
        self.rows = 10
        self.cols = 10
        self.MARGIN = 5
        self.CELDA_SIZE = 20
        self.ventana = Ventana(self.rows, self.cols, self.MARGIN, self.CELDA_SIZE)

    def test_calcularTamañoVentana(self):
        """Probar que el tamaño de la ventana se calcula correctamente."""
        expected_size = (self.MARGIN + 120 + (self.cols * self.CELDA_SIZE) + self.MARGIN,
                         self.MARGIN + 70 + (self.rows * self.CELDA_SIZE) + self.MARGIN)
        self.assertEqual(self.ventana.calcularTamañoVentana(self.rows, self.cols, self.MARGIN, self.CELDA_SIZE), expected_size)

    def test_crearVentana(self):
        """Probar que la ventana se crea correctamente."""
        screen = self.ventana.crearVentana(self.rows, self.cols, self.MARGIN, self.CELDA_SIZE)
        self.assertIsNotNone(screen)
        self.assertIsInstance(screen, pygame.Surface)

    def test_update(self):
        """Probar que la ventana se actualiza correctamente."""
        self.ventana.update()
        # No hay una manera directa de probar pygame.display.flip(), pero no debería lanzar una excepción

if __name__ == '__main__':
    unittest.main()