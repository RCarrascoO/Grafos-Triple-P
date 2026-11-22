"""Efecto de cada edición sobre una copia de la red inicial."""

import unittest
from copy import deepcopy

from core.ediciones import agregar_arco, cambiar_capacidad, cambiar_estado
from core.red import cargar_red
from core.resolvedor import resolver


class TestModificaciones(unittest.TestCase):
    """Comprueba por separado las tres modificaciones candidatas."""

    def setUp(self):
        """Sin entradas externas; prepara una copia independiente y no devuelve valor."""
        self.red = deepcopy(cargar_red("data/initial_network.json"))

    def test_desactivar(self):
        """Con una ruta desactivada, comprueba flujo 13; no devuelve valor."""
        cambiar_estado(self.red, "CON-TEM", False)
        self.assertEqual(resolver(self.red, "STG", "PMO")["max_flow_value"], 13)

    def test_ampliar(self):
        """Con capacidad 9 en CON-TEM, comprueba flujo 21; no devuelve valor."""
        self.assertIsNone(cambiar_capacidad(self.red, "CON-TEM", 9))
        self.assertEqual(resolver(self.red, "STG", "PMO")["max_flow_value"], 21)

    def test_agregar(self):
        """Con CON-VAL de capacidad 8, comprueba flujo y corte; no devuelve valor."""
        self.assertIsNone(agregar_arco(self.red, "CON", "VAL", 8))
        resultado = resolver(self.red, "STG", "PMO")
        self.assertEqual(resultado["max_flow_value"], 23)
        self.assertEqual(resultado["cut"]["arcs"], ["OSO-PMO", "VAL-PMO"])
