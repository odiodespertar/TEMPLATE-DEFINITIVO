import streamlit as st
from streamlit.components.v1 import html

st.set_page_config(page_title="Monitor Logístico - Liliana García", layout="wide")

# CSS para diseño limpio de Streamlit
st.markdown("""
    <style>
    .block-container {padding: 0rem !important;}
    footer, #MainMenu, header {visibility: hidden;}
    body { background-color: #f5f7f9; }
    </style>
""", unsafe_allow_html=True)

# --- DATOS BASE ---
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
        st_base = "background: #ebebeb; color: #969696;"
        rows += f'''
        <tr class="master-row" style="{st_base}">
            <td contenteditable="true" class="edit-name" oninput="recalc()" style="font-weight: bold; text-align: left; padding-left: 10px; border: 0.5px solid #ccc; width: 150px;">{name}</td>
            <td contenteditable="true" class="edit-spr-min" oninput="recalc()" style="text-align: center; border: 0.5px solid #ccc; width: 45px;">{spr[0]}</td>
            <td contenteditable="true" class="edit-spr-max" oninput="recalc()" style="text-align: center; border: 0.5px solid #ccc; width: 45px;">{spr[1]}</td>
            <td contenteditable="true" class="edit-orh" style="text-align: center; border: 0.5px solid #ccc; width: 45px;">480</td>
            <td contenteditable="true" class="f-stock" oninput="recalc()" style="text-align: center; border: 0.5px solid #ccc; width: 55px; font-weight: bold; font-size: 16px;">0</td>
            <td class="f-left" style="font-weight: bold; text-align: center; border: 0.5px solid #ccc; width: 60px; font-size: 14px;">0</td>
        </tr>'''
    return rows

def gen_poligonos():
    polys = ""
    btn_s = "cursor:pointer; border:none; background:rgba(0,0,0,0.08); color:#333; font-weight:bold; width:22px; height:22px; border-radius:4px; margin:0 2px;"
    fila_inner = f'''
    <tr class="calc-row">
        <td class="u-manual-cell" style="background: #e3defa; text-align: center; border: 0.6px solid #ccc; padding: 10px 5px;">
            <button style="{btn_s}" onclick="stepVal(this, -1, 'u')">-</button>
            <span contenteditable="true" class="u-manual" oninput="manualEdit(this)" style="font-weight: bold; margin:0 5px;">0</span>
            <button style="{btn_s}" onclick="stepVal(this, 1, 'u')">+</button>
        </td>
        <td class="spr-real-cell" style="background: #def3ed; text-align: center; border: 0.6px solid #ccc; padding: 10px 5px;">
            <button style="{btn_s}" onclick="stepVal(this, -1, 's')">-</button>
            <span contenteditable="true" class="spr-real-val" oninput="manualEdit(this)" style="font-weight: bold; margin:0 5px;">0</span>
            <button style="{btn_s}" onclick="stepVal(this, 1, 's')">+</button>
        </td>
        <td style="border: 0.5px solid #ccc; padding: 2px;"><select class="s-type" onchange="resetRow(this)" style="width:auto; min-width:120px; max-width:250px; border:none; background:transparent; font-weight:bold; font-size:11px; color:#333;"><option>SELECCIONAR...</option></select></td>
        <td style="text-align: center; border: 0.5px solid #ccc;"><input type="checkbox" class="ok-check" style="transform: scale(1.3);"></td>
    </tr>'''
    for i in range(1, 11):
        polys += f'''
        <div class="poligono-bloque" style="margin-bottom: 25px; box-shadow: 0 10px 20px rgba(0,0,0,0.1); border-radius: 12px; overflow: hidden; background: white; border: 1px solid #e1e1e1;">
            <table style="width: 100%; border-collapse: collapse;">
                <thead>
                    <tr style="background: linear-gradient(180deg, #696969, #808080); color: white; font-size: 12px; height: 36px;">
                        <th style="padding: 0 10px;">PLAN / RUTA</th>
                        <th>VOL. TOTAL</th>
                        <th style="width: 110px;"># ASIGNADAS</th>
                        <th style="width: 110px;">SPR REAL</th>
                        <th>TIPO DE UNIDAD</th>
                        <th style="width: 40px;">OK</th>
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

app_html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: sans-serif; background: #f5f7f9; padding: 15px; }}
        
        /* BOTONES FILTRO 3D */
        .filter-btn {{
            cursor: pointer; font-size: 13px; padding: 8px 18px; border-radius: 8px;
            font-weight: bold; transition: all 0.1s ease; border: 1px solid rgba(0,0,0,0.2);
            display: inline-block; text-transform: uppercase; outline: none;
        }}
        .btn-activas {{
            background: linear-gradient(180deg, #2ecc71 0%, #27ae60 100%);
            color: white; box-shadow: 0 4px 0 #1e8449, 0 5px 10px rgba(0,0,0,0.2);
            margin-right: 8px;
        }}
        .btn-todas {{
            background: linear-gradient(180deg, #ffffff 0%, #e0e0e0 100%);
            color: #333; box-shadow: 0 4px 0 #b3b3b3, 0 5px 10px rgba(0,0,0,0.15);
        }}
        .filter-btn:active {{ box-shadow: 0 0 0 transparent; transform: translateY(4px); }}

        /* TABLAS */
        .meli-table {{ 
            border-collapse: separate; border-spacing: 0; width: 100%; 
            border-radius: 10px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.1); border: 1px solid #ccc;
        }}
        .meli-table th {{ background: #222; color: white; font-size: 11px; height: 35px; text-align: center; }}
        .meli-table td {{ border-bottom: 1px solid #eee; border-right: 1px solid #eee; font-size: 11px; text-align: center; }}

        /* PESTAÑAS */
        .tab-btn {{ 
            padding: 10px 20px; cursor: pointer; border: 1px solid #bbb; 
            background: #f0f0f0; border-radius: 8px 8px 0 0; font-weight: bold;
        }}
        .tab-btn.active {{ background: #333; color: white; }}

        /* HERRAMIENTAS */
        .tools-panel {{ display: flex; flex-direction: column; gap: 10px; margin-top: 15px; }}
        .google-tool {{ background: #dfdff5; padding: 10px; border-radius: 12px; border: 1px solid #ccc; text-align: center; }}
        #calc_wrapper {{ background: #22c5bc; border-radius: 20px; padding: 15px; }}
        .calc-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 5px; }}
        .btn-c {{ background: white; border: none; border-radius: 8px; padding: 10px; cursor: pointer; font-weight: bold; }}
        .crono-card {{ background: #1c1c1c; border-radius: 12px; padding: 15px; color: white; text-align: center; }}
        
        #google-alert {{ 
            position: fixed; top: -100px; left: 50%; transform: translateX(-50%);
            background: #d32f2f; color: white; padding: 15px; border-radius: 8px; transition: 0.4s; z-index: 10000;
        }}
        #google-alert.show {{ top: 20px; }}
    </style>
</head>
<body>

<div id="google-alert">⚠️ <span id="alert-msg"></span> [ENTER para cerrar]</div>

<div style="display: flex; gap: 20px;">
    <div style="flex: 1;">
        <div style="background: #696969; color: white; padding: 10px; border-radius: 8px; text-align: center; font-weight: bold; margin-bottom: 10px;">📋 PLANIFICACIÓN POR POLÍGONOS</div>
        <div id="polys-2" class="p-content">{gen_poligonos()}</div>
        <div id="polys-3" class="p-content" style="display:none;">{gen_poligonos()}</div>
        <div id="polys-1" class="p-content" style="display:none;">{gen_poligonos()}</div>
        <div id="polys-4" class="p-content" style="display:none;">{gen_poligonos()}</div>
    </div>

    <div style="width: 450px;">
        <div style="background: #000; color: white; padding: 10px; border-radius: 8px; font-weight: bold; text-align: center; margin-bottom: 10px;">🚚 DISPONIBILIDAD DE FLOTA</div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
            <div>
                <button class="tab-btn active" onclick="showTab(2, this)">C1</button>
                <button class="tab-btn" onclick="showTab(3, this)">C2</button>
                <button class="tab-btn" onclick="showTab(1, this)">SD</button>
                <button class="tab-btn" onclick="showTab(4, this)">SDE</button>
            </div>
            <div style="padding-bottom: 5px;">
                <button onclick="filterRows(true)" class="filter-btn btn-activas">ACTIVAS</button>
                <button onclick="filterRows(false)" class="filter-btn btn-todas">TODAS</button>
            </div>
        </div>

        <div id="tab-2" class="t-content">
            <table class="meli-table">
                <thead>
                    <tr><th rowspan="2">UNIDAD</th><th colspan="2">SPR</th><th rowspan="2">MINS</th><th rowspan="2">STOCK</th><th rowspan="2">REST</th></tr>
                    <tr><th>MIN</th><th>MAX</th></tr>
                </thead>
                <tbody id="body-2">{gen_master_rows(u_C1, 2)}</tbody>
            </table>
        </div>
        <!-- (Resto de las pestañas simplificadas para el ejemplo, pero en tu código real puedes dejarlas igual) -->
        <div id="tab-3" class="t-content" style="display:none;"><table class="meli-table"><tbody id="body-3">{gen_master_rows(u_C2, 3)}</tbody></table></div>
        <div id="tab-1" class="t-content" style="display:none;"><table class="meli-table"><tbody id="body-1">{gen_master_rows(u_SD, 1)}</tbody></table></div>
        <div id="tab-4" class="t-content" style="display:none;"><table class="meli-table"><tbody id="body-4">{gen_master_rows(u_SDE, 4)}</tbody></table></div>

        <div class="tools-panel">
            <div class="google-tool">
                ⏱️ <input type="number" id="min-in" style="width:60px;" oninput="convertTime()">
                <span id="time-res" style="font-weight: bold;">0h 0m</span>
            </div>
            <div id="calc_wrapper">
                <div id="calc_display_box" style="background:white; padding:10px; border-radius:5px; text-align:right; margin-bottom:5px;">
                    <div id="calc_r" style="font-size:20px; font-weight:bold;">0</div>
                </div>
                <div class="calc-grid">
                    <button onclick="cl()" class="btn-c">AC</button><button onclick="ao('/')" class="btn-c">÷</button>
                    <button onclick="an('7')" class="btn-c">7</button><button onclick="ao('*')" class="btn-c">×</button>
                    <button onclick="calc_eq()" class="btn-c" style="grid-column: span 2;">=</button>
                </div>
            </div>
            <div class="crono-card">
                <div id="crono-main" style="font-size:24px;">00:00:00</div>
                <button onclick="startC()">▶</button><button onclick="stopC()">⏸</button><button onclick="resetC()">🔄</button>
            </div>
        </div>
    </div>
</div>

<script>
    let currentTab = 2;
    let editedRowsPlan = new Set();
    let curC = "";
    let chronoInterval, startTime, elapsedTime = 0;

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

    function stepVal(btn, delta, type) {{
        let row = btn.closest('tr');
        let sel = row.querySelector('.s-type').value;
        if(sel === "SELECCIONAR...") return;
        if(type === 'u') {{
            let span = row.querySelector('.u-manual');
            span.innerText = Math.max(0, parseInt(span.innerText) + delta);
        }} else {{
            let span = row.querySelector('.spr-real-val');
            span.innerText = Math.max(0, parseFloat(span.innerText) + delta).toFixed(1);
        }}
        editedRowsPlan.add(row);
        recalc();
    }}

    function recalc() {{
        let fleet = {{}};
        document.querySelectorAll('#body-' + currentTab + ' tr').forEach(row => {{
            let name = row.querySelector('.edit-name').innerText.trim();
            let stock = parseInt(row.querySelector('.f-stock').innerText) || 0;
            if(name !== "NUEVA UNIDAD") fleet[name] = {{ stock: stock, used: 0, max: 120 }};
        }});

        document.querySelectorAll('#polys-' + currentTab + ' .poligono-bloque').forEach(bl => {{
            let vT = parseFloat(bl.querySelector('.v-total-val').innerText) || 0, vA = 0;
            bl.querySelectorAll('.calc-row').forEach(r => {{
                let s = r.querySelector('.s-type').value;
                let u = parseInt(r.querySelector('.u-manual').innerText) || 0;
                if(fleet[s]) {{ fleet[s].used += u; vA += u * 100; }}
            }});
            bl.querySelector('.v-calculado-total').innerText = vA;
        }});
        
        // Actualizar opciones de los selectores
        document.querySelectorAll('#polys-' + currentTab + ' .s-type').forEach(s => {{
            let cur = s.value, opt = '<option>SELECCIONAR...</option>';
            Object.keys(fleet).forEach(k => {{ if(fleet[k].stock > 0 || k === cur) opt += `<option value="${{k}}">${{k}}</option>`; }});
            s.innerHTML = opt; s.value = cur;
        }});
    }}

    function filterRows(active) {{
        document.querySelectorAll('#body-' + currentTab + ' tr').forEach(r => {{
            let s = parseInt(r.querySelector('.f-stock').innerText) || 0;
            r.style.display = (active && s === 0) ? 'none' : '';
        }});
    }}

    function convertTime() {{
        let m = document.getElementById('min-in').value || 0;
        document.getElementById('time-res').innerText = Math.floor(m/60) + "h " + (m%60) + "m";
    }}

    function an(n) {{ curC += n; updateCalc(); }}
    function ao(o) {{ curC += o; updateCalc(); }}
    function cl() {{ curC = ""; updateCalc(); }}
    function updateCalc() {{ document.getElementById('calc_r').innerText = curC || "0"; }}
    function calc_eq() {{ try {{ curC = eval(curC).toString(); updateCalc(); }} catch {{ }} }}

    function startC() {{ if(!chronoInterval) {{ startTime = Date.now() - elapsedTime; chronoInterval = setInterval(()=>{{ elapsedTime = Date.now() - startTime; updateCDisplay(); }}, 100); }} }}
    function stopC() {{ clearInterval(chronoInterval); chronoInterval = null; }}
    function resetC() {{ stopC(); elapsedTime = 0; updateCDisplay(); }}
    function updateCDisplay() {{ 
        let d = new Date(elapsedTime);
        document.getElementById('crono-main').innerText = d.toISOString().substr(11, 8);
    }}

    function manualEdit(el) {{ editedRowsPlan.add(el.closest('tr')); recalc(); }}
    function resetRow(sel) {{ recalc(); }}

    document.addEventListener('keydown', (e) => {{ if(e.key === 'Enter') document.getElementById('google-alert').classList.remove('show'); }});
</script>
</body>
</html>
"""

html(app_html, height=1200, scrolling=True)
