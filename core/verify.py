"""Comprobaciones del flujo y del corte, independientes del motor."""

from core.network import active_arcs


def check_capacity(network, flows) -> bool:
    """Recibe la red y sus flujos; devuelve si cada flujo activo es entero y cabe."""
    for arc in active_arcs(network):
        flow = flows[arc["id"]]
        if type(flow) is not int or not 0 <= flow <= arc["capacity"]:
            return False
    return True


def check_conservation(network, flows, s, t) -> tuple[bool, list]:
    """Recibe red, flujos y terminales; devuelve conservación y tabla de nodos intermedios."""
    arcs = active_arcs(network)
    table = []
    for node in sorted(node["id"] for node in network["nodes"]):
        if node == s or node == t:
            continue
        incoming = sum(flows[arc["id"]] for arc in arcs if arc["to"] == node)
        outgoing = sum(flows[arc["id"]] for arc in arcs if arc["from"] == node)
        table.append({"node": node, "in": incoming, "out": outgoing})
    return all(row["in"] == row["out"] for row in table), table


def flow_value(network, flows, s) -> int:
    """Recibe red, flujos y origen; devuelve el flujo que sale menos el que entra."""
    arcs = active_arcs(network)
    outgoing = sum(flows[arc["id"]] for arc in arcs if arc["from"] == s)
    incoming = sum(flows[arc["id"]] for arc in arcs if arc["to"] == s)
    return outgoing - incoming


def cut_capacity(network, S) -> int:
    """Recibe la red y el conjunto S; devuelve la capacidad activa de S hacia fuera."""
    return sum(
        arc["capacity"] for arc in active_arcs(network)
        if arc["from"] in S and arc["to"] not in S
    )


def verify_all(network, flows, S, s, t) -> dict:
    """Recibe red, flujos, S y terminales; devuelve el bloque checks del contrato."""
    conservation_ok, table = check_conservation(network, flows, s, t)
    return {
        "capacity_ok": check_capacity(network, flows),
        "conservation_ok": conservation_ok,
        "conservation_table": table,
        "duality_ok": s in S and t not in S
        and flow_value(network, flows, s) == cut_capacity(network, S),
    }
