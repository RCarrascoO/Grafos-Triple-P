"""Motor de flujo máximo mediante el algoritmo de Edmonds-Karp (BFS)."""

from collections import deque

from core.red import arcos_activos


def construir_residual(red) -> dict:
    """Construye la red residual inicial (x = 0) a partir de los arcos activos.

    Entradas:
        red: diccionario de red con claves ``nodes`` y ``arcs`` (no se modifica).
    Salida:
        ``dict[str, dict[str, int]]`` con ``residual[u][v] = c(u, v)`` y
        ``residual[v][u] = 0`` por cada arco activo, incluyendo como clave a todos los nodos.
    Invariante:
        Para todo arco activo (u, v), ``residual[u][v] + residual[v][u] == c(u, v)``.
    """
    residual = {nodo["id"]: {} for nodo in red["nodes"]}
    for arco in arcos_activos(red):
        u, v, cap = arco["from"], arco["to"], arco["capacity"]
        residual[u][v] = cap
        residual[v][u] = 0
    return residual


def buscar_camino(residual, s, t) -> list | None:
    """Busca un camino aumentante más corto en número de arcos usando BFS.

    Entradas:
        residual: red residual ``dict[str, dict[str, int]]``.
        s: identificador del nodo origen.
        t: identificador del nodo destino.
    Salida:
        Lista ``[s, ..., t]`` con el camino aumentante más corto, o ``None``
        si no existe camino con capacidad residual positiva.
    Invariante:
        Recorre vecinos en orden lexicográfico y solo usa arcos con ``residual[u][v] > 0``.
    """
    padre = {s: None}
    cola = deque([s])
    while cola:
        u = cola.popleft()
        for v in sorted(residual[u]):
            if residual[u][v] > 0 and v not in padre:
                padre[v] = u
                if v == t:
                    camino = []
                    nodo = t
                    while nodo is not None:
                        camino.append(nodo)
                        nodo = padre[nodo]
                    camino.reverse()
                    return camino
                cola.append(v)
    return None


def cuello_botella(residual, camino) -> int:
    """Calcula el cuello de botella de un camino aumentante en la red residual.

    Entradas:
        residual: red residual ``dict[str, dict[str, int]]``.
        camino: lista de nodos ``[v_0, ..., v_k]`` con al menos dos nodos.
    Salida:
        Entero mínimo ``residual[u][v]`` entre los pares consecutivos de ``camino``.
    """
    return min(residual[u][v] for u, v in zip(camino, camino[1:]))


def aumentar(residual, camino, delta) -> None:
    """Actualiza la red residual in-place aumentando ``delta`` unidades por ``camino``.

    Entradas:
        residual: red residual ``dict[str, dict[str, int]]`` a modificar.
        camino: lista de nodos del camino aumentante.
        delta: cantidad entera positiva de flujo a enviar.
    Salida:
        None.
    Invariante:
        Preserva ``residual[u][v] + residual[v][u] == c(u, v)`` en cada arco del camino.
    """
    for u, v in zip(camino, camino[1:]):
        residual[u][v] -= delta
        residual[v][u] += delta


def edmonds_karp(red, s, t) -> tuple:
    """Calcula el flujo máximo entre ``s`` y ``t`` con Edmonds-Karp (BFS).

    Entradas:
        red: diccionario de red (no se modifica).
        s: identificador del nodo origen.
        t: identificador del nodo destino.
    Salida:
        Tupla ``(valor, flujos, iteraciones, residual)`` con el valor del flujo máximo,
        flujo por arco activo, registro de iteraciones y red residual final.
    Invariantes:
        En cada iteración ``delta >= 1``, ``valor`` crece estrictamente y la
        longitud de los caminos encontrados nunca disminuye.
    """
    residual = construir_residual(red)
    valor = 0
    iteraciones = []
    while camino := buscar_camino(residual, s, t):
        delta = cuello_botella(residual, camino)
        aumentar(residual, camino, delta)
        valor += delta
        iteraciones.append({
            "k": len(iteraciones) + 1,
            "path": camino,
            "bottleneck": delta,
            "value_after": valor,
        })
    flujos = {
        arco["id"]: arco["capacity"] - residual[arco["from"]][arco["to"]]
        for arco in arcos_activos(red)
    }
    return valor, flujos, iteraciones, residual
