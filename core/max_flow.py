"""Motor de flujo máximo mediante el algoritmo de Edmonds-Karp (BFS)."""

from collections import deque

from core.network import active_arcs


def build_residual(network) -> dict:
    """Construye la red residual inicial (x = 0) a partir de los arcos activos.

    Entradas:
        network: diccionario de red con claves ``nodes`` y ``arcs`` (no se modifica).
    Salida:
        ``dict[str, dict[str, int]]`` con ``res[u][v] = c(u, v)`` y ``res[v][u] = 0``
        por cada arco activo, incluyendo como clave a todos los nodos.
    Invariante:
        Para todo arco activo (u, v), ``res[u][v] + res[v][u] == c(u, v)``.
    """
    res = {node["id"]: {} for node in network["nodes"]}
    for arc in active_arcs(network):
        u, v, cap = arc["from"], arc["to"], arc["capacity"]
        res[u][v] = cap
        res[v][u] = 0
    return res


def bfs_augmenting_path(res, s, t) -> list | None:
    """Busca un camino aumentante más corto en número de arcos usando BFS.

    Entradas:
        res: red residual ``dict[str, dict[str, int]]``.
        s: identificador del nodo origen.
        t: identificador del nodo destino.
    Salida:
        Lista ``[s, ..., t]`` con el camino aumentante más corto, o ``None``
        si no existe camino con capacidad residual positiva.
    Invariante:
        Recorre vecinos en orden lexicográfico y solo usa arcos con ``res[u][v] > 0``.
    """
    parent = {s: None}
    queue = deque([s])
    while queue:
        u = queue.popleft()
        for v in sorted(res[u]):
            if res[u][v] > 0 and v not in parent:
                parent[v] = u
                if v == t:
                    path = []
                    node = t
                    while node is not None:
                        path.append(node)
                        node = parent[node]
                    path.reverse()
                    return path
                queue.append(v)
    return None


def bottleneck(res, path) -> int:
    """Calcula el cuello de botella de un camino aumentante en la red residual.

    Entradas:
        res: red residual ``dict[str, dict[str, int]]``.
        path: lista de nodos ``[v_0, ..., v_k]`` con al menos dos nodos.
    Salida:
        Entero mínimo ``res[u][v]`` entre los pares consecutivos de ``path``.
    """
    return min(res[u][v] for u, v in zip(path, path[1:]))


def augment(res, path, delta) -> None:
    """Actualiza la red residual in-place aumentando ``delta`` unidades por ``path``.

    Entradas:
        res: red residual ``dict[str, dict[str, int]]`` a modificar.
        path: lista de nodos del camino aumentante.
        delta: cantidad entera positiva de flujo a enviar.
    Salida:
        None.
    Invariante:
        Preserva ``res[u][v] + res[v][u] == c(u, v)`` en cada arco del camino.
    """
    for u, v in zip(path, path[1:]):
        res[u][v] -= delta
        res[v][u] += delta


def edmonds_karp(network, s, t) -> tuple:
    """Calcula el flujo máximo entre ``s`` y ``t`` con Edmonds-Karp (BFS).

    Entradas:
        network: diccionario de red (no se modifica).
        s: identificador del nodo origen.
        t: identificador del nodo destino.
    Salida:
        Tupla ``(value, flows, iterations, res)`` con el valor del flujo máximo,
        flujo por arco activo, registro de iteraciones y red residual final.
    Invariantes:
        En cada iteración ``delta >= 1``, ``value`` crece estrictamente y la
        longitud de los caminos encontrados nunca disminuye.
    """
    res = build_residual(network)
    value = 0
    iterations = []
    while True:
        path = bfs_augmenting_path(res, s, t)
        if path is None:
            break
        delta = bottleneck(res, path)
        augment(res, path, delta)
        value += delta
        iterations.append({
            "k": len(iterations) + 1,
            "path": path,
            "bottleneck": delta,
            "value_after": value,
        })
    flows = {
        arc["id"]: arc["capacity"] - res[arc["from"]][arc["to"]]
        for arc in active_arcs(network)
    }
    return value, flows, iterations, res
