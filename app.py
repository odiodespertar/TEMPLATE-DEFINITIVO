import streamlit as st
from streamlit.components.v1 import html

st.set_page_config(page_title="Monitor Logístico VP04 - Total Pro", layout="wide")

st.markdown("""
    <style>
    .block-container {padding: 0rem !important;}
    footer, #MainMenu, header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- CATÁLOGOS ---
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
        st_base = "background: #ebebeb; color: #555;" if is_real else "background: #fcfcfc; color: #ccc;"
        rows += f'''
        <tr data-table="{table_id}" class="master-row">
            <td contenteditable="true" class="edit-name" oninput="recalc()" style="{st_base} text-align: left; padding-left: 10px; border: 0.5px solid #ccc; font-weight: bold;">{name}</td>
            <td contenteditable="true" class="edit-spr-min" oninput="recalc()" style="{st_base} text-align: center; border: 0.5px solid #ccc;">{spr[0]}</td>
            <td contenteditable="true" class="edit-spr-max" oninput="recalc()" style="{st_base} text-align: center; border: 0.5px solid #ccc;">{spr[1]}</td>
            <td contenteditable="true" class="edit-orh" style="{st_base} text-align: center; border: 0.5px solid #ccc;">480</td>
            <td contenteditable="true" class="f-stock" oninput="recalc()" style="{st_base} text-align: center; border: 0.5px solid #ccc;">0</td>
            <td class="f-left" style="background: #fff; font-weight: bold; text-align: center; border: 0.5px solid #ccc;">0</td>
        </tr>'''
    return rows

def gen_poligonos():
    polys = ""
    btn_s = "cursor:pointer; border:none; background:rgba(0,0,0,0.1); font-weight:bold; width:22px; height:22px; border-radius:4px;"
    fila_inner = f'''
    <tr class="calc-row">
        <td class="u-manual-cell" style="background: #e3defa; text-align: center; border: 0.5px solid #ccc;">
            <button style="{btn_s}" onclick="stepVal(this, -1, 'u')">-</button>
            <span contenteditable="true" class="u-manual" oninput="manualEdit(this)">0</span>
            <button style="{btn_s}" onclick="stepVal(this, 1, 'u')">+</button>
        </td>
        <td class="spr-real-cell" style="background: #def3ed; text-align: center; border: 0.5px solid #ccc;">
            <button style="{btn_s}" onclick="stepVal(this, -1, 's')">-</button>
            <span contenteditable="true" class="spr-real-val" oninput="manualEdit(this)">0</span>
            <button style="{btn_s}" onclick="stepVal(this, 1, 's')">+</button>
        </td>
        <td style="border: 0.5px solid #ccc;"><select class="s-type" onchange="resetRow(this)" style="width:100%; border:none; background:transparent; font-weight:bold; color:#333;"><option>SELECCIONAR...</option></select></td>
        <td style="text-align: center; border: 0.5px solid #ccc;"><input type="checkbox" class="ok-check" style="transform: scale(1.8); cursor:pointer;"></td>
    </tr>'''
    for i in range(1, 11):
        polys += f'''
        <div class="poligono-bloque" style="margin-bottom: 15px; border-radius: 10px; overflow: hidden; background: white; border: 1px solid #ccc;">
            <table class="meli-table tabla-planes" style="width: 100%; border-collapse: collapse;">
                <thead>
                    <tr><th class="header-poly">PLAN {i}</th><th class="header-poly">VOL. TOTAL</th><th class="header-poly" style="width:100px;"># ASIGNADAS</th><th class="header-poly" style="width:100px;">SPR REAL</th><th class="header-poly">TIPO DE UNIDAD</th><th class="header-poly" style="width:55px;">OK</th></tr>
                </thead>
                <tbody>
                    <tr class="calc-row">
                        <td rowspan="5" contenteditable="true" class="v-total" style="background: #D3D3D3; font-weight:bold; text-align:center; border: 1px solid #808080;">P{i}</td>
                        <td rowspan="5" contenteditable="true" class="v-total-val" oninput="recalc()" style="color: #20B2AA; font-weight: bold; font-size: 16px; text-align: center; border: 1px solid #808080;">0</td>
                        <td class="u-manual-cell" style="background: #e3defa; text-align: center; border: 0.5px solid #ccc;">
                            <button style="{btn_s}" onclick="stepVal(this, -1, 'u')">-</button>
                            <span contenteditable="true" class="u-manual" oninput="manualEdit(this)">0</span>
                            <button style="{btn_s}" onclick="stepVal(this, 1, 'u')">+</button>
                        </td>
                        <td class="spr-real-cell" style="background: #def3ed; text-align: center; border: 0.5px solid #ccc;">
                            <button style="{btn_s}" onclick="stepVal(this, -1, 's')">-</button>
                            <span contenteditable="true" class="spr-real-val" oninput="manualEdit(this)">0</span>
                            <button style="{btn_s}" onclick="stepVal(this, 1, 's')">+</button>
                        </td>
                        <td style="border: 0.5px solid #ccc;"><select class="s-type" onchange="resetRow(this)" style="width:100%; border:none; background:transparent; font-weight:bold; color:#333;"><option>SELECCIONAR...</option></select></td>
                        <td style="text-align: center; border: 0.5px solid #ccc;"><input type="checkbox" class="ok-check" style="transform: scale(1.8); cursor:pointer;"></td>
                    </tr>
                    {fila_inner * 4}
                    <tr><td colspan="2" style="text-align:center; font-weight:bold; background:#f8f9fa; border: 1px solid #808080;">ESTADO:</td><td class="v-calculado-total" style="font-weight: bold; font-size: 16px; color: #d32f2f; text-align: center; border: 1px solid #808080;">0</td><td class="p-diff" colspan="3" style="font-weight: bold; text-align: center; border: 1px solid #808080;">VACÍO</td></tr>
                </tbody>
            </table>
        </div>'''
    return polys

full_html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: 'Segoe UI', sans-serif; background: #f5f7f9; padding: 20px; }}
        .header-poly {{ background: linear-gradient(180deg, #888888 0%, #696969 100%) !important; color: white; padding: 8px; }}
        .header-flota {{ background: linear-gradient(180deg, #333333 0%, #000000 100%) !important; color: white; padding: 8px; text-align: center; }}
        .main-header-flota {{ background: #000; color: white; padding: 12px; border-radius: 10px; font-weight: bold; margin-bottom: 15px; }}
        .tab-btn {{ padding: 10px 20px; cursor: pointer; border: none; background: #e0e0e0; border-radius: 8px 8px 0 0; font-weight: bold; }}
        .tab-btn.active {{ background: #000 !important; color: white !important; }}
        
        #google-alert {{ 
            position: fixed; top: -200px; left: 50%; transform: translateX(-50%);
            background: #d32f2f; color: white; padding: 25px 50px; border-radius: 15px;
            box-shadow: 0 15px 40px rgba(0,0,0,0.6); transition: 0.4s;
            z-index: 99999; text-align: center; border: 3px solid #fff; min-width: 450px;
        }}
        #google-alert.show {{ top: 40px; }}
        
        #calc_container {{ background: linear-gradient(145deg, #22c5bc, #1da29b); border-radius: 25px; padding: 20px; outline:none; }}
        #calc_container:focus {{ outline: 5px solid #FF00FF; }}
        .btn-calc {{ border-radius: 8px; background: white; cursor: pointer; font-weight: bold; padding: 10px; border: 1px solid #ccc; }}
        
        .u-manual, .spr-real-val {{ margin: 0 8px; display: inline-block; min-width: 25px; font-weight: bold; }}
    </style>
</head>
<body>

<div id="google-alert">
    <div style="font-size: 24px; font-weight: bold; margin-bottom: 10px;">⚠️ ALERTA CRÍTICA</div>
    <div id="alert-msg" style="font-size: 18px;">Mensaje</div>
    <div style="margin-top: 15px; font-size: 14px; background: rgba(0,0,0,0.2); padding: 5px; border-radius: 5px;">Presiona [ENTER] para continuar</div>
</div>

<div style="display: flex; gap: 20px;">
    <div style="flex: 1;">
        <div style="background: #696969; color: white; padding: 10px; border-radius: 8px; text-align: center; font-weight: bold; margin-bottom: 10px;">📋 PLANES GENERADOS</div>
        <div id="polys-2" class="p-content">{gen_poligonos()}</div>
        <div id="polys-3" class="p-content" style="display:none;">{gen_poligonos()}</div>
        <div id="polys-1" class="p-content" style="display:none;">{gen_poligonos()}</div>
        <div id="polys-4" class="p-content" style="display:none;">{gen_poligonos()}</div>
    </div>

    <div style="width: 480px; position: sticky; top: 10px;">
        <div class="main-header-flota">🚚 DISPONIBILIDAD DE FLOTA</div>
        <div style="display: flex; justify-content: space-between;">
            <div>
                <button class="tab-btn active" onclick="showTab(2, this)">C1</button>
                <button class="tab-btn" onclick="showTab(3, this)">C2</button>
                <button class="tab-btn" onclick="showTab(1, this)">SD</button>
                <button class="tab-btn" onclick="showTab(4, this)">SDE</button>
            </div>
            <div>
                <button onclick="filterFlota(true)" style="background:#C0C0C0; border:none; padding: 5px 10px; border-radius: 5px; cursor:pointer;">ACTIVAS</button>
                <button onclick="filterFlota(false)" style="background:#20B2AA; border:none; padding: 5px 10px; border-radius: 5px; cursor:pointer; color:white;">TODAS</button>
            </div>
        </div>

        <div style="background: white; padding: 15px; border-radius: 0 0 12px 12px; border: 1px solid #ccc;">
            <div id="tab-2" class="t-content"><table class="meli-table" style="width:100%; border-collapse:collapse;"><thead><tr><th class="header-flota" rowspan="2">UNIDADES (C1)</th><th class="header-flota" colspan="2">SPR</th><th class="header-flota" rowspan="2">ORH</th><th class="header-flota" rowspan="2">SCHED</th><th class="header-flota" rowspan="2">ME QUEDAN</th></tr><tr><th class="header-flota">min</th><th class="header-flota">max</th></tr></thead><tbody id="body-2">{gen_master_rows(u_C1, 2)}</tbody></table></div>
            <div id="tab-3" class="t-content" style="display:none;"><table class="meli-table" style="width:100%; border-collapse:collapse;"><thead><tr><th class="header-flota" rowspan="2">UNIDADES (C2)</th><th class="header-flota" colspan="2">SPR</th><th class="header-flota" rowspan="2">ORH</th><th class="header-flota" rowspan="2">SCHED</th><th class="header-flota" rowspan="2">ME QUEDAN</th></tr><tr><th class="header-flota">min</th><th class="header-flota">max</th></tr></thead><tbody id="body-3">{gen_master_rows(u_C2, 3)}</tbody></table></div>
            <div id="tab-1" class="t-content" style="display:none;"><table class="meli-table" style="width:100%; border-collapse:collapse;"><thead><tr><th class="header-flota" rowspan="2">UNIDADES (SD)</th><th class="header-flota" colspan="2">SPR</th><th class="header-flota" rowspan="2">ORH</th><th class="header-flota" rowspan="2">SCHED</th><th class="header-flota" rowspan="2">ME QUEDAN</th></tr><tr><th class="header-flota">min</th><th class="header-flota">max</th></tr></thead><tbody id="body-1">{gen_master_rows(u_SD, 1)}</tbody></table></div>
            <div id="tab-4" class="t-content" style="display:none;"><table class="meli-table" style="width:100%; border-collapse:collapse;"><thead><tr><th class="header-flota" rowspan="2">UNIDADES (SDE)</th><th class="header-flota" colspan="2">SPR</th><th class="header-flota" rowspan="2">ORH</th><th class="header-flota" rowspan="2">SCHED</th><th class="header-flota" rowspan="2">ME QUEDAN</th></tr><tr><th class="header-flota">min</th><th class="header-flota">max</th></tr></thead><tbody id="body-4">{gen_master_rows(u_SDE, 4)}</tbody></table></div>
        </div>

        <!-- Componentes -->
        <div style="background: #e2dcf5; border-radius: 15px; padding: 15px; margin: 15px 0; text-align: center;">
            <div style="font-size: 11px; font-weight: bold; color: #4e3396;">🕑 CONVERTIDOR DE TIEMPO</div>
            <input type="number" id="minInp" oninput="convertirMin()" style="width: 80px; height: 30px; text-align: center;">
            <span id="resConv" style="margin-left: 15px; font-size: 20px; font-weight: bold; color: #ac40de;">0h 0m</span>
        </div>

        <div id="calc_container" tabindex="0">
            <div style="background: #fffacd; padding: 10px; border-radius: 10px; text-align: right; margin-bottom: 15px; border: 1px solid #ccc;">
                <div id="h_calc" style="font-size: 12px; color: #666; height: 15px;">0</div>
                <div id="r_calc" style="font-size: 26px; font-weight: bold;">0</div>
            </div>
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px;">
                <button onclick="cl()" class="btn-calc" style="grid-column: span 2; background: #ffaaaa;">AC</button>
                <button onclick="del()" class="btn-calc">⌫</button><button onclick="ao('/')" class="btn-calc">÷</button>
                <button onclick="an('7')" class="btn-calc">7</button><button onclick="an('8')" class="btn-calc">8</button><button onclick="an('9')" class="btn-calc">9</button><button onclick="ao('*')" class="btn-calc">×</button>
                <button onclick="an('4')" class="btn-calc">4</button><button onclick="an('5')" class="btn-calc">5</button><button onclick="an('6')" class="btn-calc">6</button><button onclick="ao('-')" class="btn-calc">-</button>
                <button onclick="an('1')" class="btn-calc">1</button><button onclick="an('2')" class="btn-calc">2</button><button onclick="an('3')" class="btn-calc">3</button><button onclick="ao('+')" class="btn-calc">+</button>
                <button onclick="an('0')" class="btn-calc" style="grid-column: span 2;">0</button><button onclick="calc_eq()" class="btn-calc" style="background: #FF00FF; color: white;">=</button>
            </div>
        </div>

        <div style="background: #1a1a1a; padding: 15px; border-radius: 12px; color: white; margin-top: 15px;">
            <div style="display: flex; justify-content: space-between; font-size: 12px;"><span>HORA ACTUAL</span><span id="reloj-f" style="color: #00d4ff;">00:00:00</span></div>
            <div style="text-align: center;">
                <div id="display-f" style="font-size: 32px; font-weight: bold; font-family: monospace;">00:00:00.0</div>
                <div style="display: flex; gap: 10px; justify-content: center; margin-top: 10px;">
                    <button onclick="t_start()" style="background:#28a745; color:white; border:none; padding:8px 15px; border-radius:5px; cursor:pointer;">▶</button>
                    <button onclick="t_stop()" style="background:#ffc107; border:none; padding:8px 15px; border-radius:5px; cursor:pointer;">⏸</button>
                    <button onclick="t_reset()" style="background:#dc3545; color:white; border:none; padding:8px 15px; border-radius:5px; cursor:pointer;">🔄</button>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
    let curTab = 2;
    let edited = new Set();
    let alertShownSD = false;
    let curC = "";

    function showAlert(msg) {{
        document.getElementById('alert-msg').innerText = msg;
        document.getElementById('google-alert').classList.add('show');
    }}

    function hideAlert() {{
        document.getElementById('google-alert').classList.remove('show');
    }}

    function showTab(n, btn) {{
        curTab = n;
        document.querySelectorAll('.p-content, .t-content').forEach(el => el.style.display = 'none');
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.getElementById('polys-'+n).style.display = 'block';
        document.getElementById('tab-'+n).style.display = 'block';
        btn.classList.add('active');
        recalc();
    }}

    function filterFlota(hide) {{
        document.querySelectorAll('#body-' + curTab + ' tr').forEach(row => {{
            let s = parseInt(row.querySelector('.f-stock').innerText) || 0;
            row.style.display = (hide && s === 0) ? 'none' : '';
        }});
    }}

    function stepVal(btn, d, type) {{
        let row = btn.closest('tr');
        let sel = row.querySelector('.s-type');
        if(sel.value === "SELECCIONAR...") return;

        let fData = null;
        document.querySelectorAll('#body-' + curTab + ' tr').forEach(r => {{
            if(r.querySelector('.edit-name').innerText.trim() === sel.value) {{
                fData = {{ left: parseInt(r.querySelector('.f-left').innerText)||0, max: parseFloat(r.querySelector('.edit-spr-max').innerText)||0 }};
            }}
        }});

        if(type === 'u') {{
            let span = row.querySelector('.u-manual');
            let v = parseInt(span.innerText) || 0;
            if(d > 0 && fData && fData.left <= 0) {{
                if(curTab === 1 && !alertShownSD) {{ showAlert("⚠️ UNIDADES AGOTADAS EN SD. Solicitar autorización."); alertShownSD = true; }}
                else if(curTab !== 1 && curTab !== 4) {{ showAlert("⚠️ AGOTADO. Bloqueo de asignación."); return; }}
                else if(curTab === 4) showAlert("⚠️ EXCESO EN SDE. Bajo supervisión.");
            }}
            span.innerText = Math.max(0, v + d);
        }} else {{
            let span = row.querySelector('.spr-real-val');
            let v = parseFloat(span.innerText) || 0;
            if(d > 0 && fData && v >= fData.max) {{
                showAlert("⚠️ LÍMITE SPR ALCANZADO.");
                if(curTab !== 4) return;
            }}
            span.innerText = Math.max(0, v + d);
        }}
        edited.add(row);
        recalc();
    }}

    function recalc() {{
        let fleet = {{}};
        let hasOver = false;

        document.querySelectorAll('#body-' + curTab + ' tr').forEach(row => {{
            let n = row.querySelector('.edit-name').innerText.trim();
            let s = parseInt(row.querySelector('.f-stock').innerText) || 0;
            let spMin = row.querySelector('.edit-spr-min'), spMax = row.querySelector('.edit-spr-max'), fSt = row.querySelector('.f-stock');
            
            // Colores Dinámicos
            spMin.style.background = (parseFloat(spMin.innerText) > 0) ? "#def3ed" : "#ebebeb";
            spMax.style.background = (parseFloat(spMax.innerText) > 0) ? "#def3ed" : "#ebebeb";
            fSt.style.background = (s > 0) ? "#e3defa" : "#ebebeb";

            if(n !== "" && n !== "NUEVA UNIDAD") fleet[n] = {{ max: parseFloat(spMax.innerText)||0, stock: s, used: 0 }};
        }});

        document.querySelectorAll('#polys-' + curTab + ' .poligono-bloque').forEach(bl => {{
            let vT = parseFloat(bl.querySelector('.v-total-val').innerText) || 0, vA = 0;
            bl.querySelectorAll('.calc-row').forEach(row => {{
                let sel = row.querySelector('.s-type'), uS = row.querySelector('.u-manual'), sS = row.querySelector('.spr-real-val');
                if(sel.value !== "SELECCIONAR..." && fleet[sel.value]) {{
                    if(!edited.has(row)) sS.innerText = fleet[sel.value].max;
                    let u = parseInt(uS.innerText) || 0;
                    fleet[sel.value].used += u;
                    vA += (u * parseFloat(sS.innerText));
                }}
            }});
            let r = bl.querySelector('.v-calculado-total'), d = bl.querySelector('.p-diff');
            r.innerText = Math.round(vA);
            if(vT === 0) {{ d.innerText = "VACÍO"; d.style.background = "none"; }}
            else {{
                d.innerText = (vA >= vT) ? (vA === vT ? "OK" : "EXCESO: " + Math.round(vA-vT)) : "FALTAN: " + Math.round(vT-vA);
                d.style.background = (vA >= vT) ? (vA === vT ? "#ceedd6" : "#ffe4b5") : "#f7cdd1";
            }}
        }});

        document.querySelectorAll('#body-' + curTab + ' tr').forEach(row => {{
            let n = row.querySelector('.edit-name').innerText.trim();
            if(fleet[n]) {{
                let left = fleet[n].stock - fleet[n].used;
                let cL = row.querySelector('.f-left');
                cL.innerText = left;
                cL.style.background = (left <= 0) ? "#f7cdd1" : "#fff";
                if(left < 0) hasOver = true;
            }}
        }});
        
        let h = document.querySelector('#tab-' + curTab + ' .header-flota[rowspan="2"]:last-child');
        if(h) h.innerText = (hasOver && curTab === 4) ? "ME PASÉ POR" : "ME QUEDAN";

        document.querySelectorAll('#polys-' + curTab + ' .s-type').forEach(s => {{
            let val = s.value, opt = '<option>SELECCIONAR...</option>';
            Object.keys(fleet).sort().forEach(n => {{ if(fleet[n].stock > 0) opt += `<option value="${{n}}">${{n}}</option>`; }});
            s.innerHTML = opt; s.value = val;
        }});
    }}

    // Teclado Global
    document.addEventListener('keydown', (e) => {{
        if(e.key === 'Enter' && document.getElementById('google-alert').classList.contains('show')) {{
            hideAlert();
            e.preventDefault();
        }}
        if(document.activeElement.id === 'calc_container') {{
            if(e.key >= '0' && e.key <= '9') an(e.key);
            if(['+','-','*','/'].includes(e.key)) ao(e.key);
            if(e.key === 'Enter') calc_eq();
            if(e.key === 'Backspace') del();
            e.preventDefault();
        }}
    }});

    // Funciones básicas
    const rD = document.getElementById('r_calc'), hD = document.getElementById('h_calc');
    function an(n) {{ curC += n; rD.innerText = curC; }}
    function ao(o) {{ curC += " " + o + " "; rD.innerText = curC; }}
    function cl() {{ curC = ""; rD.innerText = "0"; hD.innerText = "0"; }}
    function del() {{ curC = curC.trim().slice(0, -1); rD.innerText = curC || "0"; }}
    function calc_eq() {{ try {{ let res = eval(curC); hD.innerText = curC + " ="; rD.innerText = res; curC = res.toString(); }} catch {{ rD.innerText = "Err"; }} }}
    function convertirMin() {{ let m = parseInt(document.getElementById('minInp').value) || 0; document.getElementById('resConv').innerText = Math.floor(m/60) + "h " + (m%60) + "m"; }}
    
    let sT, eT=0, run=false, tInt;
    setInterval(()=>{{ document.getElementById('reloj-f').innerText = new Date().toLocaleTimeString(); }}, 1000);
    function t_start() {{ if(!run) {{ run=true; sT=Date.now()-eT; tInt=setInterval(()=>{{ eT=Date.now()-sT; document.getElementById('display-f').innerText=fmt(eT); }},100); }} }}
    function t_stop() {{ run=false; clearInterval(tInt); }}
    function t_reset() {{ run=false; clearInterval(tInt); eT=0; document.getElementById('display-f').innerText="00:00:00.0"; }}
    function fmt(t) {{ let ms=Math.floor((t%1000)/100), s=Math.floor((t/1000)%60), m=Math.floor((t/60000)%60), h=Math.floor(t/3600000); return `${{h.toString().padStart(2,'0')}}:${{m.toString().padStart(2,'0')}}:${{s.toString().padStart(2,'0')}}.${{ms}}`; }}
    
    function manualEdit(el) {{ edited.add(el.closest('tr')); recalc(); }}
    function resetRow(sel) {{ let r = sel.closest('tr'); r.querySelector('.u-manual').innerText = "0"; r.querySelector('.spr-real-val').innerText = "0"; edited.delete(r); recalc(); }}
    
    recalc();
</script>
</body>
</html>
"""

html(full_html, height=2000, scrolling=True)
