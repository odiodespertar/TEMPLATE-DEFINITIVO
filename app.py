import streamlit as st

# Configuración de la página profesional
st.set_page_config(page_title="Monitor Logístico VP04", layout="wide")

# Estilos para ocultar elementos de Streamlit y dar apariencia de App nativa
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {padding-top: 1rem; padding-bottom: 0rem;}
    </style>
""", unsafe_allow_html=True)

# --- CÓDIGO MAESTRO (HTML + CSS + JS) ---
herramienta_html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f0f2f5; margin: 0; padding: 20px; }
        
        /* Cronómetro Flotante 3D */
        #crono-wrapper {
            position: fixed; top: 10px; right: 10px; z-index: 9999;
            background: #1a1a1a; padding: 12px 15px; border-radius: 10px;
            color: white; width: 220px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); border: 1px solid #333;
        }

        /* Estilos de Tablas Tipo MELI */
        .meli-table { width: 100%; border-collapse: separate; border-spacing: 0; margin-bottom: 20px; border: 1px solid #ccc; border-radius: 8px; overflow: hidden; background: white; }
        .meli-table th { background: #696969; color: white; padding: 10px; font-size: 12px; }
        .meli-table td { padding: 8px; border-bottom: 1px solid #eee; font-size: 13px; }

        /* Calculadora Aqua */
        #calc_container {
            background: linear-gradient(145deg, #22c5bc, #1da29b);
            border-radius: 20px; padding: 15px; box-shadow: 5px 5px 15px #aaa;
            margin-top: 20px; border: 1px solid #178f88;
        }
        .calc-display { background: #fffacd; padding: 10px; text-align: right; border-radius: 8px; margin-bottom: 10px; border: 1px solid #ddd; }
        .btn-calc { 
            background: linear-gradient(180deg, #ffffff 0%, #f0f4f8 100%);
            border: 1px solid #ccc; border-radius: 8px; padding: 12px; font-weight: bold; cursor: pointer;
            box-shadow: 1px 1px 3px rgba(0,0,0,0.2);
        }
        .btn-calc:active { transform: translateY(2px); }

        /* Contenedores Principales */
        .main-grid { display: grid; grid-template-columns: 1fr 450px; gap: 20px; }
        .poligono-bloque { background: white; border-radius: 10px; padding: 15px; margin-bottom: 15px; border-left: 5px solid #20B2AA; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        
        [contenteditable]:focus { background: #fffde7; outline: 2px solid #20B2AA; }
    </style>
</head>
<body>

<div id="crono-wrapper">
    <div style="display: flex; justify-content: space-between; font-size: 11px; color: #00d4ff; margin-bottom: 5px;">
        <span>HORA LOCAL</span> <span id="reloj-f">00:00:00</span>
    </div>
    <div id="display-f" style="font-size: 26px; text-align: center; font-family: monospace; font-weight: bold; margin: 5px 0;">00:00:00.0</div>
    <div style="display: flex; gap: 5px; justify-content: center;">
        <button onclick="startT()" style="background:#28a745; border:none; color:white; padding:5px 10px; border-radius:4px; cursor:pointer;">START</button>
        <button onclick="pauseT()" style="background:#ffc107; border:none; padding:5px 10px; border-radius:4px; cursor:pointer;">PAUSE</button>
        <button onclick="resetT()" style="background:#dc3545; border:none; color:white; padding:5px 10px; border-radius:4px; cursor:pointer;">RESET</button>
    </div>
</div>

<div class="main-grid">
    <!-- COLUMNA IZQUIERDA: GESTIÓN DE PLANES -->
    <div id="planes-seccion">
        <h2 style="color: #444; border-bottom: 2px solid #696969;">📋 Gestión de Polígonos</h2>
        <div class="poligono-bloque">
            <table class="meli-table">
                <thead>
                    <tr><th>TIPO</th><th>CANT.</th><th>SPR REAL</th></tr>
                </thead>
                <tbody id="filas-plan">
                    <tr class="calc-row">
                        <td><select class="s-type" onchange="recalc()"><option>C1</option></select></td>
                        <td class="u-manual" contenteditable="true" oninput="recalc()">0</td>
                        <td class="spr-real-val" contenteditable="true" oninput="recalc()">100</td>
                    </tr>
                </tbody>
            </table>
            <div style="display: flex; justify-content: space-between; align-items: center; font-weight: bold;">
                <div>VOL. TOTAL: <span class="v-total-val">500</span></div>
                <div>CALCULADO: <span class="v-calculado-total">0</span></div>
                <div class="p-diff" style="padding: 5px 10px; border-radius: 5px;">VACÍO</div>
            </div>
        </div>
    </div>

    <!-- COLUMNA DERECHA: FLOTA Y CALCULADORA -->
    <div>
        <h2 style="color: #444;">🚚 Flota Disponible</h2>
        <table class="meli-table">
            <thead>
                <tr id="header-flota">
                    <th>UNIDAD</th><th>STOCK</th><th id="col-quedan">ME QUEDAN</th>
                </tr>
            </thead>
            <tbody id="body-flota">
                <tr>
                    <td class="edit-name">C1</td>
                    <td class="edit-stock" contenteditable="true" oninput="recalc()">10</td>
                    <td class="f-left" style="font-weight: bold;">10</td>
                    <td class="edit-spr-min" style="display:none">80</td>
                    <td class="edit-spr-max" style="display:none">120</td>
                </tr>
            </tbody>
        </table>

        <!-- CALCULADORA -->
        <div id="calc_container">
            <div class="calc-display">
                <div id="h_calc" style="font-size: 12px; color: #777;">0</div>
                <div id="r_calc" style="font-size: 24px; font-weight: bold;">0</div>
            </div>
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px;">
                <button class="btn-calc" onclick="an('7')">7</button><button class="btn-calc" onclick="an('8')">8</button><button class="btn-calc" onclick="an('9')">9</button><button class="btn-calc" onclick="ao('/')">÷</button>
                <button class="btn-calc" onclick="an('4')">4</button><button class="btn-calc" onclick="an('5')">5</button><button class="btn-calc" onclick="an('6')">6</button><button class="btn-calc" onclick="ao('*')">×</button>
                <button class="btn-calc" onclick="an('1')">1</button><button class="btn-calc" onclick="an('2')">2</button><button class="btn-calc" onclick="an('3')">3</button><button class="btn-calc" onclick="ao('-')">-</button>
                <button class="btn-calc" onclick="an('0')">0</button><button class="btn-calc" onclick="cl()">AC</button><button class="btn-calc" style="background:#FF00FF; color:white;" onclick="calc_eq()">=</button><button class="btn-calc" onclick="ao('+')">+</button>
            </div>
        </div>
    </div>
</div>

<script>
    // LÓGICA DE RECALC (Tu código de precisión)
    let editedRows = new Set();
    
    function recalc() {
        let fleet = {};
        // 1. Mapear flota
        document.querySelectorAll('#body-flota tr').forEach(row => {
            let nC = row.querySelector('.edit-name'), sC = row.querySelector('.edit-stock');
            let miC = row.querySelector('.edit-spr-min'), maC = row.querySelector('.edit-spr-max');
            let lC = row.querySelector('.f-left');
            
            let name = nC.innerText.trim();
            let stock = parseInt(sC.innerText) || 0;
            
            if (name !== "") {
                fleet[name] = { min: 80, max: 120, stock: stock, used: 0 };
            }
        });

        // 2. Procesar planes
        let volTotal = parseFloat(document.querySelector('.v-total-val').innerText) || 0;
        let volAsignadoAcumulado = 0;

        document.querySelectorAll('.calc-row').forEach(row => {
            let type = row.querySelector('.s-type').value;
            let spanU = row.querySelector('.u-manual'), spanS = row.querySelector('.spr-real-val');

            if (fleet[type]) {
                let uVal = parseInt(spanU.innerText) || 0;
                let sVal = parseInt(spanS.innerText) || 0;
                fleet[type].used += uVal;
                volAsignadoAcumulado += (uVal * sVal);
            }
        });

        // 3. Actualizar Volumen
        let celdaTotal = document.querySelector('.v-calculado-total');
        let totalRedondeado = Math.round(volAsignadoAcumulado);
        celdaTotal.innerText = totalRedondeado;
        celdaTotal.style.color = (totalRedondeado === volTotal) ? "#20B2AA" : "#d32f2f";

        // 4. Actualizar Flota y Negativos
        let tieneNegativosGlobal = false;
        document.querySelectorAll('#body-flota tr').forEach(row => {
            let n = row.querySelector('.edit-name').innerText.trim();
            if(fleet[n]) {
                let rest = fleet[n].stock - fleet[n].used;
                let c = row.querySelector('.f-left');
                c.innerText = rest;
                
                if (rest < 0) {
                    tieneNegativosGlobal = true;
                    c.style.color = "#FF4500";
                    c.style.fontSize = "18px";
                } else {
                    c.style.color = "#228B22";
                    c.style.fontSize = "18px";
                }
            }
        });

        // Título dinámico
        document.getElementById('col-quedan').innerText = tieneNegativosGlobal ? "ME PASÉ POR" : "ME QUEDAN";
    }

    // CALCULADORA FUNCIONES
    let cur = ""; 
    const rD = document.getElementById('r_calc'), hD = document.getElementById('h_calc');
    function an(n) { cur += n; rD.innerText = cur; }
    function ao(o) { if(cur!=="") { cur += o; rD.innerText = cur; } }
    function cl() { cur = ""; rD.innerText = "0"; hD.innerText = "0"; }
    function calc_eq() { try { hD.innerText = cur + " ="; cur = eval(cur).toString(); rD.innerText = cur; } catch { rD.innerText = "Err"; } }

    // CRONÓMETRO LÓGICA
    let timer, elapsed = 0;
    function startT() { if(!timer) timer = setInterval(() => { elapsed += 100; updateD(); }, 100); }
    function pauseT() { clearInterval(timer); timer = null; }
    function resetT() { pauseT(); elapsed = 0; updateD(); }
    function updateD() {
        let ms = Math.floor((elapsed % 1000) / 100);
        let s = Math.floor((elapsed / 1000) % 60);
        let m = Math.floor((elapsed / 60000) % 60);
        document.getElementById('display-f').innerText = `${m.toString().padStart(2,'0')}:${s.toString().padStart(2,'0')}.${ms}`;
    }
    setInterval(() => { document.getElementById('reloj-f').innerText = new Date().toLocaleTimeString(); }, 1000);

    // ATAJOS TECLADO
    document.addEventListener('keydown', (e) => {
        if (e.key >= '0' && e.key <= '9') an(e.key);
        if (e.key === 'Enter') calc_eq();
        if (e.key === 'Escape') cl();
    });

    recalc();
</script>
</body>
</html>
"""

# Renderizar en Streamlit
st.components.v1.html(herramienta_html, height=1000, scrolling=True)
