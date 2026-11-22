"""Casos de aceptación de N2, N3, N5, N6 y N7."""

import unittest
from copy import deepcopy

from core.ediciones import agregar_arco, cambiar_capacidad, cambiar_estado
from core.red import cargar_red
from core.validacion import capacidad_valida, validar_arco_nuevo, validar_red


class TestValidacion(unittest.TestCase):
    """Comprueba códigos de error y que las ediciones rechazadas no cambien la red."""

    def test_capacidad_valida(self):
        """Con límites y tipos inválidos, comprueba N2; no devuelve valor."""
        for valor in (1, 12):
            self.assertTrue(capacidad_valida(valor))
        for valor in (0, 13, 2.5, "5", True):
            with self.subTest(valor=valor):
                self.assertFalse(capacidad_valida(valor))

    def test_arco_nuevo(self):
        """Con arcos válidos e inválidos, comprueba N3 y rechazo sin cambios; no devuelve valor."""
        red = cargar_red("data/figura1.json")
        for u, v, capacidad, esperado in (
            ("A", "O", 5, "E_RECIPROCAL"),
            ("A", "A", 5, "E_LOOP"),
            ("O", "A", 5, "E_DUPLICATE"),
            ("O", "C", 13, "E_CAPACITY"),
            ("X", "C", 5, "E_UNKNOWN_NODE"),
        ):
            with self.subTest(u=u, v=v):
                antes = deepcopy(red)
                self.assertEqual(validar_arco_nuevo(red, u, v, capacidad), esperado)
                self.assertEqual(agregar_arco(red, u, v, capacidad), esperado)
                self.assertEqual(red, antes)
        self.assertIsNone(validar_arco_nuevo(red, "O", "C", 5))
        cambiar_estado(red, "O-A", False)
        self.assertEqual(validar_arco_nuevo(red, "A", "O", 5), "E_RECIPROCAL")
        self.assertEqual(validar_arco_nuevo(red, "O", "A", 5), "E_DUPLICATE")

    def test_redes_y_perfil(self):
        """Con tres JSON y un perfil incorrecto, comprueba N5; no devuelve valor."""
        for archivo in ("figura1", "manual_case", "initial_network"):
            with self.subTest(red=archivo):
                self.assertEqual(validar_red(cargar_red(f"data/{archivo}.json")), [])
        red = cargar_red("data/figura1.json")
        red["profile"] = "initial"
        self.assertEqual(set(validar_red(red)), {"E_V_RANGE", "E_E_RANGE"})

    def test_invariantes_red(self):
        """Con una infracción por red, comprueba los códigos globales; no devuelve valor."""
        for u, v, capacidad, esperado in (
            ("A", "A", 5, "E_LOOP"),
            ("O", "A", 5, "E_DUPLICATE"),
            ("A", "O", 5, "E_RECIPROCAL"),
            ("O", "C", 13, "E_CAPACITY"),
        ):
            with self.subTest(error=esperado):
                red = cargar_red("data/figura1.json")
                red["arcs"].append({
                    "id": f"{u}-{v}", "from": u, "to": v,
                    "capacity": capacidad, "active": True,
                })
                self.assertEqual(validar_red(red), [esperado])

    def test_agregar_arco(self):
        """Con una adición válida y otra recíproca, comprueba N6; no devuelve valor."""
        red = cargar_red("data/initial_network.json")
        antes = deepcopy(red)
        self.assertEqual(agregar_arco(red, "TEM", "CON", 5), "E_RECIPROCAL")
        self.assertEqual(red, antes)
        self.assertEqual(len(red["arcs"]), 19)
        self.assertIsNone(agregar_arco(red, "CON", "VAL", 8))
        self.assertEqual(len(red["arcs"]), 20)
        self.assertEqual(red["arcs"][-1], {
            "id": "CON-VAL", "from": "CON", "to": "VAL", "capacity": 8, "active": True,
        })

    def test_cambiar_capacidad(self):
        """Con capacidades válidas e inválidas, comprueba N7 sin cambios al rechazar; no devuelve valor."""
        red = cargar_red("data/initial_network.json")
        self.assertIsNone(cambiar_capacidad(red, "CON-TEM", 9))
        arco = next(arco for arco in red["arcs"] if arco["id"] == "CON-TEM")
        self.assertEqual(arco["capacity"], 9)
        antes = deepcopy(red)
        for capacidad in (0, 13):
            with self.subTest(capacidad=capacidad):
                self.assertEqual(cambiar_capacidad(red, "CON-TEM", capacidad), "E_CAPACITY")
                self.assertEqual(red, antes)
