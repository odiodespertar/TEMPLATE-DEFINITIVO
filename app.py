import streamlit as st
from streamlit.components.v1 import html

st.set_page_config(page_title="Monitor Logístico VP04", layout="wide")

st.markdown("""
    <style>
    .block-container {padding: 0rem !important;}
    footer, #MainMenu, header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- DATOS BASE ---
u_C1 = {"RENTAL LARGE VAN": [120, 120], "SMALL VAN VAR(MLP)":[80, 80], "CAR MLP": [50, 50], "MOTO 3 HRS": [28, 28]}
u_C2 = {"LARGE VAN HÍBRIDA": [100, 100], "SMALL VAN VAR(MLP)":[80, 80], "CROWD 5 HRS": [60, 60]}
u_SD = {"MOTO 3 HRS": [25, 25], "MOTO NEWBIE": [20, 22], "CROWD 5 HRS / SMALL VAN": [35, 37]}
u_SDE = {"CROWD 5 HRS": [25, 28], "CROWD 3 HRS": [25, 28], "MOTO 3 HRS": [25, 28]}

def gen_master_rows(data_dict, table_id):
    rows = ""
    items = list(data_dict.items())
    for i in range(15):
        is_real = i < len(items)
        name, spr = (items[i][0], items[i][1]) if is_real else ("NUEVA UNIDAD", [0, 0])
        # Gris más oscuro para unidades con nombre, claro para "Nueva unidad"
        text_color = "#444" if is_real else "#C0C0C0"
        rows += f'''
        <tr data-table="{table_id}" class="master-row" style="color: {text_color}; background: #ebebeb;">
            <td contenteditable="true" class="edit-name" oninput="recalc()" style="font-weight: bold; width: 140px; text-align: left; padding-left: 5px;">{name}</td>
            <td contenteditable="true" class="edit-spr-min" oninput="recalc()" style="width: 45px; text-align: center;">{spr[0]}</td>
            <td contenteditable="true" class="edit-spr-max" oninput="recalc()" style="width: 45px; text-align: center;">{spr[1]}</td>
            <td contenteditable="true" class="edit-orh" style="width: 45px; text-align: center;">480</td>
            <td contenteditable="true" class="f-stock" oninput="recalc()" style="font-weight: bold; width: 50px; text-align: center;">0</td>
            <td class="f-left" style="font-weight: bold; width: 80px; text-align: center;">0</td>
        </tr>'''
    return rows

def gen_poligonos():
    polys = ""
    btn_s = "cursor:pointer; border:none; background:rgba(0,0,0,0.05); color:#696969; font-weight:bold; width:18px; height:18px; border-radius:3px;"
    fila_inner = f'''
    <tr class="calc-row">
        <td class="u-manual-cell" style="background: #e3defa; text-align: center; width: 90px;">
            <button style="{btn_s}" onclick="stepVal(this, -1, 'u')">-</button>
            <span contenteditable="true" class="u-manual" oninput="manualEdit(this)">0</span>
            <button style="{btn_s}" onclick="stepVal(this, 1, 'u')">+</button>
        </td>
        <td class="spr-real-cell" style="background: #def3ed; text-align: center; width: 80px;">
            <button style="{btn_s}" onclick="stepVal(this, -1, 's')">-</button>
            <span contenteditable="true" class="spr-real-val" oninput="manualEdit(this)">0</span>
            <button style="{btn_s}" onclick="stepVal(this, 1, 's')">+</button>
        </td>
        <td style="width: 150px;"><select class="s-type" onchange="resetRow(this)" style="width: 100%; border:none; background:transparent; font-size: 10px;"><option>SELECCIONAR...</option></select></td>
        <td style="text-align: center; width: 35px;"><input type="checkbox" class="ok-check"></td>
    </tr>'''
    for i in range(1, 11):
        polys += f'''
        <div class="poligono-bloque" style="margin-bottom: 12px; border: 2px solid #ccc; border-radius: 8px; overflow: hidden; background: white;">
            <table class="meli-table" style="table-layout: fixed; width: 100%;">
                <thead>
                    <tr><th class="h-p">PLAN {i}</th><th class="h-p">VOL. TOTAL</th><th class="h-p"># ASIGNADAS</th><th class="h-p">SPR REAL</th><th class="h-p">TIPO UNIDAD</th><th class="h-p">OK</th></tr>
                </thead>
                <tbody>
                    <tr class="calc-row">
                        <td rowspan="5" contenteditable="true" class="v-total" style="background: #D3D3D3; font-weight:bold; text-align:center; width: 80px;">P{i}</td>
                        <td rowspan="5" contenteditable="true" class="v-total-val" oninput="recalc()" style="color: #20B2AA; font-weight: bold; font-size: 16px; text-align: center; width: 70px;">0</td>
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
                        <td><select class="s-type" onchange="resetRow(this)" style="width: 100%; border:none; background:transparent; font-size: 10px;"><option>SELECCIONAR...</option></select></td>
                        <td style="text-align: center;"><input type="checkbox" class="ok-check"></td>
                    </tr>
                    {fila_inner*4}
                    <tr style="height: 25px;"><td colspan="2" style="text-align:center; font-weight:bold; background:#f0f0f0;">ESTADO:</td><td class="v-calculado-total" style="font-weight: bold; text-align: center;">0</td><td class="p-diff" colspan="3" style="text-align: center; font-weight: bold;">VACÍO</td></tr>
                </tbody>
            </table>
        </div>'''
    return polys

full_app_html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: 'Segoe UI', sans-serif; background: #f5f7f9; padding: 15px; width: 1200px; margin: 0 auto; }}
        .meli-table {{ border-collapse: collapse; font-size: 11px; table-layout: fixed; }}
        .meli-table td, .meli-table th {{ border: 1px solid #bbb; padding: 3px; height: 22px; }}
        .h-p {{ background: #696969; color: white; }}
        .h-f {{ background: #000; color: white; }}
        .tab-btn {{ padding: 6px 12px; cursor: pointer; border: none; background: #ccc; border-radius: 5px 5px 0 0; font-weight: bold; }}
        .tab-btn.active {{ background: #000; color: #fff; }}
        
        #calc_container:focus-within {{ outline: 4px solid #FF00FF; box-shadow: 0 0 15px #FF00FF; }}
        #calc_container {{ background: #22c5bc; border-radius: 15px; padding: 15px; margin-top: 15px; }}
        .btn-calc {{ border: 1px solid #ccc; border-radius: 5px; background: white; cursor: pointer; font-weight: bold; padding: 8px; }}
        
        #block-alert {{ position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(255,77,77,0.9); z-index: 20000; display: none; flex-direction: column; justify-content: center; align-items: center; color: white; text-align: center; }}
        #block-alert h1 {{ font-size: 40px; margin-bottom: 20px; }}
    </style>
</head>
<body>

<div id="block-alert">
    <h1>⚠️ UNIDADES AGOTADAS</h1>
    <p style="font-size: 24px;">No hay unidades disponibles. <br>Favor de contactar al service para solicitar más.</p>
    <p style="margin-top: 30px;">Presiona ENTER para cerrar</p>
</div>

<div style="display: flex; gap: 20px;">
    <div style="width: 700px;">
        <div style="background: #696969; color: white; padding: 8px; text-align: center; font-weight: bold; border-radius: 5px; margin-bottom: 10px;">📋 PLANES GENERADOS</div>
        <div id="polys-2" class="p-cont">{gen_poligonos()}</div>
        <div id="polys-3" class="p-cont" style="display:none;">{gen_poligonos()}</div>
        <div id="polys-1" class="p-cont" style="display:none;">{gen_poligonos()}</div>
        <div id="polys-4" class="p-cont" style="display:none;">{gen_poligonos()}</div>
    </div>

    <div style="width: 450px; position: sticky; top: 10px;">
        <div style="background: #000; color: white; padding: 8px; text-align: center; font-weight: bold; border-radius: 5px; margin-bottom: 5px;">🚚 DISPONIBILIDAD DE FLOTA</div>
        
        <div style="display: flex; justify-content: space-between; align-items: flex-end;">
            <div>
                <button class="tab-btn active" onclick="showTab(2, this)">C1</button>
                <button class="tab-btn" onclick="showTab(3, this)">C2</button>
                <button class="tab-btn" onclick="showTab(1, this)">SD</button>
                <button class="tab-btn" onclick="showTab(4, this)">SDE</button>
            </div>
            <div style="padding-bottom: 5px;">
                <button onclick="filterFlota(true)" style="background: #C0C0C0; padding: 4px 8px; border-radius: 4px; font-weight:bold; cursor:pointer;">ACTIVAS</button>
                <button onclick="filterFlota(false)" style="background: #20B2AA; color: white; padding: 4px 8px; border-radius: 4px; font-weight:bold; cursor:pointer;">TODAS</button>
            </div>
        </div>

        <div style="background: white; padding: 10px; border: 1px solid #ccc; border-radius: 0 0 10px 10px;">
            <table class="meli-table" style="width: 100%;">
                <thead>
                    <tr>
                        <th class="h-f" rowspan="2">UNIDAD</th>
                        <th class="h-f" colspan="2" id="header-spr">SPR</th>
                        <th class="h-f" rowspan="2">ORH</th>
                        <th class="h-f" rowspan="2">SCHED</th>
                        <th class="h-f" rowspan="2" id="header-left">ME QUEDAN</th>
                    </tr>
                    <tr><th class="h-f">min</th><th class="h-f">max</th></tr>
                </thead>
                <tbody id="body-2">{gen_master_rows(u_C1, 2)}</tbody>
                <tbody id="body-3" style="display:none;">{gen_master_rows(u_C2, 3)}</tbody>
                <tbody id="body-1" style="display:none;">{gen_master_rows(u_SD, 1)}</tbody>
                <tbody id="body-4" style="display:none;">{gen_master_rows(u_SDE, 4)}</tbody>
            </table>
        </div>

        <div id="calc_container" tabindex="0">
            <div style="background: #fffacd; padding: 8px; text-align: right; border-radius: 5px; margin-bottom: 10px; font-weight: bold; font-size: 18px;" id="r_calc">0</div>
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 5px;">
                <button onclick="cl()" class="btn-calc" style="grid-column: span 2;">AC</button>
                <button onclick="del()" class="btn-calc">⌫</button><button onclick="ao('/')" class="btn-calc">÷</button>
                <button onclick="an('7')" class="btn-calc">7</button><button onclick="an('8')" class="btn-calc">8</button><button onclick="an('9')" class="btn-calc">9</button><button onclick="ao('*')" class="btn-calc">×</button>
                <button onclick="an('4')" class="btn-calc">4</button><button onclick="an('5')" class="btn-calc">5</button><button onclick="an('6')" class="btn-calc">6</button><button onclick="ao('-')" class="btn-calc">-</button>
                <button onclick="an('1')" class="btn-calc">1</button><button onclick="an('2')" class="btn-calc">2</button><button onclick="an('3')" class="btn-calc">3</button><button onclick="ao('+')" class="btn-calc">+</button>
                <button onclick="an('0')" class="btn-calc" style="grid-column: span 2;">0</button>
                <button onclick="calc_eq()" class="btn-calc" style="background: #FF00FF; color: white;">=</button>
            </div>
        </div>

        <div style="margin-top: 15px; background: #1a1a1a; padding: 12px; border-radius: 12px; color: white;">
            <div id="reloj-actual" style="font-size: 14px; text-align: center; color: #aaa; margin-bottom: 5px;">00:00:00</div>
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div id="display-f" style="font-size: 24px; font-family: monospace; font-weight: bold;">00:00:00.0</div>
                <div style="display: flex; gap: 5px;">
                    <button onclick="t_start()" style="background:#28a745; border:none; color:white; padding:5px 10px; border-radius:4px; cursor:pointer;">▶</button>
                    <button onclick="t_stop()" style="background:#ffc107; border:none; padding:5px 10px; border-radius:4px; cursor:pointer;">⏸</button>
                    <button onclick="t_reset()" style="background:#dc3545; border:none; color:white; padding:5px 10px; border-radius:4px; cursor:pointer;">🔄</button>
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
        document.querySelectorAll('.p-cont, tbody[id^="body-"]').forEach(el => el.style.display = 'none');
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.getElementById('polys-'+n).style.display = 'block';
        document.getElementById('body-'+n).style.display = 'table-row-group';
        btn.classList.add('active'); recalc();
    }}

    function filterFlota(hide) {{
        document.querySelectorAll('#body-' + curTab + ' tr').forEach(row => {{
            let s = parseInt(row.querySelector('.f-stock').innerText) || 0;
            row.style.display = (hide && s === 0) ? 'none' : '';
        }});
    }}

    function stepVal(btn, d, t) {{
        let row = btn.closest('tr');
        let type = row.querySelector('.s-type').value;
        if(type === "SELECCIONAR...") return;

        let span = t === 'u' ? row.querySelector('.u-manual') : row.querySelector('.spr-real-val');
        let currentVal = parseInt(span.innerText) || 0;
        
        // Bloqueo de unidades (No SDE)
        if(t === 'u' && d > 0 && curTab !== 4) {{
            let leftCell = document.querySelector(`.master-row[data-table="${{curTab}}"] .edit-name:contains-exact("${{type}}")`);
            if(!leftCell) {{ // Buscamos por texto
                 let allNames = document.querySelectorAll('#body-' + curTab + ' .edit-name');
                 for(let n of allNames) {{ if(n.innerText.trim() === type) leftCell = n; }}
            }}
            let leftVal = parseInt(leftCell.parentElement.querySelector('.f-left').innerText);
            if(leftVal <= 0) {{
                document.getElementById('block-alert').style.display = 'flex';
                return;
            }}
        }}

        span.innerText = Math.max(0, currentVal + d);
        edited.add(row); recalc();
    }}

    function manualEdit(el) {{ edited.add(el.closest('tr')); recalc(); }}

    function recalc() {{
        let fleet = {{}}, hasOver = false;
        document.querySelectorAll('#body-' + curTab + ' tr').forEach(row => {{
            let name = row.querySelector('.edit-name').innerText.trim();
            let sched = parseInt(row.querySelector('.f-stock').innerText) || 0;
            
            // Lógica de Colores Dinámicos
            if(sched > 0) {{
                row.style.background = "#fff"; row.style.color = "#000";
                row.querySelector('.f-stock').style.background = "#e3defa";
                row.querySelector('.edit-spr-min').style.background = "#def3ed";
                row.querySelector('.edit-spr-max').style.background = "#def3ed";
                fleet[name] = {{ min: parseFloat(row.querySelector('.edit-spr-min').innerText)||0, max: parseFloat(row.querySelector('.edit-spr-max').innerText)||0, stock: sched, used: 0 }};
            }} else {{
                row.style.background = "#ebebeb"; 
                row.querySelector('.f-stock').style.background = "transparent";
                row.querySelector('.edit-spr-min').style.background = "transparent";
                row.querySelector('.edit-spr-max').style.background = "transparent";
            }}
        }});

        document.querySelectorAll('#polys-' + curTab + ' .poligono-bloque').forEach(bl => {{
            let vT = parseFloat(bl.querySelector('.v-total-val').innerText) || 0, vA = 0;
            bl.querySelectorAll('.calc-row').forEach(row => {{
                let type = row.querySelector('.s-type').value;
                let u = parseInt(row.querySelector('.u-manual').innerText) || 0;
                let sCell = row.querySelector('.spr-real-val');
                let sVal = parseInt(sCell.innerText) || 0;

                if (type !== "SELECCIONAR..." && fleet[type]) {{
                    if (!edited.has(row)) {{ sVal = fleet[type].max; sCell.innerText = sVal; }}
                    fleet[type].used += u; vA += (u * sVal);
                }}
            }});
            let res = bl.querySelector('.v-calculado-total'), dif = bl.querySelector('.p-diff');
            res.innerText = Math.round(vA);
            if(vT === 0) {{ dif.innerText = "VACÍO"; dif.style.background = "none"; }}
            else if(vA >= vT) {{ dif.innerText = "OK"; dif.style.background = "#20B2AA"; dif.style.color="#fff"; }}
            else {{ dif.innerText = "FALTAN: " + Math.round(vT - vA); dif.style.background = "#ff4d4d"; dif.style.color="#fff"; }}
        }});

        // Actualizar ME QUEDAN / ME PASÉ
        let headLeft = document.getElementById('header-left');
        document.querySelectorAll('#body-' + curTab + ' tr').forEach(row => {{
            let n = row.querySelector('.edit-name').innerText.trim();
            if(fleet[n]) {{
                let diff = fleet[n].stock - fleet[n].used;
                let leftCell = row.querySelector('.f-left');
                leftCell.innerText = Math.abs(diff);
                if(diff < 0) {{
                    leftCell.style.color = "red";
                    headLeft.innerText = "ME PASÉ POR";
                    hasOver = true;
                }} else {{
                    leftCell.style.color = "black";
                    headLeft.innerText = "ME QUEDAN";
                }}
            }}
        }});

        // Dropdowns de Planes
        document.querySelectorAll('#polys-' + curTab + ' .s-type').forEach(sel => {{
            let val = sel.value;
            let opt = '<option>SELECCIONAR...</option>';
            Object.keys(fleet).forEach(n => opt += `<option value="${{n}}">${{n}}</option>`);
            sel.innerHTML = opt; sel.value = val;
        }});
    }}

    // Reloj y Crono
    setInterval(() => {{ document.getElementById('reloj-actual').innerText = new Date().toLocaleTimeString(); }}, 1000);
    
    document.addEventListener('keydown', (e) => {{
        if(e.key === 'Enter') document.getElementById('block-alert').style.display = 'none';
        if (e.target.contentEditable === "true") {{
            let c = e.target, r = c.parentElement, idx = Array.from(r.cells).indexOf(c);
            if (e.key === "ArrowDown" && r.nextElementSibling) r.nextElementSibling.cells[idx].focus();
            if (e.key === "ArrowUp" && r.previousElementSibling) r.previousElementSibling.cells[idx].focus();
            if (e.key === "ArrowRight" && idx < r.cells.length - 1) r.cells[idx+1].focus();
            if (e.key === "ArrowLeft" && idx > 0) r.cells[idx-1].focus();
        }}
    }});

    function an(n){{ curC += n; document.getElementById('r_calc').innerText = curC; }}
    function ao(o){{ curC += " "+o+" "; document.getElementById('r_calc').innerText = curC; }}
    function cl(){{ curC = ""; document.getElementById('r_calc').innerText = "0"; }}
    function del(){{ curC = curC.trim().slice(0,-1); document.getElementById('r_calc').innerText = curC || "0"; }}
    function calc_eq(){{ try{{ curC = eval(curC).toString(); document.getElementById('r_calc').innerText = curC; }}catch{{}} }}

    let sT, eT=0, r_run=false, t_int;
    function t_start(){{ if(!r_run){{ r_run=true; sT=Date.now()-eT; t_int=setInterval(()=>{{ eT=Date.now()-sT; document.getElementById('display-f').innerText=fmt(eT); }},100); }} }}
    function t_stop(){{ r_run=false; clearInterval(t_int); }}
    function t_reset(){{ r_run=false; clearInterval(t_int); eT=0; document.getElementById('display-f').innerText="00:00:00.0"; }}
    function fmt(t){{ let ms=Math.floor((t%1000)/100), s=Math.floor((t/1000)%60), m=Math.floor((t/60000)%60), h=Math.floor(t/3600000); return `${{h.toString().padStart(2,'0')}}:${{m.toString().padStart(2,'0')}}:${{s.toString().padStart(2,'0')}}.${{ms}}`; }}
    
    recalc();
</script>
</body>
</html>
"""

html(full_app_html, height=1800, scrolling=True)
