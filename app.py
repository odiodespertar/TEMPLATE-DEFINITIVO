import streamlit as st
from streamlit.components.v1 import html

# Configuración de página
st.set_page_config(page_title="Monitor Logístico - Liliana García", layout="wide")

# CSS para ocultar elementos de Streamlit
st.markdown("""
    <style>
    .block-container {padding: 0rem !important;}
    footer, #MainMenu, header {visibility: hidden;}
    body { background-color: #f5f7f9; }
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

# --- 2. GENERADORES DE HTML ---
def gen_master_rows(data_dict, table_id):
    rows = ""
    items = list(data_dict.items())
    for i in range(15):
        is_real = i < len(items)
        name, spr = (items[i][0], items[i][1]) if is_real else ("NUEVA UNIDAD", [0, 0])
        st_base = "background: #ebebeb; color: #969696;" if is_real else "background: #fcfcfc; color: #C0C0C0;"
        rows += f'''
        <tr data-table="{table_id}" class="master-row" style="{st_base}">
            <td contenteditable="true" class="edit-name" oninput="recalc()" style="font-weight: bold; text-align: left; padding-left: 10px; border: 0.5px solid #ccc; width: 150px;">{name}</td>
            <td contenteditable="true" class="edit-spr-min" oninput="recalc()" style="text-align: center; border: 0.5px solid #ccc; width: 45px;">{spr[0]}</td>
            <td contenteditable="true" class="edit-spr-max" oninput="recalc()" style="text-align: center; border: 0.5px solid #ccc; width: 45px;">{spr[1]}</td>
            <td contenteditable="true" class="edit-orh" style="text-align: center; border: 0.5px solid #ccc; width: 45px;">480</td>
            <td contenteditable="true" class="f-stock" oninput="recalc()" style="text-align: center; border: 0.5px solid #ccc; width: 55px;">0</td>
            <td class="f-left" style="font-weight: bold; text-align: center; border: 0.5px solid #ccc; width: 60px;">0</td>
        </tr>'''
    return rows

def gen_poligonos():
    polys = ""
    btn_s = "cursor:pointer; border:none; background:rgba(0,0,0,0.08); color:#333; font-weight:bold; width:22px; height:22px; border-radius:4px;"
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
        <td style="border: 0.5px solid #ccc; padding: 2px;"><select class="s-type" onchange="resetRow(this)" style="width:100%; border:none; background:transparent; font-weight:bold; font-size:11px;"><option>SELECCIONAR...</option></select></td>
        <td style="text-align: center; border: 0.5px solid #ccc;"><input type="checkbox" class="ok-check" style="transform: scale(1.3);"></td>
    </tr>'''
    
    for i in range(1, 11):
        polys += f'''
        <div class="poligono-bloque" style="margin-bottom: 20px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); border-radius: 8px; overflow: hidden; background: white; border: 1px solid #ccc;">
            <table style="width: 100%; border-collapse: collapse; table-layout: fixed;">
                <thead>
                    <tr style="background: #696969; color: white; font-size: 12px;">
                        <th style="width: 80px; padding: 8px;">PLAN {i}</th><th style="width: 80px;">VOL. TOTAL</th>
                        <th style="width: 100px;"># ASIGNADAS</th><th style="width: 100px;">SPR REAL</th>
                        <th>TIPO UNIDAD</th><th style="width: 40px;">OK</th>
                    </tr>
                </thead>
                <tbody>
                    <tr class="calc-row">
                        <td rowspan="5" style="background: #f0f0f0; font-weight:bold; text-align:center; border: 1px solid #ccc;">PLAN {i}</td>
                        <td rowspan="5" contenteditable="true" class="v-total-val" oninput="recalc()" style="color: #20B2AA; font-weight: bold; font-size: 18px; text-align: center; border: 1px solid #ccc;">0</td>
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
                        <td style="border: 0.5px solid #ccc; padding: 2px;"><select class="s-type" onchange="resetRow(this)" style="width:100%; border:none; background:transparent; font-weight:bold; font-size:11px;"><option>SELECCIONAR...</option></select></td>
                        <td style="text-align: center; border: 0.5px solid #ccc;"><input type="checkbox" class="ok-check" style="transform: scale(1.3);"></td>
                    </tr>
                    {fila_inner}{fila_inner}{fila_inner}{fila_inner}
                    <tr style="background:#f8f9fa;">
                        <td colspan="2" style="text-align:center; font-weight:bold; border: 1px solid #ccc; font-size: 11px;">ESTADO:</td>
                        <td class="v-calculado-total" style="font-weight: bold; font-size: 16px; color: #d32f2f; border: 1px solid #ccc; text-align: center;">0</td>
                        <td class="p-diff" colspan="3" style="text-align: center; font-weight: bold; border: 1px solid #ccc; font-size: 11px;">VACÍO</td>
                    </tr>
                </tbody>
            </table>
        </div>'''
    return polys

# --- 3. ENSAMBLAJE FINAL ---
app_html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: sans-serif; background: #f5f7f9; padding: 15px; }}
        .meli-table {{ border-collapse: collapse; width: 100%; }}
        .meli-table th, .meli-table td {{ border: 1px solid #ccc; font-size: 12px; }}
        #google-alert {{ 
            position: fixed; top: -100px; left: 50%; transform: translateX(-50%);
            background: #d32f2f; color: white; padding: 15px 25px; border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3); transition: 0.4s; z-index: 10000;
        }}
        #google-alert.show {{ top: 20px; }}
        .tab-btn {{ padding: 8px 15px; cursor: pointer; border: none; background: #e0e0e0; border-radius: 4px 4px 0 0; font-weight: bold; margin-right: 2px; }}
        .tab-btn.active {{ background: #333; color: white; }}
    </style>
</head>
<body>

<div id="google-alert">⚠️ <span id="alert-msg"></span> [ENTER para cerrar]</div>

<div style="display: flex; gap: 20px; max-width: 1400px; margin: auto;">
    <div style="flex: 1;">
        <div style="background: #696969; color: white; padding: 10px; border-radius: 6px; text-align: center; font-weight: bold; margin-bottom: 10px;">📋 PLANES</div>
        <div id="polys-2" class="p-content">{gen_poligonos()}</div>
        <div id="polys-3" class="p-content" style="display:none;">{gen_poligonos()}</div>
        <div id="polys-1" class="p-content" style="display:none;">{gen_poligonos()}</div>
        <div id="polys-4" class="p-content" style="display:none;">{gen_poligonos()}</div>
    </div>

    <div style="width: 450px; position: sticky; top: 10px; height: fit-content;">
        <div style="background: #000; color: white; padding: 10px; border-radius: 6px; font-weight: bold; margin-bottom: 10px; text-align: center;">🚚 FLOTA</div>
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <button class="tab-btn active" onclick="showTab(2, this)">C1</button>
                <button class="tab-btn" onclick="showTab(3, this)">C2</button>
                <button class="tab-btn" onclick="showTab(1, this)">SD</button>
                <button class="tab-btn" onclick="showTab(4, this)">SDE</button>
            </div>
            <button onclick="recalc()" style="background: #20B2AA; color: white; border: none; padding: 5px 10px; border-radius: 4px; cursor: pointer;">Actualizar</button>
        </div>
        <div style="background: white; padding: 10px; border: 1px solid #ccc; border-radius: 0 0 6px 6px;">
            <div id="tab-2" class="t-content"><table class="meli-table"><thead><tr style="background:#333; color:white;"><th>UNIDAD (C1)</th><th>MIN</th><th>MAX</th><th>ORH</th><th>SCHED</th><th>REST</th></tr></thead><tbody id="body-2">{gen_master_rows(u_C1, 2)}</tbody></table></div>
            <div id="tab-3" class="t-content" style="display:none;"><table class="meli-table"><thead><tr style="background:#333; color:white;"><th>UNIDAD (C2)</th><th>MIN</th><th>MAX</th><th>ORH</th><th>SCHED</th><th>REST</th></tr></thead><tbody id="body-3">{gen_master_rows(u_C2, 3)}</tbody></table></div>
            <div id="tab-1" class="t-content" style="display:none;"><table class="meli-table"><thead><tr style="background:#333; color:white;"><th>UNIDAD (SD)</th><th>MIN</th><th>MAX</th><th>ORH</th><th>SCHED</th><th>REST</th></tr></thead><tbody id="body-1">{gen_master_rows(u_SD, 1)}</tbody></table></div>
            <div id="tab-4" class="t-content" style="display:none;"><table class="meli-table"><thead><tr style="background:#333; color:white;"><th>UNIDAD (SDE)</th><th>MIN</th><th>MAX</th><th>ORH</th><th>SCHED</th><th>REST</th></tr></thead><tbody id="body-4">{gen_master_rows(u_SDE, 4)}</tbody></table></div>
        </div>
    </div>
</div>

<script>
    let currentTab = 2;
    let alertShownSDE = false;
    let editedRowsPlan = new Set();

    function showTab(n, btn) {{
        currentTab = n;
        document.querySelectorAll('.p-content, .t-content').forEach(el => el.style.display = 'none');
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.getElementById('polys-'+n).style.display = 'block';
        document.getElementById('tab-'+n).style.display = 'block';
        btn.classList.add('active');
        recalc();
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

        let span = (type === 'u') ? row.querySelector('.u-manual') : row.querySelector('.spr-real-val');
        let val = parseFloat(span.innerText) || 0;
        
        if (delta > 0 && type === 'u') {{
            let fRow = Array.from(document.querySelectorAll('#body-'+currentTab+' tr')).find(r => r.querySelector('.edit-name').innerText.trim() === sel);
            let left = parseInt(fRow.querySelector('.f-left').innerText) || 0;
            if (left <= 0) {{
                if (currentTab === 4) {{ if(!alertShownSDE) {{ showAlert("EXCESO EN SDE PERMITIDO"); alertShownSDE=true; }} }}
                else {{ showAlert("AGOTADO. BLOQUEO DE ASIGNACIÓN"); return; }}
            }}
        }}
        span.innerText = Math.max(0, val + delta);
        editedRowsPlan.add(row);
        recalc();
    }}

    function recalc() {{
        let fleet = {{}};
        document.querySelectorAll('#body-' + currentTab + ' tr').forEach(row => {{
            let n = row.querySelector('.edit-name').innerText.trim();
            let s = parseInt(row.querySelector('.f-stock').innerText) || 0;
            let ma = parseFloat(row.querySelector('.edit-spr-max').innerText) || 0;
            let mi = row.querySelector('.edit-spr-min'), sch = row.querySelector('.f-stock'), nameC = row.querySelector('.edit-name');
            
            if(n !== "" && n !== "NUEVA UNIDAD") {{
                if(s > 0) {{
                    nameC.style.background = "white"; nameC.style.color="black";
                    sch.style.background = "#e3defa"; mi.style.background = "#def3ed";
                }} else {{
                    nameC.style.background = "#ebebeb"; nameC.style.color="#969696";
                    sch.style.background = "#ebebeb"; mi.style.background = "#ebebeb";
                }}
                fleet[n] = {{ max: ma, stock: s, used: 0 }};
            }}
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
                d.innerText = (vA >= vT) ? (vA === vT ? "OK" : "EXCESO: "+Math.round(vA-vT)) : "FALTAN: "+Math.round(vT-vA);
                d.style.background = (vA >= vT) ? (vA===vT ? "#ceedd6":"#ffe4b5") : "#f7cdd1";
            }}
        }});

        document.querySelectorAll('#body-' + currentTab + ' tr').forEach(row => {{
            let n = row.querySelector('.edit-name').innerText.trim();
            if(fleet[n]) {{
                let res = fleet[n].stock - fleet[n].used, cL = row.querySelector('.f-left');
                cL.innerText = res; cL.style.background = (res < 0) ? "#f25a5a" : "white";
                cL.style.color = (res < 0) ? "white" : "green";
            }}
        }});

        document.querySelectorAll('#polys-' + currentTab + ' .s-type').forEach(s => {{
            let cur = s.value, opt = '<option>SELECCIONAR...</option>';
            Object.keys(fleet).forEach(k => {{ if(fleet[k].stock > 0 || k === cur) opt += `<option value="${{k}}">${{k}}</option>`; }});
            s.innerHTML = opt; s.value = cur;
        }});
    }}

    document.addEventListener('keydown', (e) => {{ if(e.key === 'Enter') hideAlert(); }});
    function manualEdit(el) {{ editedRowsPlan.add(el.closest('tr')); recalc(); }}
    function resetRow(sel) {{ let r=sel.closest('tr'); r.querySelector('.u-manual').innerText="0"; r.querySelector('.spr-real-val').innerText="0"; editedRowsPlan.delete(r); recalc(); }}
    recalc();
</script>
</body>
</html>
"""

html(app_html, height=1200, scrolling=True)
