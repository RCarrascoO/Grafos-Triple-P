"""Carga de la red desde JSON. La red en memoria es el diccionario del JSON."""

import json


def load_network(path) -> dict:
    """Carga una red; recibe la ruta de un archivo JSON y devuelve su diccionario."""
    with open(path, encoding="utf-8") as file:
        return json.load(file)


def active_arcs(network) -> list[dict]:
    """Filtra los arcos activos; recibe network y devuelve la lista de arcos con active == True."""
    return [arc for arc in network["arcs"] if arc["active"] is True]
