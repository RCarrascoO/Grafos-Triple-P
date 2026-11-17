"""Casos de aceptación de S2–S6 y bordes de la verificación independiente."""

import unittest
from copy import deepcopy

from core.network import load_network
from core.verify import (
    check_capacity, check_conservation, cut_capacity, flow_value, verify_all,
)


class TestVerify(unittest.TestCase):
    """Comprueba las fórmulas con flujos de referencia, sin ejecutar el motor."""

    def setUp(self):
        """Sin entradas externas; prepara redes y flujos de referencia para cada prueba."""
        self.figure = load_network("data/figura1.json")
        self.figure_flows = {
            "O-A": 8, "O-B": 6, "A-C": 5, "A-D": 3,
            "B-D": 6, "C-T": 5, "D-T": 9,
        }
        self.manual = load_network("data/manual_case.json")
        self.manual_flows = {
            "s-b": 5, "s-c": 3, "b-a": 0, "b-d": 5,
            "c-a": 3, "d-c": 0, "a-t": 3, "d-t": 5,
        }

    def test_capacity(self):
        """Con flujos válidos e inválidos, comprueba aceptación y rechazo; no devuelve valor."""
        self.assertTrue(check_capacity(self.figure, self.figure_flows))
        for value in (9, -1, 2.5, True, "5"):
            with self.subTest(value=value):
                flows = self.figure_flows.copy()
                flows["O-A"] = value
                self.assertFalse(check_capacity(self.figure, flows))

    def test_conservation(self):
        """Con el caso manual, comprueba tabla ordenada y un desequilibrio; no devuelve valor."""
        ok, table = check_conservation(self.manual, self.manual_flows, "s", "t")
        self.assertTrue(ok)
        self.assertEqual(table, [
            {"node": "a", "in": 3, "out": 3},
            {"node": "b", "in": 5, "out": 5},
            {"node": "c", "in": 3, "out": 3},
            {"node": "d", "in": 5, "out": 5},
        ])
        self.manual_flows["c-a"] = 2
        ok, table = check_conservation(self.manual, self.manual_flows, "s", "t")
        self.assertFalse(ok)

    def test_flow_value(self):
        """Con dos referencias y una entrada al origen, comprueba flujo neto; no devuelve valor."""
        self.assertEqual(flow_value(self.figure, self.figure_flows, "O"), 14)
        self.assertEqual(flow_value(self.manual, self.manual_flows, "s"), 8)
        self.manual["arcs"].append(
            {"id": "a-s", "from": "a", "to": "s", "capacity": 2, "active": True}
        )
        self.manual_flows["a-s"] = 2
        self.assertEqual(flow_value(self.manual, self.manual_flows, "s"), 6)

    def test_cut_capacity(self):
        """Con cortes conocidos, comprueba suma y dirección de arcos; no devuelve valor."""
        network = load_network("data/initial_network.json")
        self.assertEqual(cut_capacity(network, {"STG", "RAN", "TAL", "CHI", "CON", "LAN"}), 20)
        self.assertEqual(cut_capacity(network, {"STG"}), 28)
        self.assertEqual(cut_capacity(self.manual, {"s", "a", "c"}), 8)

    def test_verify_all(self):
        """Con el caso manual, comprueba contrato y ausencia de mutaciones; no devuelve valor."""
        before = deepcopy((self.manual, self.manual_flows))
        checks = verify_all(self.manual, self.manual_flows, {"s", "a", "c"}, "s", "t")
        self.assertEqual(set(checks), {
            "capacity_ok", "conservation_ok", "conservation_table", "duality_ok",
        })
        for key in ("capacity_ok", "conservation_ok", "duality_ok"):
            self.assertIs(checks[key], True)
        self.assertEqual(checks["conservation_table"][0], {"node": "a", "in": 3, "out": 3})
        self.assertEqual((self.manual, self.manual_flows), before)
        checks = verify_all(self.manual, self.manual_flows, {"s"}, "s", "t")
        self.assertFalse(checks["duality_ok"])

    def test_inactive_arcs_and_isolated_nodes(self):
        """Sin arcos activos ni flujos, comprueba ceros y terminales del corte; no devuelve valor."""
        for arc in self.manual["arcs"]:
            arc["active"] = False
        checks = verify_all(self.manual, {}, {"s"}, "s", "t")
        self.assertTrue(checks["capacity_ok"])
        self.assertTrue(checks["conservation_ok"])
        self.assertTrue(checks["duality_ok"])
        self.assertEqual(checks["conservation_table"], [
            {"node": node, "in": 0, "out": 0} for node in ("a", "b", "c", "d")
        ])
        self.assertEqual(flow_value(self.manual, {}, "s"), 0)
        self.assertEqual(cut_capacity(self.manual, {"s"}), 0)
        for S in (set(), {"s", "t"}):
            checks = verify_all(self.manual, {}, S, "s", "t")
            self.assertFalse(checks["duality_ok"])
