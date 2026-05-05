import streamlit as st
from streamlit.components.v1 import html

st.set_page_config(page_title="Monitor Logístico - Liliana García", layout="wide")

# CSS para ocultar elementos de Streamlit y forzar el diseño limpio
st.markdown("""
    <style>
    .block-container {padding: 0rem !important;}
    footer, #MainMenu, header {visibility: hidden;}
    body { background-color: #f5f7f9; }
    </style>
""", unsafe_allow_html=True)

# --- DATOS BASE (Sin cambios) ---
u_SDE = {"CROWD 5 HRS": [25, 28], "CROWD 5 HRS EXTENDIDA": [25, 28], "CROWD 3 HRS": [25, 28], "MOTO 3 HRS": [25, 28]}
u_SD = {"MOTO 3 HRS": [25, 25], "MOTO NEWBIE": [20, 22], "CROWD 5 HRS / SMALL VAN": [35, 37]}
u_C1 = {
    "RENTAL ELEC LARGE VAN": [120, 120], "RENTAL ELEC SMALL VAN": [120, 120], "RENTAL LARGE VAN": [120, 120], 
    "RENTAL SMALL VAN": [120, 120], "LARGE VAN VAR(MLP)": [100, 100], "SMALL VAN VAR(MLP)":[80, 80],
    "CAR MLP": [50, 50], "MOTO 3 HRS": [28, 28], "CROWD NEWBIE 3 hrs": [30, 30], "CROWD EXTRA 8 HRS": [80, 85], "CROWD 5 HRS": [60, 60]
}
u_C2 = u_C1.copy()
u_C2["LARGE VAN HÍBRIDA"] = [100, 100]

def gen_master_rows(data_dict, table_id):
    rows = ""
    items = list(data_dict.items())
    for i in range(15):
        is_real = i < len(items)
        name, spr = (items[i][0], items[i][1]) if is_real else ("NUEVA UNIDAD", [0, 0])
        st_base = "background: #ebebeb; color: #969696;" if is_real else "background: #fcfcfc; color: #C0C0C0;"
        rows += f'''
        <tr data-table="{table_id}" class="master-row" style="{st_base}">
            <td contenteditable="true" class="edit-name" oninput="recalc()" style="font-weight: bold; text-align: left; padding-left: 10px; border: 0.5px solid #ccc; width: 150px; white-space: nowrap;">{name}</td>
            <td contenteditable="true" class="edit-spr-min" oninput="recalc()" style="text-align: center; border: 0.5px solid #ccc; width: 45px;">{spr[0]}</td>
            <td contenteditable="true" class="edit-spr-max" oninput="recalc()" style="text-align: center; border: 0.5px solid #ccc; width: 45px;">{spr[1]}</td>
            <td contenteditable="true" class="edit-orh" style="text-align: center; border: 0.5px solid #ccc; width: 45px;">480</td>
            <td contenteditable="true" class="f-stock" oninput="recalc()" style="text-align: center; border: 0.5px solid #ccc; width: 55px; font-weight: bold;">0</td>
            <td class="f-left" style="font-weight: bold; text-align: center; border: 0.5px solid #ccc; width: 60px;">0</td>
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
        <td style="text-align: center; border: 0.5px solid #ccc;"><input type="checkbox" class="ok-check" style="transform: scale(1.3);"></td>
    </tr>'''
    for i in range(1, 11):
        polys += f'''
        <div class="poligono-bloque" style="margin-bottom: 20px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); border-radius: 8px; overflow: hidden; background: white; border: 1px solid #ccc;">
            <table style="width: 100%; border-collapse: collapse; table-layout: auto;">
                <thead>
                    <tr style="background: linear-gradient(180deg, #888888 0%, #696969 100%); color: white; font-size: 12px; height: 35px;">
                        <th style="padding: 0 10px; min-width: 80px; white-space: nowrap;">PLAN / RUTA</th>
                        <th style="min-width: 80px; white-space: nowrap;">VOL. TOTAL</th>
                        <th style="width: 110px;"># ASIGNADAS</th>
                        <th style="width: 110px;">SPR REAL</th>
                        <th>TIPO DE UNIDAD</th>
                        <th style="width: 40px;">OK</th>
                    </tr>
                </thead>
                <tbody>
                    <tr class="calc-row">
                        <td rowspan="5" contenteditable="true" style="background: #f0f0f0; font-weight:bold; text-align:center; border: 1px solid #ccc; white-space: nowrap; padding: 5px; color:#333;">PLAN {i}</td>
                        <td rowspan="5" contenteditable="true" class="v-total-val" oninput="recalc()" style="color: #20B2AA; font-weight: bold; font-size: 18px; text-align: center; border: 1px solid #ccc; white-space: nowrap; padding: 5px;">0</td>
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
                        <td style="text-align: center; border: 0.5px solid #ccc;"><input type="checkbox" class="ok-check" style="transform: scale(1.3);"></td>
                    </tr>
                    {fila_inner}{fila_inner}{fila_inner}{fila_inner}
                    <tr style="background:#f8f9fa;">
                        <td colspan="2" style="text-align:center; font-weight:bold; border: 1px solid #ccc; font-size: 11px; color:#333;">ESTADO:</td>
                        <td class="v-calculado-total" style="font-weight: bold; font-size: 16px; color: #d32f2f; border: 1px solid #ccc; text-align: center;">0</td>
                        <td class="p-diff" colspan="3" style="text-align: center; font-weight: bold; border: 1px solid #ccc; font-size: 11px;">VACÍO</td>
                    </tr>
                </tbody>
            </table>
        </div>'''
    return polys

# --- 3. ENSAMBLAJE FINAL ---
app_html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: sans-serif; background: #f5f7f9; padding: 15px; }}
        .meli-table {{ border-collapse: collapse; width: 100%; table-layout: fixed; }}
        .meli-table th, .meli-table td {{ border: 1px solid #ccc; font-size: 12px; height: 30px; }}
        #google-alert {{ 
            position: fixed; top: -100px; left: 50%; transform: translateX(-50%);
            background: #d32f2f; color: white; padding: 15px 25px; border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3); transition: 0.4s; z-index: 10000;
        }}
        #google-alert.show {{ top: 20px; }}
        .tab-btn {{ padding: 8px 15px; cursor: pointer; border: none; background: #e0e0e0; border-radius: 4px 4px 0 0; font-weight: bold; margin-right: 2px; }}
        .tab-btn.active {{ background: #333; color: white; }}
        
        .activas-todas-btn {{ 
            background: linear-gradient(180deg, #5ae0d9 0%, #20B2AA 100%); 
            color: white; border: none; padding: 6px 12px; border-radius: 4px; 
            cursor: pointer; font-weight: bold; font-size: 11px; box-shadow: 2px 2px 4px rgba(0,0,0,0.1); 
        }}
        .activas-todas-btn:active {{ transform: translateY(1px); box-shadow: none; }}

        /* ESTILOS HERRAMIENTAS (IMAGEN 2) */
        .tools-panel {{ display: flex; flex-direction: column; gap: 10px; margin-top: 15px; }}
        
        .google-tool {{ background: #dfdff5; padding: 15px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border: 1px solid #ccc; text-align: center; }}
        .google-tool-title {{ font-size: 11px; font-weight: bold; color: #4e3396; letter-spacing: 1px; display: flex; align-items: center; justify-content: center; gap: 5px; }}
        .google-input {{ border: 1px solid #ccc; border-radius: 5px; height: 30px; text-align: center; font-weight: bold; margin: 0 5px; width: 60px; }}
        .google-res {{ font-size: 20px; font-weight: bold; color: #ac40de; }}

        /* CALCULADORA AQUA (CALCADA DE LA IMAGEN) */
        #calc_wrapper {{ background: #22c5bc; border-radius: 20px; padding: 15px; box-shadow: 0 10px 20px rgba(0,0,0,0.15); border: 1px solid #1a1a1a; }}
        #calc_display_box {{ background: #fffacd; border-radius: 10px; padding: 10px; text-align: right; margin-bottom: 15px; position: relative; border: 1px solid rgba(0,0,0,0.1); }}
        #calc_h {{ font-size: 12px; color: #666; height: 15px; font-family: monospace; }}
        #calc_r {{ font-size: 26px; font-weight: bold; color: black; font-family: monospace; }}
        .calc-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; }}
        .btn-c {{ background: white; color: black; border: none; font-size: 16px; font-weight: bold; border-radius: 10px; padding: 12px; cursor: pointer; box-shadow: 0 4px #ccc; transition: 0.1s; }}
        .btn-c:active {{ transform: translateY(2px); box-shadow: 0 2px #ccc; }}
        .btn-c-op {{ background: #f0f0f0; }}
        .btn-c-eq {{ background: #FF00FF; color: white; border-radius: 10px; padding: 12px; cursor: pointer; font-weight: bold; box-shadow: 0 4px #c200c2; transition: 0.1s; }}
        .btn-c-eq:active {{ transform: translateY(2px); box-shadow: 0 2px #c200c2; }}

        /* CRONÓMETRO */
        .crono-box {{ background: #1a1a1a; padding: 15px; border-radius: 15px; color: white; text-align: center; box-shadow: 0 6px 12px rgba(0,0,0,0.3); }}
        .crono-time {{ font-size: 36px; font-weight: bold; font-family: monospace; letter-spacing: -2px; margin: 5px 0; color: white; text-shadow: 0 0 10px rgba(255,255,255,0.2); }}
    </style>
</head>
<body>

<div id="google-alert">⚠️ <span id="alert-msg"></span> [ENTER para cerrar]</div>

<div style="display: flex; gap: 20px; max-width: 1700px; margin: auto;">
    
    <!-- COLUMNA IZQUIERDA: PLANES -->
    <div style="flex: 1; min-width: 700px; width: 0;">
        <div style="background: linear-gradient(180deg, #888888 0%, #696969 100%); color: white; padding: 12px; border-radius: 8px; text-align: center; font-weight: bold; margin-bottom: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">📋 PLANIFICACIÓN POR POLÍGONOS</div>
        <div id="polys-2" class="p-content">{gen_poligonos()}</div>
        <div id="polys-3" class="p-content" style="display:none;">{gen_poligonos()}</div>
        <div id="polys-1" class="p-content" style="display:none;">{gen_poligonos()}</div>
        <div id="polys-4" class="p-content" style="display:none;">{gen_poligonos()}</div>
    </div>

    <!-- COLUMNA DERECHA: FLOTA Y HERRAMIENTAS -->
    <div style="width: 470px; flex-shrink: 0; position: sticky; top: 10px; height: fit-content;">
        
        <div style="background: linear-gradient(180deg, #333 0%, #000 100%); color: white; padding: 12px; border-radius: 8px; font-weight: bold; margin-bottom: 10px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.2);">🚚 DISPONIBILIDAD DE FLOTA</div>
        <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 0;">
            <div>
                <button class="tab-btn active" onclick="showTab(2, this)">C1</button>
                <button class="tab-btn" onclick="showTab(3, this)">C2</button>
                <button class="tab-btn" onclick="showTab(1, this)">SD</button>
                <button class="tab-btn" onclick="showTab(4, this)">SDE</button>
            </div>
            <!-- BOTONES RESTAURADOS -->
            <div style="display:flex; gap:5px; padding-bottom:5px;">
                <button onclick="filterFlota(true)" class="activas-todas-btn" style="background:#C0C0C0; color:#333;">ACTIVAS</button>
                <button onclick="filterFlota(false)" class="activas-todas-btn">TODAS</button>
            </div>
        </div>
        <div style="background: white; padding: 10px; border: 1px solid #ccc; border-radius: 0 0 6px 6px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <div id="tab-2" class="t-content"><table class="meli-table"><thead style="background:#333; color:white;"><tr><th>UNIDAD</th><th>MIN</th><th>MAX</th><th>ORH</th><th>SCH</th><th>REST</th></tr></thead><tbody id="body-2">{gen_master_rows(u_C1, 2)}</tbody></table></div>
            <div id="tab-3" class="t-content" style="display:none;"><table class="meli-table"><thead style="background:#333; color:white;"><tr><th>UNIDAD</th><th>MIN</th><th>MAX</th><th>ORH</th><th>SCH</th><th>REST</th></tr></thead><tbody id="body-3">{gen_master_rows(u_C2, 3)}</tbody></table></div>
            <div id="tab-1" class="t-content" style="display:none;"><table class="meli-table"><thead style="background:#333; color:white;"><tr><th>UNIDAD</th><th>MIN</th><th>MAX</th><th>ORH</th><th>SCH</th><th>REST</th></tr></thead><tbody id="body-1">{gen_master_rows(u_SD, 1)}</tbody></table></div>
            <div id="tab-4" class="t-content" style="display:none;"><table class="meli-table"><thead style="background:#333; color:white;"><tr><th>UNIDAD</th><th>MIN</th><th>MAX</th><th>ORH</th><th>SCH</th><th>REST</th></tr></thead><tbody id="body-4">{gen_master_rows(u_SDE, 4)}</tbody></table></div>
        </div>

        <div class="tools-panel">
            <!-- CONVERTIDOR ESTILO IMAGEN 2 -->
            <div class="google-tool">
                <div class="google-tool-title">⏱️ CONVERTIDOR DE TIEMPO</div>
                <div style="display: flex; align-items: center; justify-content: center; margin-top: 5px;">
                    <input type="number" id="min-in" placeholder="Min" class="google-input" oninput="convertTime()">
                    <span id="time-res" class="google-res">0h 0m</span>
                </div>
            </div>

            <!-- CALCULADORA AQUA ESTILO IMAGEN 2 -->
            <div id="calc_wrapper">
                <div id="calc_display_box">
                    <div id="calc_h">0</div>
                    <div id="calc_r">0</div>
                </div>
                <div class="calc-grid">
                    <button onclick="cl()" class="btn-c" style="grid-column: span 2;">AC</button>
                    <button onclick="del()" class="btn-c">⌫</button><button onclick="ao('/')" class="btn-c btn-c-op">÷</button>
                    <button onclick="an('7')" class="btn-c">7</button><button onclick="an('8')" class="btn-c">8</button><button onclick="an('9')" class="btn-c">9</button><button onclick="ao('*')" class="btn-c btn-c-op">×</button>
                    <button onclick="an('4')" class="btn-c">4</button><button onclick="an('5')" class="btn-c">5</button><button onclick="an('6')" class="btn-c">6</button><button onclick="ao('-')" class="btn-c btn-c-op">-</button>
                    <button onclick="an('1')" class="btn-c">1</button><button onclick="an('2')" class="btn-c">2</button><button onclick="an('3')" class="btn-c">3</button><button onclick="ao('+')" class="btn-c btn-c-op">+</button>
                    <button onclick="an('0')" class="btn-c" style="grid-column: span 2;">0</button><button onclick="calc_eq()" class="btn-c-eq">=</button>
                </div>
            </div>

            # --- COLUMNA DERECHA: PANEL DE HERRAMIENTAS REFORMADO ---
        <div class="tools-panel">
            
            <!-- 1. CONVERTIDOR DE TIEMPO -->
            <div class="google-tool">
                <div class="google-tool-title">⏱️ CONVERTIDOR DE TIEMPO</div>
                <div style="display: flex; align-items: center; justify-content: center; margin-top: 5px;">
                    <input type="number" id="min-in" placeholder="Min" class="google-input" oninput="convertTime()">
                    <span id="time-res" class="google-res">0h 0m</span>
                </div>
            </div>

            <!-- 2. CALCULADORA AQUA -->
            <div id="calc_wrapper">
                <div id="calc_display_box">
                    <div id="calc_h">0</div>
                    <div id="calc_r">0</div>
                </div>
                <div class="calc-grid">
                    <button onclick="cl()" class="btn-c" style="grid-column: span 2;">AC</button>
                    <button onclick="del()" class="btn-c">⌫</button><button onclick="ao('/')" class="btn-c btn-c-op">÷</button>
                    <button onclick="an('7')" class="btn-c">7</button><button onclick="an('8')" class="btn-c">8</button><button onclick="an('9')" class="btn-c">9</button><button onclick="ao('*')" class="btn-c btn-c-op">×</button>
                    <button onclick="an('4')" class="btn-c">4</button><button onclick="an('5')" class="btn-c">5</button><button onclick="an('6')" class="btn-c">6</button><button onclick="ao('-')" class="btn-c btn-c-op">-</button>
                    <button onclick="an('1')" class="btn-c">1</button><button onclick="an('2')" class="btn-c">2</button><button onclick="an('3')" class="btn-c">3</button><button onclick="ao('+')" class="btn-c btn-c-op">+</button>
                    <button onclick="an('0')" class="btn-c" style="grid-column: span 2;">0</button><button onclick="calc_eq()" class="btn-c-eq">=</button>
                </div>
            </div>

            <!-- 3. CRONÓMETRO (DISEÑO SEGÚN IMAGEN_CBEDBF.PNG) -->
            <div class="crono-card" style="background: #1c1c1c; border-radius: 12px; padding: 15px; color: white; font-family: monospace;">
                <div class="crono-header" style="display: flex; justify-content: space-between; border-bottom: 1px solid #444; padding-bottom: 5px; margin-bottom: 10px;">
                    <span style="font-size: 10px; color: #888;">HORA ACTUAL</span>
                    <span id="reloj-actual" style="font-size: 14px; color: #00e5ff; font-weight: bold;">00:00:00</span>
                </div>
                <div id="crono-main" style="font-size: 38px; text-align: center; font-weight: bold; margin-bottom: 15px;">00:00:00.0</div>
                <div class="crono-controls" style="display: flex; justify-content: center; gap: 10px;">
                    <button onclick="startC()" style="width:50px; height:50px; background:#28a745; border:none; border-radius:8px; color:white; cursor:pointer;">▶</button>
                    <button onclick="stopC()" style="width:50px; height:50px; background:#ffc107; border:none; border-radius:8px; color:white; cursor:pointer;">⏸</button>
                    <button onclick="resetC()" style="width:50px; height:50px; background:#dc3545; border:none; border-radius:8px; color:white; cursor:pointer;">🔄</button>
                </div>
            </div>
        </div>

    </div>
</div>

<script>
    let currentTab = 2;
    let editedRowsPlan = new Set();
    let alertShownSD = false;
    let chronoInterval;
    let seconds = 0;
    let curC = "";

    function showTab(n, btn) {{
        currentTab = n;
        document.querySelectorAll('.p-content, .t-content').forEach(el => el.style.display = 'none');
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.getElementById('polys-'+n).style.display = 'block';
        document.getElementById('tab-'+n).style.display = 'block';
        btn.classList.add('active');
        recalc();
    }}

    function filterFlota(hide) {{
        document.querySelectorAll('#body-' + currentTab + ' tr').forEach(row => {{
            let stock = parseInt(row.querySelector('.f-stock').innerText) || 0;
            row.style.display = (hide && stock === 0) ? 'none' : '';
        }});
    }}

    function showAlert(msg) {{
        document.getElementById('alert-msg').innerText = msg;
        document.getElementById('google-alert').classList.add('show');
    }}

    function hideAlert() {{ document.getElementById('google-alert').classList.remove('show'); }}

    function stepVal(btn, delta, type) {{
        let row = btn.closest('tr');
        let sel = row.querySelector('.s-type').value;
        if(sel === "SELECCIONAR...") return;

        let fRow = Array.from(document.querySelectorAll('#body-'+currentTab+' tr')).find(r => r.querySelector('.edit-name').innerText.trim() === sel);
        let left = parseInt(fRow.querySelector('.f-left').innerText) || 0;

        if(type === 'u') {{
            let span = row.querySelector('.u-manual');
            let val = parseInt(span.innerText) || 0;
            if (delta > 0 && left <= 0 && currentTab !== 4) {{ // Bloqueo si no es SDE
                if (currentTab === 1 && !alertShownSD) {{ showAlert("⚠️ AGOTADO EN SD."); alertShownSD = true; }}
                else if (currentTab !== 1) {{ showAlert("⚠️ AGOTADO. Bloqueo asignación SVC."); return; }}
            }}
            span.innerText = Math.max(0, val + delta);
        }} else {{
            let span = row.querySelector('.spr-real-val');
            let val = parseFloat(span.innerText) || 0;
            span.innerText = Math.max(0, val + delta);
        }}
        editedRowsPlan.add(row);
        recalc();
    }}

    function recalc() {{
        let fleet = {{}};
        let hasOverGlobal = false;

        document.querySelectorAll('#body-' + currentTab + ' tr').forEach(row => {{
            let n = row.querySelector('.edit-name').innerText.trim();
            let s = parseInt(row.querySelector('.f-stock').innerText) || 0;
            let mi = row.querySelector('.edit-spr-min'), ma = row.querySelector('.edit-spr-max'), fS = row.querySelector('.f-stock'), nC = row.querySelector('.edit-name');
            
            // Colores Dinámicos
            if(s > 0) {{
                nC.style.background = "white"; nC.style.color="black";
                fS.style.background = "#e3defa"; mi.style.background = "#def3ed"; ma.style.background = "#def3ed";
            }} else {{
                nC.style.background = "#ebebeb"; nC.style.color="#969696";
                fS.style.background = "#ebebeb"; mi.style.background = "#ebebeb"; ma.style.background = "#ebebeb";
            }}
            if(n !== "" && n !== "NUEVA UNIDAD") fleet[n] = {{ max: parseFloat(ma.innerText)||0, stock: s, used: 0 }};
        }});

        document.querySelectorAll('#polys-' + currentTab + ' .poligono-bloque').forEach(bl => {{
            let vT = parseFloat(bl.querySelector('.v-total-val').innerText) || 0, vA = 0;
            bl.querySelectorAll('.calc-row').forEach(r => {{
                let s = r.querySelector('.s-type').value, u = parseInt(r.querySelector('.u-manual').innerText) || 0, sp = r.querySelector('.spr-real-val');
                if(s !== "SELECCIONAR..." && fleet[s]) {{
                    if(!editedRowsPlan.has(r)) sp.innerText = fleet[s].max;
                    fleet[s].used += u; vA += (u * parseFloat(sp.innerText));
                }}
            }});
            bl.querySelector('.v-calculado-total').innerText = Math.round(vA);
            let d = bl.querySelector('.p-diff');
            if(vT===0) {{ d.innerText="VACÍO"; d.style.background="none"; }}
            else {{
                d.innerText = (vA >= vT) ? (vA===vT ? "OK" : "EXCESO: "+Math.round(vA-vT)) : "FALTAN: "+Math.round(vT-vA);
                d.style.background = (vA >= vT) ? (vA===vT ? "#ceedd6":"#ffe4b5") : "#f7cdd1";
            }}
        }});

        document.querySelectorAll('#body-' + currentTab + ' tr').forEach(row => {{
            let n = row.querySelector('.edit-name').innerText.trim();
            if(fleet[n]) {{
                let res = fleet[n].stock - fleet[n].used, cL = row.querySelector('.f-left');
                cL.innerText = Math.abs(res);
                
                if (res <= 0) {{
                    cL.style.background = "#d32f2f"; // Rojo brillante
                    cL.style.color = "white";
                }} else {{
                    cL.style.background = "#fff";
                    cL.style.color = "green";
                }}
                if(res < 0) hasOverGlobal = true;
            }}
        }});

        // Cambio Título ME QUEDAN / ME PASÉ (Solo SDE)
        let h = document.querySelector('#tab-' + currentTab + ' .header-flota[rowspan="2"]:last-child');
        if(h) h.innerText = (currentTab === 4 && hasOverGlobal) ? "ME PASÉ POR" : "ME QUEDAN";

        // Actualizar dropdowns
        document.querySelectorAll('#polys-' + currentTab + ' .s-type').forEach(s => {{
            let cur = s.value, opt = '<option>SELECCIONAR...</option>';
            Object.keys(fleet).forEach(k => {{ if(fleet[k].stock > 0 || k === cur) opt += `<option value="${{k}}">${{k}}</option>`; }});
            s.innerHTML = opt; s.value = cur;
        }});
    }}

    // HERRAMIENTAS
    function convertTime() {{
        let m = parseInt(document.getElementById('min-in').value) || 0;
        document.getElementById('time-res').innerText = Math.floor(m/60) + "h " + (m%60) + "m";
    }}
    function an(n) {{ curC += n; updateCalc(); }}
    function ao(o) {{ curC += " " + o + " "; updateCalc(); }}
    function cl() {{ curC = ""; updateCalc(); }}
    function del() {{ curC = curC.trim().slice(0, -1); updateCalc(); }}
    function updateCalc() {{ document.getElementById('calc_r').innerText = curC || "0"; }}
    function calc_eq() {{ try {{ let res = eval(curC); document.getElementById('calc_h').innerText = curC + " ="; curC = res.toString(); updateCalc(); }} catch {{ }} }}
    function startChrono() {{ if(chronoInterval) return; chronoInterval = setInterval(()=>{{ seconds++; updateChrono(); }}, 1000); }}
    function stopChrono() {{ clearInterval(chronoInterval); chronoInterval = null; }}
    function resetChrono() {{ stopChrono(); seconds = 0; updateChrono(); }}
    function updateChrono() {{ let h=Math.floor(seconds/3600), m=Math.floor((seconds%3600)/60), s=seconds%60; document.getElementById('chrono-display').innerText = String(h).padStart(2,'0')+":"+String(m).padStart(2,'0')+":"+String(s).padStart(2,'0'); }}
    document.addEventListener('keydown', (e) => {{ if(e.key === 'Enter') hideAlert(); }});
    function manualEdit(el) {{ editedRowsPlan.add(el.closest('tr')); recalc(); }}
    function resetRow(sel) {{ let r=sel.closest('tr'); r.querySelector('.u-manual').innerText="0"; r.querySelector('.spr-real-val').innerText="0"; editedRowsPlan.delete(r); recalc(); }}
    recalc();
</script>
</body>
</html>
"""

html(app_html, height=1300, scrolling=True)
