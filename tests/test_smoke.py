"""Prueba de humo para verificar que los paquetes y módulos importan sin errores."""
import unittest


class TestSmokeImports(unittest.TestCase):
    """Comprueba que el esqueleto y los módulos base no generan errores de importación."""

    def test_imports(self):
        """Verifica la importación de app, core y sus submódulos."""
        import app
        import core
        import core.edits
        import core.validation

        self.assertIsNotNone(core)
        self.assertIsNotNone(app)
