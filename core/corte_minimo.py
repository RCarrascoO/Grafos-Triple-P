"""Cálculo del corte mínimo por alcanzabilidad en la red residual final."""

from collections import deque

from core.red import arcos_activos


def alcanzables_desde(residual, s) -> set:
    """Obtiene los nodos alcanzables desde ``s`` en la red residual con BFS.

    Entradas:
        residual: red residual ``dict[str, dict[str, int]]``.
        s: identificador del nodo origen.
    Salida:
        Conjunto ``set[str]`` de nodos alcanzables por arcos con ``residual[u][v] > 0``
        (siempre incluye a ``s``).
    """
    visitados = {s}
    cola = deque([s])
    while cola:
        u = cola.popleft()
        for v in residual[u]:
            if residual[u][v] > 0 and v not in visitados:
                visitados.add(v)
                cola.append(v)
    return visitados


def corte_minimo(red, residual, s) -> dict:
    """Construye la partición de corte mínimo ``(S, T)`` desde la residual final.

    Entradas:
        red: diccionario de red (no se modifica).
        residual: red residual final ``dict[str, dict[str, int]]``.
        s: identificador del nodo origen.
    Salida:
        Diccionario con claves ``S``, ``T``, ``arcs`` (listas ordenadas) y
        ``capacity`` (suma de capacidades de los arcos activos de ``S`` a ``T``).
    """
    conjunto_s = alcanzables_desde(residual, s)
    conjunto_t = {nodo["id"] for nodo in red["nodes"]} - conjunto_s
    arcos_corte = [
        arco for arco in arcos_activos(red)
        if arco["from"] in conjunto_s and arco["to"] in conjunto_t
    ]
    return {
        "S": sorted(conjunto_s),
        "T": sorted(conjunto_t),
        "arcs": sorted(arco["id"] for arco in arcos_corte),
        "capacity": sum(arco["capacity"] for arco in arcos_corte),
    }
