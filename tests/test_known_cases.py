"""Resultados conocidos de las tres redes del proyecto."""

import unittest

from core.red import cargar_red
from core.resolvedor import resolver


class TestCasosConocidos(unittest.TestCase):
    """Contrasta el resultado completo con las referencias de la fase 1."""

    def comprobar_red(self, archivo, valor, iteraciones, S):
        """Recibe archivo y resultados esperados; comprueba el contrato sin devolver valor."""
        red = cargar_red(f"data/{archivo}.json")
        resultado = resolver(red, red["source"], red["sink"])
        self.assertEqual(resultado["max_flow_value"], valor)
        self.assertEqual(len(resultado["iterations"]), iteraciones)
        self.assertEqual(resultado["cut"]["S"], S)
        self.assertEqual(resultado["max_flow_value"], resultado["cut"]["capacity"])
        for clave in ("capacity_ok", "conservation_ok", "duality_ok"):
            self.assertIs(resultado["checks"][clave], True)

    def test_figura1(self):
        """Sin entradas externas; comprueba la Figura 1 y no devuelve valor."""
        self.comprobar_red("figura1", 14, 3, ["O"])

    def test_manual(self):
        """Sin entradas externas; comprueba el caso manual y no devuelve valor."""
        self.comprobar_red("manual_case", 8, 3, ["a", "c", "s"])

    def test_inicial(self):
        """Sin entradas externas; comprueba la red inicial y no devuelve valor."""
        self.comprobar_red("initial_network", 20, 9, ["CHI", "CON", "LAN", "RAN", "STG", "TAL"])
