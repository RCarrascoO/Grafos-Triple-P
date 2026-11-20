"""Cálculo del corte mínimo por alcanzabilidad en la red residual final."""

from collections import deque

from core.network import active_arcs


def reachable_from(res, s) -> set:
    """Obtiene los nodos alcanzables desde ``s`` en la red residual con BFS.

    Entradas:
        res: red residual ``dict[str, dict[str, int]]``.
        s: identificador del nodo origen.
    Salida:
        Conjunto ``set[str]`` de nodos alcanzables por arcos con ``res[u][v] > 0``
        (siempre incluye a ``s``).
    """
    visited = {s}
    queue = deque([s])
    while queue:
        u = queue.popleft()
        for v in sorted(res[u]):
            if res[u][v] > 0 and v not in visited:
                visited.add(v)
                queue.append(v)
    return visited


def min_cut(network, res, s) -> dict:
    """Construye la partición de corte mínimo ``(S, T)`` desde la residual final.

    Entradas:
        network: diccionario de red (no se modifica).
        res: red residual final ``dict[str, dict[str, int]]``.
        s: identificador del nodo origen.
    Salida:
        Diccionario con claves ``S``, ``T``, ``arcs`` (listas ordenadas) y
        ``capacity`` (suma de capacidades de los arcos activos de ``S`` a ``T``).
    """
    s_set = reachable_from(res, s)
    t_set = {node["id"] for node in network["nodes"]} - s_set
    cut_arcs = [
        arc for arc in active_arcs(network)
        if arc["from"] in s_set and arc["to"] in t_set
    ]
    return {
        "S": sorted(s_set),
        "T": sorted(t_set),
        "arcs": sorted(arc["id"] for arc in cut_arcs),
        "capacity": sum(arc["capacity"] for arc in cut_arcs),
    }
