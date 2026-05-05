import streamlit as st
from streamlit.components.v1 import html

st.set_page_config(page_title="Monitor Logístico - Liliana García", layout="wide")

# CSS para diseño limpio de Streamlit y recuperación de estilos
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
        # Estilo restaurado: Gris para inactivas, se activa con Stock > 0 en JS
        rows += f'''
        <tr class="master-row" data-active="false" style="background: #ebebeb; color: #969696;">
            <td contenteditable="true" class="edit-name" oninput="recalc()" style="font-weight: bold; text-align: left; padding-left: 10px; border: 0.5px solid #ccc; width: 150px;">{name}</td>
            <td contenteditable="true" class="edit-spr-min" oninput="recalc()" style="text-align: center; border: 0.5px solid #ccc; width: 45px;">{spr[0]}</td>
            <td contenteditable="true" class="edit-spr-max" oninput="recalc()" style="text-align: center; border: 0.5px solid #ccc; width: 45px;">{spr[1]}</td>
            <td contenteditable="true" class="edit-orh" style="text-align: center; border: 0.5px solid #ccc; width: 45px;">480</td>
            <td contenteditable="true" class="f-stock" oninput="recalc()" style="text-align: center; border: 0.5px solid #ccc; width: 55px; font-weight: bold; font-size: 16px; background: #fff;">0</td>
            <td class="f-left" style="font-weight: bold; text-align: center; border: 0.5px solid #ccc; width: 60px; font-size: 14px;">0</td>
        </tr>'''
    return rows

def gen_poligonos():
    polys = ""
    btn_s = "cursor:pointer; border:none; background:rgba(0,0,0,0.08); color:#333; font-weight:bold; width:22px; height:22px; border-radius:4px; margin:0 2px;"
    fila_inner = f'''
    <tr class="calc-row">
        <td class="u-manual-cell" style="background: #e3defa; text-align: center; border: 0.6px solid #ccc; padding: 5px;">
            <button style="{btn_s}" onclick="stepVal(this, -1, 'u')">-</button>
            <span contenteditable="true" class="u-manual" oninput="manualEdit(this)" style="font-weight: bold; margin:0 5px;">0</span>
            <button style="{btn_s}" onclick="stepVal(this, 1, 'u')">+</button>
        </td>
        <td class="spr-real-cell" style="background: #def3ed; text-align: center; border: 0.6px solid #ccc; padding: 5px;">
            <button style="{btn_s}" onclick="stepVal(this, -1, 's')">-</button>
            <span contenteditable="true" class="spr-real-val" oninput="manualEdit(this)" style="font-weight: bold; margin:0 5px;">0</span>
            <button style="{btn_s}" onclick="stepVal(this, 1, 's')">+</button>
        </td>
        <td style="border: 0.5px solid #ccc;"><select class="s-type" onchange="resetRow(this)" style="width:100%; border:none; background:transparent; font-weight:bold; font-size:11px;"></select></td>
        <td style="text-align: center; border: 0.5px solid #ccc;"><input type="checkbox" class="ok-check" style="transform: scale(1.3);"></td>
    </tr>'''
    for i in range(1, 11):
        polys += f'''
        <div class="poligono-bloque" style="margin-bottom: 20px; border-radius: 12px; overflow: hidden; background: white; border: 1px solid #e1e1e1;">
            <table style="width: 100%; border-collapse: collapse;">
                <thead style="background: linear-gradient(180deg, #696969, #808080); color: white; font-size: 11px;">
                    <tr><th>PLAN {i}</th><th>VOL. TOTAL</th><th style="width:100px;">UNIDADES</th><th style="width:100px;">SPR REAL</th><th>TIPO</th><th>OK</th></tr>
                </thead>
                <tbody>
                    <tr class="calc-row">
                        <td rowspan="5" contenteditable="true" style="background: #f0f0f0; font-weight:bold; text-align:center; border: 1px solid #ccc; width: 80px;">RUTA</td>
                        <td rowspan="5" contenteditable="true" class="v-total-val" oninput="recalc()" style="color: #20B2AA; font-weight: bold; font-size: 18px; text-align: center; border: 1px solid #ccc; width: 90px;">0</td>
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
                        <td style="border: 0.5px solid #ccc;"><select class="s-type" onchange="resetRow(this)" style="width:100%; border:none; background:transparent; font-weight:bold; font-size:11px;"></select></td>
                        <td style="text-align: center; border: 0.5px solid #ccc; width: 35px;"><input type="checkbox" class="ok-check" style="transform: scale(1.3);"></td>
                    </tr>
                    {fila_inner}{fila_inner}{fila_inner}{fila_inner}
                    <tr style="background:#f8f9fa;">
                        <td colspan="2" style="text-align:center; font-weight:bold; border: 1px solid #ccc; font-size: 11px;">CARGA ACTUAL:</td>
                        <td class="v-calculado-total" style="font-weight: bold; font-size: 16px; color: #d32f2f; border: 1px solid #ccc; text-align: center;">0</td>
                        <td class="p-diff" colspan="3" style="text-align: center; font-weight: bold; border: 1px solid #ccc; font-size: 11px;">ESPERANDO DATOS</td>
                    </tr>
                </tbody>
            </table>
        </div>'''
    return polys

# Renderizado del HTML con Cronómetro y Calculadora Restaurada
app_html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: sans-serif; background: #f5f7f9; padding: 10px; }}
        /* Botones con efecto 3D restaurados */
        .filter-btn {{ cursor: pointer; font-size: 14px; padding: 8px 15px; border-radius: 6px; font-weight: bold; border: none; outline: none; }}
        .btn-activas {{ background: #f0f0f0; color: #333; box-shadow: 0 4px #bbb; margin-right: 8px; border: 1px solid #ccc; }}
        .btn-activas:active {{ box-shadow: 0 1px #bbb; transform: translateY(3px); }}
        .btn-todas {{ background: #20B2AA; color: white; box-shadow: 0 4px #167d77; }}
        .btn-todas:active {{ box-shadow: 0 1px #167d77; transform: translateY(3px); }}

        .meli-table {{ border-collapse: collapse; width: 100%; border-radius: 8px; overflow: hidden; border: 1px solid #ccc; background: white; }}
        .meli-table th {{ background: #222; color: white; font-size: 10px; height: 30px; text-transform: uppercase; }}
        .meli-table td {{ border: 0.5px solid #eee; font-size: 11px; height: 28px; }}

        /* Resaltado de filas activas */
        tr.active-row {{ background: #fff !important; color: #000 !important; }}
        tr.active-row .f-stock {{ background: #fff7e6 !important; color: #ff8c00 !important; border: 1px solid #ff8c00 !important; }}

        /* Cronómetro */
        .crono-card {{ background: #1c1c1c; border-radius: 12px; padding: 15px; color: white; text-align: center; margin-top: 10px; border: 2px solid #333; }}
        .crono-time {{ font-size: 32px; font-family: monospace; color: #00ff00; text-shadow: 0 0 10px #00ff00; }}
        .crono-btn {{ padding: 5px 12px; border-radius: 5px; border: none; cursor: pointer; font-weight: bold; margin: 5px; }}

        /* Calculadora Completa */
        #calc_wrapper {{ background: #22c5bc; border-radius: 15px; padding: 12px; margin-top: 10px; }}
        .calc-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 5px; }}
        .btn-c {{ background: white; border: none; font-weight: bold; border-radius: 6px; padding: 10px; cursor: pointer; font-size: 14px; }}
        .btn-op {{ background: #1a8a84; color: white; }}
        .btn-eq {{ background: #FF00FF; color: white; grid-column: span 2; }}

        .tab-btn {{ padding: 8px 15px; cursor: pointer; border: 1px solid #bbb; background: #dcdcdc; border-radius: 6px 6px 0 0; font-weight: bold; font-size: 12px; }}
        .tab-btn.active {{ background: #000; color: white; }}
    </style>
</head>
<body>

<div style="display: flex; gap: 15px;">
    <!-- COLUMNA IZQUIERDA: POLÍGONOS -->
    <div style="flex: 1;">
        <div style="background: #696969; color: white; padding: 8px; border-radius: 6px; text-align: center; font-weight: bold; margin-bottom: 10px;">PLANIFICACIÓN POR POLÍGONOS</div>
        <div id="polys-2" class="p-content">{gen_poligonos()}</div>
        <div id="polys-3" class="p-content" style="display:none;">{gen_poligonos()}</div>
        <div id="polys-1" class="p-content" style="display:none;">{gen_poligonos()}</div>
        <div id="polys-4" class="p-content" style="display:none;">{gen_poligonos()}</div>
    </div>

    <!-- COLUMNA DERECHA: FLOTA Y HERRAMIENTAS -->
    <div style="width: 420px;">
        <div style="background: #000; color: white; padding: 8px; border-radius: 6px; font-weight: bold; text-align: center; margin-bottom: 10px;">DISPONIBILIDAD DE FLOTA</div>
        <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 5px;">
            <div>
                <button class="tab-btn active" onclick="showTab(2, this)">C1</button>
                <button class="tab-btn" onclick="showTab(3, this)">C2</button>
                <button class="tab-btn" onclick="showTab(1, this)">SD</button>
                <button class="tab-btn" onclick="showTab(4, this)">SDE</button>
            </div>
            <div>
                <button onclick="filterRows(true)" class="filter-btn btn-activas">ACTIVAS</button>
                <button onclick="filterRows(false)" class="filter-btn btn-todas">TODAS</button>
            </div>
        </div>

        <div id="tab-2" class="t-content">
            <table class="meli-table">
                <thead><tr><th rowspan="2">UNIDAD</th><th colspan="2">SPR</th><th rowspan="2">MIN</th><th rowspan="2">STK</th><th rowspan="2">RES</th></tr><tr><th>MIN</th><th>MAX</th></tr></thead>
                <tbody id="body-2">{gen_master_rows(u_C1, 2)}</tbody>
            </table>
        </div>
        <!-- (Otras pestañas se generan igual mediante JS) -->
        <div id="tab-3" class="t-content" style="display:none;"><table class="meli-table"><thead><tr><th rowspan="2">UNIDAD</th><th colspan="2">SPR</th><th rowspan="2">MIN</th><th rowspan="2">STK</th><th rowspan="2">RES</th></tr><tr><th>MIN</th><th>MAX</th></tr></thead><tbody id="body-3">{gen_master_rows(u_C2, 3)}</tbody></table></div>
        <div id="tab-1" class="t-content" style="display:none;"><table class="meli-table"><thead><tr><th rowspan="2">UNIDAD</th><th colspan="2">SPR</th><th rowspan="2">MIN</th><th rowspan="2">STK</th><th rowspan="2">RES</th></tr><tr><th>MIN</th><th>MAX</th></tr></thead><tbody id="body-1">{gen_master_rows(u_SD, 1)}</tbody></table></div>
        <div id="tab-4" class="t-content" style="display:none;"><table class="meli-table"><thead><tr><th rowspan="2">UNIDAD</th><th colspan="2">SPR</th><th rowspan="2">MIN</th><th rowspan="2">STK</th><th rowspan="2">RES</th></tr><tr><th>MIN</th><th>MAX</th></tr></thead><tbody id="body-4">{gen_master_rows(u_SDE, 4)}</tbody></table></div>

        <!-- HERRAMIENTAS -->
        <div class="crono-card">
            <div style="font-size:12px; color:#aaa; margin-bottom:5px;">⏱️ TIEMPO DE OPERACIÓN</div>
            <div id="display-crono" class="crono-time">00:00:00</div>
            <button class="crono-btn" style="background:#28a745; color:white;" onclick="startCrono()">INICIAR</button>
            <button class="crono-btn" style="background:#dc3545; color:white;" onclick="stopCrono()">PARAR</button>
            <button class="crono-btn" style="background:#6c757d; color:white;" onclick="resetCrono()">RESETEAR</button>
        </div>

        <div id="calc_wrapper">
            <div style="background:white; border-radius:6px; padding:8px; text-align:right; margin-bottom:8px; font-size:20px; font-weight:bold; height:30px;" id="calc_display">0</div>
            <div class="calc-grid">
                <button onclick="cl()" class="btn-c" style="background:#ff4444; color:white;">AC</button>
                <button onclick="del()" class="btn-c">⌫</button>
                <button onclick="ao('/')" class="btn-c btn-op">÷</button>
                <button onclick="ao('*')" class="btn-c btn-op">×</button>
                
                <button onclick="an('7')" class="btn-c">7</button><button onclick="an('8')" class="btn-c">8</button><button onclick="an('9')" class="btn-c">9</button>
                <button onclick="ao('-')" class="btn-c btn-op">-</button>
                
                <button onclick="an('4')" class="btn-c">4</button><button onclick="an('5')" class="btn-c">5</button><button onclick="an('6')" class="btn-c">6</button>
                <button onclick="ao('+')" class="btn-c btn-op">+</button>
                
                <button onclick="an('1')" class="btn-c">1</button><button onclick="an('2')" class="btn-c">2</button><button onclick="an('3')" class="btn-c">3</button>
                <button onclick="an('0')" class="btn-c">0</button>
                
                <button onclick="an('.')" class="btn-c">.</button>
                <button onclick="calc_eq()" class="btn-c btn-eq">=</button>
            </div>
        </div>
    </div>
</div>

<script>
    let currentTab = 2;
    let editedRowsPlan = new Set();
    let curC = "";
    
    // CRONÓMETRO
    let startTime, timerInterval;
    function startCrono() {{
        if (!timerInterval) {{
            startTime = Date.now() - (startTime || 0);
            timerInterval = setInterval(updateCrono, 1000);
        }}
    }}
    function stopCrono() {{ clearInterval(timerInterval); timerInterval = null; startTime = Date.now() - startTime; }}
    function resetCrono() {{ stopCrono(); startTime = 0; document.getElementById('display-crono').innerText = "00:00:00"; }}
    function updateCrono() {{
        let diff = Date.now() - startTime;
        let h = Math.floor(diff / 3600000);
        let m = Math.floor((diff % 3600000) / 60000);
        let s = Math.floor((diff % 60000) / 1000);
        document.getElementById('display-crono').innerText = 
            [h, m, s].map(v => v < 10 ? "0" + v : v).join(":");
    }}

    // CALCULADORA
    function an(n) {{ curC += n; updateCalc(); }}
    function ao(o) {{ curC += " " + o + " "; updateCalc(); }}
    function cl() {{ curC = ""; updateCalc(); }}
    function del() {{ curC = curC.trim().slice(0, -1); updateCalc(); }}
    function updateCalc() {{ document.getElementById('calc_display').innerText = curC || "0"; }}
    function calc_eq() {{ try {{ curC = eval(curC).toString(); updateCalc(); }} catch {{ curC = "Error"; updateCalc(); }} }}

    // LÓGICA DE TABLAS
    function showTab(n, btn) {{
        currentTab = n;
        document.querySelectorAll('.p-content, .t-content').forEach(el => el.style.display = 'none');
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.getElementById('polys-'+n).style.display = 'block';
        document.getElementById('tab-'+n).style.display = 'block';
        btn.classList.add('active');
        recalc();
    }}

    function recalc() {{
        let fleet = {{}};
        document.querySelectorAll('#body-' + currentTab + ' tr').forEach(row => {{
            let name = row.querySelector('.edit-name').innerText.trim();
            let stock = parseInt(row.querySelector('.f-stock').innerText) || 0;
            let maxSpr = parseFloat(row.querySelector('.edit-spr-max').innerText) || 0;
            
            // Efecto Visual: Si tiene stock, se colorea la fila
            if(stock > 0) {{
                row.classList.add('active-row');
                row.style.background = "#fff";
                row.style.color = "#000";
            }} else {{
                row.classList.remove('active-row');
                row.style.background = "#ebebeb";
                row.style.color = "#969696";
            }}

            if(name !== "" && name !== "NUEVA UNIDAD") {{
                fleet[name] = {{ max: maxSpr, stock: stock, used: 0 }};
            }}
        }});

        document.querySelectorAll('#polys-' + currentTab + ' .poligono-bloque').forEach(bl => {{
            let vT = parseFloat(bl.querySelector('.v-total-val').innerText) || 0, vA = 0;
            bl.querySelectorAll('.calc-row').forEach(r => {{
                let s = r.querySelector('.s-type').value, u = parseInt(r.querySelector('.u-manual').innerText) || 0;
                let sp = r.querySelector('.spr-real-val');
                if(s !== "SELECCIONAR..." && fleet[s]) {{
                    if(!editedRowsPlan.has(r)) sp.innerText = fleet[s].max;
                    fleet[s].used += u; 
                    vA += (u * parseFloat(sp.innerText));
                }}
            }});
            let dispTotal = bl.querySelector('.v-calculado-total');
            dispTotal.innerText = Math.round(vA);
            
            // Diferencia y colores de estado
            let diff = vA - vT;
            let pDiff = bl.querySelector('.p-diff');
            if(vT === 0) {{ pDiff.innerText = "SIN VOLUMEN"; pDiff.style.color = "#999"; }}
            else if(diff >= 0) {{ pDiff.innerText = "CUBIERTO (+" + Math.round(diff) + ")"; pDiff.style.color = "#28a745"; }}
            else {{ pDiff.innerText = "FALTANTE (" + Math.round(diff) + ")"; pDiff.style.color = "#dc3545"; }}
        }});

        // Actualizar Selects
        document.querySelectorAll('#polys-' + currentTab + ' .s-type').forEach(s => {{
            let cur = s.value, opt = '<option>SELECCIONAR...</option>';
            Object.keys(fleet).forEach(k => {{ if(fleet[k].stock > 0 || k === cur) opt += `<option value="${{k}}">${{k}}</option>`; }});
            s.innerHTML = opt; s.value = cur;
        }});
        
        // Actualizar Restante en Flota
        document.querySelectorAll('#body-' + currentTab + ' tr').forEach(row => {{
            let name = row.querySelector('.edit-name').innerText.trim();
            if(fleet[name]) {{
                row.querySelector('.f-left').innerText = fleet[name].stock - fleet[name].used;
            }}
        }});
    }}

    function stepVal(btn, delta, type) {{
        let row = btn.closest('tr');
        let sel = row.querySelector('.s-type').value;
        if(sel === "SELECCIONAR...") return;
        let span = (type === 'u') ? row.querySelector('.u-manual') : row.querySelector('.spr-real-val');
        let val = parseFloat(span.innerText) || 0;
        span.innerText = type === 'u' ? Math.max(0, val + delta) : Math.max(0, val + delta).toFixed(1);
        editedRowsPlan.add(row);
        recalc();
    }}

    function filterRows(onlyActive) {{
        document.querySelectorAll('#body-' + currentTab + ' tr').forEach(row => {{
            const stock = parseInt(row.querySelector('.f-stock').innerText) || 0;
            row.style.display = (onlyActive && stock === 0) ? 'none' : '';
        }});
    }}

    function manualEdit(el) {{ editedRowsPlan.add(el.closest('tr')); recalc(); }}
    function resetRow(sel) {{ let r=sel.closest('tr'); r.querySelector('.u-manual').innerText="0"; r.querySelector('.spr-real-val').innerText="0"; editedRowsPlan.delete(r); recalc(); }}

    recalc();
</script>
</body>
</html>
"""

html(app_html, height=1200, scrolling=True)
