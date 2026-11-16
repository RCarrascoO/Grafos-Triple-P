"""Ediciones básicas de una red dirigida."""

from .validation import check_new_arc, valid_capacity


def add_arc(network, u, v, capacity) -> str | None:
    """Agrega un arco válido; recibe network, sus extremos y capacidad, y devuelve un código o None."""
    error = check_new_arc(network, u, v, capacity)
    if error is not None:
        return error
    network["arcs"].append(
        {"id": f"{u}-{v}", "from": u, "to": v, "capacity": capacity, "active": True}
    )
    return None


def set_capacity(network, arc_id, capacity) -> str | None:
    """Cambia la capacidad de un arco; recibe network, su id y capacidad, y devuelve un código o None."""
    if not valid_capacity(capacity):
        return "E_CAPACITY"
    for arc in network["arcs"]:
        if arc["id"] == arc_id:
            arc["capacity"] = capacity
            break
    return None


def set_active(network, arc_id, active) -> None:
    """Cambia el estado activo; recibe network, el id del arco y un valor, y no devuelve nada."""
    for arc in network["arcs"]:
        if arc["id"] == arc_id:
            arc["active"] = bool(active)
            break


def remove_arc(network, arc_id) -> None:
    """Elimina un arco; recibe network y su id, y no devuelve nada."""
    network["arcs"][:] = [arc for arc in network["arcs"] if arc["id"] != arc_id]
