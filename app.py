import streamlit as st
import streamlit.components.v1 as components

# Configuración de página para usar todo el ancho
st.set_page_config(layout="wide", page_title="Tracker Logística VP04")

# Estructura de datos inicial (Copiada exactamente de tu lógica)
unidades_data = {
    "SDE": {"CROWD 5 HRS": [25, 28], "CROWD 5 HRS EXTENDIDA": [25, 28], "CROWD 3 HRS": [25, 28], "MOTO 3 HRS": [25, 28]},
    "SD": {"MOTO 3 HRS": [25, 25], "MOTO NEWBIE": [20, 22], "CROWD 5 HRS / SMALL VAN": [35, 37]},
    "C1": {
        "RENTAL ELEC LARGE VAN": [120, 120], "RENTAL ELEC SMALL VAN": [120, 120],
        "RENTAL LARGE VAN": [120, 120], "RENTAL SMALL VAN": [120, 120],
        "LARGE VAN VAR(MLP)": [100, 100], "SMALL VAN VAR(MLP)":[80, 80],
        "CAR MLP": [50, 50], "MOTO 3 HRS": [28, 28], "CROWD NEWBIE 3 hrs": [30, 30],
        "CROWD EXTRA 8 HRS": [80, 85], "CROWD 5 HRS": [60, 60]
    },
    "C2": {
        "RENTAL ELEC LARGE VAN": [120, 120], "RENTAL ELEC SMALL VAN": [120, 120],
        "RENTAL LARGE VAN": [120, 120], "RENTAL SMALL VAN": [120, 120],
        "LARGE VAN HÍBRIDA": [100, 100], "LARGE VAN VAR(MLP)": [100, 100],
        "SMALL VAN VAR(MLP)":[80, 80], "CAR MLP": [50, 50], "MOTO 3 HRS": [28, 28],
        "CROWD NEWBIE 3 hrs": [30, 30], "CROWD EXTRA 8 HRS": [80, 85], "CROWD 5 HRS": [60, 60]
    }
}

# Helper para generar filas de flota
def get_fleet_rows(data, table_id):
    rows = ""
    items = list(data.items())
    for i in range(15):
        name, spr = (items[i][0], items[i][1]) if i < len(items) else ("NUEVA UNIDAD", [0, 0])
        style = "color: #969696; background: #ebebeb;" # Estado inicial desactivado (Imagen 1)
        rows += f'''
        <tr data-table="{table_id}" class="master-row">
            <td contenteditable="true" class="edit-name" oninput="recalc()" style="{style} font-weight: bold; text-align: left; padding-left: 10px;">{name}</td>
            <td contenteditable="true" class="edit-spr-min" oninput="recalc()" style="{style} font-weight: bold; text-align: center;">{spr[0]}</td>
            <td contenteditable="true" class="edit-spr-max" oninput="recalc()" style="{style} font-weight: bold; text-align: center;">{spr[1]}</td>
            <td contenteditable="true" class="edit-orh" style="{style} font-weight: normal; text-align: center;">480</td>
            <td contenteditable="true" class="f-stock" style="{style} font-weight: bold; text-align: center; border: 2px solid #4A90E2 !important;" oninput="recalc()">0</td>
            <td class="f-left" style="{style} font-weight: bold; text-align: center;">0</td>
        </tr>'''
    return rows

# Helper para generar polígonos
def get_polygons(tab_id):
    polys = ""
    btn_s = "cursor:pointer; border:none; background:rgba(0,0,0,0.05); color:#696969; font-weight:bold; width:18px; height:18px; border-radius:3px; margin:0 2px;"
    for i in range(1, 11):
        fila_inner = f'''
        <tr class="calc-row">
            <td class="u-manual-cell" style="background: #e3defa; text-align: center;">
                <button style="{btn_s}" onclick="stepVal(this, -1, 'u')">-</button>
                <span contenteditable="true" class="u-manual" oninput="manualEdit(this)">0</span>
                <button style="{btn_s}" onclick="stepVal(this, 1, 'u')">+</button>
            </td>
            <td class="spr-real-cell" style="background: #def3ed; text-align: center;">
                <button style="{btn_s}" onclick="stepVal(this, -1, 's')">-</button>
                <span contenteditable="true" class="spr-real-val" oninput="manualEdit(this)">0</span>
                <button style="{btn_s}" onclick="stepVal(this, 1, 's')">+</button>
            </td>
            <td><select class="s-type" onchange="resetRow(this)"><option>SELECCIONAR...</option></select></td>
            <td style="text-align: center;"><input type="checkbox" class="ok-check"></td>
        </tr>'''
        
        polys += f'''
        <div class="poligono-bloque" style="margin-bottom: 15px;">
            <table class="meli-table tabla-planes">
                <thead>
                    <tr><th class="header-poly">PLAN {i}</th><th class="header-poly">VOL. TOTAL</th><th class="header-poly" style="width:90px;"># ASIGNADAS</th><th class="header-poly" style="width:70px;">SPR REAL</th><th class="header-poly">TIPO</th><th class="header-poly" style="width:35px;">OK</th></tr>
                </thead>
                <tbody>
                    <tr class="calc-row">
                        <td rowspan="5" contenteditable="true" class="v-total" style="width:100px; background:#D3D3D3; text-align:center;">PLAN {i}</td>
                        <td rowspan="5" contenteditable="true" class="v-total-val" oninput="recalc()" style="width:70px; color:#20B2AA; font-weight:bold; font-size:16px; text-align:center;">0</td>
                        <td class="u-manual-cell" style="background: #e3defa; text-align: center;">
                            <button style="{btn_s}" onclick="stepVal(this, -1, 'u')">-</button>
                            <span contenteditable="true" class="u-manual" oninput="manualEdit(this)">0</span>
                            <button style="{btn_s}" onclick="stepVal(this, 1, 'u')">+</button>
                        </td>
                        <td class="spr-real-cell" style="background: #def3ed; text-align: center;">
                            <button style="{btn_s}" onclick="stepVal(this, -1, 's')">-</button>
                            <span contenteditable="true" class="spr-real-val" oninput="manualEdit(this)">0</span>
                            <button style="{btn_s}" onclick="stepVal(this, 1, 's')">+</button>
                        </td>
                        <td><select class="s-type" onchange="resetRow(this)"><option>SELECCIONAR...</option></select></td>
                        <td style="text-align: center;"><input type="checkbox" class="ok-check"></td>
                    </tr>
                    {fila_inner * 4}
                    <tr><td colspan="2" style="text-align:center; font-weight:bold; background:#f8f9fa;">ESTADO:</td><td class="v-calculado-total" style="font-weight:bold; color:#d32f2f; text-align:center;">0</td><td class="p-diff" colspan="3" style="text-align:center; font-size:11px; font-weight:bold;">VACÍO</td></tr>
                </tbody>
            </table>
        </div>'''
    return polys

# Construcción del HTML Final para Streamlit
html_content = f"""
<style>
    {open("style.css").read() if False else ""} /* Espacio para CSS externo si fuera necesario */
    body {{ background-color: #f5f7f9; font-family: 'Segoe UI', sans-serif; }}
    .main-wrapper {{ display: flex; gap: 20px; padding: 10px; min-width: 1200px; }} /* Evita colapso en zoom */
    .left-panel {{ flex: 1; max-height: 95vh; overflow-y: auto; padding-right: 10px; }}
    .right-panel {{ width: 450px; position: sticky; top: 0; height: fit-content; }}
    
    .meli-table {{ width: 100%; border-collapse: separate; border-spacing: 0; border: 2px solid #ccc; border-radius: 10px; overflow: hidden; font-size: 11px; background: white; }}
    .header-flota {{ background: linear-gradient(180deg, #333, #000); color: white; padding: 8px; text-align: center; border: 0.5px solid #444; }}
    .header-poly {{ background: linear-gradient(180deg, #888, #696969); color: white; padding: 8px; text-align: center; }}
    .tabla-flota td, .tabla-planes td {{ border: 0.5px solid #ccc; padding: 5px; }}

    .tab-btn {{ padding: 8px 15px; cursor: pointer; border: none; background: #e0e0e0; border-radius: 8px 8px 0 0; font-weight: bold; margin-right: 2px; }}
    .tab-btn.active {{ background: #000; color: white; box-shadow: inset 2px 2px 5px rgba(0,0,0,0.5); }}
    
    .btn-calc {{ border: 1px solid #ccc; border-radius: 8px; background: linear-gradient(180deg, #fff, #f0f4f8); font-weight: bold; padding: 10px; cursor: pointer; }}
    .btn-calc:active {{ transform: translateY(2px); box-shadow: inset 2px 2px 5px rgba(0,0,0,0.3); }}
    
    .conv-container {{ background: linear-gradient(145deg, #e2dcf5, #d1c9f0); border-radius: 15px; padding: 10px; margin-top: 10px; text-align: center; border: 2px solid #d1d1d1; }}
    
    /* Estilos de la Calculadora Aqua */
    #calc_container {{
        background: linear-gradient(145deg, #22c5bc, #1da29b) !important;
        border-radius: 20px; padding: 15px; margin-top: 10px;
        box-shadow: 5px 5px 15px #aaa, inset 1px 1px 2px rgba(255,255,255,0.3);
    }}
</style>

<div class="main-wrapper">
    <div class="left-panel">
        <div style="background: #696969; color: white; padding: 10px; border-radius: 8px; font-weight: bold; text-align: center; margin-bottom: 10px;">📋 PLANES GENERADOS</div>
        <div id="polys-2" class="poly-tab-content">{get_polygons(2)}</div>
        <div id="polys-3" class="poly-tab-content" style="display:none;">{get_polygons(3)}</div>
        <div id="polys-1" class="poly-tab-content" style="display:none;">{get_polygons(1)}</div>
        <div id="polys-4" class="poly-tab-content" style="display:none;">{get_polygons(4)}</div>
    </div>

    <div class="right-panel">
        <div style="background: linear-gradient(90deg, #000, #444); color: white; padding: 10px; border-radius: 8px; font-weight: bold; margin-bottom: 10px;">🚚 DISPONIBILIDAD DE FLOTA</div>
        <div style="display: flex; justify-content: space-between; align-items: flex-end;">
            <div>
                <button class="tab-btn active" onclick="showTab(2, this)">C1</button>
                <button class="tab-btn" onclick="showTab(3, this)">C2</button>
                <button class="tab-btn" onclick="showTab(1, this)">SD</button>
                <button class="tab-btn" onclick="showTab(4, this)">SDE</button>
            </div>
            <div style="margin-bottom: 5px;">
                <button onclick="filterFlota(true)" style="background:#C0C0C0; font-weight:bold; cursor:pointer; border-radius:4px; padding:4px 8px;">ACTIVAS</button>
                <button onclick="filterFlota(false)" style="background:#20B2AA; color:white; font-weight:bold; cursor:pointer; border-radius:4px; padding:4px 8px;">TODAS</button>
            </div>
        </div>

        <div class="master-container" style="background: white; padding: 10px; border-radius: 0 0 12px 12px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
            <div id="tab-flota-2" class="tab-content">
                <table class="meli-table">
                    <thead>
                        <tr><th class="header-flota" rowspan="2">UNIDADES (C1)</th><th class="header-flota" colspan="2">SPR</th><th class="header-flota" rowspan="2">ORH</th><th class="header-flota" rowspan="2">SCHED</th><th class="header-flota" rowspan="2">ME QUEDAN</th></tr>
                        <tr><th class="header-flota">min</th><th class="header-flota">max</th></tr>
                    </thead>
                    <tbody id="body-2">{get_fleet_rows(unidades_data["C1"], 2)}</tbody>
                </table>
            </div>
            <div id="tab-flota-3" class="tab-content" style="display:none;">
                <table class="meli-table">
                    <thead>
                        <tr><th class="header-flota" rowspan="2">UNIDADES (C2)</th><th class="header-flota" colspan="2">SPR</th><th class="header-flota" rowspan="2">ORH</th><th class="header-flota" rowspan="2">SCHED</th><th class="header-flota" rowspan="2">ME QUEDAN</th></tr>
                        <tr><th class="header-flota">min</th><th class="header-flota">max</th></tr>
                    </thead>
                    <tbody id="body-3">{get_fleet_rows(unidades_data["C2"], 3)}</tbody>
                </table>
            </div>
            <div id="tab-flota-1" class="tab-content" style="display:none;">
                <table class="meli-table">
                    <thead>
                        <tr><th class="header-flota" rowspan="2">UNIDADES (SD)</th><th class="header-flota" colspan="2">SPR</th><th class="header-flota" rowspan="2">ORH</th><th class="header-flota" rowspan="2">SCHED</th><th class="header-flota" rowspan="2">ME QUEDAN</th></tr>
                        <tr><th class="header-flota">min</th><th class="header-flota">max</th></tr>
                    </thead>
                    <tbody id="body-1">{get_fleet_rows(unidades_data["SD"], 1)}</tbody>
                </table>
            </div>
            <div id="tab-flota-4" class="tab-content" style="display:none;">
                <table class="meli-table">
                    <thead>
                        <tr><th class="header-flota" rowspan="2">UNIDADES (SDE)</th><th class="header-flota" colspan="2">SPR</th><th class="header-flota" rowspan="2">ORH</th><th class="header-flota" rowspan="2">SCHED</th><th class="header-flota" rowspan="2">ME QUEDAN</th></tr>
                        <tr><th class="header-flota">min</th><th class="header-flota">max</th></tr>
                    </thead>
                    <tbody id="body-4">{get_fleet_rows(unidades_data["SDE"], 4)}</tbody>
                </table>
            </div>
        </div>

        <div class="conv-container">
            <div style="font-size: 10px; font-weight: bold; color: #4e3396;">🕑 CONVERTIDOR</div>
            <input type="number" id="minInp" oninput="convertirMinutos()" placeholder="Min" style="width: 70px; text-align: center; border-radius: 5px; border: 1px solid #b8afde;">
            <span id="resConv" style="margin-left: 10px; font-size: 16px; font-weight: bold; color: #ac40de;">0h 0m</span>
        </div>

        <div id="calc_container" tabindex="0">
            <div style="background: #fffacd; border-radius: 8px; padding: 5px; text-align: right; margin-bottom: 10px; border: 1px solid rgba(0,0,0,0.1);">
                <div id="h_calc" style="font-size:10px; color:#666;">0</div>
                <div id="r_calc" style="font-size: 20px; font-weight: bold;">0</div>
            </div>
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 5px;">
                <button onclick="cl()" class="btn-calc" style="grid-column: span 2;">AC</button>
                <button onclick="del()" class="btn-calc">⌫</button>
                <button onclick="ao('/')" class="btn-calc">÷</button>
                <button onclick="an('7')" class="btn-calc">7</button><button onclick="an('8')" class="btn-calc">8</button><button onclick="an('9')" class="btn-calc">9</button>
                <button onclick="ao('*')" class="btn-calc">×</button>
                <button onclick="an('4')" class="btn-calc">4</button><button onclick="an('5')" class="btn-calc">5</button><button onclick="an('6')" class="btn-calc">6</button>
                <button onclick="ao('-')" class="btn-calc">-</button>
                <button onclick="an('1')" class="btn-calc">1</button><button onclick="an('2')" class="btn-calc">2</button><button onclick="an('3')" class="btn-calc">3</button>
                <button onclick="ao('+')" class="btn-calc">+</button>
                <button onclick="an('0')" class="btn-calc" style="grid-column: span 2;">0</button>
                <button onclick="calc_eq()" class="btn-calc" style="background: #FF00FF; color:white;">=</button>
            </div>
        </div>
    </div>
</div>

<script>
    var currentTab = 2;
    var editedRows = new Set();

    function showTab(n, btn) {{
        currentTab = n;
        document.querySelectorAll('.tab-content').forEach(t => t.style.display = 'none');
        document.querySelectorAll('.poly-tab-content').forEach(p => p.style.display = 'none');
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.getElementById('tab-flota-' + n).style.display = 'block';
        document.getElementById('polys-' + n).style.display = 'block';
        btn.classList.add('active');
        recalc();
    }}

    function filterFlota(hide) {{
        document.querySelectorAll('#body-' + currentTab + ' tr').forEach(row => {{
            let stock = parseInt(row.querySelector('.f-stock').innerText) || 0;
            row.style.display = (hide && stock === 0) ? 'none' : '';
        }});
    }}

    function stepVal(btn, delta, type) {{
        let row = btn.closest('tr');
        let span = (type === 'u') ? row.querySelector('.u-manual') : row.querySelector('.spr-real-val');
        let val = parseInt(span.innerText) || 0;
        span.innerText = Math.max(0, val + delta);
        editedRows.add(row);
        recalc();
    }}

    function recalc() {{
        let fleet = {{}};
        // 1. Leer flota y aplicar colores de activación (Imagen 2)
        document.querySelectorAll('#body-' + currentTab + ' tr').forEach(row => {{
            let nC = row.querySelector('.edit-name'), sC = row.querySelector('.f-stock'),
                miC = row.querySelector('.edit-spr-min'), maC = row.querySelector('.edit-spr-max'),
                orC = row.querySelector('.edit-orh'), lC = row.querySelector('.f-left');
            let name = nC.innerText.trim(), stock = parseInt(sC.innerText) || 0;
            
            if (name !== "" && name !== "NUEVA UNIDAD") {{
                if (stock > 0) {{
                    nC.style.background = "#ffffff"; nC.style.color = "black";
                    sC.style.background = "#e3defa"; sC.style.color = "black";
                    [miC, maC, orC, lC].forEach(c => {{ c.style.background = "#def4ed"; c.style.color = "#008080"; }});
                }} else {{
                    [nC, sC, miC, maC, orC, lC].forEach(c => {{ c.style.background = "#ebebeb"; c.style.color = "#969696"; }});
                }}
                fleet[name] = {{ min: parseFloat(miC.innerText)||0, max: parseFloat(maC.innerText)||0, stock: stock, used: 0 }};
            }}
        }});

        // 2. Procesar planes
        document.querySelectorAll('#polys-' + currentTab + ' .poligono-bloque').forEach(bl => {{
            let volTotal = parseFloat(bl.querySelector('.v-total-val').innerText) || 0;
            let volAsignadoAcumulado = 0;

            bl.querySelectorAll('.calc-row').forEach(row => {{
                let type = row.querySelector('.s-type').value;
                let spanU = row.querySelector('.u-manual'), spanS = row.querySelector('.spr-real-val');

                if (type !== "SELECCIONAR..." && fleet[type]) {{
                    let f = fleet[type];
                    if (!editedRows.has(row)) {{ spanS.innerText = f.max; editedRows.add(row); }}
                    let uVal = parseInt(spanU.innerText) || 0;
                    let sVal = parseInt(spanS.innerText) || 0;
                    f.used += uVal;
                    volAsignadoAcumulado += (uVal * sVal);
                }}
            }});

            let celdaTotal = bl.querySelector('.v-calculado-total');
            celdaTotal.innerText = Math.round(volAsignadoAcumulado);
            celdaTotal.style.color = (Math.round(volAsignadoAcumulado) === volTotal && volTotal > 0) ? "#20B2AA" : "#d32f2f";
            
            let diffC = bl.querySelector('.p-diff');
            if (volTotal > 0) {{
                let diff = Math.round(volAsignadoAcumulado) - volTotal;
                diffC.innerText = diff === 0 ? "OK" : (diff > 0 ? "EXCESO: "+diff : "FALTAN: "+Math.abs(diff));
                diffC.style.background = diff === 0 ? "#ceedd6" : (diff > 0 ? "#ffe4b5" : "#f7cdd1");
            }} else {{ diffC.innerText = "VACÍO"; diffC.style.background = "transparent"; }}
        }});

        // 3. Actualizar "Me quedan"
        document.querySelectorAll('#body-' + currentTab + ' tr').forEach(row => {{
            let n = row.querySelector('.edit-name').innerText.trim();
            if(fleet[n]) {{
                let rest = fleet[n].stock - fleet[n].used;
                let c = row.querySelector('.f-left');
                c.innerText = rest;
                c.style.color = rest < 0 ? "#FF4500" : (rest === 0 ? "#f25a5a" : "#228B22");
            }}
        }});

        // 4. Actualizar Selects
        document.querySelectorAll('#polys-' + currentTab + ' .s-type').forEach(s => {{
            let cur = s.value;
            let h = '<option>SELECCIONAR...</option>';
            Object.keys(fleet).sort().forEach(name => {{
                h += `<option value="${{name}}">${{name}}</option>`;
            }});
            s.innerHTML = h; s.value = cur;
        }});
    }}

    // Calculadora Logica
    var cur = ""; const rD = document.getElementById('r_calc'), hD = document.getElementById('h_calc');
    function an(n) {{ cur += n; rD.innerText = cur; }}
    function ao(o) {{ if(cur!=="") {{ cur += " " + o + " "; rD.innerText = cur; }} }}
    function cl() {{ cur = ""; rD.innerText = "0"; hD.innerText = "0"; }}
    function del() {{ cur = cur.trim().slice(0, -1); rD.innerText = cur || "0"; }}
    function calc_eq() {{ try {{ let res = eval(cur.replace('×', '*').replace('÷', '/')); hD.innerText = cur + " ="; rD.innerText = res; cur = res.toString(); }} catch {{ rD.innerText = "Err"; }} }}
    function convertirMinutos() {{
        let m = parseInt(document.getElementById('minInp').value) || 0;
        document.getElementById('resConv').innerText = Math.floor(m / 60) + "h " + (m % 60) + "m";
    }}

    setTimeout(recalc, 500);
</script>
"""

# Renderizar en Streamlit (con altura suficiente para evitar scrolls internos molestos)
components.html(html_content, height=1200, scrolling=True)
