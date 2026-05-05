import streamlit as st
from streamlit.components.v1 import html

# Configuración de página con título personalizado
st.set_page_config(page_title="Monitor Logístico - Liliana García", layout="wide")

# Ocultar elementos de Streamlit y fondo limpio
st.markdown("""
    <style>
    .block-container {padding: 0rem !important;}
    footer, #MainMenu, header {visibility: hidden;}
    body { background-color: #f5f7f9; }
    </style>
""", unsafe_allow_html=True)

# --- 1. DATOS DE UNIDADES (CATÁLOGOS ACTUALIZADOS) ---
u_SDE = {"CROWD 5 HRS": [25, 28], "CROWD 5 HRS EXTENDIDA": [25, 28], "CROWD 3 HRS": [25, 28], "MOTO 3 HRS": [25, 28]}
u_SD = {"MOTO 3 HRS": [25, 25], "MOTO NEWBIE": [20, 22], "CROWD 5 HRS / SMALL VAN": [35, 37]}
u_C1 = {
    "RENTAL ELEC LARGE VAN": [120, 120], "RENTAL ELEC SMALL VAN": [120, 120], "RENTAL LARGE VAN": [120, 120], 
    "RENTAL SMALL VAN": [120, 120], "LARGE VAN VAR(MLP)": [100, 100], "SMALL VAN VAR(MLP)":[80, 80],
    "CAR MLP": [50, 50], "MOTO 3 HRS": [28, 28], "CROWD NEWBIE 3 hrs": [30, 30], "CROWD EXTRA 8 HRS": [80, 85], "CROWD 5 HRS": [60, 60]
}
u_C2 = u_C1.copy()
u_C2["LARGE VAN HÍBRIDA"] = [100, 100]

# --- 2. GENERADORES DE HTML CON DISEÑO FIJO (ESTILO COLAB) ---
def gen_master_rows(data_dict, table_id):
    rows = ""
    items = list(data_dict.items())
    for i in range(15):
        is_real = i < len(items)
        name, spr = (items[i][0], items[i][1]) if is_real else ("NUEVA UNIDAD", [0, 0])
        st_base = "background: #ebebeb; color: #969696;" if is_real else "background: #fcfcfc; color: #C0C0C0;"
        rows += f'''
        <tr data-table="{table_id}" class="master-row" style="{st_base}">
            <td contenteditable="true" class="edit-name" oninput="recalc()" style="font-weight: bold; text-align: left; padding-left: 10px; border: 0.5px solid #ccc; width: 140px; white-space: nowrap; overflow: visible;">{name}</td>
            <td contenteditable="true" class="edit-spr-min" oninput="recalc()" style="text-align: center; border: 0.5px solid #ccc; width: 35px;">{spr[0]}</td>
            <td contenteditable="true" class="edit-spr-max" oninput="recalc()" style="text-align: center; border: 0.5px solid #ccc; width: 35px;">{spr[1]}</td>
            <td contenteditable="true" class="edit-orh" style="text-align: center; border: 0.5px solid #ccc; width: 35px;">480</td>
            <td contenteditable="true" class="f-stock" oninput="recalc()" style="text-align: center; border: 0.5px solid #ccc; width: 35px; font-weight: bold;">0</td>
            <td class="f-left" style="font-weight: bold; text-align: center; border: 0.5px solid #ccc; width: 35px;">0</td>
        </tr>'''
    return rows

def gen_poligonos():
    polys = ""
    btn_s = "cursor:pointer; border:none; background:rgba(0,0,0,0.08); color:#333; font-weight:bold; width:22px; height:22px; border-radius:4px; margin:0 2px;"
    
    fila_inner = f'''
    <tr class="calc-row">
        <td class="u-manual-cell" style="background: #e3defa; text-align: center; border: 0.5px solid #ccc;">
            <button style="{btn_s}" onclick="stepVal(this, -1, 'u')">-</button>
            <span contenteditable="true" class="u-manual" oninput="manualEdit(this)" style="font-weight: bold; margin:0 5px;">0</span>
            <button style="{btn_s}" onclick="stepVal(this, 1, 'u')">+</button>
        </td>
        <td class="spr-real-cell" style="background: #def3ed; text-align: center; border: 0.5px solid #ccc;">
            <button style="{btn_s}" onclick="stepVal(this, -1, 's')">-</button>
            <span contenteditable="true" class="spr-real-val" oninput="manualEdit(this)" style="font-weight: bold; margin:0 5px;">0</span>
            <button style="{btn_s}" onclick="stepVal(this, 1, 's')">+</button>
        </td>
        <td style="border: 0.5px solid #ccc; padding: 2px;"><select class="s-type" onchange="resetRow(this)" style="width:100%; border:none; background:transparent; font-weight:bold; font-size:11px; color:#333;"><option>SELECCIONAR...</option></select></td>
        <td style="text-align: center; border: 0.5px solid #ccc;"><input type="checkbox" class="ok-check" style="transform: scale(1.3); cursor:pointer;"></td>
    </tr>'''
    
    for i in range(1, 11):
        polys += f'''
        <div class="poligono-bloque" style="margin-bottom: 20px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); border-radius: 8px; overflow: visible; background: white; border: 1px solid #ccc;">
            <table class="meli-table tabla-planes" style="width: 100%; border-collapse: collapse; table-layout: fixed;">
                <thead>
                    <tr style="background: linear-gradient(180deg, #888888 0%, #696969 100%); color: white; font-size: 11px; height: 35px;">
                        <th style="padding: 0 10px; width: 60px;">PLAN 1</th>
                        <th style="width: 60px;">VOL. TOTAL</th>
                        <th style="width: 90px;"># ASIGNADAS</th>
                        <th style="width: 90px;">SPR REAL</th>
                        <th style="width: 200px;">TIPO DE UNIDAD</th>
                        <th style="width: 35px;">OK</th>
                    </tr>
                </thead>
                <tbody>
                    <tr class="calc-row">
                        <td rowspan="5" style="background: #f0f0f0; font-weight:bold; text-align:center; border: 1px solid #ccc; width: 60px; color:#333;">PLAN {i}</td>
                        <td rowspan="5" contenteditable="true" class="v-total-val" oninput="recalc()" style="color: #20B2AA; font-weight: bold; font-size: 18px; text-align: center; border: 1px solid #ccc; width: 60px;">0</td>
                        <td class="u-manual-cell" style="background: #e3defa; text-align: center; border: 0.5px solid #ccc; width: 90px;">
                            <button style="{btn_s}" onclick="stepVal(this, -1, 'u')">-</button>
                            <span contenteditable="true" class="u-manual" oninput="manualEdit(this)" style="font-weight: bold; margin:0 5px;">0</span>
                            <button style="{btn_s}" onclick="stepVal(this, 1, 'u')">+</button>
                        </td>
                        <td class="spr-real-cell" style="background: #def3ed; text-align: center; border: 0.5px solid #ccc; width: 90px;">
                            <button style="{btn_s}" onclick="stepVal(this, -1, 's')">-</button>
                            <span contenteditable="true" class="spr-real-val" oninput="manualEdit(this)" style="font-weight: bold; margin:0 5px;">0</span>
                            <button style="{btn_s}" onclick="stepVal(this, 1, 's')">+</button>
                        </td>
                        <td style="border: 0.5px solid #ccc; padding: 2px; width: 200px; white-space: nowrap; overflow: visible;"><select class="s-type" onchange="resetRow(this)" style="width:100%; border:none; background:transparent; font-weight:bold; font-size:11px; color:#333;"><option>SELECCIONAR...</option></select></td>
                        <td style="text-align: center; border: 0.5px solid #ccc; width: 35px;"><input type="checkbox" class="ok-check" style="transform: scale(1.3); cursor:pointer;"></td>
                    </tr>
                    {fila_inner}{fila_inner}{fila_inner}{fila_inner}
                    <tr style="background:#f8f9fa; height: 30px;">
                        <td colspan="2" style="text-align:center; font-weight:bold; border: 1px solid #ccc; font-size: 11px; color:#333;">ESTADO:</td>
                        <td class="v-calculado-total" style="font-weight: bold; font-size: 16px; color: #d32f2f; border: 1px solid #ccc; text-align: center;">0</td>
                        <td class="p-diff" colspan="3" style="text-align: center; font-weight: bold; border: 1px solid #ccc; font-size: 11px;">VACÍO</td>
                    </tr>
                </tbody>
            </table>
        </div>'''
    return polys

# --- 3. ENSAMBLAJE DE LA INTERFAZ COMPLETA ---
# Aquí se insertará el código HTML/JS/CSS que definiremos en la Parte 2.
app_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<!-- Pega aquí el CSS de la Parte 2 -->
</head>
<body>
<!-- Pega aquí el HTML de la Parte 2 -->
<!-- Pega aquí el JS de la Parte 2 -->
</body>
</html>
"""

# Renderizado final
# Se fija el ancho del HTML para evitar colapsos
html(app_html, width=1350, height=1500, scrolling=True)
