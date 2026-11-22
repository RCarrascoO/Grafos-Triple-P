"""Comparación con todos los cortes, sin usar el motor para calcular el mínimo."""

import random
import unittest
from itertools import combinations

from core.ediciones import agregar_arco
from core.red import cargar_red
from core.resolvedor import resolver
from core.validacion import validar_red
from core.verificacion import capacidad_corte


def brute_force_min_cut(network, s, t) -> int:
    """Recibe una red y terminales distintos; enumera cortes y devuelve su menor capacidad."""
    intermedios = [nodo["id"] for nodo in network["nodes"] if nodo["id"] not in (s, t)]
    minimo = capacidad_corte(network, {s})
    for cantidad in range(len(intermedios) + 1):
        for subconjunto in combinations(intermedios, cantidad):
            S = {s} | set(subconjunto)
            minimo = min(minimo, capacidad_corte(network, S))
    return minimo


class TestFuerzaBruta(unittest.TestCase):
    """Contrasta el motor con un procedimiento independiente en redes pequeñas."""

    def test_redes_conocidas(self):
        """Con los tres JSON, compara mínimo enumerado y flujo; no devuelve valor."""
        for archivo in ("figura1", "manual_case", "initial_network"):
            with self.subTest(red=archivo):
                red = cargar_red(f"data/{archivo}.json")
                s, t = red["source"], red["sink"]
                self.assertEqual(brute_force_min_cut(red, s, t), resolver(red, s, t)["max_flow_value"])

    def test_redes_aleatorias(self):
        """Con semilla 1, genera 20 redes válidas de seis nodos y compara; no devuelve valor."""
        random.seed(1)
        nodos = ["s", "a", "b", "c", "d", "t"]
        for numero in range(20):
            with self.subTest(red=numero):
                red = {
                    "nodes": [{"id": nodo} for nodo in nodos], "arcs": [],
                    "source": "s", "sink": "t", "profile": "manual",
                }
                for u, v in combinations(nodos, 2):
                    if random.random() < 0.5:
                        if random.random() < 0.5:
                            u, v = v, u
                        self.assertIsNone(agregar_arco(red, u, v, random.randint(1, 12)))
                self.assertEqual(validar_red(red), [])
                resultado = resolver(red, "s", "t")
                self.assertEqual(brute_force_min_cut(red, "s", "t"), resultado["max_flow_value"])
                for clave in ("capacity_ok", "conservation_ok", "duality_ok"):
                    self.assertIs(resultado["checks"][clave], True)
