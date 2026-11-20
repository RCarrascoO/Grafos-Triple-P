"""Punto de entrada único del motor: flujo máximo, corte mínimo y verificación."""

from core.flujo_maximo import edmonds_karp
from core.corte_minimo import corte_minimo
from core.verificacion import verificar_todo


def resolver(red, origen, destino) -> dict:
    """Resuelve flujo máximo, corte mínimo y comprobaciones para ``origen -> destino``.

    Entradas:
        red: diccionario de red (no se modifica).
        origen: identificador del nodo origen.
        destino: identificador del nodo destino.
    Salida:
        Diccionario de error ``{"error": codigo}`` si los terminales son inválidos,
        o el diccionario de resultado del contrato con ``source``, ``sink``,
        ``max_flow_value``, ``flows``, ``iterations``, ``cut`` y ``checks``.
    """
    ids_nodos = {nodo["id"] for nodo in red["nodes"]}
    if origen not in ids_nodos or destino not in ids_nodos:
        return {"error": "E_UNKNOWN_NODE"}
    if origen == destino:
        return {"error": "E_ST_EQUAL"}

    valor, flujos, iteraciones, residual = edmonds_karp(red, origen, destino)
    corte = corte_minimo(red, residual, origen)
    comprobaciones = verificar_todo(red, flujos, set(corte["S"]), origen, destino)
    return {
        "source": origen,
        "sink": destino,
        "max_flow_value": valor,
        "flows": flujos,
        "iterations": iteraciones,
        "cut": corte,
        "checks": comprobaciones,
    }
