import json
import streamlit as st 
import pandas as pd
import io
from streamlit.components.v1 import html  
from reglas import reglas_ruteo, MAPA_ORIGENES, PREGUNTAS_FRECUENTES

st.set_page_config(page_title="Monitor Logístico - Liliana García", layout="wide", initial_sidebar_state="expanded")



# ==========================================
# ESTADO Y CONTROL DEL MODO FLOTANTE
# ==========================================
if "flotar_activo" not in st.session_state:
    st.session_state.flotar_activo = False

def toggle_flotar():
    st.session_state.flotar_activo = not st.session_state.flotar_activo

if st.session_state.flotar_activo:
    st.markdown("""
        <style>
            div[data-testid="stHorizontalBlock"]:has(> div:has(h3)), 
            div.element-container:has(div.stMetric),
            div.element-container:has(text),
            div[data-testid="stHorizontalBlock"] button:not(:has(p:contains("FLOTAR"))),
            .row-widget.stButton:not(:has(button:contains("FLOTAR"))) {
                display: none !important;
            }

            table, div[data-testid="stTable"], .js-plotly-plot {
                max-height: 380px !important;
                overflow-y: auto !important;
                display: block !important;
            }
        </style>
    """, unsafe_allow_html=True)



# ==========================================
# CSS GENERAL + ESTILO DE VENTANA FLOTANTE
# ========================================== 
st.markdown("""
    <style>
    .block-container {padding: 0rem !important;}
    footer, #MainMenu, header {visibility: hidden;}
    body { background-color: #25282b; }
    .poligono-bloque {
        letter-spacing: -0.2px; 
        white-space: nowrap;    
        zoom: 0.95; 
    }
    #contenedor-padre { display: flex; flex-direction: column; }
    .delta { display: none !important; }
    #visor { padding-right: 210px !important; box-sizing: border-box; }
    .tabla-flota-reducida {
        max-width: 80% !important;
        margin-left: 0 !important;
        margin-right: auto;
    }
    table {
        table-layout: fixed;
        width: 100%;
        word-wrap: break-word;
    }
    @media (max-width: 1200px) {
        .calc-row td, .calc-row select, .calc-row span {
            font-size: 12px !important;
        }
    }
    @media screen and (-webkit-min-device-pixel-ratio:0) {
        .poligono-bloque {
            zoom: 0.95; 
        }
    }
    /* --- VENTANA FLOTANTE AJUSTADA Y ORDENADA --- */
    div[data-testid="stExpander"] {
        position: fixed !important;
        bottom: 15px !important;
        right: 15px !important;
        width: 550px !important;
        max-height: 100vh !important; /* Limitado al alto de la pantalla */
        z-index: 999999 !important;
        background-color: #fcf1b6 !important;
        border-radius: 12px !important;
        border: 4px solid #FFD700 !important;
        box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.7) !important;
        overflow: hidden !important;
    }
    
    /* 🔥 TÍTULO DEL BOT ("🤖 BOT prioridades") EN NEGRO OSCURO BIEN VISIBLE */
    div[data-testid="stExpander"] summary,
    div[data-testid="stExpander"] summary p, 
    div[data-testid="stExpander"] summary span,
    div[data-testid="stExpander"] summary div,
    div[data-testid="stExpander"] summary svg {
        color: #1e1d1f !important;
        fill: #19191a !important;
        font-weight: 800 !important;
        font-size: 1.1rem !important;
    }

    /* 🔥 TEXTO INDICATIVO INTERNO ("👉 Escribe el SVC a consultar.🔍") EN NEGRO */
    div[data-testid="stExpander"] div[data-testid="stMarkdownContainer"] p {
        color: #19191a !important;
        font-weight: bold !important;
    }

    /* --- MENSAJE DEL USUARIO (Lila eléctrico con texto blanco) --- */
    div[data-testid="stChatMessage"]:has(div[aria-label="user"]),
    div[data-testid="stChatMessage"]:has([data-testid*="User"]) {
        background-color: #FFD700 !important;
        border-radius: 10px !important;
        padding: 8px !important;
        margin: 6px 0 !important;
        box-shadow: 0px 2px 5px rgba(0,0,0,0.2) !important;
    }

    div[data-testid="stChatMessage"]:has(div[aria-label="user"]) *,
    div[data-testid="stChatMessage"]:has([data-testid*="User"]) * {
        color: #FFFFFF !important;
    }

    /* --- MENSAJE DEL BOT / ASISTENTE (Fondo Blanco Puro y Esquema Claro) --- */
    div[data-testid="stChatMessage"]:has(div[aria-label="assistant"]),
    div[data-testid="stChatMessage"]:has([data-testid*="Assistant"]) {
        color-scheme: light !important; /* 🔥 Bloquea la inversión del modo oscuro del navegador */
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 2px solid #FFD700 !important;
        border-radius: 10px !important;
        padding: 8px !important;
        margin: 6px 0 !important;
    }

    /* 🔥 FORZAR A TODOS LOS ELEMENTOS HIJOS (párrafos, listas, viñetas, negritas, spans) */
    div[data-testid="stChatMessage"]:has(div[aria-label="assistant"]) *,
    div[data-testid="stChatMessage"]:has([data-testid*="Assistant"]) * {
        color-scheme: light !important;
        color: #000000 !important;
        font-weight: 600 !important;
    }

    /* Altura fija del bloque de mensajes */
    div[data-testid="stExpander"] div[data-testid="stVerticalBlock"] {
        max-height: 760px !important;
        overflow-y: auto !important;
        display: flex !important;
        flex-direction: column !important;
    }

    /* Cuando el panel está flotando, oculta los botones y la barra de pestañas */
    .fleet-floating .vista-excel-btn,
    .fleet-floating .autocalcular-btn,
    .fleet-floating .activas-btn,
    .fleet-floating .todas-btn,
    .fleet-floating .pestanas-container {
        display: none !important;
    }

    
    </style>
""", unsafe_allow_html=True)




# ==========================================
# 🤖 ASISTENTE DE PRIORIDADES Y RESUMEN
# ==========================================
with st.expander("🤖 ¿INDICACIONES DE RUTEOS? Te ayudo", expanded=False):

    # 🎨 FORZAR COLORES CLAROS Y LEGIBLES EN COMPONENTES NATIVOS
    st.markdown("""
    <style>
        div[data-testid="stExpander"] button {
            background-color: #f1f5f9 !important;
            color: #0f172a !important;
            border: 1px solid #cbd5e1 !important;
            font-weight: 600 !important;
        }
        div[data-testid="stExpander"] button:hover {
            background-color: #e2e8f0 !important;
            color: #0284c7 !important;
            border-color: #0284c7 !important;
        }
        div[data-testid="stExpander"] label p {
            color: #0f172a !important;
            font-weight: 600 !important;
        }
    </style>
    """, unsafe_allow_html=True)

    st.write("👉 Consulta un SVC para indicaciones 🔍")

    # Inicialización de Estados
    if "main_chat_messages" not in st.session_state:
        st.session_state.main_chat_messages = []
    if "esperando_subtipo_smx5" not in st.session_state:
        st.session_state.esperando_subtipo_smx5 = False
    if "flujo_resumen" not in st.session_state:
        st.session_state.flujo_resumen = False
    if "paso_resumen" not in st.session_state:
        st.session_state.paso_resumen = 0
    if "paso_historial" not in st.session_state:
        st.session_state.paso_historial = []
    if "data_resumen" not in st.session_state:
        st.session_state.data_resumen = {}

    with st.container(height=480):
        # 1. MOSTRAR HISTORIAL DE MENSAJES
        for idx, msg in enumerate(st.session_state.main_chat_messages):
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"], unsafe_allow_html=True)
                
                # CUESTIONARIO INTERACTIVO DENTRO DEL ÚLTIMO GLOBO DEL BOT
                if st.session_state.flujo_resumen and idx == len(st.session_state.main_chat_messages) - 1:
                    paso = st.session_state.paso_resumen

                    # PASO 1: Ciclo
                    if paso == 1:
                        st.write("👇 **¿Qué tipo de ciclo fue?:**")
                        col1, col2 = st.columns(2)
                        if col1.button("1️⃣ Uniciclo", key="btn_resumen_uniciclo", use_container_width=True):
                            st.session_state.data_resumen["ciclo"] = "Uniciclo"
                            st.session_state.paso_historial.append(1)
                            st.session_state.paso_resumen = 2
                            st.rerun()
                        if col2.button("2️⃣ Ciclo 1", key="btn_resumen_c1", use_container_width=True):
                            st.session_state.data_resumen["ciclo"] = "C1"
                            st.session_state.paso_historial.append(1)
                            st.session_state.paso_resumen = 2
                            st.rerun()

                    # PASO 2: Unidades Dedicadas para Nodos
                    elif paso == 2:
                        st.write("👇 **Unidades dedicadas para nodos (selecciona la casilla):**")
                        
                        u1 = st.checkbox("3.5 tons", key="chk_35")
                        u2 = st.checkbox("Delivery Cell", key="chk_del")
                        
                        unidades_elegidas = []
                        if u1:
                            unidades_elegidas.append("3.5 tons")
                        if u2:
                            unidades_elegidas.append("Delivery Cell")
                        
                        st.write("¿Logis tomó todas?")
                        col_s, col_n = st.columns(2)
                        if col_s.button("1️⃣ Sí", use_container_width=True):
                            st.session_state.data_resumen["unidades_centro"] = unidades_elegidas
                            st.session_state.data_resumen["logis_tomo_todas"] = True
                            st.session_state.paso_historial.append(2)
                            st.session_state.paso_resumen = 2.5
                            st.rerun()
                        if col_n.button("2️⃣ No", use_container_width=True):
                            st.session_state.data_resumen["unidades_centro"] = unidades_elegidas
                            st.session_state.data_resumen["logis_tomo_todas"] = False
                            st.session_state.paso_historial.append(2)
                            st.session_state.paso_resumen = 2.2
                            st.rerun()

                    # PASO 2.2: Preguntar cuáles dejó fuera Logis
                    elif paso == 2.2:
                        st.write("👇 **¿Cuál o cuáles unidades dejó fuera Logis?**")
                        unis_pre = st.session_state.data_resumen.get("unidades_centro", [])
                        
                        fuera_elegidas = []
                        for i_idx, u in enumerate(unis_pre):
                            if st.checkbox(f"Dejó fuera: {u}", key=f"chk_fuera_{i_idx}"):
                                fuera_elegidas.append(u)
                        
                        if st.button("Continuar ➡️", use_container_width=True):
                            st.session_state.data_resumen["unidades_fuera"] = fuera_elegidas
                            st.session_state.paso_historial.append(2.2)
                            st.session_state.paso_resumen = 2.5
                            st.rerun()

                    # PASO 2.5: Bulk (H&B)
                    elif paso == 2.5:
                        st.write("👇 **¿Hubo Bulk (H&B)?**")
                        c1, c2 = st.columns(2)
                        if c1.button("1️⃣ Sí", use_container_width=True):
                            st.session_state.data_resumen["hubo_bulk"] = True
                            st.session_state.paso_historial.append(2.5)
                            st.session_state.paso_resumen = 3
                            st.rerun()
                        if c2.button("2️⃣ No", use_container_width=True):
                            st.session_state.data_resumen["hubo_bulk"] = False
                            st.session_state.paso_historial.append(2.5)
                            st.session_state.paso_resumen = 3
                            st.rerun()

                    # PASO 3: Dropeo de Nodos
                    elif paso == 3:
                        st.write("👇 **¿Hubo dropeo de nodos?**")
                        c1, c2 = st.columns(2)
                        if c1.button("1️⃣ Sí", use_container_width=True):
                            st.session_state.data_resumen["dropeo_nodos"] = True
                            st.session_state.paso_historial.append(3)
                            st.session_state.paso_resumen = 3.5
                            st.rerun()
                        if c2.button("2️⃣ No", use_container_width=True):
                            st.session_state.data_resumen["dropeo_nodos"] = False
                            st.session_state.data_resumen["dropeo_restriccion"] = False
                            st.session_state.paso_historial.append(3)
                            st.session_state.paso_resumen = 4
                            st.rerun()

                    # PASO 3.5: Dropeo por Restricción
                    elif paso == 3.5:
                        st.write("👇 **¿En la contingencia hubo dropeo de IDs por restricción?**")
                        c1, c2 = st.columns(2)
                        if c1.button("1️⃣ Sí", use_container_width=True):
                            st.session_state.data_resumen["dropeo_restriccion"] = True
                            st.session_state.paso_historial.append(3.5)
                            st.session_state.paso_resumen = 4
                            st.rerun()
                        if c2.button("2️⃣ No", use_container_width=True):
                            st.session_state.data_resumen["dropeo_restriccion"] = False
                            st.session_state.paso_historial.append(3.5)
                            st.session_state.paso_resumen = 4
                            st.rerun()

                    # PASO 4: Alchichica AM0
                    elif paso == 4:
                        st.write("👇 **¿Se cargó Alchichica ND en AM0?**")
                        c1, c2 = st.columns(2)
                        if c1.button("1️⃣ Sí", use_container_width=True):
                            st.session_state.data_resumen["alchichica"] = True
                            st.session_state.paso_historial.append(4)
                            st.session_state.paso_resumen = 4.5
                            st.rerun()
                        if c2.button("2️⃣ No", use_container_width=True):
                            st.session_state.data_resumen["alchichica"] = False
                            st.session_state.paso_historial.append(4)
                            st.session_state.paso_resumen = 5
                            st.rerun()

                    # PASO 4.5: Unidades Alchichica
                    elif paso == 4.5:
                        st.write("👇 **¿Fue con 2 Small Van MLP?**")
                        c1, c2 = st.columns(2)
                        if c1.button("1️⃣ Sí", use_container_width=True):
                            st.session_state.data_resumen["alchichica_2sv"] = True
                            st.session_state.paso_historial.append(4.5)
                            st.session_state.paso_resumen = 5
                            st.rerun()
                        if c2.button("2️⃣ No", use_container_width=True):
                            st.session_state.data_resumen["alchichica_2sv"] = False
                            st.session_state.paso_historial.append(4.5)
                            st.session_state.paso_resumen = 5
                            st.rerun()

                    # PASO 5: Día y Generación Final
                    elif paso == 5:
                        st.write("👇 **Día del ruteo:**")
                        dia_sel = st.selectbox(
                            "Selecciona:",
                            ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"],
                            index=4
                        )
                        
                        if st.button("🚀 Generar Resumen", use_container_width=True):
                            d = st.session_state.data_resumen
                            ciclo_txt = d.get("ciclo", "C1")
                            
                            unis = d.get("unidades_centro", [])
                            logis_tomo_todas = d.get("logis_tomo_todas", True)
                            unis_fuera = d.get("unidades_fuera", [])

                            # Construcción del texto de unidades
                            if logis_tomo_todas or not unis_fuera:
                                texto_unidades = "👉 <b>Unidades 3.5 tons y Delivery Cell</b>: se asignaron al polígono de Centro, logis tomó ambas."
                            elif len(unis_fuera) == len(unis):
                                texto_unidades = "👉 <b>Unidades 3.5 tons y Delivery Cell</b>: se asignaron al polígono de Centro, logis dejó fuera ambas."
                            else:
                                fuera_str = " y ".join([", ".join(unis_fuera[:-1]), unis_fuera[-1]]) if len(unis_fuera) > 1 else unis_fuera[0]
                                texto_unidades = f"👉 <b>Unidades 3.5 tons y Delivery Cell</b>: se asignaron al polígono de Centro, logis dejó fuera la {fuera_str}."

                            # Construcción del texto de dropeo
                            if d.get("dropeo_nodos", False):
                                if d.get("dropeo_restriccion", False):
                                    texto_dropeo = f"👉 <b>Hubo dropeo de nodo</b> y se cargó en contingencia (logis nos dejó fuera ids por zona de restricción)."
                                else:
                                    texto_dropeo = f"👉 <b>Hubo dropeo de nodo</b> y se cargó en contingencia."
                            else:
                                texto_dropeo = "👉 No hubo dropeo de nodo."

                            # Construcción del texto de Alchichica
                            if d.get("alchichica", False):
                                if d.get("alchichica_2sv", True):
                                    texto_alchichica = "🚛 Se cargó plan de <b>Alchichica ND</b> en AM0 con 2 unidades Small Van MLP."
                                else:
                                    texto_alchichica = "🚛 Se cargó plan de <b>Alchichica ND</b> en AM0."
                            else:
                                texto_alchichica = ""

                            # Bulk
                            texto_bulk = "📦 Se asignó H&B para el volumen Bulk." if d.get("hubo_bulk", False) else ""

                            # HTML con contenedor de peso normal para contrarrestar el CSS global
                            lineas_html = [
                                f"**Queda publicado {ciclo_txt} team**:<br><br>",
                                '<span style="font-weight: normal;">',
                                "📌 Se trabajó con el volumen disponible al momento de iniciar el ruteo.<br>",
                                "📌 Se cargaron las Rentals como híbridas en Centro, pero el sistema no las consideró todas como híbridas.<br>",
                                f"{texto_unidades}<br>"
                            ]
                            
                            if texto_bulk:
                                lineas_html.append(f"{texto_bulk}<br>")
                                
                            lineas_html.append(f"{texto_dropeo}<br>")
                            
                            if texto_alchichica:
                                lineas_html.append(f"{texto_alchichica}<br>")
                                
                            lineas_html.append(f"📌 Se usaron los parámetros establecidos para C1 del día {dia_sel}.<br>")
                            lineas_html.append("📋 Comparto template final.")
                            lineas_html.append("</span><br><br>")
                            lineas_html.append("<b>**¡Excelente turno! 👋**</b>")

                            resumen_final = "".join(lineas_html)

                            # Resetear flujo
                            st.session_state.flujo_resumen = False
                            st.session_state.paso_resumen = 0
                            st.session_state.paso_historial = []
                            st.session_state.main_chat_messages.append({"role": "assistant", "content": resumen_final})
                            st.rerun()

                    

                    # 🔙 BOTÓN DE VOLVER / CORREGIR PASO ANTERIOR
                    if len(st.session_state.paso_historial) > 0 and paso > 1:
                        st.markdown("---")
                        if st.button("↩️ Volver al paso anterior / Corregir", key="btn_atras_resumen"):
                            st.session_state.paso_resumen = st.session_state.paso_historial.pop()
                            st.rerun()

        # 2. OPCIONES INTERACTIVAS SMX5
        if st.session_state.esperando_subtipo_smx5:
            with st.chat_message("assistant"):
                st.write("👇 **Selecciona una opción o escribe 1 ó 2:**")
                col1, col2 = st.columns(2)
                eleccion_btn = None
                with col1:
                    if st.button("1️⃣ Extendido", key="btn_smx5_1", use_container_width=True):
                        eleccion_btn = "1"
                with col2:
                    if st.button("2️⃣ Precarga", key="btn_smx5_2", use_container_width=True):
                        eleccion_btn = "2"

                if eleccion_btn:
                    st.session_state.esperando_subtipo_smx5 = False
                    if eleccion_btn == "1":
                        st.session_state.main_chat_messages.append({"role": "user", "content": "1️⃣ Extendido"})
                        st.session_state.main_chat_messages.append({"role": "assistant", "content": reglas_ruteo["smx5_extendido"]})
                    else:
                        st.session_state.main_chat_messages.append({"role": "user", "content": "2️⃣ Precarga"})
                        st.session_state.main_chat_messages.append({"role": "assistant", "content": reglas_ruteo["smx5_precarga"]})
                    st.rerun()

        # 3. CAMPO DE ENTRADA AL FINAL
        if query_main := st.chat_input("✏️ Escribe tu consulta...", key="main_chat_input"):
            st.session_state.main_chat_messages.append({"role": "user", "content": query_main})
            query_lower = query_main.lower().strip()

            # A) RESUMEN O CIERRE
            if "resumen" in query_lower or "cierre" in query_lower or "ciere" in query_lower:
                st.session_state.flujo_resumen = True
                st.session_state.paso_resumen = 1
                st.session_state.paso_historial = []
                st.session_state.data_resumen = {}
                st.session_state.main_chat_messages.append({
                    "role": "assistant", 
                    "content": "📋 **Generador de Cierre.** Responde seleccionando las opciones de abajo:"
                })
                st.rerun()

            # B) FLUJO INTERACTIVO SMX5
            elif st.session_state.esperando_subtipo_smx5:
                st.session_state.esperando_subtipo_smx5 = False
                if "extendido" in query_lower or "1" in query_lower:
                    respuesta_main = reglas_ruteo["smx5_extendido"]
                elif "precarga" in query_lower or "2" in query_lower:
                    respuesta_main = reglas_ruteo["smx5_precarga"]
                else:
                    respuesta_main = "⚠️ Opción no válida. Consulta escribiendo **SMX5** nuevamente."

            # C) DETECCION ESPECIFICA SMX5
            elif query_lower == "smx5":
                st.session_state.esperando_subtipo_smx5 = True
                respuesta_main = "🔍 Detecté **SMX5**. ¿De cuál requieres las prioridades?\n\n1️⃣ **Extendido**\n2️⃣ **Precarga**\n\n*(Elige dando clic en los botones superiores o escribe 1 ó 2)*"

            # D) BUSCADOR INTELIGENTE LOCAL
            else:
                partes_respuesta = []

                # 1. BÚSQUEDA EN MAPA OPERATIVO
                svc_mapa = None
                for key in MAPA_ORIGENES.keys():
                    if key in query_lower:
                        svc_mapa = key
                        break

                if svc_mapa:
                    info = MAPA_ORIGENES[svc_mapa]
                    origen_tag = f"<span style='background-color: #e2e8f0; color: #0f172a; padding: 2px 8px; border-radius: 4px; font-weight: bold; font-family: monospace;'>{info['origen']}</span>"
                    
                    bloque_mapa = (
                        f"📍 **Origen y Validación para {svc_mapa.upper()}:**\n\n"
                        f"* 🗺️ **Región:** Región {info['region']}\n"
                        f"* 🏢 **Origen(es) On Way:** {origen_tag}\n"
                        f"* ✅ **Validación requerida:** {info['val']}\n\n"
                        f"*(Nota: Si el SVC solicita agregar blancos, se anexan)*"
                    )
                    partes_respuesta.append(bloque_mapa)

                # 2. BÚSQUEDA EN PREGUNTAS FRECUENTES
                coincidencias_faq = []
                
                if any(w in query_lower for w in ["large van sdd", "sdd"]):
                    coincidencias_faq.append(PREGUNTAS_FRECUENTES["large_van_sdd"])
                
                if "bulk" in query_lower:
                    if "sja1" in query_lower or "centro 1" in query_lower or "centro 2" in query_lower:
                        coincidencias_faq.append(PREGUNTAS_FRECUENTES["bulk_sja1"])
                    else:
                        coincidencias_faq.append(PREGUNTAS_FRECUENTES["bulk_general"])
                
                if "alchichica" in query_lower: 
                    coincidencias_faq.append(PREGUNTAS_FRECUENTES["alchichica"])
                
                if any(w in query_lower for w in ["xico", "tuzamapa"]):
                    coincidencias_faq.append(PREGUNTAS_FRECUENTES["tuzamapa_xico"])
                
                if "dropeo" in query_lower or "drop" in query_lower:
                    coincidencias_faq.append(PREGUNTAS_FRECUENTES["dropeo_nodos_sja1"])
                
                if "prioridad" in query_lower or "prioridades" in query_lower or "asignacion" in query_lower or "asignación" in query_lower:
                    if "sja1" in query_lower and any(w in query_lower for w in ["foraneo", "foráneo", "foraneos", "foráneos"]):
                        coincidencias_faq.append(PREGUNTAS_FRECUENTES["prioridades_foraneos_sja1"])
                    elif "sja1" in query_lower:
                        coincidencias_faq.append(PREGUNTAS_FRECUENTES["prioridades_centro_sja1"])
                        coincidencias_faq.append(PREGUNTAS_FRECUENTES["prioridades_foraneos_sja1"])
                    elif "smd1" in query_lower:
                        coincidencias_faq.append(PREGUNTAS_FRECUENTES["smd1_prioridad"])

                if any(w in query_lower for w in ["quitar", "quitar unidades", "ciclo 2", "pasar a ciclo 2", "orh"]):
                    if "scp1" in query_lower or not svc_mapa:
                        coincidencias_faq.append(PREGUNTAS_FRECUENTES["scp1_cambios"])

                if coincidencias_faq:
                    partes_respuesta.append("\n\n---\n\n".join(coincidencias_faq))

                # 3. BÚSQUEDA EN REGLAS DE RUTEO TRADICIONALES
                if not coincidencias_faq:
                    mapeo_centros = {
                        "smx9": "smx9_extendido", "sgd2": "sgd2_extendido", "smx4": "smx4_extendido",
                        "smx2": "smx2_extendido", "smt2": "smt2_extendido", "scp1": "scp1",
                        "smd1": "smd1", "sch1": "sch1", "sja1": "sja1"
                    }

                    centro_encontrado = None
                    clave_regla = None

                    if "smx5" in query_lower:
                        centro_encontrado = "SMX5"
                        clave_regla = "smx5_precarga" if "precarga" in query_lower else "smx5_extendido"
                    else:
                        for termino, clave in mapeo_centros.items():
                            if termino in query_lower:
                                centro_encontrado = termino.upper()
                                clave_regla = clave
                                break

                    busqueda_origen = any(w in query_lower for w in ["origen", "origenes", "orígenes", "de donde", "de dónde", "sale"])
                    busqueda_hora = any(w in query_lower for w in ["despacho", "hora", "horario", "tiempo"])
                    busqueda_unidad = any(w in query_lower for w in ["unidad", "unidades", "moto", "motos", "van", "crowd", "rental"])

                    if clave_regla and clave_regla in reglas_ruteo:
                        texto_regla = reglas_ruteo[clave_regla]
                        lineas = [l.strip() for l in texto_regla.split("\n") if l.strip()]

                        if svc_mapa:
                            lineas = [l for l in lineas if not any(palabra in l.lower() for palabra in ["origen", "orígenes", "📌 origen"])]

                        lineas_filtradas = []
                        if busqueda_hora:
                            lineas_filtradas = [l for l in lineas if any(h in l.lower() for h in ["despacho", "pm", "am", "hora"])]
                        elif busqueda_unidad:
                            lineas_filtradas = [l for l in lineas if any(u in l.lower() for u in ["moto", "van", "rental", "crowd", "mlp", "cell", "small"])]

                        if lineas_filtradas:
                            res = "\n".join(lineas_filtradas)
                            bloque_regla = f"📌 **Indicaciones específicas ({centro_encontrado}):**\n\n{res}"
                        else:
                            res = "\n".join(lineas)
                            bloque_regla = f"📋 **Indicaciones complementarias ({centro_encontrado}):**\n\n{res}"

                        if lineas and not (svc_mapa and busqueda_origen):
                            partes_respuesta.append(bloque_regla)

                # 4. MONTAJE DE LA RESPUESTA FINAL
                if partes_respuesta:
                    respuesta_main = "\n\n---\n\n".join(partes_respuesta)
                else:
                    if "resumen" in query_lower:
                        respuesta_main = "Aquí tienes la opción para armar tu reporte."
                    else:
                        respuesta_main = "⚠️ No encontré esa consulta en la base de datos. Puedes consultar por un SVC (ej. SJA1, SLE1, SCP1) o sobre temas específicos como **Alchichica, Xico, Dropeo, Bulk, SDD, etc.**"

            st.session_state.main_chat_messages.append({"role": "assistant", "content": respuesta_main})
            st.rerun()




# --- DATOS BASE ---
u_SDE = {"Moto Car - 3": [25, 30], "Moto Car Newbie": [25, 25], "Car - 5h": [25, 30], "Car - 5 Extendida": [25, 30], "Car - 3h": [25, 28]}

u_PREC = {      
    "Car - 8h": [70, 75],
    "Small 9h Ext Car": [70, 75] 
}

NOMBRES_PLANES_PREC = ["CHALCO", "COYOACÁN", "IZTAPALAPA", "MILPA ALTA", "TLAHUAC", "TLALPAN NORTE", "TLALPAN SUR", "XOCHIMILCO"]


# --- AÑADE ESTO DEBAJO DE U_PREC ---
u_PREC_SMX2 = {
    "Car - 8h": [70, 75],
    "Small 9h Ext Car": [70, 75],
    "Car Zona Extendida": [65, 65]
}
NOMBRES_PLANES_PREG = ["CHALCO", "CHIMAS", "IXTAPALUCA VALLE CHALCO", "IZTAPALAPA 1", "IZTAPALAPA 2", "LA PAZ", "PUEBLOS", "TEXCOCO"]


NOMBRES_PLANES_C1 = [
    "CALKINI", 
    "CAMPECHE",
    "CANDELARIA",
    "CHAMPOTÓN",
    "ESCÁRCEGA",
    "ESCÁRCEGA EXT",
    "HOLPECHEN",
    "MAXCANUN",
    "SEYBAPLAYA",
    "PLAN 10",
    "PLAN 11"
]

u_C1 = {
    "Rental Large Van": [100, 100], "Large Van MLP": [100, 100], "Small Van MLP":[100, 100], "Delivery Cell Large Van": [1, 1], "Delivery Cell Small Van": [1, 1]
}

u_C2 = u_C1.copy()
u_C2["Large Van Híbrida"] = [100, 100]


# --- DATOS NUEVOS PARA C1 SJA1 ---
u_C1_SJA1 = { 
    "Small Van MLP foráneo": [110, 120], 
    "Large Van MLP foráneo": [110, 120], 
    "Car MLP": [80, 100],
    "Extra Large Van MLP H&B": [70, 70],
    "Rental Electric Large Van": [150, 150],
    "Rental Large Van": [120, 120],
    "Rental Replacement": [120, 120],
    "Truck 3.5 tons MLP": [1, 1],
    "Delivery Cell Large Van": [1, 1],
    "Car 8h": [70, 70], 
    "Car Newbie": [70, 70],
    "Car Zona Extendida": [70, 70],
    "Moto 3h": [30, 30],
    "Small Van 9h": [70, 70],
    "Small Van 9h Ext": [70, 70],
    "Small Van Newbie": [70, 70],
    "Media Milla SP": [1, 1]
}

NOMBRES_PLANES_C1_SJA1 = [
   "ACTOPAN", "⚠️ CENTRO 1", "⚠️ CENTRO 2", "EJA1 SP", "MISANTLA", "NAOLINCO", "PEROTE", "TEZUITLAN", "TLALTETELA", "TRAPICHE",  
   "TUZAMAPA", "XICO", "CONTINGENCIA NODO", "PLAN 14", "PLAN 15", "PLAN 16", "PLAN 17"
]


# --- DATOS NUEVOS PARA C1 SCH1 ---
u_C1_SCH1 = { 
    "Car MLP": [110, 120],
    "Small Van MLP": [110, 120],
    "Large Van MLP": [110, 120],
    "Small Van MLP Newbie": [110, 120],
    "Large Van MLP Newbie": [110, 120],
    "Extra large Van MLP": [110, 120],
    "Small Van MLP XPT": [110, 120],
    "Small Van MLP foráneo": [110, 120],
    "Large Van MLP foráneo": [110, 120],
    "Car MLP foráneo": [110, 120],
    "Extra large Van MLP H&B": [100, 100],
    "Rental Car": [120, 150],
    "Rental Electric Large Van": [120, 150],
    "Rental Large Van": [120, 150],
    "Rental Replacement": [120, 150],
    "Rental Small Van Electrica": [120, 150],
    "Rental Small Van": [120, 150],
    "Delivery Cells Car": [1, 1],
    "Truck 3.5 tons MLP": [1, 1],
    "Delivery Cell Large Van": [1, 1],
    "Car 8h": [70, 70],
    "Car Newbie": [50, 50],
    "Car Zona Extendida": [60, 60],
    "Moto 3h": [30, 30],
    "Moto Newbie": [25, 25],
    "Small Van 11h Ext": [70, 70],
    "Small Van 9h": [70, 70],
    "Small Van 9h Ext": [70, 70],
    "Small Van Newbie": [70, 70]
}

NOMBRES_PLANES_C1_SCH1 = [
   "AEROPUERTO", "CANTERA", "DELICIAS", "GRANJAS", "MEOQUI", "NORTE", "SUR", "CUAUHTEMOC", "PARRAL", "PLAN 10",  
   "PLAN 11", "PLAN 12", "PLAN 13", "PLAN 14"
]


# --- DATOS NUEVOS PARA C1 VACÍA (TAB 9) ---
u_C1_VACIA = { 
    "Car MLP": [110, 120],
    "Small Van MLP": [110, 120],
    "Large Van MLP": [110, 120],
    "Small Van MLP Newbie": [110, 120],
    "Large Van MLP Newbie": [110, 120],
    "Extra large Van MLP": [110, 120],
    "Small Van MLP XPT": [110, 120],
    "Small Van MLP foráneo": [110, 120],
    "Large Van MLP foráneo": [110, 120],
    "Car MLP foráneo": [110, 120],
    "Extra large Van MLP H&B": [100, 100],
    "Rental Car": [120, 150],
    "Rental Electric Large Van": [120, 150],
    "Rental Large Van": [120, 150],
    "Rental Replacement": [120, 150],
    "Rental Small Van Electrica": [120, 150],
    "Rental Small Van": [120, 150],
    "Delivery Cells Car": [1, 1],
    "Truck 3.5 tons MLP": [1, 1],
    "Delivery Cell Large Van": [1, 1],
    "Car 8h": [70, 70],
    "Car Newbie": [50, 50],
    "Car Zona Extendida": [60, 60],
    "Car 3h": [30,30],
    "Car 5h": [30, 30],
    "Moto 3h": [30, 30],
    "Moto Newbie": [25, 25],
    "Small Van 11h Ext": [70, 70],
    "Small Van 9h": [70, 70],
    "Small Van 9h Ext": [70, 70],
    "Small Van Newbie": [70, 70]
}

NOMBRES_PLANES_C1_VACIA = [
   "PLAN 1", "PLAN 2", "PLAN 3", "PLAN 4", "PLAN 5", "PLAN 6", "PLAN 7", "PLAN 8", "PLAN 9", "PLAN 10",  
   "PLAN 11", "PLAN 12", "PLAN 13", "PLAN 14"
]


# --- DATOS NUEVOS PARA C1 SMD1 ---
u_C1_SMD1 = { 
    "Car MLP": [110, 120],
    "Small Van MLP": [110, 120],
    "Large Van MLP": [110, 120],
    "Small Van MLP Newbie": [110, 120],
    "Large Van MLP Newbie": [110, 120],
    "Extra large Van MLP": [110, 120],
    "Small Van MLP XPT": [110, 120],
    "Small Van MLP foráneo": [110, 120],
    "Large Van MLP foráneo": [110, 120],
    "Large Van MLP Bulk": [100, 100],
    "Extra large Van MLP H&B": [50, 50],
    "Rental Car": [120, 150],
    "Rental Electric Large Van": [120, 150],
    "Rental Large Van": [120, 150],
    "Rental Replacement": [120, 150],
    "Rental Small Van Electrica": [120, 150],
    "Rental Small Van": [120, 150],
    "Delivery Cells Car": [1, 1],
    "Truck 3.5 tons MLP": [1, 1],
    "Delivery Cell Large Van": [1, 1],
    "Car 8h": [70, 70],
    "Car Newbie": [50, 50],
    "Car Zona Ext 10h": [70, 70],
    "Moto 3h": [30, 30],
    "Moto Newbie": [25, 25],
    "Small Van 11h Ext": [70, 70],
    "Small Van 9h": [70, 70],
    "Small Van 9h Ext": [70, 70],
    "Small Van Newbie": [70, 70]
}

NOMBRES_PLANES_C1_SMD1 = [
   "⚠️ CENTRO 1", "⚠️ CENTRO 2", "⚠️ KANASIN", "MOTUL", "MUNA", "⚠️ NORTE", "SEYE", "UMAN", "PLAN 9", "PLAN 10",  
   "PLAN 11", "PLAN 12", "PLAN 13", "PLAN 14"
]


# ================= ORH POR UNIDAD =================

ORH_FIJOS = {
    "Rental E. Large Van": ["500", "70"],
    "Rental E. Small Van": ["450", "70"],
    "Rental Large Van": ["54", "70"],
    "Rental Small Van": ["480", "70"],

    "Large Van MLP": ["500", "80"],
    "Small Van MLP": ["487", "70"],
    "Large Van SDD": ["487", "70"],
    "Small Van SDD": ["487", "70"],

    "Car MLP": ["300", "66"],
    "Car Newbie 3h": ["180", "66"],
    "Car Newbie": ["360", "83"],

    "Car - 8h": ["360", "66"],
    "Car - 8h E1": ["360", "66"],
    "Car - 5h": ["300", "66"],
    "Car - 3h": ["300", "66"],

    "Moto - 3h": ["180", "66"],

    "Small Van SDD": ["487", "70"],
    "Car Zona Extendida": ["360", "66"],
    "Car - 5 Extendida": ["330", "66"],
    "Small 9h Ext Car": ["360", "66"]
}



def gen_master_rows(data_dict, table_id):
    rows = ""
    items = list(data_dict.items())
    total_items = len(items)

    nombres_prec = ["CHALCO", "COYOACÁN", "IZTAPALAPA", "MILPA ALTA", "TLAHUAC", "TLALPAN NORTE", "TLALPAN SUR", "XOCHIMILCO"]
    nombres_smx2 = ["CHALCO", "CHIMAS", "IXTAPALUCA VALLE CHALCO", "IZTAPALAPA 1", "IZTAPALAPA 2", "LA PAZ", "PUEBLOS", "TEXCOCO"]

    # ✅ Mostrar ORH/OCUPACIÓN solo en C1 y PREC SMX5 (ajusta si tu id real de PREC SMX5 es otro)
    mostrar_orh_ocup = (table_id in [1, 2, 6, 7, 8, 5, 9])

    num_filas_objetivo = 45 if table_id == "PREC" else 3
    rango_final = max(total_items, num_filas_objetivo)

    for i in range(1, rango_final + 1):
        if (data_dict == u_PREC) and (i-1) < len(nombres_prec):
            p_name = nombres_prec[i-1]
        elif (data_dict == u_PREC_SMX2) and (i-1) < len(nombres_smx2):
            p_name = nombres_smx2[i-1]
        else:
            p_name = f"PLAN {i}"

        if (i-1) < total_items:
            name, spr = items[i-1]
        else:
            name, spr = "", [0, 0]

        # Caso A: Encabezado/Divisor
        if "---" in name:
            # Antes colspaneabas 5; ahora depende si agregamos 2 columnas visibles
            colspan = 8 if mostrar_orh_ocup else 5

            rows += f'''
            <tr class="es-divisor" style="background: #25282b !important; color: #25282b; height: 28px;">
                <td colspan="{colspan}" style="text-align: center; font-weight: bold; font-size: 13px; letter-spacing: 3px; border: none; pointer-events: none;"> 
                    {name}
                </td>
                <td class="edit-name" style="display:none;">IGNORAR</td>
                <td class="edit-spr-min" style="display:none;">0</td>
                <td class="edit-spr-max" style="display:none;">0</td>
                <td class="edit-orh" style="display:none;">0</td>
                <td class="edit-ocup" style="display:none;">0</td>
                <td class="f-stock" style="display:none;">0</td>
                <td class="f-left" style="display:none;">0</td>
            </tr>'''

        # Caso B: unidad normal o espacio vacío
        else:
            st_base = "background: #ebebeb; color: #969696;" if not name else ""

            # ✅ Celdas extra visibles SOLO en C1 y PREC SMX5
            celdas_orh_ocup = ""
            if mostrar_orh_ocup:
                celdas_orh_ocup = f'''
                <td contenteditable="true"
                    class="edit-orh"
                    oninput="recalc()"
                    style="text-align:center; border:0.2px solid #25282b; width:45px; background:#ffffff; color:#141414;">
                    0
                </td>

                <td class="orh-hora"
                    style="text-align:center; border:0.2px solid #25282b; width:60px; background:#f5f5f5; color:#141414; font-weight:bold;">
                    00:00 hs
                </td>

                <td contenteditable="true"
                    class="edit-ocup"
                    oninput="recalc()"
                    style="text-align:center; border:0.2px solid #25282b; width:70px; background:#ffffff; color:#25282b;">
                    0
                </td>
                '''


                
            else:
                # En tablas donde NO deben verse, se mantienen ocultas (como ya lo tenías)
                celdas_orh_ocup = '''
                <td class="edit-orh" style="display:none;">0</td>
                <td class="orh-hora" style="display:none;">00:00 hs</td>
                <td class="edit-ocup" style="display:none;">0</td>
                '''

            rows += f'''
            <tr class="master-row" style="{st_base}">
                <td contenteditable="true" class="edit-name" oninput="recalc()"
                    style="font-weight: bold; text-align: left; padding-left: 10px; border: 0.2px solid #25282b; width: 150px; color: #25282b;">
                    {name}
                </td>

                {celdas_orh_ocup}

                <td contenteditable="true" class="edit-spr-min" oninput="recalc()"
                    style="text-align: center; border: 0.2px solid #25282b; width: 45px; background-color: #25282b; color: #ffffff;">
                    {spr[0]}
                </td>

                <td contenteditable="true" class="edit-spr-max" oninput="recalc()"
                    style="text-align: center; border: 0.2px solid #25282b; width: 45px; background-color: #25282b; color: #ffffff;">
                    {spr[1]}
                </td>

                <td contenteditable="true" class="f-stock" oninput="recalc()"
                    style="text-align: center; border: 0.2px solid #25282b; width: 55px; font-weight: bold; font-size: 13px;">
                    0
                </td>

                <td class="f-ruteadas" 
                    style="text-align: center; border: 0.2px solid #25282b; width: 55px; background-color: #ffffff; font-weight: bold;">
                    0
                </td>

                <td class="f-left"
                    style="text-align:center; border:0.2px solid #25282b; width:45px; font-weight:bold; color:#25282b; border-radius:2px;">
                    0
                </td>
            </tr>'''
    return rows






def export_c1_csv():
    data = []
    for unidad, spr in u_C1.items():
        data.append({{
            "PLAN": "C1",
            "UNIDAD": unidad,
            "SPR_MIN": spr[0],
            "SPR_MAX": spr[1]
        }})

    df_c1 = pd.DataFrame(data)
    csv = df_c1.to_csv(index=False).encode("utf-8")
    return csv






def gen_poligonos(data_target=None):
    polys = ""  # ✅ NO usar triple comillas aquí
 
    # Botones con dimensiones totalmente congeladas a nivel píxel
    btn_s = "cursor:pointer; border:none; background:rgba(0,0,0,0.08); color:#25282b; font-weight:bold; width:24px; min-width:24px; max-width:24px; height:24px; min-height:24px; max-height:24px; border-radius:4px; flex-shrink:0; display:inline-flex; align-items:center; justify-content:center;"
    
    nombres_prec = ["CHALCO", "COYOACÁN", "IZTAPALAPA", "MILPA ALTA", "TLAHUAC", "TLALPAN NORTE", "TLALPAN SUR", "XOCHIMILCO"]
    nombres_smx2 = ["CHALCO", "CHIMAS", "IXTAPALUCA VALLE CHALCO", "IZTAPALAPA 1", "IZTAPALAPA 2", "LA PAZ", "PUEBLOS", "TEXCOCO"]
    nombres_c1 = ["ESCÁRCEGA", "CAMPECHE", "ESCÁRCEGA EXT", "MAXCANUN", "CANDELARIA", "SEYBAPLAYA", "CHAMPOTÓN", "HOLPECHEN"]  
   
    es_c1 = data_target in (
        u_C1,
        u_C1_SJA1,
        u_C1_SCH1,
        u_C1_SMD1,
        u_C1_VACIA,
    )
    es_sde = (data_target == u_SDE)
    es_prec = (data_target == u_PREC)
    es_prec_smx2 = (data_target == u_PREC_SMX2)

    
    # Contenedor flex con ancho bloqueado al 100% de la celda
    div_flex = "display: flex; align-items: center; justify-content: space-between; padding: 2px 4px; width: 100%; min-width: 100%; max-width: 100%; box-sizing: border-box;"
    
    # Cajas de texto para números (Unidades y SPR)
    span_num_u = "font-weight: bold; display: inline-block; text-align: center; width: 28px; min-width: 28px; max-width: 28px; flex-shrink: 0;"
    span_num_spr = "font-weight: bold; display: inline-block; text-align: center; width: 38px; min-width: 38px; max-width: 43px; flex-shrink: 0;"
    
    # 🔥 ESTILO DEL SELECTOR RECALIBRADO (Letra más grande, legible y cómoda para la operación)
    select_style = "width:160px; max-width: 160px; border:none; background:transparent; font-weight:600; font-size:14px; color:#25282b; padding: 4px; cursor: pointer;"


    fila_nodos = '''
<tr class="fila-nodos">
    <td style="background:#ededed; border:0.5px solid #25282b; text-align:center; font-weight:bold; color:#FF6347;">
        NODOS
    </td>
    <td contenteditable="true"
        class="nodos-val"
        style="border:1.0px solid #25282b; text-align:center; font-weight:bold;">
        0
    </td>
    <td colspan="2" style="border:0.5px solid #25282b;"></td>
</tr>
'''


    
    fila_inner = f'''
    <tr class="calc-row">
        <td class="u-manual-cell" style="background: #d3f0e5; border: 0.6px solid #25282b; padding: 2px; width: 105px; min-width: 105px; max-width: 105px;">
            <div style="{div_flex}">
                <button style="{btn_s}" onclick="stepVal(this, -1, 'u')">-</button>
                <span contenteditable="true" class="u-manual" oninput="manualEdit(this)" style="{span_num_u}color: #25282b !important;">0</span>
                <button style="{btn_s}" onclick="stepVal(this, 1, 'u')">+</button>
            </div>
        </td>
        <td class="spr-real-cell" style="background: #FFFFFF; border: 0.6px solid #25282b; padding: 2px; width: 90px; min-width: 90px; max-width: 90px;">
            <div style="{div_flex}">
                <button style="{btn_s}" onclick="stepVal(this, -1, 's')">-</button>
                <span contenteditable="true" class="spr-real-val" oninput="manualEdit(this)" style="{span_num_spr} color: #25282b !important;">0</span>
                <button style="{btn_s}" onclick="stepVal(this, 1, 's')">+</button>
            </div>
        </td>
        <td style="border: 0.5px solid #25282b; padding: 2px; width: 170px; min-width: 170px; max-width: 170px;">
            <select class="s-type" onchange="resetRow(this); updateSelectColor(this);" style="{select_style} color: #808080;"> 
                <option value="">Seleccionar...</option>
            </select>
        </td>
        <td style="width: 45px; min-width: 45px; max-width: 45px; text-align: center; border: 0.5px solid #25282b;"><input type="checkbox" class="ok-check" style="transform: scale(1.7); accent-color: #9ACD32; cursor: pointer;"></td>
    </tr>'''



    campo_volumen_normal = '''
<div style="text-align:center;">
    <span class="v-total-val"
            contenteditable="true"
            oninput="recalc()"
            style="
            display:inline-block;
            min-width:55px;
            padding:2px 8px;
            border:none;
            border-radius:4px;
            background:#ededed;
            font-size:22px;
            font-weight:bold;
            color:#808080;
            text-align:center;
          ">
        0
    </span>
</div>
'''

    
    campo_volumen_c1 = '''
<div style="text-align:center;">
    <span class="v-total-val"
          contenteditable="true"
          oninput="recalc()"
          style="
            display:inline-block;
            min-width:55px;
            padding:2px 8px;
            border:none;
            border-radius:4px;
            background:#ededed;
            font-size:22px;
            font-weight:bold;
            color:#808080;
            text-align:center;
          ">
        0
    </span>
</div>

<hr style="margin:4px 0; border:none; border-top:2px solid #999;">

<!-- 🔥 NODOS EN DOS LÍNEAS (Palabra arriba, número 0 abajo) -->
<div style="font-size:12px; font-weight:bold; color:#25282b; text-align:center;">
    <div>Nodos:</div>
    <span class="nodos-val"
      contenteditable="true"
      style="
        display:inline-block;
        min-width:28px;
        text-align:center;
        border:none;
        border-radius:4px;
        background:#ededed;
        font-size:16px;
        font-weight:bold;
        color:#FF6347;
        padding:0 4px;
        margin-top:2px;
      ">
        0
    </span>
</div>
'''

    campo_campeche = '''
<div style="text-align:center;">
    <span class="v-total-val"
          contenteditable="true"
          oninput="recalc()"
          style="
            display:inline-block;
            min-width:55px;
            padding:2px 8px;
            border:none;
            border-radius:4px;
            background:#ededed;
            font-size:22px;
            font-weight:bold;
            color:#808080;
            text-align:center;
          ">
        0
    </span>
</div>

<hr style="margin:4px 0; border:none; border-top:1px solid #999;">

<div style="font-size:13px; font-weight:bold; color:#25282b; text-align:center;">
    Nodos:
    <div style="margin-top:2px;">
        <span class="nodos-campeche"
              contenteditable="true"
              style="
                display:inline-block;
                min-width:28px;
                text-align:center;
                border:none;
                border-radius:4px;
                background:#ededed;
                font-size:16px;
                font-weight:bold;
                color:#FF6347;
                padding:0 4px;
              ">
            0
        </span>
    </div>
</div>
'''


    ## Definimos dinámicamente si renderiza 10 o 20 tablas de polígonos
    if data_target == u_C1_SJA1:
        limite_tablas = len(NOMBRES_PLANES_C1_SJA1) + 1

    elif data_target == u_C1_SCH1:
        limite_tablas = 16

    elif data_target == u_C1_SMD1:
        limite_tablas = 20

    elif data_target == u_C1_VACIA:
        limite_tablas = 16  # 👈 CORREGIDO: Renderiza 15 tablas (16 - 1)

    elif es_sde:
        limite_tablas = 5

    else:
        limite_tablas = 20
    
    for i in range(1, limite_tablas): 

        # 🟢 EVALUAR VACÍA PRIMERO
        if data_target == u_C1_VACIA and (i-1) < len(NOMBRES_PLANES_C1_VACIA):
            nombre_final = NOMBRES_PLANES_C1_VACIA[i-1]

        elif data_target == u_PREC and (i-1) < len(nombres_prec):
            nombre_final = nombres_prec[i-1]

        elif data_target == u_PREC_SMX2 and (i-1) < len(nombres_smx2):
            nombre_final = nombres_smx2[i-1]

        elif data_target == u_C1 and (i-1) < len(NOMBRES_PLANES_C1):
            nombre_final = NOMBRES_PLANES_C1[i-1]
            
        elif data_target == u_C1_SJA1 and (i-1) < len(NOMBRES_PLANES_C1_SJA1):
            nombre_final = NOMBRES_PLANES_C1_SJA1[i-1]

        elif data_target == u_C1_SCH1 and (i-1) < len(NOMBRES_PLANES_C1_SCH1):
            nombre_final = NOMBRES_PLANES_C1_SCH1[i-1]

        elif data_target == u_C1_SMD1 and (i-1) < len(NOMBRES_PLANES_C1_SMD1):
            nombre_final = NOMBRES_PLANES_C1_SMD1[i-1]

        else:
            nombre_final = f"PLAN {i}"

        # Asignación de formato de volumen
        if nombre_final == "CAMPECHE":
            contenido_volumen = campo_campeche

        elif es_c1:
            contenido_volumen = campo_volumen_c1

        else:
            contenido_volumen = campo_volumen_normal

        # 🌟 DEFINIMOS EL ALTO DE LA CELDA GRIS (ROWSPAN)
        if es_sde:
            rowspan_actual = 3
        elif es_prec:
            rowspan_actual = 3
        
        elif data_target == u_C1_SJA1:
            if nombre_final == "⚠️ CENTRO 1":
                rowspan_actual = 8
            else:
                rowspan_actual = 5
        
        elif data_target in (u_C1_SMD1, u_C1_VACIA):
            rowspan_actual = 5  # 👈 CORREGIDO: 5 filas por tabla para C1 VACÍA
            
        else:
            rowspan_actual = 3

        # 🌟 AGREGAMOS LAS FILAS EXTRA CORRESPONDIENTES
        if es_sde:
            filas_extra = fila_inner * 2
        elif es_prec:
            filas_extra = fila_inner * 2
        elif data_target == u_C1_SJA1:
            if nombre_final == "⚠️ CENTRO 1":
                filas_extra = fila_inner * 7
            else:
                filas_extra = fila_inner * 4
        elif data_target in (u_C1_SMD1, u_C1_VACIA):
            filas_extra = fila_inner * 4  # 👈 CORREGIDO: 4 filas extra (5 en total con la principal)
        else:
            filas_extra = fila_inner * 2

        
        
        polys += f'''
        <div class="poligono-bloque" style="margin-bottom:12px; box-shadow: none; border-radius: 0px; overflow-x: auto; background: #ededed; border: 1.5px solid #25282b;">           
            <table style="width: 100%; min-width: 630px; border-collapse: collapse; border: 1.5px solid #25282b;">
                <thead>
                    <tr style="background: #25282b; color: white; font-size: 12px; height: 28px;">                        
                        <th style="padding: 0 10px; border-right: 1px solid #25282b; min-width: 130px; width: 130px;">PLAN</th>
                        <th style="border-right: 1px solid #25282b; width: 85px;">VOL. TOTAL</th>
                        <th style="width: 105px; min-width: 105px; max-width: 105px; border-right: 1px solid #25282b;"># USADAS</th>
                        <th style="width: 105px; min-width: 105px; max-width: 105px; border-right: 1px solid #25282b;">SPR</th>
                        <th style="width: 180px; min-width: 180px; max-width: 180px; border-right: 1px solid #25282b;">TIPO DE UNIDAD</th>
                        <th style="width: 45px; min-width: 45px; max-width: 45px; text-align: center;">OK</th> 
                    </tr>
                </thead>
                <tbody>
                    <tr class="calc-row"> 
                        <td class="plan-cell" rowspan="{rowspan_actual}" contenteditable="true" style="background: #dcdcdc; font-weight: bold; text-align:center; border: 1px solid #25282b; padding: 5px; color:#141414;">{nombre_final}</td>
                        <td class="vol-cell" rowspan="{rowspan_actual}"
                            style="color:#808080;
                                   font-weight:bold;
                                   text-align:center;
                                   border:1px solid #25282b;
                                   padding:5px;">
                            {contenido_volumen}
                        </td>
                        <td class="u-manual-cell" style="background: #d3f0e5; border: 0.5px solid #25282b; padding: 2px; width: 105px; min-width: 105px; max-width: 105px;">
                            <div style="{div_flex}">
                                <button style="{btn_s}" onclick="stepVal(this, -1, 'u')">-</button> 
                                <span contenteditable="true" class="u-manual" oninput="manualEdit(this)" style="{span_num_u} color: #25282b !important;">0</span>
                                <button style="{btn_s}" onclick="stepVal(this, 1, 'u')">+</button>
                            </div>
                        </td>
                        <td class="spr-real-cell" style="background: #FFFFFF; border: 0.5px solid #25282b; padding: 2px; width: 90px; min-width: 90px; max-width: 90px;">
                            <div style="{div_flex}">
                                <button style="{btn_s}" onclick="stepVal(this, -1, 's')">-</button>
                                <span contenteditable="true" class="spr-real-val" oninput="manualEdit(this)" style="{span_num_spr}">0</span>
                                <button style="{btn_s}" onclick="stepVal(this, 1, 's')">+</button>
                            </div>
                        </td>
                        <td style="border: 0.5px solid #25282b; padding: 2px;">
                            <select class="s-type" onchange="resetRow(this)" style="{select_style}">
                                <option>Seleccionar...</option>
                            </select>
                        </td>
                        <td style="width: 45px; min-width: 45px; max-width: 45px; text-align: center; border: 0.5px solid #25282b;"><input type="checkbox" class="ok-check" style="transform: scale(1.7); accent-color: #9ACD32; cursor: pointer;"></td>
                    </tr>
                    {filas_extra}
                    {""}
                    <tr style="background:#ededed; height: 32px;">
                        <td colspan="3" style="text-align:center; font-weight:bold; border: 1px solid #25282b; font-size: 14px; color:#25282b;">ESTADO:</td>
                        <td class="v-calculado-total" style="font-weight: bold; font-size: 14px; color: #d32f2f; border: 1px solid #25282b; text-align: center;">0</td>
                      <td class="p-diff delta" colspan="2" style="text-align: center; font-weight: bold; border: 1px solid #25282b; font-size: 14px; color: #25282b">VACÍO:</td>
                    </tr>
                    
                </tbody>
                
                   <div style="text-align:center; padding:5px; background:#ededed;">
                <button onclick="agregarFilaPlan(this)" 
                        style="cursor:pointer; margin-right:5px;">
                    ➕ 
                </button>

                <button onclick="quitarFilaPlan(this)"
                        style="cursor:pointer;">
                    ➖ 
                </button>

                <span class="contador-filas" style="margin-left:10px;font-weight:bold;">
                    Filas: {rowspan_actual}
                </span>
            </div>     
            
        </table>

            

        </div>'''
    return polys


# --- PERFILES LIMPIOS (DESACTIVADOS) ---
PERFILES = {}
perfil_actual = "LUNES"


app_html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
      
         
        /* Efecto de iluminación al pasar el mouse por las filas */
        tr.master-row:hover, tr.calc-row:hover {{
            background-color: #fffecd !important;
            box-shadow: inset 0 0 2px #ffc107 !important;
            transition: background-color 0.15s ease, box-shadow 0.15s ease;
            cursor: pointer;
        }}


        /* Opcional: Para asegurar que el texto no se pierda al iluminar */
tr.master-row:hover td, tr.calc-row:hover td {{
    color: #000 !important; /* Asegura que el texto sea oscuro sobre el fondo amarillo */
}}


/* 📊 CONTADOR EXCLUSIVO PESTAÑA SCP1 */
        #mi-contador-scp1 {{
            position: fixed;
            top: 156px; 
            right: 20px; 
            background: rgba(37, 40, 43, 0.98); 
            color: #ffffff; 
            padding: 16px; 
            border-radius: 10px; 
            z-index: 999999; 
            font-family: sans-serif;
            font-size: 14px;
            box-shadow: 0 6px 18px rgba(0,0,0,0.6);
            border: 1.2px solid transparent;
            width: 300px;
            max-height: 410px;
            overflow-y: auto;
            pointer-events: auto;
            display: block;
        }}

        /* 📊 CONTADOR EXCLUSIVO PESTAÑA SJA1 */
        #mi-contador-sja1 {{
            position: fixed;
            top: 156px; 
            right: 20px; 
            background: rgba(37, 40, 43, 0.98); 
            color: #ffffff; 
            padding: 16px; 
            border-radius: 10px; 
            z-index: 999999; 
            font-family: sans-serif;
            font-size: 14px;
            box-shadow: 0 6px 18px rgba(0,0,0,0.6);
            border: 1.2px solid transparent;
            width: 350px;
            max-height: 210px;
            overflow-y: auto;
            pointer-events: auto;
            display: none;
        }}

        .cont-item {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid rgba(255,255,255,0.15);
            padding: 8px 0;
        }}

        .cont-item:last-child {{
            border-bottom: none;
        }}

        .cont-name {{
            font-weight: normal;
            color: #D3D3D3;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            max-width: 150px;
            font-size: 14px;
        }}

        .cont-vals {{
            font-family: monospace;
            font-weight: bold;
            text-align: right;
            font-size: 14px;
        }}





        /* Redondear botones de +/- para que parezcan botones 3D físicos */
        .poligono-bloque button {{
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            transition: all 0.1s;
        }}

        .poligono-bloque button:active {{
            box-shadow: 0 0px 0px transparent;
            transform: translateY(1px); /* Se hunde al presionar */
        }}

         /* Efecto de hundimiento para botones de filtro (ACTIVAS/TODAS) */
.filter-btn:active {{
    transform: translateY(4px); 
    box-shadow: none !important;
}}  


/* 🔥 NUEVO: Color verde suave cuando la fila de polígono esté completada (OK) */
        tr.fila-ok {{
            background-color: #e8f5e9 !important; /* Verde pastel muy limpio */
            transition: background-color 0.3s ease;
        }}
        /* Mantiene el texto y celdas legibles en tonos verdes operativos */
        tr.fila-ok td {{
            color: #1b5e20 !important;
        }}
        

    </style>
    
</head>

    <style>
body {{ font-family: sans-serif; background: #ffffff; padding: 14px; }}
/* 1. ESTO EVITA QUE LA TABLA SE PEGUE AL CONTADOR FLOTANTE */
#visor {{
    margin-right: 250px !important; /* Deja espacio vacío a la derecha */
}}

/* 2. TABLA AL 100% PARA QUE NO SE VEA CORTADA */
.meli-table {{
    width: 100% !important; 
    border-collapse: collapse !important;
    border-spacing: 0 !important;
    table-layout: fixed;
    background: white;
    border: 1px solid #25282b;
    box-shadow: none !important;
    border-radius: 0 !important;
    overflow: hidden;
}}

.meli-table th {{
    background: #f3f3f3 !important;
    color: #222 !important;
    font-size: 14px;
    font-weight: 600;
    border: 1px solid #25282b !important;
    padding: 4px 6px;
    text-align: center;
    height: 24px;
}}

/* Quitar el borde derecho del último elemento (OK) para no chocar con el borde externo */
.meli-table th:last-child {{
    border-right: 2 !important;
}}

/* Asegurar que la tabla mantenga su borde externo principal */
.meli-table {{
    border: none !important;
    border-collapse: separate !important;
    border-spacing: 0 !important;
}}

.meli-table td {{
    border: 1px solid #25282b;
    padding: 2px 4px;
    font-size: 14px;
    height: 24px;
    background: white;
    color: #25282b;
}}



/* ===== MODO FLOTANTE PERFECTAMENTE CENTRADO ===== */
#fleet-sticky.fleet-floating {{
  position: fixed !important;
  top: 170px;
  left: 50% !important;
  transform: translateX(-50%);
  width: min(1050px, 92vw) !important;
  max-height: 370px !important;
  overflow: hidden !important;
  z-index: 999999 !important;
  background: #ffffff !important;
  border: 3px solid #25282b !important;
  border-radius: 10px !important;
  box-shadow: 0 10px 30px rgba(0,0,0,0.50) !important;
  padding: 6px !important;
  margin: 0 !important;
}}

/* Muestra la barra superior de agarre al estar flotando */
#fleet-sticky.fleet-floating #handle-moverse-flotante {{
  display: block !important;
}}

/* Muestra la tabla limpia con scroll y oculta botones que estén dentro de las celdas */
#fleet-sticky.fleet-floating .t-content {{
  max-height: 320px !important;
  overflow: auto !important;
}}

#fleet-sticky.fleet-floating .t-content button {{
  display: none !important;
}}

/* Panel en modo NORMAL */
#fleet-sticky.fleet-normal {{
  position: static !important;
  transform: none !important;
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
  padding: 0 !important;
}}





/* El efecto Neomórfico en cada fila */
        .master-row {{ 
            border-radius: 9px;
            box-shadow: 1px 1px 5px #ededed, -2px -2px 6px #efefef;
            transition: all 0.2s ease;
        }}

/* Redondear las esquinas de las filas */
        .meli-table td:first-child {{ border-radius: 3px 0 0 3px; }}
        .meli-table td:last-child {{ border-radius: 0 3px 3px 0; }}

        
        #google-alert {{ 
            position: fixed; top: -100px; left: 50%; transform: translateX(-50%);
            background: #d32f2f; color: white; padding: 15px 25px; border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3); transition: 0.4s; z-index: 10000;
        }}
        #google-alert.show {{ top: 20px; }}
/* Pestañas Modernas con Volumen */
.tab-btn {{ 
    padding: 10px 12px; 
    cursor: pointer; 
    border: 1px solid #25282b; 
    background: linear-gradient(180deg, #f0f0f0 0%, #dcdcdc 100%); /* Efecto 3D de relieve */
    border-radius: 8px 8px 0 0; 
    font-weight: bold; 
    font-size: 13px;
    color: #25282b;
    transition: all 0.2s ease;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.8), 0 2px 4px rgba(0,0,0,0.1);
    margin-right: 2px;
    outline: none;
}}

/* Efecto al pasar el mouse (Hover) */
.tab-btn:hover {{ 
    background: linear-gradient(180deg, #ffffff 0%, #f8fbff 100%);
    color: #25282b;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    transform: translateY(-2px); /* Se levanta un poco */
}}

/* Pestaña Activa (Seleccionada) */
.tab-btn.active {{
    background: linear-gradient(180deg, #424242 0%, #25282b 100%) !important;
    color: #ffffff !important; 
    border: 1px solid #061821 !important;
    box-shadow: inset 0 2px 5px rgba(0,0,0,0.3);
    transform: translateY(0); /* Se queda pegada abajo */
}}        .tab-btn.active {{ background: #333; color: white; }}
        
        .tools-panel {{ display: flex; flex-direction: column; gap: 10px; margin-top: 15px; }}
        .google-tool {{ background: linear-gradient(145deg, #ffffff, #DDA0DD); padding: 15px; border-radius: 15px; border: 1px solid #25282b; text-align: center; box-shadow: 5px 5px 15px #d1d1d1, -5px -5px 15px #ffffff; transition: transform 0.2s;}}
        .google-tool:hover {{
            transform: translateY(-3px);
        }}
        .google-tool input {{
            border-radius: 8px;
            border: 1px solid #25282b;
            padding: 5px;
            font-size: 16px;
            outline: none;
            box-shadow: inset 2px 2px 5px #d9dbde;
        }}

        
       /* CALCULADORA CON RESPLANDOR NEÓN */
        #calc_wrapper {{ background: #22c5bc; border-radius: 20px; padding: 15px; border: transparent; outline: none; transition: 0.3s; }}
        #calc_wrapper:focus {{ box-shadow: 0 0 20px #FF00FF, 0 0 40px #FF00FF; border: 2px solid #FF00FF; }}
        
        #calc_display_box {{ background: #fffacd; border-radius: 10px; padding: 10px; text-align: right; margin-bottom: 10px; min-height: 60px; }}
        .calc-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 5px; }}
        .btn-c {{ background: white; border: none; font-weight: bold; border-radius: 8px; padding: 12px; cursor: pointer; box-shadow: 0 3px #ccc; font-size: 14px; }}
        .btn-c-eq {{ background: #FF00FF; color: white; border: none; border-radius: 8px; cursor: pointer; font-weight: bold; font-size: 14px; }}
        .crono-card {{ background: #1c1c1c; border-radius: 12px; padding: 15px; color: white; font-family: sans-serif; text-align: center; }}
        /* Botones con un relieve sutil */
        .btn-c {{
            background: #f0f0f0; 
            border: none; 
            font-weight: bold; 
            border-radius: 12px; 
            padding: 12px; 
            cursor: pointer; 
            /* Sombra pequeña para que cada botón destaque */
            box-shadow: 3px 3px 6px #1da39b, -2px -2px 5px #27ebd2;
            transition: transform 0.1s;
        }}

        /* Efecto de "clic" real */
        .btn-c:active {{
            transform: scale(0.95);
            box-shadow: inset 2px 2px 5px #b1b1b1;
        }}


   /* FORZADO ULTRA-COMPACTO PARA LA FILA DE ESTADO */

/* SELECTOR DE ALTA ESPECIFICIDAD PARA LA FILA DE ESTADO */
html body .meli-table tbody tr:last-child td {{
    height: 25px !important;       /* Altura sin reducción */
    min-height: 25px !important;   /* Elimina restricciones */
    max-height: 20px !important;   /* Bloquea el crecimiento */
    padding-top: 2px !important;
    padding-bottom: 3px !important;
    line-height: 25px !important;  /* Centra el texto en el nuevo alto */
    font-size: 14px !important;    /* Reduce un poco la letra */
}}

/* Forzar que la fila misma no tenga altura mínima */
html body .meli-table tbody tr:last-child {{
    height: 16px !important;
}}


/* Colores y sombras (la sombra da el efecto de grosor) */
.btn-start {{ background: #28a745; color: white; box-shadow: 0 5px 0 #1e7e34; }}
.btn-stop  {{ background: #ffc107; color: #333;  box-shadow: 0 5px 0 #d39e00; }}
.btn-reset {{ background: #dc3545; color: white; box-shadow: 0 5px 0 #bd2130; }}

/* EFECTO DE CLIC (REACCIÓN) */
.crono-card button:active {{
    transform: translateY(4px); /* El botón baja físicamente */
    box-shadow: 0 1px 0 #333;   /* La sombra se reduce, pareciendo que se hunde */
}}

/* Efecto Hover (brillo sutil al pasar el mouse) */
.crono-card button:hover {{
    filter: brightness(1.1);
}}

/* Ajuste específico para los encabezados de Polígonos */
#body-plan-container th, 
.meli-table:nth-of-type(2) th {{
    font-size: 22px !important;    /* Tamaño de la letra */
    height: 90px !important;      /* Alto de la celda */
    padding: 11px 6px !important; /* Espacio interno */
    vertical-align: middle !important;
}}




/* ===== MODO EXCEL CORREGIDO ===== */ 

body.excel-view #fleet-float,
body.excel-view #ruteo-float,
body.excel-view .tools-panel,
body.excel-view #btn-excel-view {{
    display: none !important;
}}

/* TABLAS MODO EXCEL: Encabezados compactos y datos legibles */
body.excel-view .meli-table td {{
    padding: 2px 3px !important;
    font-size: 14px !important; /* Datos legibles de 14px */
}}

body.excel-view .meli-table th {{
    padding: 2px 1px !important;       
    font-size: 11px !important;        
    letter-spacing: -0.3px !important; 
    overflow: hidden !important;
    line-height: 1.0 !important;        /* Hace que las dos líneas estén muy juntas y ordenadas */
    vertical-align: middle !important;
}}


/* ===== TOTAL RUTEADAS EN VISTA EXCEL (más grande y visible) ===== */
body.excel-view .meli-table tfoot.fila-total td {{
    font-size: 16px !important;   /* tamaño letra */
    padding: 6px 8px !important;  /* alto de la fila */
    line-height: 18px !important;
    font-weight: 900 !important;
}}

body.excel-view .meli-table tfoot.fila-total td[id^="total-ruteadas-"] {{
    font-size: 20px !important;   /* tamaño del número */
    font-weight: 900 !important;
    color: #66CDAA !important;
    text-align: center !important;
}}


/* ===== POLÍGONOS MODO EXCEL (FORZADO) ===== */

body.excel-view .poligono-bloque table {{
    border-collapse: collapse !important;
    width: 120% !important;
    table-layout: fixed !important; /* Mantiene las columnas bajo control estricto */
}}

body.excel-view .poligono-bloque td, 
body.excel-view .poligono-bloque th {{
    padding: 8px 3px !important;    /* Aumentamos el primer valor (6px) para dar altura */
    height: 60px !important;        /* Forzamos una altura de fila más cómoda */
    font-size: 13px !important;     /* Subimos un pelín la letra para que se lea bien */
    overflow: hidden !important;
    white-space: nowrap !important;
    text-overflow: ellipsis !important;
    text-align: center !important;
    vertical-align: middle !important;
}}

/* Fuerza anchos mínimos para las columnas críticas */
body.excel-view .poligono-bloque th:nth-child(5) {{ width: 90px !important; }} /* SCHEDULE */
body.excel-view .poligono-bloque th:nth-child(6) {{ width: 55px !important; }} /* USADAS */
body.excel-view .poligono-bloque th:nth-child(7) {{ width: 45px !important; }} /* DELTA */

</style> 
</head>





<div id="google-alert">⚠️ <span id="alert-msg"></span> [ENTER para cerrar]</div>
<div style="display:flex; flex-direction:column; gap:20px; width:100%;">






    <!-- COLUMNA DERECHA --> 


<!-- PANEL SUPERIOR -->
<div style="
    width:100%;
    padding:0;
    margin-bottom:10px;
">

        <div style="background-color: #25282b; color: white; padding: 10px; border-radius: 2px; font-weight: bold; text-align: center; margin-bottom: 10px;">🚚 🚚 DISPONIBILIDAD DE FLOTA 🚛 🚛</div>
    


<div id="panel-control-unico" style="display: flex; gap: 20px; background: #25282b; padding: 15px; border-radius: 10px; color: white; justify-content: center; align-items: center; margin: 20px 0;">
    <div style="text-align: center;">
        <div id="hora-actual" style="font-size: 22px; font-weight: bold;">00:00:00</div>
        <div style="font-size: 9px; color: #26d0ff; letter-spacing: 1px;">HORA ACTUAL</div>
    </div>
    <div style="text-align: center; border-left: 1px solid #ffffff; padding-left: 20px; min-width: 120px;">
        <div id="proximo-ruteo" style="font-size: 16px; font-weight: bold; color: #ff9b21; line-height: 1.1;">Sin tareas</div>
        <div id="hora-ruteo" style="font-size: 14px; font-weight: bold; color: #ffffff; margin-top: 2px;">--</div>
        <div style="font-size: 9px; color: #d0d0d0; letter-spacing: 1px; margin-top: 2px;">SIGUIENTE RUTEO</div>
    </div>
    <div style="text-align: center; border-left: 1px solid #ffffff; padding-left: 20px;">
        <div id="cuenta-regresiva" style="font-size: 22px; font-weight: bold; color: #7CFFB2;">00:00</div>
        <div style="font-size: 9px; color: #d0d0d0; letter-spacing: 1px;">TIEMPO RESTANTE</div>
    </div>
</div>

        <div id="resumen-flota-ruteada" style="display: flex; gap: 15px; margin: 15px 0; justify-content: center;">
        <div style="background: #d7e5fa; padding: 8px; border-radius: 5px; border: 1px solid #bbdefb; text-align: center; width: 100px;">
            <div style="font-size: 10px; font-weight: bold; color: #0861c7;">MLP</div>
            <div id="val-mlp-rute-2" style="font-size: 14px; font-weight: bold;">0</div>
        </div>
        <div style="background: #c6f7f3; padding: 8px; border-radius: 5px; border: 1px solid #68b0ac; text-align: center; width: 100px;">
            <div style="font-size: 10px; font-weight: bold; color: #12736d;">RENTAL</div>
            <div id="val-rental-rute-2" style="font-size: 14px; font-weight: bold;">0</div>
        </div>
        <div style="background: #d3f5d3; padding: 8px; border-radius: 5px; border: 1px solid #90EE90; text-align: center; width: 100px;">
            <div style="font-size: 10px; font-weight: bold; color: #209626;">CAR</div>
            <div id="val-car-rute-2" style="font-size: 14px; font-weight: bold;">0</div>
        </div>
    </div>


<div id="dos-pct-global"
     style="
        background:#f5f5f5;
        border:1px solid #d0d0d0;
        border-radius:6px;
        padding:6px;
        margin-bottom:10px;
        text-align:center;
        font-weight:bold;
        color:#25282b;">
</div>



<!-- 1. BOTONES SUPERIORES (SE QUEDAN SIEMPRE FIJOS ATRÁS) -->
<div id="fleet-drag-handle" style="display: flex; justify-content: center; align-items: center; gap: 8px; flex-wrap: wrap; padding: 4px 0; margin-bottom: 8px;">
    
    <button id="fleet-toggle-btn"
      onclick="toggleFleetFloating();"
      style="cursor:pointer; border:none; background:#25282b; color:white; padding:4px 9px; border-radius:6px; font-weight:bold; font-size:12px; box-shadow:0 2px 0 #111213; outline:none;">
      FLOTAR ☁️
    </button>

    <div class="btn-tooltip-container">
        <button id="excel-btn" onclick="toggleExcelView()" title="VISTA EXCEL"
            style="cursor:pointer; background:#228B22; color:white; border:none; font-size:12px; padding:4px 9px; border-radius:6px; font-weight:bold; box-shadow:0 2px 0 #1c6d1c; outline:none;">
            VISTA EXCEL
        </button>
    </div>

    <button onclick="distribuirAutomatico()" 
        style="cursor:pointer; background: #26d4ca; color: #2e3030; border: none; font-size: 12px; padding: 4px 9px; border-radius: 6px; font-weight: bold; box-shadow: 0 2px 0 #2d968f; outline: none;">
        🧠 AUTO-CALCULAR
    </button>
    
    <button class="filter-btn" onclick="filterRows(true)" 
        style="cursor:pointer; background: linear-gradient(180deg, #4f4f4f 0%, #25282b 100%); color: white; border: 1px solid #25282b; font-size: 12px; padding: 4px 9px; border-radius: 6px; font-weight: bold; outline: none;">
        ACTIVAS
    </button>

    <button class="filter-btn" onclick="filterRows(false)" 
        style="cursor:pointer; background: #808080; color:white; border:none; font-size:12px; padding:4px 9px; border-radius:6px; font-weight:bold; outline: none;">
        TODAS
    </button>

</div>



<!-- 3. CONTENEDOR EXCLUSIVO PARA LA TABLA QUE SÍ VA A FLOTAR -->
<div id="fleet-sticky" class="fleet-normal">

  <!-- Barrita con evento pointerdown nativo para soltado perfecto -->
  <div id="handle-moverse-flotante" 
       onpointerdown="iniciarArrastreFlotante(event)"
       style="display:none; width:100%; height:28px; background:#343a40; color:#ffffff; font-size:11px; font-weight:bold; line-height:28px; border-radius:6px 6px 0 0; margin:-6px -6px 6px -6px; cursor:grab; user-select:none; z-index:9999999; position:relative; padding:0 8px; box-sizing:border-box; touch-action:none;">
    
    <span style="float:left;">:: CLIC Y ARRASTRA AQUÍ PARA MOVER ::</span>
    
    <button onclick="toggleFleetFloating();" 
            onpointerdown="event.stopPropagation();"
            style="float:right; margin-top:3px; cursor:pointer; background:#dc3545; color:white; border:none; padding:2px 8px; border-radius:4px; font-size:10px; font-weight:bold; outline:none;">
      ✕ NORMAL (enter)
    </button>
    
    <div style="clear:both;"></div>
  </div>

  <!-- AQUÍ SIGUEN TODAS TUS TABLAS (tab-2, tab-6, tab-7, etc.) SIN CAMBIOS -->



<!-- AQUÍ PEGAS EL NUEVO SELECTOR DESPLEGABLE -->
<div style="margin: 10px 0; text-align: center;">
    <select id="ciclo-selector" onchange="cambiarCiclo(this.value)" style="
        background: #FFFFFF;
        color: #000000;
        border: 2px solid #242526;
        padding: 8px 15px;
        border-radius: 4px;
        font-size: 14px;
        font-weight: bold;
        outline: none;
        cursor: pointer;
        width: 250px;
        text-align-last: center;
    ">
        <option value="2">🟠 C1 SCP1</option>
        <option value="6">🔴 C1 SJA1</option>
        <option value="7">🔴 C1 SCH1</option>
        <option value="8">🔴 C1 SMD1</option>
        <option value="1">🟡 PREC SMX5</option>
        <option value="5">🟡 PREC SMX2</option>
        <option value="4" selected>🟢 EXTENDIDO</option> <!-- AQUÍ AGREGAS 'selected' -->
        <option value="9">🟣 C1 VACÍA</option>
</select>
</div>




  <!-- TABLAS DE DISPONIBILIDAD INTEGRADAS DENTRO DE FLEET-STICKY -->
  <div id="tab-2" class="t-content" style="display:none;">
      <table class="meli-table" style="width: 100%; table-layout: fixed; border-collapse: collapse;">
          <thead>
              <tr style="background: linear-gradient(180deg, #0a2e42 0%, #25282b 100%); color: white;">
                  <th style="border-right: 0.5px solid #25282b; padding: 4px 8px; font-size: 14px; color: #25282b !important;">UNIDAD</th>
                  <th colspan="2" style="border-right: 0.5px solid #25282b; padding: 2px; font-size: 11px; color: #25282b !important; width: 105px;">ORH</th>
                  <th style="border-right: 0.5px solid #25282b; padding: 2px; font-size: 11px; color: #25282b !important; width: 45px;">% OCUP</th>
                  <th style="border-right: 0.5px solid #25282b; padding: 2px; font-size: 11px; color: #25282b !important; width: 45px;">SPR<br>MIN</th>
                  <th style="border-right: 0.5px solid #25282b; padding: 2px; font-size: 11px; color: #25282b !important; width: 45px;">SPR<br>MAX</th>
                  <th style="border-right:0.5px solid #25282b; padding:4px 8px; font-size:11px; color:#25282b !important; width:60px;">SCHEDULE</th>
                  <th style="border-right:0.7px solid #25282b; padding:4px 9px; font-size:11px; color:#25282b !important; width:57px; text-align:center; display:table-cell; vertical-align:middle;">USADAS</th>
                  <th style="border-right:0.5px solid #25282b; padding:4px 8px; font-size:11px; color:#25282b !important; width:50px;">DELTA</th>
              </tr>
          </thead>
          <tbody id="body-2">{gen_master_rows(u_C1, 2)}</tbody>
          <tfoot class="fila-total">
              <tr class="fila-total">
                  <td style="border:none;"></td>
                  <td colspan="6" style="padding:6px; text-align:right;">🚛 TOTAL RUTEADAS</td>
                  <td id="total-ruteadas-2" style="text-align:center; color:#3CB371; font-size:16px; font-weight:bold;">0</td>
              </tr>
          </tfoot>
      </table>
  </div>

  <div id="tab-6" class="t-content" style="display:none;">
      <table class="meli-table" style="width: 100%; table-layout: fixed; border-collapse: collapse;">
          <thead>
              <tr style="background: linear-gradient(180deg, #0a2e42 0%, #25282b 100%); color: white;">
                  <th style="border-right: 0.5px solid #25282b; padding: 4px 8px; font-size: 14px; color: #25282b !important;">UNIDAD</th>
                  <th colspan="2" style="border-right: 0.5px solid #25282b; padding: 2px; font-size: 11px; color: #25282b !important; width: 105px;">ORH</th>
                  <th style="border-right: 0.5px solid #25282b; padding: 2px; font-size: 11px; color: #25282b !important; width: 45px;">% OCUP</th>
                  <th style="border-right: 0.5px solid #25282b; padding: 2px; font-size: 11px; color: #25282b !important; width: 45px;">SPR<br>MIN</th>
                  <th style="border-right: 0.5px solid #25282b; padding: 2px; font-size: 11px; color: #25282b !important; width: 45px;">SPR<br>MAX</th>
                  <th style="border-right:0.5px solid #25282b; padding:4px 8px; font-size:11px; color:#25282b !important; width:60px;">SCHEDULE</th>
                  <th style="border-right:0.7px solid #25282b; padding:4px 9px; font-size:11px; color:#25282b !important; width:57px; text-align:center; display:table-cell; vertical-align:middle;">USADAS</th>
                  <th style="border-right:0.5px solid #25282b; padding:4px 8px; font-size:11px; color:#25282b !important; width:50px;">DELTA</th>
              </tr>
          </thead>
          <tbody id="body-6">{gen_master_rows(u_C1_SJA1, 6)}</tbody>
          <tfoot class="fila-total"> 
              <tr class="fila-total">
                  <td style="border:none;"></td>
                  <td colspan="6" style="padding:6px; text-align:right;">🚛 TOTAL RUTEADAS</td>
                  <td id="total-ruteadas-6" style="text-align:center; color:#3CB371; font-size:16px; font-weight:bold !important;">0</td>
              </tr>
          </tfoot>
      </table>
  </div>



<div id="tab-7" class="t-content" style="display:none;">
    <table class="meli-table" style="width: 100%; table-layout: fixed; border-collapse: collapse;">
        <thead>
            <tr style="background: linear-gradient(180deg, #0a2e42 0%, #25282b 100%); color: white;">
                  <th style="border-right: 0.5px solid #25282b; padding: 4px 8px; font-size: 14px; color: #25282b !important;">UNIDAD</th>
                  <th colspan="2" style="border-right: 0.5px solid #25282b; padding: 2px; font-size: 11px; color: #25282b !important; width: 105px;">ORH</th>
                  <th style="border-right: 0.5px solid #25282b; padding: 2px; font-size: 11px; color: #25282b !important; width: 45px;">% OCUP</th>
                  <th style="border-right: 0.5px solid #25282b; padding: 2px; font-size: 11px; color: #25282b !important; width: 45px;">SPR<br>MIN</th>
                  <th style="border-right: 0.5px solid #25282b; padding: 2px; font-size: 11px; color: #25282b !important; width: 45px;">SPR<br>MAX</th>
                  <th style="border-right:0.5px solid #25282b; padding:4px 8px; font-size:11px; color:#25282b !important; width:60px;">SCHEDULE</th>
                  <th style="border-right:0.7px solid #25282b; padding:4px 9px; font-size:11px; color:#25282b !important; width:57px; text-align:center; display:table-cell; vertical-align:middle;">USADAS</th>
                  <th style="border-right:0.5px solid #25282b; padding:4px 8px; font-size:11px; color:#25282b !important; width:50px;">DELTA</th>
              </tr>
        </thead>
        <tbody id="body-7">{gen_master_rows(u_C1_SCH1, 7)}</tbody>
        <tfoot class="fila-total"> 
    <tr class="fila-total">
        <td style="border:none;"></td>
        <td colspan="6" style="padding:6px; text-align:right;">🚛 TOTAL RUTEADAS</td>
        <td id="total-ruteadas-7" style="text-align:center; color:#3CB371; font-size:16px; font-weight:bold !important;">0</td>
    </tr>
</tfoot>
    </table>
</div>


<div id="tab-8" class="t-content" style="display:none;">
    <table class="meli-table" style="width: 100%; table-layout: fixed; border-collapse: collapse;">
        <thead>
            <tr style="background: linear-gradient(180deg, #0a2e42 0%, #25282b 100%); color: white;">
                  <th style="border-right: 0.5px solid #25282b; padding: 4px 8px; font-size: 14px; color: #25282b !important;">UNIDAD</th>
                  <th colspan="2" style="border-right: 0.5px solid #25282b; padding: 2px; font-size: 11px; color: #25282b !important; width: 105px;">ORH</th>
                  <th style="border-right: 0.5px solid #25282b; padding: 2px; font-size: 11px; color: #25282b !important; width: 45px;">% OCUP</th>
                  <th style="border-right: 0.5px solid #25282b; padding: 2px; font-size: 11px; color: #25282b !important; width: 45px;">SPR<br>MIN</th>
                  <th style="border-right: 0.5px solid #25282b; padding: 2px; font-size: 11px; color: #25282b !important; width: 45px;">SPR<br>MAX</th>
                  <th style="border-right:0.5px solid #25282b; padding:4px 8px; font-size:11px; color:#25282b !important; width:60px;">SCHEDULE</th>
                  <th style="border-right:0.7px solid #25282b; padding:4px 9px; font-size:11px; color:#25282b !important; width:57px; text-align:center; display:table-cell; vertical-align:middle;">USADAS</th>
                  <th style="border-right:0.5px solid #25282b; padding:4px 8px; font-size:11px; color:#25282b !important; width:50px;">DELTA</th>
              </tr>
        </thead>
        <tbody id="body-8">{gen_master_rows(u_C1_SMD1, 8)}</tbody>
        <tfoot class="fila-total"> 
    <tr class="fila-total">
        <td style="border:none;"></td>
        <td colspan="6" style="padding:6px; text-align:right;">🚛 TOTAL RUTEADAS</td>
        <td id="total-ruteadas-8" style="text-align:center; color:#3CB371; font-size:16px; font-weight:bold !important;">0</td>
    </tr>
</tfoot>
    </table>
</div>




  <div id="tab-1" class="t-content" style="display:none;">
      <table class="meli-table" style="width: 100%; table-layout: fixed; border-collapse: collapse;">
          <thead>
              <tr style="background: linear-gradient(180deg, #0a2e42 0%, #25282b 100%); color: white;">
                  <th style="border-right: 0.5px solid #25282b; padding: 4px 8px; font-size: 14px; color: #25282b !important;">UNIDAD</th>
                  <th colspan="2" style="border-right: 0.5px solid #25282b; padding: 2px; font-size: 11px; color: #25282b !important; width: 105px;">ORH</th>
                  <th style="border-right: 0.5px solid #25282b; padding: 2px; font-size: 11px; color: #25282b !important; width: 45px;">% OCUP</th>
                  <th style="border-right: 0.5px solid #25282b; padding: 2px; font-size: 11px; color: #25282b !important; width: 45px;">SPR<br>MIN</th>
                  <th style="border-right: 0.5px solid #25282b; padding: 2px; font-size: 11px; color: #25282b !important; width: 45px;">SPR<br>MAX</th>
                  <th style="border-right:0.5px solid #25282b; padding:4px 8px; font-size:11px; color: #25282b !important; width:60px;">SCHEDULE</th>
                  <th style="border-right:0.7px solid #25282b; padding:4px 9px; font-size:11px; color:#25282b !important; width:57px; text-align:center; display:table-cell; vertical-align:middle;">USADAS</th>
                  <th style="border-right:0.5px solid #25282b; padding:4px 8px; font-size:11px; color: #25282b !important; width:50px;">DELTA</th>
              </tr>
          </thead>
          <tbody id="body-1">{gen_master_rows(u_PREC, 1)}</tbody>
          <tfoot class="fila-total">
              <tr class="fila-total">
                  <td style="border:none;"></td>
                  <td colspan="6" style="padding:6px; text-align:right;">🚛 TOTAL RUTEADAS</td>
                  <td id="total-car-real-1" style="text-align:center; color:#3CB371; font-size:16px; font-weight:bold;">0</td>
              </tr>
          </tfoot>
      </table>
  </div>

  <div id="tab-5" class="t-content" style="display:none;">
      <table class="meli-table" style="width: 100%; table-layout: fixed; border-collapse: collapse;">
          <thead>
              <tr style="background: linear-gradient(180deg, #0a2e42 0%, #25282b 100%); color: white;">
                  <th style="border-right: 0.5px solid #25282b; padding: 4px 8px; font-size: 14px; color: #25282b !important;">UNIDAD</th>
                  <th colspan="2" style="border-right: 0.5px solid #25282b; padding: 2px; font-size: 11px; color: #25282b !important; width: 105px;">ORH</th>
                  <th style="border-right: 0.5px solid #25282b; padding: 2px; font-size: 11px; color: #25282b !important; width: 45px;">% OCUP</th>
                  <th style="border-right: 0.5px solid #25282b; padding: 2px; font-size: 11px; color: #25282b !important; width: 45px;">SPR<br>MIN</th>
                  <th style="border-right: 0.5px solid #25282b; padding: 2px; font-size: 11px; color: #25282b !important; width: 45px;">SPR<br>MAX</th>
                  <th style="border-right:0.5px solid #25282b; padding:4px 8px; font-size:11px; color: #25282b !important; width:60px;">SCHEDULE</th>
                  <th style="border-right:0.7px solid #25282b; padding:4px 9px; font-size:11px; color:#25282b !important; width:57px; text-align:center; display:table-cell; vertical-align:middle;">USADAS</th>
                  <th style="border-right:0.5px solid #25282b; padding:4px 8px; font-size:11px; color: #25282b !important; width:50px;">DELTA</th>
              </tr>
          </thead>
          <tbody id="body-5">{gen_master_rows(u_PREC_SMX2, 5)}</tbody>
          <tfoot class="fila-total">
              <tr class="fila-total">
                  <td style="border:none;"></td>
                  <td colspan="6" style="padding:6px; text-align:right;">🚛 TOTAL RUTEADAS</td>
                  <td id="total-car-real-5" style="text-align:center; color:#3CB371; font-size:16px; font-weight:bold;">0</td>
              </tr>
          </tfoot>
      </table>
  </div>

  <div id="tab-4" class="t-content">
      <table class="meli-table" style="width: 100%; table-layout: fixed; border-collapse: collapse;">
          <thead>
              <tr style="background: linear-gradient(180deg, #0a2e42 0%, #25282b 100%); color: white;">
                  <th style="border-right: 0.5px solid #25282b; padding: 4px 8px; font-size: 14px; color: #25282b !important;">UNIDAD</th>
                  <th style="border-right: 0.5px solid #25282b; padding: 2px; font-size: 11px; color: #25282b !important; width: 45px;">SPR<br>MIN</th>
                  <th style="border-right: 0.5px solid #25282b; padding: 2px; font-size: 11px; color: #25282b !important; width: 45px;">SPR<br>MAX</th>
                  <th style="border-right:0.5px solid #25282b; padding:4px 8px; font-size:11px; color: #25282b !important; width:60px;">SCHEDULE</th>
                  <th style="border-right:0.7px solid #25282b; padding:4px 9px; font-size:11px; color:#25282b !important; width:57px; text-align:center; display:table-cell; vertical-align:middle;">USADAS</th>
                  <th style="border-right:0.5px solid #25282b; padding:4px 8px; font-size:11px; color: #25282b !important; width:50px;">DELTA</th>
              </tr>
          </thead>
          <tbody id="body-4">{gen_master_rows(u_SDE, 4)}</tbody>
          <tfoot class="fila-total">
              <tr class="fila-total">
                  <td style="border:none;"></td>
                  <td colspan="3" style="padding:6px; text-align:right;">🚛 TOTAL RUTEADAS</td>
                  <td id="total-car-real-4" style="text-align:center; color:#3CB371; font-size:16px; font-weight:bold;">0</td>
              </tr>
          </tfoot>
      </table>
  </div>



<!-- TABLA FLOTA C1 VACÍA (ID 9) -->
<div id="tab-9" class="t-content" style="display:none;">
    <table class="meli-table">
        <thead>
            <tr style="background: linear-gradient(180deg, #0a2e42 0%, #25282b 100%); color: white;">
                  <th style="border-right: 0.5px solid #25282b; padding: 4px 8px; font-size: 14px; color: #25282b !important;">UNIDAD</th>
                  <th colspan="2" style="border-right: 0.5px solid #25282b; padding: 2px; font-size: 11px; color: #25282b !important; width: 105px;">ORH</th>
                  <th style="border-right: 0.5px solid #25282b; padding: 2px; font-size: 11px; color: #25282b !important; width: 45px;">% OCUP</th>
                  <th style="border-right: 0.5px solid #25282b; padding: 2px; font-size: 11px; color: #25282b !important; width: 45px;">SPR<br>MIN</th>
                  <th style="border-right: 0.5px solid #25282b; padding: 2px; font-size: 11px; color: #25282b !important; width: 45px;">SPR<br>MAX</th>
                  <th style="border-right:0.5px solid #25282b; padding:4px 8px; font-size:11px; color:#25282b !important; width:60px;">SCHEDULE</th>
                  <th style="border-right:0.7px solid #25282b; padding:4px 9px; font-size:11px; color:#25282b !important; width:57px; text-align:center; display:table-cell; vertical-align:middle;">USADAS</th>
                  <th style="border-right:0.5px solid #25282b; padding:4px 8px; font-size:11px; color:#25282b !important; width:50px;">DELTA</th>
              </tr>
        </thead>
        <tbody id="body-9">{gen_master_rows(u_C1_VACIA, 9)}</tbody>
        <tfoot class="fila-total">
            <tr class="fila-total">
                <td style="border:none;"></td>
                <td colspan="6" style="padding:6px; text-align:right;">🚛 TOTAL RUTEADAS</td>
                <td id="total-ruteadas-9" style="text-align:center; color:#3CB371; font-size:16px; font-weight:bold;">0</td>
            </tr>
        </tfoot>
    </table>
</div>


</div> <!-- CIERRE CORRECTO DEL PANEL FLOTANTE FLEET-STICKY -->

        
        
            
                <button id="toggle-tools-btn" onclick="toggleTools()" 
        style="display: none !important; 
               background:#25282b !important; 
               background-image: none !important; 
               box-shadow: none !important; 
               color: #ffffff !important; 
               border: 1px solid #4682B4; 
           font-size: 11px; 
           padding: 5px 0; 
           border-radius: 3px; 
           font-weight: bold; 
           outline: none; 
           width: 100%; 
           margin-bottom: 15px;">
    ❌ OCULTAR UTILERÍAS
</button>




                <!--
                <div style="font-weight:bold; color:#25282b; margin-bottom:10px; font-size:12px; letter-spacing:1px;">⏱️ CONVERTIDOR DE TIEMPO</div>
                <input type="number" id="min-in" placeholder="Minutos" style="width:80px; text-align:center;" oninput="convertTime()">
                <div style="margin-top:10px;">
                    <span id="time-res" style="font-size: 24px; font-weight: bold; color: #FF4500;">0h 0m</span>
                 </div>
             </div>
        </div>
    </div>
</div>
-->




<!-- COLUMNA IZQUIERDA -->


<!-- PLANNERS -->
<div style="
    width:100%;
    overflow-y:auto;
    overflow-x:hidden;
">

    
         <div style="
    background: #25282b !important; 
    background-image: none !important; 
    box-shadow: none !important; 
    border: none !important;
    color: #20B2AA; 
    padding: 10px; 
    border-radius: 6px; 
    text-align: center; 
    font-weight: bold; 
    margin-top: 50px !important;
    margin-bottom: 10px !important;">
    📋 PLANIFICACIÓN POR POLÍGONOS
</div>
        
        <div id="polys-2" class="p-content" style="display:none;">{gen_poligonos(u_C1)}</div>
        <div id="polys-6" class="p-content" style="display:none;">{gen_poligonos(u_C1_SJA1)}</div>
        <div id="polys-7" class="p-content" style="display:none;">{gen_poligonos(u_C1_SCH1)}</div>
        <div id="polys-8" class="p-content" style="display:none;">{gen_poligonos(u_C1_SMD1)}</div>
        <div id="polys-1" class="p-content" style="display:none;">{gen_poligonos(u_PREC)}</div>
        <div id="polys-5" class="p-content" style="display:none;">{gen_poligonos(u_PREC_SMX2)}</div>
        <div id="polys-4" class="p-content">{gen_poligonos(u_SDE)}</div>
        <div id="polys-9" class="p-content" style="display:none;">{gen_poligonos(u_C1_VACIA)}</div>


        <div id="excel-polys" style="display:none; margin-top:10px;">
            <div style="background:#25282b; color:white; font-weight:bold; text-align:center; padding:8px; font-size:18px; border:1px solid #0f5b84;">
                📋 RESUMEN DE POLÍGONOS
            </div>

            <table style="width:100%; border-collapse:collapse; background:white; font-size:16px; table-layout:fixed;">
                <thead>
                    <tr style="background:#25282b; color:white; height:28px;">
                        <th style="border:1px solid #c0c0c0;">PLAN</th>
                        <th style="border:1px solid #c0c0c0;">VOL</th>
                        <th style="border:1px solid #c0c0c0;">UNIDAD</th>
                        <th style="border:1px solid #c0c0c0; width:55px;">ASIG</th>
                        <th style="border:1px solid #c0c0c0;">NODO</th>
                    </tr>
                </thead>
                <tbody id="excel-polys-body"></tbody>
            </table>
        </div>
        
        
    </div>


<!-- CONTADOR FLOTANTE OCULTO -->
<div id="fleet-float" hidden>
    <div style="font-weight:bold; margin-bottom:8px;">
        🚛 DISPONIBLE
    </div>

    <div id="fleet-float-body">
        Cargando...
    </div>
</div>





<script>

    const perfiles = {json.dumps(PERFILES)};
    const perfilActual = "{perfil_actual}";

    let currentTab = 2;
    let editedRowsPlan = new Set();
    let curC = "";
    let chronoInterval;
    let startTime;
    let elapsedTime = 0;
    let estadoPaquetesAntesDeExcel = "none"; // Guarda si el bloque estaba abierto o cerrado



    function cambiarCiclo(valorTab) {{
    // 1. Ocultar todas las tablas de disponibilidad y dejar visible solo la seleccionada
    document.querySelectorAll('.t-content').forEach(el => {{
        el.style.display = 'none';
    }});
    const tablaActiva = document.getElementById('tab-' + valorTab);
    if (tablaActiva) {{
        tablaActiva.style.display = 'block';
    }}

    // 2. Ocultar todos los bloques de polígonos y mostrar solo el del ciclo correspondiente
    document.querySelectorAll('.p-content').forEach(el => {{
        el.style.display = 'none';
    }});
    const polyActivo = document.getElementById('polys-' + valorTab);
    if (polyActivo) {{
        polyActivo.style.display = 'block';
    }}

    // 3. Actualizar la variable de control global
    currentTab = parseInt(valorTab);
    
    // 4. Recalcular valores de la interfaz
    if (typeof recalc === 'function') {{
        recalc();
    }}
}}



    function aplicarPerfil() {{

    let perfil = perfiles[perfilActual];

    if(!perfil) return;

    Object.keys(perfil).forEach(tabId => {{

        document.querySelectorAll('#body-' + tabId + ' tr').forEach(row => {{

            let unidad =
                row.querySelector('.edit-name')?.innerText.trim(); 

            if(perfil[tabId][unidad]) {{

                let data = perfil[tabId][unidad];

                let orh =
                    row.querySelector('.edit-orh');

                let disp =
                    row.querySelector('.edit-ocup');

                if(orh)
                    orh.innerText = data.orh;

                if(disp)
                    disp.innerText = data.disp;
            }}
        }});
   }});

    recalc();
}}


// --- LÓGICA DE SUMA A PRUEBA DE ERRORES ---
    (function initSuma() {{
        console.log("Iniciando lógica de suma...");
        const inputs = document.querySelectorAll('.sum-input');
        const totalDisplay = document.getElementById('total-final');

        if (inputs.length === 0) {{
            console.error("ERROR: No se encontraron los inputs con clase .sum-input");
        }}

        inputs.forEach(input => {{
            input.addEventListener('input', () => {{
                let sum = 0;
                inputs.forEach(i => {{
                    sum += parseFloat(i.value) || 0;
                }});
                if (totalDisplay) {{
                    totalDisplay.value = sum;
                    console.log("Total actualizado:", sum);
                }}
            }});
        }});
    }})();



function agregarFilaPlan(btn){{

    const bloque = btn.closest(".poligono-bloque");
    const tbody = bloque.querySelector("tbody");

    const filas = tbody.querySelectorAll(".calc-row");

    const filaBase = filas[0];

    const nuevaFila = filaBase.cloneNode(true);


    // quitar celdas con rowspan (PLAN y VOL)
    nuevaFila.querySelectorAll("[rowspan]").forEach(td => {{
        td.remove();
    }});


    // limpiar valores
    const u = nuevaFila.querySelector(".u-manual");
    if(u) u.innerText = "0";

    const spr = nuevaFila.querySelector(".spr-real-val");
    if(spr) spr.innerText = "0";

    const select = nuevaFila.querySelector(".s-type");
    if(select) select.selectedIndex = 0;

    const check = nuevaFila.querySelector(".ok-check");
    if(check) check.checked = false;


    // insertar antes de ESTADO
    const estado = tbody.querySelector("tr:last-child");

    tbody.insertBefore(nuevaFila, estado);
 

    actualizarRowspan(bloque);

    recalc();
}}



function quitarFilaPlan(btn){{

    const bloque = btn.closest(".poligono-bloque");
    const tbody = bloque.querySelector("tbody");

    const filas = tbody.querySelectorAll(".calc-row");


    if(filas.length <= 1){{
        return;
    }}


    filas[filas.length - 1].remove();


    actualizarRowspan(bloque);


    // 🔥 obliga al navegador a recalcular la tabla completa
    const tabla = bloque.querySelector("table");

    if(tabla){{

        tabla.style.width = "100%";
        tabla.style.tableLayout = "fixed";

        // refresca el render
        void tabla.offsetWidth;

        setTimeout(() => {{
            tabla.style.tableLayout = "fixed";
        }}, 50);
    }}


    recalc();
}}



function actualizarContador(bloque){{

    const filas = bloque.querySelectorAll(".calc-row");

    const contador = bloque.querySelector(".contador-filas");

    if(contador){{
        contador.innerText = "Filas: " + filas.length;
    }}

}}


function actualizarRowspan(bloque){{

    let filas = bloque.querySelectorAll(".calc-row").length;

    let plan = bloque.querySelector(".plan-cell");
    let vol = bloque.querySelector(".vol-cell");

    if(plan) plan.rowSpan = filas;
    if(vol) vol.rowSpan = filas;
}}


function actualizarRowspan(bloque){{

    const filas = bloque.querySelectorAll(".calc-row").length;

    const plan = bloque.querySelector("td.plan-cell");
    const volumen = bloque.querySelector("td.vol-cell");

    if(plan){{
        plan.rowSpan = filas;
    }}

    if(volumen){{
        volumen.rowSpan = filas;
    }}


    const contador = bloque.querySelector(".contador-filas");

    if(contador){{
        contador.innerText = "Filas: " + filas;
    }}
}}


function toggleMenuPestanas() {{
    let panel = document.getElementById("panel-selector-pestanas");
    if (panel) {{
        panel.style.display = (panel.style.display === "none" || panel.style.display === "") ? "block" : "none";
    }}
}}

function toggleBtnPestana(btnId, visible) {{
    let btn = document.getElementById(btnId);
    if (btn) {{
        btn.style.display = visible ? "inline-block" : "none";
    }}
}}




function toggleFleetFloating() {{
  const panel = document.getElementById("fleet-sticky");
  const btn = document.getElementById("fleet-toggle-btn");
  if (!panel) return;

  const goingToFloat = !panel.classList.contains("fleet-floating");

  if (goingToFloat) {{
    panel.classList.remove("fleet-normal");
    panel.classList.add("fleet-floating");
    if (btn) btn.textContent = "NORMAL (enter)";
  }} else {{
    panel.classList.remove("fleet-floating");
    panel.classList.add("fleet-normal");
    panel.removeAttribute("style");
    if (btn) btn.textContent = "FLOTAR ☁️";
  }}
}}




function showTab(n, btn) {{


    
        // 1. --- LOGICA NUEVA PARA EL BLOQUE C1 ---
    const bloqueC1 = document.getElementById('contenedor-paquetes-c1');
        if (bloqueC1) {{
            // Asumimos que la pestaña C1 es la que tiene el número 6 (si es otra, cambia el 6)
           if (n === 6) {{
            bloqueC1.style.display = 'block';
           }} else {{
              bloqueC1.style.display = 'none';
           }}
        }}


    
        // 1. Si la Vista Excel estaba activa, la apagamos de forma segura antes de cambiar de pestaña
        if (document.body.classList.contains("excel-view")) {{
            document.body.classList.remove("excel-view");
            
            // Cambiamos el texto del botón a su estado original
            let bExcel = document.getElementById("excel-btn");
            if (bExcel) bExcel.innerHTML = "VISTA EXCEL";
            
            // Ocultamos el bloque de la tabla espejo de Excel
            let excelPanel = document.getElementById("excel-polys");
            if (excelPanel) excelPanel.style.display = "none";
            
            // Restauramos de inmediato TODAS las filas de totales ocultas para que no se pierdan en SMX5/SDE
            const idsArestaurar = [
                "total-no-car-2", "total-car-schedule-2", "total-car-real-2",
                "total-no-car-6", "total-car-schedule-6", "total-car-real-6",
                "total-no-car-7", "total-car-schedule-7", "total-car-real-7",
                "total-no-car-8", "total-car-schedule-8", "total-car-real-8",
                "total-no-car-1", "total-car-schedule-1", "total-car-real-1",
                "total-no-car-5", "total-car-schedule-5", "total-car-real-5"
             ];
            idsArestaurar.forEach(id => {{
                let el = document.getElementById(id);
                if (el) {{
                    let fila = el.closest('tr');
                    if (fila) fila.style.removeProperty('display');
                }}
            }});
            
            // Aseguramos que los footers de todas las tablas vuelvan a mostrarse normales
            document.querySelectorAll('.meli-table tfoot tr').forEach(fila => {{
                fila.style.setProperty('display', 'table-row', 'important');
            }});
        }}

        // 2. Lógica nativa de tu aplicación para mover pestañas
        currentTab = n;
        document.querySelectorAll('.p-content, .t-content')
            .forEach(el => el.style.display = 'none');
        document.querySelectorAll('.tab-btn')
            .forEach(b => b.classList.remove('active'));

        document.getElementById('polys-' + n).style.display = 'block';
        document.getElementById('tab-' + n).style.display = 'block';

        btn.classList.add('active');

        recalc();
        if (typeof actualizarVisibilidadContador === "function") actualizarVisibilidadContador();
        updateFleetFloat();

        // ==============================================================================
        // 🔒 CANDADO DE VISIBILIDAD EXCLUSIVA (GANÁNDOLE AL CSS)
        // ==============================================================================
        const excelBtn = document.getElementById('excel-btn');
        if (excelBtn) {{
            if (n === 2 || n === 6 || n === 7 || n === 8 || n === 9) {{ // 🟢 Añadido "n === 9"
                excelBtn.style.setProperty('display', 'inline-block', 'important');
            }} else {{
                excelBtn.style.setProperty('display', 'none', 'important');
            }}
        }}
    }}






    function showAlert(msg) {{
        document.getElementById('alert-msg').innerText = msg;
        document.getElementById('google-alert').classList.add('show');
    }}
    function hideAlert() {{ document.getElementById('google-alert').classList.remove('show'); }}

    function stepVal(btn, delta, type) {{
    let row = btn.closest('tr');
    let sel = row.querySelector('.s-type').value;
    
    // Si no hay unidad seleccionada, no hace nada
    if(sel === "Seleccionar..." || !sel) return;

    // Buscamos la fila correspondiente en la tabla de Flota para sacar el MAX
    let fRows = Array.from(document.querySelectorAll('#body-' + currentTab + ' tr'));
    let fRow = fRows.find(r => r.querySelector('.edit-name').innerText.trim() === sel);
    
    if (!fRow) return; // Seguridad por si no encuentra la unidad

    let left = parseInt(fRow.querySelector('.f-left').innerText) || 0;
    let sprMaxReal = parseFloat(fRow.querySelector('.edit-spr-max').innerText) || 0;

    if(type === 'u') {{
        let span = row.querySelector('.u-manual');
        let val = parseInt(span.innerText) || 0;
        let newVal = val + delta;
        if (newVal < 0) newVal = 0; // Evita valores negativos en la celda del polígono

        // 🔥 PERMITE AGREGAR CUALQUIER UNIDAD ADICIONAL CON EL BOTÓN +
        if (delta > 0 && left <= 0) {{
            showAlert("⚠️ UNIDAD ADICIONAL. Se registrará como exceso en Delta.");
        }}
        
        span.innerText = newVal;
    }} else {{
        let span = row.querySelector('.spr-real-val');
        let val = parseFloat(span.innerText) || 0;
        let newVal = Math.round(val + delta);

        // VALIDACIÓN: Solo bloquea si intentas SUBIR el SPR por encima del máximo
        if (delta > 0 && newVal > sprMaxReal) {{
            showAlert("⚠️ NO PUEDES SOBREPASAR EL SPR MÁXIMO (" + sprMaxReal + ")");
            return; 
        }}
        
        span.innerText = newVal;
    }}
    editedRowsPlan.add(row);
    recalc();
}}



function actualizarHoraMinuto(celda){{

    let valor = celda.innerText.trim().replace(",", ".");

    if(valor === "") valor = "0";

    let numero = parseFloat(valor);

    if(isNaN(numero))
        numero = 0;

    let minutosTotales;

    // Si tiene decimal, se interpreta como HORAS
    if(valor.includes(".")){{
        minutosTotales = Math.round(numero * 60);
    }}
    // Si es entero grande (ej. 145), se interpreta como MINUTOS
    else if(numero >= 24){{
        minutosTotales = Math.round(numero);
    }}
    // Si es entero pequeño (ej. 2), se interpreta como HORAS
    else{{
        minutosTotales = Math.round(numero * 60);
    }}

    let horas = Math.floor(minutosTotales / 60);
    let mins = minutosTotales % 60;

    let fila = celda.closest("tr");
    let hm = fila.querySelector(".orh-hora");

    if(hm){{
        // 🔥 CAMBIO DE COLOR HORA ORH: Forzamos el color naranja/café llamativo (#d97706) en el texto nativo
        hm.style.color = "#141414";
        
        hm.innerText =
            String(horas).padStart(2,"0") +
            ":" +
            String(mins).padStart(2,"0");
    }}
}}

document.querySelectorAll(".edit-orh").forEach(function(celda){{

    actualizarHoraMinuto(celda);

    celda.addEventListener("input", function(){{

        actualizarHoraMinuto(this);

    }});

}});




function actualizarDosPorciento() {{

    let volumenTotal = 0;

    document.querySelectorAll(
        '#polys-' + currentTab + ' .v-total-val'
    ).forEach(el => {{

        volumenTotal +=
            parseFloat(el.innerText) || 0;

    }});

    let permitido =
        Math.round(volumenTotal * 0.02);

    let div =
        document.getElementById('dos-pct-global');

    if (div) {{

        div.innerHTML =
            `<b>2% PERMITIDO:</b> ${{permitido.toLocaleString()}}`;

    }}
}}







    function recalc() {{
        let fleet = {{}};
        
        // --- NORMALIZACIÓN DE PESTAÑA PARA MANEJO DE IDS ---
        let tabId = currentTab;
        // ----------------------------------------------------


        // 1. Capturar datos de la flota (Tabla de arriba)
document.querySelectorAll('#body-' + tabId + ' tr').forEach(row => {{
    let nameCell = row.querySelector('.edit-name');
    let name = nameCell.innerText.trim();
    let sch = parseInt(row.querySelector('.f-stock').innerText) || 0;
    let mi = row.querySelector('.edit-spr-min'), ma = row.querySelector('.edit-spr-max'), fs = row.querySelector('.f-stock');
    
    if(sch > 0) {{
        // --- ESTE ES EL COLOR DE FONDO DE LA FILA COMPLETA ---
        row.style.background = "white"; 


        // Eliminamos row.style.color para no forzar toda la fila 
// --- ESTE ES EL COLOR DE FONDO DE LA CELDA DE STOCK Y MÍNIMOS ---
        fs.style.background = "#fcf8cc"; 


// =======================================================================
        // 🔥 AQUÍ SE CAMBIA EL COLOR DE SPR MIN Y SPR MAX CUANDO SCHEDULE > 0
        // =======================================================================
        mi.style.background = "#ffffff"; mi.style.color = "#25282b"; mi.style.fontWeight = "bold";
        ma.style.background = "#ffffff"; ma.style.color = "#25282b"; ma.style.fontWeight = "bold";


// --- ESTE ES EL COLOR DEL NOMBRE DE LA UNIDAD ---
        // Ponemos nombre en NEGRO
        nameCell.style.color = "#25282b";
        nameCell.style.fontWeight = "bold";
    }} else {{
        row.style.background = "#DCDCDC"; 
        // Eliminamos row.style.color = "#969696"
        fs.style.background = "#FFFF00"; 
        mi.style.background = "#dcdcdc"; mi.style.color = "#969696"; mi.style.fontWeight = "normal";
        ma.style.background = "#dcdcdc"; ma.style.color = "#969696"; ma.style.fontWeight = "normal";
        
        // Ponemos nombre en GRIS
        nameCell.style.color = "#969696";
        nameCell.style.fontWeight = "normal";
    }}
    
    if(name !== "" && name !== "NUEVA UNIDAD") {{
        fleet[name] = {{ max: parseFloat(ma.innerText)||0, stock: sch, used: 0 }};
    }}
}});


// --- INICIO DEL BLOQUE DE SINCRONIZACIÓN ---
let mapeoRuteadas = {{}};
document.querySelectorAll('#polys-' + tabId + ' .calc-row').forEach(row => {{
    let s = row.querySelector('.s-type').value;
    let u = parseInt(row.querySelector('.u-manual').innerText) || 0;
    if (s && s !== "Seleccionar...") {{
        mapeoRuteadas[s] = (mapeoRuteadas[s] || 0) + u;
    }}
}});

document.querySelectorAll('#body-' + tabId + ' tr').forEach(row => {{
    let nameCell = row.querySelector('.edit-name');
    let ruteadaCell = row.querySelector('.f-ruteadas');
    if (nameCell && ruteadaCell) {{
        let name = nameCell.innerText.trim();
        ruteadaCell.innerText = mapeoRuteadas[name] || 0;
    }}
}});
// --- FIN DEL BLOQUE DE SINCRONIZACIÓN ---



// 2. Calcular ocupación por polígono (Tabla de abajo)
document.querySelectorAll('#polys-' + tabId + ' .poligono-bloque').forEach(bl => {{
    let vT = parseFloat(bl.querySelector('.v-total-val').innerText) || 0, vA = 0;
    let vCalcEl = bl.querySelector('.v-calculado-total');

    // Obtenemos el nombre del plan aquí para identificar CENTRO 1 y CENTRO 2
    let nombrePlanPadre = bl.querySelector('td[rowspan]')?.innerText?.toUpperCase()?.trim() || "";
    let esCentro = (nombrePlanPadre === "⚠️ CENTRO 1" || nombrePlanPadre === "⚠️ CENTRO 2");
    
    let celdaNodos = bl.querySelector('.nodos-val');
    let tieneNodo = (tabId == 6 && celdaNodos && parseInt(celdaNodos.innerText) > 0);
    
    // Obtenemos todas las filas del bloque
    let filas = bl.querySelectorAll('.calc-row');

    filas.forEach((r, index) => {{
        let sType = r.querySelector('.s-type');
        let uManual = r.querySelector('.u-manual');
        let sp = r.querySelector('.spr-real-val');
        
        // 🔥 AQUÍ ESTÁ LA MAGIA:
        // Si NO es Centro Y tiene nodo, aplica la regla (Funciona para todos los demás)
        // Si ES Centro, esta condición da FALSE y se salta la asignación automática
        if (!esCentro && tieneNodo && index === 0 && (sType.value === "" || sType.value === "Seleccionar...")) {{
            sType.value = "Large Van MLP foráneo";
            uManual.innerText = "1";
        }}

        // Si el usuario cambió la unidad manualmente, aseguramos que si es "Seleccionar...", la cantidad sea 0
        if (sType.value === "" || sType.value === "Seleccionar...") {{
            uManual.innerText = "0";
        }}
        
        let s = sType.value;
        let u = parseInt(uManual.innerText) || 0;

        // 🔥 CANDADO ALCHICHICA
        let nombrePlanPadre = bl.querySelector('td[rowspan]')?.innerText?.toUpperCase() || "";
        if (nombrePlanPadre.includes("ALCHICHICA")) {{
            if (s !== "Seleccionar..." && s !== "") {{
                vA += (u * (parseFloat(sp.innerText) || 0));
                sp.style.fontWeight = "bold";
                sp.style.setProperty("background-color", "#edf2f2");
                sp.style.setProperty("color", "#25282b");
            }}
            return; 
        }}

        // Lógica de flota
        if(s !== "Seleccionar..." && s !== "" && fleet[s]) {{
            if(!editedRowsPlan.has(r)) sp.innerText = fleet[s].max; 
            fleet[s].used += u; 
            vA += (u * (parseFloat(sp.innerText) || 0));
            sp.style.setProperty("background-color", "#edf2f2");
            sp.style.setProperty("color", "#25282b");
        }} else {{
            sp.style.setProperty("background-color", "#FFFFFF");
        }}
    }});

    // ... (Cálculo de vCalcEl y vT igual que antes) ...
    vCalcEl.innerText = Math.round(vA);
    let d = bl.querySelector('.p-diff');
    let diffVal = Math.round(vA);
    if (vT === 0) d.innerText = "VACÍO";
    else if (diffVal === Math.round(vT)) {{ d.innerText = "OK"; d.style.background = "#61b888"; }}
    else if (vA > vT) {{ d.innerText = "EXCESO: " + Math.round(vA - vT); d.style.background = "#f2bd5c"; }}
    else {{ d.innerText = "FALTAN: " + Math.round(vT - vA); d.style.background = "#fc9a88"; }}
}});



// 3. REPLICAR Y CALCULAR DELTA BASADO EN "RUTEADAS" MANUALES
document.querySelectorAll('#body-' + tabId + ' tr').forEach(row => {{
    let nameCell = row.querySelector('.edit-name');
    if (!nameCell) return;
    
    let n = nameCell.innerText.trim();
    
    // Buscamos el valor de Ruteadas (USADAS) y del Schedule
    let ruteadasManuales = parseFloat(row.querySelector('.f-ruteadas')?.innerText || 0);
    let stock = parseFloat(row.querySelector('.f-stock')?.innerText || 0);
    let cL = row.querySelector('.f-left'); // Columna DELTA
    
    // --- Lógica de color para columna USADAS ---
    let ruteadaCell = row.querySelector('.f-ruteadas');
    if (ruteadaCell) {{
        if (ruteadasManuales > 0) {{
            ruteadaCell.style.backgroundColor = "#d3f0e5"; // Fondo verde claro
            ruteadaCell.style.color = "#008B8B";           // Número verde
            ruteadaCell.style.fontWeight = "bold";
        }} else {{
            ruteadaCell.style.backgroundColor = "#dcdcdc";
            ruteadaCell.style.color = "";
            ruteadaCell.style.fontWeight = "bold";
        }}
    }}

    // --- LÓGICA DE COLOR Y FORMATO POSITIVO PARA DELTA ---
    if (cL) {{
        let exceso = ruteadasManuales - stock; // Diferencia de adicionales
        
        if (exceso > 0) {{
            // 🔥 Si excediste el Schedule, muestra +3 en color rojo
            cL.innerText = "+" + exceso;
            cL.style.color = "red"; 
            cL.style.fontWeight = "bold"; 
            cL.style.background = "transparent";
        }} else if (ruteadasManuales === stock && stock > 0) {{
            // Si consumiste exactamente todo el Schedule (0 sobrantes, 0 faltantes)
            cL.innerText = "0";
            cL.style.color = "white"; 
            cL.style.background = "#fc765d"; // Naranja/Rojo de completado
            cL.style.fontWeight = "bold";
        }} else {{
            // Si todavía te quedan unidades por usar del Schedule
            let restantes = stock - ruteadasManuales;
            cL.innerText = restantes;
            cL.style.color = "#17191a"; 
            cL.style.background = "transparent"; 
            cL.style.fontWeight = "normal";
        }}
    }}
}});




// 3.5 BADGE DE UNIDADES ADICIONALES EN POLÍGONOS (CÁLCULO EXACTO POR FILA)
let contadorAcumulado = {{}};

document.querySelectorAll('#polys-' + tabId + ' .calc-row').forEach(r => {{
    let sel = r.querySelector('.s-type')?.value;
    let uCell = r.querySelector('.u-manual-cell');
    let divFlex = uCell ? uCell.querySelector('div') : null;
    let spanU = r.querySelector('.u-manual');
    let uManual = parseInt(spanU?.innerText) || 0;

    if (!divFlex) return;

    let badge = divFlex.querySelector('.badge-adicional');

    if (sel && sel !== "Seleccionar..." && fleet[sel] && uManual > 0) {{
        let stockInicial = fleet[sel].stock;
        let usadasPrevias = contadorAcumulado[sel] || 0;

        // Calculamos cuántas de las unidades de ESTA FILA entran en el Schedule restante
        let cubiertasPorSchedule = Math.max(0, Math.min(uManual, stockInicial - usadasPrevias));
        let excesoFila = uManual - cubiertasPorSchedule;

        // Acumulamos el uso para la siguiente fila
        contadorAcumulado[sel] = usadasPrevias + uManual;

        if (excesoFila > 0) {{
            // 🔥 Si esta fila específica consumió unidades por encima del Schedule
            if (!badge) {{
                badge = document.createElement('span');
                badge.className = 'badge-adicional';
                badge.style.cssText = 'font-size: 10px; background: #d32f2f; color: white; padding: 1px 4px; border-radius: 3px; font-weight: bold; margin-left: 2px;';
                if (spanU) spanU.after(badge);
            }}
            badge.innerText = `+${{excesoFila}}`;
            badge.style.display = 'inline-block';
            badge.title = `${{cubiertasPorSchedule}} de Schedule + ${{excesoFila}} adicionales en este plan`;
            uCell.style.backgroundColor = "#d3f0e5";
        }} else {{
            if (badge) badge.style.display = 'none';
            uCell.style.backgroundColor = "#d3f0e5";
        }}
    }} else {{
        if (badge) badge.style.display = 'none';
        if (uCell) uCell.style.backgroundColor = "#d3f0e5";
    }}
}});




       // 4. FILTRAR LISTA (Solo las crowd permanecen siempre visibles)
document.querySelectorAll('#polys-' + tabId + ' .poligono-bloque').forEach(bl => {{

    // 🔥 Lista de unidades permitidas para seguir apareciendo sin stock
    const permitidasSinStock = ["car 8h", "car - 8h", "car 5h", "car - 5h", "car 3h", "car - 3h"];

    bl.querySelectorAll('.s-type').forEach(s => {{ 
        let cur = s.value; 
        let opt = '<option value="">Seleccionar...</option>';
        
        Object.keys(fleet).forEach(k => {{
            let nameLower = k.toLowerCase().trim();
            let stock = fleet[k].stock;
            let used = fleet[k].used;
            
            let esPermitida = permitidasSinStock.some(u => nameLower.includes(u));
            let tieneCapacidad = (stock - used > 0);
            
            // Muestra la unidad si tiene saldo libre, o si es de las permitidas, o si ya está seleccionada en esta fila
            if (tieneCapacidad || esPermitida || k === cur) {{
                opt += `<option value="${{k}}">${{k}}</option>`;
            }}
        }});
        
        s.innerHTML = opt;
        s.value = cur;

        updateSelectColor(s);
    }});
}});


    // --- 5. CALCULO DE TOTALES (Lógica Precisa) ---
let totals = {{
    mlpDecl: 0, mlpRute: 0,
    rentalDecl: 0, rentalRute: 0,
    carDecl: 0, carRute: 0,
    otrosRute: 0,
    totalRuteadas: 0
}};

// 1. DECLARADAS: Suma la columna "SCHEDULE" de la tabla de arriba
document.querySelectorAll('#body-' + tabId + ' tr').forEach(row => {{
    let name = row.querySelector('.edit-name')?.innerText.toLowerCase().trim() || "";
    let sch = parseInt(row.querySelector('.f-stock')?.innerText) || 0;
    
    if (name.includes("mlp")) totals.mlpDecl += sch;
    else if (name.includes("rental")) totals.rentalDecl += sch;
    else if (name.includes("car") || name.includes("moto") || name.includes("Newbie") || name.includes("9h")) totals.carDecl += sch;
}});


// 2. Calcular ocupación y totales
totals.totalRuteadas = 0; // Reiniciamos el acumulador
totals.mlpRute = 0;
totals.rentalRute = 0;
totals.carRute = 0;
totals.otrosRute = 0; 

document.querySelectorAll('#polys-' + tabId + ' .calc-row').forEach(row => {{
    let s = row.querySelector('.s-type').value; 
    let u = parseInt(row.querySelector('.u-manual').innerText) || 0;

    if (!s || s === "Seleccionar...") return;

    let name = s.toLowerCase().trim();

    // 1. CLASIFICACIÓN
    if (name.includes("mlp")) {{
        totals.mlpRute += u;
    }} else if (name.includes("rental")) {{
        totals.rentalRute += u;
    }} else if (name.includes("delivery")) {{
        totals.otrosRute += u;
    }} else if (name.includes("car") || name.includes("moto") || name.includes("Newbie") || name.includes("9h")) {{
        totals.carRute += u;
    }} else {{
        totals.otrosRute += u; 
    }}

    // 2. SUMA TOTAL (Aquí sumamos todas las categorías recién actualizadas)
    // Esto garantiza que el total siempre sea la suma de las partes
    totals.totalRuteadas = totals.mlpRute + totals.rentalRute + totals.carRute + totals.otrosRute;
}});



// 3. ACTUALIZACIÓN DE PANTALLA

totals.totalRuteadas = totals.mlpRute + totals.rentalRute + totals.carRute + totals.otrosRute;

console.log("DEBUG: MLP=" + totals.mlpRute + ", Rental=" + totals.rentalRute + ", Car=" + totals.carRute + ", Otros=" + totals.otrosRute + ", TOTAL=" + totals.totalRuteadas);

// 3. ACTUALIZACIÓN DE PANTALLA
function setT(id, val) {{
    let finalId = id + '-' + tabId;
    let el = document.getElementById(finalId);
    
    if (el) {{
        el.innerText = Math.round(val);
        console.log("ÉXITO: Se actualizó el ID " + finalId + " con valor " + val);
    }} else {{
        console.error("¡ERROR! No encontré el ID: " + finalId);
    }}
}}

// --- PONLO AQUÍ: Esto garantiza que la suma sea la correcta ---
totals.totalRuteadas = totals.mlpRute + totals.rentalRute + totals.carRute + totals.otrosRute;
// -----------------------------------------------------------------

// Ahora llamamos a los setT
setT('total-mlp-decl', totals.mlpDecl);
setT('total-mlp-rute', totals.mlpRute);
setT('total-rental-decl', totals.rentalDecl);
setT('total-rental-rute', totals.rentalRute);
setT('total-car-schedule', totals.carDecl);
setT('total-car-real', totals.carRute);
setT('total-otros', totals.otrosRute); 
// En lugar de llamar a setT normalmente para el total, hacemos esto:
setTimeout(() => {{
    let valorCorrecto = totals.mlpRute + totals.rentalRute + totals.carRute + totals.otrosRute;
    let el = document.getElementById('total-ruteadas-' + tabId);
    if (el) {{
        el.innerText = Math.round(valorCorrecto);
        el.style.color = "#66CDAA"; // Le damos un color para saber que el forzado funcionó
        console.log("FORZADO: El total ahora es " + valorCorrecto);
    }}
}}, 500); // Espera medio segundo después de que todo se ejecute para forzar el valor

updateFleetFloat();

actualizarTotales();

actualizarDosPorciento();

// --- ACTUALIZACIÓN DINÁMICA SEGÚN LA PESTAÑA (tabId) ---
    // Esto busca el ID específico de la pestaña actual (ej: val-mlp-rute-2)
    let elMlp = document.getElementById('val-mlp-rute-' + tabId);
    let elRental = document.getElementById('val-rental-rute-' + tabId);
    let elCar = document.getElementById('val-car-rute-' + tabId);

    // Solo actualizamos si el elemento realmente existe en la pestaña actual
    if(elMlp) elMlp.innerText = Math.round(totals.mlpRute);
    if(elRental) elRental.innerText = Math.round(totals.rentalRute);
    if(elCar) elCar.innerText = Math.round(totals.carRute);

    }}



// --- ENTER: SALIR DE FLOTANTE / CIERRA PRIORIDADES / ALERTAS ---
document.addEventListener('keydown', function(event) {{
    if (event.key !== 'Enter') return;

    // 1️⃣ SI ESTÁ FLOTANDO: Salir inmediatamente a la vista NORMAL al dar Enter
    const fleet = document.getElementById("fleet-sticky");
    if (fleet && fleet.classList.contains("fleet-floating")) {{
        event.preventDefault();
        if (typeof toggleFleetFloating === "function") {{
            toggleFleetFloating();
        }}
        return;
    }}

    // 2️⃣ SI NO ESTÁ FLOTANDO: Validar controles interactivos
    const ae = document.activeElement;
    const tag = ae && ae.tagName ? ae.tagName.toLowerCase() : "";
    if (tag === "button" || tag === "input" || tag === "select" || tag === "textarea") {{
        return;
    }}
    if (ae && ae.isContentEditable) {{
        return;
    }}

    // 3️⃣ LÓGICA PANEL PRIORIDADES
    let panel = document.getElementById('panel-prioridades');
    if (panel && panel.style.top === "0px") {{
        panel.style.top = "-600px";
        if (document.activeElement) document.activeElement.blur();
    }}

    // 4️⃣ LÓGICA ALERTAS ROJAS
    let alerta = document.querySelector('.alerta-roja, .p-diff');
    if (alerta && alerta.innerText.includes('EXCESO')) {{
        if (document.activeElement) document.activeElement.blur();
    }}
}});




    
    function focusCalc() {{
        document.getElementById('calc_wrapper').focus();
    }}



    function filterRows(onlyActive) {{
        // 1. Filtrar las filas de la tabla de disponibilidad de flota (Derecha)
        const rows = document.querySelectorAll('#body-' + currentTab + ' .master-row');
        rows.forEach(row => {{
            const stock = parseInt(row.querySelector('.f-stock').innerText) || 0;
            row.style.display = (onlyActive && stock === 0) ? 'none' : '';
        }});
        
        // La lógica de polígonos fue eliminada para que no interfiera.
    }}



            
    // ==========================================
// 🔥 PEGA LA FUNCIÓN TOGGLETOOLS EXACTAMENTE AQUÍ:
// ==========================================
    let herramientasVisibles = true;

    function toggleTools() {{
    const crono = document.querySelector('.crono-card');
    const convertidorContenido = document.querySelectorAll('.google-tool > *:not(#toggle-tools-btn)');
    const boton = document.getElementById('toggle-tools-btn');

    herramientasVisibles = !herramientasVisibles;

    if (crono) {{
        crono.style.display = herramientasVisibles ? '' : 'none';
    }}

    convertidorContenido.forEach(elemento => {{
        elemento.style.display = herramientasVisibles ? '' : 'none';
    }});

    // AQUÍ ESTÁ EL CAMBIO:
    if (!herramientasVisibles) {{
        boton.innerHTML = '🛠️ MOSTRAR UTILERÍAS';
        boton.className = 'btn-mostrar'; // Cambiamos la clase, no el estilo
    }} else {{
        boton.innerHTML = '❌ OCULTAR UTILERÍAS';
        boton.className = 'btn-ocultar'; // Cambiamos la clase, no el estilo
    }}
}}


    function convertTime() {{
        let m = parseInt(document.getElementById('min-in').value) || 0;
        document.getElementById('time-res').innerText = Math.floor(m/60) + "h " + (m%60) + "m";
    }}
    function an(n) {{ curC += n; updateCalc(); }}
    function ao(o) {{ curC += " " + o + " "; updateCalc(); }}
    function cl() {{ curC = ""; updateCalc(); document.getElementById('calc_h').innerText = ""; }}
    function del() {{ curC = curC.trim().slice(0, -1); updateCalc(); }}
    function updateCalc() {{ document.getElementById('calc_r').innerText = curC || "0"; }}
    function calc_eq() {{ try {{ let res = eval(curC); document.getElementById('calc_h').innerText = curC + " ="; curC = res.toString(); updateCalc(); }} catch {{ }} }}
    
    function updateReloj() {{ document.getElementById('reloj-actual').innerText = new Date().toLocaleTimeString('en-GB'); }}
    setInterval(updateReloj, 1000);

    function startC() {{ if(!chronoInterval) {{ startTime = Date.now() - elapsedTime; chronoInterval = setInterval(()=>{{ elapsedTime = Date.now() - startTime; updateCDisplay(); }}, 100); }} }}
    function stopC() {{ clearInterval(chronoInterval); chronoInterval = null; }}
    function resetC() {{ stopC(); elapsedTime = 0; updateCDisplay(); }}
    function updateCDisplay() {{ 
        let d = new Date(elapsedTime);
        let h = String(Math.floor(elapsedTime/3600000)).padStart(2,'0');
        let m = String(d.getUTCMinutes()).padStart(2,'0');
        let s = String(d.getUTCSeconds()).padStart(2,'0');
        let ms = Math.floor(d.getUTCMilliseconds()/100);
        document.getElementById('crono-main').innerText = `${{h}}:${{m}}:${{s}}.${{ms}}`;
    }}


function manualEdit(el) {{ 
        let r = el.closest('tr');
        if (r) {{
            editedRowsPlan.add(r);
            
            let table = r.closest('table');
            let tbody = table ? table.querySelector('tbody') : null;
            let selectType = r.querySelector('.s-type');
            let unidadSeleccionada = selectType ? selectType.value : "";
            
            let permiteInfinito = false;
            let esUnidadCar = unidadSeleccionada.toLowerCase().includes("car");

            // 1. Validamos la pestaña activa de la misma forma segura
            let activeTabBtn = document.querySelector('.tab-btn.active');
            if (activeTabBtn) {{
                let tabId = activeTabBtn.textContent.trim();
                
                // Regla C: SCH1 (7) y SMD1 (8) con CAR 8H
                if ((currentTab === 7 || currentTab === 8) && unidadSeleccionada.trim() === "CAR 8H") {{
                    permiteInfinito = true;
                }}
                // Regra A: C1 con Large Van MLP
                else if (tabId === "C1 SCP1" && unidadSeleccionada.trim() === "Large Van MLP") {{
                    permiteInfinito = true;
                }} 
                // Regla B: SDE o PREC con cualquier Car
                else if ((tabId === "SDE" || tabId === "PREC") && esUnidadCar) {{
                    permiteInfinito = true;
                }}
            }}

            // 2. Si cumple la regla y es la última fila, la clonamos antes del recálculo
            if (permiteInfinito && tbody) {{
                let filasCalculo = tbody.querySelectorAll('tr.calc-row');
                let ultimaFila = filasCalculo[filasCalculo.length - 1];
                
                if (r === ultimaFila) {{
                    let nuevaFila = r.cloneNode(true);
                    
                    let nuevoSelect = nuevaFila.querySelector('.s-type');
                    if (nuevoSelect) {{
                        nuevoSelect.value = "";
                        nuevoSelect.style.color = "#808080";
                    }}
                    
                    let nuevoSpanU = nuevaFila.querySelector('.u-manual');
                    if (nuevoSpanU) nuevoSpanU.innerText = "0";
                    
                    let nuevoSpanS = nuevaFila.querySelector('.spr-real-val');
                    if (nuevoSpanS) nuevoSpanS.innerText = "0";

                    let nuevoCheck = nuevaFila.querySelector('.ok-check');
                    if (nuevoCheck) nuevoCheck.checked = false;

                    tbody.appendChild(nuevaFila);
                }}
            }}
        }}
        // 3. Ejecutamos tu recálculo original pase lo que pase
        recalc(); 
    }}


function resetRow(sel) {{ 
        let r = sel.closest('tr');
        if (!r) return;
        let table = sel.closest('table');
        if (!table) return;

        let tbody = table.querySelector('tbody');
        let unidadSeleccionada = sel.value;

        // 1. Limpieza si se regresa a la opción por defecto
        if (unidadSeleccionada === "") {{
            r.querySelector('.u-manual').innerText = "0";
            r.querySelector('.spr-real-val').innerText = "0";
            editedRowsPlan.delete(r);
            recalc();
            return;
        }}

        // 2. Capturar el Volumen Total de este bloque de polígono
        let volTotalSpan = table.querySelector('.v-total-val');
        let volumenTotal = volTotalSpan ? parseFloat(volTotalSpan.textContent) || 0 : 0;

        // 3. Obtener el SPR, el Stock Total inicial (Schedule)
        let sprEncontrado = 0;
        let stockInicialFlota = 0;
        let totalUnidadesUsadasEnEstaPestana = 0;
        
        let filasFlota = document.querySelectorAll('#body-' + currentTab + ' .master-row');
        for (let filaFlota of filasFlota) {{
            let celdaNombre = filaFlota.querySelector('.edit-name');
            if (celdaNombre && celdaNombre.innerText.trim() === unidadSeleccionada.trim()) {{
                let celdaSprMax = filaFlota.querySelector('.edit-spr-max');
                let celdaStock = filaFlota.querySelector('.f-stock'); // Columna SCHEDULE de la tabla superior activa
                
                if (celdaSprMax) sprEncontrado = parseFloat(celdaSprMax.innerText) || 0;
                if (celdaStock) stockInicialFlota = parseInt(celdaStock.innerText) || 0;
                break;
            }}
        }}

        // 4. Inyectar el SPR en la celda correspondiente
        let spanS = r.querySelector('.spr-real-val');
        if (spanS) {{
            spanS.innerText = sprEncontrado;
        }}

        // 5. CALCULAR EL VOLUMEN CUBIERTO POR LAS *OTRAS* FILAS DE ESTE MISMO POLÍGONO
        let volumenYaCubierto = 0;
        let todasLasFilasPlan = tbody.querySelectorAll('tr.calc-row');
        
        todasLasFilasPlan.forEach(filaPlan => {{
            if (filaPlan !== r) {{
                let u = parseInt(filaPlan.querySelector('.u-manual').innerText) || 0;
                let spr = parseFloat(filaPlan.querySelector('.spr-real-val').innerText) || 0;
                volumenYaCubierto += (u * spr);
            }}
        }});

        // El volumen que verdaderamente nos falta cubrir
        let volumenRestantePlan = volumenTotal - volumenYaCubierto;
        if (volumenRestantePlan < 0) volumenRestantePlan = 0;

        // 6. CORREGIDO: CONTAR UNIDADES OCUPADAS ÚNICAMENTE EN LA PESTAÑA ACTIVA
        // Filtramos usando el ID específico de los polígonos activos (#polys-X)
        document.querySelectorAll('#polys-' + currentTab + ' .calc-row').forEach(fGlobal => {{
            if (fGlobal !== r) {{
                let t = fGlobal.querySelector('.s-type')?.value || "";
                if (t.trim() === unidadSeleccionada.trim()) {{
                    totalUnidadesUsadasEnEstaPestana += parseInt(fGlobal.querySelector('.u-manual').innerText) || 0;
                }}
            }}
        }});

        // Inventario real remanente en el patio para la pestaña actual
        let inventarioDisponibleReal = stockInicialFlota - totalUnidadesUsadasEnEstaPestana;
        if (inventarioDisponibleReal < 0) inventarioDisponibleReal = 0;

        // 7. CÁLCULO DE LAS UNIDADES NECESARIAS CON SU TOPE INVIOLABLE
        let unidadesCalculadas = 0;
        
        if (unidadSeleccionada.trim() === "Delivery Cell Large Van") {{
            unidadesCalculadas = 1;
        }} else if (volumenRestantePlan > 0 && sprEncontrado > 0) {{
            // Cuántas se necesitan idealmente para finiquitar los paquetes faltantes
            unidadesCalculadas = Math.ceil(volumenRestantePlan / sprEncontrado);
            
            // Reglas de excepciones infinitas/negativas para tus otras pestañas
            let permiteInfinito = false;
            let esUnidadCar = unidadSeleccionada.toLowerCase().includes("car");
            let activeTabBtn = document.querySelector('.tab-btn.active');
            
            if (activeTabBtn) {{
                let tabId = activeTabBtn.textContent.trim();

                // Regla nueva para CAR 8H en pestañas 7 y 8
                if ((currentTab === 7 || currentTab === 8) && unidadSeleccionada.trim() === "CAR 8H") {{
                    permiteInfinito = true;
                }}
                else if (tabId === "C1 SCP1" && unidadSeleccionada.trim() === "Large Van MLP") {{
                    permiteInfinito = true;
                }} 
                else if ((currentTab === 1 || currentTab === 5 || currentTab === 4) && esUnidadCar) {{
                    if (unidadSeleccionada.trim() !== "Small 9h Ext Car") {{
                        permiteInfinito = true;
                    }}
                }}
            }}

            // CANDADO DE DISPONIBILIDAD: Si no es unidad infinita, limitamos estrictamente al stock físico real de la pestaña
            if (!permiteInfinito) {{
                if (unidadesCalculadas > inventarioDisponibleReal) {{
                    unidadesCalculadas = inventarioDisponibleReal; // Agarra todo lo que queda de esta pestaña
                    
                    if (unidadesCalculadas === 0) {{
                        showAlert("⚠️ FLOTA AGOTADA. No quedan unidades disponibles de: " + unidadSeleccionada);
                    }} else {{
                        showAlert("⚠️ FLOTA INSUFICIENTE. Se asignaron las últimas " + unidadesCalculadas + " unidades para amortiguar el volumen.");
                    }}
                }}
            }}
        }}

        // Inyectar el resultado final calculado en la columna "# USADAS"
        let spanU = r.querySelector('.u-manual');
        if (spanU) {{
            spanU.innerText = unidadesCalculadas;
        }}

        // 8. ADICIÓN MANUAL DE FILA EXTRA (Conserva tu expansión automática de la tabla)
        let permiteInfinitoFila = false;
        let esUnidadCarFila = unidadSeleccionada.toLowerCase().includes("car");
        let activeTabBtnFila = document.querySelector('.tab-btn.active');
        
        if (activeTabBtnFila) {{
            let tabId = activeTabBtnFila.textContent.trim();
            if (tabId === "C1 SCP1" && unidadSeleccionada.trim() === "Large Van MLP") {{
                permiteInfinitoFila = true;
            }} else if ((currentTab === 1 || currentTab === 5 || currentTab === 4) && esUnidadCarFila) {{
                if (unidadSeleccionada.trim() !== "Small 9h Ext Car") {{
                    permiteInfinitoFila = true;
                }}
            }}
        }}

        if (permiteInfinitoFila && tbody) {{
            let filasCalculo = tbody.querySelectorAll('tr.calc-row');
            let ultimaFila = filasCalculo[filasCalculo.length - 1];
            
            if (r === ultimaFila) {{
                let nuevaFila = r.cloneNode(true);
                let nuevoSelect = nuevaFila.querySelector('.s-type');
                if (nuevoSelect) {{
                    nuevoSelect.value = "";
                    nuevoSelect.style.color = "#808080";
                }}
                
                let nuevoSpanU = nuevaFila.querySelector('.u-manual');
                if (nuevoSpanU) nuevoSpanU.innerText = "0";
                
                let nuevoSpanS = nuevaFila.querySelector('.spr-real-val');
                if (nuevoSpanS) nuevoSpanS.innerText = "0";

                let nuevoCheck = nuevaFila.querySelector('.ok-check');
                if (nuevoCheck) nuevoCheck.checked = false;

                tbody.appendChild(nuevaFila);
            }}
        }}

        // Disparar recálculo general para sincronizar los paneles flotantes y contadores
        if (typeof manualEdit === 'function' && spanU) {{
            manualEdit(spanU);
        }} else {{
            recalc();
        }}
    }}




    // === TU ESCUCHADOR DE TECLADO SIGUE TOTALMENTE INTACTO ABAJO ===
    document.addEventListener('keydown', (e) => {{
        const calc = document.getElementById('calc_wrapper');
        const alerta = document.getElementById('google-alert');

        if (e.key === 'Enter' && alerta.classList.contains('show')) {{
            e.preventDefault();
            e.stopPropagation();
            hideAlert();
            return;
        }}

        if (document.activeElement === calc) {{
            if (e.key >= '0' && e.key <= '9') an(e.key);
            if (e.key === '+') ao('+');
            if (e.key === '-') ao('-');
            if (e.key === '*') ao('*');
            if (e.key === '/') {{ e.preventDefault(); ao('/'); }}
            if (e.key === 'Enter') {{ e.preventDefault(); calc_eq(); }}
            if (e.key === 'Escape') cl();
            if (e.key === 'Backspace') del();
        }}
    }});


    document.addEventListener("DOMContentLoaded", function() {{
        const selector = document.getElementById("ciclo-selector");
        if (selector) {{
            cambiarCiclo(selector.value);
        }}
    }});


function toggleExcelView() {{
    const isExcel = !document.body.classList.contains("excel-view");
    document.body.classList.toggle("excel-view", isExcel);
    
    let btn = document.getElementById("excel-btn");
    let excel = document.getElementById("excel-polys");
    let bPaquetes = document.getElementById("contenedor-paquetes-c1"); // <--- Captura el contenedor
    
    // IDs de las filas que quieres ocultar en modo Excel
    const idsAocultar = [
        "total-no-car-2", "total-car-schedule-2", "total-car-real-2",
        "total-no-car-6", "total-car-schedule-6", "total-car-real-6",
        "total-no-car-7", "total-car-schedule-7", "total-car-real-7",
        "total-no-car-8", "total-car-schedule-8", "total-car-real-8",
        "total-no-car-1", "total-car-schedule-1", "total-car-real-1",
        "total-no-car-9", "total-car-schedule-9", "total-car-real-9",
        "total-no-car-5", "total-car-schedule-5", "total-car-real-5"
    ];
    if (isExcel) {{
        // --- MODO EXCEL: OCULTAR ---
        if (bPaquetes) {{
            estadoPaquetesAntesDeExcel = bPaquetes.style.display; // Guarda el estado actual (si era block o none)
            bPaquetes.style.display = "none"; // 🔥 Oculta el contenedor en Excel
        }}
        
        generarExcelPolys();
        btn.innerHTML = "VISTA NORMAL";
        if(excel) excel.style.display = "block";
        
        ["polys-1", "polys-2", "polys-4", "polys-5", "polys-6", "polys-7", "polys-8", "polys-9"].forEach(id => {{
            let el = document.getElementById(id);
            if(el) el.style.display = "none";
        }});
        idsAocultar.forEach(id => {{
            let el = document.getElementById(id);
            if(el) {{
                let fila = el.closest('tr');
                if(fila) fila.style.display = 'none';
            }}
        }});
    }} else {{
        // --- MODO NORMAL: RESTAURAR ---
        if (bPaquetes) {{
            bPaquetes.style.display = estadoPaquetesAntesDeExcel; // 🔥 Devuelve su estado correcto en Vista Normal
        }}
        
        btn.innerHTML = "VISTA EXCEL";
        if(excel) excel.style.display = "none";
        
        // Restaurar bloques de pestañas
        ["polys-1", "polys-2", "polys-4", "polys-5", "polys-6", "polys-7", "polys-8", "polys-9"].forEach(id => {{
            let el = document.getElementById(id);
            if(el) el.style.display = (id === "polys-" + currentTab) ? "block" : "none";
        }});
        
        // 📊 RESTAURACIÓN INTELIGENTE: Devolvemos la visibilidad al contador que corresponda según la pestaña activa
        if (contScp1 && contSja1) {{
            if (currentTab == 2) {{
                contScp1.style.display = 'block';
                contSja1.style.display = 'none';
            }} else if (currentTab == 6) {{
                contScp1.style.display = 'none';
                contSja1.style.display = 'block';
            }} else {{
                contScp1.style.display = 'none';
                contSja1.style.display = 'none';
            }}
        }}

        // RESTAURACIÓN FORZADA:
        // 1. Quitar el 'display: none' de las filas ocultas
        idsAocultar.forEach(id => {{
            let el = document.getElementById(id);
            if(el) {{
                let fila = el.closest('tr');
                if(fila) fila.style.removeProperty('display');
            }}
        }});
        // 2. Obligar a las filas del tfoot a mostrarse
        document.querySelectorAll('.meli-table tfoot tr').forEach(fila => {{
            fila.style.setProperty('display', 'table-row', 'important');
            actualizarVisibilidadContador();
        }});
    }}
}}



function generarExcelPolys() {{
    let body = document.getElementById("excel-polys-body");
    if(!body) return;

    body.innerHTML = "";
    let tabId = currentTab;
    document.querySelectorAll('#polys-' + tabId + ' .poligono-bloque').forEach(bl => {{
        let plan = bl.querySelector('tbody tr td')?.innerText.trim() || "";
        let vol = bl.querySelector('.v-total-val')?.innerText.trim() || "0";

        let nodoExcel = bl.querySelector('.nodos-val')?.innerText.trim() ||
                        bl.querySelector('.nodos-campeche')?.innerText.trim() || "0";
        let nodoTxt = (parseInt(nodoExcel) || 0) > 0 ? nodoExcel : "-";

        let filasCalc = Array.from(bl.querySelectorAll('.calc-row'));
        let filasValidas = filasCalc.filter(r => {{
            let u = r.querySelector('.s-type')?.value || "";
            return u !== "" && u !== "Seleccionar...";
        }});

        if (filasValidas.length === 0) return;

        filasValidas.forEach((r, index) => {{
            let unidad = r.querySelector('.s-type')?.value || "";
            let asignadas = r.querySelector('.u-manual')?.innerText.trim() || "0";

            let fRows = Array.from(document.querySelectorAll('#body-' + tabId + ' tr'));
            let fRow = fRows.find(fr => fr.querySelector('.edit-name')?.innerText.trim() === unidad);
            let valSpr = "-";

            

            let filaHtml = '<tr>';
            if (index === 0) {{
                filaHtml += `
                    <td rowspan="${{filasValidas.length}}" style="border:1px solid #808080; padding:3px; text-align:center; font-weight:bold; vertical-align:middle;">${{plan}}</td>
                    <td rowspan="${{filasValidas.length}}" style="border:1px solid #808080; text-align:center; font-weight:bold; vertical-align:middle;">${{vol}}</td>
                `;
            }}
            filaHtml += `
                <td style="border:1px solid #808080; padding-left:6px; vertical-align:middle;">${{unidad}}</td>
                <td style="border:1px solid #808080; text-align:center; vertical-align:middle; font-weight:bold;">${{asignadas}}</td>
            `;
            if (index === 0) {{
                filaHtml += `<td rowspan="${{filasValidas.length}}" style="border:1px solid #808080; text-align:center; font-weight:bold; vertical-align:middle;">${{nodoTxt}}</td>`;
            }}
            filaHtml += '</tr>';
            body.innerHTML += filaHtml;
        }});
    }});

    let valRuteadasNormal = document.getElementById('total-ruteadas-' + tabId)?.innerText || "0";
    let celdaTotalExcel = document.getElementById('excel-total-ruteadas-naranja');
    if(celdaTotalExcel) celdaTotalExcel.innerText = valRuteadasNormal;

    let tablaActual = document.querySelector('#tab-' + tabId + ' table');
    if (tablaActual) {{
        let filasFooter = tablaActual.querySelectorAll('tfoot tr');
        filasFooter.forEach(fila => {{
            if (!fila.innerText.includes("TOTAL RUTEADAS")) {{
                fila.style.display = 'none';
            }}
        }});
    }}
}}




function obtenerCarFlexible() {{

    const opciones = [
        "Car - 8h",
        "Car - 5h",
        "Car - 3h"
    ];

    for (let nombre of opciones) {{

        let unidad = fleet.find(f =>
            f.nombre === nombre &&
            f.stock > 0
        );

        if (unidad) {{
            return unidad;
        }}
    }}

    return null;

}}





function distribuirAutomatico() {{

    // ==============================================================================
    // ⚙️ SECCIÓN 1: CAPTURA DE DATOS EN PANTALLA Y CONFIGURACIÓN INICIAL
    // ==============================================================================
    
    // 1.1 LEER FLOTA DISPONIBLE DESDE LA TABLA SUPERIOR ACTIVA
    let fleet = [];
    document.querySelectorAll('#body-' + currentTab + ' tr').forEach(row => {{
        let nombre = row.querySelector('.edit-name')?.innerText.trim();
        let sprMax = parseFloat(row.querySelector('.edit-spr-max')?.innerText) || 0;
        let stock = parseInt(row.querySelector('.f-stock')?.innerText) || 0;

        if (nombre && nombre !== "IGNORAR" && stock > 0) {{
            fleet.push({{
                nombre: nombre,
                spr: sprMax,
                stock: stock,
                restante: stock
            }});
        }}
    }});

    // 1.2 DESCONTAR DEL INVENTARIO LO QUE YA INGRESASTE MANUALMENTE EN LOS POLÍGONOS
    document.querySelectorAll('#polys-' + currentTab + ' .calc-row').forEach(r => {{
        let tipo = r.querySelector('.s-type')?.value;
        let unidades = parseInt(r.querySelector('.u-manual')?.innerText) || 0;

        if (tipo && tipo !== "Seleccionar..." && unidades > 0) {{
            let unidadReal = fleet.find(f => f.nombre === tipo);
            if (unidadReal) {{
                unidadReal.restante -= unidades;
            }}
        }}
    }});

    console.log("FLEET DISPONIBLE EN PESTAÑA ACTIVA:", fleet.map(f => f.nombre));

    // 1.3 ORDENAR FLOTA POR CAPACIDAD (MAYOR SPR) REGLA NATIVA
    fleet.sort((a, b) => b.spr - a.spr);

    // 1.4 CAPTURAR Y ORDENAR POLÍGONOS POR PRIORIDAD DE NODO/VOLUMEN
    let bloques = Array.from(document.querySelectorAll('#polys-' + currentTab + ' .poligono-bloque'));
    let polys = [];

    bloques.forEach(bl => {{
        let volumen = parseFloat(bl.querySelector('.v-total-val')?.innerText) || 0;
        if (volumen > 0) {{
            polys.push({{
                bloque: bl,
                volumen: volumen
            }});
        }}
    }});

    // 🔒 CONDICIONAL EXCLUSIVA: Solo se aplica si la pestaña activa es C1 SJA1 (ID 6)
    if (currentTab == 6) {{
        polys.sort((a, b) => {{
            let nameA = a.bloque.querySelector('td[rowspan]')?.innerText?.toUpperCase()?.trim() || "";
            let nameB = b.bloque.querySelector('td[rowspan]')?.innerText?.toUpperCase()?.trim() || "";
            
            let esPrioritarioA = (nameA === "PEROTE" || nameA === "TLALTETELA") ? 1 : 0;
            let esPrioritarioB = (nameB === "PEROTE" || nameB === "TLALTETELA") ? 1 : 0;
            
            // Coloca a Perote y Tlaltetela al principio del arreglo
            return esPrioritarioB - esPrioritarioA;
        }});
    }}


    // ==============================================================================
    // 🚚 SECCIÓN 2: BLOQUE DE PREASIGNACIONES ESPECÍFICAS (PASO 1 DEL MOTOR)
    // ==============================================================================
    
    // --- 🟢 CARRIL PESTAÑA 1: PREC SMX5 ---
    if (currentTab == 1) {{
        let small9h = fleet.find(f => f.nombre === "Small 9h Ext Car");
        if (small9h && small9h.restante > 0) {{
            let planesPrioridad = ["IZTAPALAPA", "COYOACÁN"];
            planesPrioridad.forEach(nombreBuscado => {{
                let polyPlan = polys.find(p => (p.bloque.querySelector('td[rowspan]')?.innerText?.trim()?.toUpperCase() || "") === nombreBuscado);
                if (!polyPlan) return;

                let objetivo = parseFloat(polyPlan.bloque.querySelector('.v-total-val')?.innerText) || 0;
                let yaAsignado = 0;
                polyPlan.bloque.querySelectorAll('.calc-row').forEach(r => {{
                    yaAsignado += (parseInt(r.querySelector('.u-manual')?.innerText) || 0) * (parseFloat(r.querySelector('.spr-real-val')?.innerText) || 0);
                }});

                let restante = objetivo - yaAsignado;
                if (restante <= 0) return;

                let usar = Math.min(Math.ceil(restante / small9h.spr), small9h.restante);
                if (usar <= 0) return;

                let filaLibre = Array.from(polyPlan.bloque.querySelectorAll('.calc-row')).find(f => {{
                    let tipo = f.querySelector('.s-type')?.value?.trim() || "";
                    let unidades = parseInt(f.querySelector('.u-manual')?.innerText) || 0;
                    return unidades === 0 && (tipo === "" || tipo === "Seleccionar...");
                }});

                if (filaLibre) {{
                    filaLibre.querySelector('.s-type').value = small9h.nombre;
                    filaLibre.querySelector('.u-manual').innerText = usar;
                    filaLibre.querySelector('.spr-real-val').innerText = small9h.spr;
                    editedRowsPlan.add(filaLibre);
                    small9h.restante -= usar;
                }}
            }});

            // Asignación de stock sobrante a Tláhuac
            if (small9h.restante > 0) {{
                polys.forEach(polyPlan => {{
                    if (small9h.restante <= 0) return;
                    let nombrePlan = polyPlan.bloque.querySelector('td[rowspan]')?.innerText?.trim()?.toUpperCase() || "";
                    if (nombrePlan !== "TLAHUAC") return;

                    let objetivo = parseFloat(polyPlan.bloque.querySelector('.v-total-val')?.innerText) || 0;
                    let yaAsignado = 0;
                    polyPlan.bloque.querySelectorAll('.calc-row').forEach(r => {{
                        yaAsignado += (parseInt(r.querySelector('.u-manual')?.innerText) || 0) * (parseFloat(r.querySelector('.spr-real-val')?.innerText) || 0);
                    }});

                    let restante = objetivo - yaAsignado;
                    if (restante <= 0) return;

                    let usar = Math.min(Math.ceil(restante / small9h.spr), small9h.restante);
                    if (usar <= 0) return;

                    let filaLibre = Array.from(polyPlan.bloque.querySelectorAll('.calc-row')).find(f => {{
                        let tipo = f.querySelector('.s-type')?.value?.trim() || "";
                        let unidades = parseInt(f.querySelector('.u-manual')?.innerText) || 0;
                        return unidades === 0 && (tipo === "" || tipo === "Seleccionar...");
                    }});

                    if (filaLibre) {{
                        filaLibre.querySelector('.s-type').value = small9h.nombre;
                        filaLibre.querySelector('.u-manual').innerText = usar;
                        filaLibre.querySelector('.spr-real-val').innerText = small9h.spr;
                        editedRowsPlan.add(filaLibre);
                        small9h.restante -= usar;
                    }}
                }});
            }}
        }}
    }}

    // --- 🟡 CARRIL PESTAÑA 5: PREC SMX2 ---
    if (currentTab == 5) {{
        // Preasignación Small Van SDD
        let smallVan = fleet.find(f => f.nombre === "Small Van SDD");
        if (smallVan && smallVan.restante > 0) {{
            let planesPrioridad = ["IZTAPALAPA 1", "IZTAPALAPA 2", "LA PAZ"];
            planesPrioridad.forEach(nombreBuscado => {{
                let polyPlan = polys.find(p => (p.bloque.querySelector('td[rowspan]')?.innerText?.trim()?.toUpperCase() || "") === nombreBuscado);
                if (!polyPlan) return;

                let objetivo = parseFloat(polyPlan.bloque.querySelector('.v-total-val')?.innerText) || 0;
                let yaAsignado = 0;
                polyPlan.bloque.querySelectorAll('.calc-row').forEach(r => {{
                    yaAsignado += (parseInt(r.querySelector('.u-manual')?.innerText) || 0) * (parseFloat(r.querySelector('.spr-real-val')?.innerText) || 0);
                }});

                let restante = objetivo - yaAsignado;
                if (restante <= 0) return;

                let usar = Math.min(Math.ceil(restante / smallVan.spr), smallVan.restante);
                if (usar <= 0) return;

                let filaLibre = Array.from(polyPlan.bloque.querySelectorAll('.calc-row')).find(f => {{
                    let tipo = f.querySelector('.s-type')?.value?.trim() || "";
                    let unidades = parseInt(f.querySelector('.u-manual')?.innerText) || 0;
                    return unidades === 0 && (tipo === "" || tipo === "Seleccionar...");
                }});

                if (filaLibre) {{
                    filaLibre.querySelector('.s-type').value = smallVan.nombre;
                    filaLibre.querySelector('.u-manual').innerText = usar;
                    filaLibre.querySelector('.spr-real-val').innerText = smallVan.spr;
                    editedRowsPlan.add(filaLibre);
                    smallVan.restante -= usar;
                }}
            }});

            // Sobrante de Small Van a Chimas
            if (smallVan.restante > 0) {{
                polys.forEach(polyPlan => {{
                    if (smallVan.restante <= 0) return;
                    let nombrePlan = polyPlan.bloque.querySelector('td[rowspan]')?.innerText?.trim()?.toUpperCase() || "";
                    if (!nombrePlan.includes("CHIMAS")) return;

                    let objetivo = parseFloat(polyPlan.bloque.querySelector('.v-total-val')?.innerText) || 0;
                    let yaAsignado = 0;
                    polyPlan.bloque.querySelectorAll('.calc-row').forEach(r => {{
                        yaAsignado += (parseInt(r.querySelector('.u-manual')?.innerText) || 0) * (parseFloat(r.querySelector('.spr-real-val')?.innerText) || 0);
                    }});

                    let restante = objetivo - yaAsignado;
                    if (restante <= 0) return;

                    let usar = Math.min(Math.ceil(restante / smallVan.spr), smallVan.restante);
                    if (usar <= 0) return;

                    let filaLibre = Array.from(polyPlan.bloque.querySelectorAll('.calc-row')).find(f => {{
                        let tipo = f.querySelector('.s-type')?.value?.trim() || "";
                        let unidades = parseInt(f.querySelector('.u-manual')?.innerText) || 0;
                        return unidades === 0 && (tipo === "" || tipo === "Seleccionar...");
                    }});

                    if (filaLibre) {{
                        filaLibre.querySelector('.s-type').value = smallVan.nombre;
                        filaLibre.querySelector('.u-manual').innerText = usar;
                        filaLibre.querySelector('.spr-real-val').innerText = smallVan.spr;
                        editedRowsPlan.add(filaLibre);
                        smallVan.restante -= usar;
                    }}
                }});
            }}
        }}

        // Preasignación Car Zona Extendida
        let CarZonaExtendida = fleet.find(f => f.nombre === "Car Zona Extendida");
        if (CarZonaExtendida && CarZonaExtendida.restante > 0) {{
            let planesPrioridad = ["PUEBLOS", "TEXCOCO"];
            planesPrioridad.forEach(nombreBuscado => {{
                let polyPlan = polys.find(p => (p.bloque.querySelector('td[rowspan]')?.innerText?.trim()?.toUpperCase() || "") === nombreBuscado);
                if (!polyPlan) return;

                let objetivo = parseFloat(polyPlan.bloque.querySelector('.v-total-val')?.innerText) || 0;
                let yaAsignado = 0;
                polyPlan.bloque.querySelectorAll('.calc-row').forEach(r => {{
                    yaAsignado += (parseInt(r.querySelector('.u-manual')?.innerText) || 0) * (parseFloat(r.querySelector('.spr-real-val')?.innerText) || 0);
                }});

                let restante = objetivo - yaAsignado;
                if (restante <= 0) return;

                let usar = Math.min(Math.ceil(restante / CarZonaExtendida.spr), CarZonaExtendida.restante);
                if (usar <= 0) return;

                let filaLibre = Array.from(polyPlan.bloque.querySelectorAll('.calc-row')).find(f => {{
                    let tipo = f.querySelector('.s-type')?.value?.trim() || "";
                    let unidades = parseInt(f.querySelector('.u-manual')?.innerText) || 0;
                    return unidades === 0 && (tipo === "" || tipo === "Seleccionar...");
                }});

                if (filaLibre) {{
                    filaLibre.querySelector('.s-type').value = CarZonaExtendida.nombre;
                    filaLibre.querySelector('.u-manual').innerText = usar;
                    filaLibre.querySelector('.spr-real-val').innerText = CarZonaExtendida.spr;
                    editedRowsPlan.add(filaLibre);
                    CarZonaExtendida.restante -= usar;
                }}
            }});

            // Sobrante de Car Zona Extendida a Chalco
            if (CarZonaExtendida.restante > 0) {{
                let chalco = polys.find(p => (p.bloque.querySelector('td[rowspan]')?.innerText?.trim()?.toUpperCase() || "") === "CHALCO");
                if (chalco) {{
                    let filaLibre = Array.from(chalco.bloque.querySelectorAll('.calc-row')).find(f => {{
                        let tipo = f.querySelector('.s-type')?.value?.trim() || "";
                        let unidades = parseInt(f.querySelector('.u-manual')?.innerText) || 0;
                        return unidades === 0 && (tipo === "" || tipo === "Seleccionar...");
                    }});
                    if (filaLibre) {{
                        filaLibre.querySelector('.s-type').value = CarZonaExtendida.nombre;
                        filaLibre.querySelector('.u-manual').innerText = CarZonaExtendida.restante;
                        filaLibre.querySelector('.spr-real-val').innerText = CarZonaExtendida.spr;
                        editedRowsPlan.add(filaLibre);
                        CarZonaExtendida.restante = 0;
                    }}
                }}
            }}
        }}
    }}


    // --- 🔵 CARRIL PESTAÑA 2: C1 BASE / SCP1 (Incluye Campeche y sus Dedicadas) ---
    if (currentTab == 2) {{
        // Preasignación Large Van MLP
        let largeVanMLP = fleet.find(f => f.nombre === "Large Van MLP");
        if (largeVanMLP && largeVanMLP.restante > 0) {{
            let planesPrioridad = ["ESCÁRCEGA", "ESCÁRCEGA EXT", "MAXCANUN", "CANDELARIA", "SEYBAPLAYA", "CHAMPOTÓN", "HOLPECHEN"];
            planesPrioridad.forEach(nombreBuscado => {{
                let polyPlan = polys.find(p => (p.bloque.querySelector('td[rowspan]')?.innerText?.trim()?.toUpperCase() || "") === nombreBuscado);
                if (!polyPlan) return;

                let objetivo = parseFloat(polyPlan.bloque.querySelector('.v-total-val')?.innerText) || 0;
                let yaAsignado = 0;
                polyPlan.bloque.querySelectorAll('.calc-row').forEach(r => {{
                    yaAsignado += (parseInt(r.querySelector('.u-manual')?.innerText) || 0) * (parseFloat(r.querySelector('.spr-real-val')?.innerText) || 0);
                }});

                let restante = objetivo - yaAsignado;
                if (restante <= 0) return;

                let usar = Math.min(Math.ceil(restante / largeVanMLP.spr), largeVanMLP.restante);
                if (usar <= 0) return;

                let filaLibre = Array.from(polyPlan.bloque.querySelectorAll('.calc-row')).find(f => {{
                    let tipo = f.querySelector('.s-type')?.value?.trim() || "";
                    let unidades = parseInt(f.querySelector('.u-manual')?.innerText) || 0;
                    return unidades === 0 && (tipo === "" || tipo === "Seleccionar...");
                }});

                if (filaLibre) {{
                    filaLibre.querySelector('.s-type').value = largeVanMLP.nombre;
                    filaLibre.querySelector('.u-manual').innerText = usar;
                    filaLibre.querySelector('.spr-real-val').innerText = largeVanMLP.spr;
                    editedRowsPlan.add(filaLibre);
                    largeVanMLP.restante -= usar;
                }}
            }});
        }}

        // Preasignación Exclusiva de Delivery Cell para los Nodos de CAMPECHE
        let deliveryCell = fleet.find(f => f.nombre === "Delivery Cell Large Van");
        if (deliveryCell && deliveryCell.restante > 0) {{
            let campeche = polys.find(p => (p.bloque.querySelector('td[rowspan]')?.innerText?.trim()?.toUpperCase() || "") === "CAMPECHE");
            if (campeche) {{
                let nodos = parseInt(campeche.bloque.querySelector('.nodos-campeche')?.innerText) || 0;
                if (nodos > 0) {{
                    let filaLibre = Array.from(campeche.bloque.querySelectorAll('.calc-row')).find(f => {{
                        let tipo = f.querySelector('.s-type')?.value?.trim() || "";
                        let unidades = parseInt(f.querySelector('.u-manual')?.innerText) || 0;
                        return unidades === 0 && (tipo === "" || tipo === "Seleccionar...");
                    }});
                    if (filaLibre) {{
                        filaLibre.querySelector('.s-type').value = deliveryCell.nombre;
                        filaLibre.querySelector('.u-manual').innerText = 1;
                        filaLibre.querySelector('.spr-real-val').innerText = deliveryCell.spr;
                        editedRowsPlan.add(filaLibre);
                        deliveryCell.restante -= 1;
                    }}
                }}
            }}
        }}
    }}


    // ==============================================================================
    // 🎛️ SECCIÓN 3: MOTOR DE DISTRIBUCIÓN PRINCIPAL POR PESTAÑA (PASO 2 DEL MOTOR)
    // ==============================================================================
    if (currentTab == 6) {{
        // 🚀 EJECUTA EL NUEVO MOTOR EN CARRIL AISLADO PARA C1 SJA1
        polys.forEach(poly => {{
            procesarAsignacionUnidadSJA1(poly);
        }});
    }} else {{
        // 🔴 OPERACIÓN ORIGINAL PARA EL RESTO DE LAS PESTAÑAS (C1 SCP1, SDE, PREC)
        polys.forEach(poly => {{
            let bloque = poly.bloque;
            let nombrePlan = bloque.querySelector('td[rowspan]')?.innerText?.toUpperCase()?.trim() || "";
            let objetivo = parseFloat(bloque.querySelector('.v-total-val')?.innerText) || 0;

            let yaAsignado = 0;
            bloque.querySelectorAll('.calc-row').forEach(r => {{
                yaAsignado += (parseInt(r.querySelector('.u-manual')?.innerText) || 0) * (parseFloat(r.querySelector('.spr-real-val')?.innerText) || 0);
            }});

            let restante = objetivo - yaAsignado;
            if (restante <= 0) return;

            let filas = Array.from(bloque.querySelectorAll('.calc-row'));
            for (let fila of filas) {{
                let yaTieneUnidad = parseInt(fila.querySelector('.u-manual')?.innerText) > 0;
                let tipoActual = fila.querySelector('.s-type')?.value?.trim() || "";
                let yaTieneTipo = tipoActual !== "" && tipoActual !== "Seleccionar...";

                if (yaTieneUnidad || yaTieneTipo) continue;
                if (restante <= 0) break;

                let unidad = null;

                // Regla Nativa de Flota para Pestaña 2 (Asignación General vs Campeche)
                if (currentTab == 2 && nombrePlan == "CAMPECHE") {{
                    unidad = fleet.find(f => f.nombre === "Rental Large Van");
                }} else if (currentTab == 2) {{
                    unidad = fleet.find(f => f.restante > 0 && f.nombre !== "Rental Large Van");
                }} else {{
                    unidad = fleet.find(f => f.restante > 0);
                }}

                // Desborde de Emergencia Tradicional Nativo (Si se vacía el stock principal)
                if (!unidad) {{
                    if (currentTab == 4) {{ // SDE
                        let options = ["Car - 5h", "Car - 3h"];
                        for (let opt of options) {{
                            unidad = fleet.find(f => f.nombre.includes(opt));
                            if (unidad) break;
                        }}
                    }} else if (currentTab == 7) {{ // C1 SCH1
                        let options = ["Car - 8h"];
                        for (let opt of options) {{
                            unidad = fleet.find(f => f.nombre.includes(opt));
                            if (unidad) break;
                        }}
                    }} else if (currentTab == 8) {{ // C1 SMD2
                        let options = ["Car - 8h"];
                        for (let opt of options) {{
                            unidad = fleet.find(f => f.nombre.includes(opt));
                            if (unidad) break;
                        }}
                    }} else if (currentTab == 2) {{ // C1 SCP1
                        let options = ["Large Van MLP", "Car - 8h", "Car - 5h"];
                        for (let opt of options) {{
                            unidad = fleet.find(f => f.nombre.includes(opt));
                            if (unidad) break;
                        }}
                    }} else if (currentTab == 1 || currentTab == 5) {{ // PRECARGAS
                        let options = ["Car - 8h", "Car - 5h"];
                        for (let opt of options) {{
                            unidad = fleet.find(f => f.nombre.includes(opt));
                            if (unidad) break;
                        }}
                    }}
                    if (!unidad) break;
                }}

                // MATEMÁTICA TRADICIONAL DE REPARTO REAL NATIVO
                let necesarias = Math.ceil(restante / unidad.spr);
                let usar;

                let permiteNegativo = unidad.nombre === "Car - 8h" || unidad.nombre === "Car - 5h" || unidad.nombre === "Car - 3h" || (currentTab == 2 && unidad.nombre === "Large Van MLP");
                if (unidad.restante > 0) {{
                    usar = Math.min(necesarias, unidad.restante);
                }} else if (permiteNegativo) {{
                    usar = necesarias;
                }} else {{
                    usar = 0;
                }}

                if (usar <= 0) continue;

                let filaExistente = filas.find(f => f.querySelector('.s-type')?.value === unidad.nombre);
                if (filaExistente) {{
                    let actual = parseInt(filaExistente.querySelector('.u-manual')?.innerText) || 0;
                    filaExistente.querySelector('.u-manual').innerText = actual + usar;
                    filaExistente.querySelector('.spr-real-val').innerText = unidad.spr;
                    editedRowsPlan.add(filaExistente);
                }} else {{
                    fila.querySelector('.s-type').value = unidad.nombre;
                    fila.querySelector('.u-manual').innerText = usar;
                    fila.querySelector('.spr-real-val').innerText = unidad.spr;
                    editedRowsPlan.add(fila);
                }}

                unidad.restante -= usar;
                restante -= (usar * unidad.spr);
            }}
        }});
    }}


// ==============================================================================
// 🔥 SECCIÓN 4: MOTOR EXCLUSIVO CON NUEVAS PRIORIDADES PARA C1 SJA1 (TAB 6)
// ==============================================================================
function procesarAsignacionUnidadSJA1(poly) {{
    let bloque = poly.bloque;
    let nombrePlan = bloque.querySelector('td[rowspan]')?.innerText?.toUpperCase()?.trim() || "";
    let objetivo = parseFloat(bloque.querySelector('.v-total-val')?.innerText) || 0;

    let yaAsignado = 0;
    bloque.querySelectorAll('.calc-row').forEach(r => {{
        let unidades = parseInt(r.querySelector('.u-manual')?.innerText) || 0;
        let spr = parseFloat(r.querySelector('.spr-real-val')?.innerText) || 0;
        yaAsignado += (unidades * spr);
    }});

    let restante = objetivo - yaAsignado;
    if (restante <= 0) return;

    let filas = Array.from(bloque.querySelectorAll('.calc-row'));
    for (let fila of filas) {{
        let yaTieneUnidad = parseInt(fila.querySelector('.u-manual')?.innerText) > 0;
        let tipoActual = fila.querySelector('.s-type')?.value?.trim() || "";
        let yaTieneTipo = tipoActual !== "" && tipoActual !== "Seleccionar...";

        if (yaTieneUnidad || yaTieneTipo) continue;
        if (restante <= 0) break;

        let unidad = null;

        // 4.1 PRIORIDAD PLANES LOCALES: "CENTRO 1" Y "CENTRO 2"
        if (nombrePlan === "⚠️ CENTRO 1" || nombrePlan === "⚠️ CENTRO 2") {{
            
            if (nombrePlan === "⚠️ CENTRO 1") {{
                const listaEspecialesC1 = [
                    "Extra Large Van MLP H&B", 
                    "Truck 3.5 tons MLP", 
                    "Delivery Cell Large Van"
                ];
                
                for (let nombre of listaEspecialesC1) {{
                    unidad = fleet.find(f => f.restante > 0 && f.nombre.toLowerCase() === nombre.toLowerCase());
                    if (unidad) break;
                }}

                if (!unidad) {{
                    const listaRental = ["Rental Electric Large Van", "Rental Large Van", "Rental Replacement"];
                    for (let nombre of listaRental) {{
                        unidad = fleet.find(f => f.restante > 0 && f.nombre.toLowerCase().includes(nombre.toLowerCase()));
                        if (unidad) break;
                    }}
                }}

            }} else if (nombrePlan === "⚠️ CENTRO 2") {{
                const listaRental = ["Rental Electric Large Van", "Rental Large Van", "Rental Replacement"];
                for (let nombre of listaRental) {{
                    unidad = fleet.find(f => f.restante > 0 && f.nombre.toLowerCase().includes(nombre.toLowerCase()));
                    if (unidad) break;
                }}
            }}
        }}

        // 4.2 PLAN ESPECÍFICO: EJA1 SP (Media Milla SP)
        else if (nombrePlan.includes("EJA1 SP") || nombrePlan.includes("EJA1")) {{
            unidad = fleet.find(f => f.restante > 0 && (f.nombre.toLowerCase().includes("media milla sp") || f.nombre.toLowerCase().includes("media milla")));
        }}

        // 4.3 CASOS ESPECÍFICOS PARA XICO Y TUZAMAPA
        else if (nombrePlan === "XICO" || nombrePlan === "TUZAMAPA") {{
            unidad = fleet.find(f => f.restante > 0 && f.nombre.toLowerCase().includes("large van mlp foráneo"));

            if (!unidad) {{
                unidad = fleet.find(f => f.restante > 0 && f.nombre.toLowerCase().includes("small van mlp foráneo"));
            }}

            if (!unidad) {{
                let listaSustitutas = [
                    "car 8h", 
                    "car newbie", 
                    "car zona extendida", 
                    "small van 9h", 
                    "small van 9h ext", 
                    "small van newbie", 
                    "moto 3h"
                ];
                for (let palabra of listaSustitutas) {{
                    unidad = fleet.find(f => f.restante > 0 && f.nombre.toLowerCase().includes(palabra));
                    if (unidad) break;
                }}
            }}
        }}

        // 4.4 🌟 PRIORIDAD MÁXIMA FORÁNEA: PEROTE Y TLALTETELA (FORÁNEOS CON NODO)
        else if (nombrePlan === "PEROTE" || nombrePlan === "TLALTETELA") {{
            // Exigen llenar con Large Van MLP foráneo para soportar los nodos
            unidad = fleet.find(f => f.restante > 0 && f.nombre.toLowerCase().includes("large van mlp foráneo"));

            // Si se agotan, pasan a Small Van como respaldo
            if (!unidad) {{
                unidad = fleet.find(f => f.restante > 0 && f.nombre.toLowerCase().includes("small van mlp foráneo"));
            }}
        }}

        // 4.5 RESTO DE PLANES FORÁNEOS GENERALES
        else {{
            unidad = fleet.find(f => f.restante > 0 && f.nombre.toLowerCase().includes("large van mlp foráneo"));
            
            if (!unidad) {{
                unidad = fleet.find(f => f.restante > 0 && f.nombre.toLowerCase().includes("small van mlp foráneo"));
            }}
        }}

        if (!unidad) break;

        // MATEMÁTICA DE ASIGNACIÓN REGULAR PARA SJA1
        let necesarias = Math.ceil(restante / unidad.spr);
        let usar = (unidad.restante > 0) ? Math.min(necesarias, unidad.restante) : 0;

        if (usar <= 0) continue;

        let filaExistente = filas.find(f => f.querySelector('.s-type')?.value === unidad.nombre);
        if (filaExistente) {{
            let actual = parseInt(filaExistente.querySelector('.u-manual')?.innerText) || 0;
            filaExistente.querySelector('.u-manual').innerText = actual + usar;
            filaExistente.querySelector('.spr-real-val').innerText = unidad.spr;
            editedRowsPlan.add(filaExistente);
        }} else {{
            fila.querySelector('.s-type').value = unidad.nombre;
            fila.querySelector('.u-manual').innerText = usar;
            fila.querySelector('.spr-real-val').innerText = unidad.spr;
            editedRowsPlan.add(fila);
        }}

        unidad.restante -= usar;
        restante -= (usar * unidad.spr);
    }}
}}




    // ============================================================================================
    // 📊 SECCIÓN 5: RECALCULAR COMPLETO Y REFRESCAR TOTALES// TERMINA DISTRIBUIDOR AUTOMATICO
    // ============================================================================================
    recalc();
}}





function actualizarTotales() {{
        // La lógica fue movida a updateFleetFloat() 
        return;
    }}


// --- AQUÍ PEGA LA FUNCIÓN NUEVA ---
    function updateSelectColor(selectElement) {{
        if (selectElement.value === "") {{
            selectElement.style.color = "#A9A9A9"; // Gris
        }} else {{
            selectElement.style.color = "#25282b"; // Negro
        }}
    }}


function updateFleetFloat() {{
    let htmlLeft = "";
    let htmlRight = "";

    let totalMLPReal = 0;       // Ruteadas (Usadas)
    let totalMLPStock = 0;      // Declaradas (Sched)

    let totalRentalReal = 0;    // Ruteadas (Usadas)
    let totalRentalStock = 0;   // Declaradas (Sched)

    let totalCarReal = 0;       // Ruteadas
    let totalCarSchedule = 0;   // Declaradas
    let totalNoCar = 0;         // El total original de MLP que tu código ya calculaba

    // ⬇️ BUCLE DE ACTUALIZACIÓN
    document.querySelectorAll('#body-' + currentTab + ' tr').forEach(row => {{
        let name = row.querySelector('.edit-name')?.innerText.trim();
        let stock = parseInt(row.querySelector('.f-stock')?.innerText) || 0;
        
        // 🔥 LEEMOS DIRECTAMENTE LO QUE DICE EN "USADAS"
        let asignado = parseInt(row.querySelector('.f-ruteadas')?.innerText) || 0;

        if(name && (stock > 0 || asignado > 0)) {{
            let nameLower = name.toLowerCase();

            // 🔥 EXCLUSIÓN EXPLÍCITA: Ignorar "Extra Large Van MLP H&B" y "Truck 3.5 tons MLP" de los cálculos MLP
            let esExtraLargeMLP = nameLower.includes("extra large van mlp h&b") || nameLower.includes("extra large van mlp h & b");
            let esTruck35MLP = nameLower.includes("truck 3.5 tons mlp") || nameLower.includes("truck 3.5 ton mlp");
            let debeExcluirMLP = esExtraLargeMLP || esTruck35MLP;

            // 1. CONTEO DE CARS (Ajustado para evitar falsos positivos)
            let esCarStrict = (
                (nameLower.includes("car") || nameLower.includes("moto") || nameLower.includes("small van") || nameLower.includes("newbie")) &&
                !nameLower.includes("mlp") && !nameLower.includes("van grande") && !nameLower.includes("large van")
            );

            if (esCarStrict) {{
                totalCarSchedule += stock;
            }}

            // 2. CONTEO DE MLP (Excluyendo explícitamente las unidades añadidas)
            if (name.includes("MLP") && !debeExcluirMLP) {{
                totalMLPStock += stock;
                totalMLPReal += asignado;
            }}

            // 3. CONTEO DE RENTALS
            if (nameLower.includes("rental")) {{
                totalRentalStock += stock;
                totalRentalReal += asignado;
            }}

            let colorCategoria = esCarStrict ? "#FF4500" : "#0000CD";

            // 🔥 SUMA DIRECTA DE LA COLUMNA USADAS 
            if (esCarStrict) {{
                totalCarReal += asignado;
            }} else {{
                if (!debeExcluirMLP && (name === "Large Van MLP" || name === "Small Van MLP" || name.includes("foráneo"))) {{
                    totalNoCar += asignado;
                }}
            }}

            let leftDisplay = row.querySelector('.f-left')?.innerText || "0";

            htmlLeft += `
                <div style="display:flex; justify-content:space-between; margin-bottom:4px; font-size:14px;"> 
                    <span style="color:#0a2745;">${{name}}</span>
                    <span style="color:${{colorCategoria}}; font-weight:bold;">${{leftDisplay}}/${{stock}}</span>
                </div>
            `;
        }}
    }});

    // Columna derecha flotante: Desglose Declaradas vs Ruteadas
    htmlRight = `
        <div style="margin-top: 5px; padding-top: 5px;"> 
            <div style="display:flex; justify-content:space-between; color: #D2691E; font-weight: 800; font-size: 14px;">
                <span>TOTAL CAR (sched):</span> <span>${{totalCarSchedule}}</span>
            </div>
            <div style="display:flex; justify-content:space-between; color: #FF4500; font-weight: 800; font-size: 14px; margin-bottom: 8px;">
                <span>TOTAL CAR (real):</span> <span>${{totalCarReal}}</span>
            </div>

            <div style="border-top: 1px solid #25282b; padding-top: 4px;"></div>

            <div style="display:flex; justify-content:space-between; color: #0000CD; font-weight: 800; font-size: 14px;">
                <span>TOTAL MLP (decl):</span> <span>${{totalMLPStock}}</span>
            </div>
            <div style="display:flex; justify-content:space-between; color: #0000CD; font-weight: 800; font-size: 14px; margin-bottom: 8px;">
                <span>TOTAL MLP (rute):</span> <span>${{totalMLPReal}}</span>
            </div>

            <div style="border-top: 1px solid #25282b; padding-top: 4px;"></div>

            <div style="display:flex; justify-content:space-between; color: #25282b; font-weight: 800; font-size: 14px;">
                <span>TOTAL RENTAL (decl):</span> <span>${{totalRentalStock}}</span>
            </div>
            <div style="display:flex; justify-content:space-between; color: #25282b; font-weight: 800; font-size: 14px;">
                <span>TOTAL RENTAL (rute):</span> <span>${{totalRentalReal}}</span>
            </div>
        </div>
    `;

    let html = `
    <div style="display:flex; gap:15px; align-items:flex-start;">
        <div style="flex:1; min-width:180px;">${{htmlLeft}}</div>
        <div style="width:190px; border-left:2px solid #25282b; padding-left:12px;">${{htmlRight}}</div>
    </div>
    `;

    let elNoCar = document.getElementById('total-no-car-' + currentTab);
    if (elNoCar) {{
        elNoCar.innerText = totalNoCar; 
    }}

    let elCarReal = document.getElementById('total-car-real-' + currentTab);
    if (elCarReal) {{
        elCarReal.innerText = totalCarReal;
    }}

    let totalRuteadas = totalMLPReal + totalCarReal + totalRentalReal; 
    let elRuteadas = document.getElementById('total-ruteadas-' + currentTab);
    if (elRuteadas) {{
        elRuteadas.innerText = totalRuteadas;
    }}

    let elCarSchedule = document.getElementById('total-car-schedule-' + currentTab);
    if (elCarSchedule) {{
        elCarSchedule.innerText = totalCarSchedule;
    }}

    document.getElementById('fleet-float-body').innerHTML = html;

    // Actualización de los cuadritos superiores
    document.getElementById("val-mlp-rute-2").innerText = totalMLPReal;
    document.getElementById("val-rental-rute-2").innerText = totalRentalReal;
    document.getElementById("val-car-rute-2").innerText = totalCarReal;

    if (typeof guardarEstado === 'function') {{ guardarEstado(); }}
}}

aplicarPerfil();
recalc();


// ==============================================================================
//  🚨 PEGA TU FUNCIÓN EXCLUSIVAMENTE EN ESTE ESPACIO VACÍO (FUERA DE LAS OTRAS)
// ==============================================================================
function togglePrioridades() {{
    const panel = document.getElementById('panel-prioridades');
    // Si el top es negativo, lo ponemos en 0 para que baje
    if (panel.style.top === '0px') {{
        panel.style.top = '-600px'; // Se oculta subiendo
    }} else {{
        panel.style.top = '0px';    // Se despliega bajando
    }}
}}








// --- FUNCIÓN DE FILTRADO ---
function actualizarSelects() {{

    const listaPermitidas = [
        "Small Van MLP foráneo",
        "Car 8h",
        "Car - 8h"
    ];

    document.querySelectorAll('.s-type').forEach(select => {{
        let valorActual = select.value;
        select.innerHTML = '<option value="">Seleccionar...</option>';
        
        document.querySelectorAll('#body-' + currentTab + ' tr').forEach(row => {{
            let name = row.querySelector('.edit-name')?.innerText.trim();
            if (!name || name === "IGNORAR") return;
            
            let stock = parseInt(row.querySelector('.f-stock')?.innerText) || 0;
            let left = parseInt(row.querySelector('.f-left')?.innerText) || 0;
            let nameLower = name.toLowerCase();

            let permiteSinStock = listaPermitidas.some(u => nameLower.includes(u));
            
            // Si permite sin stock O aún tiene disponible en patio, la agregamos
            if (permiteSinStock || left > 0 || stock > 0) {{
                let opt = document.createElement('option');
                opt.value = name;
                opt.textContent = name;
                select.appendChild(opt);
            }}
        }});
        select.value = valorActual;
    }});
}}

// Este bloque ahora llama a recalc() en lugar de a actualizarSelects
document.addEventListener('input', (e) => {{
    if (e.target.classList.contains('f-stock') || e.target.classList.contains('u-manual')) {{
        recalc(); 
    }}
}});

// Esto asegura que al cargar la página ya esté filtrado
window.addEventListener('load', () => {{
    actualizarSelects();
    agregarIndicadorSchedule(); // <--- Aquí añadimos la llamada
}});

actualizarDosPorciento();
// ==============================================================================





// ==============================================================================
// NAVEGACIÓN TIPO EXCEL
// ==============================================================================

document.addEventListener("keydown", function(e){{

    const celda = document.activeElement;

    if (!celda || !celda.hasAttribute("contenteditable")) return;

    const fila = celda.closest("tr");
    if (!fila) return;

    const tabla = fila.closest("table");
    if (!tabla) return;

    const filas = Array.from(
        tabla.querySelectorAll("tbody tr")
    );

    const filaIdx = filas.indexOf(fila);

    const celdasFila = Array.from(
        fila.querySelectorAll('[contenteditable="true"]')
    );

    const colIdx = celdasFila.indexOf(celda);

    if(e.key === "ArrowDown"){{
        e.preventDefault();

        const sigFila = filas[filaIdx + 1];

        if(sigFila){{
            const celdas = sigFila.querySelectorAll('[contenteditable="true"]');
            if(celdas[colIdx]) celdas[colIdx].focus();
        }}
    }}

    if(e.key === "ArrowUp"){{
        e.preventDefault();

        const antFila = filas[filaIdx - 1];

        if(antFila){{
            const celdas = antFila.querySelectorAll('[contenteditable="true"]');
            if(celdas[colIdx]) celdas[colIdx].focus();
        }}
    }}

    if(e.key === "ArrowRight"){{
        e.preventDefault();

        if(celdasFila[colIdx + 1]){{
            celdasFila[colIdx + 1].focus();
        }}
    }}

    if(e.key === "ArrowLeft"){{
        e.preventDefault();

        if(celdasFila[colIdx - 1]){{
            celdasFila[colIdx - 1].focus();
        }}
    }}

}});

// ==============================================================================



// =====================================
// SELECCIONAR TODO AL ENTRAR A UNA CELDA
// =====================================

document.addEventListener("focusin", function(e) {{

    const celda = e.target;

    if (!celda.hasAttribute("contenteditable")) return;

    setTimeout(() => {{

        const rango = document.createRange();
        rango.selectNodeContents(celda);

        const seleccion = window.getSelection();
        seleccion.removeAllRanges();
        seleccion.addRange(rango);

    }}, 0);

}});




// ======================================================
// RELOJ Y RUTEOS
// ======================================================

const ruteos = [

    {{
        nombre:"SMX9",
        hora:"16:40"
    }},
    
    {{
        nombre:"SMX5",
        hora:"17:20"
    }},

    {{
        nombre:"SMX2",
        hora:"18:05"
    }},
    
    {{
        nombre:"SMT2",
        hora:"18:40"
    }},
    
    {{
        nombre:"SJA1 C1",
        hora:"23:30"
    }}

];

let ultimaAlerta = "";


function actualizarRelojRuteos() {{
    const ahora = new Date();
    document.getElementById("hora-actual").innerText = ahora.toLocaleTimeString();
    
    let siguiente = null;
    for (let tarea of ruteos) {{
        let partes = tarea.hora.split(":");
        let fechaTarea = new Date();
        fechaTarea.setHours(parseInt(partes[0]), parseInt(partes[1]), 0, 0);
        if (fechaTarea > ahora) {{
            siguiente = {{ tarea, fechaTarea }};
            break;
        }}
    }}

    const elProximo = document.getElementById("proximo-ruteo");
    const elCuenta = document.getElementById("cuenta-regresiva");
    const elHora = document.getElementById("hora-ruteo");

    if (!siguiente) {{
        elProximo.innerText = "Fin del turno";
        if (elHora) elHora.innerText = "--";
        elCuenta.innerText = "--:--";
    }} else {{
        elProximo.innerText = siguiente.tarea.nombre;
        
        // 🕒 AQUÍ SE INYECTA LA HORA AUTOMÁTICAMENTE
        if (elHora) {{
            elHora.innerText = "A LAS " + siguiente.tarea.hora;
        }}
        
        let diff = siguiente.fechaTarea - ahora;
        let mins = Math.floor(diff / 60000);
        let secs = Math.floor((diff % 60000) / 1000);
        
        elCuenta.innerText = String(mins).padStart(2,"0") + ":" + String(secs).padStart(2,"0");
        elCuenta.style.color = mins < 5 ? "#FF0000" : "#7CFFB2";
    }}
}}
setInterval(actualizarRelojRuteos, 1000);
actualizarRelojRuteos();



// ==============================================================================
// FUNCIÓN MOVER VERTICAL CON SOLTADO AUTOMÁTICO (POINTER CAPTURE)
// ==============================================================================
function iniciarArrastreFlotante(e) {{
  const el = document.getElementById("fleet-sticky");
  const handle = document.getElementById("handle-moverse-flotante");
  if (!el || !handle) return;

  // Previene selección accidental de texto
  e.preventDefault();
  e.stopPropagation();

  // 🔒 Amarra el puntero del ratón a la barra para no perder el evento mouseup/pointerup
  if (e.pointerId !== undefined) {{
    try {{
      handle.setPointerCapture(e.pointerId);
    }} catch(err) {{}}
  }}

  const startY = e.clientY;
  const rect = el.getBoundingClientRect();
  const startTop = rect.top;

  handle.style.cursor = "grabbing";

  function enMovimiento(evt) {{
    const dy = evt.clientY - startY;
    let newTop = startTop + dy;

    // Respeta los límites de la pantalla
    const minTop = 10;
    const maxTop = window.innerHeight - el.offsetHeight - 10;
    newTop = Math.max(minTop, Math.min(maxTop, newTop));

    el.style.setProperty("top", newTop + "px", "important");
  }}

  function alSoltar(evt) {{
    handle.style.cursor = "grab";
    
    // 🔓 Libera la captura del puntero
    if (evt && evt.pointerId !== undefined) {{
      try {{
        handle.releasePointerCapture(evt.pointerId);
      }} catch(err) {{}}
    }}

    // Remueve eventos al soltar el clic
    window.removeEventListener("pointermove", enMovimiento, true);
    window.removeEventListener("pointerup", alSoltar, true);
    window.removeEventListener("pointercancel", alSoltar, true);
  }}

  // Escucha los Pointer Events globales
  window.addEventListener("pointermove", enMovimiento, true);
  window.addEventListener("pointerup", alSoltar, true);
  window.addEventListener("pointercancel", alSoltar, true);
}}


    
</script>
</body>
</html>
"""

html(app_html, height=1200, scrolling=True)








import streamlit as st
import streamlit.components.v1 as components

# 1. ENLACE DE IMAGEN (Mapa de regiones)
ID_IMAGEN = "1M4GLEwFzhLrZjV-zmvGrdTQhC6IjwxOJ"
url_final = f"https://drive.google.com/thumbnail?id={ID_IMAGEN}&sz=w1000"

# HTML/CSS: SOLO RELOJ RESTADOR E IMAGEN DE MAPA
html_limpio = f"""
<style>
    body {{ background-color: #25282b; font-family: 'Segoe UI', Tahoma, sans-serif; margin: 0; }}
    .main-box {{ background: #25282b; padding: 10px; display: flex; flex-direction: column; align-items: center; }}
    
    .unified-console {{
        background: #25282b; border-radius: 15px; padding: 15px; 
        margin-bottom: 20px; border: 1px solid #25282b; text-align: center; width: 100%; max-width: 500px;
    }}
    .display-screen {{
        background: #25282b; border-radius: 10px; padding: 10px; margin-bottom: 15px; border: 2px solid #25282b;
    }}
    .btn-3d {{
        background: linear-gradient(145deg, #1e90ff, #1c82e6);
        color: white; border: none; padding: 12px 25px; border-radius: 10px;
        font-weight: bold; cursor: pointer; box-shadow: 0 5px #0a56a3; transition: 0.1s;
    }}
    .btn-3d:active {{ box-shadow: 0 2px #0a56a3; transform: translateY(3px); }}
    
    /* Contenedor del Mapa */
    .map-container {{
        background: #1e1e1e; border-radius: 12px; padding: 15px; 
        width: 100%; max-width: 900px; text-align: center; box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }}
    .map-container img {{
        max-width: 100%; height: auto; border-radius: 8px; border: 2px solid #444;
    }}
</style>

<div class="main-box">
    <!-- Reloj Restador / Consola -->
    <div class="unified-console"> 
        <div class="display-screen">
            <div style="color: #ffffff; font-size: 10px; margin-bottom: 5px;">HORA / RESTADOR / CONVERTIDOR</div>
            <div id="horaReal" style="font-size: 38px; color: #FF00FF; font-family: sans-serif; font-weight: bold;">--:--</div>
        </div>
        <div style="display: flex; justify-content: center; align-items: center; gap: 15px;">
            <div>
                <span style="color: #add8e6; font-size: 11px; display: block;">MINUTOS</span>
                <input type="number" id="minInput" value="10" 
                    style="background: #222; color: #FFE4E1; border: none; padding: 8px; border-radius: 5px; width: 70px; text-align: center; font-size: 20px; font-weight: bold;">
            </div>
            <button class="btn-3d" onclick="ejecutarTodo()">CALCULAR</button>
        </div>
    </div>

    <!-- Imagen del Mapa -->
    <div class="map-container">
        <h3 style="color: #1E90FF; margin-top: 0; margin-bottom: 15px;">🗺️ MAPA OPERATIVO</h3>
        <img src="{url_final}" alt="Mapa de regiones">
    </div>
</div>

<script>
    function ejecutarTodo() {{
        const mins = document.getElementById('minInput').value || 0;
        const ahora = new Date();
        const nuevaFecha = new Date(ahora.getTime() - (mins * 60000));
        const h = String(nuevaFecha.getHours()).padStart(2, '0');
        const m = String(nuevaFecha.getMinutes()).padStart(2, '0');
        document.getElementById('horaReal').innerText = h + ":" + m;
    }}
    ejecutarTodo();
</script>
"""

# RENDERIZADO EN STREAMLIT
st.markdown("---")
components.html(html_limpio, height=850, scrolling=True)
