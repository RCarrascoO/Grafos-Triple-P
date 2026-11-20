"""Ediciones básicas de una red dirigida."""

from .validacion import capacidad_valida, validar_arco_nuevo


def agregar_arco(red, u, v, capacidad) -> str | None:
    """Agrega un arco válido; recibe la red, sus extremos y capacidad, y devuelve un código o None."""
    error = validar_arco_nuevo(red, u, v, capacidad)
    if error is not None:
        return error
    red["arcs"].append(
        {"id": f"{u}-{v}", "from": u, "to": v, "capacity": capacidad, "active": True}
    )
    return None


def cambiar_capacidad(red, id_arco, capacidad) -> str | None:
    """Cambia la capacidad de un arco; recibe la red, su id y capacidad, y devuelve un código o None."""
    if not capacidad_valida(capacidad):
        return "E_CAPACITY"
    for arco in red["arcs"]:
        if arco["id"] == id_arco:
            arco["capacity"] = capacidad
            break
    return None


def cambiar_estado(red, id_arco, activo) -> None:
    """Cambia el estado activo; recibe la red, el id del arco y un valor, y no devuelve nada."""
    for arco in red["arcs"]:
        if arco["id"] == id_arco:
            arco["active"] = bool(activo)
            break


def eliminar_arco(red, id_arco) -> None:
    """Elimina un arco; recibe la red y su id, y no devuelve nada."""
    red["arcs"][:] = [arco for arco in red["arcs"] if arco["id"] != id_arco]
