import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="Tracker Logística - Versión Restaurada")

# 1. Diccionarios originales de Liliana
unidades_data = {
    "C1": {"RENTAL ELEC LARGE VAN": [120, 120], "RENTAL ELEC SMALL VAN": [120, 120], "RENTAL LARGE VAN": [120, 120], "RENTAL SMALL VAN": [120, 120], "LARGE VAN VAR(MLP)": [100, 100], "SMALL VAN VAR(MLP)": [80, 80], "CAR MLP": [50, 50], "MOTO 3 HRS": [28, 28], "CROWD NEWBIE 3 hrs": [30, 30], "CROWD EXTRA 8 HRS": [80, 85], "CROWD 5 HRS": [60, 60]},
    "C2": {"RENTAL ELEC LARGE VAN": [120, 120], "RENTAL ELEC SMALL VAN": [120, 120], "RENTAL LARGE VAN": [120, 120], "RENTAL SMALL VAN": [120, 120], "LARGE VAN HÍBRIDA": [100, 100], "LARGE VAN VAR(MLP)": [100, 100], "SMALL VAN VAR(MLP)": [80, 80], "CAR MLP": [50, 50], "MOTO 3 HRS": [28, 28], "CROWD NEWBIE 3 hrs": [30, 30], "CROWD EXTRA 8 HRS": [80, 85], "CROWD 5 HRS": [60, 60]},
    "SD": {"MOTO 3 HRS": [25, 25], "MOTO NEWBIE": [20, 22], "CROWD 5 HRS / SMALL VAN": [35, 37]},
    "SDE": {"CROWD 5 HRS": [25, 28], "CROWD 5 HRS EXTENDIDA": [25, 28], "CROWD 3 HRS": [25, 28], "MOTO 3 HRS": [25, 28]}
}

def gen_master_rows(data, tid):
    h = ""
    items = list(data.items())
    for i in range(15):
        name, spr = items[i] if i < len(items) else ("NUEVA UNIDAD", [0,0])
        h += f'''<tr data-table="{tid}">
            <td contenteditable="true" class="edit-name">{name}</td>
            <td contenteditable="true" class="edit-spr-min">{spr[0]}</td>
            <td contenteditable="true" class="edit-spr-max">{spr[1]}</td>
            <td contenteditable="true" class="edit-orh">480</td>
            <td contenteditable="true" class="f-stock" oninput="recalc()">0</td>
            <td class="f-left">0</td></tr>'''
    return h

def gen_polygons():
    h = ""
    for i in range(1, 11):
        rows = "".join([f'''<tr class="calc-row">
            <td class="u-manual-cell"><button onclick="stepVal(this,-1,'u')">-</button><span contenteditable="true" class="u-manual" oninput="manualEdit(this)">0</span><button onclick="stepVal(this,1,'u')">+</button></td>
            <td class="spr-real-cell"><button onclick="stepVal(this,-1,'s')">-</button><span contenteditable="true" class="spr-real-val" oninput="manualEdit(this)">0</span><button onclick="stepVal(this,1,'s')">+</button></td>
            <td><select class="s-type" onchange="resetRow(this)"><option>SELECCIONAR...</option></select></td>
            <td><input type="checkbox"></td></tr>''' for _ in range(5)])
        h += f'''<div class="poligono-bloque">
            <table><thead><tr><th>PLAN {i}</th><th>VOL. TOTAL</th><th># ASIGNADAS</th><th>SPR REAL</th><th>TIPO</th><th>OK</th></tr></thead>
            <tbody><tr><td rowspan="5">PLAN {i}</td><td rowspan="5" contenteditable="true" class="v-total-val" oninput="recalc()">0</td>{rows[rows.find('</td>')+5:]}
            <tr><td colspan="2">ESTADO:</td><td class="v-calculado-total">0</td><td class="p-diff" colspan="3">VACÍO</td></tr></tbody></table></div>'''
    return h

# 2. HTML y CSS con el diseño original (sin restricciones de zoom agresivas)
layout = f"""
<style>
    body {{ font-family: sans-serif; background: #f0f2f5; }}
    .flex-main {{ display: flex; gap: 10px; width: 100%; }}
    .left {{ flex: 2; }}
    .right {{ flex: 1; position: sticky; top: 0; height: 100vh; overflow-y: auto; }}
    table {{ width: 100%; border-collapse: collapse; font-size: 12px; background: white; margin-bottom: 10px; }}
    th {{ background: #333; color: white; padding: 5px; border: 1px solid #444; }}
    td {{ border: 1px solid #ccc; padding: 4px; text-align: center; }}
    .tab-btn {{ padding: 5px 10px; cursor: pointer; border: none; background: #ddd; }}
    .tab-btn.active {{ background: #000; color: white; }}
    .u-manual, .spr-real-val {{ font-weight: bold; min-width: 20px; display: inline-block; }}
    
    /* Calculadora Aqua Original */
    #calc_container {{ background: linear-gradient(145deg, #22c5bc, #1da29b) !important; border-radius: 20px; padding: 15px; border: 1px solid #178f88; box-shadow: 8px 8px 16px #acacac; }}
    .btn-calc {{ background: #b2aaaa; border: 1px solid #ccc; border-radius: 8px; padding: 8px; cursor: pointer; width: 100%; }}
    
    /* Cronómetro / Convertidor */
    .cron-box {{ background: #e3defa; padding: 10px; border-radius: 10px; margin-top: 10px; text-align: center; }}
</style>

<div class="flex-main">
    <div class="left">
        <div id="polys-2">{gen_polygons()}</div>
        <div id="polys-3" style="display:none;">{gen_polygons()}</div>
        <div id="polys-1" style="display:none;">{gen_polygons()}</div>
        <div id="polys-4" style="display:none;">{gen_polygons()}</div>
    </div>
    <div class="right">
        <div style="background:#000; color:white; padding:10px; font-weight:bold;">🚚 DISPONIBILIDAD DE FLOTA</div>
        <div style="margin: 5px 0;">
            <button class="tab-btn active" onclick="showTab(2, this)">C1</button>
            <button class="tab-btn" onclick="showTab(3, this)">C2</button>
            <button class="tab-btn" onclick="showTab(1, this)">SD</button>
            <button class="tab-btn" onclick="showTab(4, this)">SDE</button>
            <button onclick="filterFlota(true)" style="background:#ccc;">ACTIVAS</button>
            <button onclick="filterFlota(false)" style="background:#20B2AA; color:white;">TODAS</button>
        </div>
        
        <div id="tab-flota-2" class="tab-content"><table><thead><tr><th>UNIDADES (C1)</th><th>min</th><th>max</th><th>ORH</th><th>SCHED</th><th>ME QUEDAN</th></tr></thead><tbody id="body-2">{gen_master_rows(unidades_data["C1"], 2)}</tbody></table></div>
        <div id="tab-flota-3" class="tab-content" style="display:none;"><table><thead><tr><th>UNIDADES (C2)</th><th>min</th><th>max</th><th>ORH</th><th>SCHED</th><th>ME QUEDAN</th></tr></thead><tbody id="body-3">{gen_master_rows(unidades_data["C2"], 3)}</tbody></table></div>
        <div id="tab-flota-1" class="tab-content" style="display:none;"><table><thead><tr><th>UNIDADES (SD)</th><th>min</th><th>max</th><th>ORH</th><th>SCHED</th><th>ME QUEDAN</th></tr></thead><tbody id="body-1">{gen_master_rows(unidades_data["SD"], 1)}</tbody></table></div>
        <div id="tab-flota-4" class="tab-content" style="display:none;"><table><thead><tr><th>UNIDADES (SDE)</th><th>min</th><th>max</th><th>ORH</th><th>SCHED</th><th>ME QUEDAN</th></tr></thead><tbody id="body-4">{gen_master_rows(unidades_data["SDE"], 4)}</tbody></table></div>

        <div class="cron-box">
             <div style="font-size:11px; font-weight:bold;">CONVERTIDOR DE TIEMPO</div>
             <input type="number" id="minInp" oninput="convertirMinutos()" style="width:60px;"> min = <span id="resConv" style="font-weight:bold;">0h 0m</span>
        </div>

        <div id="calc_container" tabindex="0">
            <div style="background: #fffacd; padding: 5px; text-align: right; margin-bottom: 10px;">
                <div id="h_calc" style="font-size:10px;">0</div><div id="r_calc" style="font-size: 20px; font-weight: bold;">0</div>
            </div>
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 5px;">
                <button onclick="cl()" class="btn-calc" style="grid-column: span 2;">AC</button><button onclick="del()" class="btn-calc">⌫</button><button onclick="ao('/')" class="btn-calc">÷</button>
                <button onclick="an('7')" class="btn-calc">7</button><button onclick="an('8')" class="btn-calc">8</button><button onclick="an('9')" class="btn-calc">9</button><button onclick="ao('*')" class="btn-calc">×</button>
                <button onclick="an('4')" class="btn-calc">4</button><button onclick="an('5')" class="btn-calc">5</button><button onclick="an('6')" class="btn-calc">6</button><button onclick="ao('-')" class="btn-calc">-</button>
                <button onclick="an('1')" class="btn-calc">1</button><button onclick="an('2')" class="btn-calc">2</button><button onclick="an('3')" class="btn-calc">3</button><button onclick="ao('+')" class="btn-calc">+</button>
                <button onclick="an('0')" class="btn-calc" style="grid-column: span 2;">0</button><button onclick="calc_eq()" class="btn-calc" style="background:#FF00FF; color:white;">=</button>
            </div>
        </div>
    </div>
</div>
"""

# 3. Script original de Liliana con validaciones de bloqueo y sincronización
script = """
<script>
    var currentTab = 2;
    var editedRows = new Set();

    function showTab(n, btn) {
        currentTab = n;
        document.querySelectorAll('.tab-content, .poly-tab-content').forEach(el => el.style.display = 'none');
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.getElementById('tab-flota-'+n).style.display = 'block';
        document.getElementById('polys-'+n).style.display = 'block';
        btn.classList.add('active');
        recalc();
    }

    function filterFlota(hide) {
        document.querySelectorAll('#body-' + currentTab + ' tr').forEach(row => {
            let stock = parseInt(row.querySelector('.f-stock').innerText) || 0;
            row.style.display = (hide && stock === 0) ? 'none' : '';
        });
    }

    function resetRow(selectEl) {
        let row = selectEl.closest('tr');
        row.querySelector('.u-manual').innerText = "0";
        row.querySelector('.spr-real-val').innerText = "0";
        editedRows.delete(row);
        recalc();
    }

    function manualEdit(el) { editedRows.add(el.closest('tr')); recalc(); }

    function stepVal(btn, delta, type) {
        let row = btn.closest('tr');
        let select = row.querySelector('.s-type');
        let typeSelected = select ? select.value : "";
        let span = (type === 'u') ? row.querySelector('.u-manual') : row.querySelector('.spr-real-val');
        let val = parseInt(span.innerText) || 0;

        if (typeSelected === "SELECCIONAR...") return;

        // Validaciones de Liliana (Bloqueos y Topes)
        let fleetRows = document.querySelectorAll('#body-' + currentTab + ' tr');
        let fData = null;
        for (let r of fleetRows) {
            if (r.querySelector('.edit-name').innerText.trim() === typeSelected) {
                fData = {
                    max: parseFloat(r.querySelector('.edit-spr-max').innerText) || 0,
                    left: parseInt(r.querySelector('.f-left').innerText) || 0
                };
                break;
            }
        }

        if (type === 's' && delta > 0 && (val + delta) > fData.max) {
            alert("⚠️ LÍMITE ALCANZADO: El SPR máximo para " + typeSelected + " es " + fData.max);
            return;
        }
        if (type === 'u' && delta > 0 && fData.left <= 0 && currentTab !== 4) {
            alert("🚫 BLOQUEO: No hay unidades disponibles.");
            return;
        }

        span.innerText = Math.max(0, val + delta);
        editedRows.add(row);
        recalc();
    }

    function recalc() {
        let fleet = {};
        document.querySelectorAll('#body-' + currentTab + ' tr').forEach(row => {
            let name = row.querySelector('.edit-name').innerText.trim();
            let stock = parseInt(row.querySelector('.f-stock').innerText) || 0;
            let min = parseFloat(row.querySelector('.edit-spr-min').innerText) || 0;
            let max = parseFloat(row.querySelector('.edit-spr-max').innerText) || 0;
            
            // Estilo de Activación de Liliana
            let cells = [row.querySelector('.edit-name'), row.querySelector('.f-stock'), row.querySelector('.edit-spr-min'), row.querySelector('.edit-spr-max'), row.querySelector('.f-left')];
            if (stock > 0) {
                cells.forEach(c => { c.style.background = "#def4ed"; c.style.color = "#000"; });
            } else {
                cells.forEach(c => { c.style.background = "#ebebeb"; c.style.color = "#969696"; });
            }

            fleet[name] = { min, max, stock, used: 0 };
        });

        document.querySelectorAll('#polys-' + currentTab + ' .poligono-bloque').forEach(bl => {
            let volTotal = parseFloat(bl.querySelector('.v-total-val').innerText) || 0;
            let sum = 0;

            bl.querySelectorAll('.calc-row').forEach(row => {
                let type = row.querySelector('.s-type').value;
                let spanU = row.querySelector('.u-manual'), spanS = row.querySelector('.spr-real-val');

                if (type !== "SELECCIONAR..." && fleet[type]) {
                    if (!editedRows.has(row)) { spanS.innerText = fleet[type].max; }
                    let u = parseInt(spanU.innerText) || 0;
                    let s = parseInt(spanS.innerText) || 0;
                    fleet[type].used += u;
                    sum += (u * s);
                }
            });

            let res = bl.querySelector('.v-calculado-total');
            res.innerText = Math.round(sum);
            res.style.color = (Math.round(sum) === volTotal && volTotal > 0) ? "#20B2AA" : "#d32f2f";
        });

        // Actualizar Me Quedan y Alertas
        document.querySelectorAll('#body-' + currentTab + ' tr').forEach(row => {
            let n = row.querySelector('.edit-name').innerText.trim();
            if(fleet[n]) {
                let rest = fleet[n].stock - fleet[n].used;
                let c = row.querySelector('.f-left');
                c.innerText = rest;
                c.style.color = rest < 0 ? "red" : (rest === 0 ? "orange" : "green");
            }
        });

        // Actualizar Selects
        document.querySelectorAll('#polys-' + currentTab + ' .s-type').forEach(s => {
            let cur = s.value;
            let h = '<option>SELECCIONAR...</option>';
            Object.keys(fleet).forEach(name => { h += `<option value="${name}">${name}</option>`; });
            s.innerHTML = h; s.value = cur;
        });
    }

    // Calculadora Aqua
    var cur = ""; const rD = document.getElementById('r_calc'), hD = document.getElementById('h_calc');
    function an(n) { cur += n; rD.innerText = cur; }
    function ao(o) { if(cur!=="") { cur += " " + o + " "; rD.innerText = cur; } }
    function cl() { cur = ""; rD.innerText = "0"; hD.innerText = "0"; }
    function del() { cur = cur.trim().slice(0, -1); rD.innerText = cur || "0"; }
    function calc_eq() { try { let res = eval(cur.replace('×', '*').replace('÷', '/')); hD.innerText = cur + " ="; rD.innerText = res; cur = res.toString(); } catch { rD.innerText = "Err"; } }
    function convertirMinutos() {
        let m = parseInt(document.getElementById('minInp').value) || 0;
        document.getElementById('resConv').innerText = Math.floor(m / 60) + "h " + (m % 60) + "m";
    }

    recalc();
</script>
"""

components.html(layout + script, height=2000, scrolling=True)
