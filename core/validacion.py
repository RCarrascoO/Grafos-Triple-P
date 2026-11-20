"""Validaciones de invariantes y perfiles para redes dirigidas."""

from core.red import arcos_activos


def capacidad_valida(valor):
    """Valida una capacidad; recibe cualquier valor y devuelve un booleano."""
    return type(valor) is int and 1 <= valor <= 12


def validar_arco_nuevo(red, u, v, capacidad):
    """Valida un arco nuevo; recibe la red, u, v y la capacidad, y devuelve un código o None."""
    ids_nodos = {nodo["id"] for nodo in red["nodes"]}
    if u not in ids_nodos or v not in ids_nodos:
        return "E_UNKNOWN_NODE"
    if u == v:
        return "E_LOOP"

    pares = {(arco["from"], arco["to"]) for arco in red["arcs"]}
    if (u, v) in pares:
        return "E_DUPLICATE"
    if (v, u) in pares:
        return "E_RECIPROCAL"
    if not capacidad_valida(capacidad):
        return "E_CAPACITY"
    return None


def contar_caminos(red, s, t, limite=2):
    """Cuenta caminos activos; recibe la red, s, t y un límite, y devuelve un entero acotado."""
    if limite <= 0 or s == t:
        return 0
    vecinos = {}
    for arco in arcos_activos(red):
        vecinos.setdefault(arco["from"], []).append(arco["to"])

    def buscar(nodo, visitados):
        """Cuenta recursivamente los caminos desde nodo sin repetir vértices."""
        if nodo == t:
            return 1
        total = 0
        for vecino in vecinos.get(nodo, []):
            if vecino not in visitados:
                total += buscar(vecino, visitados | {vecino})
                if total >= limite:
                    return limite
        return total

    return buscar(s, {s})


def validar_red(red):
    """Valida una red; recibe la red y devuelve la lista de códigos de error encontrados."""
    errores = []
    def agregar_error(codigo):
        """Añade el código una sola vez a la lista de errores."""
        if codigo not in errores:
            errores.append(codigo)

    ids_nodos = [nodo["id"] for nodo in red["nodes"]]
    conjunto_nodos = set(ids_nodos)
    arcos = red["arcs"]
    pares = [(arco["from"], arco["to"]) for arco in arcos]

    if any(u == v for u, v in pares):
        agregar_error("E_LOOP")
    if len(pares) != len(set(pares)):
        agregar_error("E_DUPLICATE")
    conjunto_pares = set(pares)
    if any((v, u) in conjunto_pares for u, v in conjunto_pares if u != v):
        agregar_error("E_RECIPROCAL")
    if any(not capacidad_valida(arco["capacity"]) for arco in arcos):
        agregar_error("E_CAPACITY")
    if any(arco["from"] not in conjunto_nodos or arco["to"] not in conjunto_nodos for arco in arcos):
        agregar_error("E_UNKNOWN_NODE")

    origen = red["source"]
    destino = red["sink"]
    if origen not in conjunto_nodos or destino not in conjunto_nodos:
        agregar_error("E_UNKNOWN_NODE")
    if origen == destino:
        agregar_error("E_ST_EQUAL")

    perfil = red["profile"]
    activos = arcos_activos(red)
    if perfil == "initial":
        if not 10 <= len(ids_nodos) <= 12:
            agregar_error("E_V_RANGE")
        if not 15 <= len(activos) <= 20:
            agregar_error("E_E_RANGE")
        incidentes = {id_nodo for arco in activos for id_nodo in (arco["from"], arco["to"])}
        if not conjunto_nodos <= incidentes:
            agregar_error("E_ISOLATED")
        if contar_caminos(red, origen, destino) < 2:
            agregar_error("E_PATHS")
    elif perfil == "manual" and not 4 <= len(ids_nodos) <= 6:
        agregar_error("E_V_RANGE_MANUAL")
    return errores
