import streamlit as st
from streamlit.components.v1 import html

st.set_page_config(page_title="Monitor Logístico VP04", layout="wide")

# Limpieza de márgenes de Streamlit
st.markdown("""
    <style>
    .block-container {padding: 0rem !important;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- DATOS BASE ---
unidades_SDE = {"CROWD 5 HRS": [25, 28], "CROWD 3 HRS": [25, 28], "MOTO 3 HRS": [25, 28]}
unidades_SD = {"MOTO 3 HRS": [25, 25], "MOTO NEWBIE": [20, 22], "CROWD 5 HRS / SMALL VAN": [35, 37]}
unidades_C1 = {"RENTAL LARGE VAN": [120, 120], "SMALL VAN VAR(MLP)":[80, 80], "CAR MLP": [50, 50], "MOTO 3 HRS": [28, 28]}
unidades_C2 = {"LARGE VAN HÍBRIDA": [100, 100], "SMALL VAN VAR(MLP)":[80, 80], "CROWD 5 HRS": [60, 60]}

def gen_master_rows(data_dict, table_id):
    rows = ""
    items = list(data_dict.items())
    for i in range(15):
        name, spr = (items[i][0], items[i][1]) if i < len(items) else ("NUEVA UNIDAD", [0, 0])
        style = "color: #555; background: #ebebeb;" if i < len(items) else "color: #C0C0C0; background: #fcfcfc;"
        rows += f'''
        <tr data-table="{table_id}" class="master-row">
            <td contenteditable="true" class="edit-name" oninput="recalc()" style="{style} font-weight: bold; text-align: left; padding-left: 10px;">{name}</td>
            <td contenteditable="true" class="edit-spr-min" oninput="recalc()" style="{style} font-weight: bold; text-align: center;">{spr[0]}</td>
            <td contenteditable="true" class="edit-spr-max" oninput="recalc()" style="{style} font-weight: bold; text-align: center;">{spr[1]}</td>
            <td contenteditable="true" class="edit-orh" style="{style} font-weight: normal; text-align: center;">480</td>
            <td contenteditable="true" class="f-stock" style="{style} font-weight: bold; text-align: center;" oninput="updateSchedStyle(this); recalc()">0</td>
            <td class="f-left" style="{style} font-weight: bold; text-align: center;">0</td>
        </tr>'''
    return rows

def gen_poligonos():
    polys = ""
    btn_s = "cursor:pointer; border:none; background:rgba(0,0,0,0.05); color:#696969; font-weight:bold; width:18px; height:18px; border-radius:3px; margin:0 2px;"
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
    for i in range(1, 11):
        polys += f'''
        <div class="poligono-bloque" style="margin-bottom: 15px;">
            <table class="meli-table">
                <thead>
                    <tr><th class="header-poly">PLAN {i}</th><th class="header-poly">VOL. TOTAL</th><th class="header-poly"># ASIGNADAS</th><th class="header-poly">SPR REAL</th><th class="header-poly">TIPO DE UNIDAD</th><th class="header-poly">OK</th></tr>
                </thead>
                <tbody>
                    <tr class="calc-row">
                        <td rowspan="5" contenteditable="true" class="v-total" style="background: #D3D3D3; font-weight:bold; text-align:center;">PLAN {i}</td>
                        <td rowspan="5" contenteditable="true" class="v-total-val" oninput="recalc()" style="color: #20B2AA; font-weight: bold; font-size: 16px; text-align: center;">0</td>
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
                    {fila_inner*4}
                    <tr><td colspan="2" style="text-align:center; font-weight:bold; background:#f8f9fa;">ESTADO:</td><td class="v-calculado-total" style="font-weight: bold; font-size: 16px; text-align: center;">0</td><td class="p-diff" colspan="3" style="text-align: center; font-weight: bold;">VACÍO</td></tr>
                </tbody>
            </table>
        </div>'''
    return polys

# --- COMPONENTE HTML ---
full_app_html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: 'Segoe UI', sans-serif; background: #f5f7f9; padding: 20px; }}
        .meli-table {{ border-collapse: separate; border-spacing: 0; width: 100%; font-size: 11px; margin-bottom: 20px; border-radius: 11px; overflow: hidden; border: 2px solid #ccc; box-shadow: 0 4px 8px rgba(0,0,0,0.05); }}
        .header-poly {{ background: linear-gradient(180deg, #888888 0%, #696969 100%); color: white; padding: 8px; text-align: center; }}
        .header-flota {{ background: linear-gradient(180deg, #333333 0%, #000000 100%); color: white; padding: 8px; text-align: center; }}
        .tab-btn {{ padding: 8px 15px; cursor: pointer; border: none; background: #e0e0e0; border-radius: 8px 8px 0 0; font-weight: bold; }}
        .tab-btn.active {{ background: #000000; color: white; }}
        .btn-calc {{ border: 1px solid #ccc; border-radius: 8px; background: white; cursor: pointer; font-weight: bold; padding: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); }}
        #calc_container {{ background: linear-gradient(145deg, #22c5bc, #1da29b); border-radius: 25px; padding: 20px; box-shadow: 8px 8px 16px #acacac; }}
        
        /* Cronómetro Flotante Abajo */
        #crono-wrapper {{ position: fixed; bottom: 20px; right: 20px; z-index: 10000; background: #1a1a1a; padding: 12px; border-radius: 10px; color: white; width: 180px; box-shadow: 0 -4px 15px rgba(0,0,0,0.3); }}
    </style>
</head>
<body>

<div style="display: flex; gap: 20px;">
    <!-- COLUMNA IZQUIERDA -->
    <div style="flex: 1;">
        <div id="polys-2" class="poly-tab-content">{gen_poligonos()}</div>
        <div id="polys-3" class="poly-tab-content" style="display:none;">{gen_poligonos()}</div>
        <div id="polys-1" class="poly-tab-content" style="display:none;">{gen_poligonos()}</div>
        <div id="polys-4" class="poly-tab-content" style="display:none;">{gen_poligonos()}</div>
    </div>

    <!-- COLUMNA DERECHA -->
    <div style="width: 450px; position: sticky; top: 10px;">
        <div style="margin-bottom: 10px;">
            <button class="tab-btn active" onclick="showTab(2, this)">C1</button>
            <button class="tab-btn" onclick="showTab(3, this)">C2</button>
            <button class="tab-btn" onclick="showTab(1, this)">SD</button>
            <button class="tab-btn" onclick="showTab(4, this)">SDE</button>
        </div>
        
        <div class="master-container" style="background: white; padding: 15px; border-radius: 12px; border: 1px solid #ccc;">
            <div id="tab-flota-2" class="tab-content">
                <table class="meli-table">
                    <thead><tr><th class="header-flota">UNIDADES</th><th class="header-flota">min</th><th class="header-flota">max</th><th class="header-flota">ORH</th><th class="header-flota">SCHED</th><th class="header-flota" id="head-left-2">ME QUEDAN</th></tr></thead>
                    <tbody id="body-2">{gen_master_rows(unidades_C1, 2)}</tbody>
                </table>
            </div>
            <div id="tab-flota-3" class="tab-content" style="display:none;">
                <table class="meli-table"><thead><tr><th class="header-flota">UNIDADES</th><th class="header-flota">min</th><th class="header-flota">max</th><th class="header-flota">ORH</th><th class="header-flota">SCHED</th><th class="header-flota" id="head-left-3">ME QUEDAN</th></tr></thead><tbody id="body-3">{gen_master_rows(unidades_C2, 3)}</tbody></table>
            </div>
            <div id="tab-flota-1" class="tab-content" style="display:none;">
                <table class="meli-table"><thead><tr><th class="header-flota">UNIDADES</th><th class="header-flota">min</th><th class="header-flota">max</th><th class="header-flota">ORH</th><th class="header-flota">SCHED</th><th class="header-flota" id="head-left-1">ME QUEDAN</th></tr></thead><tbody id="body-1">{gen_master_rows(unidades_SD, 1)}</tbody></table>
            </div>
            <div id="tab-flota-4" class="tab-content" style="display:none;">
                <table class="meli-table"><thead><tr><th class="header-flota">UNIDADES</th><th class="header-flota">min</th><th class="header-flota">max</th><th class="header-flota">ORH</th><th class="header-flota">SCHED</th><th class="header-flota" id="head-left-4">ME QUEDAN</th></tr></thead><tbody id="body-4">{gen_master_rows(unidades_SDE, 4)}</tbody></table>
            </div>
        </div>

        <div id="calc_container" style="margin-top: 20px;" tabindex="0">
            <div style="background: #fffacd; padding: 10px; text-align: right; margin-bottom: 10px; border-radius: 8px;">
                <div id="h_calc" style="font-size:12px; color:#666;">0</div>
                <div id="r_calc" style="font-size: 24px; font-weight: bold;">0</div>
            </div>
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 5px;">
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

<div id="crono-wrapper">
    <div style="text-align: center;">
        <div id="reloj-f" style="font-size: 11px; color: #00d4ff;">00:00:00</div>
        <div id="display-f" style="font-size: 22px; font-weight: bold; margin: 5px 0;">00:00:00.0</div>
        <div style="display: flex; justify-content: center; gap: 5px;">
            <button id="start-f" style="background:#28a745; border:none; color:white; padding:3px 8px; border-radius:3px;">▶</button>
            <button id="pause-f" style="background:#ffc107; border:none; padding:3px 8px; border-radius:3px;">⏸</button>
            <button id="reset-f" style="background:#dc3545; border:none; color:white; padding:3px 8px; border-radius:3px;">🔄</button>
        </div>
    </div>
</div>

<script>
    var currentTab = 2;
    var editedRows = new Set();
    var curCalc = "";

    // --- NAVEGACIÓN Y TECLADO ---
    document.addEventListener('keydown', function(e) {{
        // Calculadora
        if (document.activeElement.id === 'calc_container') {{
            if (e.key >= '0' && e.key <= '9') an(e.key);
            if (['+', '-', '*', '/'].includes(e.key)) ao(e.key);
            if (e.key === 'Enter') calc_eq();
            if (e.key === 'Backspace') del();
            if (e.key === 'Escape') cl();
            e.preventDefault();
        }}
        // Flechas en tablas
        if (e.target.contentEditable === "true") {{
            let cell = e.target, row = cell.parentElement, cells = Array.from(row.cells), idx = cells.indexOf(cell);
            if (e.key === "ArrowDown" && row.nextElementSibling) row.nextElementSibling.cells[idx].focus();
            if (e.key === "ArrowUp" && row.previousElementSibling) row.previousElementSibling.cells[idx].focus();
        }}
    }});

    function updateSchedStyle(el) {{
        let val = parseInt(el.innerText) || 0;
        el.style.background = val > 0 ? "#FFD700" : "#ebebeb";
        el.style.color = val > 0 ? "black" : "#555";
    }}

    function showTab(n, btn) {{
        currentTab = n;
        document.querySelectorAll('.tab-content, .poly-tab-content').forEach(el => el.style.display = 'none');
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.getElementById('tab-flota-'+n).style.display = 'block';
        document.getElementById('polys-'+n).style.display = 'block';
        btn.classList.add('active'); recalc();
    }}

    function manualEdit(el) {{ editedRows.add(el.closest('tr')); recalc(); }}
    function stepVal(btn, d, type) {{
        let span = type === 'u' ? btn.closest('tr').querySelector('.u-manual') : btn.closest('tr').querySelector('.spr-real-val');
        span.innerText = Math.max(0, (parseInt(span.innerText)||0) + d);
        editedRows.add(btn.closest('tr')); recalc();
    }}

    function recalc() {{
        let fleet = {{}};
        // 1. Leer disponibilidad y aplicar estilos de "ME QUEDAN"
        document.querySelectorAll('#body-' + currentTab + ' tr').forEach(row => {{
            let name = row.querySelector('.edit-name').innerText.trim();
            let stock = parseInt(row.querySelector('.f-stock').innerText) || 0;
            if (name !== "" && name !== "NUEVA UNIDAD") {{
                fleet[name] = {{ min: parseFloat(row.querySelector('.edit-spr-min').innerText)||0, max: parseFloat(row.querySelector('.edit-spr-max').innerText)||0, stock: stock, used: 0 }};
            }}
        }});

        // 2. Procesar Planes
        document.querySelectorAll('#polys-' + currentTab + ' .poligono-bloque').forEach(bl => {{
            let volT = parseFloat(bl.querySelector('.v-total-val').innerText) || 0, volA = 0;
            bl.querySelectorAll('.calc-row').forEach(row => {{
                let type = row.querySelector('.s-type').value, u = parseInt(row.querySelector('.u-manual').innerText) || 0, s = parseInt(row.querySelector('.spr-real-val').innerText) || 0;
                if (type !== "SELECCIONAR..." && fleet[type]) {{
                    if (!editedRows.has(row)) {{ s = fleet[type].max; row.querySelector('.spr-real-val').innerText = s; }}
                    fleet[type].used += u; volA += (u * s);
                    // Validar Alerta SPR
                    row.querySelector('.spr-real-cell').style.background = (s < fleet[type].min || s > fleet[type].max) ? "#ffcccc" : "#def3ed";
                }}
            }});
            
            let resCell = bl.querySelector('.v-calculado-total'), diffCell = bl.querySelector('.p-diff');
            resCell.innerText = Math.round(volA);
            
            if(volT === 0) {{ diffCell.innerText = "VACÍO"; diffCell.style.color = "gray"; resCell.style.color = "black"; }}
            else if(volA >= volT) {{ 
                diffCell.innerText = "ZONA CUBIERTA OK"; diffCell.style.background = "#20B2AA"; diffCell.style.color = "white"; 
                resCell.style.color = "#20B2AA"; 
            }} else {{ 
                diffCell.innerText = "FALTAN: " + Math.round(volT - volA); diffCell.style.background = "#ffcccc"; diffCell.style.color = "red";
                resCell.style.color = "red";
            }}
        }});

        // 3. Actualizar Master y Alertas de Unidades
        let headerLeft = document.getElementById('head-left-' + currentTab);
        let totalLeft = 0;
        document.querySelectorAll('#body-' + currentTab + ' tr').forEach(row => {{
            let n = row.querySelector('.edit-name').innerText.trim();
            if(fleet[n]) {{
                let left = fleet[n].stock - fleet[n].used;
                let cellLeft = row.querySelector('.f-left');
                cellLeft.innerText = left;
                cellLeft.style.background = left < 0 ? "#ffcccc" : "#ebebeb";
                cellLeft.style.color = left < 0 ? "red" : "black";
                totalLeft += left;
            }}
        }});
        headerLeft.innerText = totalLeft < 0 ? "ME PASÉ POR: " + Math.abs(totalLeft) : "ME QUEDAN";
        headerLeft.style.color = totalLeft < 0 ? "red" : "white";

        // 4. Actualizar dropdowns (Solo unidades con Sched > 0)
        document.querySelectorAll('#polys-' + currentTab + ' .s-type').forEach(s => {{
            let cur = s.value, h = '<option>SELECCIONAR...</option>';
            Object.keys(fleet).forEach(name => {{
                if (fleet[name].stock > 0) h += `<option value="${{name}}">${{name}}</option>`;
            }});
            s.innerHTML = h; s.value = cur;
        }});
    }}

    // --- CALCULADORA ---
    function an(n) {{ curCalc += n; document.getElementById('r_calc').innerText = curCalc; }}
    function ao(o) {{ if(curCalc!=="") curCalc += " " + o + " "; document.getElementById('r_calc').innerText = curCalc; }}
    function cl() {{ curCalc = ""; document.getElementById('r_calc').innerText = "0"; document.getElementById('h_calc').innerText = "0"; }}
    function del() {{ curCalc = curCalc.trim().slice(0, -1); document.getElementById('r_calc').innerText = curCalc || "0"; }}
    function calc_eq() {{ try {{ let r = eval(curCalc.replace('×','*').replace('÷','/')); document.getElementById('h_calc').innerText = curCalc + " ="; document.getElementById('r_calc').innerText = r; curCalc = r.toString(); }} catch {{}} }}

    // --- CRONÓMETRO ---
    let st, et=0, run=false, timer;
    document.getElementById('start-f').onclick = () => {{ if(!run){{ run=true; st=Date.now()-et; timer=setInterval(()=>{{ et=Date.now()-st; document.getElementById('display-f').innerText=timeToString(et); }},100); }} }};
    document.getElementById('pause-f').onclick = () => {{ run=false; clearInterval(timer); }};
    document.getElementById('reset-f').onclick = () => {{ run=false; clearInterval(timer); et=0; document.getElementById('display-f').innerText="00:00:00.0"; }};
    function timeToString(t){{ let ms=Math.floor((t%1000)/100), s=Math.floor((t/1000)%60), m=Math.floor((t/60000)%60), h=Math.floor(t/3600000); return `${{h.toString().padStart(2,'0')}}:${{m.toString().padStart(2,'0')}}:${{s.toString().padStart(2,'0')}}.${{ms}}`; }}
    setInterval(()=>{{ document.getElementById('reloj-f').innerText=new Date().toLocaleTimeString(); }}, 1000);

    recalc();
</script>
</body>
</html>
"""

html(full_app_html, height=1800, scrolling=True)
