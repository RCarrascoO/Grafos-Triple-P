"""Carga de la red desde JSON. La red en memoria es el diccionario del JSON."""

import json


def cargar_red(ruta) -> dict:
    """Carga una red; recibe la ruta de un archivo JSON y devuelve su diccionario."""
    with open(ruta, encoding="utf-8") as archivo:
        return json.load(archivo)


def arcos_activos(red) -> list[dict]:
    """Filtra los arcos activos; recibe la red y devuelve la lista de arcos con active == True."""
    return [arco for arco in red["arcs"] if arco["active"] is True]
