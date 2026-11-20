"""Pruebas de los criterios "listo cuando" de R1-R8 (motor de flujo máximo y corte mínimo)."""

from copy import deepcopy
import unittest

from core.flujo_maximo import (
    aumentar,
    buscar_camino,
    cuello_botella,
    construir_residual,
    edmonds_karp,
)
from core.corte_minimo import corte_minimo, alcanzables_desde
from core.red import cargar_red
from core.resolvedor import resolver


class TestMaxFlowEngine(unittest.TestCase):
    """Comprueba R1-R8 contra los casos de aceptación y bordes del contrato."""

    def setUp(self):
        """Prepara las tres redes de referencia para cada prueba."""
        self.figura1 = cargar_red("data/figura1.json")
        self.manual = cargar_red("data/manual_case.json")
        self.initial = cargar_red("data/initial_network.json")

    def test_r1_build_residual(self):
        """R1: residual inicial de figura1 tiene 6 nodos, res[O][A]==8 y res[A][O]==0."""
        res = construir_residual(self.figura1)
        self.assertEqual(len(res), 6)
        self.assertEqual(res["O"]["A"], 8)
        self.assertEqual(res["A"]["O"], 0)

    def test_r2_r3_r4_bfs_bottleneck_augment(self):
        """R2-R4: primer camino en figura1 es O-A-C-T con cuello 5 y actualización correcta."""
        res = construir_residual(self.figura1)
        path = buscar_camino(res, "O", "T")
        self.assertEqual(path, ["O", "A", "C", "T"])
        self.assertEqual(cuello_botella(res, path), 5)

        aumentar(res, path, 5)
        self.assertEqual(res["O"]["A"], 3)
        self.assertEqual(res["A"]["O"], 5)
        self.assertEqual(res["C"]["T"], 0)

        for v in res["O"]:
            res["O"][v] = 0
        self.assertIsNone(buscar_camino(res, "O", "T"))

    def test_r5_edmonds_karp(self):
        """R5: valores e iteraciones exactas en figura1, manual_case e initial_network."""
        val_f, flows_f, iters_f, _ = edmonds_karp(self.figura1, "O", "T")
        self.assertEqual((val_f, len(iters_f)), (14, 3))
        self.assertEqual(len(flows_f), 7)

        val_m, flows_m, iters_m, _ = edmonds_karp(self.manual, "s", "t")
        self.assertEqual((val_m, len(iters_m)), (8, 3))
        self.assertEqual(iters_m[2]["path"], ["s", "c", "a", "b", "d", "t"])
        self.assertEqual(iters_m[2]["bottleneck"], 3)
        self.assertEqual(flows_m["b-a"], 0)

        val_i, flows_i, iters_i, _ = edmonds_karp(self.initial, "STG", "PMO")
        self.assertEqual((val_i, len(iters_i)), (20, 9))
        self.assertEqual(len(flows_i), 19)

    def test_r6_r7_min_cut(self):
        """R6-R7: alcanzables en manual_case y cortes mínimos en figura1 e initial_network."""
        _, _, _, res_m = edmonds_karp(self.manual, "s", "t")
        self.assertEqual(alcanzables_desde(res_m, "s"), {"s", "a", "c"})

        _, _, _, res_i = edmonds_karp(self.initial, "STG", "PMO")
        cut_i = corte_minimo(self.initial, res_i, "STG")
        self.assertEqual(cut_i["arcs"], ["CHI-TEM", "CON-TEM", "LAN-TEM", "LAN-VAL"])
        self.assertEqual(cut_i["capacity"], 20)

        _, _, _, res_f = edmonds_karp(self.figura1, "O", "T")
        cut_f = corte_minimo(self.figura1, res_f, "O")
        self.assertEqual(cut_f["S"], ["O"])
        self.assertEqual(cut_f["capacity"], 14)

    def test_r8_solve_and_edge_cases(self):
        """R8: contrato completo, sin mutar la red, errores de terminales y destino inalcanzable."""
        for net, s, t in (
            (self.figura1, "O", "T"),
            (self.manual, "s", "t"),
            (self.initial, "STG", "PMO"),
        ):
            before = deepcopy(net)
            result = resolver(net, s, t)
            self.assertEqual(net, before)
            self.assertEqual(
                set(result),
                {"source", "sink", "max_flow_value", "flows", "iterations", "cut", "checks"},
            )
            self.assertEqual(result["max_flow_value"], result["cut"]["capacity"])
            for key in ("capacity_ok", "conservation_ok", "duality_ok"):
                self.assertIs(result["checks"][key], True)

        self.assertEqual(resolver(self.initial, "STG", "STG"), {"error": "E_ST_EQUAL"})
        self.assertEqual(resolver(self.initial, "NO_EXISTE", "PMO"), {"error": "E_UNKNOWN_NODE"})
        self.assertEqual(resolver(self.initial, "STG", "NO_EXISTE"), {"error": "E_UNKNOWN_NODE"})

        disconnected = deepcopy(self.initial)
        for arc in disconnected["arcs"]:
            if arc["id"] in {"VAL-PMO", "OSO-PMO"}:
                arc["active"] = False
        result = resolver(disconnected, "STG", "PMO")
        self.assertEqual(result["max_flow_value"], 0)
        self.assertEqual(result["iterations"], [])
        self.assertEqual(result["cut"]["arcs"], [])
        self.assertEqual(result["cut"]["capacity"], 0)
        self.assertNotIn("VAL-PMO", result["flows"])
        self.assertIs(result["checks"]["duality_ok"], True)
