import streamlit as st
from streamlit.components.v1 import html

# 1. CONFIGURACIÓN DE LA PÁGINA STREAMLIT
st.set_page_config(page_title="Monitor Logístico - Liliana García", layout="wide")

# Ocultar elementos nativos de Streamlit para que parezca una web profesional
st.markdown("""
    <style>
    .block-container {padding: 0rem !important;}
    footer, #MainMenu, header {visibility: hidden;}
    body { background-color: #f5f7f9; }
    </style>
""", unsafe_allow_html=True)

# 2. DEFINICIÓN DE DATOS (CATÁLOGOS)
u_C1 = {
    "RENTAL ELEC LARGE VAN": [120, 120], "RENTAL ELEC SMALL VAN": [120, 120], 
    "RENTAL LARGE VAN": [120, 120], "RENTAL SMALL VAN": [120, 120], 
    "LARGE VAN VAR(MLP)": [100, 100], "SMALL VAN VAR(MLP)":[80, 80],
    "CAR MLP": [50, 50], "MOTO 3 HRS": [28, 28], 
    "CROWD NEWBIE 3 hrs": [30, 30], "CROWD EXTRA 8 HRS": [80, 85], "CROWD 5 HRS": [60, 60]
}
u_SD = {"MOTO 3 HRS": [25, 25], "MOTO NEWBIE": [20, 22], "CROWD 5 HRS / SMALL VAN": [35, 37]}

# 3. FUNCIONES GENERADORAS DE HTML
def gen_master_rows(data_dict):
    rows = ""
    items = list(data_dict.items())
    for i in range(12): # 12 filas fijas para disponibilidad
        is_real = i < len(items)
        name, spr = (items[i][0], items[i][1]) if is_real else ("NUEVA UNIDAD", [0, 0])
        rows += f'''
        <tr class="master-row">
            <td contenteditable="true" class="edit-name">{name}</td>
            <td contenteditable="true" class="edit-spr-min">{spr[0]}</td>
            <td contenteditable="true" class="edit-spr-max">{spr[1]}</td>
            <td contenteditable="true" class="edit-orh">480</td>
            <td contenteditable="true" class="f-stock" oninput="recalc()">0</td>
            <td class="f-left">0</td>
        </tr>'''
    return rows

def gen_poligonos():
    polys = ""
    for i in range(1, 11): # 10 polígonos
        polys += f'''
        <div class="poligono-bloque">
            <table class="meli-table">
                <thead>
                    <tr class="header-plan">
                        <th style="width:60px;">PLAN {i}</th><th style="width:70px;">VOL.</th><th style="width:90px;">ASIGNADAS</th><th style="width:90px;">SPR REAL</th><th style="width:180px;">TIPO UNIDAD</th><th style="width:35px;">OK</th>
                    </tr>
                </thead>
                <tbody>
                    <tr class="calc-row">
                        <td rowspan="3" class="plan-label">PLAN {i}</td>
                        <td rowspan="3" contenteditable="true" class="v-total-val" oninput="recalc()">0</td>
                        <td class="u-manual-cell"><button onclick="step(this,-1,'u')">-</button><span contenteditable="true" class="u-manual">0</span><button onclick="step(this,1,'u')">+</button></td>
                        <td class="spr-real-cell"><button onclick="step(this,-1,'s')">-</button><span contenteditable="true" class="spr-real-val">0</span><button onclick="step(this,1,'s')">+</button></td>
                        <td><select class="s-type" onchange="resetRow(this)"><option>SELECCIONAR...</option></select></td>
                        <td><input type="checkbox"></td>
                    </tr>
                    <tr class="calc-row">
                        <td class="u-manual-cell"><button onclick="step(this,-1,'u')">-</button><span contenteditable="true" class="u-manual">0</span><button onclick="step(this,1,'u')">+</button></td>
                        <td class="spr-real-cell"><button onclick="step(this,-1,'s')">-</button><span contenteditable="true" class="spr-real-val">0</span><button onclick="step(this,1,'s')">+</button></td>
                        <td><select class="s-type" onchange="resetRow(this)"><option>SELECCIONAR...</option></select></td>
                        <td><input type="checkbox"></td>
                    </tr>
                    <tr class="footer-row">
                        <td colspan="1" style="font-size:9px;">CALC:</td><td class="v-calculado-total">0</td><td class="p-diff" colspan="2">VACÍO</td>
                    </tr>
                </tbody>
            </table>
        </div>'''
    return polys

# 4. ENSAMBLAJE FINAL (CSS + HTML + JS)
app_interface = f"""
<!DOCTYPE html>
<html>
<head>
<style>
    body {{ font-family: 'Segoe UI', sans-serif; background: #f5f7f9; width: 1280px; margin: auto; padding: 20px; }}
    .main-grid {{ display: flex; gap: 20px; }}
    
    /* Tablas Estilo Colab */
    .meli-table {{ border-collapse: collapse; width: 100%; table-layout: fixed; background: white; margin-bottom: 15px; border: 1px solid #ccc; }}
    .meli-table th, .meli-table td {{ border: 1px solid #ccc; font-size: 11px; height: 30px; text-align: center; }}
    .header-plan {{ background: #696969; color: white; }}
    .u-manual-cell {{ background: #e3defa; font-weight: bold; }}
    .spr-real-cell {{ background: #def3ed; font-weight: bold; }}
    .v-total-val {{ color: #20B2AA; font-weight: bold; font-size: 16px; }}

    /* Herramientas Derecha */
    .right-column {{ width: 450px; position: sticky; top: 10px; }}
    .google-tool {{ background: #dfdff5; padding: 15px; border-radius: 12px; margin-top: 10px; border: 1px solid #ccc; text-align: center; }}
    #calc_wrapper {{ background: #22c5bc; border-radius: 20px; padding: 15px; margin-top: 10px; border: 2px solid #333; }}
    .calc-btn {{ background: white; border: none; padding: 10px; border-radius: 8px; font-weight: bold; cursor: pointer; }}
    .calc-btn:active {{ background: #FF00FF; color: white; }}
    
    #alert-box {{ position: fixed; top: -100px; left: 50%; transform: translateX(-50%); background: #d32f2f; color: white; padding: 15px; border-radius: 8px; transition: 0.4s; z-index: 100; }}
    #alert-box.show {{ top: 20px; }}
</style>
</head>
<body>

<div id="alert-box">⚠️ <span id="msg"></span> [ENTER para cerrar]</div>

<div class="main-grid">
    <div style="width: 800px;">
        <div style="background:#696969; color:white; padding:10px; border-radius:8px; text-align:center; font-weight:bold; margin-bottom:10px;">📋 POLÍGONOS DE REPARTO</div>
        {gen_poligonos()}
    </div>

    <div class="right-column">
        <div style="background:#000; color:white; padding:10px; border-radius:8px; text-align:center; font-weight:bold;">🚚 FLOTA DISPONIBLE</div>
        <table class="meli-table" style="margin-top:10px;">
            <thead style="background:#333; color:white;">
                <tr><th style="width:140px;">UNIDAD</th><th style="width:40px;">MIN</th><th style="width:40px;">MAX</th><th style="width:40px;">SCH</th><th style="width:50px;">RESTO</th></tr>
            </thead>
            <tbody id="f-body">{gen_master_rows(u_C1)}</tbody>
        </table>

        <div class="google-tool">
            <div style="font-weight:bold; font-size:11px;">⏱️ MINUTOS A HORAS</div>
            <input type="number" id="m-in" oninput="conv()" style="width:60px; text-align:center; border-radius:4px; border:1px solid #ccc;">
            <span id="t-res" style="font-size:20px; font-weight:bold; color:#4e3396; margin-left:10px;">0h 0m</span>
        </div>

        <div id="calc_wrapper">
            <div id="d" style="background: #fffacd; padding: 10px; text-align: right; border-radius: 8px; font-weight: bold; font-size: 20px; margin-bottom:10px;">0</div>
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px;">
                <button class="calc-btn" onclick="c('7')">7</button><button class="calc-btn" onclick="c('8')">8</button><button class="calc-btn" onclick="c('9')">9</button><button class="calc-btn" onclick="o('/')">/</button>
                <button class="calc-btn" onclick="c('4')">4</button><button class="calc-btn" onclick="c('5')">5</button><button class="calc-btn" onclick="c('6')">6</button><button class="calc-btn" onclick="o('*')">*</button>
                <button class="calc-btn" onclick="c('1')">1</button><button class="calc-btn" onclick="c('2')">2</button><button class="calc-btn" onclick="c('3')">3</button><button class="calc-btn" onclick="o('-')">-</button>
                <button class="calc-btn" onclick="cl()">AC</button><button class="calc-btn" onclick="c('0')">0</button><button class="calc-btn" onclick="e()" style="background:#FF00FF; color:white;">=</button><button class="calc-btn" onclick="o('+')">+</button>
            </div>
        </div>
    </div>
</div>

<script>
    let cur = "";
    function c(n) {{ cur += n; ud(); }}
    function o(op) {{ cur += " " + op + " "; ud(); }}
    function cl() {{ cur = ""; ud(); }}
    function ud() {{ document.getElementById('d').innerText = cur || "0"; }}
    function e() {{ try {{ cur = eval(cur).toString(); ud(); }} catch {{ cur = "Error"; ud(); }} }}
    
    function conv() {{
        let m = document.getElementById('m-in').value || 0;
        document.getElementById('t-res').innerText = Math.floor(m/60) + "h " + (m%60) + "m";
    }}

    function recalc() {{
        let f = {{}};
        document.querySelectorAll('#f-body tr').forEach(r => {{
            let n = r.querySelector('.edit-name').innerText.trim();
            let s = parseInt(r.querySelector('.f-stock').innerText) || 0;
            let mx = parseFloat(r.querySelector('.edit-spr-max').innerText) || 0;
            if(n !== "NUEVA UNIDAD") f[n] = {{ s, mx, u: 0 }};
        }});

        document.querySelectorAll('.poligono-bloque').forEach(b => {{
            let vt = parseFloat(b.querySelector('.v-total-val').innerText) || 0;
            let va = 0;
            b.querySelectorAll('.calc-row').forEach(cr => {{
                let sel = cr.querySelector('.s-type').value;
                let u = parseInt(cr.querySelector('.u-manual').innerText) || 0;
                if(f[sel]) {{ f[sel].u += u; va += (u * parseFloat(cr.querySelector('.spr-real-val').innerText)); }}
            }});
            b.querySelector('.v-calculado-total').innerText = Math.round(va);
            let diff = b.querySelector('.p-diff');
            diff.innerText = (va >= vt) ? "OK" : "FALTA: " + Math.round(vt-va);
            diff.style.background = (va >= vt) ? "#ceedd6" : "#f7cdd1";
        }});

        document.querySelectorAll('#f-body tr').forEach(r => {{
            let n = r.querySelector('.edit-name').innerText.trim();
            if(f[n]) {{ r.querySelector('.f-left').innerText = f[n].s - f[n].u; }}
        }});

        // Actualizar Selects
        document.querySelectorAll('.s-type').forEach(s => {{
            let v = s.value;
            let h = '<option>SELECCIONAR...</option>';
            Object.keys(f).forEach(k => {{ if(f[k].s > 0 || k===v) h += `<option value="${{k}}">${{k}}</option>`; }});
            s.innerHTML = h; s.value = v;
        }});
    }}

    function step(b, d, t) {{
        let s = b.parentNode.querySelector('span');
        let v = parseFloat(s.innerText) || 0;
        s.innerText = Math.max(0, v + d);
        recalc();
    }}
    
    function resetRow(s) {{ s.closest('tr').querySelectorAll('span').forEach(sp => sp.innerText="0"); recalc(); }}
    document.addEventListener('keydown', e => {{ if(e.key === 'Enter') document.getElementById('alert-box').classList.remove('show'); }});
    recalc();
</script>
</body>
</html>
"""

# 5. RENDERIZADO EN STREAMLIT
html(app_interface, width=1300, height=1600, scrolling=True)
