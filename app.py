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
u_SDE = {"CROWD 5H": [25, 28], "CROWD 5H EXT": [25, 28], "CROWD 3H": [25, 28], "MOTO 3H": [25, 28]}
u_SD = {"MOTO 3H": [25, 25], "MOTO NEW": [20, 22], "CROWD 5H / SMALL V": [35, 37]}
u_C1 = {
    "RENTAL E. LARGE": [120, 120], "RENTAL E. SMALL": [120, 120], "RENTAL LARGE": [120, 120], 
    "RENTAL SMALL": [120, 120], "LARGE V VAR(MLP)": [100, 100], "SMALL V VAR(MLP)":[80, 80],
    "CAR MLP": [50, 50], "MOTO 3H": [28, 28], "CROWD NEW 3 hrs": [30, 30], "CROWD EXT 8H": [80, 85], "CROWD 5H": [60, 60]
}
u_C2 = u_C1.copy()
u_C2["LARGE VAN HÍB"] = [100, 100]

def gen_master_rows(data_dict, table_id):
    rows = ""
    items = list(data_dict.items())
    for i in range(15):
        is_real = i < len(items)
        name, spr = (items[i][0], items[i][1]) if is_real else ("NUEVA UNIDAD", [0, 0])
        st_base = "background: #ebebeb; color: #969696;"
        rows += f'''
        <tr class="master-row" style="{st_base}">
            <td contenteditable="true" class="edit-name" oninput="recalc()" style="font-weight: bold; text-align: left; padding-left: 10px; border: 0.5px solid #ccc; width: 150px;">{name}</td>
            <td contenteditable="true" class="edit-spr-min" oninput="recalc()" style="text-align: center; border: 0.5px solid #ccc; width: 45px;">{spr[0]}</td>
            <td contenteditable="true" class="edit-spr-max" oninput="recalc()" style="text-align: center; border: 0.5px solid #ccc; width: 45px;">{spr[1]}</td>
            <td contenteditable="true" class="edit-orh" style="text-align: center; border: 0.5px solid #ccc; width: 45px;">480</td>
            <td contenteditable="true" class="f-stock" oninput="recalc()" style="text-align: center; border: 0.5px solid #ccc; width: 55px; font-weight: bold; font-size: 13px;">0</td>
            <td class="f-left" style="font-weight: bold; text-align: center; border: 0.5px solid #ccc; width: 60px; font-size: 16px;">0</td>
        </tr>'''
    return rows

def gen_poligonos():
    polys = ""
    # Estilo de botones mejorado para que no se deformen
    btn_s = "cursor:pointer; border:none; background:rgba(0,0,0,0.08); color:#333; font-weight:bold; width:24px; height:24px; border-radius:4px; flex-shrink:0;"
    
    # Celda con Flexbox para mantener alineación
    # 'display:flex; justify-content:space-between; align-items:center;' es la clave
    cell_style_flex = "display:flex; justify-content:space-between; align-items:center; padding: 5px; min-height: 30px;"
    
    # CORRECCIÓN AQUÍ: Se añade background: #e3defa a la primera celda de fila_inner
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
        <td style="border: 0.5px solid #ccc; padding: 2px;"><select class="s-type" onchange="resetRow(this)" style="width:auto; min-width:120px; max-width:250px; border:none; background:transparent; font-weight:bold; font-size:12px; color:#333;"><option>SELECCIONAR...</option></select></td>
        <td style="width: 45px !important; text-align: center; border: 0.5px solid #ccc;"><input type="checkbox" class="ok-check" style="transform: scale(1.1);"></td>
</tr>'''
    for i in range(1, 11):
        polys += f'''

<div class="poligono-bloque" style="margin-bottom: 25px; box-shadow: 0 10px 20px rgba(0,0,0,0.1), 0 6px 6px rgba(0,0,0,0.1); border-radius: 12px; overflow: hidden; background: white; border: 1px solid #e1e1e1; transform: translateZ(0);">            <table style="width: 100%; border-collapse: collapse;">
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
                    <td rowspan="5" contenteditable="true" style="background: #f0f0f0; font-weight:bold; text-align:center; border: 1px solid #ccc; padding: 5px; color:#333;">PLAN {i}</td>
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
                    <td style="width: 45px !important; text-align: center; border: 0.5px solid #ccc;"><input type="checkbox" class="ok-check" style="transform: scale(1.1);"></td>
                </tr>
                {fila_inner}{fila_inner}{fila_inner}{fila_inner}
                    
                    
                    <tr style="background:#f8f9fa; height: 32px;"> <!-- Añadimos height: 32px -->
    <td colspan="2" style="text-align:center; font-weight:bold; border: 1px solid #ccc; font-size: 16px; color:#333;">ESTADO:</td>
    <td class="v-calculado-total" style="font-weight: bold; font-size: 16px; color: #d32f2f; border: 1px solid #ccc; text-align: center;">0</td>
    <!-- Aquí bajamos el colspan de 3 a 2 para dejarle espacio a la columna OK -->
    <td class="p-diff" colspan="2" style="text-align: center; font-weight: bold; border: 1px solid #ccc; font-size: 16px;">VACÍO</td>
    <!-- Esta es la celda que cierra la columna OK al final de la tabla -->
    <td style="width: 45px !important; border: 1px solid #ccc; background: #f0f0f0;"></td>
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
    border: 1px solid #696969;
}}

/* Bordes internos gris claro para el encabezado */
.meli-table th {{
    background: linear-gradient(180deg, #444444 0%, #111111 100%);
    color: white;
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
    border-bottom: 1px solid #eee; 
    border-right: 1px solid #eee;
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
    background: linear-gradient(180deg, #ffffff 0%, #e8e8e8 100%);
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
        .google-tool {{ background: linear-gradient(145deg, #ffffff, #f0f0f0); padding: 15px; border-radius: 15px; border: 1px solid #ddd; text-align: center; box-shadow: 5px 5px 15px #d1d1d1, -5px -5px 15px #ffffff; transition: transform 0.2s;}}
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
    
    </style>

    
</head>
<body>

<div id="google-alert">⚠️ <span id="alert-msg"></span> [ENTER para cerrar]</div>

<div style="display: flex; gap: 20px;">
    <!-- COLUMNA IZQUIERDA -->
    <div style="flex: 1;">
        <div style="background: #696969; color: white; padding: 10px; border-radius: 8px; text-align: center; font-weight: bold; margin-bottom: 10px;">📋 PLANIFICACIÓN POR POLÍGONOS</div>
        <div id="polys-2" class="p-content">{gen_poligonos()}</div>
        <div id="polys-3" class="p-content" style="display:none;">{gen_poligonos()}</div>
        <div id="polys-1" class="p-content" style="display:none;">{gen_poligonos()}</div>
        <div id="polys-4" class="p-content" style="display:none;">{gen_poligonos()}</div>
    </div>

    <!-- COLUMNA DERECHA -->
    <div style="width: 450px;">
        <div style="background: #000; color: white; padding: 10px; border-radius: 8px; font-weight: bold; text-align: center; margin-bottom: 10px;">🚚 DISPONIBILIDAD DE FLOTA</div>
        <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 5px;">
            <div>
                <button class="tab-btn active" onclick="showTab(2, this)">C1</button>
                <button class="tab-btn" onclick="showTab(3, this)">C2</button>
                <button class="tab-btn" onclick="showTab(1, this)">SD</button>
                <button class="tab-btn" onclick="showTab(4, this)">SDE</button>
            </div>
            <div style="padding-bottom: 5px;">
    <!-- BOTÓN ACTIVAS ACTUALIZADO -->
    <button class="filter-btn" onclick="filterRows(true)" 
        style="cursor:pointer; background: linear-gradient(180deg, #444 0%, #222 100%); color: white; border: 1px solid #111; font-size: 14px; padding: 8px 15px; border-radius: 5px; margin-right: 5px; font-weight: bold; box-shadow: 0 4px 0 #000; transition: all 0.05s; outline: none;">
        ACTIVAS
    </button>

    <!-- BOTÓN TODAS (Para que hagan juego) -->
    <button class="filter-btn" onclick="filterRows(false)" 
        style="cursor:pointer; background: #20B2AA; color:white; border:none; font-size:14px; padding:8px 15px; border-radius:5px; font-weight:bold; box-shadow: 0 4px 0 #167a75; transition: all 0.05s;">
        TODAS
    </button>
</div>
        </div>

        <!-- TABLAS CON ENCABEZADOS RESTAURADOS (CORREGIDO AL ORIGINAL) -->
        <div id="tab-2" class="t-content">
            <table class="meli-table">
                <thead>
                    <tr style="background: linear-gradient(180deg, #333333 0%, #1a1a1a 100%); color: white;">
                        <th rowspan="2" style="border-right: 0.5px solid #555; padding: 4px 8px; font-size: 11px; text-shadow: 1px 1px 2px #000; box-shadow: inset 0 1px 0 rgba(180deg, #000000 100%, #000000 100%); line-height: 1.2;">UNIDAD</th>
                        <th colspan="2" style="border-bottom: 0.5px solid #555; border-right: 0.5px solid #555; padding: 2px; font-size: 11px; letter-spacing: 1px; background: rgba(180deg, #000000 100%, #000000 100%); line-height: 1.2;">SPR</th>
                        <th rowspan="2" style="border-right: 0.5px solid #555; padding: 4px 8px; font-size: 11px; text-shadow: 1px 1px 2px #000; box-shadow: inset 0 1px 0 rgba(180deg, #000000 100%, #000000 100%); line-height: 1.2;">ORH</th>
                        <th rowspan="2" style="border-right: 0.5px solid #555; padding: 4px 8px; font-size: 11px; text-shadow: 1px 1px 2px #000; box-shadow: inset 0 1px 0 rgba(180deg, #000000 100%, #000000 100%); line-height: 1.2;">SCHED</th>
                        <th rowspan="2" style="padding: 4px 8px; font-size: 11px; text-shadow: 1px 1px 2px #000; box-shadow: inset 0 1px 0 rgba(180deg, #000000 100%, #000000 100%); line-height: 1.2;">ME QUEDAN</th>
                    </tr>
                    <tr>
                        <th style="border-right: 0.5px solid #555; padding: 2px; font-size: 10px; background: linear-gradient(180deg, #222 0%, #000 100%); color: white; line-height: 1.2;">MIN</th>
                        <th style="border-right: 0.5px solid #555; padding: 2px; font-size: 10px; background: linear-gradient(180deg, #222 0%, #000 100%); color: white; line-height: 1.2;">MAX</th>
                    </tr>
                </thead>
                <tbody id="body-2">{gen_master_rows(u_C1, 2)}</tbody>
            </table>
        </div>
        <div id="tab-3" class="t-content" style="display:none;">
            <table class="meli-table">
                <thead>
                    <tr style="background: linear-gradient(180deg, #3c3c3c 0%, #000000 100%); color: white;">
                        <th rowspan="2" style="border-right: 0.5px solid #555; padding: 4px 8px; font-size: 11px; text-shadow: 1px 1px 2px #000; box-shadow: inset 0 1px 0 rgba(255,255,255,0.1); line-height: 1.2;">UNIDAD</th>
                        <th colspan="2" style="border-bottom: 0.5px solid #555; border-right: 0.5px solid #555; padding: 2px; font-size: 11px; letter-spacing: 1px; background: rgba(255,255,255,0.05); line-height: 1.2;">SPR</th>
                        <th rowspan="2" style="border-right: 0.5px solid #555; padding: 4px 8px; font-size: 11px; text-shadow: 1px 1px 2px #000; box-shadow: inset 0 1px 0 rgba(255,255,255,0.1); line-height: 1.2;">ORH</th>
                        <th rowspan="2" style="border-right: 0.5px solid #555; padding: 4px 8px; font-size: 11px; text-shadow: 1px 1px 2px #000; box-shadow: inset 0 1px 0 rgba(255,255,255,0.1); line-height: 1.2;">SCHED</th>
                        <th rowspan="2" style="padding: 4px 8px; font-size: 11px; text-shadow: 1px 1px 2px #000; box-shadow: inset 0 1px 0 rgba(255,255,255,0.1); line-height: 1.2;">ME QUEDAN</th>
                    </tr>
                   <tr>
                        <th style="border-right: 0.5px solid #555; padding: 2px; font-size: 10px; background: linear-gradient(180deg, #222 0%, #000 100%); color: white; line-height: 1.2;">MIN</th>
                        <th style="border-right: 0.5px solid #555; padding: 2px; font-size: 10px; background: linear-gradient(180deg, #222 0%, #000 100%); color: white; line-height: 1.2;">MAX</th>
                    </tr>
                </thead>
                <tbody id="body-3">{gen_master_rows(u_C2, 3)}</tbody>
            </table>
        </div>
        <div id="tab-1" class="t-content" style="display:none;">
            <table class="meli-table">
                <thead>
                    <tr style="background: linear-gradient(180deg, #444 0%, #111 100%); color: white;">
                        <th rowspan="2" style="border-right: 0.5px solid #555; padding: 4px 8px; font-size: 11px; text-shadow: 1px 1px 2px #000; box-shadow: inset 0 1px 0 rgba(255,255,255,0.1); line-height: 1.2;">UNIDAD</th>
                        <th colspan="2" style="border-bottom: 0.5px solid #555; border-right: 0.5px solid #555; padding: 2px; font-size: 11px; letter-spacing: 1px; background: rgba(255,255,255,0.05); line-height: 1.2;">SPR</th>
                        <th rowspan="2" style="border-right: 0.5px solid #555; padding: 4px 8px; font-size: 11px; text-shadow: 1px 1px 2px #000; box-shadow: inset 0 1px 0 rgba(255,255,255,0.1); line-height: 1.2;">ORH</th>
                        <th rowspan="2" style="border-right: 0.5px solid #555; padding: 4px 8px; font-size: 11px; text-shadow: 1px 1px 2px #000; box-shadow: inset 0 1px 0 rgba(255,255,255,0.1); line-height: 1.2;">SCHED</th>
                        <th rowspan="2" style="padding: 4px 8px; font-size: 11px; text-shadow: 1px 1px 2px #000; box-shadow: inset 0 1px 0 rgba(255,255,255,0.1); line-height: 1.2;">ME QUEDAN</th>
                    </tr>
                    <tr>
                        <th style="border-right: 0.5px solid #555; padding: 2px; font-size: 10px; background: linear-gradient(180deg, #222 0%, #000 100%); color: white; line-height: 1.2;">MIN</th>
                        <th style="border-right: 0.5px solid #555; padding: 2px; font-size: 10px; background: linear-gradient(180deg, #222 0%, #000 100%); color: white; line-height: 1.2;">MAX</th>
                    </tr>
                </thead>
                <tbody id="body-1">{gen_master_rows(u_SD, 1)}</tbody>
            </table>
        </div>
        <div id="tab-4" class="t-content" style="display:none;">
            <table class="meli-table">
                <thead>
                    <tr style="background: linear-gradient(180deg, #444 0%, #111 100%); color: white;">
                        <th rowspan="2" style="border-right: 0.5px solid #555; padding: 4px 8px; font-size: 11px; text-shadow: 1px 1px 2px #000; box-shadow: inset 0 1px 0 rgba(255,255,255,0.05); line-height: 1.2;">UNIDAD</th>
                        <th colspan="2" style="border-bottom: 0.5px solid #555; border-right: 0.5px solid #555; padding: 2px; font-size: 11px; letter-spacing: 1px; background: rgba(255,255,255,0.05); line-height: 1.2;">SPR</th>
                        <th rowspan="2" style="border-right: 0.5px solid #555; padding: 4px 8px; font-size: 11px; text-shadow: 1px 1px 2px #000; box-shadow: inset 0 1px 0 rgba(255,255,255,0.05); line-height: 1.2;">ORH</th>
                        <th rowspan="2" style="border-right: 0.5px solid #555; padding: 4px 8px; font-size: 11px; text-shadow: 1px 1px 2px #000; box-shadow: inset 0 1px 0 rgba(255,255,255,0.05; line-height: 1.2;">SCHED</th>
                        <th rowspan="2" style="padding: 4px 8px; font-size: 11px; text-shadow: 1px 1px 2px #000; box-shadow: inset 0 1px 0 rgba(255,255,255,0.1); line-height: 1.2;">ME QUEDAN</th>
                    </tr>
                    <tr>
                        <th style="border-right: 0.5px solid #555; padding: 2px; font-size: 10px; background: linear-gradient(180deg, #222 0%, #000 100%); color: white; line-height: 1.2;">MIN</th>
                        <th style="border-right: 0.5px solid #555; padding: 2px; font-size: 10px; background: linear-gradient(180deg, #222 0%, #000 100%); color: white; line-height: 1.2;">MAX</th>
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
    let currentTab = 2;
    let editedRowsPlan = new Set();
    let curC = "";
    let chronoInterval;
    let startTime;
    let elapsedTime = 0;

    function showTab(n, btn) {{
        currentTab = n;
        document.querySelectorAll('.p-content, .t-content').forEach(el => el.style.display = 'none');
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.getElementById('polys-'+n).style.display = 'block';
        document.getElementById('tab-'+n).style.display = 'block';
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
                showAlert("⚠️ AGOTADO. No se puede aumentar.");
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
                cL.innerText = diff;
                cL.style.color = (diff < 0) ? "red" : (diff === 0 && fleet[n].stock > 0 ? "white" : "black");
                cL.style.background = (diff === 0 && fleet[n].stock > 0 ? "#d32f2f" : "transparent");
            }}
        }});

        document.querySelectorAll('#polys-' + currentTab + ' .s-type').forEach(s => {{
            let cur = s.value, opt = '<option>SELECCIONAR...</option>';
            Object.keys(fleet).forEach(k => {{ if(fleet[k].stock > 0 || k === cur) opt += `<option value="${{k}}">${{k}}</option>`; }});
            s.innerHTML = opt; s.value = cur;
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


    
    recalc();
</script>
</body>
</html>
"""

html(app_html, height=1200, scrolling=True)
