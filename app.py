"""Interfaz Streamlit para el simulador de red de distribución de paquetes."""

import streamlit as st

from core.ediciones import agregar_arco, eliminar_arco, cambiar_estado, cambiar_capacidad
from core.red import cargar_red

ARCHIVOS_RED = {
    "Red inicial": "data/initial_network.json",
    "Modificación 1": "data/mod1.json",
    "Modificación 2": "data/mod2.json",
    "Caso manual": "data/manual_case.json",
    "Figura 1": "data/figura1.json",
}

MENSAJES_ERROR = {
    "E_LOOP": "No se permiten lazos: el origen y el destino deben ser distintos.",
    "E_DUPLICATE": "Ya existe una ruta entre esos dos nodos en el mismo sentido.",
    "E_RECIPROCAL": "Ya existe la ruta en sentido contrario. Elimínela antes de crear esta.",
    "E_CAPACITY": "La capacidad debe ser un número entero entre 1 y 12.",
    "E_UNKNOWN_NODE": "Uno o ambos nodos no existen en la red.",
    "E_ST_EQUAL": "El origen y el destino de la red deben ser nodos distintos.",
    "E_V_RANGE": "La red inicial debe tener entre 10 y 12 nodos.",
    "E_E_RANGE": "La red inicial debe tener entre 15 y 20 arcos activos.",
    "E_ISOLATED": "Todos los nodos de la red inicial deben tener al menos un arco activo.",
    "E_PATHS": "Deben existir al menos 2 caminos simples distintos de origen a destino.",
    "E_V_RANGE_MANUAL": "El caso manual debe tener entre 4 y 6 nodos.",
}


def red_a_dot(red, resultado=None) -> str:
    """Genera texto DOT de Graphviz; recibe red y resultado opcional, y devuelve un str."""
    lineas = ["digraph { rankdir=LR; node [shape=circle, style=filled, fillcolor=white];"]
    for nodo in red["nodes"]:
        lineas.append(f'  "{nodo["id"]}" [label="{nodo["id"]}\\n{nodo["label"]}"];')
    for arco in red["arcs"]:
        atributos = f'label="{arco["capacity"]}"' + ("" if arco["active"] else ", style=dashed, color=gray")
        lineas.append(f'  "{arco["from"]}" -> "{arco["to"]}" [{atributos}];')
    lineas.append("}")
    return "\n".join(lineas)


def main() -> None:
    """Ejecuta la interfaz Streamlit en orden: estado, barra lateral y zona principal."""
    # 1. Estado (N10)
    st.set_page_config(page_title="Simulador de Red de Distribución", layout="wide")
    if "red" not in st.session_state:
        st.session_state.red = cargar_red(ARCHIVOS_RED["Red inicial"])
        st.session_state.resultado = None

    red = st.session_state.red

    # 2. Barra lateral: controles y ediciones (N17, N15, N16)
    with st.sidebar:
        st.header("Configuración")
        nombre_elegido = st.selectbox("Red", list(ARCHIVOS_RED))
        if st.button("Cargar"):
            try:
                st.session_state.red = cargar_red(ARCHIVOS_RED[nombre_elegido])
                st.session_state.resultado = None
                st.rerun()
            except FileNotFoundError:
                st.warning(f"El archivo {ARCHIVOS_RED[nombre_elegido]} todavía no existe.")

        st.divider()
        st.header("Editar ruta existente")
        arcos_por_id = {arco["id"]: arco for arco in red["arcs"]}
        if arcos_por_id:
            id_arco = st.selectbox("Ruta", list(arcos_por_id))
            arco = arcos_por_id[id_arco]
            texto_estado = "activa" if arco["active"] else "desactivada"
            st.caption(f"Capacidad actual: {arco['capacity']} | Estado: {texto_estado}")

            origen_cap = (red["name"], id_arco, arco["capacity"])
            if st.session_state.get("edit_cap_source") != origen_cap:
                st.session_state.edit_cap_source = origen_cap
                st.session_state.edit_cap = arco["capacity"]

            nueva_cap = st.number_input("Capacidad", min_value=1, max_value=12, step=1, key="edit_cap")
            if st.button("Cambiar capacidad"):
                error = cambiar_capacidad(red, id_arco, int(nueva_cap))
                if error:
                    st.warning(MENSAJES_ERROR[error])
                else:
                    st.session_state.resultado = None
                    st.rerun()

            etiqueta_alternar = "Desactivar" if arco["active"] else "Reactivar"
            if st.button(etiqueta_alternar):
                cambiar_estado(red, id_arco, not arco["active"])
                st.session_state.resultado = None
                st.rerun()

            if st.button("Eliminar"):
                eliminar_arco(red, id_arco)
                st.session_state.resultado = None
                st.rerun()
        else:
            st.info("No hay rutas en la red.")

        st.divider()
        st.header("Agregar ruta")
        ids_nodos = [nodo["id"] for nodo in red["nodes"]]
        desde = st.selectbox("Desde", ids_nodos, key="add_from")
        hasta = st.selectbox("Hasta", ids_nodos, key="add_to")
        cap_nueva = st.number_input("Capacidad", min_value=1, max_value=12, step=1, key="cap_nueva")
        if st.button("Agregar"):
            error = agregar_arco(red, desde, hasta, int(cap_nueva))
            if error:
                st.warning(MENSAJES_ERROR[error])
            else:
                st.session_state.resultado = None
                st.rerun()

    # 3. Zona principal: dibujo (N11)
    st.title("Simulador de Red de Distribución de Paquetes")
    st.subheader(red["name"])
    st.graphviz_chart(red_a_dot(red, st.session_state.resultado))


if __name__ == "__main__":
    main()
