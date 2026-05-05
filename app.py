import streamlit as st
from streamlit.components.v1 import html

# Configuración de página para que use todo el ancho
st.set_page_config(page_title="Monitor Logístico VP04", layout="wide")

# Eliminamos los márgenes de Streamlit para que no se vea "encerrado"
st.markdown("""
    <style>
    .block-container {padding: 0rem !important;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- DEFINICIÓN DE DATOS (Parte 1) ---
unidades_SDE = {"CROWD 5 HRS": [25, 28], "CROWD 5 HRS EXTENDIDA": [25, 28], "CROWD 3 HRS": [25, 28], "MOTO 3 HRS": [25, 28]}
unidades_SD = {"MOTO 3 HRS": [25, 25], "MOTO NEWBIE": [20, 22], "CROWD 5 HRS / SMALL VAN": [35, 37]}
unidades_C1 = {
    "RENTAL ELEC LARGE VAN": [120, 120], "RENTAL ELEC SMALL VAN": [120, 120],
    "RENTAL LARGE VAN": [120, 120], "RENTAL SMALL VAN": [120, 120],
    "LARGE VAN VAR(MLP)": [100, 100], "SMALL VAN VAR(MLP)":[80, 80],
    "CAR MLP": [50, 50], "MOTO 3 HRS": [28, 28], "CROWD NEWBIE 3 hrs": [30, 30],
    "CROWD EXTRA 8 HRS": [80, 85], "CROWD 5 HRS": [60, 60]
}
unidades_C2 = {
    "RENTAL ELEC LARGE VAN": [120, 120], "RENTAL ELEC SMALL VAN": [120, 120],
    "RENTAL LARGE VAN": [120, 120], "RENTAL SMALL VAN": [120, 120],
    "LARGE VAN HÍBRIDA": [100, 100], "LARGE VAN VAR(MLP)": [100, 100],
    "SMALL VAN VAR(MLP)":[80, 80], "CAR MLP": [50, 50], "MOTO 3 HRS": [28, 28],
    "CROWD NEWBIE 3 hrs": [30, 30], "CROWD EXTRA 8 HRS": [80, 85], "CROWD 5 HRS": [60, 60]
}

# --- FUNCIONES GENERADORAS (Parte 1) ---
def gen_master_rows(data_dict, table_id):
    rows = ""
    items = list(data_dict.items())
    for i in range(15):
        name, spr = (items[i][0], items[i][1]) if i < len(items) else ("NUEVA UNIDAD", [0, 0])
        style = "color: #555; background: #ebebeb;" if i < len(items) else "color: #C0C0C0; background: #fcfcfc;"
        rows += f'''<tr data-table="{table_id}" class="master-row">
            <td contenteditable="true" class="edit-name" oninput="recalc()" style="{style} font-weight: bold; text-align: left; padding-left: 10px;">{name}</td>
            <td contenteditable="true" class="edit-spr-min" oninput="recalc()" style="{style} font-weight: bold; text-align: center;">{spr[0]}</td>
            <td contenteditable="true" class="edit-spr-max" oninput="recalc()" style="{style} font-weight: bold; text-align: center;">{spr[1]}</td>
            <td contenteditable="true" class="edit-orh" style="{style} font-weight: normal; text-align: center;">480</td>
            <td contenteditable="true" class="f-stock" style="{style} font-weight: bold; text-align: center;" oninput="recalc()">0</td>
            <td class="f-left" style="{style} font-weight: bold; text-align: center;">0</td>
        </tr>'''
    return rows

def gen_poligonos():
    polys = ""
    btn_s = "cursor:pointer; border:none; background:rgba(0,0,0,0.05); color:#696969; font-weight:bold; width:18px; height:18px; border-radius:3px; margin:0 2px; line-height:1;"
    fila_inner = f'''<tr class="calc-row">
        <td class="u-manual-cell" style="background: #e3defa; text-align: center; white-space: nowrap;">
            <button style="{btn_s}" onclick="stepVal(this, -1, 'u')">-</button>
            <span contenteditable="true" class="u-manual" oninput="manualEdit(this)" style="color: #000000; font-weight: bold;">0</span>
            <button style="{btn_s}" onclick="stepVal(this, 1, 'u')">+</button>
        </td>
        <td class="spr-real-cell" style="background: #def3ed; text-align: center; white-space: nowrap;">
            <button style="{btn_s}" onclick="stepVal(this, -1, 's')">-</button>
            <span contenteditable="true" class="spr-real-val" oninput="manualEdit(this)" style="color: #000000; font-weight: bold;">0</span>
            <button style="{btn_s}" onclick="stepVal(this, 1, 's')">+</button>
        </td>
        <td><select class="s-type" onchange="resetRow(this)"><option>SELECCIONAR...</option></select></td>
        <td style="text-align: center;"><input type="checkbox" class="ok-check" onclick="toggleRowPlan(this)"></td>
    </tr>'''
    for i in range(1, 11):
        polys += f'''<div class="poligono-bloque" style="margin-bottom: 15px;">
            <table class="meli-table tabla-planes">
                <thead>
                    <tr><th class="header-poly">PLAN {i}</th><th class="header-poly">VOL. TOTAL</th><th class="header-poly"style="width: 80px;"># ASIGNADAS</th><th class="header-poly"style="width: 50px;">SPR REAL</th><th class="header-poly">TIPO DE UNIDAD</th><th class="header-poly" style="width:35px;">OK</th></tr>
                </thead>
                <tbody>
                    <tr class="calc-row">
                        <td rowspan="5" contenteditable="true" class="v-total" style="width:100px; font-weight:bold; color: #000; background: #D3D3D3; border: 1px solid #808080; text-align: center;">PLAN {i}</td>
                        <td rowspan="5" contenteditable="true" class="v-total-val" oninput="recalc()" style="width:70px; color: #20B2AA; font-weight: bold; font-size: 16px; border: 1px solid #808080; text-align: center;">0</td>
                        <td class="u-manual-cell" style="background: #e3defa; text-align: center; white-space: nowrap;">
                            <button style="{btn_s}" onclick="stepVal(this, -1, 'u')">-</button>
                            <span contenteditable="true" class="u-manual" oninput="manualEdit(this)">0</span>
                            <button style="{btn_s}" onclick="stepVal(this, 1, 'u')">+</button>
                        </td>
                        <td class="spr-real-cell" style="background: #def3ed; text-align: center; white-space: nowrap;">
                            <button style="{btn_s}" onclick="stepVal(this, -1, 's')">-</button>
                            <span contenteditable="true" class="spr-real-val" oninput="manualEdit(this)" style="font-weight: bold;">0</span>
                            <button style="{btn_s}" onclick="stepVal(this, 1, 's')">+</button>
                        </td>
                        <td><select class="s-type" onchange="resetRow(this)"><option>SELECCIONAR...</option></select></td>
                        <td style="text-align: center;"><input type="checkbox" class="ok-check" onclick="toggleRowPlan(this)"></td>
                    </tr>
                    {fila_inner*4}
                    <tr><td colspan="2" style="text-align:center; font-weight:bold; background:#f8f9fa; border: 1px solid #808080;">ESTADO:</td><td class="v-calculado-total" style="font-weight: bold; font-size: 16px; color: #d32f2f; border: 1px solid #808080; text-align: center;">0</td><td class="p-diff" colspan="3" style="font-size: 11px; font-weight: bold; border: 1px solid #808080; text-align: center;">VACÍO</td></tr>
                </tbody>
            </table>
        </div>'''
    return polys

# --- CRONÓMETRO HTML (Parte 1) ---
crono_html = """
<div id="crono-wrapper" style="position: fixed; top: 10px; right: 20px; z-index: 10000; background: #1a1a1a; padding: 12px 15px; border-radius: 10px; font-family: 'Segoe UI', sans-serif; color: white; width: 180px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); border: 1px solid #333;">
    <div style="margin-bottom: 8px; border-bottom: 1px solid #444; padding-bottom: 4px; display: flex; justify-content: space-between; align-items: center;">
        <span style="color: #888; font-size: 10px; font-weight: bold;">HORA ACTUAL</span>
        <div id="reloj-f" style="font-size: 13px; color: #00d4ff; font-family: monospace;">00:00:00</div>
    </div>
    <div style="text-align: center;">
        <div id="display-f" style="font-size: 24px; margin: 5px 0; font-family: monospace; font-weight: bold;">00:00:00.0</div>
        <div style="display: flex; gap: 6px; justify-content: center;">
            <button id="start-f" style="background: #28a745; color: white; border: none; padding: 4px 10px; border-radius: 4px; cursor: pointer;">▶</button>
            <button id="pause-f" style="background: #ffc107; border: none; padding: 4px 10px; border-radius: 4px; cursor: pointer;">⏸</button>
            <button id="reset-f" style="background: #dc3545; color: white; border: none; padding: 4px 10px; border-radius: 4px; cursor: pointer;">🔄</button>
        </div>
    </div>
</div>
"""

# --- LAYOUT Y ESTILOS (Parte 2) ---
# Aquí integramos todo tu diseño 3D y la lógica de control.
full_app_html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        /* Pegar aquí todos los estilos de la PARTE 2 */
        body {{ font-family: sans-serif; background: #f5f7f9; padding: 20px; }}
        .btn-calc {{ border: 1px solid #ccc; border-radius: 8px; background: linear-gradient(180deg, #ffffff 0%, #f0f4f8 100%); box-shadow: 2px 2px 5px rgba(0,0,0,0.2), inset 1px 1px 1px white !important; transition: 0.1s; cursor: pointer; font-weight: bold; padding: 10px; }}
        #calc_container {{ box-shadow: 8px 8px 16px #acacac, -8px -8px 16px #ffffff !important; transform: perspective(1000px) rotateX(2deg); transition: all 0.3s ease; }}
        .meli-table {{ border-collapse: separate !important; border-spacing: 0; width: 100%; font-size: 11px; margin-bottom: 20px; border-radius: 11px !important; overflow: hidden !important; box-shadow: 0 4px 8px rgba(0,0,0,0.05); border: 2px solid #ccc !important; }}
        .header-poly {{ background: linear-gradient(180deg, #888888 0%, #696969 100%) !important; color: white; padding: 8px; text-align: center; }}
        .header-flota {{ background: linear-gradient(180deg, #333333 0%, #000000 100%) !important; color: white; padding: 8px; text-align: center; }}
        .tab-btn {{ padding: 8px 15px; cursor: pointer; border: none; background: #e0e0e0; border-radius: 8px 8px 0 0; font-weight: bold; margin-right: 2px; position: relative; }}
        .tab-btn.active {{ background: #000000 !important; color: white !important; top: 2px; box-shadow: inset 2px 2px 6px rgba(0,0,0,0.5) !important; }}
        .conv-container {{ background: linear-gradient(145deg, #e2dcf5, #d1c9f0) !important; border-radius: 15px; padding: 15px; margin-bottom: 20px; text-align: center; border: 2px solid #d1d1d1 !important; }}
        .section-divider {{ background: #696969; color: white; padding: 10px; border-radius: 8px; font-weight: bold; margin-bottom: 15px; text-align: center; letter-spacing: 2px; }}
        .main-header-flota {{ background: linear-gradient(90deg, #000000, #444444); color: white; padding: 10px; border-radius: 8px; font-weight: bold; margin-bottom: 10px; }}
        /* Estilos adicionales de celdas */
        .u-manual, .spr-real-val {{ margin: 0 10px !important; display: inline-block; min-width: 20px; text-align: center; font-weight: bold; }}
    </style>
</head>
<body>

{crono_html}

<div style="display: flex; gap: 20px; align-items: flex-start;">
    <!-- COLUMNA IZQUIERDA: PLANES -->
    <div style="flex: 1;">
        <div class="section-divider">📋 PLANES GENERADOS</div>
        <div id="polys-2" class="poly-tab-content">{gen_poligonos()}</div>
        <div id="polys-3" class="poly-tab-content" style="display:none;">{gen_poligonos()}</div>
        <div id="polys-1" class="poly-tab-content" style="display:none;">{gen_poligonos()}</div>
        <div id="polys-4" class="poly-tab-content" style="display:none;">{gen_poligonos()}</div>
    </div>

    <!-- COLUMNA DERECHA: FLOTA Y CALC -->
    <div style="width: 450px; position: sticky; top: 10px;">
        <div class="main-header-flota">🚚 🚚 DISPONIBILIDAD DE FLOTA 🚚 🚚</div>
        <div style="display: flex; justify-content: space-between;">
            <div>
                <button class="tab-btn active" onclick="showTab(2, this)">C1</button>
                <button class="tab-btn" onclick="showTab(3, this)">C2</button>
                <button class="tab-btn" onclick="showTab(1, this)">SD</button>
                <button class="tab-btn" onclick="showTab(4, this)">SDE</button>
            </div>
            <div style="margin-bottom: 5px;">
                <button onclick="filterFlota(true)" style="background:#C0C0C0; padding: 4px 8px; border-radius: 4px; cursor: pointer; font-weight:bold;">ACTIVAS</button>
                <button onclick="filterFlota(false)" style="background:#20B2AA; padding: 4px 8px; border-radius: 4px; cursor: pointer; color: white; font-weight:bold;">TODAS</button>
            </div>
        </div>
        
        <div class="master-container" style="background: white; padding: 15px; border-radius: 12px; border: 1px solid #ccc;">
            <div id="tab-flota-2" class="tab-content">
                <table class="meli-table">
                    <thead><tr><th class="header-flota" rowspan="2">UNIDADES (C1)</th><th class="header-flota" colspan="2">SPR</th><th class="header-flota" rowspan="2">ORH</th><th class="header-flota" rowspan="2">SCHED</th><th class="header-flota" rowspan="2">ME QUEDAN</th></tr><tr><th class="header-flota">min</th><th class="header-flota">max</th></tr></thead>
                    <tbody id="body-2">{gen_master_rows(unidades_C1, 2)}</tbody>
                </table>
            </div>
            <div id="tab-flota-3" class="tab-content" style="display:none;">
                <table class="meli-table"><tbody id="body-3">{gen_master_rows(unidades_C2, 3)}</tbody></table>
            </div>
            <div id="tab-flota-1" class="tab-content" style="display:none;">
                <table class="meli-table"><tbody id="body-1">{gen_master_rows(unidades_SD, 1)}</tbody></table>
            </div>
            <div id="tab-flota-4" class="tab-content" style="display:none;">
                <table class="meli-table"><tbody id="body-4">{gen_master_rows(unidades_SDE, 4)}</tbody></table>
            </div>
        </div>

        <div class="conv-container">
            <div style="font-size: 10px; font-weight: bold; color: #4e3396; margin-bottom: 5px;">🕑 CONVERTIDOR DE TIEMPO</div>
            <input type="number" id="minInp" oninput="convertirMinutos()" placeholder="Min" style="width: 80px; text-align: center; font-weight: bold;">
            <span id="resConv" style="margin-left: 10px; font-size: 18px; font-weight: bold; color: #ac40de;">0h 0m</span>
        </div>

        <div id="calc_container" style="background: linear-gradient(145deg, #22c5bc, #1da29b); border-radius: 25px; padding: 20px; outline: none;" tabindex="0">
            <div style="background: #fffacd; border-radius: 10px; padding: 10px; text-align: right; margin-bottom: 15px; box-shadow: inset 2px 2px 5px rgba(0,0,0,0.1);">
                <div id="h_calc" style="font-size:12px; color:#666;">0</div>
                <div id="r_calc" style="font-size: 24px; font-weight: bold; color: black;">0</div>
            </div>
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px;">
                <button onclick="cl()" class="btn-calc" style="grid-column: span 2;">AC</button>
                <button onclick="del()" class="btn-calc">⌫</button><button onclick="ao('/')" class="btn-calc">÷</button>
                <button onclick="an('7')" class="btn-calc">7</button><button onclick="an('8')" class="btn-calc">8</button><button onclick="an('9')" class="btn-calc">9</button><button onclick="ao('*')" class="btn-calc">×</button>
                <button onclick="an('4')" class="btn-calc">4</button><button onclick="an('5')" class="btn-calc">5</button><button onclick="an('6')" class="btn-calc">6</button><button onclick="ao('-')" class="btn-calc">-</button>
                <button onclick="an('1')" class="btn-calc">1</button><button onclick="an('2')" class="btn-calc">2</button><button onclick="an('3')" class="btn-calc">3</button><button onclick="ao('+')" class="btn-calc">+</button>
                <button onclick="an('0')" class="btn-calc" style="grid-column: span 2;">0</button>
                <button onclick="calc_eq()" class="btn-calc" style="background: #FF00FF; color:white;">=</button>
            </div>
        </div>
    </div>
</div>

<script>
    // --- LÓGICA DE CONTROL (Script unificado Parte 1 y 2) ---
    var currentTab = 2;
    var editedRows = new Set();
    
    function showTab(n, btn) {{
        currentTab = n;
        document.querySelectorAll('.tab-content, .poly-tab-content').forEach(el => el.style.display = 'none');
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.getElementById('tab-flota-'+n).style.display = 'block';
        document.getElementById('polys-'+n).style.display = 'block';
        btn.classList.add('active');
        recalc();
    }}

    // Aquí van todas las funciones de recalc, stepVal, calculadora y cronómetro
    // (Incluyendo la lógica de cronómetro de la parte 1)
    
    let st, et = 0, run = false;
    document.getElementById('start-f').onclick = () => {{ if(!run){{ run=true; st=Date.now()-et; timer=setInterval(()=>{{ et=Date.now()-st; document.getElementById('display-f').innerText=timeToString(et); }},100); }} }};
    document.getElementById('pause-f').onclick = () => {{ run=false; clearInterval(timer); }};
    document.getElementById('reset-f').onclick = () => {{ run=false; clearInterval(timer); et=0; document.getElementById('display-f').innerText="00:00:00.0"; }};
    function timeToString(t){{ let ms=Math.floor((t%1000)/100), s=Math.floor((t/1000)%60), m=Math.floor((t/60000)%60); return `${{m.toString().padStart(2,'0')}}:${{s.toString().padStart(2,'0')}}.${{ms}}`; }}
    setInterval(()=>{{ document.getElementById('reloj-f').innerText=new Date().toLocaleTimeString(); }}, 1000);

    // [Resto de funciones manualEdit, recalc, stepVal, etc. idénticas a tu Parte 2]
    {script.replace('<script>', '').replace('</script>', '')}
</script>
</body>
</html>
"""

# Mostramos el HTML en Streamlit con un alto suficiente para que no salgan barras de scroll internas
html(full_app_html, height=1600, scrolling=True)
