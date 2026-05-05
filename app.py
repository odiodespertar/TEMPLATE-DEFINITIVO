import streamlit as st
from streamlit.components.v1 import html

st.set_page_config(page_title="Monitor Logístico - Liliana García", layout="wide")

# Estilos base para limpiar Streamlit
st.markdown("""
    <style>
    .block-container {padding: 0rem !important;}
    footer, #MainMenu, header {visibility: hidden;}
    body { background-color: #f0f2f5; }
    </style>
""", unsafe_allow_html=True)

# Datos de Flota
u_C1 = {
    "RENTAL ELEC LARGE VAN": [120, 120], "RENTAL ELEC SMALL VAN": [120, 120], 
    "RENTAL LARGE VAN": [120, 120], "RENTAL SMALL VAN": [120, 120], 
    "LARGE VAN VAR(MLP)": [100, 100], "SMALL VAN VAR(MLP)":[80, 80],
    "CAR MLP": [50, 50], "MOTO 3 HRS": [28, 28], 
    "CROWD NEWBIE 3 hrs": [30, 30], "CROWD EXTRA 8 HRS": [80, 85], "CROWD 5 HRS": [60, 60]
}

def gen_master_rows():
    rows = ""
    items = list(u_C1.items())
    for i in range(14):
        is_real = i < len(items)
        name, spr = (items[i][0], items[i][1]) if is_real else ("NUEVA UNIDAD", [0, 0])
        rows += f'''
        <tr class="master-row">
            <td contenteditable="true" class="edit-name" style="text-align:left; padding-left:10px;">{name}</td>
            <td contenteditable="true" class="edit-spr-min" style="color:#20B2AA; font-weight:bold;">{spr[0]}</td>
            <td contenteditable="true" class="edit-spr-max" style="color:#20B2AA; font-weight:bold;">{spr[1]}</td>
            <td contenteditable="true">480</td>
            <td contenteditable="true" class="f-stock" oninput="recalc()">0</td>
            <td class="f-left" style="font-weight:bold; color:#2e7d32;">0</td>
        </tr>'''
    return rows

def gen_poligonos():
    polys = ""
    fila_input = '''
    <tr class="calc-row">
        <td class="u-manual-cell">
            <div class="btn-group"><button onclick="step(this,-1)">-</button><span class="u-manual">0</span><button onclick="step(this,1)">+</button></div>
        </td>
        <td class="spr-real-cell">
            <div class="btn-group"><button onclick="step(this,-1)">-</button><span class="spr-real-val">0</span><button onclick="step(this,1)">+</button></div>
        </td>
        <td><select class="s-type" onchange="resetRow(this)"><option>SELECCIONAR...</option></select></td>
        <td><input type="checkbox" class="ok-check"></td>
    </tr>'''
    for i in range(1, 11):
        polys += f'''
        <div class="card-poly">
            <table class="meli-table">
                <thead>
                    <tr class="header-plan">
                        <th style="width:60px;">PLAN {i}</th><th style="width:80px;">VOL. TOTAL</th><th style="width:110px;"># ASIGNADAS</th><th style="width:110px;">SPR REAL</th><th style="width:200px;">TIPO DE UNIDAD</th><th style="width:40px;">OK</th>
                    </tr>
                </thead>
                <tbody>
                    <tr class="calc-row">
                        <td rowspan="5" class="plan-side-label">PLAN {i}</td>
                        <td rowspan="5" contenteditable="true" class="v-total-val" oninput="recalc()">0</td>
                        <td class="u-manual-cell">
                            <div class="btn-group"><button onclick="step(this,-1)">-</button><span class="u-manual">0</span><button onclick="step(this,1)">+</button></div>
                        </td>
                        <td class="spr-real-cell">
                            <div class="btn-group"><button onclick="step(this,-1)">-</button><span class="spr-real-val">0</span><button onclick="step(this,1)">+</button></div>
                        </td>
                        <td><select class="s-type" onchange="resetRow(this)"><option>SELECCIONAR...</option></select></td>
                        <td><input type="checkbox" class="ok-check"></td>
                    </tr>
                    {fila_input * 4}
                    <tr class="footer-row">
                        <td colspan="1" style="font-weight:bold; background:#f9f9f9;">ESTADO:</td>
                        <td class="v-calculado-total" style="font-weight:bold; color:red;">0</td>
                        <td class="p-diff" colspan="3" style="font-weight:bold;">VACÍO</td>
                    </tr>
                </tbody>
            </table>
        </div>'''
    return polys

# --- INTERFAZ COMPLETA ---
full_html = f"""
<!DOCTYPE html>
<html>
<head>
<style>
    body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f0f2f5; padding: 20px; width: 1400px; margin: auto; }}
    .layout {{ display: flex; gap: 20px; align-items: flex-start; }}
    
    /* Tablas y Tarjetas */
    .card-poly {{ background: white; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); padding: 5px; margin-bottom: 20px; border: 1px solid #ccc; }}
    .meli-table {{ border-collapse: collapse; width: 100%; table-layout: fixed; border-radius: 8px; overflow: hidden; }}
    .meli-table th, .meli-table td {{ border: 1px solid #ddd; font-size: 11px; height: 32px; text-align: center; }}
    .header-plan {{ background: #6d6d6d; color: white; text-transform: uppercase; }}
    .plan-side-label {{ background: #f1f1f1; font-weight: bold; font-size: 12px; }}
    
    /* Estilos Celdas */
    .v-total-val {{ font-size: 18px; color: #17a2b8; font-weight: bold; background: #fff; }}
    .u-manual-cell {{ background: #eeebff; }}
    .spr-real-cell {{ background: #e8f7f3; }}
    
    /* Botones +/- dentro de celda */
    .btn-group {{ display: flex; align-items: center; justify-content: center; gap: 8px; }}
    .btn-group button {{ border: 1px solid #ccc; background: white; border-radius: 4px; width: 22px; height: 22px; cursor: pointer; font-weight: bold; }}
    .btn-group button:hover {{ background: #f0f0f0; }}

    /* Columna Derecha */
    .right-col {{ width: 500px; position: sticky; top: 10px; display: flex; flex-direction: column; gap: 15px; }}
    .flota-header {{ background: #1a1a1a; color: white; padding: 12px; border-radius: 10px 10px 0 0; text-align: center; font-weight: bold; font-size: 14px; }}
    
    /* Convertidor */
    .tool-box {{ background: #e0dbff; border: 1px solid #c5bcff; border-radius: 15px; padding: 12px; text-align: center; }}
    .conv-input {{ width: 60px; border-radius: 5px; border: 1px solid #aaa; text-align: center; padding: 3px; }}

    /* Calculadora Estilo Imagen */
    .calc-container {{ background: #22c5bc; border-radius: 25px; padding: 15px; border: 3px solid #1a1a1a; box-shadow: 0 5px 15px rgba(0,0,0,0.2); }}
    #display {{ background: #fff9c4; border-radius: 10px; padding: 15px; text-align: right; font-size: 24px; font-weight: bold; margin-bottom: 10px; height: 40px; border: 2px solid #555; }}
    .calc-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; }}
    .btn {{ background: white; border: none; padding: 12px; border-radius: 10px; font-weight: bold; font-size: 16px; cursor: pointer; transition: 0.2s; }}
    .btn:active {{ background: #ff00ff; color: white; }}
    .btn-op {{ background: #f0f0f0; }}

    /* Cronómetro Negro */
    .timer-box {{ background: #1a1a1a; color: white; border-radius: 15px; padding: 15px; text-align: center; font-family: 'Courier New', monospace; box-shadow: 0 4px 10px rgba(0,0,0,0.5); }}
    .time-display {{ font-size: 32px; font-weight: bold; color: #fff; margin: 10px 0; }}
    .timer-btns button {{ padding: 5px 12px; margin: 0 5px; border-radius: 5px; border: none; cursor: pointer; font-weight: bold; }}
</style>
</head>
<body>

<div class="layout">
    <div style="width: 850px;">
        <div style="background:#6d6d6d; color:white; padding:12px; border-radius:10px; text-align:center; font-weight:bold; margin-bottom:15px; font-size:16px;">📋 PLANES GENERADOS</div>
        {gen_poligonos()}
    </div>

    <div class="right-col">
        <!-- FLOTA -->
        <div class="card-poly" style="padding:0; margin-bottom:0;">
            <div class="flota-header">🚚🚚 DISPONIBILIDAD DE FLOTA 🚚🚚</div>
            <div style="padding:10px; display:flex; gap:5px; background:#f9f9f9;">
                <button style="flex:1; padding:5px; font-weight:bold; border-radius:5px; background:#000; color:#fff;">C1</button>
                <button style="flex:1; padding:5px; font-weight:bold; border-radius:5px; background:#ddd;">C2</button>
                <button style="flex:1; padding:5px; font-weight:bold; border-radius:5px; background:#ddd;">SD</button>
                <button style="background:#22c5bc; color:white; border:none; padding:5px 15px; border-radius:5px; font-weight:bold;">TODAS</button>
            </div>
            <table class="meli-table" style="border:none;">
                <thead style="background:#222; color:white;">
                    <tr><th style="width:160px;">UNIDADES</th><th>min</th><th>max</th><th>ORH</th><th>SCHED</th><th>QUEDAN</th></tr>
                </thead>
                <tbody id="fleet-body">{gen_master_rows()}</tbody>
            </table>
        </div>

        <!-- CONVERTIDOR -->
        <div class="tool-box">
            <span style="font-size:11px; font-weight:bold; color:#4e3396;">🔮 CONVERTIDOR DE TIEMPO</span><br>
            <input type="number" class="conv-input" id="min-in" oninput="convertTime()" placeholder="Min">
            <span id="time-res" style="font-size:22px; font-weight:bold; color:#9c27b0; margin-left:15px;">0h 0m</span>
        </div>

        <!-- CALCULADORA AQUA -->
        <div class="calc-container">
            <div id="display">0</div>
            <div class="calc-grid">
                <button class="btn btn-op" onclick="cl()" style="grid-column: span 2;">AC</button>
                <button class="btn btn-op" onclick="del()">⌫</button>
                <button class="btn btn-op" onclick="op('/')">÷</button>
                <button class="btn" onclick="num('7')">7</button><button class="btn" onclick="num('8')">8</button><button class="btn" onclick="num('9')">9</button><button class="btn btn-op" onclick="op('*')">×</button>
                <button class="btn" onclick="num('4')">4</button><button class="btn" onclick="num('5')">5</button><button class="btn" onclick="num('6')">6</button><button class="btn btn-op" onclick="op('-')">-</button>
                <button class="btn" onclick="num('1')">1</button><button class="btn" onclick="num('2')">2</button><button class="btn" onclick="num('3')">3</button><button class="btn btn-op" onclick="op('+')">+</button>
                <button class="btn" onclick="num('0')" style="grid-column: span 2;">0</button>
                <button class="btn" onclick="eq()" style="background:#ff00ff; color:white;">=</button>
            </div>
        </div>

        <!-- CRONÓMETRO NEGRO (DEBAJO) -->
        <div class="timer-box">
            <div style="display:flex; justify-content:space-between; font-size:10px; color:#17a2b8;">
                <span>HORA ACTUAL</span>
                <span id="wall-clock">00:00:00</span>
            </div>
            <div class="time-display" id="stopwatch">00:00:00.0</div>
            <div class="timer-btns">
                <button style="background:#2e7d32; color:white;" onclick="startT()">▶</button>
                <button style="background:#f9a825; color:white;" onclick="pauseT()">II</button>
                <button style="background:#c62828; color:white;" onclick="resetT()">🔄</button>
            </div>
        </div>
    </div>
</div>

<script>
    // --- LÓGICA CALCULADORA ---
    let expression = "";
    function num(n) {{ expression += n; updateDisp(); }}
    function op(o) {{ expression += " " + o + " "; updateDisp(); }}
    function cl() {{ expression = ""; updateDisp(); }}
    function del() {{ expression = expression.trim().slice(0, -1); updateDisp(); }}
    function updateDisp() {{ document.getElementById('display').innerText = expression || "0"; }}
    function eq() {{ try {{ expression = eval(expression).toString(); updateDisp(); }} catch {{ expression = "Error"; updateDisp(); }} }}

    // --- LÓGICA LOGÍSTICA ---
    function step(btn, delta) {{
        let span = btn.parentNode.querySelector('span');
        let val = parseInt(span.innerText) || 0;
        span.innerText = Math.max(0, val + delta);
        recalc();
    }}

    function recalc() {{
        let fleet = {{}};
        document.querySelectorAll('#fleet-body tr').forEach(r => {{
            let name = r.querySelector('.edit-name').innerText.trim();
            let stock = parseInt(r.querySelector('.f-stock').innerText) || 0;
            if(name !== "NUEVA UNIDAD") fleet[name] = {{ stock: stock, used: 0 }};
        }});

        document.querySelectorAll('.card-poly').forEach(card => {{
            let vTotal = parseFloat(card.querySelector('.v-total-val')?.innerText) || 0;
            let vCalculado = 0;
            
            card.querySelectorAll('.calc-row').forEach(row => {{
                let type = row.querySelector('.s-type').value;
                let q = parseInt(row.querySelector('.u-manual').innerText) || 0;
                let spr = parseFloat(row.querySelector('.spr-real-val').innerText) || 0;
                
                if(fleet[type]) {{
                    fleet[type].used += q;
                    vCalculado += (q * spr);
                }}
            }});

            let resDisp = card.querySelector('.v-calculado-total');
            if(resDisp) {{
                resDisp.innerText = Math.round(vCalculado);
                let diffLabel = card.querySelector('.p-diff');
                if(vCalculado >= vTotal && vTotal > 0) {{
                    diffLabel.innerText = "OK"; diffLabel.style.background = "#d4edda";
                }} else {{
                    diffLabel.innerText = vTotal > 0 ? "FALTAN: " + Math.round(vTotal - vCalculado) : "VACÍO";
                    diffLabel.style.background = "#f8d7da";
                }}
            }}
        }});

        document.querySelectorAll('#fleet-body tr').forEach(r => {{
            let name = r.querySelector('.edit-name').innerText.trim();
            if(fleet[name]) {{
                r.querySelector('.f-left').innerText = fleet[name].stock - fleet[name].used;
            }}
        }});

        // Actualizar Selects dinámicamente
        document.querySelectorAll('.s-type').forEach(sel => {{
            let current = sel.value;
            let options = '<option>SELECCIONAR...</option>';
            Object.keys(fleet).forEach(k => {{
                if(fleet[k].stock > 0 || k === current) options += `<option value="${{k}}">${{k}}</option>`;
            }});
            sel.innerHTML = options; sel.value = current;
        }});
    }}

    function resetRow(sel) {{
        let row = sel.closest('tr');
        row.querySelector('.u-manual').innerText = "0";
        row.querySelector('.spr-real-val').innerText = "0";
        recalc();
    }}

    function convertTime() {{
        let m = document.getElementById('min-in').value || 0;
        document.getElementById('time-res').innerText = Math.floor(m/60) + "h " + (m%60) + "m";
    }}

    // --- CRONÓMETRO ---
    let startTime, elapsedTime = 0, timerInterval;
    function startT() {{
        if(!timerInterval) {{
            startTime = Date.now() - elapsedTime;
            timerInterval = setInterval(updateT, 100);
        }}
    }}
    function pauseT() {{ clearInterval(timerInterval); timerInterval = null; }}
    function resetT() {{ pauseT(); elapsedTime = 0; document.getElementById('stopwatch').innerText = "00:00:00.0"; }}
    function updateT() {{
        elapsedTime = Date.now() - startTime;
        let diff = elapsedTime;
        let ms = Math.floor((diff % 1000) / 100);
        let s = Math.floor((diff / 1000) % 60);
        let m = Math.floor((diff / 60000) % 60);
        let h = Math.floor(diff / 3600000);
        document.getElementById('stopwatch').innerText = 
            (h<10?'0':'')+h+":"+(m<10?'0':'')+m+":"+(s<10?'0':'')+s+"."+ms;
    }}
    setInterval(() => {{
        document.getElementById('wall-clock').innerText = new Date().toLocaleTimeString();
    }}, 1000);

    recalc();
</script>
</body>
</html>
"""

html(full_html, width=1450, height=1800, scrolling=True)
