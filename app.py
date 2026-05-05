import streamlit as st
from streamlit.components.v1 import html

# Configuración de página con título personalizado
st.set_page_config(page_title="Monitor Logístico - Liliana García", layout="wide")

# CSS para ocultar elementos de Streamlit y forzar el diseño limpio
st.markdown("""
    <style>
    .block-container {padding: 0rem !important;}
    footer, #MainMenu, header {visibility: hidden;}
    body { background-color: #f5f7f9; }
    </style>
""", unsafe_allow_html=True)

# --- 1. DATOS DE UNIDADES (CATÁLOGOS EXTRAÍDOS DE COLAB) ---
u_SDE = {"CROWD 5 HRS": [25, 28], "CROWD 5 HRS EXTENDIDA": [25, 28], "CROWD 3 HRS": [25, 28], "MOTO 3 HRS": [25, 28]}
u_SD = {"MOTO 3 HRS": [25, 25], "MOTO NEWBIE": [20, 22], "CROWD 5 HRS / SMALL VAN": [35, 37]}
u_C1 = {
    "RENTAL ELEC LARGE VAN": [120, 120], "RENTAL ELEC SMALL VAN": [120, 120], "RENTAL LARGE VAN": [120, 120], 
    "RENTAL SMALL VAN": [120, 120], "LARGE VAN VAR(MLP)": [100, 100], "SMALL VAN VAR(MLP)":[80, 80],
    "CAR MLP": [50, 50], "MOTO 3 HRS": [28, 28], "CROWD NEWBIE 3 hrs": [30, 30], "CROWD EXTRA 8 HRS": [80, 85], "CROWD 5 HRS": [60, 60]
}
u_C2 = u_C1.copy()
u_C2["LARGE VAN HÍBRIDA"] = [100, 100]

# --- 2. GENERADORES DE HTML (RESTAURADOS CON ESTILO 3D) ---
def gen_master_rows(data_dict, table_id):
    rows = ""
    items = list(data_dict.items())
    for i in range(15):
        is_real = i < len(items)
        name, spr = (items[i][0], items[i][1]) if is_real else ("NUEVA UNIDAD", [0, 0])
        
        # Estilo Base Gris (Inactivo) - Igual a Colab
        st_base = "background: #ebebeb; color: #969696;" if is_real else "background: #fcfcfc; color: #C0C0C0;"
        
        rows += f'''
        <tr data-table="{table_id}" class="master-row" style="{st_base}">
            <td contenteditable="true" class="edit-name" oninput="recalc()" style="font-weight: bold; text-align: left; padding-left: 10px; border: 0.5px solid #ccc; width: 150px; white-space: nowrap;">{name}</td>
            <td contenteditable="true" class="edit-spr-min" oninput="recalc()" style="text-align: center; border: 0.5px solid #ccc; width: 45px;">{spr[0]}</td>
            <td contenteditable="true" class="edit-spr-max" oninput="recalc()" style="text-align: center; border: 0.5px solid #ccc; width: 45px;">{spr[1]}</td>
            <td contenteditable="true" class="edit-orh" style="text-align: center; border: 0.5px solid #ccc; width: 45px;">480</td>
            <td contenteditable="true" class="f-stock" oninput="recalc()" style="text-align: center; border: 0.5px solid #ccc; width: 55px;">0</td>
            <td class="f-left" style="font-weight: bold; text-align: center; border: 0.5px solid #ccc; width: 60px;">0</td>
        </tr>'''
    return rows

def gen_poligonos():
    polys = ""
    btn_s = "cursor:pointer; border:none; background:rgba(0,0,0,0.08); color:#333; font-weight:bold; width:22px; height:22px; border-radius:4px; margin:0 2px;"
    
    fila_inner = f'''
    <tr class="calc-row">
        <td class="u-manual-cell" style="background: #e3defa; text-align: center; border: 0.5px solid #ccc; box-shadow: inset 1px 1px 2px rgba(0,0,0,0.1);">
            <button style="{btn_s}" onclick="stepVal(this, -1, 'u')">-</button>
            <span contenteditable="true" class="u-manual" oninput="manualEdit(this)" style="font-weight: bold; color:black; margin:0 5px;">0</span>
            <button style="{btn_s}" onclick="stepVal(this, 1, 'u')">+</button>
        </td>
        <td class="spr-real-cell" style="background: #def3ed; text-align: center; border: 0.5px solid #ccc; box-shadow: inset 1px 1px 2px rgba(0,0,0,0.1);">
            <button style="{btn_s}" onclick="stepVal(this, -1, 's')">-</button>
            <span contenteditable="true" class="spr-real-val" oninput="manualEdit(this)" style="font-weight: bold; color:black; margin:0 5px;">0</span>
            <button style="{btn_s}" onclick="stepVal(this, 1, 's')">+</button>
        </td>
        <td style="border: 0.5px solid #ccc; padding: 2px;"><select class="s-type" onchange="resetRow(this)" style="width:100%; border:none; background:transparent; font-weight:bold; color:#333; font-size:11px;"><option>SELECCIONAR...</option></select></td>
        <td style="text-align: center; border: 0.5px solid #ccc;"><input type="checkbox" class="ok-check" style="transform: scale(1.6); cursor:pointer; margin:0;"></td>
    </tr>'''
    
    for i in range(1, 11):
        polys += f'''
        <div class="poligono-bloque" style="margin-bottom: 20px; box-shadow: 5px 5px 15px rgba(0,0,0,0.15); border-radius: 12px; overflow: hidden; background: white; border: 1px solid #ccc; transform: perspective(1000px);">
            <table class="meli-table tabla-planes" style="width: 100%; border-collapse: collapse; table-layout: fixed;">
                <thead>
                    <tr style="background: linear-gradient(180deg, #888888 0%, #696969 100%); color: white;">
                        <th style="padding: 10px; border: 0.5px solid #777; width: 100px; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);">PLAN {i}</th>
                        <th style="padding: 10px; border: 0.5px solid #777; width: 90px; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);">VOL. TOTAL</th>
                        <th style="padding: 10px; border: 0.5px solid #777; width: 110px; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);"># ASIGNADAS</th>
                        <th style="padding: 10px; border: 0.5px solid #777; width: 110px; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);">SPR REAL</th>
                        <th style="padding: 10px; border: 0.5px solid #777; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);">TIPO DE UNIDAD</th>
                        <th style="padding: 10px; border: 0.5px solid #777; width: 50px; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);">OK</th>
                    </tr>
                </thead>
                <tbody>
                    <tr class="calc-row">
                        <td rowspan="5" contenteditable="true" class="v-total" style="background: linear-gradient(145deg, #d3d3d3, #e6e6e6); font-weight:bold; text-align:center; border: 1px solid #808080; color: #333; font-size: 14px; box-shadow: inset 2px 2px 5px rgba(0,0,0,0.1);">PLAN {i}</td>
                        <td rowspan="5" contenteditable="true" class="v-total-val" oninput="recalc()" style="color: #20B2AA; font-weight: bold; font-size: 20px; text-align: center; border: 1px solid #808080; text-shadow: 1px 1px 2px rgba(0,0,0,0.1); background: white;">0</td>
                        <td class="u-manual-cell" style="background: #e3defa; text-align: center; border: 0.5px solid #ccc; box-shadow: inset 1px 1px 2px rgba(0,0,0,0.1);">
                            <button style="{btn_s}" onclick="stepVal(this, -1, 'u')">-</button>
                            <span contenteditable="true" class="u-manual" oninput="manualEdit(this)" style="font-weight: bold; color:black;">0</span>
                            <button style="{btn_s}" onclick="stepVal(this, 1, 'u')">+</button>
                        </td>
                        <td class="spr-real-cell" style="background: #def3ed; text-align: center; border: 0.5px solid #ccc; box-shadow: inset 1px 1px 2px rgba(0,0,0,0.1);">
                            <button style="{btn_s}" onclick="stepVal(this, -1, 's')">-</button>
                            <span contenteditable="true" class="spr-real-val" oninput="manualEdit(this)" style="font-weight: bold; color:black;">0</span>
                            <button style="{btn_s}" onclick="stepVal(this, 1, 's')">+</button>
                        </td>
                        <td style="border: 0.5px solid #ccc; padding: 2px;"><select class="s-type" onchange="resetRow(this)" style="width:100%; border:none; background:transparent; font-weight:bold; color:#333; font-size:11px;"><option>SELECCIONAR...</option></select></td>
                        <td style="text-align: center; border: 0.5px solid #ccc;"><input type="checkbox" class="ok-check" style="transform: scale(1.6); cursor:pointer;"></td>
                    </tr>
                    {fila_inner}{fila_inner}{fila_inner}{fila_inner}
                    <tr style="height: 30px;">
                        <td colspan="2" style="text-align:center; font-weight:bold; background:#f8f9fa; border: 1px solid #808080; color:#333; font-size: 12px; letter-spacing: 1px;">ESTADO:
```python
import streamlit as st
from streamlit.components.v1 import html

# Configuración de página con título personalizado
st.set_page_config(page_title="Monitor Logístico - Liliana García", layout="wide")

# CSS para ocultar elementos de Streamlit y forzar el diseño limpio
st.markdown("""
    <style>
    .block-container {padding: 0rem !important;}
    footer, #MainMenu, header {visibility: hidden;}
    body { background-color: #f5f7f9; }
    </style>
""", unsafe_allow_html=True)

# --- 1. DATOS DE UNIDADES (CATÁLOGOS EXTRAÍDOS DE COLAB) ---
u_SDE = {"CROWD 5 HRS": [25, 28], "CROWD 5 HRS EXTENDIDA": [25, 28], "CROWD 3 HRS": [25, 28], "MOTO 3 HRS": [25, 28]}
u_SD = {"MOTO 3 HRS": [25, 25], "MOTO NEWBIE": [20, 22], "CROWD 5 HRS / SMALL VAN": [35, 37]}
u_C1 = {
    "RENTAL ELEC LARGE VAN": [120, 120], "RENTAL ELEC SMALL VAN": [120, 120], "RENTAL LARGE VAN": [120, 120], 
    "RENTAL SMALL VAN": [120, 120], "LARGE VAN VAR(MLP)": [100, 100], "SMALL VAN VAR(MLP)":[80, 80],
    "CAR MLP": [50, 50], "MOTO 3 HRS": [28, 28], "CROWD NEWBIE 3 hrs": [30, 30], "CROWD EXTRA 8 HRS": [80, 85], "CROWD 5 HRS": [60, 60]
}
u_C2 = u_C1.copy()
u_C2["LARGE VAN HÍBRIDA"] = [100, 100]

# --- 2. GENERADORES DE HTML (RESTAURADOS CON ESTILO 3D) ---
def gen_master_rows(data_dict, table_id):
    rows = ""
    items = list(data_dict.items())
    for i in range(15):
        is_real = i < len(items)
        name, spr = (items[i][0], items[i][1]) if is_real else ("NUEVA UNIDAD", [0, 0])
        
        # Estilo Base Gris (Inactivo) - Igual a Colab
        st_base = "background: #ebebeb; color: #969696;" if is_real else "background: #fcfcfc; color: #C0C0C0;"
        
        rows += f'''
        <tr data-table="{table_id}" class="master-row" style="{st_base}">
            <td contenteditable="true" class="edit-name" oninput="recalc()" style="font-weight: bold; text-align: left; padding-left: 10px; border: 0.5px solid #ccc; width: 150px; white-space: nowrap;">{name}</td>
            <td contenteditable="true" class="edit-spr-min" oninput="recalc()" style="text-align: center; border: 0.5px solid #ccc; width: 45px;">{spr[0]}</td>
            <td contenteditable="true" class="edit-spr-max" oninput="recalc()" style="text-align: center; border: 0.5px solid #ccc; width: 45px;">{spr[1]}</td>
            <td contenteditable="true" class="edit-orh" style="text-align: center; border: 0.5px solid #ccc; width: 45px;">480</td>
            <td contenteditable="true" class="f-stock" oninput="recalc()" style="text-align: center; border: 0.5px solid #ccc; width: 55px;">0</td>
            <td class="f-left" style="font-weight: bold; text-align: center; border: 0.5px solid #ccc; width: 60px;">0</td>
        </tr>'''
    return rows

def gen_poligonos():
    polys = ""
    btn_s = "cursor:pointer; border:none; background:rgba(0,0,0,0.08); color:#333; font-weight:bold; width:22px; height:22px; border-radius:4px; margin:0 2px;"
    
    fila_inner = f'''
    <tr class="calc-row">
        <td class="u-manual-cell" style="background: #e3defa; text-align: center; border: 0.5px solid #ccc; box-shadow: inset 1px 1px 2px rgba(0,0,0,0.1);">
            <button style="{btn_s}" onclick="stepVal(this, -1, 'u')">-</button>
            <span contenteditable="true" class="u-manual" oninput="manualEdit(this)" style="font-weight: bold; color:black; margin:0 5px;">0</span>
            <button style="{btn_s}" onclick="stepVal(this, 1, 'u')">+</button>
        </td>
        <td class="spr-real-cell" style="background: #def3ed; text-align: center; border: 0.5px solid #ccc; box-shadow: inset 1px 1px 2px rgba(0,0,0,0.1);">
            <button style="{btn_s}" onclick="stepVal(this, -1, 's')">-</button>
            <span contenteditable="true" class="spr-real-val" oninput="manualEdit(this)" style="font-weight: bold; color:black; margin:0 5px;">0</span>
            <button style="{btn_s}" onclick="stepVal(this, 1, 's')">+</button>
        </td>
        <td style="border: 0.5px solid #ccc; padding: 2px;"><select class="s-type" onchange="resetRow(this)" style="width:100%; border:none; background:transparent; font-weight:bold; color:#333; font-size:11px;"><option>SELECCIONAR...</option></select></td>
        <td style="text-align: center; border: 0.5px solid #ccc;"><input type="checkbox" class="ok-check" style="transform: scale(1.6); cursor:pointer; margin:0;"></td>
    </tr>'''
    
    for i in range(1, 11):
        polys += f'''
        <div class="poligono-bloque" style="margin-bottom: 20px; box-shadow: 5px 5px 15px rgba(0,0,0,0.15); border-radius: 12px; overflow: hidden; background: white; border: 1px solid #ccc; transform: perspective(1000px);">
            <table class="meli-table tabla-planes" style="width: 100%; border-collapse: collapse; table-layout: fixed;">
                <thead>
                    <tr style="background: linear-gradient(180deg, #888888 0%, #696969 100%); color: white;">
                        <th style="padding: 10px; border: 0.5px solid #777; width: 100px; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);">PLAN {i}</th>
                        <th style="padding: 10px; border: 0.5px solid #777; width: 90px; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);">VOL. TOTAL</th>
                        <th style="padding: 10px; border: 0.5px solid #777; width: 110px; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);"># ASIGNADAS</th>
                        <th style="padding: 10px; border: 0.5px solid #777; width: 110px; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);">SPR REAL</th>
                        <th style="padding: 10px; border: 0.5px solid #777; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);">TIPO DE UNIDAD</th>
                        <th style="padding: 10px; border: 0.5px solid #777; width: 50px; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);">OK</th>
                    </tr>
                </thead>
                <tbody>
                    <tr class="calc-row">
                        <td rowspan="5" contenteditable="true" class="v-total" style="background: linear-gradient(145deg, #d3d3d3, #e6e6e6); font-weight:bold; text-align:center; border: 1px solid #808080; color: #333; font-size: 14px; box-shadow: inset 2px 2px 5px rgba(0,0,0,0.1);">PLAN {i}</td>
                        <td rowspan="5" contenteditable="true" class="v-total-val" oninput="recalc()" style="color: #20B2AA; font-weight: bold; font-size: 20px; text-align: center; border: 1px solid #808080; text-shadow: 1px 1px 2px rgba(0,0,0,0.1); background: white;">0</td>
                        <td class="u-manual-cell" style="background: #e3defa; text-align: center; border: 0.5px solid #ccc; box-shadow: inset 1px 1px 2px rgba(0,0,0,0.1);">
                            <button style="{btn_s}" onclick="stepVal(this, -1, 'u')">-</button>
                            <span contenteditable="true" class="u-manual" oninput="manualEdit(this)" style="font-weight: bold; color:black;">0</span>
                            <button style="{btn_s}" onclick="stepVal(this, 1, 'u')">+</button>
                        </td>
                        <td class="spr-real-cell" style="background: #def3ed; text-align: center; border: 0.5px solid #ccc; box-shadow: inset 1px 1px 2px rgba(0,0,0,0.1);">
                            <button style="{btn_s}" onclick="stepVal(this, -1, 's')">-</button>
                            <span contenteditable="true" class="spr-real-val" oninput="manualEdit(this)" style="font-weight: bold; color:black;">0</span>
                            <button style="{btn_s}" onclick="stepVal(this, 1, 's')">+</button>
                        </td>
                        <td style="border: 0.5px solid #ccc; padding: 2px;"><select class="s-type" onchange="resetRow(this)" style="width:100%; border:none; background:transparent; font-weight:bold; color:#333; font-size:11px;"><option>SELECCIONAR...</option></select></td>
                        <td style="text-align: center; border: 0.5px solid #ccc;"><input type="checkbox" class="ok-check" style="transform: scale(1.6); cursor:pointer;"></td>
                    </tr>
                    {fila_inner}{fila_inner}{fila_inner}{fila_inner}
                    <tr style="height: 30px;">
                        <td colspan="2" style="text-align:center; font-weight:bold; background:#f8f9fa; border: 1px solid #808080; color:#333; font-size: 12px; letter-spacing: 1px;">ESTADO:</td>
                        <td class="v-calculado-total" style="font-weight: bold; font-size: 20px; color: #d32f2f; border: 1px solid #808080; text-align: center; background: white;">0</td>
                        <td class="p-diff" colspan="3" style="text-align: center; font-weight: bold; border: 1px solid #808080; color: #333; font-size: 11px;">VACÍO</td>
                    </tr>
                </tbody>
            </table>
        </div>'''
    return polys

# --- 3. ENSAMBLAJE DE LA INTERFAZ (RESTABLECIENDO POSICIONES Y ESTILOS) ---
app_html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: 'Segoe UI', sans-serif; background: #f5f7f9; padding: 20px; }}
        .meli-table {{ border-collapse: separate !important; border-spacing: 0; table-layout: fixed; }}
        .meli-table td, .meli-table th {{ height: 26px; }}
        
        #google-alert {{ 
            position: fixed; top: -150px; left: 50%; transform: translateX(-50%);
            background: rgba(211, 47, 47, 0.95); color: white; padding: 15px 30px; border-radius: 12px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5); transition: 0.5s;
            z-index: 99999; text-align: center; border: 2px solid #fff; min-width: 400px;
        }}
        #google-alert.show {{ top: 30px; }}
        
        #calc_container {{ 
            background: linear-gradient(145deg, #22c5bc, #1da29b) !important;
            border-radius: 25px !important; padding: 20px !important;
            box-shadow: 8px 8px 16px #acacac, -8px -8px 16px #ffffff, inset 1px 1px 2px rgba(255,255,255,0.3) !important;
            outline:none; transform: perspective(1000px) rotateX(2deg); border: 1px solid #178f88 !important;
        }}
        #calc_container:focus {{ outline: 5px solid #FF00FF !important; box-shadow: 0 0 25px rgba(255, 0, 255, 0.7) !important; }}
        .btn-calc {{ border-radius: 8px; background: linear-gradient(180deg, #ffffff 0%, #f0f4f8 100%); box-shadow: 2px 2px 5px rgba(0,0,0,0.2); cursor: pointer; font-weight: bold; padding: 10px; border: 1px solid #ccc; }}
        .btn-calc:active {{ transform: translateY(2px); box-shadow: inset 2px 2px 5px rgba(0,0,0,0.3) !important; }}

        .tab-btn {{ padding: 10px 20px; cursor: pointer; border: none; background: linear-gradient(180deg, #f0f0f0 0%, #e0e0e0 100%); border-radius: 8px 8px 0 0; font-weight: bold; box-shadow: 0 -2px 5px rgba(0,0,0,0.05); color: #333; }}
        .tab-btn.active {{ background: linear-gradient(180deg, #333 0%, #000 100%) !important; color: white !important; box-shadow: inset 0 2px 5px rgba(0,0,0,0.3); position: relative; top: 1px; }}
        
        .btn-activas-todas {{ padding: 8px 15px; cursor: pointer; font-weight: bold; border-radius: 6px; border: 1px solid rgba(0,0,0,0.2); box-shadow: 2px 2px 4px rgba(0,0,0,0.2); transition: 0.2s; }}
        .btn-activas-todas:active {{ transform: translateY(1px); box-shadow: none; }}
    </style>
</head>
<body>

<div id="google-alert">
    <div style="font-size: 20px; font-weight: bold; margin-bottom: 5px;">⚠️ ATENCIÓN</div>
    <div id="alert-msg" style="font-size: 16px;">Mensaje</div>
    <div style="margin-top: 10px; font-size: 12px;">Presiona [ENTER] para cerrar</div>
</div>

<div style="display: flex; gap: 20px; width: 100%; max-width: 1300px; margin: 0 auto;">
    <!-- Panel Izquierdo: Planes -->
    <div style="flex: 1.2; width: 0;">
        <div style="background: linear-gradient(180deg, #888888 0%, #696969 100%); color: white; padding: 12px; border-radius: 10px; text-align: center; font-weight: bold; margin-bottom: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.2); text-shadow: 1px 1px 2px rgba(0,0,0,0.5);">📋 PLANES GENERADOS</div>
        <div id="polys-2" class="p-content">{gen_poligonos()}</div>
        <div id="polys-3" class="p-content" style="display:none;">{gen_poligonos()}</div>
        <div id="polys-1" class="p-content" style="display:none;">{gen_poligonos()}</div>
        <div id="polys-4" class="p-content" style="display:none;">{gen_poligonos()}</div>
    </div>

    <!-- Panel Derecho: Flota -->
    <div style="width: 460px; flex-shrink: 0; position: sticky; top: 10px;">
        <div class="main-header-flota" style="background: linear-gradient(180deg, #333333 0%, #000000 100%); color: white; padding: 12px; border-radius: 10px; font-weight: bold; margin-bottom: 10px; text-align: center; box-shadow: 0 4px 10px rgba(0,0,0,0.2);">🚚 DISPONIBILIDAD DE FLOTA</div>
        
        <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 0px;">
            <div>
                <button class="tab-btn active" onclick="showTab(2, this)">C1</button>
                <button class="tab-btn" onclick="showTab(3, this)">C2</button>
                <button class="tab-btn" onclick="showTab(1, this)">SD</button>
                <button class="tab-btn" onclick="showTab(4, this)">SDE</button>
            </div>
            <!-- RESTAURACIÓN DE BOTONES -->
            <div style="padding-bottom: 5px;">
                <button onclick="filterFlota(true)" class="btn-activas-todas" style="background: #C0C0C0; color: #333;">ACTIVAS</button>
                <button onclick="filterFlota(false)" class="btn-activas-todas" style="background: #20B2AA; color: white;">TODAS</button>
            </div>
        </div>

        <div style="background: white; padding: 15px; border-radius: 0 0 12px 12px; border: 1px solid #ccc; box-shadow: 5px 5px 15px rgba(0,0,0,0.1); transform: perspective(1000px);">
            <div id="tab-2" class="t-content"><table class="meli-table tabla-flota" style="width:100%"><thead style="background: linear-gradient(180deg, #333333 0%, #000000 100%); color:white;"><tr><th rowspan="2" style="width:150px;">UNIDADES (C1)</th><th colspan="2">SPR</th><th rowspan="2" style="width:45px;">ORH</th><th rowspan="2" style="width:55px;">SCHED</th><th rowspan="2" style="width:60px;">ME QUEDAN</th></tr><tr><th style="width:45px;">min</th><th style="width:45px;">max</th></tr></thead><tbody id="body-2">{gen_master_rows(u_C1, 2)}</tbody></table></div>
            <div id="tab-3" class="t-content" style="display:none;"><table class="meli-table tabla-flota" style="width:100%"><thead style="background: linear-gradient(180deg, #333333 0
