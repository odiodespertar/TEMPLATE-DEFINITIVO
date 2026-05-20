import json
import streamlit as st
from streamlit.components.v1 import html     

st.set_page_config(page_title="Monitor Logístico - Liliana García", layout="wide", initial_sidebar_state="expanded")

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
NOMBRES_PLANES_PREG = ["CHALCO", "CHIMAS", "IXTAPALUCA VALLE CHALCO", "IZTAPALAPA 1", "IZTAPALAPA 2", "LA PAZ", "PUEBLOS", "TEXCOCO"]


u_C1 = {
    "Rental E. Large Van": [120, 120], "Rental E. Small Van": [120, 120], "Rental Large Van": [120, 120], 
    "Rental Small Van": [120, 120], "Large Van MLP": [100, 100], "Small Van MLP":[80, 80],
    "Car MLP": [50, 50], "Moto - 3h": [28, 28], "Car Newbie 3h": [30, 30], "Car - 8h": [80, 85], "Car - 5h": [60, 60]
}
u_C2 = u_C1.copy()
u_C2["Large Van Híbrida"] = [100, 100]


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
    "Car - 5h": ["300", "66"],
    "Car - 3h": ["300", "66"],

    "Moto - 3h": ["180", "66"],

    "Small Van SDD": ["487", "70"],
    "Car Zona Extendida": ["360", "66"],
    "Car - 5h Extendida": ["330", "66"]
}



def gen_master_rows(data_dict, table_id):
    rows = ""
    items = list(data_dict.items())
    total_items = len(items)

    nombres_prec = ["CHALCO", "COYOACÁN", "IZTAPALAPA", "MILPA ALTA", "TLAHUAC", "TLALPAN NORTE", "TLALPAN SUR", "XOCHIMILCO"]
    nombres_smx2 = ["CHALCO", "CHIMAS", "IXTAPALUCA VALLE CHALCO", "IZTAPALAPA 1", "IZTAPALAPA 2", "LA PAZ", "PUEBLOS", "TEXCOCO"]
    
    num_filas_objetivo = 45 if table_id == "PREC" else 11
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
            
        # Caso A: Es un Encabezado/Divisor
        if "---" in name:
            rows += f'''
            <tr class="es-divisor" style="background: #333 !important; color: #696969; height: 28px;">
                <td colspan="4" style="text-align: center; font-weight: bold; font-size: 11px; letter-spacing: 3px; border: none; pointer-events: none;">
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
                <td contenteditable="true" class="edit-name" oninput="recalc()" style="font-weight: bold; text-align: left; padding-left: 10px; border: 0.2px solid #A9A9A9; width: 150px; color: #878686;">{name}</td>
                <td contenteditable="true" class="edit-spr-min" oninput="recalc()" style="text-align: center; border: 0.2px solid #A9A9A9; width: 45px; background-color: #A9A9A9; color: #ffffff;">{spr[0]}</td>
                <td contenteditable="true" class="edit-spr-max" oninput="recalc()" style="text-align: center; border: 0.2px solid #A9A9A9; width: 45px; background-color: #A9A9A9; color: #ffffff;">{spr[1]}</td>
                
                <td class="edit-orh" style="display:none;">0</td>
                <td class="edit-ocup" style="display:none;">0</td>
                
                <td contenteditable="true" class="f-stock" oninput="recalc()" style="text-align: center; border: 0.2px solid #A9A9A9; width: 55px; font-weight: bold; font-size: 13px;">0</td>
                <td class="f-left" style="font-weight: bold; text-align: center; border: 0.5px solid #A9A9A9; width: 60px; font-size: 18px;">0</td>
            </tr>''' 
    return rows



def gen_poligonos(data_target=None):
    polys = ""
    # Botones con dimensiones totalmente congeladas a nivel píxel
    btn_s = "cursor:pointer; border:none; background:rgba(0,0,0,0.08); color:#333; font-weight:bold; width:24px; min-width:24px; max-width:24px; height:24px; min-height:24px; max-height:24px; border-radius:4px; flex-shrink:0; display:inline-flex; align-items:center; justify-content:center;"
    
    nombres_prec = ["CHALCO", "COYOACÁN", "IZTAPALAPA", "MILPA ALTA", "TLAHUAC", "TLALPAN NORTE", "TLALPAN SUR", "XOCHIMILCO"]
    nombres_smx2 = ["CHALCO", "CHIMAS", "IXTAPALUCA VALLE CHALCO", "IZTAPALAPA 1", "IZTAPALAPA 2", "LA PAZ", "PUEBLOS", "TEXCOCO"]
    
    # Contenedor flex con ancho bloqueado al 100% de la celda
    div_flex = "display: flex; align-items: center; justify-content: space-between; padding: 2px 4px; width: 100%; min-width: 100%; max-width: 100%; box-sizing: border-box;"
    
    # Cajas de texto para números (Unidades y SPR)
    span_num_u = "font-weight: bold; display: inline-block; text-align: center; width: 28px; min-width: 28px; max-width: 28px; flex-shrink: 0;"
    span_num_spr = "font-weight: bold; display: inline-block; text-align: center; width: 48px; min-width: 48px; max-width: 48px; flex-shrink: 0;"
    
    # 🔥 ESTILO DEL SELECTOR RECALIBRADO (Letra más grande, legible y cómoda para la operación)
    select_style = "width:100%; border:none; background:transparent; font-weight:600; font-size:14px; color:#333; padding: 4px; cursor: pointer;"

    fila_inner = f'''
    <tr class="calc-row">
        <td class="u-manual-cell" style="background: #fcfbc7; border: 0.6px solid #696969; padding: 2px; width: 105px; min-width: 105px; max-width: 105px;">
            <div style="{div_flex}">
                <button style="{btn_s}" onclick="stepVal(this, -1, 'u')">-</button>
                <span contenteditable="true" class="u-manual" oninput="manualEdit(this)" style="{span_num_u}">0</span>
                <button style="{btn_s}" onclick="stepVal(this, 1, 'u')">+</button>
            </div>
        </td>
        <td class="spr-real-cell" style="background: #FFFFFF; border: 0.6px solid #696969; padding: 2px; width: 135px; min-width: 135px; max-width: 135px;">
            <div style="{div_flex}">
                <button style="{btn_s}" onclick="stepVal(this, -1, 's')">-</button>
                <span contenteditable="true" class="spr-real-val" oninput="manualEdit(this)" style="{span_num_spr}">0</span>
                <button style="{btn_s}" onclick="stepVal(this, 1, 's')">+</button>
            </div>
        </td>
        <td style="border: 0.5px solid #696969; padding: 2px;">
    <select class="s-type" onchange="resetRow(this); updateSelectColor(this);" style="{select_style} color: #808080; width: 100%;"> 
        <option value="">SELECCIONAR...</option>
        </select>
</td>
        <td style="width: 45px; min-width: 45px; max-width: 45px; text-align: center; border: 0.5px solid #696969;"><input type="checkbox" class="ok-check" style="transform: scale(1.1); accent-color: #FF00FF; cursor: pointer;"></td>
    </tr>'''

    for i in range(1, 11):
        if data_target == u_PREC and (i-1) < len(nombres_prec):
            nombre_final = nombres_prec[i-1]
        elif data_target == u_PREC_SMX2 and (i-1) < len(nombres_smx2): 
            nombre_final = nombres_smx2[i-1]
        else:
            nombre_final = f"PLAN {i}"

        polys += f'''
        <div class="poligono-bloque" style="margin-bottom:12px; box-shadow: none; border-radius: 0px; overflow: hidden; background: #ededed; border: 1.5px solid #696969;">           
            <table style="width: 100%; border-collapse: collapse; border: 1.5px solid #696969;">
                <thead>
                    <tr style="background: #696969; color: white; font-size: 12px; height: 28px;">                        
                        <th style="padding: 0 10px; border-right: 1px solid rgba(#696969);">PLAN</th>
                        <th style="border-right: 1px solid rgba(#696969); width: 85px;">VOL. TOTAL</th>
                        <th style="width: 105px; min-width: 105px; max-width: 105px; border-right: 1px solid rgba(#696969);"># ASIGNADAS</th>
                        <th style="width: 105px; min-width: 105px; max-width: 105px; border-right: 1px solid rgba(#696969);">SPR REAL</th>
                        <th style="width: 80px, border-right: 1px solid rgba(#696969);">TIPO DE UNIDAD</th>
                        <th style="width: 45px; min-width: 45px; max-width: 45px; text-align: center;">OK</th>
                    </tr>
                </thead>
                <tbody>
                    <tr class="calc-row"> 
                        <td rowspan="5" contenteditable="true" style="background: #D3D3D3; font-weight:bold; text-align:center; border: 1px solid #696969; padding: 5px; color:#333;">{nombre_final}</td>
                        <td rowspan="5" contenteditable="true" class="v-total-val" oninput="recalc()" style="color: #20B2AA; font-weight: bold; font-size: 18px; text-align: center; border: 1px solid #696969; padding: 5px;">0</td>
                        <td class="u-manual-cell" style="background: #fcfbc7; border: 0.5px solid #696969; padding: 2px; width: 105px; min-width: 105px; max-width: 105px;">
                            <div style="{div_flex}">
                                <button style="{btn_s}" onclick="stepVal(this, -1, 'u')">-</button> 
                                <span contenteditable="true" class="u-manual" oninput="manualEdit(this)" style="{span_num_u}">0</span>
                                <button style="{btn_s}" onclick="stepVal(this, 1, 'u')">+</button>
                            </div>
                        </td>
                        <td class="spr-real-cell" style="background: #FFFFFF; border: 0.5px solid #696969; padding: 2px; width: 135px; min-width: 135px; max-width: 135px;">
                            <div style="{div_flex}">
                                <button style="{btn_s}" onclick="stepVal(this, -1, 's')">-</button>
                                <span contenteditable="true" class="spr-real-val" oninput="manualEdit(this)" style="{span_num_spr}">0</span>
                                <button style="{btn_s}" onclick="stepVal(this, 1, 's')">+</button>
                            </div>
                        </td>
                        <td style="border: 0.5px solid #696969; padding: 2px;">
                            <select class="s-type" onchange="resetRow(this)" style="{select_style}">
                                <option>SELECCIONAR...</option>
                            </select>
                        </td>
                        <td style="width: 45px; min-width: 45px; max-width: 45px; text-align: center; border: 0.5px solid #696969;"><input type="checkbox" class="ok-check" style="transform: scale(1.2); accent-color: #FF00FF; cursor: pointer;"></td>
                    </tr>
                    {fila_inner}{fila_inner}{fila_inner}{fila_inner}
                     <tr style="background:#ededed; height: 32px;">
                        <td colspan="3" style="text-align:center; font-weight:bold; border: 1px solid #696969; font-size: 14px; color:#696969;">ESTADO:</td>
                        <td class="v-calculado-total" style="font-weight: bold; font-size: 14px; color: #d32f2f; border: 1px solid #696969; text-align: center;">0</td>
                        <td class="p-diff" colspan="2" style="text-align: center; font-weight: bold; border: 1px solid #696969; font-size: 14px;">VACÍO; color: #696969</td>
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


/* Contador flotante*/

#fleet-float {{

    position: fixed !important;

    right: 14px !important; 

    top: 210px !important;

    width: 150px;

    background: rgba(20,20,20,0.96);
    color: white;

    border-radius: 14px;

    padding: 14px 16px;

    z-index: 999999 !important;

    box-shadow: 0 6px 18px rgba(0,0,0,.35);

    font-size: 12px;

    border: 1px solid rgba(255,255,255,.08);

    backdrop-filter: blur(8px);

    max-height: 75vh;

    overflow-y: auto;
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

<div style="display:flex; flex-direction:column; gap:20px; width:100%;">


    <!-- COLUMNA DERECHA --> 


<!-- PANEL SUPERIOR -->
<div style="
    width:100%;
    padding:0;
    margin-bottom:10px;
">

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
       <table class="meli-table" style="width: 100%; table-layout: fixed; border-collapse: collapse;">
        <thead>
            <tr style="background: linear-gradient(180deg, #333 0%, #1a1a1a 100%); color: white;">
                <th style="border-right: 0.5px solid #555; padding: 4px 8px; font-size: 11px;">UNIDAD</th>
                <th style="border-right: 0.5px solid #555; padding: 2px; font-size: 11px; width: 45px;">SPR MIN</th>
                <th style="border-right: 0.5px solid #555; padding: 2px; font-size: 11px; width: 45px;">SPR MAX</th>
                <th style="border-right: 0.5px solid #555; padding: 4px 8px; font-size: 11px; width: 60px;">SCHEDULE</th>
                <th style="padding: 4px 8px; font-size: 11px; width: 65px;">DELTA</th>
            </tr>
        </thead>
        <tbody id="body-2">{gen_master_rows(u_C1, 2)}</tbody>
        <tfoot>
            <tr style="background:#1a1a1a; color:white; font-weight:bold;">
                <td colspan="3" style="padding:6px; text-align:right;"> TOTAL MLP </td>
                <td id="total-no-car-2" style="text-align:center; color:#00ff99;"> 0 </td>
                <td></td>
            </tr>
            <tr style="background:#111; color:white; font-weight:bold;">
                <td colspan="3" style="padding:6px; text-align:right;"> TOTAL CAR REAL </td>
                <td id="total-car-real-2" style="text-align:center; color:#00BFFF;"> 0 </td>
                <td></td>
            </tr>
        </tfoot>
    </table>
</div>

       
        <div id="tab-1" class="t-content" style="display:none;">
            <table class="meli-table" style="width: 100%; table-layout: fixed; border-collapse: collapse;">
        <thead>
            <tr style="background: linear-gradient(180deg, #333 0%, #1a1a1a 100%); color: white;">
                <th style="border-right: 0.5px solid #555; padding: 4px 8px; font-size: 11px;">UNIDAD</th>
                <th style="border-right: 0.5px solid #555; padding: 2px; font-size: 11px; width: 45px;">SPR MIN</th>
                <th style="border-right: 0.5px solid #555; padding: 2px; font-size: 11px; width: 45px;">SPR MAX</th>
                <th style="border-right: 0.5px solid #555; padding: 4px 8px; font-size: 11px; width: 60px;">SCHEDULE</th>
                <th style="padding: 4px 8px; font-size: 11px; width: 65px;">DELTA</th>
            </tr>
        </thead>
        <tbody id="body-1">{gen_master_rows(u_PREC, 1)}</tbody>
          <tfoot>
            <tr style="background:#1a1a1a; color:white; font-weight:bold;">
                <td colspan="3" style="padding:6px; text-align:right;"> TOTAL MLP </td>
                <td id="total-no-car-1" style="text-align:center; color:#00ff99;"> 0 </td>
                <td></td>
            </tr>
            <tr style="background:#111; color:white; font-weight:bold;">
                <td colspan="3" style="padding:6px; text-align:right;"> TOTAL CAR REAL </td>
                <td id="total-car-real-1" style="text-align:center; color:#00BFFF;"> 0 </td>
                <td></td>
            </tr>
        </tfoot>
    </table>
</div>

       
        <div id="tab-5" class="t-content" style="display:none;">
            <table class="meli-table" style="width: 100%; table-layout: fixed; border-collapse: collapse;">
        <thead>
            <tr style="background: linear-gradient(180deg, #333 0%, #1a1a1a 100%); color: white;">
                <th style="border-right: 0.5px solid #555; padding: 4px 8px; font-size: 11px;">UNIDAD</th>
                <th style="border-right: 0.5px solid #555; padding: 2px; font-size: 11px; width: 45px;">SPR MIN</th>
                <th style="border-right: 0.5px solid #555; padding: 2px; font-size: 11px; width: 45px;">SPR MAX</th>
                <th style="border-right: 0.5px solid #555; padding: 4px 8px; font-size: 11px; width: 60px;">SCHEDULE</th>
                <th style="padding: 4px 8px; font-size: 11px; width: 65px;">DELTA</th>
            </tr>
        </thead>
        <tbody id="body-5">{gen_master_rows(u_PREC_SMX2, 5)}</tbody>
       <tfoot>
            <tr style="background:#1a1a1a; color:white; font-weight:bold;">
                <td colspan="3" style="padding:6px; text-align:right;"> TOTAL MLP </td>
                <td id="total-no-car-5" style="text-align:center; color:#00ff99;"> 0 </td>
                <td></td>
            </tr>
            <tr style="background:#111; color:white; font-weight:bold;">
                <td colspan="3" style="padding:6px; text-align:right;"> TOTAL CAR REAL </td>
                <td id="total-car-real-5" style="text-align:center; color:#00BFFF;"> 0 </td>
                <td></td>
            </tr>
        </tfoot>
    </table>
</div>


        
        <div id="tab-4" class="t-content" style="display:none;">
            <table class="meli-table" style="width: 100%; table-layout: fixed; border-collapse: collapse;">
        <thead>
            <tr style="background: linear-gradient(180deg, #333 0%, #1a1a1a 100%); color: white;">
                <th style="border-right: 0.5px solid #555; padding: 4px 8px; font-size: 11px;">UNIDAD</th>
                <th style="border-right: 0.5px solid #555; padding: 2px; font-size: 11px; width: 45px;">SPR MIN</th>
                <th style="border-right: 0.5px solid #555; padding: 2px; font-size: 11px; width: 45px;">SPR MAX</th>
                <th style="border-right: 0.5px solid #555; padding: 4px 8px; font-size: 11px; width: 60px;">SCHEDULE</th>
                <th style="padding: 4px 8px; font-size: 11px; width: 65px;">DELTA</th>
            </tr>
        </thead>
        <tbody id="body-4">{gen_master_rows(u_SDE, 4)}</tbody>
       <tfoot>
            <tr style="background:#1a1a1a; color:white; font-weight:bold;">
                <td colspan="3" style="padding:6px; text-align:right;"> TOTAL MLP </td>
                <td id="total-no-car-4" style="text-align:center; color:#00ff99;"> 0 </td>
                <td></td>
            </tr>
            <tr style="background:#111; color:white; font-weight:bold;">
                <td colspan="3" style="padding:6px; text-align:right;"> TOTAL CAR REAL </td>
                <td id="total-car-real-4" style="text-align:center; color:#00BFFF;"> 0 </td>
                <td></td>
            </tr>
        </tfoot>
    </table>
</div>



<!-- ================= PRIORIDADES Y RESTRICCIONES ================= -->

<div style="margin-top:15px; display:flex; flex-direction:column; gap:10px;">

    <!-- ================= SMX5 ================= -->
    <details style="border:1px solid #292928; border-radius:10px; background:#f8f8f8; overflow:hidden;">
        
        <summary style="
            cursor:pointer;
            font-weight:bold;
            font-size:14px;
            padding:12px;
            background:linear-gradient(180deg, #D3D3D3 0%, #C0C0C0 100%);
            color: #292928;
            user-select:none;
        ">
            📍 PRIORIDADES Y RESTRICCIONES SMX5 (AM0)
        </summary>

        <div style="padding:12px;">

            <div style="
                background:#fff3cd;
                border:1px solid #ffe69c;
                color:#856404;
                padding:8px;
                border-radius:6px;
                margin-bottom:10px;
                font-size:12px;
                font-weight:bold;
            ">
                ⚠️ Revisar ORH y ocupación por día en summary<br>
                Distancia de SVC 🟢🟡🟠🔴
            </div>

            <table style="
                width:100%;
                border-collapse:collapse;
                font-size:12px;
                background:white;
            ">

                <thead>
                    <tr style="
                        background:linear-gradient(180deg,#555 0%, #333 100%);
                        color:white;
                    ">
                        <th style="padding:8px; border:1px solid #ccc;">POLÍGONO</th>
                        <th style="padding:8px; border:1px solid #ccc;">PRIORIDAD / RESTRICCIÓN</th>
                        <th style="padding:8px; border:1px solid #ccc;">VOL REAL APROX</th>
                        <th style="padding:8px; border:1px solid #ccc;">ASIGNACIÓN REAL</th>
                    </tr>
                </thead>

                <tbody>

                    <tr>
                        <td style="padding:8px; border:1px solid #ddd;"><b>🟠 CHALCO</b></td>
                        <td style="padding:8px; border:1px solid #ddd;">LV MLP SDD > Crowd(6:00 hrs)</td>
                        <td style="border:1px solid #ccc; padding:5px; text-align:center;">260</td>
                        <td style="padding:8px; border:1px solid #ddd;">SOLO CROWD</td>
                    </tr>

                    <tr style="background:#f9f9f9;">
                        <td style="padding:8px; border:1px solid #ddd;"><b>🟢 COYOACÁN CENTRO</b></td>
                        <td style="padding:8px; border:1px solid #ddd;">MLP SDD > Newbie > Crowd(6:00 hrs)</td>
                        <td style="border:1px solid #ccc; padding:5px; text-align:center;">500</td>
                        <td style="padding:8px; border:1px solid #ddd;">SOLO CROWD</td>
                    </tr>

                    <tr>
                        <td style="padding:8px; border:1px solid #ddd;"><b>🟢 IZTAPALAPA</b></td>
                        <td style="padding:8px; border:1px solid #ddd;">MLP SDD > Newbie(4:30 hrs) > Crowd(6:00 hrs)</td>
                        <td style="border:1px solid #ccc; padding:5px; text-align:center;">300</td>
                        <td style="padding:8px; border:1px solid #ddd;">NEWBIES Y CROWD</td>
                    </tr>

                    <tr style="background:#f9f9f9;">
                        <td style="padding:8px; border:1px solid #ddd;"><b>🟠 MILPA ALTA</b></td>
                        <td style="padding:8px; border:1px solid #ddd;">LV MLP SDD > Crowd(6:00 hrs)</td>
                        <td style="border:1px solid #ccc; padding:5px; text-align:center;">170</td>
                        <td style="padding:8px; border:1px solid #ddd;">SOLO CROWD</td>
                    </tr>

                    <tr>
                        <td style="padding:8px; border:1px solid #ddd;"><b>🟢 TLÁHUAC</b></td>
                        <td style="padding:8px; border:1px solid #ddd;">MLP SDD > Newbie > Crowd(6:00 hrs)</td>
                        <td style="border:1px solid #ccc; padding:5px; text-align:center;">750</td>
                        <td style="padding:8px; border:1px solid #ddd;">SMALL VAN SDD Y CROWD</td>
                    </tr>

                    <tr style="background:#f9f9f9;">
                        <td style="padding:8px; border:1px solid #ddd;"><b>🟢 TLALPAN NTE</b></td>
                        <td style="padding:8px; border:1px solid #ddd;">MLP SDD(L-9:00 hrs / S-8:30 hrs) > Newbie > Crowd(6:00 hrs)</td>
                        <td style="border:1px solid #ccc; padding:5px; text-align:center;">580</td>
                        <td style="padding:8px; border:1px solid #ddd;">SMALL VAN SDD</td>
                    </tr>

                    <tr>
                        <td style="padding:8px; border:1px solid #ddd;"><b>🟢 TLALPAN SUR</b></td>
                        <td style="padding:8px; border:1px solid #ddd;">MLP SDD(L-9:00 hrs)</td>
                        <td style="border:1px solid #ccc; padding:5px; text-align:center;">90</td>
                        <td style="padding:8px; border:1px solid #ddd;">SMALL VAN SDD</td>
                    </tr>

                    <tr style="background:#f9f9f9;">
                        <td style="padding:8px; border:1px solid #ddd;"><b>🟡 XOCHIMILCO</b></td>
                        <td style="padding:8px; border:1px solid #ddd;">MLP SDD(L/S-9:00 hrs aprox.) > Crowd</td>
                        <td style="border:1px solid #ccc; padding:5px; text-align:center;">660</td>
                        <td style="padding:8px; border:1px solid #ddd;">SMALL VAN SDD Y CROWD</td>
                    </tr>

                </tbody>

            </table>

        </div>

    </details>



    <!-- ================= SMX2 ================= -->
    <details style="border:1px solid #292928; border-radius:10px; background:#f8f8f8; overflow:hidden;">
        
        <summary style="
            cursor:pointer;
            font-weight:bold;
            font-size:14px;
            padding:12px;
            background:linear-gradient(180deg, #D3D3D3 0%, #C0C0C0 100%);
            color: #292928;
            user-select:none;
        ">
            📍 PRIORIDADES Y RESTRICCIONES SMX2 (AM0)
        </summary>

        <div style="padding:12px;">

            <div style="
                background:#fff3cd;
                border:1px solid #ffe69c;
                color:#856404;
                padding:8px;
                border-radius:6px;
                margin-bottom:10px;
                font-size:12px;
                font-weight:bold;
            ">
                ⚠️ Revisar ORH y ocupación por día en summary<br>
                Distancia de SVC 🟢🟡🟠🔴
            </div>

            <table style="
                width:100%;
                border-collapse:collapse;
                font-size:12px;
                background:white;
            ">

                <thead>
                    <tr style="
                        background:linear-gradient(180deg,#555 0%, #333 100%);
                        color:white;
                    ">
                        <th style="padding:8px; border:1px solid #ccc;">POLÍGONO</th>
                        <th style="padding:8px; border:1px solid #ccc;">PRIORIDAD / RESTRICCIÓN</th>
                        <th style="padding:8px; border:1px solid #ccc;">VOL REAL APROX</th>
                        <th style="padding:8px; border:1px solid #ccc;">ASIGNACIÓN REAL</th>
                    </tr>
                </thead>

                <tbody>

                    <tr>
                        <td style="padding:8px; border:1px solid #ddd;"><b>🟠 CHALCO</b></td>
                        <td style="padding:8px; border:1px solid #ddd;">DC > Crowd(6:00 hrs)</td>
                        <td style="border:1px solid #ccc; padding:5px; text-align:center;">300</td>
                        <td style="padding:8px; border:1px solid #ddd;">EXTENDIDA Y CROWD</td>
                    </tr>

                    <tr style="background:#f9f9f9;">
                        <td style="padding:8px; border:1px solid #ddd;"><b>🟡 CHIMAS</b></td>
                        <td style="padding:8px; border:1px solid #ddd;">Newbie > Crowd > MLP(S-7:30 hrs)</td>
                        <td style="border:1px solid #ccc; padding:5px; text-align:center;">750</td>
                        <td style="padding:8px; border:1px solid #ddd;">CROWD</td>
                    </tr>

                    <tr>
                        <td style="padding:8px; border:1px solid #ddd;"><b>🔴 IXTAPALUCA-VALLE CHALCO</b></td>
                        <td style="padding:8px; border:1px solid #ddd;">Newbie > MLP > Crowd > Car Zona Ext ⚠️ (Ext y Crowd - 5:30 hrs)</td>
                        <td style="border:1px solid #ccc; padding:5px; text-align:center;">1100</td>
                        <td style="padding:8px; border:1px solid #ddd;">EXTENDIDA Y CROWD (⚠️ *Zona roja* ⚠️)</td>
                    </tr>

                    <tr style="background:#f9f9f9;">
                        <td style="padding:8px; border:1px solid #ddd;"><b>🟢 IZTAPALAPA 1</b></td>
                        <td style="padding:8px; border:1px solid #ddd;">MLP(S-3:00 a 7:30 hrs) > Crowd</td>
                        <td style="border:1px solid #ccc; padding:5px; text-align:center;">150</td>
                        <td style="padding:8px; border:1px solid #ddd;">SMALL VAN SDD Y CROWD</td>
                    </tr>

                    <tr>
                        <td style="padding:8px; border:1px solid #ddd;"><b>🟢 IZTAPALAPA 2</b></td>
                        <td style="padding:8px; border:1px solid #ddd;">Newbie > Crowd(5:30 hrs) > MLP(S-7:30 hrs)</td>
                        <td style="border:1px solid #ccc; padding:5px; text-align:center;">480</td>
                        <td style="padding:8px; border:1px solid #ddd;">SMALL VAN SDD Y CROWD</td>
                    </tr>

                    <tr style="background:#f9f9f9;">
                        <td style="padding:8px; border:1px solid #ddd;"><b>🟢 LA PAZ</b></td>
                        <td style="padding:8px; border:1px solid #ddd;">Newbie > Crowd(5:30 hrs)</td>
                        <td style="border:1px solid #ccc; padding:5px; text-align:center;">450</td>
                        <td style="padding:8px; border:1px solid #ddd;">SMALL VAN SDD Y CROWD</td>
                    </tr>

                    <tr>
                        <td style="padding:8px; border:1px solid #ddd;"><b>🟠 PUEBLOS</b></td>
                        <td style="padding:8px; border:1px solid #ddd;">MLP > Crowd(6:00 hrs)</td>
                        <td style="border:1px solid #ccc; padding:5px; text-align:center;">240</td>
                        <td style="padding:8px; border:1px solid #ddd;">SMALL VAN SDD, EXTENDIDA Y CROWD</td>
                    </tr>

                    <tr style="background:#f9f9f9;">
                        <td style="padding:8px; border:1px solid #ddd;"><b>🟠 TEXCOCO</b></td>
                        <td style="padding:8px; border:1px solid #ddd;">Crowd(6:00 hrs) > Car Zona Ext</td>
                        <td style="border:1px solid #ccc; padding:5px; text-align:center;">340</td>
                        <td style="padding:8px; border:1px solid #ddd;">EXTENDIDA Y CROWD</td>
                    </tr>

                </tbody>

            </table>

            <div style="
                margin-top:12px;
                padding:10px;
                background:#ffe5e5;
                border:1px solid #ffb3b3;
                border-radius:6px;
                font-size:12px;
            ">
                ⚠️ <b>ZONA ROJA:</b> IXTAPALUCA-VALLE CHALCO
            </div>

            <div style="
                margin-top:8px;
                padding:10px;
                background:#e8f4ff;
                border:1px solid #b5dbff;
                border-radius:6px;
                font-size:12px;
            ">
                📦 <b>Prioridad:</b> Large Van y MLP en zonas de nodos
            </div>

        </div>

    </details>

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

            

            <!-- 3. CONVERTIDOR (Ahora al final) -->
            <div class="google-tool" style="
                /* 👇 AQUÍ CONTROLAS EL DEGRADADO DIRECTAMENTE */
                background: linear-gradient(135deg, #f2f2f2 0%, #ffffff 100%) !important;
                padding: 15px;
                border-radius: 10px;
            ">
                <button id="toggle-tools-btn" onclick="toggleTools()" 
                    style="cursor:pointer; background: linear-gradient(180deg, #555 0%, #333 100%); color:white; border:1px solid #222; font-size:11px; padding:6px 0; border-radius:4px; font-weight:bold; box-shadow: 0 3px 0 #111; transition: all 0.05s; outline: none; width: 100%; margin-bottom: 15px; display: block;">
                    ❌ OCULTAR UTILERÍAS
                </button>
            
                <div style="font-weight:bold; color:#2c3e50; margin-bottom:10px; font-size:12px; letter-spacing:1px;">⏱️ CONVERTIDOR DE TIEMPO</div>
                <input type="number" id="min-in" placeholder="Minutos" style="width:80px; text-align:center;" oninput="convertTime()">
                <div style="margin-top:10px;">
                    <span id="time-res" style="font-size: 24px; font-weight: bold; color: #008B8B; text-shadow: 1px 1px 2px rgba(0,0,0,0.1);">0h 0m</span>
                 </div>
             </div>
        </div>
    </div>
</div>


<!-- COLUMNA IZQUIERDA -->


<!-- PLANNERS -->
<div style="
    width:100%;
    overflow-y:auto;
    overflow-x:hidden;
">

    
        <div style="background: #2e2e2e; color: white; padding: 10px; border-radius: 8px; text-align: center; font-weight: bold; margin-bottom: 10px;">📋 PLANIFICACIÓN POR POLÍGONOS</div>
        <div id="polys-2" class="p-content">{gen_poligonos(u_C1)}</div>
        <div id="polys-1" class="p-content" style="display:none;">{gen_poligonos(u_PREC)}</div>
        <div id="polys-5" class="p-content" style="display:none;">{gen_poligonos(u_PREC_SMX2)}</div>
        <div id="polys-4" class="p-content" style="display:none;">{gen_poligonos(u_SDE)}</div>
    </div>


<!-- CONTADOR FLOTANTE -->
<div id="fleet-float">
    <div style="font-weight:bold; margin-bottom:8px;">
        🚚 DISPONIBLE
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





    function updateFleetFloat() {{

    let html = "";

    document.querySelectorAll('#body-' + currentTab + ' tr').forEach(row => {{

        let name = row.querySelector('.edit-name')?.innerText.trim();

        let stock =
            parseInt(row.querySelector('.f-stock')?.innerText) || 0;

        let left =
            parseInt(row.querySelector('.f-left')?.innerText) || 0;

        if(name && stock > 0){{

            let color =
                left <= 0
                ? "#ff6b6b"
                : "#00ff99";

            html += `
                <div style="
                    display:flex;
                    justify-content:space-between;
                    margin-bottom:4px;
                ">

                    <span>${{name}}</span>

                    <span style="
                        color:${{color}};
                        font-weight:bold;
                    ">
                        ${{left}}/${{stock}}
                    </span>

                </div>
            `;
        }}
    }});

    document.getElementById('fleet-float-body').innerHTML = html;
}}


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

    updateFleetFloat();
    
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
        // Detectar si la unidad es CAR
let esCAR = sel.toUpperCase().includes("CAR");

// Si NO es CAR, bloquear cuando ya no hay disponibles
if (delta > 0 && left <= 0 && !esCAR) {{
        showAlert("⚠️ NO PUEDES AGREGAR MÁS UNIDADES.");
        return;
}}

// Si SÍ es CAR, permitir negativos pero mostrar alerta
if (delta > 0 && left <= 0 && esCAR) {{
        showAlert("⚠️ EXCESO DE UNIDADES CAR. Se registrará como negativo.");
}}
        span.innerText = val + delta;
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
        span.innerText = newVal.toFixed(1);
    }}
    editedRowsPlan.add(row);
    recalc();
}}


    function recalc() {{
        let fleet = {{}};
        
        // --- NORMALIZACIÓN DE PESTAÑA PARA MANEJO DE IDS ---
        // Guardamos el identificador real que usan los elementos HTML en pantalla
        let tabId = (currentTab === 'C1') ? '2' : currentTab;
        // ----------------------------------------------------

        // 1. Capturar datos de la flota (Tabla de arriba)
document.querySelectorAll('#body-' + tabId + ' tr').forEach(row => {{
    let nameCell = row.querySelector('.edit-name');
    let name = nameCell.innerText.trim();
    let sch = parseInt(row.querySelector('.f-stock').innerText) || 0;
    let mi = row.querySelector('.edit-spr-min'), ma = row.querySelector('.edit-spr-max'), fs = row.querySelector('.f-stock');
    
    if(sch > 0) {{
        row.style.background = "white"; 
        // Eliminamos row.style.color para no forzar toda la fila
        fs.style.background = "#fcfbc7"; 
        mi.style.background = "#f5ffff"; mi.style.color = "#008B8B"; mi.style.fontWeight = "bold";
        ma.style.background = "#f5ffff"; ma.style.color = "#008B8B"; ma.style.fontWeight = "bold";
        
        // Ponemos nombre en NEGRO
        nameCell.style.color = "black";
        nameCell.style.fontWeight = "bold";
    }} else {{
        row.style.background = "#DCDCDC"; 
        // Eliminamos row.style.color = "#969696"
        fs.style.background = "#DCDCDC"; 
        mi.style.background = "#DCDCDC"; mi.style.color = "#969696"; mi.style.fontWeight = "normal";
        ma.style.background = "#DCDCDC"; ma.style.color = "#969696"; ma.style.fontWeight = "normal";
        
        // Ponemos nombre en GRIS
        nameCell.style.color = "#969696";
        nameCell.style.fontWeight = "normal";
    }}
    
    if(name !== "" && name !== "NUEVA UNIDAD") {{
        fleet[name] = {{ max: parseFloat(ma.innerText)||0, stock: sch, used: 0 }};
    }}
}});

        // 2. Calcular ocupación por polígono (Tabla de abajo)
        document.querySelectorAll('#polys-' + tabId + ' .poligono-bloque').forEach(bl => {{
            let vT = parseFloat(bl.querySelector('.v-total-val').innerText) || 0, vA = 0;
            let vCalcEl = bl.querySelector('.v-calculado-total'); 


           bl.querySelectorAll('.calc-row').forEach(r => {{
                let s = r.querySelector('.s-type').value, u = parseInt(r.querySelector('.u-manual').innerText) || 0, sp = r.querySelector('.spr-real-val');
                
                // Diccionario interno de mínimos oficiales para el freno operativo
                const minimosFlota = {{
                    "Moto - 3h": 25, "Car - 3h": 25, "Car - 5h": 25, "Car - 5h Extendida": 25,
                    "Small Van SDD": 70, "Large Van SDD": 80, "Car Newbie": 40, "Car - 8h": 70
                }};

                if(s !== "SELECCIONAR..." && fleet[s]) {{
                    if(!editedRowsPlan.has(r)) sp.innerText = fleet[s].max; 
                    fleet[s].used += u; 
                    
                    let sprActual = parseFloat(sp.innerText) || 0;
                    vA += (u * sprActual);
                    sp.style.fontWeight = "bold";

                    // 🔥 CANDADO DE SEGURIDAD: Validar si hay unidades y el SPR cayó por debajo del mínimo
                    if (u > 0 && minimosFlota[s] && sprActual < minimosFlota[s]) {{
                        sp.style.setProperty("background-color", "#ffcccc", "important"); // Alerta roja
                        sp.style.setProperty("color", "#cc0000", "important");
                        sp.title = `⚠️ Operación inválida: El mínimo para ${{s}} es de ${{minimosFlota[s]}} paquetes.`;
                    }} else {{
                        // Estilo normal de cálculo
                        sp.style.setProperty("background-color", "#FFFFFF");
                        sp.style.setProperty("color", "#008B8B");
                        sp.title = "";
                    }}
                }} else {{
                    sp.style.color = "#969696"; 
                    sp.style.fontWeight = "normal";   
                    sp.style.setProperty("background-color", "#FFFFFF");
                    sp.title = "";
                }}
            }});



            vCalcEl.innerText = Math.round(vA);
            vCalcEl.style.background = "white";
            let d = bl.querySelector('.p-diff');

            if (vT === 0) {{
                d.innerText = "VACÍO"; d.style.background = "none"; vCalcEl.style.color = "#d32f2f";
            }} else {{
                let diffVal = Math.round(vA);
                if (diffVal === Math.round(vT)) {{
                    d.innerText = "OK"; d.style.background = "#3CB371"; vCalcEl.style.color = "#20B2AA";
                }} else if (vA > vT) {{
                    d.innerText = "EXCESO: " + Math.round(vA - vT); d.style.background = "#f5bf62"; vCalcEl.style.color = "#d32f2f";
                }} else {{
                    d.innerText = "FALTAN: " + Math.round(vT - vA); d.style.background = "#fa4343"; vCalcEl.style.color = "#d32f2f";
                }}
            }}
        }});

        // 3. REPLICAR NEGATIVOS EN TODAS LAS PESTAÑAS (SDE, C1, C2, PREC)
        document.querySelectorAll('#body-' + tabId + ' tr').forEach(row => {{
            let n = row.querySelector('.edit-name').innerText.trim();
            if(fleet[n]) {{
                let diff = fleet[n].stock - fleet[n].used;
                console.log("Diferencia calculada:", diff);
                let cL = row.querySelector('.f-left');
                
                // Regla universal para Car 3h, 5h, 8h y Crowd
                let esFlexible = n.toUpperCase().includes('CAR') || n.toUpperCase().includes('CROWD') || n.toUpperCase().includes('H');


                console.log("Diferencia calculada:", diff);
                cL.innerText = diff;
                
                // Color Rojo si es negativo
                if (diff < 0) {{
                    cL.style.color = "red"; cL.style.fontWeight = "bold"; cL.style.background = "transparent";
                }} else if (diff === 0 && fleet[n].stock > 0) {{
                    cL.style.color = "white"; cL.style.background = "#d32f2f";
                }} else {{
                    cL.style.color = "black"; cL.style.background = "transparent"; cL.style.fontWeight = "normal";
                }}
            }}
        }});

       // 4. FILTRAR LISTA SIN ROMPER SCHEDULE (CON CANDADO IXTAPALUCA INTEGRADO)
        document.querySelectorAll('#polys-' + tabId + ' .poligono-bloque').forEach(bl => {{
            // Capturamos el nombre del plan/polígono de este bloque específico
            let nombrePoligono = bl.querySelector('tbody tr.calc-row td[rowspan]')?.innerText.trim() || "";

            bl.querySelectorAll('.s-type').forEach(s => {{
                let cur = s.value; 
                let opt = '<option>SELECCIONAR...</option>';
                Object.keys(fleet).forEach(k => {{ 
                    if (fleet[k].stock > 0) {{
                        let disp = (fleet[k].stock - fleet[k].used > 0);
                        let flexible = k.toUpperCase().includes('CAR') || k.toUpperCase().includes('H');
                        if (disp || k === cur || flexible) {{
                            opt += `<option value="${{k}}">${{k}}</option>`;
                        }}
                    }}
                }});
                
                s.innerHTML = opt; 
                s.value = cur; 

                // 🚨 CANDADO EN EL POLÍGONO: REGLA DE ZONA ROJA IXTAPALUCA VALLE CHALCO
                if (nombrePoligono.toUpperCase().includes("IXTAPALUCA")) {{
                    let unidadTxt = cur.toUpperCase();
                    
                    // Si ya seleccionó algo, no es el valor por defecto y NO incluye la palabra "CAR"
                    if (unidadTxt !== "SELECCIONAR..." && unidadTxt !== "" && !unidadTxt.includes("CAR")) {{
                        
                        // Capturamos si ya tenía el color de advertencia puesto para no duplicar la alerta
                        let yaTieneAlerta = (s.style.backgroundColor === "rgb(255, 204, 204)" || s.style.backgroundColor === "#ffcccc");

                        // 1. Aplicamos el diseño visual de advertencia al selector
                        s.style.setProperty("background-color", "#ffcccc", "important");
                        s.style.setProperty("color", "#8b0000", "important");
                        s.style.setProperty("font-weight", "bold", "important");
                        
                        // 2. 🔥 LANZA LA ALERTA FLOTANTE SÓLO LA PRIMERA VEZ (Evita bucles infinitos)
                        if (!yaTieneAlerta) {{
                            showAlert("🚨 ⚠️⚠️ ¡PELIGRO! EN IXTAPALUCA VALLE-CHALCO SOLO SE PERMITEN UNIDADES TIPO CAR. ⚠️⚠️🚨");
                        }}
                    }} else {{
                        // Si cambia a un "CAR" o vuelve a "SELECCIONAR...", se limpian los estilos por completo
                        s.style.removeProperty("background-color");
                        s.style.removeProperty("color");
                        s.style.removeProperty("font-weight");
                    }}
                }}
            }});
        }});

updateFleetFloat();

actualizarTotales();
    }}

    // --- ARREGLO PARA EL ENTER EN ALERTAS ROJAS ---
    document.addEventListener('keydown', function(event) {{ 
        if (event.key === 'Enter') {{
            // Busca cualquier div de alerta o mensaje de error y lo cierra/limpia
            let alerta = document.querySelector('.alerta-roja, .p-diff'); 
            if (alerta && alerta.innerText.includes('EXCESO')) {{
                // Si tienes una función específica para cerrar, llámala aquí
                // O simplemente quita el foco para que no bloquee
                document.activeElement.blur();
            }}
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

        // 2. Filtrar los bloques, celdas y filas de ESTADO de los Polígonos (Izquierda)
        document.querySelectorAll('#polys-' + currentTab + ' .poligono-bloque').forEach(bl => {{
            let filasVisiblesEnBloque = 0;
            let vTotal = parseFloat(bl.querySelector('.v-total-val').innerText) || 0;

            // Buscamos todas las filas de asignación en la tabla del polígono
            bl.querySelectorAll('tbody tr.calc-row').forEach(r => {{
                let uManual = parseInt(r.querySelector('.u-manual').innerText) || 0;
                let sTypeSelect = r.querySelector('.s-type');
                let sType = sTypeSelect ? sTypeSelect.value : "SELECCIONAR...";

                if (onlyActive) {{
                    // Si está en "ACTIVAS", ocultamos las filas vacías y sin selección
                    if (uManual === 0 && (sType === "SELECCIONAR..." || sType === "")) {{
                        r.style.display = 'none';
                    }} else {{
                        r.style.display = '';
                        filasVisiblesEnBloque++;
                    }}
                }} else {{
                    // Si es "TODAS", mostramos todo el desglose original
                    r.style.display = '';
                    filasVisiblesEnBloque++;
                }}
            }});

            // 🔥 NUEVO: Ocultar o mostrar la fila de ESTADO (la última fila del tbody)
            // Buscamos la fila que no tiene la clase 'calc-row' (que es tu fila de ESTADO)
            let filaEstado = bl.querySelector('tbody tr:not(.calc-row)');
            if (filaEstado) {{
                // Si está en ACTIVAS se oculta por completo, si está en TODAS se vuelve a mostrar
                filaEstado.style.display = onlyActive ? 'none' : '';
            }}

            // CORRECCIÓN REFORZADA CON setAttribute Y rowSpan
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

            // Control visual del bloque completo (Polígono)
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

        if (!herramientasVisibles) {{
            boton.innerHTML = '🛠️ MOSTRAR UTILERÍAS';
            boton.style.background = 'linear-gradient(180deg, #ffffff 0%, #D3D3D3 100%)'; 
            boton.style.boxShadow = '0 3px 0 #D3D3D3';
            boton.style.color = '#808080';
        }} else {{
            boton.innerHTML = '❌ OCULTAR UTILERÍAS';
            boton.style.background = 'linear-gradient(180deg, #555 0%, #333 100%)'; 
            boton.style.boxShadow = '0 3px 0 #111';
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

    // =========================================
    // 1. LEER FLOTA DISPONIBLE
    // =========================================

    let fleet = [];

    document.querySelectorAll('#body-' + currentTab + ' tr').forEach(row => {{

        let nombre =
            row.querySelector('.edit-name')?.innerText.trim();

        let sprMax =
            parseFloat(
                row.querySelector('.edit-spr-max')?.innerText
            ) || 0;

        let stock =
            parseInt(
                row.querySelector('.f-stock')?.innerText
            ) || 0;

        if (
            nombre &&
            nombre !== "IGNORAR" &&
            stock > 0
        ) {{

            fleet.push({{
                nombre: nombre,
                spr: sprMax,
                stock: stock,
                restante: stock
            }});
        }}
    }});

    // =========================================
    // 2. DESCONTAR MANUALES EXISTENTES
    // =========================================

    document.querySelectorAll(
        '#polys-' + currentTab + ' .calc-row'
    ).forEach(r => {{

        let tipo =
            r.querySelector('.s-type')?.value;

        let unidades =
            parseInt(
                r.querySelector('.u-manual')?.innerText
            ) || 0;

        if (
            tipo &&
            tipo !== "SELECCIONAR..." &&
            unidades > 0
        ) {{

            let unidadReal =
                fleet.find(f => f.nombre === tipo);

            if (unidadReal) {{
                unidadReal.restante -= unidades;
            }}
        }}
    }});

    // =========================================
    // 3. PRIORIDAD MAYOR SPR
    // =========================================

    fleet.sort((a, b) => b.spr - a.spr);

    // =========================================
    // 4. OBTENER POLÍGONOS
    // =========================================

    let bloques = Array.from(
        document.querySelectorAll(
            '#polys-' + currentTab + ' .poligono-bloque'
        )
    );

    let polys = [];

    bloques.forEach(bl => {{

        let volumen =
            parseFloat(
                bl.querySelector('.v-total-val')?.innerText
            ) || 0;

        if (volumen > 0) {{

            polys.push({{
                bloque: bl,
                volumen: volumen
            }});
        }}
    }});

    // =========================================
    // 5. PRIORIDAD MAYOR VOLUMEN
    // =========================================

    polys.sort((a, b) => b.volumen - a.volumen);

    // =========================================
    // 6. AUTO-ASIGNACIÓN
    // =========================================

    polys.forEach(poly => {{

        let bloque = poly.bloque;

        let objetivo =
            parseFloat(
                bloque.querySelector('.v-total-val')?.innerText
            ) || 0;

        // =====================================
        // RESTAR LO YA MANUALMENTE ASIGNADO
        // =====================================

        let yaAsignado = 0;

        bloque.querySelectorAll('.calc-row').forEach(r => {{

            let unidades =
                parseInt(
                    r.querySelector('.u-manual')?.innerText
                ) || 0;

            let spr =
                parseFloat(
                    r.querySelector('.spr-real-val')?.innerText
                ) || 0;

            yaAsignado += (unidades * spr);
        }});

        let restante = objetivo - yaAsignado;

        if (restante <= 0) return;

        let filas = Array.from(
            bloque.querySelectorAll('.calc-row')
        );

        for (let fila of filas) {{

            // =================================
            // RESPETAR FILAS MANUALES
            // =================================

            let yaTieneUnidad =
                parseInt(
                    fila.querySelector('.u-manual')?.innerText
                ) > 0;

            let yaTieneTipo =
                fila.querySelector('.s-type')?.value &&
                fila.querySelector('.s-type')?.value !== "SELECCIONAR...";

            if (yaTieneUnidad || yaTieneTipo) {{
                continue;
            }}

            if (restante <= 0) break;

            // =================================
            // BUSCAR MEJOR UNIDAD DISPONIBLE
            // =================================

            let unidad =
                fleet.find(f => f.restante > 0);

            if (!unidad) break;

            // =================================
            // CALCULAR NECESARIAS
            // =================================

            let necesarias =
                Math.ceil(restante / unidad.spr);

            let usar =
                Math.min(
                    necesarias,
                    unidad.restante
                );

            if (usar <= 0) continue;

            // =================================
            // ASIGNAR
            // =================================

            let select =
                fila.querySelector('.s-type');

            select.value = unidad.nombre;

            fila.querySelector('.u-manual').innerText =
                usar;

            fila.querySelector('.spr-real-val').innerText =
                unidad.spr;

            unidad.restante -= usar;

            restante -= (usar * unidad.spr);

            editedRowsPlan.add(fila);
        }}
    }});

    // =========================================
    // 7. RECALCULAR
    // =========================================

    recalc();
}}
    

// =========================
// TOTALES FINALES
// =========================

function actualizarTotales() {{
        let totalNoCar = 0;
        let totalCarReal = 0;

        let tabId = (currentTab === 'C1') ? '2' : currentTab;

        // Sumar datos desde la tabla de disponibilidad activa
        document.querySelectorAll('#body-' + tabId + ' tr').forEach(row => {{
            let name = row.querySelector('.edit-name').innerText.trim().toUpperCase();
            let left = parseInt(row.querySelector('.f-left').innerText) || 0;
            let sch = parseInt(row.querySelector('.f-stock').innerText) || 0;
            let asig = sch - left;

            if (name && name !== "IGNORAR" && name !== "NUEVA UNIDAD") {{
                if (name.includes("CAR") || name.includes("HÍBRIDA")) {{
                    totalCarReal += asig;
                }} else {{
                    totalNoCar += asig;
                }}
            }}
        }});

        // Pintar en los tfoots correspondientes de la pestaña activa
        let noCarCell = document.getElementById('total-no-car-' + tabId) || document.getElementById('total-no-car');
        let carCell = document.getElementById('total-car-real-' + tabId) || document.getElementById('total-car-real');

        if (noCarCell) noCarCell.innerText = totalNoCar; 
        if (carCell) carCell.innerText = totalCarReal;
    }}


// --- AQUÍ PEGA LA FUNCIÓN NUEVA ---
    function updateSelectColor(selectElement) {{
        if (selectElement.value === "") {{
            selectElement.style.color = "#A9A9A9"; // Gris
        }} else {{
            selectElement.style.color = "#000000"; // Negro
        }}
    }}



aplicarPerfil();

    
    recalc();
</script>
</body>
</html>
"""

html(app_html, height=1200, scrolling=True)



# =====================================================================
# MÓDULO INDEPENDIENTE: CONSULTA DE SUMMARY (ORH / % OCUPACIÓN)
# =====================================================================
st.write("---")
st.markdown("### 📋 CONSULTA DE SUMMARY (ORH / % )")

DATA_PERFILES_DIARIOS = {
    "LUNES": {
        "C1 / C2": {"Car - 8h": {"orh": 99, "disp": 80}, "SV": {"orh": 91, "disp": 95}},
        "PREC SMX5": {"Large Van SDD": {"orh": 487, "disp": 70}, "Small Van SDD": {"orh": 487, "disp": 70}, "Car Newbie": {"orh": 360, "disp": 83}, "Car - 8h": {"orh": 360, "disp": 66}},
        "PREC SMX2": {"Small Van SDD": {"orh": 487, "disp": 70}, "Car - 8h": {"orh": 360, "disp": 66}, "Car Zona Extendida": {"orh": 360, "disp": 83}}
    },
    "MARTES": {
        "C1 / C2": {"CAR 8H": {"orh": 90, "disp": 94}},
        "PREC SMX5": {"Large Van SDD": {"orh": 487, "disp": 70}, "Small Van SDD": {"orh": 487, "disp": 70}, "Car Newbie": {"orh": 360, "disp": 83}, "Car - 8h": {"orh": 360, "disp": 66}},
        "PREC SMX2": {"Small Van SDD": {"orh": 487, "disp": 70}, "Car - 8h": {"orh": 360, "disp": 66}, "Car Zona Extendida": {"orh": 360, "disp": 83}}
    },
    "MIÉRCOLES": {
        "C1 / C2": {"CAR 8H": {"orh": 89, "disp": 93}},
        "PREC SMX5": {"Large Van SDD": {"orh": 487, "disp": 70}, "Small Van SDD": {"orh": 487, "disp": 70}, "Car Newbie": {"orh": 360, "disp": 83}, "Car - 8h": {"orh": 360, "disp": 66}},
        "PREC SMX2": {"Small Van SDD": {"orh": 487, "disp": 70}, "Car - 8h": {"orh": 360, "disp": 66}, "Car Zona Extendida": {"orh": 360, "disp": 83}}
    },
    "JUEVES": {
        "C1 / C2": {"CAR 8H": {"orh": 91, "disp": 95}},
        "PREC SMX5": {"Large Van SDD": {"orh": 487, "disp": 70}, "Small Van SDD": {"orh": 487, "disp": 70}, "Car Newbie": {"orh": 360, "disp": 83}, "Car - 8h": {"orh": 360, "disp": 66}},
        "PREC SMX2": {"Small Van SDD": {"orh": 487, "disp": 70}, "Car - 8h": {"orh": 360, "disp": 66}, "Car Zona Extendida": {"orh": 360, "disp": 83}}
    },
    "VIERNES": {
        "C1 / C2": {"CAR 8H": {"orh": 93, "disp": 97}},
        "PREC SMX5": {"Large Van SDD": {"orh": 487, "disp": 70}, "Small Van SDD": {"orh": 487, "disp": 70}, "Car Newbie": {"orh": 360, "disp": 83}, "Car - 8h": {"orh": 360, "disp": 66}},
        "PREC SMX2": {"Small Van SDD": {"orh": 487, "disp": 70}, "Car - 8h": {"orh": 360, "disp": 66}, "Car Zona Extendida": {"orh": 360, "disp": 83}}
    },
    "SÁBADO": {
        "C1 / C2": {"CAR 8H": {"orh": 85, "disp": 89}},
        "PREC SMX5": {"Large Van SDD": {"orh": 487, "disp": 70}, "Small Van SDD": {"orh": 487, "disp": 70}, "Car Newbie": {"orh": 360, "disp": 83}, "Car - 8h": {"orh": 360, "disp": 66}},
        "PREC SMX2": {"Small Van SDD": {"orh": 487, "disp": 70}, "Car - 8h": {"orh": 360, "disp": 66}, "Car Zona Extendida": {"orh": 360, "disp": 83}}
    },
    "DOMINGO": {
        "C1 / C2": {"CAR 8H": {"orh": 80, "disp": 85}},
        "PREC SMX5": {"Large Van SDD": {"orh": 487, "disp": 70}, "Small Van SDD": {"orh": 487, "disp": 70}, "Car Newbie": {"orh": 360, "disp": 83}, "Car - 8h": {"orh": 360, "disp": 66}},
        "PREC SMX2": {"Small Van SDD": {"orh": 487, "disp": 70}, "Car - 8h": {"orh": 360, "disp": 66}, "Car Zona Extendida": {"orh": 360, "disp": 83}}
    }
}

dia_seleccionado = st.selectbox("📅 SELECCIONA EL DÍA OPERATIVO", list(DATA_PERFILES_DIARIOS.keys()))

col1, col2, col3 = st.columns(3)

# --- ESTILO COMPACTO ---
estilo_tabla = """
<style>
    .comp-table { width: 100%; border-collapse: collapse; font-size: 14px; margin-top: 5px; }
    .comp-table th { background: #333; color: white; padding: 6px; text-align: left; font-size: 13px;}
    .comp-table td { padding: 6px; border-bottom: 1px solid #ddd; background: #fafafa; }
/* Estilo para los nombres de las categorías */
    .cat-header {
        background-color: #111; 
        color: #fff; 
        padding: 8px; 
        font-weight: bold; 
        text-align: center; 
        font-size: 14px; /* Títulos más grandes */
        border-radius: 4px;
    }  
</style>
"""
st.markdown(estilo_tabla, unsafe_allow_html=True)

# Función auxiliar para generar la tablita pequeña
def tabla_compacta(datos_cat):
    filas = "".join([f"<tr><td>{u}</td><td>{d['orh']}</td><td>{d['disp']}%</td></tr>" for u, d in datos_cat.items()])
    return f"<table class='comp-table'><tr><th>U</th><th>ORH</th><th>%</th></tr>{filas}</table>"

# --- RENDERIZADO COMPACTO EN COLUMNAS ---
with col1:
    st.markdown("<div style='background-color:#111; color:#fff; padding:4px; font-weight:bold; text-align:center;'>C1 / C2</div>", unsafe_allow_html=True)
    st.markdown(tabla_compacta(DATA_PERFILES_DIARIOS[dia_seleccionado]["C1 / C2"]), unsafe_allow_html=True)

with col2:
    st.markdown("<div style='background-color:#444; color:#fff; padding:4px; font-weight:bold; text-align:center;'>PREC SMX5</div>", unsafe_allow_html=True)
    st.markdown(tabla_compacta(DATA_PERFILES_DIARIOS[dia_seleccionado]["PREC SMX5"]), unsafe_allow_html=True)

with col3:
    st.markdown("<div style='background-color:#008080; color:#fff; padding:4px; font-weight:bold; text-align:center;'>PREC SMX2</div>", unsafe_allow_html=True)
    st.markdown(tabla_compacta(DATA_PERFILES_DIARIOS[dia_seleccionado]["PREC SMX2"]), unsafe_allow_html=True)







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
            - 👉 Vol aprox. 800 / en peak puede aumentar hasta 1600<br>
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
