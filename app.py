import streamlit as st
from streamlit.components.v1 import html

st.set_page_config(page_title="Monitor Logístico - Liliana García", layout="wide")

st.markdown("""
    <style>
    .block-container {padding: 0rem !important;}
    footer, #MainMenu, header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- DATOS ---
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
        st_base = "background: #ebebeb; color: #333;"
        rows += f'''
        <tr class="master-row" style="{st_base}">
            <td contenteditable="true" class="edit-name" oninput="recalc()" style="font-weight: bold; text-align: left; padding-left: 10px; border: 0.5px solid #ccc; width: 150px;">{name}</td>
            <td contenteditable="true" class="edit-spr-min" oninput="recalc()" style="text-align: center; border: 0.5px solid #ccc; width: 45px;">{spr[0]}</td>
            <td contenteditable="true" class="edit-spr-max" oninput="recalc()" style="text-align: center; border: 0.5px solid #ccc; width: 45px;">{spr[1]}</td>
            <td contenteditable="true" class="edit-orh" style="text-align: center; border: 0.5px solid #ccc; width: 45px;">480</td>
            <td contenteditable="true" class="f-stock" oninput="recalc()" style="text-align: center; border: 0.5px solid #ccc; width: 55px; font-weight: bold; font-size: 16px; background: #fff;">0</td>
            <td class="f-left" style="font-weight: bold; text-align: center; border: 0.5px solid #ccc; width: 60px; font-size: 14px; background: #f9f9f9;">0</td>
        </tr>'''
    return rows

def gen_poligonos():
    polys = ""
    btn_s = "cursor:pointer; border:none; background:rgba(0,0,0,0.1); color:#333; font-weight:bold; width:24px; height:24px; border-radius:4px;"
    fila_inner = f'''
    <tr class="calc-row">
        <td class="u-manual-cell" style="background: #e3defa; text-align: center; border: 0.6px solid #ccc; padding: 8px;">
            <button style="{btn_s}" onclick="stepVal(this, -1, 'u')">-</button>
            <span contenteditable="true" class="u-manual" oninput="manualEdit(this)" style="font-weight: bold; margin: 0 8px;">0</span>
            <button style="{btn_s}" onclick="stepVal(this, 1, 'u')">+</button>
        </td>
        <td class="spr-real-cell" style="background: #def3ed; text-align: center; border: 0.6px solid #ccc; padding: 8px;">
            <button style="{btn_s}" onclick="stepVal(this, -1, 's')">-</button>
            <span contenteditable="true" class="spr-real-val" oninput="manualEdit(this)" style="font-weight: bold; margin: 0 8px;">0</span>
            <button style="{btn_s}" onclick="stepVal(this, 1, 's')">+</button>
        </td>
        <td style="border: 0.5px solid #ccc; padding: 2px;"><select class="s-type" onchange="resetRow(this)" style="width:100%; border:none; background:transparent; font-weight:bold; font-size:12px;"><option>SELECCIONAR...</option></select></td>
        <td style="text-align: center; border: 0.5px solid #ccc;"><input type="checkbox" class="ok-check" style="transform: scale(1.4);"></td>
    </tr>'''
    
    for i in range(1, 11):
        polys += f'''
        <div class="poligono-bloque" style="margin-bottom: 25px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); border-radius: 10px; overflow: hidden; background: white;">
            <table style="width: 100%; border-collapse: collapse;">
                <thead>
                    <tr style="background: #20B2AA; color: white; font-size: 13px; height: 40px;">
                        <th style="width: 120px;">PLAN / RUTA</th>
                        <th style="width: 100px;">VOL. TOTAL</th>
                        <th style="width: 130px;"># ASIGNADAS</th>
                        <th style="width: 130px;">SPR REAL</th>
                        <th>TIPO DE UNIDAD</th>
                        <th style="width: 50px;">OK</th>
                    </tr>
                </thead>
                <tbody>
                    <tr class="calc-row">
                        <td rowspan="5" contenteditable="true" style="background: #f8f9fa; font-weight:bold; text-align:center; border: 1px solid #ccc;">PLAN {i}</td>
                        <td rowspan="5" contenteditable="true" class="v-total-val" oninput="recalc()" style="color: #20B2AA; font-weight: bold; font-size: 22px; text-align: center; border: 1px solid #ccc;">0</td>
                        <td class="u-manual-cell" style="background: #e3defa; text-align: center; border: 0.5px solid #ccc;">
                            <button style="{btn_s}" onclick="stepVal(this, -1, 'u')">-</button>
                            <span contenteditable="true" class="u-manual" oninput="manualEdit(this)" style="font-weight: bold; margin: 0 8px;">0</span>
                            <button style="{btn_s}" onclick="stepVal(this, 1, 'u')">+</button>
                        </td>
                        <td class="spr-real-cell" style="background: #def3ed; text-align: center; border: 0.5px solid #ccc;">
                            <button style="{btn_s}" onclick="stepVal(this, -1, 's')">-</button>
                            <span contenteditable="true" class="spr-real-val" oninput="manualEdit(this)" style="font-weight: bold; margin: 0 8px;">0</span>
                            <button style="{btn_s}" onclick="stepVal(this, 1, 's')">+</button>
                        </td>
                        <td style="border: 0.5px solid #ccc; padding: 2px;"><select class="s-type" onchange="resetRow(this)" style="width:100%; border:none; background:transparent; font-weight:bold; font-size:12px;"><option>SELECCIONAR...</option></select></td>
                        <td style="text-align: center; border: 0.5px solid #ccc;"><input type="checkbox" class="ok-check" style="transform: scale(1.4);"></td>
                    </tr>
                    {fila_inner}{fila_inner}{fila_inner}{fila_inner}
                    <tr style="background:#333; color: white;">
                        <td colspan="2" style="text-align:center; font-weight:bold; border: 1px solid #444;">DIFERENCIA:</td>
                        <td class="v-calculado-total" style="font-weight: bold; font-size: 18px; color: #00ffcc; border: 1px solid #444; text-align: center;">0</td>
                        <td class="p-diff" colspan="3" style="text-align: center; font-weight: bold; border: 1px solid #444; color: #ffeb3b;">ESPERANDO DATOS</td>
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
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f0f2f5; padding: 20px; }}
        .filter-btn {{ cursor: pointer; font-size: 12px; padding: 8px 15px; border-radius: 6px; font-weight: bold; border: none; }}
        .btn-activas {{ background: #2ecc71; color: white; box-shadow: 0 4px #27ae60; margin-right: 10px; }}
        .btn-todas {{ background: #95a5a6; color: white; box-shadow: 0 4px #7f8c8d; }}
        .meli-table {{ border-collapse: collapse; width: 100%; background: white; }}
        .meli-table th {{ background: #333; color: white; font-size: 11px; padding: 8px 2px; }}
        .tab-btn {{ padding: 10px 25px; cursor: pointer; border: none; background: #ddd; border-radius: 5px 5px 0 0; font-weight: bold; }}
        .tab-btn.active {{ background: #333; color: white; }}
        
        /* HERRAMIENTAS */
        #calc_wrapper {{ background: #20B2AA; border-radius: 15px; padding: 15px; margin-top: 20px; box-shadow: 0 4px 10px rgba(0,0,0,0.2); }}
        .calc-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; }}
        .btn-c {{ background: white; border: none; padding: 12px; border-radius: 8px; cursor: pointer; font-weight: bold; font-size: 16px; }}
        .btn-c:active {{ background: #eee; }}
        .crono-card {{ background: #1a1a1a; color: #00ff00; padding: 15px; border-radius: 12px; text-align: center; font-family: 'Courier New', Courier, monospace; margin-top: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.3); }}
    </style>
</head>
<body>

<div style="display: flex; gap: 25px;">
    <div style="flex: 1.2;">
        <div style="background: #20B2AA; color: white; padding: 12px; border-radius: 8px; text-align: center; font-weight: bold; margin-bottom: 15px; font-size: 18px;">
            ASIGNACIÓN DE POLÍGONOS Y RUTAS
        </div>
        <div id="polys-2" class="p-content">{gen_poligonos()}</div>
        <div id="polys-3" class="p-content" style="display:none;">{gen_poligonos()}</div>
        <div id="polys-1" class="p-content" style="display:none;">{gen_poligonos()}</div>
        <div id="polys-4" class="p-content" style="display:none;">{gen_poligonos()}</div>
    </div>

    <div style="width: 450px;">
        <div style="background: #333; color: white; padding: 12px; border-radius: 8px; font-weight: bold; text-align: center; margin-bottom: 15px;">
            ESTADO DE DISPONIBILIDAD
        </div>
        
        <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 5px;">
            <div>
                <button class="tab-btn active" onclick="showTab(2, this)">C1</button>
                <button class="tab-btn" onclick="showTab(3, this)">C2</button>
                <button class="tab-btn" onclick="showTab(1, this)">SD</button>
                <button class="tab-btn" onclick="showTab(4, this)">SDE</button>
            </div>
            <div style="padding-bottom: 8px;">
                <button onclick="filterRows(true)" class="filter-btn btn-activas">ACTIVAS</button>
                <button onclick="filterRows(false)" class="filter-btn btn-todas">TODAS</button>
            </div>
        </div>

        <div id="tab-2" class="t-content">
            <table class="meli-table">
                <thead>
                    <tr><th rowspan="2">UNIDAD</th><th colspan="2">SPR BASE</th><th rowspan="2">MINS</th><th rowspan="2">STOCK</th><th rowspan="2">REST</th></tr>
                    <tr><th>MIN</th><th>MAX</th></tr>
                </thead>
                <tbody id="body-2">{gen_master_rows(u_C1, 2)}</tbody>
            </table>
        </div>
        <div id="tab-3" class="t-content" style="display:none;"><table class="meli-table"><tbody id="body-3">{gen_master_rows(u_C2, 3)}</tbody></table></div>
        <div id="tab-1" class="t-content" style="display:none;"><table class="meli-table"><tbody id="body-1">{gen_master_rows(u_SD, 1)}</tbody></table></div>
        <div id="tab-4" class="t-content" style="display:none;"><table class="meli-table"><tbody id="body-4">{gen_master_rows(u_SDE, 4)}</tbody></table></div>

        <!-- CALCULADORA RESTAURADA -->
        <div id="calc_wrapper">
            <div style="background:rgba(255,255,255,0.95); padding:12px; border-radius:8px; text-align:right; margin-bottom:12px; font-size:26px; font-weight:bold; min-height:45px; color:#333; box-shadow: inset 0 2px 5px rgba(0,0,0,0.1);" id="calc_r">0</div>
            <div class="calc-grid">
                <button onclick="an('7')" class="btn-c">7</button><button onclick="an('8')" class="btn-c">8</button><button onclick="an('9')" class="btn-c">9</button><button onclick="ao('/')" class="btn-c">÷</button>
                <button onclick="an('4')" class="btn-c">4</button><button onclick="an('5')" class="btn-c">5</button><button onclick="an('6')" class="btn-c">6</button><button onclick="ao('*')" class="btn-c">×</button>
                <button onclick="an('1')" class="btn-c">1</button><button onclick="an('2')" class="btn-c">2</button><button onclick="an('3')" class="btn-c">3</button><button onclick="ao('-')" class="btn-c">-</button>
                <button onclick="cl()" class="btn-c" style="color:#d32f2f; font-weight:900;">AC</button><button onclick="an('0')" class="btn-c">0</button><button onclick="calc_eq()" class="btn-c" style="background:#333; color:white;">=</button><button onclick="ao('+')" class="btn-c">+</button>
            </div>
        </div>

        <!-- CRONÓMETRO RESTAURADO -->
        <div class="crono-card">
            <div id="crono-main" style="font-size:36px; font-weight:bold; margin-bottom:12px; letter-spacing:2px;">00:00:00</div>
            <div style="display: flex; gap: 8px; justify-content: center;">
                <button onclick="startC()" style="background:#2ecc71; border:none; padding:10px 20px; border-radius:6px; color:white; cursor:pointer; font-weight:bold;">INICIAR</button>
                <button onclick="stopC()" style="background:#e74c3c; border:none; padding:10px 20px; border-radius:6px; color:white; cursor:pointer; font-weight:bold;">PAUSA</button>
                <button onclick="resetC()" style="background:#f1c40f; border:none; padding:10px 20px; border-radius:6px; color:white; cursor:pointer; font-weight:bold;">BORRAR</button>
            </div>
        </div>
    </div>
</div>

<script>
    let currentTab = 2;
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

    function stepVal(btn, delta, type) {{
        let row = btn.closest('tr');
        let span = type === 'u' ? row.querySelector('.u-manual') : row.querySelector('.spr-real-val');
        let val = parseFloat(span.innerText) || 0;
        span.innerText = Math.max(0, val + delta).toFixed(type === 'u' ? 0 : 1);
        recalc();
    }}

    function recalc() {{
        let fleet = {{}};
        document.querySelectorAll('#body-' + currentTab + ' tr').forEach(row => {{
            let name = row.querySelector('.edit-name').innerText.trim();
            let stock = parseInt(row.querySelector('.f-stock').innerText) || 0;
            if(name !== "NUEVA UNIDAD") fleet[name] = {{ stock: stock, used: 0 }};
        }});

        document.querySelectorAll('#polys-' + currentTab + ' .poligono-bloque').forEach(bl => {{
            let vT = parseFloat(bl.querySelector('.v-total-val').innerText) || 0;
            let sumU = 0;
            bl.querySelectorAll('.calc-row').forEach(r => {{
                let s = r.querySelector('.s-type').value;
                let u = parseInt(r.querySelector('.u-manual').innerText) || 0;
                if(fleet[s]) {{ fleet[s].used += u; sumU += u; }}
            }});
            bl.querySelector('.v-calculado-total').innerText = sumU;
        }});
        
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
    
    recalc();
</script>
</body>
</html>
"""

html(app_html, height=1200, scrolling=True)
