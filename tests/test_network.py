"""Pruebas de carga de redes y filtrado de arcos activos (D1, D2)."""
import unittest

from core.network import active_arcs, load_network


class TestNetwork(unittest.TestCase):
    """Convierte el "listo cuando" de D1 y D2 en comprobaciones."""

    def test_load_network(self):
        """Los tres JSON de data/ cargan como dict con nodes y arcs."""
        for name in ("figura1", "initial_network", "manual_case"):
            network = load_network(f"data/{name}.json")
            self.assertIsInstance(network, dict)
            self.assertIn("nodes", network)
            self.assertIn("arcs", network)

    def test_active_arcs(self):
        """figura1 tiene 7 arcos activos; al desactivar uno quedan 6."""
        network = load_network("data/figura1.json")
        self.assertEqual(len(active_arcs(network)), 7)
        network["arcs"][0]["active"] = False
        self.assertEqual(len(active_arcs(network)), 6)
