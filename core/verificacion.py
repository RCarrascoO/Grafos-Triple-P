"""Comprobaciones del flujo y del corte, independientes del motor."""

from core.red import arcos_activos


def verificar_capacidad(red, flujos) -> bool:
    """Recibe la red y sus flujos; devuelve si cada flujo activo es entero y cabe."""
    for arco in arcos_activos(red):
        flujo = flujos[arco["id"]]
        if type(flujo) is not int or not 0 <= flujo <= arco["capacity"]:
            return False
    return True


def verificar_conservacion(red, flujos, s, t) -> tuple[bool, list]:
    """Recibe red, flujos y terminales; devuelve conservación y tabla de nodos intermedios."""
    arcos = arcos_activos(red)
    tabla = []
    for nodo in sorted(nodo["id"] for nodo in red["nodes"]):
        if nodo == s or nodo == t:
            continue
        entra = sum(flujos[arco["id"]] for arco in arcos if arco["to"] == nodo)
        sale = sum(flujos[arco["id"]] for arco in arcos if arco["from"] == nodo)
        tabla.append({"node": nodo, "in": entra, "out": sale})
    return all(fila["in"] == fila["out"] for fila in tabla), tabla


def valor_flujo(red, flujos, s) -> int:
    """Recibe red, flujos y origen; devuelve el flujo que sale menos el que entra."""
    arcos = arcos_activos(red)
    sale = sum(flujos[arco["id"]] for arco in arcos if arco["from"] == s)
    entra = sum(flujos[arco["id"]] for arco in arcos if arco["to"] == s)
    return sale - entra


def capacidad_corte(red, S) -> int:
    """Recibe la red y el conjunto S; devuelve la capacidad activa de S hacia fuera."""
    return sum(
        arco["capacity"] for arco in arcos_activos(red)
        if arco["from"] in S and arco["to"] not in S
    )


def verificar_todo(red, flujos, S, s, t) -> dict:
    """Recibe red, flujos, S y terminales; devuelve el bloque checks del contrato."""
    conservacion_ok, tabla = verificar_conservacion(red, flujos, s, t)
    return {
        "capacity_ok": verificar_capacidad(red, flujos),
        "conservation_ok": conservacion_ok,
        "conservation_table": tabla,
        "duality_ok": s in S and t not in S
        and valor_flujo(red, flujos, s) == capacidad_corte(red, S),
    }
