import unittest
from src.Celda import Celda

import unittest
from src.Celda import Celda

class TestCelda(unittest.TestCase):

    def setUp(self):
        # Inicia una celda en la posición (0, 0) para las pruebas
        self.celda = Celda((0, 0))

    def test_estado_inicial(self):
        """Probar que la celda empieza sin estar llena (is_filled == False)."""
        self.assertFalse(self.celda.is_painted)

    def test_posicion(self):
        """Probar que la posición de la celda es correcta."""
        self.assertEqual(self.celda.position, (0, 0))

if __name__ == '__main__':
    unittest.main()