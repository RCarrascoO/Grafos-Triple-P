"""Interfaz Streamlit para el simulador de red de distribución de paquetes."""

import streamlit as st

from core.edits import add_arc, remove_arc, set_active, set_capacity
from core.network import load_network

NETWORK_FILES = {
    "Red inicial": "data/initial_network.json",
    "Modificación 1": "data/mod1.json",
    "Modificación 2": "data/mod2.json",
    "Caso manual": "data/manual_case.json",
    "Figura 1": "data/figura1.json",
}

ERROR_MESSAGES = {
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


def network_dot(network, result=None) -> str:
    """Genera texto DOT de Graphviz; recibe network y result opcional, y devuelve un str."""
    lines = ["digraph { rankdir=LR; node [shape=circle, style=filled, fillcolor=white];"]
    for node in network["nodes"]:
        lines.append(f'  "{node["id"]}" [label="{node["id"]}\\n{node["label"]}"];')
    for arc in network["arcs"]:
        label = str(arc["capacity"])
        if not arc["active"]:
            attrs = f'label="{label}", style=dashed, color=gray'
        else:
            attrs = f'label="{label}"'
        lines.append(f'  "{arc["from"]}" -> "{arc["to"]}" [{attrs}];')
    lines.append("}")
    return "\n".join(lines)


def main() -> None:
    """Ejecuta la interfaz Streamlit en orden: estado, barra lateral y zona principal."""
    # 1. Estado (N10)
    st.set_page_config(page_title="Simulador de Red de Distribución", layout="wide")
    if "network" not in st.session_state:
        st.session_state.network = load_network(NETWORK_FILES["Red inicial"])
        st.session_state.result = None

    network = st.session_state.network

    # 2. Barra lateral: controles y ediciones (N17, N15, N16)
    with st.sidebar:
        st.header("Configuración")
        selected_name = st.selectbox("Red", list(NETWORK_FILES))
        if st.button("Cargar"):
            try:
                st.session_state.network = load_network(NETWORK_FILES[selected_name])
                st.session_state.result = None
                st.rerun()
            except FileNotFoundError:
                st.warning(f"El archivo {NETWORK_FILES[selected_name]} todavía no existe.")

        st.divider()
        st.header("Editar ruta existente")
        arcs_by_id = {arc["id"]: arc for arc in network["arcs"]}
        if arcs_by_id:
            arc_id = st.selectbox("Ruta", list(arcs_by_id))
            arc = arcs_by_id[arc_id]
            state_text = "activa" if arc["active"] else "desactivada"
            st.caption(f"Capacidad actual: {arc['capacity']} | Estado: {state_text}")

            cap_source = (network["name"], arc_id, arc["capacity"])
            if st.session_state.get("edit_cap_source") != cap_source:
                st.session_state.edit_cap_source = cap_source
                st.session_state.edit_cap = arc["capacity"]

            new_cap = st.number_input("Capacidad", min_value=1, max_value=12, step=1, key="edit_cap")
            if st.button("Cambiar capacidad"):
                error = set_capacity(network, arc_id, int(new_cap))
                if error:
                    st.warning(ERROR_MESSAGES[error])
                else:
                    st.session_state.result = None
                    st.rerun()

            toggle_label = "Desactivar" if arc["active"] else "Reactivar"
            if st.button(toggle_label):
                set_active(network, arc_id, not arc["active"])
                st.session_state.result = None
                st.rerun()

            if st.button("Eliminar"):
                remove_arc(network, arc_id)
                st.session_state.result = None
                st.rerun()
        else:
            st.info("No hay rutas en la red.")

        st.divider()
        st.header("Agregar ruta")
        node_ids = [node["id"] for node in network["nodes"]]
        origin = st.selectbox("Desde", node_ids, key="add_from")
        target = st.selectbox("Hasta", node_ids, key="add_to")
        add_cap = st.number_input("Capacidad", min_value=1, max_value=12, step=1, key="add_cap")
        if st.button("Agregar"):
            error = add_arc(network, origin, target, int(add_cap))
            if error:
                st.warning(ERROR_MESSAGES[error])
            else:
                st.session_state.result = None
                st.rerun()

    # 3. Zona principal: dibujo (N11)
    st.title("Simulador de Red de Distribución de Paquetes")
    st.subheader(network["name"])
    st.graphviz_chart(network_dot(network, st.session_state.result))


if __name__ == "__main__":
    main()
