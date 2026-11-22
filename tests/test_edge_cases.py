"""Terminales iguales, destino aislado y arcos desactivados."""

import unittest

from core.ediciones import cambiar_estado
from core.red import arcos_activos, cargar_red
from core.resolvedor import resolver


class TestCasosBorde(unittest.TestCase):
    """Comprueba los casos borde exigidos al resolvedor."""

    def setUp(self):
        """Sin entradas externas; carga una red nueva y no devuelve valor."""
        self.red = cargar_red("data/initial_network.json")

    def test_destino_inalcanzable(self):
        """Sin entradas al destino, comprueba resultado cero; no devuelve valor."""
        cambiar_estado(self.red, "VAL-PMO", False)
        cambiar_estado(self.red, "OSO-PMO", False)
        resultado = resolver(self.red, "STG", "PMO")
        self.assertEqual(resultado["max_flow_value"], 0)
        self.assertEqual(resultado["iterations"], [])
        self.assertEqual(resultado["cut"]["capacity"], 0)

    def test_terminales_iguales(self):
        """Con origen igual al destino, comprueba el código de error; no devuelve valor."""
        self.assertEqual(resolver(self.red, "STG", "STG"), {"error": "E_ST_EQUAL"})

    def test_arco_desactivado(self):
        """Con CON-TEM inactivo, comprueba que flows solo contiene activos; no devuelve valor."""
        cambiar_estado(self.red, "CON-TEM", False)
        resultado = resolver(self.red, "STG", "PMO")
        self.assertNotIn("CON-TEM", resultado["flows"])
        self.assertEqual(set(resultado["flows"]), {arco["id"] for arco in arcos_activos(self.red)})
