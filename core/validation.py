"""Validaciones de invariantes y perfiles para redes dirigidas."""


def valid_capacity(value):
    """Valida una capacidad; recibe cualquier value y devuelve un booleano."""
    return type(value) is int and 1 <= value <= 12


def check_new_arc(network, u, v, capacity):
    """Valida un arco nuevo; recibe network, u, v y capacity, y devuelve un código o None."""
    node_ids = {node["id"] for node in network["nodes"]}
    if u not in node_ids or v not in node_ids:
        return "E_UNKNOWN_NODE"
    if u == v:
        return "E_LOOP"

    for arc in network["arcs"]:
        if arc["from"] == u and arc["to"] == v:
            return "E_DUPLICATE"
    for arc in network["arcs"]:
        if arc["from"] == v and arc["to"] == u:
            return "E_RECIPROCAL"
    if not valid_capacity(capacity):
        return "E_CAPACITY"
    return None


def count_paths(network, s, t, limit=2):
    """Cuenta caminos activos; recibe network, s, t y limit, y devuelve un entero acotado."""
    if limit <= 0 or s == t:
        return 0
    node_ids = {node["id"] for node in network["nodes"]}
    if s not in node_ids or t not in node_ids:
        return 0
    neighbors = {}
    for arc in network["arcs"]:
        if arc.get("active") is True:
            neighbors.setdefault(arc["from"], []).append(arc["to"])
    for values in neighbors.values():
        values.sort()

    def dfs(node, visited):
        """Cuenta recursivamente los caminos desde node sin repetir vértices."""
        if node == t:
            return 1
        total = 0
        for neighbor in neighbors.get(node, []):
            if neighbor not in visited:
                total += dfs(neighbor, visited | {neighbor})
                if total >= limit:
                    return limit
        return total

    return dfs(s, {s})


def validate_network(network):
    """Valida una red; recibe network y devuelve la lista de códigos de error encontrados."""
    errors = []
    def add_error(code):
        """Añade code una sola vez a la lista de errores."""
        if code not in errors:
            errors.append(code)

    node_ids = [node["id"] for node in network["nodes"]]
    node_set = set(node_ids)
    arcs = network["arcs"]
    pairs = [(arc["from"], arc["to"]) for arc in arcs]

    if any(u == v for u, v in pairs):
        add_error("E_LOOP")
    if len(pairs) != len(set(pairs)):
        add_error("E_DUPLICATE")
    pair_set = set(pairs)
    if any((v, u) in pair_set for u, v in pair_set if u != v):
        add_error("E_RECIPROCAL")
    if any(not valid_capacity(arc["capacity"]) for arc in arcs):
        add_error("E_CAPACITY")
    if any(arc["from"] not in node_set or arc["to"] not in node_set for arc in arcs):
        add_error("E_UNKNOWN_NODE")

    source = network["source"]
    sink = network["sink"]
    if source not in node_set or sink not in node_set:
        add_error("E_UNKNOWN_NODE")
    if source == sink:
        add_error("E_ST_EQUAL")

    profile = network["profile"]
    active_arcs = [arc for arc in arcs if arc.get("active") is True]
    if profile == "initial":
        if not 10 <= len(node_ids) <= 12:
            add_error("E_V_RANGE")
        if not 15 <= len(active_arcs) <= 20:
            add_error("E_E_RANGE")
        incident = {node_id: False for node_id in node_set}
        for arc in active_arcs:
            if arc["from"] in incident:
                incident[arc["from"]] = True
            if arc["to"] in incident:
                incident[arc["to"]] = True
        if not all(incident.values()):
            add_error("E_ISOLATED")
        if count_paths(network, source, sink) < 2:
            add_error("E_PATHS")
    elif profile == "manual" and not 4 <= len(node_ids) <= 6:
        add_error("E_V_RANGE_MANUAL")
    return errors
