"""Punto de entrada único del motor: flujo máximo, corte mínimo y verificación."""

from core.max_flow import edmonds_karp
from core.min_cut import min_cut
from core.verify import verify_all


def solve(network, source, sink) -> dict:
    """Resuelve flujo máximo, corte mínimo y comprobaciones para ``source -> sink``.

    Entradas:
        network: diccionario de red (no se modifica).
        source: identificador del nodo origen.
        sink: identificador del nodo destino.
    Salida:
        Diccionario de error ``{"error": codigo}`` si los terminales son inválidos,
        o el diccionario de resultado del contrato con ``source``, ``sink``,
        ``max_flow_value``, ``flows``, ``iterations``, ``cut`` y ``checks``.
    """
    node_ids = {node["id"] for node in network["nodes"]}
    if source not in node_ids or sink not in node_ids:
        return {"error": "E_UNKNOWN_NODE"}
    if source == sink:
        return {"error": "E_ST_EQUAL"}

    value, flows, iterations, res = edmonds_karp(network, source, sink)
    cut = min_cut(network, res, source)
    checks = verify_all(network, flows, set(cut["S"]), source, sink)
    return {
        "source": source,
        "sink": sink,
        "max_flow_value": value,
        "flows": flows,
        "iterations": iterations,
        "cut": cut,
        "checks": checks,
    }
