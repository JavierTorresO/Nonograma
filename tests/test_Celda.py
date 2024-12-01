import unittest
from src.Celda import Celda

class TestCelda(unittest.TestCase):

    def setUp(self):
        # Inicia una celda en la posición (0, 0) para las pruebas
        self.celda = Celda((0, 0))

    def test_posicion(self):
        """Probar que la posición de la celda es correcta."""
        self.assertEqual(self.celda.position, (0, 0))

    def test_is_painted_inicial(self):
        """Probar que la celda empieza sin estar pintada (is_painted == False)."""
        self.assertFalse(self.celda.is_painted)

    def test_is_x_inicial(self):
        """Probar que la celda empieza sin tener una 'X' (is_x == False)."""
        self.assertFalse(self.celda.is_x)

    def test_is_locked_inicial(self):
        """Probar que la celda empieza sin estar bloqueada (is_locked == False)."""
        self.assertFalse(self.celda.is_locked)

    def test_toggle(self):
        """Probar que el método toggle cambia el estado de is_painted."""
        self.celda.toggle()
        self.assertTrue(self.celda.is_painted)
        self.celda.toggle()
        self.assertFalse(self.celda.is_painted)

    def test_toggle_x(self):
        """Probar que el método toggle_x cambia el estado de is_x."""
        self.celda.toggle_x()
        self.assertTrue(self.celda.is_x)
        self.celda.toggle_x()
        self.assertFalse(self.celda.is_x)

    def test_lock(self):
        """Probar que sea posible bloquear la celda."""
        self.celda.is_locked = True
        self.assertTrue(self.celda.is_locked)

    def test_unlock(self):
        """Probar que sea posible desbloquear la celda."""
        self.celda.is_locked = False
        self.assertFalse(self.celda.is_locked)

if __name__ == '__main__':
    unittest.main()