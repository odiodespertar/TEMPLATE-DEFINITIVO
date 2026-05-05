import streamlit as st
from streamlit.components.v1 import html

st.set_page_config(page_title="Monitor Logístico VP04 - Total Pro", layout="wide")

# Ocultar elementos de Streamlit para que parezca una Web App independiente
st.markdown("""
    <style>
    .block-container {padding: 0rem !important;}
    footer, #MainMenu, header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 1. DATOS DE UNIDADES (CATÁLOGOS) ---
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
        style = "color: #555; background: #ebebeb;" if is_real else "color: #C0C0C0; background: #fcfcfc;"
        rows += f'''
        <tr data-table="{table_id}" class="master-row">
            <td contenteditable="true" class="edit-name" oninput="recalc()" style="{style} font-weight: bold; text-align: left; padding-left: 10px; border: 0.5px solid #ccc;">{name}</td>
            <td contenteditable="true" class="edit-spr-min" oninput="recalc()" style="{style} font-weight: bold; text-align: center; border: 0.5px solid #ccc;">{spr[0]}</td>
            <td contenteditable="true" class="edit-spr-max" oninput="recalc()" style="{style} font-weight: bold; text-align: center; border: 0.5px solid #ccc;">{spr[1]}</td>
            <td contenteditable="true" class="edit-orh" style="{style} text-align: center; border: 0.5px solid #ccc;">480</td>
            <td contenteditable="true" class="f-stock" oninput="recalc()" style="{style} font-weight: bold; text-align: center; border: 0.5px solid #ccc;">0</td>
            <td class="f-left" style="{style} font-weight: bold; text-align: center; border: 0.5px solid #ccc;">0</td>
        </tr>'''
    return rows

def gen_poligonos():
    polys = ""
    btn_s = "cursor:pointer; border:none; background:rgba(0,0,0,0.08); color:#333; font-weight:bold; width:20px; height:20px; border-radius:4px; margin:0 2px;"
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
        <td style="border: 0.5px solid #ccc;"><select class="s-type" onchange="resetRow(this)" style="width:100%; border:none; background:transparent; font-weight:bold;"></select></td>
        <td style="text-align: center; border: 0.5px solid #ccc;"><input type="checkbox" class="ok-check"></td>
    </tr>'''
    for i in range(1, 11):
        polys += f'''
        <div class="poligono-bloque" style="margin-bottom: 15px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); border-radius: 10px; overflow: hidden; background: white;">
            <table class="meli-table tabla-planes" style="width: 100%; border-collapse: collapse;">
                <thead>
                    <tr><th class="header-poly">PLAN {i}</th><th class="header-poly">VOL. TOTAL</th><th class="header-poly" style="width:90px;"># ASIGNADAS</th><th class="header-poly" style="width:90px;">SPR REAL</th><th class="header-poly">TIPO DE UNIDAD</th><th class="header-poly" style="width:45px;">OK</th></tr>
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
                        <td style="border: 0.5px solid #ccc;"><select class="s-type" onchange="resetRow(this)" style="width:100%; border:none; background:transparent; font-weight:bold;"></select></td>
                        <td style="text-align: center; border: 0.5px solid #ccc;"><input type="checkbox" class="ok-check"></td>
                    </tr>
                    {fila_inner * 4}
                    <tr><td colspan="2" style="text-align:center; font-weight:bold; background:#f8f9fa; border: 1px solid #808080;">ESTADO:</td><td class="v-calculado-total" style="font-weight: bold; font-size: 16px; color: #d32f2f; text-align: center; border: 1px solid #808080;">0</td><td class="p-diff" colspan="3" style="font-weight: bold; text-align: center; border: 1px solid #808080;">VACÍO</td></tr>
                </tbody>
            </table>
        </div>'''
    return polys

# --- 2. INTEGRACIÓN DE DISEÑO 3D Y HTML ---
full_html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        /* Pegar aquí tus estilos de la Parte 2 */
        body {{ font-family: 'Segoe UI', sans-serif; background: #f5f7f9; padding: 20px; }}
        .header-poly {{ background: linear-gradient(180deg, #888888 0%, #696969 100%) !important; color: white; padding: 8px; text-shadow: 1px 1px 2px rgba(0,0,0,0.5); }}
        .header-flota {{ background: linear-gradient(180deg, #333333 0%, #000000 100%) !important; color: white; padding: 8px; text-align: center; }}
        .main-header-flota {{ background: linear-gradient(90deg, #000000, #444444); color: white; padding: 12px; border-radius: 10px; font-weight: bold; margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.2); }}
        .tab-btn {{ padding: 10px 20px; cursor: pointer; border: none; background: #e0e0e0; border-radius: 8px 8px 0 0; font-weight: bold; transition: 0.3s; }}
        .tab-btn.active {{ background: #000000 !important; color: white !important; box-shadow: inset 2px 2px 6px rgba(0,0,0,0.5); position: relative; top: 2px; }}
        
        #calc_container {{
            background: linear-gradient(145deg, #22c5bc, #1da29b) !important;
            border-radius: 25px; padding: 20px;
            box-shadow: 8px 8px 16px #acacac, -8px -8px 16px #ffffff !important;
            transform: perspective(1000px) rotateX(2deg); outline: none;
        }}
        #calc_container:focus {{ outline: 4px solid #FF00FF !important; box-shadow: 0 0 25px rgba(255, 0, 255, 0.7) !important; }}
        .btn-calc {{ border-radius: 8px; background: linear-gradient(180deg, #ffffff 0%, #f0f4f8 100%); box-shadow: 2px 2px 5px rgba(0,0,0,0.2); cursor: pointer; font-weight: bold; padding: 10px; border: 1px solid #ccc; }}
        .btn-calc:active {{ transform: translateY(2px); box-shadow: inset 2px 2px 5px rgba(0,0,0,0.3) !important; }}

        #block-alert {{ position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(255,0,0,0.9); z-index: 10000; display: none; flex-direction: column; justify-content: center; align-items: center; color: white; text-align: center; }}
        
        .u-manual, .spr-real-val {{ margin: 0 8px; display: inline-block; min-width: 25px; font-weight: bold; }}
    </style>
</head>
<body>

<div id="block-alert">
    <h1 style="font-size: 60px;">⚠️ UNIDADES AGOTADAS</h1>
    <p style="font-size: 24px;">Favor de contactar al service para solicitar más.</p>
    <p style="margin-top: 30px;">[Presiona ENTER para cerrar]</p>
</div>

<div style="display: flex; gap: 20px;">
    <!-- Panel Izquierdo: Planes -->
    <div style="flex: 1;">
        <div style="background: #696969; color: white; padding: 10px; border-radius: 8px; text-align: center; font-weight: bold; margin-bottom: 10px;">📋 PLANES GENERADOS</div>
        <div id="polys-2" class="p-content">{gen_poligonos()}</div>
        <div id="polys-3" class="p-content" style="display:none;">{gen_poligonos()}</div>
        <div id="polys-1" class="p-content" style="display:none;">{gen_poligonos()}</div>
        <div id="polys-4" class="p-content" style="display:none;">{gen_poligonos()}</div>
    </div>

    <!-- Panel Derecho: Flota y Herramientas -->
    <div style="width: 480px; position: sticky; top: 10px;">
        <div class="main-header-flota">🚚 DISPONIBILIDAD DE FLOTA</div>
        
        <div style="display: flex; justify-content: space-between; align-items: flex-end;">
            <div>
                <button class="tab-btn active" onclick="showTab(2, this)">C1</button>
                <button class="tab-btn" onclick="showTab(3, this)">C2</button>
                <button class="tab-btn" onclick="showTab(1, this)">SD</button>
                <button class="tab-btn" onclick="showTab(4, this)">SDE</button>
            </div>
            <div style="margin-bottom: 5px;">
                <button onclick="filterFlota(true)" style="background:#C0C0C0; border:none; padding: 5px 10px; border-radius: 5px; cursor:pointer; font-weight:bold;">ACTIVAS</button>
                <button onclick="filterFlota(false)" style="background:#20B2AA; border:none; padding: 5px 10px; border-radius: 5px; cursor:pointer; color:white; font-weight:bold;">TODAS</button>
            </div>
        </div>

        <div style="background: white; padding: 15px; border-radius: 0 0 12px 12px; box-shadow: 0 6px 12px rgba(0,0,0,0.15);">
            <div id="tab-2" class="t-content">
                <table class="meli-table" style="width:100%">
                    <thead>
                        <tr><th class="header-flota" rowspan="2">UNIDADES (C1)</th><th class="header-flota" colspan="2">SPR</th><th class="header-flota" rowspan="2">ORH</th><th class="header-flota" rowspan="2">SCHED</th><th class="header-flota" rowspan="2">ME QUEDAN</th></tr>
                        <tr><th class="header-flota">min</th><th class="header-flota">max</th></tr>
                    </thead>
                    <tbody id="body-2">{gen_master_rows(u_C1, 2)}</tbody>
                </table>
            </div>
            <!-- Otros cuerpos de tabla -->
            <div id="tab-3" class="t-content" style="display:none;"><table class="meli-table" style="width:100%"><thead><tr><th class="header-flota" rowspan="2">UNIDADES (C2)</th><th class="header-flota" colspan="2">SPR</th><th class="header-flota" rowspan="2">ORH</th><th class="header-flota" rowspan="2">SCHED</th><th class="header-flota" rowspan="2">ME QUEDAN</th></tr><tr><th class="header-flota">min</th><th class="header-flota">max</th></tr></thead><tbody id="body-3">{gen_master_rows(u_C2, 3)}</tbody></table></div>
            <div id="tab-1" class="t-content" style="display:none;"><table class="meli-table" style="width:100%"><thead><tr><th class="header-flota" rowspan="2">UNIDADES (SD)</th><th class="header-flota" colspan="2">SPR</th><th class="header-flota" rowspan="2">ORH</th><th class="header-flota" rowspan="2">SCHED</th><th class="header-flota" rowspan="2">ME QUEDAN</th></tr><tr><th class="header-flota">min</th><th class="header-flota">max</th></tr></thead><tbody id="body-1">{gen_master_rows(u_SD, 1)}</tbody></table></div>
            <div id="tab-4" class="t-content" style="display:none;"><table class="meli-table" style="width:100%"><thead><tr><th class="header-flota" rowspan="2">UNIDADES (SDE)</th><th class="header-flota" colspan="2">SPR</th><th class="header-flota" rowspan="2">ORH</th><th class="header-flota" rowspan="2">SCHED</th><th class="header-flota" rowspan="2">ME QUEDAN</th></tr><tr><th class="header-flota">min</th><th class="header-flota">max</th></tr></thead><tbody id="body-4">{gen_master_rows(u_SDE, 4)}</tbody></table></div>
        </div>

        <!-- Convertidor -->
        <div style="background: linear-gradient(145deg, #e2dcf5, #d1c9f0); border-radius: 15px; padding: 15px; margin: 15px 0; text-align: center; border: 2px solid #d1d1d1;">
            <div style="font-size: 11px; font-weight: bold; color: #4e3396; margin-bottom: 5px;">🕑 CONVERTIDOR DE TIEMPO</div>
            <input type="number" id="minInp" oninput="convertirMin()" placeholder="Min" style="width: 80px; height: 30px; text-align: center; border-radius: 5px; border: 1px solid #b8afde;">
            <span id="resConv" style="margin-left: 15px; font-size: 20px; font-weight: bold; color: #ac40de;">0h 0m</span>
        </div>

        <!-- Calculadora -->
        <div id="calc_container" tabindex="0">
            <div style="background: #fffacd; padding: 10px; border-radius: 10px; text-align: right; margin-bottom: 15px; box-shadow: inset 2px 2px 5px rgba(0,0,0,0.1);">
                <div id="h_calc" style="font-size: 12px; color: #666; height: 15px;">0</div>
                <div id="r_calc" style="font-size: 26px; font-weight: bold; color: black;">0</div>
            </div>
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px;">
                <button onclick="cl()" class="btn-calc" style="grid-column: span 2; background: #ffaaaa;">AC</button>
                <button onclick="del()" class="btn-calc">⌫</button>
                <button onclick="ao('/')" class="btn-calc">÷</button>
                <button onclick="an('7')" class="btn-calc">7</button><button onclick="an('8')" class="btn-calc">8</button><button onclick="an('9')" class="btn-calc">9</button>
                <button onclick="ao('*')" class="btn-calc">×</button>
                <button onclick="an('4')" class="btn-calc">4</button><button onclick="an('5')" class="btn-calc">5</button><button onclick="an('6')" class="btn-calc">6</button>
                <button onclick="ao('-')" class="btn-calc">-</button>
                <button onclick="an('1')" class="btn-calc">1</button><button onclick="an('2')" class="btn-calc">2</button><button onclick="an('3')" class="btn-calc">3</button>
                <button onclick="ao('+')" class="btn-calc">+</button>
                <button onclick="an('0')" class="btn-calc" style="grid-column: span 2;">0</button>
                <button onclick="calc_eq()" class="btn-calc" style="background: #FF00FF; color: white;">=</button>
            </div>
        </div>

        <!-- Cronómetro -->
        <div style="background: #1a1a1a; padding: 15px; border-radius: 12px; color: white; margin-top: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.4);">
            <div style="display: flex; justify-content: space-between; font-size: 12px; color: #888; margin-bottom: 5px;">
                <span>HORA ACTUAL</span><span id="reloj-f" style="color: #00d4ff;">00:00:00</span>
            </div>
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
    let curC = "";

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

    function resetRow(sel) {{
        let row = sel.closest('tr');
        row.querySelector('.u-manual').innerText = "0";
        row.querySelector('.spr-real-val').innerText = "0";
        edited.delete(row);
        recalc();
    }}

    function manualEdit(el) {{ edited.add(el.closest('tr')); recalc(); }}

    function stepVal(btn, d, type) {{
        let row = btn.closest('tr');
        let sel = row.querySelector('.s-type');
        if(sel.value === "SELECCIONAR...") return;

        let span = (type === 'u') ? row.querySelector('.u-manual') : row.querySelector('.spr-real-val');
        let val = parseInt(span.innerText) || 0;

        // Bloqueo de unidades
        if(type === 'u' && d > 0 && curTab !== 4) {{
            let fleetRows = document.querySelectorAll('#body-' + curTab + ' tr');
            for(let r of fleetRows) {{
                if(r.querySelector('.edit-name').innerText.trim() === sel.value) {{
                    let left = parseInt(r.querySelector('.f-left').innerText);
                    if(left <= 0) {{
                        document.getElementById('block-alert').style.display = 'flex';
                        return;
                    }}
                }}
            }}
        }}
        
        span.innerText = Math.max(0, val + d);
        edited.add(row);
        recalc();
    }}

    function recalc() {{
        let fleet = {{}};
        let hasOver = false;

        // 1. Leer Flota Maestra
        document.querySelectorAll('#body-' + curTab + ' tr').forEach(row => {{
            let nameCell = row.querySelector('.edit-name');
            let name = nameCell.innerText.trim();
            let schedCell = row.querySelector('.f-stock');
            let sched = parseInt(schedCell.innerText) || 0;
            let minC = row.querySelector('.edit-spr-min'), maxC = row.querySelector('.edit-spr-max');

            if(name !== "" && name !== "NUEVA UNIDAD") {{
                if(sched > 0) {{
                    nameCell.style.background = "#ffffff"; schedCell.style.background = "#e3defa";
                    minC.style.background = "#def3ed"; maxC.style.background = "#def3ed";
                }} else {{
                    nameCell.style.background = "#ebebeb"; schedCell.style.background = "#ebebeb";
                    minC.style.background = "#ebebeb"; maxC.style.background = "#ebebeb";
                }}
                fleet[name] = {{ min: parseFloat(minC.innerText)||0, max: parseFloat(maxC.innerText)||0, stock: sched, used: 0 }};
            }}
        }});

        // 2. Procesar Planes
        document.querySelectorAll('#polys-' + curTab + ' .poligono-bloque').forEach(bl => {{
            let vT = parseFloat(bl.querySelector('.v-total-val').innerText) || 0;
            let vA = 0;
            bl.querySelectorAll('.calc-row').forEach(row => {{
                let sel = row.querySelector('.s-type');
                let spanU = row.querySelector('.u-manual'), spanS = row.querySelector('.spr-real-val');
                
                if(sel.value !== "SELECCIONAR..." && fleet[sel.value]) {{
                    let f = fleet[sel.value];
                    if(!edited.has(row)) {{ spanS.innerText = f.max; }}
                    let u = parseInt(spanU.innerText) || 0;
                    let s = parseFloat(spanS.innerText) || 0;
                    f.used += u;
                    vA += (u * s);
                }}
            }});
            let res = bl.querySelector('.v-calculado-total'), diff = bl.querySelector('.p-diff');
            res.innerText = Math.round(vA);
            if(vT === 0) {{ diff.innerText = "VACÍO"; diff.style.background = "none"; }}
            else if(vA >= vT) {{ 
                diff.innerText = (vA === vT) ? "ZONA CUBIERTA OK" : "EXCESO: " + Math.round(vA-vT);
                diff.style.background = (vA === vT) ? "#ceedd6" : "#ffe4b5";
            }} else {{
                diff.innerText = "FALTAN: " + Math.round(vT - vA); diff.style.background = "#f7cdd1";
            }}
        }});

        // 3. Actualizar "Me quedan" y Título
        document.querySelectorAll('#body-' + curTab + ' tr').forEach(row => {{
            let name = row.querySelector('.edit-name').innerText.trim();
            if(fleet[name]) {{
                let left = fleet[name].stock - fleet[name].used;
                let cell = row.querySelector('.f-left');
                cell.innerText = left;
                if(left < 0) {{ cell.style.color = "#FF4500"; hasOver = true; }}
                else {{ cell.style.color = "#228B22"; }}
            }}
        }});

        let head = document.querySelector('#tab-' + curTab + ' .header-flota[rowspan="2"]:last-child');
        if(head) head.innerText = hasOver ? "ME PASÉ POR" : "ME QUEDAN";

        // 4. Update Selects
        document.querySelectorAll('#polys-' + curTab + ' .s-type').forEach(s => {{
            let val = s.value;
            let h = '<option>SELECCIONAR...</option>';
            Object.keys(fleet).sort().forEach(n => h += `<option value="${{n}}">${{n}}</option>`);
            s.innerHTML = h; s.value = val;
        }});
    }}

    // Calculadora Logica
    const rD = document.getElementById('r_calc'), hD = document.getElementById('h_calc');
    function an(n) {{ curC += n; rD.innerText = curC; }}
    function ao(o) {{ curC += " " + o + " "; rD.innerText = curC; }}
    function cl() {{ curC = ""; rD.innerText = "0"; hD.innerText = "0"; }}
    function del() {{ curC = curC.trim().slice(0, -1); rD.innerText = curC || "0"; }}
    function calc_eq() {{ try {{ let res = eval(curC); hD.innerText = curC + " ="; rD.innerText = res; curC = res.toString(); }} catch {{ rD.innerText = "Err"; }} }}

    // Convertidor
    function convertirMin() {{
        let m = parseInt(document.getElementById('minInp').value) || 0;
        document.getElementById('resConv').innerText = Math.floor(m/60) + "h " + (m%60) + "m";
    }}

    // Crono
    let sT, eT=0, run=false, tInt;
    function updateReloj() {{ document.getElementById('reloj-f').innerText = new Date().toLocaleTimeString(); }}
    setInterval(updateReloj, 1000);
    function t_start() {{ if(!run) {{ run=true; sT=Date.now()-eT; tInt=setInterval(()=>{{ eT=Date.now()-sT; document.getElementById('display-f').innerText=fmt(eT); }},100); }} }}
    function t_stop() {{ run=false; clearInterval(tInt); }}
    function t_reset() {{ run=false; clearInterval(tInt); eT=0; document.getElementById('display-f').innerText="00:00:00.0"; }}
    function fmt(t) {{ let ms=Math.floor((t%1000)/100), s=Math.floor((t/1000)%60), m=Math.floor((t/60000)%60), h=Math.floor(t/3600000); return `${{h.toString().padStart(2,'0')}}:${{m.toString().padStart(2,'0')}}:${{s.toString().padStart(2,'0')}}.${{ms}}`; }}

    // Teclado
    document.addEventListener('keydown', (e) => {{
        if(e.key === 'Enter' && document.getElementById('block-alert').style.display === 'flex') {{
            document.getElementById('block-alert').style.display = 'none';
        }}
        if(document.activeElement.id === 'calc_container') {{
            if(e.key >= '0' && e.key <= '9') an(e.key);
            if(e.key === '+') ao('+');
            if(e.key === '-') ao('-');
            if(e.key === '*' || e.key === 'x') ao('*');
            if(e.key === '/') ao('/');
            if(e.key === 'Enter') calc_eq();
            if(e.key === 'Backspace') del();
            if(e.key === 'Escape') cl();
            e.preventDefault();
        }}
    }});

    recalc();
</script>
</body>
</html>
"""

html(full_html, height=2000, scrolling=True)
