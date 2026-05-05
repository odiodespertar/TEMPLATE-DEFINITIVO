import streamlit as st
from streamlit.components.v1 import html

# Configuración de página con título personalizado
st.set_page_config(page_title="Monitor Logístico - Liliana García", layout="wide")

# Ocultar elementos de Streamlit y fondo limpio
st.markdown("""
    <style>
    .block-container {padding: 0rem !important;}
    footer, #MainMenu, header {visibility: hidden;}
    body { background-color: #f5f7f9; }
    </style>
""", unsafe_allow_html=True)

# --- 1. DATOS DE UNIDADES (CATÁLOGOS ACTUALIZADOS) ---
u_SDE = {"CROWD 5 HRS": [25, 28], "CROWD 5 HRS EXTENDIDA": [25, 28], "CROWD 3 HRS": [25, 28], "MOTO 3 HRS": [25, 28]}
u_SD = {"MOTO 3 HRS": [25, 25], "MOTO NEWBIE": [20, 22], "CROWD 5 HRS / SMALL VAN": [35, 37]}
u_C1 = {
    "RENTAL ELEC LARGE VAN": [120, 120], "RENTAL ELEC SMALL VAN": [120, 120], "RENTAL LARGE VAN": [120, 120], 
    "RENTAL SMALL VAN": [120, 120], "LARGE VAN VAR(MLP)": [100, 100], "SMALL VAN VAR(MLP)":[80, 80],
    "CAR MLP": [50, 50], "MOTO 3 HRS": [28, 28], "CROWD NEWBIE 3 hrs": [30, 30], "CROWD EXTRA 8 HRS": [80, 85], "CROWD 5 HRS": [60, 60]
}
u_C2 = u_C1.copy()
u_C2["LARGE VAN HÍBRIDA"] = [100, 100]

# --- 2. GENERADORES DE HTML CON DISEÑO FIJO (ESTILO COLAB) ---
def gen_master_rows(data_dict, table_id):
    rows = ""
    items = list(data_dict.items())
    for i in range(15):
        is_real = i < len(items)
        name, spr = (items[i][0], items[i][1]) if is_real else ("NUEVA UNIDAD", [0, 0])
        st_base = "background: #ebebeb; color: #969696;" if is_real else "background: #fcfcfc; color: #C0C0C0;"
        rows += f'''
        <tr data-table="{table_id}" class="master-row" style="{st_base}">
            <td contenteditable="true" class="edit-name" oninput="recalc()" style="font-weight: bold; text-align: left; padding-left: 10px; border: 0.5px solid #ccc; width: 140px; white-space: nowrap; overflow: visible;">{name}</td>
            <td contenteditable="true" class="edit-spr-min" oninput="recalc()" style="text-align: center; border: 0.5px solid #ccc; width: 35px;">{spr[0]}</td>
            <td contenteditable="true" class="edit-spr-max" oninput="recalc()" style="text-align: center; border: 0.5px solid #ccc; width: 35px;">{spr[1]}</td>
            <td contenteditable="true" class="edit-orh" style="text-align: center; border: 0.5px solid #ccc; width: 35px;">480</td>
            <td contenteditable="true" class="f-stock" oninput="recalc()" style="text-align: center; border: 0.5px solid #ccc; width: 35px; font-weight: bold;">0</td>
            <td class="f-left" style="font-weight: bold; text-align: center; border: 0.5px solid #ccc; width: 35px;">0</td>
        </tr>'''
    return rows

def gen_poligonos():
    polys = ""
    btn_s = "cursor:pointer; border:none; background:rgba(0,0,0,0.08); color:#333; font-weight:bold; width:22px; height:22px; border-radius:4px; margin:0 2px;"
    
    fila_inner = f'''
    <tr class="calc-row">
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
        <td style="text-align: center; border: 0.5px solid #ccc;"><input type="checkbox" class="ok-check" style="transform: scale(1.3); cursor:pointer;"></td>
    </tr>'''
    
    for i in range(1, 11):
        polys += f'''
        <div class="poligono-bloque" style="margin-bottom: 20px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); border-radius: 8px; overflow: visible; background: white; border: 1px solid #ccc;">
            <table class="meli-table tabla-planes" style="width: 100%; border-collapse: collapse; table-layout: fixed;">
                <thead>
                    <tr style="background: linear-gradient(180deg, #888888 0%, #696969 100%); color: white; font-size: 11px; height: 35px;">
                        <th style="padding: 0 10px; width: 60px;">PLAN 1</th>
                        <th style="width: 60px;">VOL. TOTAL</th>
                        <th style="width: 90px;"># ASIGNADAS</th>
                        <th style="width: 90px;">SPR REAL</th>
                        <th style="width: 200px;">TIPO DE UNIDAD</th>
                        <th style="width: 35px;">OK</th>
                    </tr>
                </thead>
                <tbody>
                    <tr class="calc-row">
                        <td rowspan="5" style="background: #f0f0f0; font-weight:bold; text-align:center; border: 1px solid #ccc; width: 60px; color:#333;">PLAN {i}</td>
                        <td rowspan="5" contenteditable="true" class="v-total-val" oninput="recalc()" style="color: #20B2AA; font-weight: bold; font-size: 18px; text-align: center; border: 1px solid #ccc; width: 60px;">0</td>
                        <td class="u-manual-cell" style="background: #e3defa; text-align: center; border: 0.5px solid #ccc; width: 90px;">
                            <button style="{btn_s}" onclick="stepVal(this, -1, 'u')">-</button>
                            <span contenteditable="true" class="u-manual" oninput="manualEdit(this)" style="font-weight: bold; margin:0 5px;">0</span>
                            <button style="{btn_s}" onclick="stepVal(this, 1, 'u')">+</button>
                        </td>
                        <td class="spr-real-cell" style="background: #def3ed; text-align: center; border: 0.5px solid #ccc; width: 90px;">
                            <button style="{btn_s}" onclick="stepVal(this, -1, 's')">-</button>
                            <span contenteditable="true" class="spr-real-val" oninput="manualEdit(this)" style="font-weight: bold; margin:0 5px;">0</span>
                            <button style="{btn_s}" onclick="stepVal(this, 1, 's')">+</button>
                        </td>
                        <td style="border: 0.5px solid #ccc; padding: 2px; width: 200px; white-space: nowrap; overflow: visible;"><select class="s-type" onchange="resetRow(this)" style="width:100%; border:none; background:transparent; font-weight:bold; font-size:11px; color:#333;"><option>SELECCIONAR...</option></select></td>
                        <td style="text-align: center; border: 0.5px solid #ccc; width: 35px;"><input type="checkbox" class="ok-check" style="transform: scale(1.3); cursor:pointer;"></td>
                    </tr>
                    {fila_inner}{fila_inner}{fila_inner}{fila_inner}
                    <tr style="background:#f8f9fa; height: 30px;">
                        <td colspan="2" style="text-align:center; font-weight:bold; border: 1px solid #ccc; font-size: 11px; color:#333;">ESTADO:</td>
                        <td class="v-calculado-total" style="font-weight: bold; font-size: 16px; color: #d32f2f; border: 1px solid #ccc; text-align: center;">0</td>
                        <td class="p-diff" colspan="3" style="text-align: center; font-weight: bold; border: 1px solid #ccc; font-size: 11px;">VACÍO</td>
                    </tr>
                </tbody>
            </table>
        </div>'''
    return polys

# --- 3. ENSAMBLAJE DE LA INTERFAZ COMPLETA ---
# Aquí se insertará el código HTML/JS/CSS que definiremos en la Parte 2.
app_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<!-- <style>
    body {{ font-family: sans-serif; background: #f5f7f9; padding: 15px; width: 1300px; margin: auto; }}
    .p-tab-panel {{ display: flex; gap: 20px; }}
    .meli-table {{ border-collapse: collapse; width: 100%; table-layout: fixed; }}
    .meli-table td, .meli-table th {{ border: 1px solid #ccc; font-size: 11px; height: 26px; }}
    
    #google-alert {{ 
        position: fixed; top: -100px; left: 50%; transform: translateX(-50%);
        background: #d32f2f; color: white; padding: 15px 25px; border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3); transition: 0.4s; z-index: 10000;
    }}
    #google-alert.show {{ top: 20px; }}
    
    .tab-btn {{ padding: 8px 15px; cursor: pointer; border: none; background: #e0e0e0; border-radius: 4px 4px 0 0; font-weight: bold; margin-right: 2px; }}
    .tab-btn.active {{ background: #333; color: white; }}
    
    .activas-todas-btn {{ background: linear-gradient(180deg, #5ae0d9 0%, #20B2AA 100%); color: white; border: none; padding: 6px 12px; border-radius: 4px; cursor: pointer; font-weight: bold; font-size: 11px; box-shadow: 2px 2px 4px rgba(0,0,0,0.1); }}
    .activas-todas-btn:active {{ transform: translateY(1px); box-shadow: none; }}

    /* ESTILOS HERRAMIENTAS CORREGIDOS (IMAGEN 2) */
    .tools-panel {{ display: flex; flex-direction: column; gap: 15px; margin-top: 20px; }}
    .google-tool {{ background: #dfdff5; padding: 15px; border-radius: 12px; border: 1px solid #ccc; text-align: center; }}
    .google-tool-title {{ font-size: 11px; font-weight: bold; color: #4e3396; letter-spacing: 1px; display: flex; align-items: center; justify-content: center; gap: 5px; }}
    .google-input {{ border: 1px solid #ccc; border-radius: 5px; height: 30px; text-align: center; font-weight: bold; margin: 0 5px; width: 60px; }}
    .google-res {{ font-size: 20px; font-weight: bold; color: #ac40de; }}

    /* CALCULADORA AQUA CORREGIDA */
    #calc_wrapper {{ background: #22c5bc; border-radius: 20px; padding: 15px; border: 1px solid #1a1a1a; cursor: pointer; }}
    #calc_display_box {{ background: #fffacd; border-radius: 10px; padding: 10px; text-align: right; margin-bottom: 10px; }}
    .calc-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; }}
    .btn-c {{ background: white; border: none; font-weight: bold; border-radius: 8px; padding: 10px; cursor: pointer; box-shadow: 0 3px #ccc; }}
    .btn-c:active {{ background: #eee; transform: translateY(1px); }}
    .btn-c-eq {{ background: #FF00FF; color: white; border: none; border-radius: 8px; cursor: pointer; font-weight: bold; }}

    /* CRONÓMETRO */
    .crono-card {{ background: #1c1c1c; border-radius: 12px; padding: 15px; color: white; font-family: monospace; text-align: center; }}
</style> -->
</head>
<body>
<!-- <div id="google-alert">⚠️ <span id="alert-msg"></span> [ENTER para cerrar]</div>

<div class="p-tab-panel">
    <!-- COLUMNA IZQUIERDA -->
    <div style="width: 780px;">
        <div style="background: #696969; color: white; padding: 10px; border-radius: 8px; text-align: center; font-weight: bold; margin-bottom: 10px;">📋 PLANIFICACIÓN POR POLÍGONOS</div>
        <div id="polys-2" class="p-content">{gen_poligonos()}</div>
        <div id="polys-3" class="p-content" style="display:none;">{gen_poligonos()}</div>
        <div id="polys-1" class="p-content" style="display:none;">{gen_poligonos()}</div>
        <div id="polys-4" class="p-content" style="display:none;">{gen_poligonos()}</div>
    </div>

    <!-- COLUMNA DERECHA -->
    <div style="width: 470px; position: sticky; top: 10px; height: fit-content;">
        <div style="background: #000; color: white; padding: 10px; border-radius: 8px; font-weight: bold; text-align: center; margin-bottom: 10px;">🚚 DISPONIBILIDAD DE FLOTA</div>
        <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 0;">
            <div>
                <button class="tab-btn active" onclick="showTab(2, this)">C1</button>
                <button class="tab-btn" onclick="showTab(3, this)">C2</button>
                <button class="tab-btn" onclick="showTab(1, this)">SD</button>
                <button class="tab-btn" onclick="showTab(4, this)">SDE</button>
            </div>
            <!-- BOTONES RESTAURADOS -->
            <div style="display:flex; gap:5px; padding-bottom:5px;">
                <button onclick="filterFlota(true)" class="activas-todas-btn" style="background:#C0C0C0; color:#333;">ACTIVAS</button>
                <button onclick="filterFlota(false)" class="activas-todas-btn">TODAS</button>
            </div>
        </div>
        <div style="background: white; padding: 10px; border: 1px solid #ccc; border-radius: 0 0 6px 6px;">
            <div id="tab-2" class="t-content"><table class="meli-table"><thead style="background:#333; color:white;"><tr><th style="width:140px;">UNIDAD</th><th style="width:35px;">MIN</th><th style="width:35px;">MAX</th><th style="width:35px;">ORH</th><th style="width:35px;">SCH</th><th class="header-res" style="width:35px;">ME QUEDAN</th></tr></thead><tbody id="body-2">{gen_master_rows(u_C1, 2)}</tbody></table></div>
            <div id="tab-3" class="t-content" style="display:none;"><table class="meli-table"><thead style="background:#333; color:white;"><tr><th style="width:140px;">UNIDAD</th><th style="width:35px;">MIN</th><th style="width:35px;">MAX</th><th style="width:35px;">ORH</th><th style="width:35px;">SCH</th><th class="header-res" style="width:35px;">ME QUEDAN</th></tr></thead><tbody id="body-3">{gen_master_rows(u_C2, 3)}</tbody></table></div>
            <div id="tab-1" class="t-content" style="display:none;"><table class="meli-table"><thead style="background:#333; color:white;"><tr><th style="width:140px;">UNIDAD</th><th style="width:35px;">MIN</th><th style="width:35px;">MAX</th><th style="width:35px;">ORH</th><th style="width:35px;">SCH</th><th class="header-res" style="width:35px;">ME QUEDAN</th></tr></thead><tbody id="body-1">{gen_master_rows(u_SD, 1)}</tbody></table></div>
            <div id="tab-4" class="t-content" style="display:none;"><table class="meli-table"><thead style="background:#333; color:white;"><tr><th style="width:140px;">UNIDAD</th><th style="width:35px;">MIN</th><th style="width:35px;">MAX</th><th style="width:35px;">ORH</th><th style="width:35px;">SCH</th><th class="header-res" style="width:35px;">ME QUEDAN</th></tr></thead><tbody id="body-4">{gen_master_rows(u_SDE, 4)}</tbody></table></div>
        </div>

        <div class="tools-panel">
            <!-- HERRAMIENTAS IMAGEN 2 -->
            <div class="google-tool">
                <div class="google-tool-title">⏱️ CONVERTIDOR DE TIEMPO</div>
                <div style="display: flex; align-items: center; justify-content: center; margin-top: 5px;">
                    <input type="number" id="min-in" placeholder="Min" class="google-input" oninput="convertTime()">
                    <span id="time-res" class="google-res">0h 0m</span>
                </div>
            </div>

            <div id="calc_wrapper" tabindex="0">
                <div id="calc_display_box">
                    <div id="calc_h" style="font-size:10px; color:#666; height:15px;"></div>
                    <div id="calc_r" style="font-size:24px; font-weight:bold;">0</div>
                </div>
                <div class="calc-grid">
                    <button onclick="cl()" class="btn-c" style="grid-column: span 2;">AC</button>
                    <button onclick="del()" class="btn-c">⌫</button><button onclick="ao('/')" class="btn-c">÷</button>
                    <button onclick="an('7')" class="btn-c">7</button><button onclick="an('8')" class="btn-c">8</button><button onclick="an('9')" class="btn-c">9</button><button onclick="ao('*')" class="btn-c">×</button>
                    <button onclick="an('4')" class="btn-c">4</button><button onclick="an('5')" class="btn-c">5</button><button onclick="an('6')" class="btn-c">6</button><button onclick="ao('-')" class="btn-c">-</button>
                    <button onclick="an('1')" class="btn-c">1</button><button onclick="an('2')" class="btn-c">2</button><button onclick="an('3')" class="btn-c">3</button><button onclick="ao('+')" class="btn-c">+</button>
                    <button onclick="an('0')" class="btn-c" style="grid-column: span 2;">0</button><button onclick="calc_eq()" class="btn-c-eq">=</button>
                </div>
            </div>

            <div class="crono-card">
                <div style="font-size:10px; color:#888;">HORA ACTUAL: <span id="reloj-actual" style="color:#00e5ff;">00:00:00</span></div>
                <div id="crono-main" style="font-size:32px; font-weight:bold; margin:10px 0;">00:00:00.0</div>
                <div>
                    <button onclick="startC()" style="background:#28a745; color:white; border:none; padding:8px; border-radius:5px;">▶</button>
                    <button onclick="stopC()" style="background:#ffc107; border:none; padding:8px; border-radius:5px;">⏸</button>
                    <button onclick="resetC()" style="background:#dc3545; color:white; border:none; padding:8px; border-radius:5px;">🔄</button>
                </div>
            </div>
        </div>
    </div>
</div> -->
<!-- <script>
    let currentTab = 2;
    let editedRowsPlan = new Set();
    let alertShownSD = false;
    let curC = "";
    let chronoInterval;
    let startTime;
    let elapsedTime = 0;

    // LÓGICA DE HERRAMIENTAS Y CLIC ROSA
    document.getElementById('calc_wrapper').addEventListener('focus', function() {{
        this.style.outline = '4px solid #FF00FF';
        this.style.boxShadow = '0 0 15px #FF00FF';
    }});
    document.getElementById('calc_wrapper').addEventListener('blur', function() {{
        this.style.outline = 'none';
        this.style.boxShadow = '0 10px 20px rgba(0,0,0,0.15)';
    }});

    function showTab(n, btn) {{
        currentTab = n;
        document.querySelectorAll('.p-content, .t-content').forEach(el => el.style.display = 'none');
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.getElementById('polys-'+n).style.display = 'block';
        document.getElementById('tab-'+n).style.display = 'block';
        btn.classList.add('active');
        recalc();
    }}

    // FILTRO ACTIVAS/TODAS RESTAURADO
    function filterFlota(hide) {{
        document.querySelectorAll('#body-' + currentTab + ' tr').forEach(row => {{
            let sch = parseInt(row.querySelector('.f-stock').innerText) || 0;
            if (hide) {{
                row.style.display = (sch > 0) ? '' : 'none';
            }} else {{
                row.style.display = '';
            }}
        }});
    }}

    function showAlert(msg) {{
        document.getElementById('alert-msg').innerText = msg;
        document.getElementById('google-alert').classList.add('show');
    }}
    function hideAlert() {{ document.getElementById('google-alert').classList.remove('show'); }}

    function stepVal(btn, delta, type) {{
        let row = btn.closest('tr');
        let sel = row.querySelector('.s-type').value;
        if(sel === "SELECCIONAR...") return;

        let fRow = Array.from(document.querySelectorAll('#body-'+currentTab+' tr')).find(r => r.querySelector('.edit-name').innerText.trim() === sel);
        let left = parseInt(fRow.querySelector('.f-left').innerText) || 0;
        let sch = parseInt(fRow.querySelector('.f-stock').innerText) || 0;
        let ma_spr = parseFloat(fRow.querySelector('.edit-spr-max').innerText) || 0;

        if(type === 'u') {{
            let span = row.querySelector('.u-manual');
            let val = parseInt(span.innerText) || 0;
            if (delta > 0 && left <= 0 && sch > 0) {{
                if (currentTab === 4) {{ showAlert("⚠️ EXCESO EN SDE PERMITIDO."); }}
                else {{ showAlert("⚠️ AGOTADO. No se puede aumentar."); return; }}
            }}
            span.innerText = Math.max(0, val + delta);
        }} else {{
            let span = row.querySelector('.spr-real-val');
            let val = parseFloat(span.innerText) || 0;
            // TOPE SPR REAL RESTAURADO
            if (delta > 0 && val >= ma_spr) {{ showAlert("⚠️ TOPE DE SPR ALCANZADO para esta unidad."); return; }}
            span.innerText = Math.max(0, val + delta);
        }}
        editedRowsPlan.add(row);
        recalc();
    }}

    function recalc() {{
        let fleet = {{}};
        let hasOverGlobal = false;

        document.querySelectorAll('#body-' + currentTab + ' tr').forEach(row => {{
            let n = row.querySelector('.edit-name').innerText.trim();
            let sch = parseInt(row.querySelector('.f-stock').innerText) || 0;
            let mi = row.querySelector('.edit-spr-min'), ma = row.querySelector('.edit-spr-max'), fs = row.querySelector('.f-stock'), nC = row.querySelector('.edit-name');
            
            // Lógica de Sombreado Dinámico: Ahora SCH y SPR Max se sombrean
            if(sch > 0) {{
                nC.style.background = "white"; nC.style.color="black";
                fs.style.background = "#e3defa"; mi.style.background = "#def3ed"; ma.style.background = "#def3ed";
            }} else {{
                nC.style.background = "#ebebeb"; nC.style.color="#969696";
                fs.style.background = "#ebebeb"; mi.style.background = "#ebebeb"; ma.style.background = "#ebebeb";
            }}
            if(n !== "" && n !== "NUEVA UNIDAD") fleet[n] = {{ max: parseFloat(ma.innerText)||0, stock: sch, used: 0 }};
        }});

        document.querySelectorAll('#polys-' + currentTab + ' .poligono-bloque').forEach(bl => {{
            let vT = parseFloat(bl.querySelector('.v-total-val').innerText) || 0, vA = 0;
            bl.querySelectorAll('.calc-row').forEach(r => {{
                let s = r.querySelector('.s-type').value, u = parseInt(r.querySelector('.u-manual').innerText) || 0, sp = r.querySelector('.spr-real-val');
                if(s !== "SELECCIONAR..." && fleet[s]) {{
                    if(!editedRowsPlan.has(r)) sp.innerText = fleet[s].max;
                    fleet[s].used += u; vA += (u * parseFloat(sp.innerText));
                }}
            }});
            bl.querySelector('.v-calculado-total').innerText = Math.round(vA);
            let d = bl.querySelector('.p-diff');
            if(vT===0) {{ d.innerText="VACÍO"; d.style.background="none"; }}
            else {{
                d.innerText = (vA >= vT) ? (vA===vT ? "OK" : "EXCESO: "+Math.round(vA-vT)) : "FALTAN: "+Math.round(vT-vA);
                d.style.background = (vA >= vT) ? (vA===vT ? "#ceedd6":"#ffe4b5") : "#f7cdd1";
            }}
        }});

        document.querySelectorAll('#body-' + currentTab + ' tr').forEach(row => {{
            let n = row.querySelector('.edit-name').innerText.trim();
            if(fleet[n]) {{
                let sch = fleet[n].stock, res = sch - fleet[n].used, cL = row.querySelector('.f-left');
                cL.innerText = res;
                
                // ME QUEDAN / ME PASÉ Y ROJO
                if (res === 0 && sch > 0) {{
                    cL.style.background = "#d32f2f"; cL.style.color = "white"; // Rojo brillante
                }} else if (res < 0) {{
                    cL.style.background = "white"; cL.style.color = "red";
                    hasOverGlobal = true;
                }} else {{
                    cL.style.background = "transparent"; cL.style.color = "black";
                }}
            }}
        }});

        let header = document.querySelector('#tab-' + currentTab + ' .header-res');
        if(header) header.innerText = (currentTab === 4 && hasOverGlobal) ? "ME PASÉ POR" : "ME QUEDAN";

        // Actualizar Selects
        document.querySelectorAll('#polys-' + currentTab + ' .s-type').forEach(s => {{
            let cur = s.value, opt = '<option>SELECCIONAR...</option>';
            Object.keys(fleet).sort().forEach(k => {{ if(fleet[k].stock > 0 || k === cur) opt += `<option value="${{k}}">${{k}}</option>`; }});
            s.innerHTML = opt; s.value = cur;
        }});
    }}

    // HERRAMIENTAS JS CORREGIDAS
    function convertTime() {{
        let m = parseInt(document.getElementById('min-in').value) || 0;
        document.getElementById('time-res').innerText = Math.floor(m/60) + "h " + (m%60) + "m";
    }}
    function an(n) {{ curC += n; updateCalc(); }}
    function ao(o) {{ curC += " " + o + " "; updateCalc(); }}
    function cl() {{ curC = ""; updateCalc(); document.getElementById('calc_h').innerText = ""; }}
    function del() {{ curC = curC.trim().slice(0, -1); updateCalc(); }}
    function updateCalc() {{ document.getElementById('calc_r').innerText = curC || "0"; }}
    function calc_eq() {{ try {{ let res = eval(curC); document.getElementById('calc_h').innerText = curC + " ="; curC = res.toString(); updateCalc(); }} catch {{ }} }}
    function updateReloj() {{ document.getElementById('reloj-actual').innerText = new Date().toLocaleTimeString('en-GB'); }}
    setInterval(updateReloj, 1000);
    function startC() {{ if(!chronoInterval) {{ startTime = Date.now() - elapsedTime; chronoInterval = setInterval(()=>{{ elapsedTime = Date.now() - startTime; updateCDisplay(); }}, 100); }} }}
    function stopC() {{ clearInterval(chronoInterval); chronoInterval = null; }}
    function resetC() {{ stopC(); elapsedTime = 0; updateCDisplay(); }}
    function updateCDisplay() {{ 
        let d = new Date(elapsedTime), h = String(Math.floor(elapsedTime/3600000)).padStart(2,'0'), m = String(d.getUTCMinutes()).padStart(2,'0'), s = String(d.getUTCSeconds()).padStart(2,'0'), ms = Math.floor(d.getUTCMilliseconds()/100);
        document.getElementById('crono-main').innerText = `${{h}}:${{m}}:${{s}}.${{ms}}`;
    }}

    // CERRAR ALERTA SOLO CON ENTER
    document.addEventListener('keydown', (e) => {{
        if(e.key === 'Enter' && document.getElementById('google-alert').classList.contains('show')) {{
            hideAlert();
            e.preventDefault();
        }}
    }});
    function manualEdit(el) {{ editedRowsPlan.add(el.closest('tr')); recalc(); }}
    function resetRow(sel) {{ let r=sel.closest('tr'); r.querySelector('.u-manual').innerText="0"; r.querySelector('.spr-real-val').innerText="0"; editedRowsPlan.delete(r); recalc(); }}
    recalc();
</script> -->
</body>
</html>
"""

# Renderizado final
# Se fija el ancho del HTML para evitar colapsos
html(app_html, width=1350, height=1500, scrolling=True)
