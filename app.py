import streamlit as st
from streamlit.components.v1 import html 

st.set_page_config(page_title="Monitor Logístico - Liliana García", layout="wide")

# CSS para diseño limpio
st.markdown("""
    <style>
    .block-container {padding: 0rem !important;}
    footer, #MainMenu, header {visibility: hidden;}
    body { background-color: #f5f7f9; }
    </style>
""", unsafe_allow_html=True)

# --- DATOS BASE ---
u_SDE = {"Moto - 3h": [25, 28], "Car - 5h": [25, 28], "Car - 5h Extendida": [25, 28], "Car - 3h": [25, 28]}

u_PREC = {  
    "Large Van SDD": [80, 85], 
    "Small Van SDD": [70, 80],  
    "Car Newbie": [40, 45],  
    "Car - 8h": [70, 75]
}

NOMBRES_PLANES_PREC = ["CHALCO", "COYOACÁN", "IZTAPALAPA", "MILPA ALTA", "TLAHUAC", "TLALPAN NORTE", "TLALPAN SUR", "XOCHIMILCO"]


# --- AÑADE ESTO DEBAJO DE U_PREC ---
u_PREC_SMX2 = {
    "Small Van SDD": [70, 80],
    "Car - 8h": [70, 75],
    "Car Zona Extendida": [65, 65]
}
NOMBRES_PLANES_PREG = ["CHALCO", "CHIMAS", "VALLE CHALCO", "IZTAPALAPA 1", "IZTAPALAPA 2", "LA PAZ", "PUEBLOS", "TEXCOCO"]


u_C1 = {
    "Rental E. Large Van": [120, 120], "Rental E. Small Van": [120, 120], "Rental Large Van": [120, 120], 
    "Rental Small Van": [120, 120], "Large Van MLP": [100, 100], "Small Van MLP":[80, 80],
    "Car MLP": [50, 50], "Moto - 3h": [28, 28], "Car Newbie 3h": [30, 30], "Car - 8h": [80, 85], "Car - 5h": [60, 60]
}
u_C2 = u_C1.copy()
u_C2["Large Van Híbrida"] = [100, 100]


# --- PANEL DE REGLAS Y RESTRICCIONES (Sidebar) ---
with st.sidebar.expander("🛠️ REGLAS Y RESTRICCIONES"):
    st.info("Configura prioridades por polígono:")
    reglas_config = {}
    
    # Combinamos las listas
    todos_polis = NOMBRES_PLANES_PREC + NOMBRES_PLANES_PREG
    todas_unidades = list(set(list(u_PREC.keys()) + list(u_C1.keys())))
    
    # Usamos enumerate para evitar llaves duplicadas (KeyError)
    for i, poli in enumerate(todos_polis):
        st.markdown(f"**📍 {poli}**")
        # La KEY ahora es única usando el índice i
        prio = st.multiselect(f"Prioridad:", options=todas_unidades, key=f"prio_{i}_{poli}")
        roja = st.checkbox("Zona Roja", key=f"roja_{i}_{poli}")
        
        # Guardamos en el diccionario usando el nombre del polígono como clave
        reglas_config[poli] = {
            "prioridad": prio,
            "zona_roja": roja
        }

import json
reglas_json = json.dumps(reglas_config)


def gen_master_rows(data_dict, table_id):
    rows = ""
    items = list(data_dict.items())
    total_items = len(items)

   # Listas de nombres para que la función las reconozca
    nombres_prec = ["CHALCO", "COYOACÁN", "IZTAPALAPA", "MILPA ALTA", "TLAHUAC", "TLALPAN NORTE", "TLALPAN SUR", "XOCHIMILCO"]
    nombres_smx2 = ["CHALCO", "CHIMAS", "VALLE CHALCO", "IZTAPALAPA 1", "IZTAPALAPA 2", "LA PAZ", "PUEBLOS", "TEXCOCO"]
    
    # Determinamos el total de filas final
    # Si es PREC, queremos al menos 45 para que quepa todo y sobren espacios
    # Si no, las 18 de siempre
    num_filas_objetivo = 45 if table_id == "PREC" else 11
    
    # Usamos el número más grande entre el contenido real y nuestro objetivo
    # Esto evita que se corte SMX11 si el diccionario crece
    rango_final = max(total_items, num_filas_objetivo)
    
    for i in range(1, rango_final + 1):
        # Lógica de nombres
        if (data_dict == u_PREC) and (i-1) < len(nombres_prec):
            p_name = nombres_prec[i-1]
        elif (data_dict == u_PREC_SMX2) and (i-1) < len(nombres_smx2):
            p_name = nombres_smx2[i-1]
        else:
            p_name = f"PLAN {i}"
            
        # Obtener datos de la unidad si existe
        if (i-1) < total_items:
            name, spr = items[i-1]
        else:
            name, spr = "", [0, 0]
            
        
        # --- DISEÑO DE FILAS ---
        
        # Caso A: Es un Encabezado/Divisor
        if "---" in name:
            # Quitamos 'master-row' de la clase para que el JS de polígonos no la cuente
            rows += f'''
            <tr class="es-divisor" style="background: #333 !important; color: #00e5ff; height: 28px;">
                <td colspan="6" style="text-align: center; font-weight: bold; font-size: 11px; letter-spacing: 3px; border: none; pointer-events: none;">
                    {name}
                </td>
                <td class="edit-name" style="display:none;">IGNORAR</td>
                <td class="edit-spr-min" style="display:none;">0</td>
                <td class="edit-spr-max" style="display:none;">0</td>
                <td class="edit-orh" style="display:none;">0</td>
                <td class="f-stock" style="display:none;">0</td>
                <td class="f-left" style="display:none;">0</td>
            </tr>'''
        
        # Caso B: Es una unidad normal o espacio vacío
        else:
            st_base = "background: #ebebeb; color: #969696;" if not name else ""
            rows += f'''
            <tr class="master-row" style="{st_base}">
                <td contenteditable="true" class="edit-name" oninput="recalc()" style="font-weight: bold; text-align: left; padding-left: 10px; border: 0.5px solid #ccc; width: 150px;">{name}</td>
                <td contenteditable="true" class="edit-spr-min" oninput="recalc()" style="text-align: center; border: 0.5px solid #ccc; width: 45px; background-color: #000000; color: #ffffff;">{spr[0]}</td>
                <td contenteditable="true" class="edit-spr-max" oninput="recalc()" style="text-align: center; border: 0.5px solid #ccc; width: 45px; background-color: #000000; color: #ffffff;">{spr[1]}</td>
                <td contenteditable="true" class="edit-orh" style="text-align: center; border: 0.5px solid #ccc; width: 45px;">480</td>
                <td contenteditable="true" class="f-stock" oninput="recalc()" style="text-align: center; border: 0.5px solid #ccc; width: 55px; font-weight: bold; font-size: 13px;">0</td>
                <td class="f-left" style="font-weight: bold; text-align: center; border: 0.5px solid #ccc; width: 60px; font-size: 18px;">0</td>
            </tr>''' 
    return rows



def gen_poligonos(data_target=None): # Usamos un nombre genérico para evitar errores
    polys = ""
    btn_s = "cursor:pointer; border:none; background:rgba(0,0,0,0.08); color:#333; font-weight:bold; width:24px; height:24px; border-radius:4px; flex-shrink:0;"
    
    # Tu lista de nombres
    nombres_prec = ["CHALCO", "COYOACÁN", "IZTAPALAPA", "MILPA ALTA", "TLAHUAC", "TLALPAN NORTE", "TLALPAN SUR", "XOCHIMILCO"]
    nombres_smx2 = ["CHALCO", "CHIMAS", "VALLE CHALCO", "IZTAPALAPA 1", "IZTAPALAPA 2", "LA PAZ", "PUEBLOS", "TEXCOCO"]
    
    fila_inner = f'''
    <tr class="calc-row">
        <td class="u-manual-cell" style="background: #e3defa; text-align: center; border: 0.6px solid #ccc; padding: 10px 5px; width: 80px; min-width: 80px; max-width: 80px;">
            <button style="{btn_s}" onclick="stepVal(this, -1, 'u')">-</button>
            <span contenteditable="true" class="u-manual" oninput="manualEdit(this)" style="font-weight: bold; margin:0 5px;">0</span>
            <button style="{btn_s}" onclick="stepVal(this, 1, 'u')">+</button>
        </td>
        <td class="spr-real-cell" style="background: #def3ed; text-align: center; border: 0.6px solid #ccc; padding: 10px 5px; width: 110px; min-width: 110px; max-width: 110px;">
            <button style="{btn_s}" onclick="stepVal(this, -1, 's')">-</button>
            <span contenteditable="true" class="spr-real-val" oninput="manualEdit(this)" style="font-weight: bold; margin:0 5px;">0</span>
            <button style="{btn_s}" onclick="stepVal(this, 1, 's')">+</button>
        </td>
        <td style="border: 0.5px solid #ccc; padding: 2px;"><select class="s-type" onchange="resetRow(this)" style="width:100%; border:none; background:transparent; font-weight:bold; font-size:12px !important; color:#333; appearance:none; -webkit-appearance:none;"><option>SELECCIONAR...</option></select></td>
        <td style="width: 45px !important; text-align: center; border: 0.5px solid #ccc;"><input type="checkbox" class="ok-check" style="transform: scale(1.1); accent-color: #FF00FF; cursor: pointer;"></td>
    </tr>'''

    for i in range(1, 11):
        # --- LÓGICA DE NOMBRES CORREGIDA ---
        if (data_target == u_PREC) and (i-1) < len(nombres_prec):
            nombre_final = nombres_prec[i-1]
        elif (data_target == u_PREC_SMX2) and (i-1) < len(nombres_smx2):
            nombre_final = nombres_smx2[i-1]
        else:
            nombre_final = f"PLAN {i}"

        polys += f'''
        <div class="poligono-bloque" style="margin-bottom: 25px; box-shadow: 0 10px 20px rgba(0,0,0,0.1), 0 6px 6px rgba(0,0,0,0.1); border-radius: 12px; overflow: hidden; background: white; border: 1px solid #e1e1e1; transform: translateZ(0);">           
            <table style="width: 100%; border-collapse: collapse;">
                <thead>
                    <tr style="background: linear-gradient(180deg, #696969, #808080); color: white; font-size: 12px; height: 36px;">                        
                        <th style="padding: 0 10px; border-right: 2px solid rgba(255,255,255,0.2);">PLAN</th>
                        <th style="border-right: 2px solid rgba(255,255,255,0.2);">VOL. TOTAL</th>
                        <th style="width: 80px; min-width: 80px; max-width: 80px; border-right: 2px solid rgba(255,255,255,0.2);"># ASIGNADAS</th>
                        <th style="width: 110px; min-width: 110px; max-width: 110px; border-right: 2px solid rgba(255,255,255,0.2);">SPR REAL</th>
                        <th style="border-right: 2px solid rgba(255,255,255,0.2);">TIPO DE UNIDAD</th>
                        <th style="width: 45px !important; text-align: center;">OK</th>
                    </tr>
                </thead>
                <tbody>
                    <tr class="calc-row">
                        <td rowspan="5" contenteditable="true" style="background: #f0f0f0; font-weight:bold; text-align:center; border: 1px solid #ccc; padding: 5px; color:#333;">{nombre_final}</td>
                        <td rowspan="5" contenteditable="true" class="v-total-val" oninput="recalc()" style="color: #20B2AA; font-weight: bold; font-size: 18px; text-align: center; border: 1px solid #ccc; padding: 5px;">0</td>
                        
                        <td class="u-manual-cell" style="background: #e3defa; text-align: center; border: 0.5px solid #ccc;">
                            <button style="{btn_s}" onclick="stepVal(this, -1, 'u')">-</button>
                            <span contenteditable="true" class="u-manual" oninput="manualEdit(this)" style="font-weight: bold; margin:0 5px;">0</span>
                            <button style="{btn_s}" onclick="stepVal(this, 1, 'u')">+</button>
                        </td>
                        <td class="spr-real-cell" style="background: #def3ed; text-align: center; border: 0.5px solid #ccc; width: 110px;">
                            <button style="{btn_s}" onclick="stepVal(this, -1, 's')">-</button>
                            <span contenteditable="true" class="spr-real-val" oninput="manualEdit(this)" style="font-weight: bold; margin:0 5px;">0</span>
                            <button style="{btn_s}" onclick="stepVal(this, 1, 's')">+</button>
                        </td>
                        <td style="border: 0.5px solid #ccc; padding: 2px;">
                            <select class="s-type" onchange="resetRow(this)" style="width:100%; border:none; background:transparent; font-weight:bold; font-size:11px; color:#333;">
                                <option>SELECCIONAR...</option>
                            </select>
                        </td>
                        <td style="width: 45px !important; text-align: center; border: 0.5px solid #ccc;"><input type="checkbox" class="ok-check" style="transform: scale(1.2); accent-color: #FF00FF; cursor: pointer;"></td>
                    </tr>
                    {fila_inner}{fila_inner}{fila_inner}{fila_inner}
                    
                    <tr style="background:#f8f9fa; height: 32px;">
                        <td colspan="2" style="text-align:center; font-weight:bold; border: 1px solid #ccc; font-size: 16px; color:#333;">ESTADO:</td>
                        <td class="v-calculado-total" style="font-weight: bold; font-size: 16px; color: #d32f2f; border: 1px solid #ccc; text-align: center;">0</td>
                        <td class="p-diff" colspan="2" style="text-align: center; font-weight: bold; border: 1px solid #ccc; font-size: 16px;">VACÍO</td>
                        <td style="width: 45px !important; border: 1px solid #ccc; background: #FFFFFF;"></td>
                    </tr>
                </tbody>
            </table>
        </div>'''
    return polys




app_html = f"""
<!DOCTYPE html>
<html>
<head>
<head>
    <style>
        /* ... Aquí están tus estilos anteriores (meli-table, google-alert, etc.) ... */

        /* AÑADE EL ÚLTIMO CÓDIGO AQUÍ, ANTES DEL CIERRE */

       
        
        /* Efecto de iluminación al pasar el mouse por las filas */
        tr.master-row:hover, tr.calc-row:hover {{
            background-color: #f8fbff !important;
            box-shadow: inset 0 0 10px rgba(0,0,0,0.05);
            cursor: default;
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
    </style>
    
</head>

    <style>
body {{ font-family: sans-serif; background: #ffffff; padding: 14px; }}
.meli-table {{ 
    border-collapse: separate; /* Cambiado para que se noten las sombras de celda */
    border-spacing: 0 8px;
    width: 100%; 
    table-layout: auto; 
    border-radius: 10px; 
    overflow: hidden; 
    box-shadow: 0 4px 15px rgba(0,0,0,0.15), inset 0 0 2px white; /* Efecto de profundidad */
    border: 1px solid #000000;
}}

/* Bordes internos gris claro para el encabezado */
.meli-table th {{
    background: linear-gradient(180deg, #444444 0%, #111111 100%);
    color: #FFFFFF;
    font-size: 11px;
    height: 40px;
    font-weight: bold;
    text-align: center;
    border-bottom: 1px solid #555 !important;
    
    /* Borde interno (derecho) en gris claro */
    border-right: 1px solid #808080 !important; 
    border-left: 1px solid #808080 !important;
    padding: 2px 5px;
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
    border-bottom: 1px solid #333232; 
    border-right: 1px solid #333232;
    font-size: 14px; 
    height: 32px; 
    transition: background 0.2s; /* Animación sutil al pasar el mouse */
    padding: 1px 3px;
}}

/* El efecto Neomórfico en cada fila */
        .master-row {{ 
            border-radius: 9px;
            box-shadow: 1px 1px 5px #ededed, -2px -2px 6px #efefef;
            transition: all 0.2s ease;
        }}

/* Redondear las esquinas de las filas */
        .meli-table td:first-child {{ border-radius: 12px 0 0 12px; }}
        .meli-table td:last-child {{ border-radius: 0 12px 12px 0; }}

        
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
    border: 1px solid #bbb; 
    background: linear-gradient(180deg, #f0f0f0 0%, #dcdcdc 100%); /* Efecto 3D de relieve */
    border-radius: 8px 8px 0 0; 
    font-weight: bold; 
    font-size: 13px;
    color: #333;
    transition: all 0.2s ease;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.8), 0 2px 4px rgba(0,0,0,0.1);
    margin-right: 2px;
    outline: none;
}}

/* Efecto al pasar el mouse (Hover) */
.tab-btn:hover {{ 
    background: linear-gradient(180deg, #ffffff 0%, #f8fbff 100%);
    color: #000;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    transform: translateY(-2px); /* Se levanta un poco */
}}

/* Pestaña Activa (Seleccionada) */
.tab-btn.active {{
    background: linear-gradient(180deg, #444 0%, #000 100%); /* Color oscuro profundo */
    color: #fff; 
    border-bottom: none;
    box-shadow: inset 0 2px 5px rgba(0,0,0,0.5);
    transform: translateY(0); /* Se queda pegada abajo */
}}        .tab-btn.active {{ background: #333; color: white; }}
        
        .tools-panel {{ display: flex; flex-direction: column; gap: 10px; margin-top: 15px; }}
        .google-tool {{ background: linear-gradient(145deg, #ffffff, #DDA0DD); padding: 15px; border-radius: 15px; border: 1px solid #ddd; text-align: center; box-shadow: 5px 5px 15px #d1d1d1, -5px -5px 15px #ffffff; transition: transform 0.2s;}}
        .google-tool:hover {{
            transform: translateY(-3px);
        }}
        .google-tool input {{
            border-radius: 8px;
            border: 1px solid #ccc;
            padding: 5px;
            font-size: 16px;
            outline: none;
            box-shadow: inset 2px 2px 5px #e0e0e0;
        }}

        
       /* CALCULADORA CON RESPLANDOR NEÓN */
        #calc_wrapper {{ background: #22c5bc; border-radius: 20px; padding: 15px; border: transparent; outline: none; transition: 0.3s; }}
        #calc_wrapper:focus {{ box-shadow: 0 0 20px #FF00FF, 0 0 40px #FF00FF; border: 2px solid #FF00FF; }}
        
        #calc_display_box {{ background: #fffacd; border-radius: 10px; padding: 10px; text-align: right; margin-bottom: 10px; min-height: 60px; }}
        .calc-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 5px; }}
        .btn-c {{ background: white; border: none; font-weight: bold; border-radius: 8px; padding: 12px; cursor: pointer; box-shadow: 0 3px #ccc; font-size: 14px; }}
        .btn-c-eq {{ background: #FF00FF; color: white; border: none; border-radius: 8px; cursor: pointer; font-weight: bold; font-size: 14px; }}
        .crono-card {{ background: #1c1c1c; border-radius: 12px; padding: 15px; color: white; font-family: monospace; text-align: center; }}
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
    font-size: 11px !important;    /* Reduce un poco la letra */
}}

/* Forzar que la fila misma no tenga altura mínima */
html body .meli-table tbody tr:last-child {{
    height: 16px !important;
}}

/* Estilo base para los botones del cronómetro */
.crono-card button {{
    position: relative;
    border: none;
    border-radius: 6px;
    padding: 10px 18px;
    font-size: 18px;
    cursor: pointer;
    transition: all 0.1s ease; /* Transición rápida para el rebote */
    margin: 5px;
    font-weight: bold;
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

/////////////////

/* Agrégalo al final de tu sección <style> */
.ok-check {{
    accent-color: #FF00FF !important; /* Cambia aquí el color (ej. #20B2AA para Turquesa) */
    cursor: pointer;
}}
    
    </style>

    
</head>
<body>

<div id="google-alert">⚠️ <span id="alert-msg"></span> [ENTER para cerrar]</div>

<div style="display: flex; gap: 20px;">
    <!-- COLUMNA IZQUIERDA -->
    <div style="flex: 1;">
        <div style="background: #696969; color: white; padding: 10px; border-radius: 8px; text-align: center; font-weight: bold; margin-bottom: 10px;">📋 PLANIFICACIÓN POR POLÍGONOS</div>
        <div id="polys-2" class="p-content">{gen_poligonos(u_C1)}</div>
        <div id="polys-1" class="p-content" style="display:none;">{gen_poligonos(u_PREC)}</div>
        <div id="polys-5" class="p-content" style="display:none;">{gen_poligonos(u_PREC_SMX2)}</div>
        <div id="polys-4" class="p-content" style="display:none;">{gen_poligonos(u_SDE)}</div>
    </div>

    <!-- COLUMNA DERECHA -->
    <div style="width: 450px;">
        <div style="background: #000; color: white; padding: 10px; border-radius: 8px; font-weight: bold; text-align: center; margin-bottom: 10px;">🚚 🚚 DISPONIBILIDAD DE FLOTA 🚛 🚛</div>
        <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 5px;">
            <div>
                <button class="tab-btn active" onclick="showTab(2, this)">C1</button>
                <button class="tab-btn" onclick="showTab(1, this)">PREC SMX5</button>
                <button class="tab-btn" onclick="showTab(5, this)">PREC SMX2</button>
                <button class="tab-btn" onclick="showTab(4, this)">SDE</button>
            </div>

            
            <div style="padding-bottom: 5px; display: flex; gap: 6px; align-items: center;">
    <button onclick="distribuirAutomatico()" 
    style="cursor:pointer; background: #FF00FF; color: white; border: none; font-size: 12px; padding: 6px 12px; border-radius: 4px; font-weight: bold; box-shadow: 0 3px 0 #b300b3; transition: all 0.05s; outline: none;"
    onmousedown="this.style.transform='translateY(2px)'; this.style.boxShadow='0 1px 0 #b300b3';"
    onmouseup="this.style.transform='translateY(0px)'; this.style.boxShadow='0 3px 0 #b300b3';"
    onmouseleave="this.style.transform='translateY(0px)'; this.style.boxShadow='0 3px 0 #b300b3';">
    ⚡ AUTO-CALCULAR
</button>
    
    <button class="filter-btn" onclick="filterRows(true)" 
        style="cursor:pointer; background: linear-gradient(180deg, #444 0%, #222 100%); color: white; border: 1px solid #111; font-size: 12px; padding: 6px 12px; border-radius: 4px; font-weight: bold; box-shadow: 0 3px 0 #000; transition: all 0.05s; outline: none;">
        ACTIVAS
    </button>

    <button class="filter-btn" onclick="filterRows(false)" 
        style="cursor:pointer; background: #20B2AA; color:white; border:none; font-size:12px; padding:6px 12px; border-radius:4px; font-weight:bold; box-shadow: 0 3px 0 #167a75; transition: all 0.05s; outline: none;">
        TODAS
    </button>
</div>


        </div>

        <!-- TABLAS CON ENCABEZADOS RESTAURADOS (CORREGIDO AL ORIGINAL) -->

        
       
        <div id="tab-2" class="t-content">
            <table class="meli-table">
                <thead>
                    <tr style="background: linear-gradient(180deg, #333 0%, #1a1a1a 100%); color: white;">
                        <th rowspan="2" style="border-right: 0.5px solid #555; padding: 4px 8px; font-size: 11px;">UNIDAD</th>
                        <th colspan="2" style="border-bottom: 0.5px solid #555; border-right: 0.5px solid #555; padding: 2px; font-size: 11px;">SPR</th>
                        <th rowspan="2" style="border-right: 0.5px solid #555; padding: 4px 8px; font-size: 11px;">ORH</th>
                        <th rowspan="2" style="border-right: 0.5px solid #555; padding: 4px 8px; font-size: 11px;">SCHED</th>
                        <th rowspan="2" style="padding: 4px 8px; font-size: 11px;">ME QUEDAN</th>
                    </tr>
                    <tr>
                        <th style="border-right: 0.5px solid #555; padding: 2px; font-size: 10px;">MIN</th>
                        <th style="border-right: 0.5px solid #555; padding: 2px; font-size: 10px;">MAX</th>
                    </tr>
                </thead>
                <tbody id="body-2">{gen_master_rows(u_C1, 2)}</tbody>
            </table>
        </div>

       
        <div id="tab-1" class="t-content" style="display:none;">
            <table class="meli-table">
                <thead>
                    <tr style="background: linear-gradient(180deg, #444 0%, #111 100%); color: white;">
                        <th rowspan="2" style="border-right: 0.5px solid #555; padding: 4px 8px; font-size: 11px;">UNIDAD</th>
                        <th colspan="2" style="border-bottom: 0.5px solid #555; border-right: 0.5px solid #555; padding: 2px; font-size: 11px;">SPR</th>
                        <th rowspan="2" style="border-right: 0.5px solid #555; padding: 4px 8px; font-size: 11px;">ORH</th>
                        <th rowspan="2" style="border-right: 0.5px solid #555; padding: 4px 8px; font-size: 11px;">SCHED</th>
                        <th rowspan="2" style="padding: 4px 8px; font-size: 11px;">ME QUEDAN</th>
                    </tr>
                    <tr>
                        <th style="border-right: 0.5px solid #555; padding: 2px; font-size: 10px;">MIN</th>
                        <th style="border-right: 0.5px solid #555; padding: 2px; font-size: 10px;">MAX</th>
                    </tr>
                </thead>
                <tbody id="body-1">{gen_master_rows(u_PREC, 1)}</tbody>
            </table>
        </div>

       
        <div id="tab-5" class="t-content" style="display:none;">
            <table class="meli-table">
                <thead>
                    <tr style="background: linear-gradient(180deg, #444 0%, #111 100%); color: white;">
                        <th rowspan="2" style="border-right: 0.5px solid #555; padding: 4px 8px; font-size: 11px;">UNIDAD</th>
                        <th colspan="2" style="border-bottom: 0.5px solid #555; border-right: 0.5px solid #555; padding: 2px; font-size: 11px;">SPR</th>
                        <th rowspan="2" style="border-right: 0.5px solid #555; padding: 4px 8px; font-size: 11px;">ORH</th>
                        <th rowspan="2" style="border-right: 0.5px solid #555; padding: 4px 8px; font-size: 11px;">SCHED</th>
                        <th rowspan="2" style="padding: 4px 8px; font-size: 11px;">ME QUEDAN</th>
                    </tr>
                    <tr>
                        <th style="border-right: 0.5px solid #555; padding: 2px; font-size: 10px;">MIN</th>
                        <th style="border-right: 0.5px solid #555; padding: 2px; font-size: 10px;">MAX</th>
                    </tr>
                </thead>
                <tbody id="body-5">{gen_master_rows(u_PREC_SMX2, 5)}</tbody>
            </table>
        </div>


        
        <div id="tab-4" class="t-content" style="display:none;">
            <table class="meli-table">
                <thead>
                    <tr style="background: linear-gradient(180deg, #444 0%, #111 100%); color: white;">
                        <th rowspan="2" style="border-right: 0.5px solid #555; padding: 4px 8px; font-size: 11px;">UNIDAD</th>
                        <th colspan="2" style="border-bottom: 0.5px solid #555; border-right: 0.5px solid #555; padding: 2px; font-size: 11px;">SPR</th>
                        <th rowspan="2" style="border-right: 0.5px solid #555; padding: 4px 8px; font-size: 11px;">ORH</th>
                        <th rowspan="2" style="border-right: 0.5px solid #555; padding: 4px 8px; font-size: 11px;">SCHED</th>
                        <th rowspan="2" style="padding: 4px 8px; font-size: 11px;">ME QUEDAN</th>
                    </tr>
                    <tr>
                        <th style="border-right: 0.5px solid #555; padding: 2px; font-size: 10px;">MIN</th>
                        <th style="border-right: 0.5px solid #555; padding: 2px; font-size: 10px;">MAX</th>
                    </tr>
                </thead>
                <tbody id="body-4">{gen_master_rows(u_SDE, 4)}</tbody>
            </table>
        </div>


        
        <!-- COLUMNA DERECHA: PANEL DE HERRAMIENTAS REORDENADO -->
        <div class="tools-panel">
            
            <!-- 1. CRONÓMETRO (Ahora primero) -->
            <div class="crono-card">
                <div style="font-size:10px; color:#888;">HORA ACTUAL: <span id="reloj-actual" style="color:#00e5ff;">00:00:00</span></div>
                <div id="crono-main" style="font-size:32px; font-weight:bold; margin:10px 0;">00:00:00.0</div>
                <div>
                    <button onclick="startC()" style="background:#28a745; color:white; border:none; padding:8px; border-radius:5px; cursor:pointer;">▶</button>
                    <button onclick="stopC()" style="background:#ffc107; border:none; padding:8px; border-radius:5px; cursor:pointer;">⏸</button>
                    <button onclick="resetC()" style="background:#dc3545; color:white; border:none; padding:8px; border-radius:5px; cursor:pointer;">🔄</button>
                </div>
            </div>

            <!-- 2. CALCULADORA (Ahora segunda) -->
            <div id="calc_wrapper" onclick="focusCalc()" tabindex="0">
                <div id="calc_display_box">
                    <div id="calc_h" style="font-size:10px; color:#666;"></div>
                    <div id="calc_r" style="font-size:24px; font-weight:bold;">0</div>
                </div>
                <div class="calc-grid">
                    <button onclick="cl()" class="btn-c" style="grid-column: span 2;">AC</button> 
                    <button onclick="del()" class="btn-c">⌫</button><button onclick="ao('/')" class="btn-c">÷</button>
                    <button onclick="an('7')" class="btn-c">7</button><button onclick="an('8')" class="btn-c">8</button><button onclick="an('9')" class="btn-c">9</button><button onclick="ao('*')" class="btn-c">×</button>
                    <button onclick="an('4')" class="btn-c">4</button><button onclick="an('5')" class="btn-c">5</button><button onclick="an('6')" class="btn-c">6</button><button onclick="ao('-')" class="btn-c">-</button>
                    <button onclick="an('1')" class="btn-c">1</button><button onclick="an('2')" class="btn-c">2</button><button onclick="an('3')" class="btn-c">3</button><button onclick="ao('+')" class="btn-c">+</button>
                    <button onclick="an('0')" class="btn-c" style="grid-column: span 2;">0</button><button onclick="calc_eq()" class="btn-c-eq">=</button>
                </div>
            </div>

            <!-- 3. CONVERTIDOR (Ahora al final) -->
            <div class="google-tool">
                <div style="font-weight:bold; color:#2c3e50; margin-bottom:10px; font-size:12px; letter-spacing:1px;">⏱️ CONVERTIDOR DE TIEMPO</div>
                <input type="number" id="min-in" placeholder="Minutos" style="width:80px; text-align:center;" oninput="convertTime()">
                <div style="margin-top:10px;">
                    <span id="time-res" style="font-size: 24px; font-weight: bold; color: #008B8B; text-shadow: 1px 1px 2px rgba(0,0,0,0.1);">0h 0m</span>
                 </div>
             </div>
        </div>
    </div>
</div>



<script>

// --- 1. AQUÍ RECIBES LA TABLA DE REGLAS/RESTRICCIONES ---
    // Esta variable 'ID_REGLAS_DINAMICAS' es la que el .replace() de Python llenará
const reglasEspeciales = JSON.parse('ID_REGLAS_DINAMICAS');

    let currentTab = 2;
    let editedRowsPlan = new Set();
    let curC = "";
    let chronoInterval;
    let startTime;
    let elapsedTime = 0;

    function showTab(n, btn) {{
        currentTab = n;
    // Oculta todo el contenido de polígonos y todas las tablas
    document.querySelectorAll('.p-content, .t-content').forEach(el => el.style.display = 'none');
    
    // Quita el color azul a los botones
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    
    // Muestra el bloque de polígonos de abajo
    document.getElementById('polys-' + n).style.display = 'block';
    
    // Muestra la tabla de unidades de arriba (la que acabamos de arreglar)
    document.getElementById('tab-' + n).style.display = 'block';
    
    // Pone el botón actual en azul
    btn.classList.add('active');
    
    recalc();
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
    if(sel === "SELECCIONAR...") return;

    // Buscamos la fila correspondiente en la tabla de Flota para sacar el MAX
    let fRows = Array.from(document.querySelectorAll('#body-' + currentTab + ' tr'));
    let fRow = fRows.find(r => r.querySelector('.edit-name').innerText.trim() === sel);
    
    if (!fRow) return; // Seguridad por si no encuentra la unidad

    let left = parseInt(fRow.querySelector('.f-left').innerText) || 0;
    let sprMaxReal = parseFloat(fRow.querySelector('.edit-spr-max').innerText) || 0;

    if(type === 'u') {{
        let span = row.querySelector('.u-manual');
        let val = parseInt(span.innerText) || 0;
        if (delta > 0 && left <= 0) {{
            if (currentTab === 4) {{
                showAlert("⚠️ EXCESO EN SDE. Se registrará como negativo.");
            }} else {{
                showAlert("⚠️ UNIDADES AGOTADAS: Solicita más a SVC.");
                return;
            }}
        }}
        span.innerText = Math.max(0, val + delta);
                }} else {{
        let span = row.querySelector('.spr-real-val');
        let val = parseFloat(span.innerText) || 0;
        let newVal = parseFloat((val + delta).toFixed(1)); // Redondeo para evitar errores de decimales

        // VALIDACIÓN: Solo bloquea si intentas SUBIR (delta > 0) y YA te pasaste del máximo
        if (delta > 0 && newVal > sprMaxReal) {{
            showAlert("⚠️ NO PUEDES SOBREPASAR EL SPR MÁXIMO (" + sprMaxReal + ")");
            return; 
        }}
        
        // Si es para bajar o está dentro del rango, permite el cambio
        span.innerText = Math.max(0, newVal).toFixed(1);
    }}
    
    editedRowsPlan.add(row);
    recalc();
}}

    function recalc() {{
        let fleet = {{}};
        document.querySelectorAll('#body-' + currentTab + ' tr').forEach(row => {{
            let name = row.querySelector('.edit-name').innerText.trim();
            let sch = parseInt(row.querySelector('.f-stock').innerText) || 0;
            let mi = row.querySelector('.edit-spr-min'), ma = row.querySelector('.edit-spr-max'), fs = row.querySelector('.f-stock');
            
            if(sch > 0) {{
                row.style.background = "white"; row.style.color = "black";
                fs.style.background = "#e3defa"; mi.style.background = "#def3ed"; 
                mi.style.color = "#008B8B"; // Color Aqua (DarkTurquoise)
                mi.style.fontWeight = "bold";
                
                ma.style.background = "#def3ed";
                ma.style.color = "#008B8B"; // Color Aqua (DarkTurquoise)
                ma.style.fontWeight = "bold";
            }} else {{
                row.style.background = "#ebebeb"; 
                row.style.color = "#969696";
                fs.style.background = "#ebebeb"; 
                // Resetear cuando SCHED es 0
                mi.style.background = "#ebebeb"; 
                mi.style.color = "#969696";
                mi.style.fontWeight = "normal";
                
                ma.style.background = "#ebebeb";
                ma.style.color = "#969696";
                ma.style.fontWeight = "normal";
            }}
            if(name !== "" && name !== "NUEVA UNIDAD") {{
                fleet[name] = {{ max: parseFloat(ma.innerText)||0, stock: sch, used: 0 }};
            }}
        }});

        document.querySelectorAll('#polys-' + currentTab + ' .poligono-bloque').forEach(bl => {{
            let vT = parseFloat(bl.querySelector('.v-total-val').innerText) || 0, vA = 0;
            
            // Referencia al número de ASIGNADAS
            let vCalcEl = bl.querySelector('.v-calculado-total'); 

            bl.querySelectorAll('.calc-row').forEach(r => {{
                let s = r.querySelector('.s-type').value, u = parseInt(r.querySelector('.u-manual').innerText) || 0, sp = r.querySelector('.spr-real-val');
                if(s !== "SELECCIONAR..." && fleet[s]) {{
                    if(!editedRowsPlan.has(r)) sp.innerText = fleet[s].max;
                    fleet[s].used += u; 
                    vA += (u * parseFloat(sp.innerText));
// CAMBIO: Aplicar color turquesa al SPR REAL cuando hay una unidad seleccionada
        sp.style.color = "#008B8B"; 
        sp.style.fontWeight = "bold";
    }} else {{
        // Resetear color si no hay selección (opcional, para limpieza)
        sp.style.color = "#969696";
        sp.style.fontWeight = "normal";   
                }}
            }});

            vCalcEl.innerText = Math.round(vA);
            let d = bl.querySelector('.p-diff');

            // Mantenemos la celda blanca siempre
            vCalcEl.style.background = "white";

            if (vT === 0) {{
                d.innerText = "VACÍO";
                d.style.background = "none";
                vCalcEl.style.color = "#d32f2f"; // Rojo si no hay nada
            }} else {{
                if (Math.round(vA) === Math.round(vT)) {{
                    // COINCIDENCIA: SOLO CAMBIA EL COLOR DEL TEXTO
                    d.innerText = "OK";
                    d.style.background = "#ceedd6"; 
                    vCalcEl.style.color = "#20B2AA"; // Texto en AQUA
                }} else if (vA > vT) {{
                    d.innerText = "EXCESO: " + Math.round(vA - vT);
                    d.style.background = "#ffe4b5";
                    vCalcEl.style.color = "#d32f2f";
                }} else {{
                    d.innerText = "FALTAN: " + Math.round(vT - vA);
                    d.style.background = "#f7cdd1";
                    vCalcEl.style.color = "#d32f2f";
                }}
            }}
        }});
        

        document.querySelectorAll('#body-' + currentTab + ' tr').forEach(row => {{
            let n = row.querySelector('.edit-name').innerText.trim();
            if(fleet[n]) {{
                let diff = fleet[n].stock - fleet[n].used;
                let cL = row.querySelector('.f-left');
                
                // REGLA DE ORO: Si es SDE o las especiales con unidad Car - 8h, permitimos el negativo visual
                let esEspecial = (currentTab === 'SDE') || 
                                 ((currentTab === 'PREC' || currentTab === 'PREC_SMX2') && (n.includes('Car - 8h') || n.includes('Car')));

                if (esEspecial) {{
                    cL.innerText = diff; // Mostrará -1, -2, etc.
                }} else {{
                    cL.innerText = diff < 0 ? 0 : diff; // Para el resto, bloquea en 0
                }}

                // Colores originales (Rojo si falta, Blanco sobre Rojo si es exacto)
                cL.style.color = (diff < 0) ? "red" : (diff === 0 && fleet[n].stock > 0 ? "white" : "black");
                cL.style.background = (diff === 0 && fleet[n].stock > 0 ? "#d32f2f" : "transparent");
            }}
        }});
    





       // --- ESTA ES LA PARTE QUE FILTRA LA LISTA DESPLEGABLE ---
        document.querySelectorAll('#polys-' + currentTab + ' .s-type').forEach(s => {{
            let cur = s.value; // Guardamos lo que está seleccionado actualmente
            let opt = '<option>SELECCIONAR...</option>';
            
            Object.keys(fleet).forEach(k => {{ 
                // REGLA: Mostrar en la lista solo si tiene stock > 0 
                // O si es la unidad que YA está seleccionada en esa fila
                if (fleet[k].stock - fleet[k].used > 0 || k === cur) {{ 
                    opt += `<option value="${{k}}">${{k}}</option>`; 
                }} 
            }});
            
            s.innerHTML = opt; 
            s.value = cur; // Mantenemos la selección actual para que no se borre lo que ya hiciste
        }});
  
    
    }}
    
    function focusCalc() {{
        document.getElementById('calc_wrapper').focus();
    }}

    function filterRows(onlyActive) {{
        const rows = document.querySelectorAll('#body-' + currentTab + ' tr');
        rows.forEach(row => {{
            const stock = parseInt(row.querySelector('.f-stock').innerText) || 0;
            row.style.display = (onlyActive && stock === 0) ? 'none' : '';
        }});
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

    function manualEdit(el) {{ editedRowsPlan.add(el.closest('tr')); recalc(); }}
    function resetRow(sel) {{ let r=sel.closest('tr'); r.querySelector('.u-manual').innerText="0"; r.querySelector('.spr-real-val').innerText="0"; editedRowsPlan.delete(r); recalc(); }}
    
   document.addEventListener('keydown', (e) => {{
        const calc = document.getElementById('calc_wrapper');
        const alerta = document.getElementById('google-alert');

        // Si la alerta está visible (tiene la clase 'show'), el Enter la cierra y NO hace nada más
        if (e.key === 'Enter' && alerta.classList.contains('show')) {{
            e.preventDefault();
            e.stopPropagation();
            hideAlert();
            return; // Detiene la ejecución aquí para que no afecte a la calculadora
        }}

        // Lógica de la calculadora (solo si está seleccionada)
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


function distribuirAutomatico() {{
        let fleet = {{}};
        document.querySelectorAll('#body-' + currentTab + ' tr').forEach(row => {{
            let name = row.querySelector('.edit-name').innerText.trim();
            let ma = row.querySelector('.edit-spr-max');
            let cL = row.querySelector('.f-left'); 
            let disponibles = parseInt(cL ? cL.innerText : 0) || 0;
            let sprMax = parseFloat(ma ? ma.innerText : 0) || 28;

            if (disponibles > 0 && name !== "" && name !== "NUEVA UNIDAD") {{
                fleet[name] = {{ max: sprMax, stock: disponibles }};
            }}
        }});

        if (Object.keys(fleet).length === 0) {{
            alert("⚠️ No hay unidades disponibles en SCHED para esta pestaña.");
            return;
        }}

        document.querySelectorAll('#polys-' + currentTab + ' .poligono-bloque').forEach(bl => {{
            let nombrePoli = bl.querySelector('.p-name').innerText.trim().toUpperCase();
            
            let vT = parseFloat(bl.querySelector('.v-total-val').innerText) || 0;
            let vA = parseFloat(bl.querySelector('.v-calculado-total').innerText) || 0;
            let faltante = vT - vA;

            if (faltante > 1) {{
                bl.querySelectorAll('.calc-row').forEach(r => {{
                    let s = r.querySelector('.s-type');
                    let u = r.querySelector('.u-manual');
                    let sp = r.querySelector('.spr-real-val');

                    if (s.value === "SELECCIONAR..." && faltante > 0) {{
                    
                        // --- 2. NUEVO: BUSCAR PRIORIDAD SEGÚN TU TABLA DE RESTRICCIONES ---
                    // Si el polígono tiene una prioridad guardada, la usa. Si no, usa toda la flota.
                    let configPoli = reglasEspeciales[nombrePoli] || {{ prioridad: [], zona_roja: false }};
                    let ordenBusqueda = configPoli.prioridad.length > 0 ? configPoli.prioridad : Object.keys(fleet);

                    // Buscamos la unidad que toque según el orden de prioridad
                    let key = ordenBusqueda.find(k => fleet[k] && fleet[k].stock > 0);
                    
                    if (key) {{
                        let unidad = fleet[key];
                        let necesito = Math.ceil(faltante / unidad.max);
                        let asigno = Math.min(necesito, unidad.stock);
                        
                        if (asigno > 0) {{
                            s.value = key;
                            u.innerText = asigno;
                            
                            let sprSugerido = (faltante / asigno);
                            let sprFinal = Math.min(sprSugerido, unidad.max);
                            sp.innerText = Math.round(sprFinal * 10) / 10;
                            
                            unidad.stock -= asigno;
                            faltante -= (asigno * sprFinal);
                            editedRowsPlan.add(r);
                            }}
                        }}
                    }}
                }});
            }}
        }});
        recalc();
    }}

    
    recalc();
</script>
</body>
</html>
"""

html(app_html.replace('ID_REGLAS_DINAMICAS', reglas_json), height=1200, scrolling=True)





import streamlit as st
import streamlit.components.v1 as components

# 1. ENLACE DE IMAGEN (Mapa de regiones)
ID_IMAGEN = "1M4GLEwFzhLrZjV-zmvGrdTQhC6IjwxOJ"
url_final = f"https://drive.google.com/thumbnail?id={ID_IMAGEN}&sz=w1000"

# 2. INFORMACIÓN OPERATIVA 100% COMPLETA
info_operativa = {
    "SDE": f"""
        <div style='text-align: center; margin-bottom: 25px;'>
            <img src="{url_final}" style="width: 100%; max-width: 800px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
        </div>

        <h3 style='color: #000; margin-bottom: 5px;'>ROL VP04</h3>
        <hr style='border: 1px solid #1E90FF; margin-bottom: 20px;'>
        
        <div style='background: white; border-left: 6px solid #1E90FF; padding: 15px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); color: #000; margin-bottom: 20px;'>
            <p style='margin: 0;'><strong>👉👉 PARA SDE</strong><br>
            - 🔷 Revisar si SVC agrega blancos<br>
            - Orígenes (imagen) + onway + despacho de hoy de las 3 pm en adelante + fecha promesa y/o quemada ...validar<br>
            - SPR 30<br>
            - ❌ delimitación / ❌ restricción<br>
            - Quito puntos muy lejanos</p>
        </div>

        <h3 style='color: #000; margin-top: 25px;'>🟪 SDE 🟪</h3>
        <hr style='border: 1px solid #FF00FF; margin-bottom: 20px;'>
        
        <div style='background: white; border-left: 6px solid #FF00FF; padding: 12px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); color: #000; margin-bottom: 12px;'>
            <p style='margin: 0;'><strong><span style="color: #FF00FF;">●</span> SMX9 PM2 - ⏰ 16:40 - 17:00</strong><br>
            - 📌 Orígenes: MXCD02, MXCD06<br>
            - 👉 Vol aprox. 800<br>
            - 👉 fecha promesa</p>
        </div>

        <div style='background: white; border-left: 6px solid #FF00FF; padding: 12px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); color: #000; margin-bottom: 12px;'>
            <p style='margin: 0;'><strong><span style="color: #FF00FF;">●</span> SMX5 PM2 - ⏰ 17:20 - 17:40</strong><br>
             - 📌 Orígenes: MXCD02, MXCD06<br>
             - 👉 Vol aprox. 400<br>
             - 👉 fecha promesa + quemada</p>
        </div>

        <div style='background: white; border-left: 6px solid #FF00FF; padding: 12px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); color: #000; margin-bottom: 12px;'>
            <p style='margin: 0;'><strong><span style="color: #FF00FF;">●</span> SMX4 PM2 - ⏰ 17:40 - 18:00</strong><br>
            - 📌 Orígenes: MXCD02, MXCD06<br>
            - 👉 Vol aprox. 550<br>
            - 🏍️ Motos en donde sea con SPR 25<br>
            - 👉 fecha promesa + quemada</p>
        </div>

        <div style='background: white; border-left: 6px solid #FF00FF; padding: 12px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); color: #000; margin-bottom: 12px;'>
            <p style='margin: 0;'><strong><span style="color: #FF00FF;">●</span> SMX2 PM1 - ⏰ 18:00 - 18:20</strong><br>
            - 📌 Orígenes: MXCD02, MXCD06<br>
            - 👉 fecha promesa + quemada</p>
            - 👉 Vol aprox. 250<br>
            - 👉 SPR 28</p>
        </div>

        <div style='background: white; border-left: 6px solid #FF00FF; padding: 12px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); color: #000; margin-bottom: 12px;'>
            <p style='margin: 0;'><strong><span style="color: #FF00FF;">●</span> SMT2 PM2 - ⏰ 18:40 - 19:00</strong><br>
            - 📌 Origen MXNL01<br>
            - 👉 Despacho hoy después 3 pm<br>
            - 👉 fecha promesa + quemada<br>
            - 👉 Vol. 800 aprox.<br>
            - 👉 SPR 27-28 / se van las 30 unidades<br>
            - 👉 Pido validación</p>
        </div>

        <h3 style='color: #000; margin-top: 25px;'>🟥 PRE-CARGAS 🟥</h3>
        <hr style='border: 1px solid #ff8c00; margin-bottom: 20px;'>

        <div style='background: white; border-left: 6px solid #ff8c00; padding: 15px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); color: #000; margin-bottom: 20px;'>
            <p style='margin: 0;'><strong>👉👉 INDICACIONES</strong><br>
            - 📌 Origen + onway / si no especifican<br>
            - 👉 Schedule del día siguiente / apartado en archivo AMO<br>
            - 👀 Revisar si mandan ids a agregar<br>
            - ✅ delimitación / ✅ dejar restricción para MLP /  ✅ dejar restricción para Crowd<br>
            - Revisar en qué polígonos acepta MLP para meterlas</p>
        </div>
        
        <div style='background: white; border-left: 6px solid #ff8c00; padding: 12px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); color: #000; margin-bottom: 12px;'>
            <p style='margin: 0;'><strong><span style="color: #ff8c00;">●</span> SMX5 AM3 - ⏰ 21:50 - 22:30</strong><br>
             - 📌 Orígen: MXCD09 / indicado por SVC<br>
             - 👉 Todo Onway / indicado por SVC<br>
             - 👉 Si SVC no indica origen, tomo los de playbook<br>
             - ➕ Agregan ids a ciclo (revisar forms)<br>
             - ✅  Validan volumen / aprox. 2500-2600<br>
             - 🚛 MLP van a ➡️ Xochimilco ➡️ Tlalpan Norte ➡️ Tlalpan Sur</p>
        </div>

        <div style='background: white; border-left: 6px solid #ff8c00; padding: 12px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); color: #000; margin-bottom: 12px;'>
            <p style='margin: 0;'><strong><span style="color: #ff8c00;">●</span> SMX2 AM3 - ⏰ 22:40 - 23:20</strong><br>
             - 📌 Orígen: MXCD09 + MXCD02 / indicados por SVC<br>
             - 👉 Todo Onway<br>
             - 👉 Si SVC no indica origen, tomo los de playbook / MXCD02 despacho 16:00 / MXCD09  despacho 14:00 / MXCD10  despacho 21:00<br>
             - 👀 Revisar si se agrega ➕ forms<br>
             - ✅  Validan volumen / aprox. 1900-2000<br>
             - 🚛 Revisar si se usa MLP hasta ahora solo Crowd 8h</p>
        </div>




        <h3 style='color: #000; margin-top: 25px;'>👉 OTROS RUTEOS PM2 (SDE)</h3>
        <hr style='border: 1px solid #808080; margin-bottom: 20px;'>


        

        <div style='background: white; border-left: 6px solid #808080; padding: 12px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); color: #000; margin-bottom: 12px;'>
            <p style='margin: 0;'><strong><span style="color: #808080;">●</span> SMX20 (SMX10) PM2 - ⏰ 0:20 pm</strong><br>
            - 📌 Origen 20 / ❌ SPR / ❌ Ocupación<br>
            - 👉 Meto ORH de 4 hrs para crowd 5 hrs / solo para dividir paquetes uso SPR 30<br>
            - 👉 Pido validación ➡️ @Luisa Itzel Perez y @Ibrahim</p>
        </div>

        <div style='background: white; border-left: 6px solid #808080; padding: 12px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); color: #000; margin-bottom: 12px;'>
            <p style='margin: 0;'><strong><span style="color: #808080;">●</span> SMX8 PM2 - ⏰ 5:30 pm</strong><br>
            - 👉 Sin schedule</p>
        </div>

        <div style='background: white; border-left: 6px solid #808080; padding: 12px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); color: #000; margin-bottom: 12px;'>
            <p style='margin: 0;'><strong><span style="color: #808080;">●</span> SMX3 PM2 - ⏰ 4:30 pm</strong><br>
            - 📌 Orígenes: MXCD02, MXCD06<br>
            - ✅ delimitación (salen planes) / ❌ restricción<br>
            - SPR 30/Moto y Crowd<br>
            - 🏍️ MOTOS ➡️ Cuauhtémoc-Polanco</p>
        </div>

        <div style='background: white; border-left: 6px solid #808080; padding: 12px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); color: #000; margin-bottom: 12px;'>
            <p style='margin: 0;'><strong><span style="color: #808080;">●</span> SBJ1 PM2 - ⏰ A partir de las 5:00 pm</strong><br>
            - 👉 Pido autorización para iniciar ruteo / SPR 28 / 200-300 pqt aprox</p>
        </div>

        <div style='background: white; border-left: 6px solid #808080; padding: 12px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); color: #000; margin-bottom: 12px;'>
            <p style='margin: 0;'><strong><span style="color: #808080;">●</span> SHM1 PM2 - ⏰ 7:20 pm</strong><br>
            - 👉 SPR 21 / crowd 5 hrs</p>
        </div>

        <div style='background: white; border-left: 6px solid #808080; padding: 12px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); color: #000; margin-bottom: 12px;'>
            <p style='margin: 0;'><strong><span style="color: #808080;">●</span> SMT1 PM2 - ⏰ 5:10 pm</strong><br>
            - 📌 Orígen: MXNL01<br>
            - 👉 SVC manda data (la envían tarde, solo hago el cruce para cotejo)</p>
        </div>

        <div style='background: white; border-left: 6px solid #808080; padding: 12px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); color: #000; margin-bottom: 12px;'>
            <p style='margin: 0;'><strong><span style="color: #808080;">●</span> SMT3 PM2 - ⏰ 5:15 pm</strong><br>
            - 👉 SPR 28 / crowd 5 hrs / 500 pqt aprox</p>
        </div>

        <div style='background: white; border-left: 6px solid #808080; padding: 12px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); color: #000; margin-bottom: 12px;'>
            <p style='margin: 0;'><strong><span style="color: #808080;">●</span> SGD1 PM2 - ⏰ 4:50 pm</strong><br>
             - 📌 Orígen: MXJC01</p>
        </div>

        <div style='background: white; border-left: 6px solid #808080; padding: 12px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); color: #000; margin-bottom: 12px;'>
            <p style='margin: 0;'><strong><span style="color: #808080;">●</span> SGD2 PM2 - ⏰ 0:00 pm</strong><br>
            - 👉 SPR 28</p>
        </div>

        <div style='background: white; border-left: 6px solid #808080; padding: 12px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); color: #000; margin-bottom: 12px;'>
            <p style='margin: 0;'><strong><span style="color: #808080;">●</span> SGD3 PM2 - ⏰ 4:50 pm</strong><br>
            - 👉 SPR 30 / crowd 5 y 3 hrs</p>
        </div>

        <div style='background: white; border-left: 6px solid #808080; padding: 12px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); color: #000; margin-bottom: 12px;'>
            <p style='margin: 0;'><strong><span style="color: #808080;">●</span> SMD2 PM1 - ⏰ 5:30 pm</strong><br>
            - 📌 Orígen: MXYU01<br>
            - 👉 Sin schedule / contemplo crowd 5 hrs<br>
            - 🚛 SVC manda en cuantas unidades y el SPR / entre 5 a 6 crowd 5 hrs con SPR 30<br>
            - 👉 Espero a que carguen volumen (x lo general lo cargan 10 min. antes de las 6:00 pm)<br>
            - 👉 Pido validación<br>
            - 👉 Piden mejor dispersion, indico: "Se publicó de acuerdo a la herramienta team, ya no podemos manipular la dispersión como antes"</p>
        </div>

        <div style='background: white; border-left: 6px solid #808080; padding: 12px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); color: #000; margin-bottom: 12px;'>
            <p style='margin: 0;'><strong><span style="color: #808080;">●</span> SPB1 PM2 - ⏰ 6:00 pm</strong><br>
            - 📌 Origen MXPB01<br>
            - 👉 Sin schedule / ocupo crowd 5 hrs a 30 SPR - depende puede mandarlas a 25 SPR<br>
            - 👉 Se carga en contingencia, no tiene ciclo normal creado<br>
            - 👉 Revisan volumen, notifican con palomita<br>
            - 👉 Pido validación</p>
        </div>

        
    """,
    "SIDE_LINE": """
        <h3 style='color: #000; margin-bottom: 5px;'>¿CÓMO LO HAGO?</h3>
        <hr style='border: 1px solid #1E90FF; margin-bottom: 20px;'>
        <div style='background: white; border-left: 6px solid #1E90FF; padding: 15px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); color: #000; margin-bottom: 20px;'>
            <p style='margin: 0;'>1️⃣ Descargo query de places (script job de SVC trabajado ▶️ ejecutar)<br>
            2️⃣ Routing matutino ▶️ busco lista places (sáb / dom)</p>
        </div>
        <div style='background: white; border-left: 6px solid #1E90FF; padding: 15px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); color: #000;'>
            <p style='margin: 0;'><strong>PASOS DETALLADOS:</strong><br>
            ▶️ Docto script job ▶️ BuscarV ▶️ columna U (customer id) ▶️ clic 1a celda<br>
            ▶️ En archivo places (copio desde place id / 5,0)<br>
            ▶️ Sale A, B ó C ▶️ copio y pego esos id´s ▶️ nueva pestaña en data (nombro "places")<br>
            ▶️ En data ▶️ buscarv para buscar en pestaña places<br>
            ▶️ No deben coincidir todos los id´s<br>
            ▶️ Lo que salga de cruce = places (no se rutea)<br><br>
            <strong>- Elijo "pasar al siguiente día"</strong><br>
            - C1 y C2 es el mismo proceso</p>
        </div>
    """,
    "ENLACES": """
        <h3 style='color: #000; margin-bottom: 5px;'>ENLACES</h3>
        <hr style='border: 1px solid #1E90FF; margin-bottom: 20px;'>
        <div style='background: white; border-left: 6px solid #1E90FF; padding: 15px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); color: #000;'>
            <div style='display: flex; flex-direction: column; gap: 15px;'>
                <a href="https://drive.google.com/drive/folders/1VNCUhdFxnV6MltnBFt4sH6AN_FJjL5jj" target="_blank" style="color: #1E90FF; text-decoration: none; font-weight: bold;">📁 SUBIR DATAS</a>
                <a href="https://docs.google.com/spreadsheets/d/1mj1krN2hXQQ1yFzswDoPscd9tPhguDnB-mAxB4aLPy0/edit" target="_blank" style="color: #1E90FF; text-decoration: none; font-weight: bold;">📅 SCHEDULE METRO</a>
                <a href="https://docs.google.com/spreadsheets/d/1lcrV9kxqwZB8007DPn4binDfDoD4enX26nISPWkOXDM/edit" target="_blank" style="color: #1E90FF; text-decoration: none; font-weight: bold;">📅 SCHEDULE CENTRO</a>
                <a href="https://docs.google.com/spreadsheets/d/1Gw1RG4XGfDCyz2lKmoj01OoOHQcaPpVagWCeKj-oCzE/edit" target="_blank" style="color: #1E90FF; text-decoration: none; font-weight: bold;">📅 SCHEDULE NORTE</a>
                <a href="https://docs.google.com/spreadsheets/d/1irZgPeFGGtJL2rRu2CYK6NHsjoieX-9DEA-rQCrRjKI/edit" target="_blank" style="color: #1E90FF; text-decoration: none; font-weight: bold;">📅 SCHEDULE SUR</a>
            </div>
        </div>
    """,
    "C1": "<div style='text-align:center; padding-top:100px; color:#666;'><i>Información C1 pendiente...</i></div>",
    "C2": "<div style='text-align:center; padding-top:100px; color:#666;'><i>Información C2 pendiente...</i></div>",
    "PREC": "<div style='text-align:center; padding-top:100px; color:#666;'><i>Información PRECARGA pendiente...</i></div>"
}

# 3. HTML/CSS (DISEÑO FINAL)
html_notitas = f"""
<style>
    body {{ background-color: #000; font-family: 'Segoe UI', Tahoma, sans-serif; margin: 0; }}
    .main-box {{ background: #000; padding: 10px; }}
    
    /* CONSOLA UNIFICADA (ARRIBA) */
    .unified-console {{
        background: #1a1a1a; border-radius: 15px; padding: 15px; 
        margin-bottom: 20px; border: 1px solid #333; text-align: center;
    }}
    .display-screen {{
        background: #000; border-radius: 10px; padding: 10px; margin-bottom: 15px; border: 2px solid #222;
    }}
    .btn-3d {{
        background: linear-gradient(145deg, #1e90ff, #1c82e6);
        color: white; border: none; padding: 12px 25px; border-radius: 10px;
        font-weight: bold; cursor: pointer; box-shadow: 0 5px #0a56a3; transition: 0.1s;
    }}
    .btn-3d:active {{ box-shadow: 0 2px #0a56a3; transform: translateY(3px); }}

    .tab-bar {{ display: flex; gap: 8px; margin-bottom: 15px; overflow-x: auto; }}
    .tab-btn {{
        background: #333; color: white; border: none; padding: 10px 18px;
        border-radius: 8px; cursor: pointer; font-weight: bold; font-size: 12px; white-space: nowrap;
    }}
    .tab-btn.active {{ background: #add8e6; color: black; box-shadow: 0 0 12px #add8e6; }}
    
    .content-area {{ background: #c8dee0; border-radius: 12px; padding: 20px; min-height: 600px; color: #000; }}
</style>

<div class="main-box">
    <div class="unified-console">
        <div class="display-screen">
            <div style="color: #888; font-size: 10px; margin-bottom: 5px;">HORA / RESTADOR / CONVERTIDOR</div>
            <div id="horaReal" style="font-size: 38px; color: #FF00FF; font-family: monospace; font-weight: bold;">--:--</div>
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

    <h3 style="color: #1E90FF; text-align: center; margin-bottom: 15px;">🍓 NOTITAS OPERATIVAS</h3>
    <div class="tab-bar">
        <button class="tab-btn active" onclick="changeTab(event, 'SDE')">SDE</button>
        <button class="tab-btn" onclick="changeTab(event, 'C1')">C1</button>
        <button class="tab-btn" onclick="changeTab(event, 'C2')">C2</button>
        <button class="tab-btn" onclick="changeTab(event, 'PREC')">PREC</button>
        <button class="tab-btn" onclick="changeTab(event, 'SIDE_LINE')">SIDE LINE</button>
        <button class="tab-btn" onclick="changeTab(event, 'ENLACES')">ENLACES</button>
    </div>
    <div id="visor" class="content-area">
        {info_operativa['SDE']}
    </div>
</div>

<script>
    const allData = {info_operativa}; 
    function changeTab(e, name) {{
        document.getElementById('visor').innerHTML = allData[name];
        let btns = document.getElementsByClassName('tab-btn');
        for (let b of btns) {{ b.classList.remove('active'); }}
        e.currentTarget.classList.add('active');
    }}
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

# 4. RENDERIZADO EN STREAMLIT
st.markdown("---")
components.html(html_notitas, height=1200, scrolling=True)
