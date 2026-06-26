import json
import streamlit as st
import pandas as pd
import io
from streamlit.components.v1 import html      

st.set_page_config(page_title="Monitor Logístico - Liliana García", layout="wide", initial_sidebar_state="expanded")

# CSS para diseño limpio 
st.markdown("""
    <style>
    .block-container {padding: 0rem !important;}
    footer, #MainMenu, header {visibility: hidden;}
    body { background-color: #25282b; }

    #contenedor-padre { display: flex; flex-direction: column; }
    
    .delta { display: none !important; }

    #visor { padding-right: 210px !important; box-sizing: border-box; }
    
    .tabla-flota-reducida {
        max-width: 80% !important;
        margin-left: 0 !important;
        margin-right: auto;
    }
    </style>
    """, unsafe_allow_html=True)


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
    "ESCÁRCEGA",
    "CAMPECHE",
    "ESCÁRCEGA EXT",
    "MAXCANUN",
    "CANDELARIA",
    "SEYBAPLAYA",
    "CHAMPOTÓN",
    "HOLPECHEN",
    "CALKINI",
    "PLAN 10"
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
    "Extra Large Van MLP H&B": [70, 70],
    "Rental Electric Large Van": [150, 150],
    "Rental Large Van": [120, 120],
    "Rental Replacement": [120, 120],
    "Truck 3.5 tons MLP": [1, 1], 
    "Media milla SP": [1, 1], 
    "Car 8h": [70, 70], 
    "Car Newbie": [70, 70],
    "Moto 3h": [30, 30],
    "Small Van 9h": [70, 70],
    "Small Van 9h Ext": [70, 70],
    "Small Van Newbie": [70, 70]
}

NOMBRES_PLANES_C1_SJA1 = [
   "ACTOPAN", "CENTRO 1", "CENTRO 2", "MISANTLA", "NAOLINCO", "PEROTE", "TEZUITLAN", "TLALTETELA", "TRAPICHE",  
   "TUZAMAPA", "XICO", "PLAN 12", "PLAN 13", "PLAN 14", "PLAN 15", "PLAN 16", "PLAN 17", "PLAN 18", "PLAN 19", "PLAN 20" 
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

    mostrar_orh_ocup = (table_id in [1, 2, 6])

    num_filas_objetivo = 45 if table_id == "PREC" else 4
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

        if "---" in name:
            colspan = 7 if mostrar_orh_ocup else 5

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

        else:
            st_base = "background: #ebebeb; color: #969696;" if not name else ""

            celdas_orh_ocup = ""
            if mostrar_orh_ocup:
                celdas_orh_ocup = f'''
                <td contenteditable="true" class="edit-orh" oninput="recalc()"
                    style="text-align:center; border:0.2px solid #25282b; width:45px; background:#ffffff; color:#25282b;">
                    0
                </td>
                <td contenteditable="true" class="edit-ocup" oninput="recalc()"
                    style="text-align:center; border:0.2px solid #25282b; width:70px; background:#ffffff; color:#25282b;">
                    0
                </td>
                '''
            else:
                celdas_orh_ocup = '''
                <td class="edit-orh" style="display:none;">0</td>
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
        data.append({
            "PLAN": "C1",
            "UNIDAD": unidad,
            "SPR_MIN": spr[0],
            "SPR_MAX": spr[1]
        })

    df_c1 = pd.DataFrame(data)
    csv = df_c1.to_csv(index=False).encode("utf-8")
    return csv


def gen_poligonos(data_target=None):
    polys = '''
    <div id="mi-contador" style="position: fixed; top: 10px; right: 220px; background: #000; color: #fff; padding: 10px; border-radius: 5px; z-index: 9999; pointer-events: none; font-family: sans-serif; font-weight: bold;">
        U: 0 | ORH: 0 | Occ: 0
    </div>
    '''

    btn_s = "cursor:pointer; border:none; background:rgba(0,0,0,0.08); color:#25282b; font-weight:bold; width:24px; min-width:24px; max-width:24px; height:24px; min-height:24px; max-height:24px; border-radius:4px; flex-shrink:0; display:inline-flex; align-items:center; justify-content:center;"
    
    nombres_prec = ["CHALCO", "COYOACÁN", "IZTAPALAPA", "MILPA ALTA", "TLAHUAC", "TLALPAN NORTE", "TLALPAN SUR", "XOCHIMILCO"]
    nombres_smx2 = ["CHALCO", "CHIMAS", "IXTAPALUCA VALLE CHALCO", "IZTAPALAPA 1", "IZTAPALAPA 2", "LA PAZ", "PUEBLOS", "TEXCOCO"]
    nombres_c1 = ["ESCÁRCEGA", "CAMPECHE", "ESCÁRCEGA EXT", "MAXCANUN", "CANDELARIA", "SEYBAPLAYA", "CHAMPOTÓN", "HOLPECHEN"]  
   
    es_c1 = (data_target == u_C1 or data_target == u_C1_SJA1)
    es_sde = (data_target == u_SDE)
    es_prec = (data_target == u_PREC)

    div_flex = "display: flex; align-items: center; justify-content: space-between; padding: 2px 4px; width: 100%; min-width: 100%; max-width: 100%; box-sizing: border-box;"
    span_num_u = "font-weight: bold; display: inline-block; text-align: center; width: 28px; min-width: 28px; max-width: 28px; flex-shrink: 0;"
    span_num_spr = "font-weight: bold; display: inline-block; text-align: center; width: 38px; min-width: 38px; max-width: 43px; flex-shrink: 0;"
    select_style = "width:160px; max-width: 160px; border:none; background:transparent; font-weight:600; font-size:14px; color:#25282b; padding: 4px; cursor: pointer;"

    fila_inner = f'''
    <tr class="calc-row">
        <td class="u-manual-cell" style="background: #fff8b8; border: 0.6px solid #25282b; padding: 2px; width: 105px; min-width: 105px; max-width: 105px;">
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
    <span class="v-total-val" contenteditable="true" oninput="recalc()" style="display:inline-block; min-width:55px; padding:2px 8px; border:none; border-radius:4px; background:#ededed; font-size:22px; font-weight:bold; color:#808080; text-align:center;">
        0
    </span>
</div>
'''
    
    campo_volumen_c1 = '''
<div style="text-align:center;">
    <span class="v-total-val" contenteditable="true" oninput="recalc()" style="display:inline-block; min-width:55px; padding:2px 8px; border:none; border-radius:4px; background:#ededed; font-size:22px; font-weight:bold; color:#808080; text-align:center;">
        0
    </span>
</div>
'''

    campo_campeche = '''
<div style="text-align:center;">
    <span class="v-total-val" contenteditable="true" oninput="recalc()" style="display:inline-block; min-width:55px; padding:2px 8px; border:none; border-radius:4px; background:#ededed; font-size:22px; font-weight:bold; color:#808080; text-align:center;">
        0
    </span>
</div>

<hr style="margin:4px 0; border:none; border-top:2px solid #999;">

<div style="font-size:13px;font-weight:bold;color:#25282b;">
    Nodos:
    <span class="nodos-campeche" contenteditable="true" style="display:inline-block; min-width:28px; text-align:center; border:none; border-radius:4px; background:#ededed; font-size:16px; font-weight:bold; color:#FF6347; padding:0 4px; margin-left:3px;">
        0
    </span>
</div>
'''

    limite_tablas = 21 if data_target == u_C1_SJA1 else 11
    
    for i in range(1, limite_tablas):

        if data_target == u_PREC and (i-1) < len(nombres_prec):
            nombre_final = nombres_prec[i-1]
        elif data_target == u_PREC_SMX2 and (i-1) < len(nombres_smx2):
             nombre_final = nombres_smx2[i-1]
        elif data_target == u_C1 and (i-1) < len(NOMBRES_PLANES_C1):
            nombre_final = NOMBRES_PLANES_C1[i-1]
        elif data_target == u_C1_SJA1 and (i-1) < len(NOMBRES_PLANES_C1_SJA1):
            nombre_final = NOMBRES_PLANES_C1_SJA1[i-1]
        else:
            nombre_final = f"PLAN {i}"

        if nombre_final == "CAMPECHE":
             contenido_volumen = campo_campeche
        elif es_c1:
             contenido_volumen = campo_volumen_c1
        else:
             contenido_volumen = campo_volumen_normal

        if es_sde:
             rowspan_actual = 5
        elif es_prec:
             rowspan_actual = 4
        elif data_target == u_C1_SJA1:
             rowspan_actual = 5  
        else:
             rowspan_actual = 3

        if es_sde:
            filas_extra = f"{fila_inner}{fila_inner}{fila_inner}{fila_inner}"
        elif es_prec:
            filas_extra = f"{fila_inner}{fila_inner}{fila_inner}"
        elif data_target == u_C1_SJA1:
            filas_extra = f"{fila_inner}{fila_inner}{fila_inner}{fila_inner}" 
        else:
            filas_extra = f"{fila_inner}{fila_inner}"

        polys += f'''
        <div class="poligono-bloque" style="margin-bottom:12px; box-shadow: none; border-radius: 0px; overflow: hidden; background: #ededed; border: 1.5px solid #25282b;">           
            <table style="width: 100%; border-collapse: collapse; border: 1.5px solid #25282b;">
                <thead>
                    <tr style="background: #25282b; color: white; font-size: 12px; height: 28px;">                        
                        <th style="padding: 0 10px; border-right: 1px solid #25282b;">PLAN</th>
                        <th style="border-right: 1px solid #25282b; width: 85px;">VOL. TOTAL</th>
                        <th style="width: 105px; min-width: 105px; max-width: 105px; border-right: 1px solid #25282b;"># USADAS</th>
                        <th style="width: 105px; min-width: 105px; max-width: 105px; border-right: 1px solid #25282b;">SPR</th>
                        <th style="width: 80px, border-right: 1px solid #25282b;">TIPO DE UNIDAD</th>
                        <th style="width: 45px; min-width: 45px; max-width: 45px; text-align: center;">OK</th> 
                    </tr>
                </thead>
                <tbody>
                    <tr class="calc-row"> 
                        <td rowspan="{rowspan_actual}" contenteditable="true" style="background: #dcdcdc; font-weight:bold; text-align:center; border: 1px solid #25282b; padding: 5px; color:#141414;">{nombre_final}</td>
                        <td rowspan="{rowspan_actual}" style="color:#808080; font-weight:bold; text-align:center; border:1px solid #25282b; padding:5px;">
                            {contenido_volumen}
                        </td>
                        <td class="u-manual-cell" style="background: #fff8b8; border: 0.5px solid #25282b; padding: 2px; width: 105px; min-width: 105px; max-width: 105px;">
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
        tr.master-row:hover, tr.calc-row:hover {{
            background-color: #ffffff !important;
            box-shadow: inset 0 0 10px rgba(0,0,0,0.05);
            cursor: default;
        }}

        #mi-contador {{
            position: fixed;
            top: 10px; 
            right: 220px; 
            background: #000; 
            color: #fff; 
            padding: 10px; 
            border-radius: 5px; 
            z-index: 9999; 
            pointer-events: none; 
            font-family: sans-serif;
            font-size: 12px;
        }}

        .poligono-bloque button {{
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            transition: all 0.1s;
        }}

        .poligono-bloque button:active {{
            box-shadow: 0 0px 0px transparent;
            transform: translateY(1px); 
        }}

        .filter-btn:active {{
            transform: translateY(4px);
            box-shadow: none !important;
        }}  

        tr.fila-ok {{
            background-color: #e8f5e9 !important;
            transition: background-color 0.3s ease;
        }}
        tr.fila-ok td {{
            color: #1b5e20 !important;
        }}
        
        body {{ font-family: sans-serif; background: #ffffff; padding: 14px; }}
        #visor {{
            margin-right: 250px !important;
        }}

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

        .meli-table th:last-child {{
            border-right: 2 !important;
        }}

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

        .master-row {{ 
            border-radius: 9px;
            box-shadow: 1px 1px 5px #ededed, -2px -2px 6px #efefef;
            transition: all 0.2s ease;
        }}

        .meli-table td:first-child {{ border-radius: 3px 0 0 3px; }}
        .meli-table td:last-child {{ border-radius: 0 3px 3px 0; }}

        #google-alert {{ 
            position: fixed;
            top: -100px; left: 50%; transform: translateX(-50%);
            background: #d32f2f; color: white; padding: 15px 25px; border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            transition: 0.4s; z-index: 10000;
        }}
        #google-alert.show {{ top: 20px; }}

        .tab-btn {{ 
            padding: 10px 12px; 
            cursor: pointer; 
            border: 1px solid #25282b;
            background: linear-gradient(180deg, #f0f0f0 0%, #dcdcdc 100%); 
            border-radius: 8px 8px 0 0;
            font-weight: bold; 
            font-size: 13px;
            color: #25282b;
            transition: all 0.2s ease;
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.8), 0 2px 4px rgba(0,0,0,0.1);
            margin-right: 2px;
            outline: none;
        }}

        .tab-btn:hover {{ 
            background: linear-gradient(180deg, #ffffff 0%, #f8fbff 100%);
            color: #25282b;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            transform: translateY(-2px); 
        }}

        .tab-btn.active {{
            background: linear-gradient(180deg, #0a2e42 0%, #25282b 100%) !important;
            color: #ffffff !important; 
            border: 1px solid #061821 !important;
            box-shadow: inset 0 2px 5px rgba(0,0,0,0.3);
            transform: translateY(0);
        }}        
        .tab-btn.active {{ background: #333; color: white; }}
        
        .tools-panel {{ display: flex; flex-direction: column; gap: 10px; margin-top: 15px; }}
        .google-tool {{ background: linear-gradient(145deg, #ffffff, #DDA0DD); padding: 15px; border-radius: 15px; border: 1px solid #25282b; text-align: center; box-shadow: 5px 5px 15px #d1d1d1, -5px -5px 15px #ffffff; transition: transform 0.2s;}}
        .google-tool:hover {{ transform: translateY(-3px); }}
        .google-tool input {{ border-radius: 8px; border: 1px solid #25282b; padding: 5px; font-size: 16px; outline: none; box-shadow: inset 2px 2px 5px #d9dbde; }}

        #calc_wrapper {{ background: #22c5bc; border-radius: 20px; padding: 15px; border: transparent; outline: none; transition: 0.3s; }}
        #calc_wrapper:focus {{ box-shadow: 0 0 20px #FF00FF, 0 0 40px #FF00FF; border: 2px solid #FF00FF; }}
        
        #calc_display_box {{ background: #fffacd; border-radius: 10px; padding: 10px; text-align: right; margin-bottom: 10px; min-height: 60px; }}
        .calc-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 5px; }}
        .btn-c {{ background: white; border: none; font-weight: bold; border-radius: 8px; padding: 12px; cursor: pointer; box-shadow: 0 3px #ccc; font-size: 14px; }}
        .btn-c-eq {{ background: #FF00FF; color: white; border: none; border-radius: 8px; cursor: pointer; font-weight: bold; font-size: 14px; }}
        .crono-card {{ background: #1c1c1c; border-radius: 12px; padding: 15px; color: white; font-family: sans-serif; text-align: center; }}
        .btn-c {{ background: #f0f0f0; border: none; font-weight: bold; border-radius: 12px; padding: 12px; cursor: pointer; box-shadow: 3px 3px 6px #1da39b, -2px -2px 5px #27ebd2; transition: transform 0.1s; }}
        .btn-c:active {{ transform: scale(0.95); box-shadow: inset 2px 2px 5px #b1b1b1; }}

        html body .meli-table tbody tr:last-child td {{
            height: 25px !important;
            min-height: 25px !important;
            max-height: 20px !important;
            padding-top: 2px !important;
            padding-bottom: 3px !important;
            line-height: 25px !important;
            font-size: 14px !important;
        }}

        html body .meli-table tbody tr:last-child {{ height: 16px !important; }}

        .btn-start {{ background: #28a745; color: white; box-shadow: 0 5px 0 #1e7e34; }}
        .btn-stop  {{ background: #ffc107; color: #333;  box-shadow: 0 5px 0 #d39e00; }}
        .btn-reset {{ background: #dc3545; color: white; box-shadow: 0 5px 0 #bd2130; }}

        .crono-card button:active {{ transform: translateY(4px); box-shadow: 0 1px 0 #333; }}
        .crono-card button:hover {{ filter: brightness(1.1); }}

        #body-plan-container th, .meli-table:nth-of-type(2) th {{ font-size: 22px !important; height: 90px !important; padding: 11px 6px !important; vertical-align: middle !important; }}

        body.excel-view #fleet-float, body.excel-view #ruteo-float, body.excel-view .tools-panel, body.excel-view #btn-excel-view {{ display: none !important; }}
        body.excel-view .meli-table td, body.excel-view .meli-table th {{ padding: 2px 3px !important; font-size: 12px !important; }}

        body.excel-view .poligono-bloque table {{ border-collapse: collapse !important; width: 120% !important; table-layout: fixed !important; }}
        body.excel-view .poligono-bloque td, body.excel-view .poligono-bloque th {{ padding: 8px 3px !important; height: 60px !important; font-size: 13px !important; overflow: hidden !important; white-space: nowrap !important; text-overflow: ellipsis !important; text-align: center !important; vertical-align: middle !important; }}

        body.excel-view .poligono-bloque th:nth-child(5) {{ width: 60px !important; }} 
        body.excel-view .poligono-bloque th:nth-child(6) {{ width: 55px !important; }} 
        body.excel-view .poligono-bloque th:nth-child(7) {{ width: 45px !important; }} 
    </style> 
</head>

<body>
<div id="panel-prioridades" style="position: fixed; top: -600px; left: 0; width: 100%; height: 268px; background: #f7efeb; border-bottom: 3px solid #FF6347; box-shadow: 0 5px 15px rgba(0,0,0,0.3); z-index: 9999999; transition: top 0.4s ease; padding: 5px 20px 20px 20px; box-sizing: border-box; overflow-y: auto; font-family: Arial, sans-serif;">
    <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #696969; padding-bottom: 8px; margin-bottom: 12px;">
        <h3 style="margin: 0; color: #333; font-size: 16px; font-weight: bold;">Prioridades de asignación</h3>
    </div>

    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
        <div>
            <h4 style="margin: 0 0 10px 0; color: #FF6347; font-size: 14px; font-weight: bold;">Prioridades destrucción / SCP1 C1</h4>
            <ul style="padding-left: 20px; margin: 0; line-height: 1.4; font-size: 13px;">
                <li>🔴 Campeche ➤ Rental Large Van ➤ NODOS = Delivery Cell-Dedicada.</li>
                <li>🟢 Resto planes ➤ Large Van MLP (nodo=híbrida).</li>
            </ul>
        </div>
        <div>
            <h4 style="margin: 0 0 10px 0; color: #FF6347; font-size: 14px; font-weight: bold;">Prioridades SMX5</h4>
            <ul style="padding-left: 20px; margin: 0; line-height: 1.4; font-size: 13px;">
                <li>🟠 Todos los planes ➤ Car 8h/Car extra 8h E1 Tlalpan Nte, Sur y Xochi</li>
                <li>👉 Cercanía de SVC ➤ Coyoacán, Iztapalapa, Tláhuac, Tlalpan nte, Tlalpan sur, Xochi, Chalco y Milpa Alta</li>
            </ul>
        </div>
        <div>
            <h4 style="margin: 0 0 10px 0; color: #FF6347; font-size: 14px; font-weight: bold;">Prioridades SJA1 C1</h4>
            <ul style="padding-left: 20px; margin: 0; line-height: 1.4; font-size: 13px;">
                <li>🟢 Locales (Centros) ➤ Rentals, MLP y crowd.</li>
                <li>👉 Planes foráneos ➤ MLP (nodo=híbrida) ➡️ Solo Xico/Tuzamapa ➤ MLP y Crowd.</li>
                <li>👉 Cercanía de SVC ➤ 🟢Tuzamapa 🟢Xico 🟡Actopan 🟡Trapiche 🟠Naolinco 🟠Perote 🔴Misantla 🔴Tezuitlan 🔴Tlaltetela</li>
                <li>🔵 EJA1-SP ➤ Media milla-ruteo fake.</li>
                <li>🟣 Meganodo ➤ Truck 3.5 MLP.</li>
                <li>🟤 Alchichica ND ➤ Small Van-AM0.</li>
            </ul>
        </div>
    </div>
</div>

<button onclick="togglePrioridades()" style="position: fixed; top: 25px; right: 25px; z-index: 99999999; background: #FF6347; color: white; border: 1px solid #333; padding: 8px 12px; font-weight: bold; cursor: pointer; border-radius: 4px; box-shadow: 2px 2px 5px rgba(0,0,0,0.3);">
    🚦 Prioridades
</button>

<div id="google-alert">⚠️ <span id="alert-msg"></span> [ENTER para cerrar]</div>
<div style="display:flex; flex-direction:column; gap:20px; width:100%;">

<div style="width:100%; padding:0; margin-bottom:10px;">
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
        <div style="background: #edddea; padding: 8px; border-radius: 5px; border: 1px solid #ffa8ff; text-align: center; width: 100px;">
            <div style="font-size: 10px; font-weight: bold; color: #d021eb;">RENTAL</div>
            <div id="val-rental-rute-2" style="font-size: 14px; font-weight: bold;">0</div>
        </div>
        <div style="background: #e4f5ce; padding: 8px; border-radius: 5px; border: 1px solid #c8e6c9; text-align: center; width: 100px;">
            <div style="font-size: 10px; font-weight: bold; color: #209626;">CAR</div>
            <div id="val-car-rute-2" style="font-size: 14px; font-weight: bold;">0</div>
        </div>
    </div>

<div id="dos-pct-global" style="background:#f5f5f5; border:1px solid #d0d0d0; border-radius:6px; padding:6px; margin-bottom:10px; text-align:center; font-weight:bold; color:#25282b;"></div>
        
        <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 5px;">
            <div>
                <button class="tab-btn active" onclick="showTab(2, this)">C1 SCP1</button>
                <button class="tab-btn" onclick="showTab(6, this)">C1 SJA1</button>
                <button class="tab-btn" onclick="showTab(1, this)">PREC SMX5</button>
                <button class="tab-btn" onclick="showTab(4, this)">SDE</button>
            </div> 

            <div style="padding-bottom: 5px; display: flex; gap: 6px; align-items: center;"> 
    <button onclick="distribuirAutomatico()" style="cursor:pointer; background: #FFD700; color: black; border: none; font-size: 12px; padding: 6px 12px; border-radius: 4px; font-weight: bold; box-shadow: 0 3px 0 #FFA500; transition: all 0.05s; outline: none;" onmousedown="this.style.transform='translateY(2px)'; this.style.boxShadow='0 1px 0 #FFA500';" onmouseup="this.style.transform='translateY(0px)'; this.style.boxShadow='0 3px 0 #FFA500';" onmouseleave="this.style.transform='translateY(0px)'; this.style.boxShadow='0 3px 0 #FFA500';">
        🧠 AUTO-CALCULAR
    </button>
    <button class="filter-btn" onclick="filterRows(true)" style="cursor:pointer; background: linear-gradient(180deg, #0f4563 0%, #25282b 100%); color: white; border: 1px solid #0a3045; font-size: 12px; padding: 6px 12px; border-radius: 4px; font-weight: bold; box-shadow: 0 3px 0 #0a3045; transition: all 0.05s; outline: none;">
        ACTIVAS
    </button>
    <button class="filter-btn" onclick="filterRows(false)" style="cursor:pointer; background: #808080; color:white; border:none; font-size:12px; padding:6px 12px; border-radius:4px; font-weight:bold; box-shadow: 0 3px 0 #454545; transition: all 0.05s; outline: none;">
        TODAS
    </button>
</div>

<button id="excel-btn" class="excel-only" onclick="toggleExcelView()" style="cursor:pointer; background:#228B22; color:white; border:none; font-size:12px; padding:6px 12px; border-radius:4px; font-weight:bold; box-shadow:0 3px 0 #1c6d1c; transition:all 0.05s; outline:none;">
    📸 VISTA EXCEL
</button>
</div>

     <div id="tab-2" class="t-content">
       <table class="meli-table" style="width: 100%; table-layout: fixed; border-collapse: collapse;">
        <thead>
            <tr style="background: linear-gradient(180deg, #0a2e42 0%, #25282b 100%); color: white;">
                <th style="border-right: 0.5px solid #25282b; padding: 4px 8px; font-size: 14px; color: #25282b !important;">UNIDAD</th>
                <th style="border-right: 0.5px solid #25282b; padding: 2px; font-size: 11px; color: #25282b !important; width: 45px;">ORH</th>
                <th style="border-right: 0.5px solid #25282b; padding: 2px; font-size: 11px; color: #25282b !important; width: 70px;">OCUPACIÓN</th>
                <th style="border-right: 0.5px solid #25282b; padding: 2px; font-size: 11px; color: #25282b !important; width: 45px;">SPR MIN</th>
                <th style="border-right: 0.5px solid #25282b; padding: 2px; font-size: 11px; color: #25282b !important; width: 45px;">SPR MAX</th>
                <th style="border-right:0.5px solid #25282b; padding:4px 8px; font-size:11px; color:#25282b !important; width:60px;">SCHEDULE</th>
                <th style="border-right:0.7px solid #25282b; padding:4px 9px; font-size:11px; color:#25282b !important; width:57px; text-align:center; display:table-cell; vertical-align:middle;">USADAS</th>
                <th style="border-right:0.5px solid #25282b; padding:4px 8px; font-size:11px; color:#25282b !important; width:50px;">DELTA</th>
            </tr>
        </thead>
        <tbody id="body-2">{gen_master_rows(u_C1, 2)}</tbody>
<tfoot class="fila-total">
    <tr class="fila-total">
        <td style="border:none;"></td>
        <td colspan="5" style="padding:6px; text-align:right;">TOTAL RUTEADAS</td>
        <td id="total-ruteadas-2" style="text-align:center; color:#FF0000; font-size:16px; font-weight:bold;">0</td>
    </tr>
</tfoot>
    </table>
</div>

<div id="tab-6" class="t-content" style="display:none;">
    <table class="meli-table" style="width: 100%; table-layout: fixed; border-collapse: collapse;">
        <thead>
            <tr style="background: linear-gradient(180deg, #0a2e42 0%, #25282b 100%); color: white;">
                <th style="border-right: 0.5px solid #25282b; padding: 4px 8px; font-size: 14px; color: #25282b !important;">UNIDAD</th>
                <th style="border-right: 0.5px solid #25282b; padding: 2px; font-size: 11px; color: #25282b !important; width: 45px;">ORH</th>
                <th style="border-right: 0.5px solid #25282b; padding: 2px; font-size: 11px; color: #25282b !important; width: 70px;">OCUPACIÓN</th>
                <th style="border-right: 0.5px solid #25282b; padding: 2px; font-size: 11px; color: #25282b !important; width: 45px;">SPR MIN</th>
                <th style="border-right: 0.5px solid #25282b; padding: 2px; font-size: 11px; color: #25282b !important; width: 45px;">SPR MAX</th>
                <th style="border-right:0.5px solid #25282b; padding:4px 8px; font-size:11px; color:#25282b !important; width:60px;">SCHEDULE</th>
                <th style="border-right:0.7px solid #25282b; padding:4px 9px; font-size:11px; color:#25282b !important; width:57px; text-align:center; display:table-cell; vertical-align:middle;">USADAS</th>
                <th style="border-right:0.5px solid #25282b; padding:4px 8px; font-size:11px; color:#25282b !important; width:50px;">DELTA</th>
            </tr>
        </thead>
        <tbody id="body-6">{gen_master_rows(u_C1_SJA1, 6)}</tbody>
        <tfoot class="fila-total"> 
    <tr class="fila-total">
        <td style="border:none;"></td>
        <td colspan="5" style="padding:6px; text-align:right;">TOTAL RUTEADAS</td>
        <td id="total-ruteadas-6" style="text-align:center; color:#FF0000; font-size:16px; font-weight:bold !important;">0</td>
    </tr>
</tfoot>
    </table>
</div>
       
        <div id="tab-1" class="t-content" style="display:none;">
            <table class="meli-table" style="width: 100%; table-layout: fixed; border-collapse: collapse;">
        <thead>
  <tr style="background: linear-gradient(180deg, #0a2e42 0%, #25282b 100%); color: white;">
    <th style="border-right: 0.5px solid #25282b; padding: 4px 8px; font-size: 14px; color: #25282b !important;">UNIDAD</th>
    <th style="border-right: 0.5px solid #25282b; padding: 2px; font-size: 11px; color: #25282b !important; width: 45px;">ORH</th>
    <th style="border-right: 0.5px solid #25282b; padding: 2px; font-size: 11px; color: #25282b !important; width: 70px;">OCUPACIÓN</th>
    <th style="border-right: 0.5px solid #25282b; padding: 2px; font-size: 11px; color: #25282b !important; width: 45px;">SPR MIN</th>
    <th style="border-right: 0.5px solid #25282b; padding: 2px; font-size: 11px; color: #25282b !important; width: 45px;">SPR MAX</th>
    <th style="border-right:0.5px solid #25282b; padding:4px 8px; font-size:11px; color: #25282b !important; width:60px;">SCHEDULE</th>
   <th style="border-right:0.7px solid #25282b; padding:4px 9px; font-size:11px; color:#25282b !important; width:57px; text-align:center; display:table-cell; vertical-align:middle;">USADAS</th>
    <th style="border-right:0.5px solid #25282b; padding:4px 8px; font-size:11px; color: #25282b !important; width:50px;">DELTA</th>
  </tr>
</thead>
        <tbody id="body-1">{gen_master_rows(u_PREC, 1)}</tbody>
          <tfoot class="fila-total">
<tr class="fila-total">
    <td style="border:none;"></td>
    <td colspan="5" style="padding:6px; text-align:right;">TOTAL CAR RUTEADAS</td>
    <td id="total-car-real-1" style="text-align:center; color:#FF0000; font-size:16px; font-weight:bold;">0</td>
</tr>
</tfoot>
    </table>
</div>
       
        <div id="tab-5" class="t-content" style="display:none;">
            <table class="meli-table" style="width: 100%; table-layout: fixed; border-collapse: collapse;">
        <thead>
            <tr style="background: linear-gradient(180deg, #0a2e42 0%, #25282b 100%); color: white;">
                <th style="border-right: 0.5px solid #25282b; padding: 4px 8px; font-size: 14px; color: #25282b !important;">UNIDAD</th>
                <th style="border-right: 0.5px solid #25282b; padding: 2px; font-size: 11px; color: #25282b !important; width: 45px;">SPR MIN</th>
                <th style="border-right: 0.5px solid #25282b; padding: 2px; font-size: 11px; color: #25282b !important; width: 45px;">SPR MAX</th>
                <th style="border-right:0.5px solid #25282b; padding:4px 8px; font-size:11px; color: #25282b !important; width:60px;">SCHEDULE</th>
                <th style="border-right:0.7px solid #25282b; padding:4px 9px; font-size:11px; color:#25282b !important; width:57px; text-align:center; display:table-cell; vertical-align:middle;">USADAS</th>
                <th style="border-right:0.5px solid #25282b; padding:4px 8px; font-size:11px; color: #25282b !important; width:50px;">DELTA</th>
            </tr>
        </thead>
        <tbody id="body-5">{gen_master_rows(u_PREC_SMX2, 5)}</tbody>
         <tfoot class="fila-total">
<tr class="fila-total">
    <td style="border:none;"></td>
    <td colspan="3" style="padding:6px; text-align:right;">TOTAL RUTEADAS</td>
    <td id="total-ruteadas-5" style="text-align:center; color:#FF0000; font-size:16px; font-weight:bold;">0</td>
</tr>
</tfoot>
    </table>
</div>

        <div id="tab-4" class="t-content" style="display:none;">
            <table class="meli-table" style="width: 100%; table-layout: fixed; border-collapse: collapse;">
        <thead>
            <tr style="background: linear-gradient(180deg, #0a2e42 0%, #25282b 100%); color: white;">
                <th style="border-right: 0.5px solid #25282b; padding: 4px 8px; font-size: 14px; color: #25282b !important;">UNIDAD</th>
                <th style="border-right: 0.5px solid #25282b; padding: 2px; font-size: 11px; color: #25282b !important; width: 45px;">SPR MIN</th>
                <th style="border-right: 0.5px solid #25282b; padding: 2px; font-size: 11px; color: #25282b !important; width: 45px;">SPR MAX</th>
                <th style="border-right:0.5px solid #25282b; padding:4px 8px; font-size:11px; color: #25282b !important; width:60px;">SCHEDULE</th>
                <th style="border-right:0.7px solid #25282b; padding:4px 9px; font-size:11px; color:#25282b !important; width:57px; text-align:center; display:table-cell; vertical-align:middle;">USADAS</th>
                <th style="border-right:0.5px solid #25282b; padding:4px 8px; font-size:11px; color: #25282b !important; width:50px;">DELTA</th>
            </tr>
        </thead>
        <tbody id="body-4">{gen_master_rows(u_SDE, 4)}</tbody>
       <tfoot class="fila-total">
<tr class="fila-total">
    <td style="border:none;"></td>
    <td colspan="3" style="padding:6px; text-align:right;">TOTAL CAR RUTEADAS</td>
    <td id="total-car-real-4" style="text-align:center; color:#FF4500; font-size:16px; font-weight:bold;">0</td>
</tr>
</tfoot>
    </table>
</div>
</div>

        <div class="tools-panel">
            <div class="google-tool" style="border: none !important; box-shadow: none !important; background: transparent; border-radius: 7px; ">
                <button id="toggle-tools-btn" onclick="toggleTools()" style="cursor:pointer; background:#25282b !important; background-image: none !important; box-shadow: none !important; color: #ffffff !important; border: 1px solid #4682B4; font-size: 11px; padding: 5px 0; border-radius: 3px; font-weight: bold; outline: none; width: 100%; margin-bottom: 15px;">
                    ❌ OCULTAR UTILERÍAS
                </button>
                <div style="font-weight:bold; color:#25282b; margin-bottom:10px; font-size:12px; letter-spacing:1px;">⏱️ CONVERTIDOR DE TIEMPO</div>
                <input type="number" id="min-in" placeholder="Minutos" style="width:80px; text-align:center;" oninput="convertTime()">
                <div style="margin-top:10px;">
                    <span id="time-res" style="font-size: 24px; font-weight: bold; color: #FF4500;">0h 0m</span>
                 </div>
             </div>
        </div>
    </div>
</div>

<div style="width:100%; overflow-y:auto; overflow-x:hidden;">
    <div style="background: #25282b !important; background-image: none !important; box-shadow: none !important; border: none !important; color: #f9d633; padding: 10px; border-radius: 6px; text-align: center; font-weight: bold; margin-bottom: 10px;">
        📋 PLANIFICACIÓN POR POLÍGONOS
    </div>
        
        <div id="polys-2" class="p-content">{gen_poligonos(u_C1)}</div>
        <div id="polys-6" class="p-content" style="display:none;">{gen_poligonos(u_C1_SJA1)}</div>
        <div id="polys-1" class="p-content" style="display:none;">{gen_poligonos(u_PREC)}</div>
        <div id="polys-5" class="p-content" style="display:none;">{gen_poligonos(u_PREC_SMX2)}</div>
        <div id="polys-4" class="p-content" style="display:none;">{gen_poligonos(u_SDE)}</div>

        <div id="excel-polys" style="display:none; margin-top:10px;">
    <div style="background:#25282b; color:white; font-weight:bold; text-align:center; padding:8px; font-size:18px; border:1px solid #0f5b84;">
        📋 RESUMEN DE POLÍGONOS
    </div>
    <table style="width:100%; border-collapse:collapse; background:white; font-size:12px; table-layout:fixed;">
        <thead>
<tr style="background:#25282b; color:white; height:28px;">
    <th style="border:1px solid #c0c0c0;">PLAN</th>
    <th style="border:1px solid #c0c0c0;">VOL</th>
    <th style="border:1px solid #c0c0c0;">UNIDAD</th>
    <th style="border:1px solid #c0c0c0;">ASIG</th>
    <th style="border:1px solid #c0c0c0;">ORH/OCUP</th>
    <th style="border:1px solid #c0c0c0;">NODO</th>
</tr>
</thead>
        <tbody id="excel-polys-body"></tbody>
    </table>
</div>
</div>

<div id="fleet-float" hidden>
    <div style="font-weight:bold; margin-bottom:8px;">🚛 DISPONIBLE</div>
    <div id="fleet-float-body">Cargando...</div>
</div>

<div id="mi-contador-flotante" style="position: fixed; bottom: 20px; right: 20px; background: rgba(0, 0, 0, 0.85); color: white; padding: 15px; border-radius: 8px; font-family: sans-serif; z-index: 9999; pointer-events: none; border: 1px solid #444;">
    Cargando datos...
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

    function aplicarPerfil() {{
    let perfil = perfiles[perfilActual];
    if(!perfil) return;
    Object.keys(perfil).forEach(tabId => {{
        document.querySelectorAll('#body-' + tabId + ' tr').forEach(row => {{
            let unidad = row.querySelector('.edit-name')?.innerText.trim(); 
            if(perfil[tabId][unidad]) {{
                let data = perfil[tabId][unidad];
                let orh = row.querySelector('.edit-orh');
                let disp = row.querySelector('.edit-ocup');
                if(orh) orh.innerText = data.orh;
                if(disp) disp.innerText = data.disp;
            }}
        }});
   }});
    recalc();
}}

function showTab(n, btn) {{
    document.body.classList.remove("excel-view");
    currentTab = n;
    document.querySelectorAll('.p-content, .t-content')
        .forEach(el => el.style.display = 'none');
    document.querySelectorAll('.tab-btn')
        .forEach(b => b.classList.remove('active'));

    document.getElementById('polys-' + n).style.display = 'block';
    document.getElementById('tab-' + n).style.display = 'block';

    btn.classList.add('active');

    recalc();
    actualizarVisibilidadContador();
    updateFleetFloat();

    const excelBtn = document.getElementById('excel-btn');
    if (excelBtn) {{
        excelBtn.style.display = (n === 2 || n === 6) ? 'inline-block' : 'none';
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
    
    if(sel === "Seleccionar..." || sel === "") return;
    let fRows = Array.from(document.querySelectorAll('#body-' + currentTab + ' tr'));
    let fRow = fRows.find(r => r.querySelector('.edit-name').innerText.trim() === sel);
    
    if (!fRow) return;

    let left = parseInt(fRow.querySelector('.f-left').innerText) || 0;
    let sprMaxReal = parseFloat(fRow.querySelector('.edit-spr-max').innerText) || 0;

    if(type === 'u') {{
        let span = row.querySelector('.u-manual');
        let val = parseInt(span.innerText) || 0;

        let nombreUpper = sel.toUpperCase();
        let esFlexible = nombreUpper.includes("CAR - 3H") || nombreUpper.includes("CAR - 5H") || nombreUpper.includes("CAR - 8H") || currentTab == 6;
        
        if (delta > 0 && left <= 0 && !esFlexible) {{
            showAlert("⚠️ NO PUEDES AGREGAR MÁS UNIDADES.");
            return;
        }}

        if (delta > 0 && left <= 0 && esFlexible && currentTab != 6) {{
            showAlert("⚠️ EXCESO DE UNIDADES CAR. Se registrará como negativo.");
        }}
        span.innerText = val + delta;
    }} else {{
        let span = row.querySelector('.spr-real-val');
        let val = parseFloat(span.innerText) || 0;
        let newVal = Math.round(val + delta);

        if (delta > 0 && newVal > sprMaxReal) {{
            showAlert("⚠️ NO PUEDES SOBREPASAR EL SPR MÁXIMO (" + sprMaxReal + ")");
            return; 
        }}
        span.innerText = newVal;
    }}
    editedRowsPlan.add(row);
    recalc();
}}

function actualizarDosPorciento() {{
    let volumenTotal = 0;
    document.querySelectorAll('#polys-' + currentTab + ' .v-total-val').forEach(el => {{
        volumenTotal += parseFloat(el.innerText) || 0;
    }});
    let permitido = Math.round(volumenTotal * 0.02);
    let div = document.getElementById('dos-pct-global');
    if (div) {{
        div.innerHTML = `<b>2% PERMITIDO:</b> \${{permitido.toLocaleString()}}`;
    }}
}}

    function recalc() {{
        let fleet = {{}};
        let tabId = currentTab;

        document.querySelectorAll('#body-' + tabId + ' tr').forEach(row => {{
    let nameCell = row.querySelector('.edit-name');
    let name = nameCell.innerText.trim();
    let sch = parseInt(row.querySelector('.f-stock').innerText) || 0;
    let mi = row.querySelector('.edit-spr-min'), ma = row.querySelector('.edit-spr-max'), fs = row.querySelector('.f-stock');
    
    if(sch > 0) {{
        row.style.background = "#FFFFFF"; 
        fs.style.background = "#fcf8cc"; 
        mi.style.background = "#edf7f7"; mi.style.color = "#25282b"; mi.style.fontWeight = "bold";
        ma.style.background = "#edf7f7"; ma.style.color = "#25282b"; ma.style.fontWeight = "bold";
        nameCell.style.color = "#25282b"; nameCell.style.fontWeight = "bold";
    }} else {{
        row.style.background = "#DCDCDC";
        fs.style.background = "#FFFF00"; 
        mi.style.background = "#dcdcdc"; mi.style.color = "#969696"; mi.style.fontWeight = "normal";
        ma.style.background = "#dcdcdc"; ma.style.color = "#969696"; ma.style.fontWeight = "normal";
        nameCell.style.color = "#969696"; nameCell.style.fontWeight = "normal";
    }}
    
    if(name !== "" && name !== "NUEVA UNIDAD") {{
        fleet[name] = {{ max: parseFloat(ma.innerText)||0, stock: sch, used: 0 }};
    }}
}});

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

document.querySelectorAll('#polys-' + tabId + ' .poligono-bloque').forEach(bl => {{
    let vT = parseFloat(bl.querySelector('.v-total-val').innerText) || 0, vA = 0;
    let vCalcEl = bl.querySelector('.v-calculado-total');
    let filas = bl.querySelectorAll('.calc-row');

    filas.forEach((r, index) => {{
        let sType = r.querySelector('.s-type');
        let uManual = r.querySelector('.u-manual');
        let sp = r.querySelector('.spr-real-val');
        
        if (sType.value === "" || sType.value === "Seleccionar...") {{
            uManual.innerText = "0";
        }}
        
        let s = sType.value;
        let u = parseInt(uManual.innerText) || 0;

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

    vCalcEl.innerText = Math.round(vA);
    let d = bl.querySelector('.p-diff');
    if (vT === 0) d.innerText = "VACÍO";
    else if (Math.round(vA) === Math.round(vT)) {{ d.innerText = "OK"; d.style.background = "#61b888"; }}
    else if (vA > vT) {{ d.innerText = "EXCESO: " + Math.round(vA - vT); d.style.background = "#f2bd5c"; }}
    else {{ d.innerText = "FALTAN: " + Math.round(vT - vA); d.style.background = "#fc9a88"; }}
}});

document.querySelectorAll('#body-' + tabId + ' tr').forEach(row => {{
    let nameCell = row.querySelector('.edit-name');
    if (!nameCell) return;
    
    let n = nameCell.innerText.trim();
    let ruteadasManuales = parseFloat(row.querySelector('.f-ruteadas')?.innerText || 0);
    let stock = parseFloat(row.querySelector('.f-stock')?.innerText || 0);
    let cL = row.querySelector('.f-left'); 
    
    let ruteadaCell = row.querySelector('.f-ruteadas');
    if (ruteadaCell) {{
        if (ruteadasManuales > 0) {{
            ruteadaCell.style.backgroundColor = "#ffffff"; 
            ruteadaCell.style.color = "#2E8B57";           
            ruteadaCell.style.fontWeight = "bold";
        }} else {{
            ruteadaCell.style.backgroundColor = "#dcdcdc";
            ruteadaCell.style.color = "";
            ruteadaCell.style.fontWeight = "bold";         
        }}
    }}
    
    if (cL) {{
        let diff = stock - ruteadasManuales;
        cL.innerText = diff;
        
        if (diff < 0) {{
            cL.style.color = "red";
            cL.style.fontWeight = "bold"; 
            cL.style.background = "transparent";
        }} else if (diff === 0 && stock > 0) {{
            cL.style.color = "white";
            cL.style.background = "#f05d5d";
        }} else {{
            cL.style.color = "#0e4c6e";
            cL.style.background = "transparent"; 
            cL.style.fontWeight = "normal";
        }}
    }}
}});

document.querySelectorAll('#polys-' + tabId + ' .poligono-bloque').forEach(bl => {{
            const listaNegativos = ["Car - 8h", "Car - 5h", "Car - 3h", "Car 8h"];

            bl.querySelectorAll('.s-type').forEach(s => {{
                let cur = s.value; 
                let opt = '<option value="">Seleccionar...</option>';
             
                Object.keys(fleet).forEach(k => {{
                    let nameLower = k.toLowerCase();
                    let stock = fleet[k].stock;
                    let used = fleet[k].used;
          
                    let esFlexible = listaNegativos.some(u => nameLower.includes(u.toLowerCase())) || tabId == 6;
                    let tieneStockInicial = (stock > 0); 
                    let tieneCapacidad = (stock - used > 0);
            
                    if (tieneStockInicial && (tieneCapacidad || esFlexible || k === cur)) {{
                        opt += `<option value="\${{k}}">\${{k}}</option>`;
                    }}
                }});
                
                s.innerHTML = opt;
                s.value = cur;
                updateSelectColor(s);
            }});
        }});

let totals = {{
    mlpDecl: 0, mlpRute: 0,
    rentalDecl: 0, rentalRute: 0,
    carDecl: 0, carRute: 0,
    otrosRute: 0,
    totalRuteadas: 0
}};

document.querySelectorAll('#body-' + tabId + ' tr').forEach(row => {{
    let name = row.querySelector('.edit-name')?.innerText.toLowerCase().trim() || "";
    let sch = parseInt(row.querySelector('.f-stock')?.innerText) || 0;
    
    if (name.includes("mlp")) totals.mlpDecl += sch;
    else if (name.includes("rental")) totals.rentalDecl += sch;
    else if (name.includes("car") || name.includes("moto") || name.includes("van")) totals.carDecl += sch;
}});

totals.totalRuteadas = 0; 
totals.mlpRute = 0;
totals.rentalRute = 0;
totals.carRute = 0;
totals.otrosRute = 0; 

document.querySelectorAll('#polys-' + tabId + ' .calc-row').forEach(row => {{
    let s = row.querySelector('.s-type').value; 
    let u = parseInt(row.querySelector('.u-manual').innerText) || 0;

    if (!s || s === "Seleccionar...") return;

    let name = s.toLowerCase().trim();

    if (name.includes("mlp")) {{
        totals.mlpRute += u;
    }} else if (name.includes("rental")) {{
        totals.rentalRute += u;
    }} else if (name.includes("delivery")) {{
        totals.otrosRute += u;
    }} else if (name.includes("car") || name.includes("moto") || name.includes("van")) {{
        totals.carRute += u;
    }} else {{
        totals.otrosRute += u; 
    }}
    totals.totalRuteadas = totals.mlpRute + totals.rentalRute + totals.carRute + totals.otrosRute;
}});

totals.totalRuteadas = totals.mlpRute + totals.rentalRute + totals.carRute + totals.otrosRute;

function setT(id, val) {{
    let finalId = id + '-' + tabId;
    let el = document.getElementById(finalId);
    if (el) {{ el.innerText = Math.round(val); }}
}}

totals.totalRuteadas = totals.mlpRute + totals.rentalRute + totals.carRute + totals.otrosRute;

setT('total-mlp-decl', totals.mlpDecl);
setT('total-mlp-rute', totals.mlpRute);
setT('total-rental-decl', totals.rentalDecl);
setT('total-rental-rute', totals.rentalRute);
setT('total-car-schedule', totals.carDecl);
setT('total-car-real', totals.carRute);
setT('total-otros', totals.otrosRute);

setTimeout(() => {{
    let valorCorrecto = totals.mlpRute + totals.rentalRute + totals.carRute + totals.otrosRute;
    let el = document.getElementById('total-ruteadas-' + tabId);
    if (el) {{
        el.innerText = Math.round(valorCorrecto);
        el.style.color = "#FF8C00"; 
    }}
}}, 500);

updateFleetFloat();
actualizarDosPorciento();

    let elMlp = document.getElementById('val-mlp-rute-' + tabId);
    let elRental = document.getElementById('val-rental-rute-' + tabId);
    let elCar = document.getElementById('val-car-rute-' + tabId);
    if(elMlp) elMlp.innerText = Math.round(totals.mlpRute);
    if(elRental) elRental.innerText = Math.round(totals.rentalRute);
    if(elCar) elCar.innerText = Math.round(totals.carRute);
    }}

document.addEventListener('keydown', function(event) {{
    if (event.key === 'Enter') {{
        let panel = document.getElementById('panel-prioridades');
        if (panel && panel.style.top === "0px") {{
            panel.style.top = "-600px"; 
            document.activeElement.blur();
        }}
        let alerta = document.querySelector('.alerta-roja, .p-diff'); 
        if (alerta && alerta.innerText.includes('EXCESO')) {{
            document.activeElement.blur();
        }}
    }}
}});

function focusCalc() {{ document.getElementById('calc_wrapper').focus(); }}

    function filterRows(onlyActive) {{
        const rows = document.querySelectorAll('#body-' + currentTab + ' .master-row');
        rows.forEach(row => {{
            const stock = parseInt(row.querySelector('.f-stock').innerText) || 0;
            row.style.display = (onlyActive && stock === 0) ? 'none' : '';
        }});
        document.querySelectorAll('#polys-' + currentTab + ' .poligono-bloque').forEach(bl => {{
            let filasVisiblesEnBloque = 0;
            let vTotal = parseFloat(bl.querySelector('.v-total-val').innerText) || 0;

            bl.querySelectorAll('tbody tr.calc-row').forEach(r => {{
                let uManual = parseInt(r.querySelector('.u-manual').innerText) || 0;
                let sTypeSelect = r.querySelector('.s-type');
                let sType = sTypeSelect ? sTypeSelect.value : "Seleccionar..."; 

                if (onlyActive) {{
                    if (uManual === 0 && (sType === "Seleccionar..." || sType === "")) {{
                        r.style.display = 'none';
                    }} else {{
                        r.style.display = '';
                        filasVisiblesEnBloque++;
                    }}
                }} else {{
                    r.style.display = '';
                    filasVisiblesEnBloque++;
                }}
            }});
            let filaEstado = bl.querySelector('tbody tr:not(.calc-row)');
            if (filaEstado) {{
                filaEstado.style.display = onlyActive ? 'none' : '';
            }}

            let nuevoRowspan = Math.max(1, filasVisiblesEnBloque);
            let celdaPlan = bl.querySelector('tbody tr.calc-row td[rowspan]');
            let celdaVolumen = bl.querySelector('tbody tr.calc-row .v-total-val');
            if (celdaPlan) {{ 
                celdaPlan.rowSpan = nuevoRowspan;
                celdaPlan.setAttribute('rowspan', nuevoRowspan);
            }}
            if (celdaVolumen) {{ 
                celdaVolumen.rowSpan = nuevoRowspan;
                celdaVolumen.setAttribute('rowspan', nuevoRowspan);
            }}

            if (onlyActive) {{
                if (vTotal === 0 && filasVisiblesEnBloque === 0) {{
                    bl.style.display = 'none';
                }} else {{
                    bl.style.display = '';
                }}
            }} else {{
                bl.style.display = '';
            }}
        }});
    }}

    let herramientasVisibles = true;
function toggleTools() {{
    const crono = document.querySelector('.crono-card');
    const convertidorContenido = document.querySelectorAll('.google-tool > *:not(#toggle-tools-btn)');
    const boton = document.getElementById('toggle-tools-btn');
    herramientasVisibles = !herramientasVisibles;

    if (crono) {{ crono.style.display = herramientasVisibles ? '' : 'none'; }}
    convertidorContenido.forEach(elemento => {{ elemento.style.display = herramientasVisibles ? '' : 'none'; }});
    if (!herramientasVisibles) {{
        boton.innerHTML = '🛠️ MOSTRAR UTILERÍAS';
        boton.className = 'btn-mostrar'; 
    }} else {{
        boton.innerHTML = '❌ OCULTAR UTILERÍAS';
        boton.className = 'btn-ocultar'; 
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
        document.getElementById('crono-main').innerText = `\${{h}}:\${{m}}:\${{s}}.\${{ms}}`;
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

            let activeTabBtn = document.querySelector('.tab-btn.active');
            if (activeTabBtn) {{
                let tabId = activeTabBtn.textContent.trim();
                if (tabId === "C1 SCP1" && unidadSeleccionada.trim() === "Large Van MLP") {{
                    permiteInfinito = true;
                }} 
                else if ((tabId === "SDE" || tabId === "PREC" || tabId === "C1 SJA1") && (esUnidadCar || tabId === "C1 SJA1")) {{
                    permiteInfinito = true;
                }}
            }}

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
        recalc();
    }}

 function resetRow(sel) {{ 
        let r = sel.closest('tr');
        if (!r) return;
        let table = sel.closest('table');
        if (!table) return;

        let tbody = table.querySelector('tbody');
        let unidadSeleccionada = sel.value;
        if (unidadSeleccionada === "") {{
            r.querySelector('.u-manual').innerText = "0";
            r.querySelector('.spr-real-val').innerText = "0";
            editedRowsPlan.delete(r);
            recalc();
            return;
        }}

        let volTotalSpan = table.querySelector('.v-total-val');
        let volumenTotal = volTotalSpan ? parseFloat(volTotalSpan.textContent) || 0 : 0;
        let sprEncontrado = 0;
        let filasFlota = document.querySelectorAll('.master-row');
        for (let filaFlota of filasFlota) {{
            let celdaNombre = filaFlota.querySelector('.edit-name');
            if (celdaNombre && celdaNombre.innerText.trim() === unidadSeleccionada.trim()) {{
                let celdaSprMax = filaFlota.querySelector('.edit-spr-max');
                if (celdaSprMax) {{
                    sprEncontrado = parseFloat(celdaSprMax.innerText) || 0;
                }}
                break;
            }}
        }}

        let spanS = r.querySelector('.spr-real-val');
        if (spanS) {{ spanS.innerText = sprEncontrado; }}

        let unidadesCalculadas = 1;
        if (unidadSeleccionada.trim() === "Delivery Cell Large Van") {{
            unidadesCalculadas = 1;
        }} else if (volumenTotal > 0 && sprEncontrado > 0) {{
            unidadesCalculadas = Math.ceil(volumenTotal / sprEncontrado);
        }}

        let spanU = r.querySelector('.u-manual');
        if (spanU) {{ spanU.innerText = unidadesCalculadas; }}

        let permiteInfinito = false;
        let esUnidadCar = unidadSeleccionada.toLowerCase().includes("car");

        let activeTabBtn = document.querySelector('.tab-btn.active');
        if (activeTabBtn) {{
            let tabId = activeTabBtn.textContent.trim();
            if (tabId === "C1 SCP1" && unidadSeleccionada.trim() === "Large Van MLP") {{
                permiteInfinito = true;
            }} 
            else if ((tabId === "SDE" || tabId === "PREC" || tabId === "C1 SJA1") && (esUnidadCar || tabId === "C1 SJA1")) {{
                permiteInfinito = true;
            }}
        }}

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

        if (typeof manualEdit === 'function' && spanU) {{
            manualEdit(spanU);
        }} else {{
            recalc();
        }}
    }}
    
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

function toggleExcelView() {{
    const isExcel = !document.body.classList.contains("excel-view");
    document.body.classList.toggle("excel-view", isExcel);
    
    let btn = document.getElementById("excel-btn");
    let excel = document.getElementById("excel-polys");
    const idsAocultar = [
        "total-no-car-2", "total-car-schedule-2", "total-car-real-2",
        "total-no-car-6", "total-car-schedule-6", "total-car-real-6",
        "total-no-car-1", "total-car-schedule-1", "total-car-real-1",
        "total-no-car-5", "total-car-schedule-5", "total-car-real-5"
    ];
    if (isExcel) {{
        generarExcelPolys();
        btn.innerHTML = "🔙 VISTA NORMAL";
        if(excel) excel.style.display = "block";
        
        ["polys-1", "polys-2", "polys-4", "polys-5", "polys-6"].forEach(id => {{
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
        btn.innerHTML = "📸 VISTA EXCEL";
        if(excel) excel.style.display = "none";
        
        ["polys-1", "polys-2", "polys-4", "polys-5", "polys-6"].forEach(id => {{
            let el = document.getElementById(id);
            if(el) el.style.display = (id === "polys-" + currentTab) ? "block" : "none";
        }});
        idsAocultar.forEach(id => {{
            let el = document.getElementById(id);
            if(el) {{
                let fila = el.closest('tr');
                if(fila) fila.style.removeProperty('display');
            }}
        }});
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
        let nodoTxt = "-";

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
            if (fRow) {{
                let sMin = fRows[fRows.indexOf(fRow)].querySelectorAll('td')[1]?.innerText.trim() || "0";
                let sMax = fRows[fRows.indexOf(fRow)].querySelectorAll('td')[2]?.innerText.trim() || "0";
                valSpr = sMin + " / " + sMax;
            }}

            let filaHtml = '<tr>';
            if (index === 0) {{
                filaHtml += `
                    <td rowspan="\${{filasValidas.length}}" style="border:1px solid #808080; padding:3px; text-align:center; font-weight:bold; vertical-align:middle;">\${{plan}}</td>
                    <td rowspan="\${{filasValidas.length}}" style="border:1px solid #808080; text-align:center; font-weight:bold; vertical-align:middle;">\${{vol}}</td>
                `;
            }}
            filaHtml += `
                <td style="border:1px solid #808080; padding-left:6px; vertical-align:middle;">\${{unidad}}</td>
                <td style="border:1px solid #808080; text-align:center; vertical-align:middle;">\${{asignadas}}</td>
                <td style="border:1px solid #808080; text-align:center; vertical-align:middle;">\${{valSpr}}</td>
            `;
            if (index === 0) {{
                filaHtml += `<td rowspan="\${{filasValidas.length}}" style="border:1px solid #808080; text-align:center; font-weight:bold; vertical-align:middle;">\${{nodoTxt}}</td>`;
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
    const opciones = ["Car - 8h", "Car - 5h", "Car - 3h"];
    for (let nombre of opciones) {{
        let unidad = fleet.find(f => f.nombre === nombre && f.stock > 0);
        if (unidad) {{ return unidad; }}
    }}
    return null;
}}

function distribuirAutomatico() {{
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

    fleet.sort((a, b) => b.spr - a.spr);
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

    if (currentTab == 5) {{
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

    if (currentTab == 2) {{
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

    if (currentTab == 6) {{
        polys.forEach(poly => {{
            procesarAsignacionUnidadSJA1(poly);
        }});
    }} else {{
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

                if (currentTab == 2 && nombrePlan == "CAMPECHE") {{
                    unidad = fleet.find(f => f.nombre === "Rental Large Van");
                }} else if (currentTab == 2) {{
                    unidad = fleet.find(f => f.restante > 0 && f.nombre !== "Rental Large Van");
                }} else {{
                    unidad = fleet.find(f => f.restante > 0);
                }}

                if (!block) {{
                    if (currentTab == 4) {{ 
                        let options = ["Car - 5h", "Car - 3h"];
                        for (let opt of options) {{
                            unidad = fleet.find(f => f.nombre.includes(opt));
                            if (unidad) break;
                        }}
                    }} else if (currentTab == 2) {{ 
                        let options = ["Large Van MLP", "Car - 8h", "Car - 5h"];
                        for (let opt of options) {{
                            unidad = fleet.find(f => f.nombre.includes(opt));
                            if (unidad) break;
                        }}
                    }} else if (currentTab == 1 || currentTab == 5) {{ 
                        let options = ["Car - 8h", "Car - 5h"];
                        for (let opt of options) {{
                            unidad = fleet.find(f => f.nombre.includes(opt));
                            if (unidad) break;
                        }}
                    }}
                    if (!unidad) break;
                }}

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

    recalc();
}}

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

            if (nombrePlan === "CENTRO 1" || nombrePlan === "CENTRO 2") {{
                const listaRental = ["Rental Electric Large Van", "Rental Large Van", "Rental Replacement"];
                for (let nombre of listaRental) {{
                    unidad = fleet.find(f => f.restante > 0 && f.nombre === nombre);
                    if (unidad) break;
                }}
            }}
            else if (["ACTOPAN", "MISANTLA", "NAOLINCO", "PEROTE", "TEZUITLÁN", "TEZUITLAN", "TLALTETELA", "TRAPICHE", "TUZAMAPA", "XICO"].includes(nombrePlan)) {{
                
                unidad = fleet.find(f => f.restante > 0 && f.nombre === "Large Van MLP foráneo");
                if (!unidad) {{
                    unidad = fleet.find(f => f.restante > 0 && f.nombre === "Small Van MLP foráneo");
                }}

                if (!unidad) {{
                    const listaLigeras = ["Car 8h", "Small Van 9h", "Small Van 9h Ext", "Moto 3h", "Small Van Newbie"];
                    for (let nombreCar of listaLigeras) {{
                        unidad = fleet.find(f => f.restante > 0 && f.nombre === nombreCar);
                        if (unidad) break;
                    }}
                }}
            }}

            if (!unidad) break;

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

    function togglePrioridades() {{
        const panel = document.getElementById('panel-prioridades');
        if (panel.style.top === '0px') {{
            panel.style.top = '-600px';
        }} else {{
            panel.style.top = '0px';
        }}
    }}

function actualizarSelects() {{
    const listaNegativos = ["Car - 8h", "Car - 5h", "Car - 3h", "Car 8h"];
    document.querySelectorAll('.s-type').forEach(select => {{
        let valorActual = select.value;
        select.innerHTML = '<option value="">Seleccionar...</option>';
        
        document.querySelectorAll('#body-' + currentTab + ' tr').forEach(row => {{
            let name = row.querySelector('.edit-name')?.innerText.trim();
            if (!name || name === "IGNORAR") return;
            
            let stock = parseInt(row.querySelector('.f-stock')?.innerText) || 0;
            let left = parseInt(row.querySelector('.f-left')?.innerText) || 0;
            let nameLower = name.toLowerCase();

            let permiteNegativos = listaNegativos.some(u => nameLower.includes(u.toLowerCase())) || currentTab == 6;
            
            if (permiteNegativos || stock > left) {{
                let opt = document.createElement('option');
                opt.value = name;
                opt.textContent = name;
                select.appendChild(opt);
            }}
        }});
        select.value = valorActual;
    }});
}}

document.addEventListener('input', (e) => {{
    if (e.target.classList.contains('f-stock') || e.target.classList.contains('u-manual')) {{
        recalc(); 
    }}
}});
window.addEventListener('load', () => {{
    actualizarSelects();
    agregarIndicadorSchedule(); 
}});
actualizarDosPorciento();

function agregarIndicadorSchedule() {{
    let headers = document.querySelectorAll('th');
    headers.forEach(th => {{
        if (th.innerText.includes("SCHEDULE") && !th.querySelector('.hand-emoji')) {{
            th.innerHTML = '<div style="display: flex; flex-direction: column; align-items: center; line-height: 1.1;">' +
                           '<span class="hand-emoji" style="font-size: 14px; margin-bottom: 2px;">👇</span>' +
                           '<span>SCHEDULE</span>' +
                           '</div>';
        }}
    }});
}}

document.addEventListener("keydown", function(e){{
    const celda = document.activeElement;
    if (!celda || !celda.hasAttribute("contenteditable")) return;
    const fila = celda.closest("tr");
    if (!fila) return;
    const tabla = fila.closest("table");
    if (!tabla) return;
    const filas = Array.from(tabla.querySelectorAll("tbody tr"));
    const filaIdx = filas.indexOf(fila);
    const celdasFila = Array.from(fila.querySelectorAll('[contenteditable="true"]'));
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
        if(celdasFila[colIdx + 1]){{ celdasFila[colIdx + 1].focus(); }}
    }}
    if(e.key === "ArrowLeft"){{
        e.preventDefault();
        if(celdasFila[colIdx - 1]){{ celdasFila[colIdx - 1].focus(); }}
    }}
}});

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

const ruteos = [
    {{ nombre:"SMX9", hora:"16:40" }},
    {{ nombre:"SGD2", hora:"17:00" }},
    {{ nombre:"SMX5", hora:"17:20" }},
    {{ nombre:"SMX4", hora:"17:40" }},
    {{ nombre:"SMX2", hora:"18:05" }},
    {{
        nombre:"SMT2",
        hora:"18:40"
    }},
    {{
        nombre:"SCP1 C1",
        hora:"20:00"
    }},
    {{
        nombre:"SMX5 PREC",
        hora:"21:30"
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
        if (elHora) {{ elHora.innerText = "A LAS " + siguiente.tarea.hora; }}
        let diff = siguiente.fechaTarea - ahora;
        let mins = Math.floor(diff / 60000);
        let secs = Math.floor((diff % 60000) / 1000);
        elCuenta.innerText = String(mins).padStart(2,"0") + ":" + String(secs).padStart(2,"0");
        elCuenta.style.color = mins < 5 ? "#FF0000" : "#7CFFB2";
    }}
}}
setInterval(actualizarRelojRuteos, 1000);

function convertTime() {{
    let m = parseInt(document.getElementById('min-in').value) || 0;
    document.getElementById('time-res').innerText = Math.floor(m/60) + "h " + (m%60) + "m";
}}

function updateFleetFloat() {{
    let body = document.getElementById('fleet-float-body');
    if (!body) return;
    let html = "";
    document.querySelectorAll('#body-' + currentTab + ' tr').forEach(row => {{
        let name = row.querySelector('.edit-name')?.innerText.trim();
        let left = row.querySelector('.f-left')?.innerText.trim();
        if (name && name !== "IGNORAR") {{
            html += `<div><b>\${name}:</b> \${left}</div>`;
        }}
    }});
    body.innerHTML = html;
}}

function actualizarVisibilidadContador() {{
    let div = document.getElementById('mi-contador');
    if (div) {{ div.style.display = 'block'; }}
}}

function updateSelectColor(select) {{
    if (select.value === "") {{ select.style.color = "#808080"; }}
    else {{ select.style.color = "#25282b"; }}
}}

function toggleTools() {{
    let panel = document.querySelector('.tools-panel');
    let btn = document.getElementById('toggle-tools-btn');
    if (panel.style.display === 'none') {{
        panel.style.display = 'flex';
        btn.innerText = '❌ OCULTAR UTILERÍAS';
    }} else {{
        panel.style.display = 'none';
        btn.innerText = '⚙️ MOSTRAR UTILERÍAS';
    }}
}}

    function aplicarOpcionesSelect() {{
        let optionsHtml = '<option value="">Seleccionar...</option>';
        document.querySelectorAll('#body-' + currentTab + ' tr').forEach(row => {{
            let name = row.querySelector('.edit-name')?.innerText.trim();
            if (name && name !== "IGNORAR") {{
                optionsHtml += `<option value="\${name}">\${name}</option>`;
            }}
        }});
        document.querySelectorAll('#polys-' + currentTab + ' .s-type').forEach(select => {{
            let val = select.value;
            select.innerHTML = optionsHtml;
            select.value = val;
            updateSelectColor(select);
        }});
    }}

    setTimeout(() => {{
        aplicarOpcionesSelect();
        recalc();
    }}, 800);

</script>
</body>
</html>
"""

html(app_html, height=1200, scrolling=True)


# --- SECCIÓN NOTITAS OPERATIVAS ---
import streamlit.components.v1 as components

ID_IMAGEN = "1M4GLEwFzhLrZjV-zmvGrdTQhC6IjwxOJ"
url_final = f"https://drive.google.com/thumbnail?id={ID_IMAGEN}&sz=w1000"

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
            - ❌ delimitación / ❌ restriction<br>
            - Quito puntos muy lejanos</p>
        </div>

        <h3 style='color: #000; margin-top: 25px;'>🟪 SDE 🟪</h3>
        <hr style='border: 1px solid #FF00FF; margin-bottom: 20px;'>
        
        <div style='background: white; border-left: 6px solid #FF00FF; padding: 12px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); color: #000; margin-bottom: 12px;'>
            <p style='margin: 0;'><strong><span style="color: #FF00FF;">●</span> SMX9 PM2 - ⏰ 16:40 - 17:00</strong><br>
            - 📌 Orígenes: MXCD02, MXCD06<br>
            - 👉 Vol aprox. 800 / en peak puede aumentar hasta 1600<br>
            - 👉 fecha promesa</p>
        </div>

        <div style='background: white; border-left: 6px solid #FF00FF; padding: 12px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); color: #000; margin-bottom: 12px;'>
            <p style='margin: 0;'><strong><span style="color: #FF00FF;">●</span> SGD2 PM2 - ⏰ 17:00 - 17:20</strong><br>
             - 📌 Orígenes: MXJC01<br>
             - 👉 Vol aprox. __<br>
             - 👉 fecha promesa + quemada</p>
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
            <p style='margin: 0;'><strong><span style="color: #FF00FF;">●</span> SMX2 PM2 - ⏰ 18:00 - 18:20</strong><br>
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

        <h3 style='color: #000; margin-top: 25px;'>🟥 CICLO 1 🟥</h3>
        <hr style='border: 1px solid #ff8c00; margin-bottom: 20px;'>

        <div style='background: white; border-left: 6px solid #DC143C; padding: 12px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); color: #000; margin-bottom: 12px;'>
            <p style='margin: 0;'><strong><span style="color: #DC143C;">●</span> SCP1 AM1 - ⏰ 20:00 - 21:00</strong><br>
             - 📌 Ellos envían el volumen a tomar, por lo que puede tomarse todo o descartarse ciertos despachos y orígenes<br>
             - 👉 Vieja experiencia<br>
             - 👉 Archivo de vehículos<br>
             - 👀 Revisar si se agrega ➕ forms<br>
             - ✅ Volumen aprox. 3000<br>
             - 1️⃣ Large Van MLP resto de planes / Cuando hay vol. normal y Nodos = Híbrida<br>
             - 1️⃣ Rental Large Van en Campeche = vol. normal / Delivery Cell (dedicada) = NODOS solo Campeche</p>
        </div>

        <h3 style='color: #000; margin-top: 25px;'>🟧 PRE-CARGA 🟧</h3>
        <hr style='border: 1px solid #ff8c00; margin-bottom: 20px;'>

        <div style='background: white; border-left: 6px solid #ff8c00; padding: 15px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); color: #000; margin-bottom: 20px;'>
            <p style='margin: 0;'><strong>👉👉 INDICACIONES</strong><br>
            - 📌 Origen + despachos (playbook - ó indicados por SVC) + onway<br>
            - 👉 Schedule del día siguiente / apartado en archivo AMO<br>
            - ➕ Mandan ids a agregar<br>
            - ✅ delimitación / ✅ dejar restricción</p>
        </div>
        
        <div style='background: white; border-left: 6px solid #ff8c00; padding: 12px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); color: #000; margin-bottom: 12px;'>
            <p style='margin: 0;'><strong><span style="color: #ff8c00;">●</span> SMX5 AM3 - ⏰ 21:30 - 22:10</strong><br>
             - 📌 Origen 09 + onway<br>
             - ➕ Agregan ids a ciclo (de origen 10)<br>
             - ✅ Validan volumen / aprox. 2500-2600<br>
             - 🚛 Tlalpan norte, sur y Xochimilco con car 8h extra E1 (para no dropear)</p>
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
            - 🏍️ Ocupo MOTOS ➡️ Cuauhtémoc-Polanco</p>
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

        <div style='background: white; border-left: 6px solid #ff8c00; padding: 12px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); color: #000; margin-bottom: 12px;'>
            <p style='margin: 0;'><strong><span style="color: #ff8c00;">●</span> SMX2 AM3 - ⏰ 22:40 - 23:20</strong><br>
             - 📌 Orígenes: MXCD02 despacho de hoy hasta 16:00 / MXCD09  despacho de hoy hasta 14:00 / MXCD10  despacho de hoy hasta 21:00<br>
             - 👉 Todo Onway<br>
             - 👀 Revisar si se agrega ➕ forms<br>
             - ✅ Validan volumen / aprox. 1900-2000<br>
             - 🚛 Extendidas en Texcoco, Pueblos y Chalco</p>
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

html_notitas = f"""
<style>
    body {{ background-color: #25282b; font-family: 'Segoe UI', Tahoma, sans-serif; margin: 0; }}
    .main-box {{ background: #25282b; padding: 10px; }}
    
    .unified-console {{
        background: #25282b; border-radius: 15px; padding: 15px; 
        margin-bottom: 20px; border: 1px solid #25282b; text-align: center;
    }}
    .display-screen {{
        background: #25282b; border-radius: 10px; padding: 10px; margin-bottom: 15px; border: 2px solid #25282b;
    }}
    .btn-3d {{
        background: linear-gradient(145deg, #1e90ff, #1c82e6);
        color: white;
        border: none; padding: 12px 25px; border-radius: 10px;
        font-weight: bold; cursor: pointer; box-shadow: 0 5px #0a56a3; transition: 0.1s;
    }}
    .btn-3d:active {{ box-shadow: 0 2px #0a56a3; transform: translateY(3px); }}

    .tab-bar {{ display: flex; gap: 8px; margin-bottom: 15px; overflow-x: auto; }}
    .tab-btn {{
        background: #333;
        color: white; border: none; padding: 10px 18px;
        border-radius: 8px; cursor: pointer; font-weight: bold; font-size: 12px; white-space: nowrap;
    }}
    .tab-btn.active {{ background: #add8e6; color: black; box-shadow: 0 0 12px #add8e6; }}

    body:not(.tab-2) #excel-btn {{ display: none !important; }}
    
    .content-area {{ background: #c8dee0; border-radius: 12px; padding: 20px; min-height: 600px; color: #000; }}
</style>

<div class="main-box">
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

st.markdown("---")
components.html(html_notitas, height=1200, scrolling=True)
