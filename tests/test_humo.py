"""Prueba de humo para verificar que los paquetes de core importan sin errores."""

import unittest


class TestSmokeImports(unittest.TestCase):
    """Comprueba que los módulos base de core importan usando solo biblioteca estándar."""

    def test_imports(self):
        """Verifica la importación de core y sus submódulos sin depender de Streamlit."""
        import core
        import core.ediciones
        import core.red
        import core.validacion

        self.assertIsNotNone(core)
        self.assertIsNotNone(core.red)
        self.assertIsNotNone(core.validacion)
        self.assertIsNotNone(core.ediciones)
