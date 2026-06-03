function updateFleetFloat() {{
        let html = "";
        let totalNoCar = 0;
let totalCarReal = 0;
let totalCarSchedule = 0;

        document.querySelectorAll('#body-' + currentTab + ' tr').forEach(row => {{
            let name = row.querySelector('.edit-name')?.innerText.trim();
            let stock = parseInt(row.querySelector('.f-stock')?.innerText) || 0;
            let left = parseInt(row.querySelector('.f-left')?.innerText) || 0;
            
            // Calculamos lo asignado
            let asignado = stock - left;

            if(name && stock > 0) {{

    // 🔥 TOTAL CAR SCHEDULE
    if(name.toLowerCase().includes("car")) {{
        totalCarSchedule += stock;
    }}

    let isCar = name.toLowerCase().includes("car") || name.toLowerCase().includes("híbrida");
                let colorCategoria = isCar ? "#FF4500" : "#0000CD";

                // Acumulamos totales
                if (isCar) {{
                    totalCarReal += asignado;
                }} else {{
                    totalNoCar += asignado;
                }}

                html += `
                    <div style="display:flex; justify-content:space-between; margin-bottom:4px; font-size: 14px;">
                        <span style="color: #135b83;">${{name}}</span>
                        <span style="color: ${{colorCategoria}}; font-weight: bold;">
                            ${{left}}/${{stock}}
                        </span>
                    </div>
                `;
            }}
        }});

        // Dibujamos los totales abajo
        html += `

            <div style="margin-top: 15px; padding-top: 10px; border-top: 2px solid #135b83;"> 


<div style="display:flex; justify-content:space-between; color: #000000; font-weight: 800; font-size: 16px;">
    <span>TOTAL CAR (sched):</span> <span>${{totalCarSchedule}}</span>
</div>
        
            <div style="margin-top: 15px; padding-top: 10px; border-top: 2px solid #135b83;"> 


    <div style="font-weight:bold; margin-bottom:8px;">
          <span>🚚 USADAS</span>
          </div>
          
                <div style="display:flex; justify-content:space-between; color: #0000CD; font-weight: 900; font-size: 16px;">
    <span>TOTAL MLP:</span> <span>${{totalNoCar}}</span>
</div>

<div style="display:flex; justify-content:space-between; color: #FF4500; font-weight: 900; font-size: 16px;">
    <span>TOTAL CAR (real):</span> <span>${{totalCarReal}}</span>
</div>

            </div>
        `;

        document.getElementById('fleet-float-body').innerHTML = html;

let panelBody = document.getElementById('panel-flota-body');

if(panelBody){{
    panelBody.innerHTML = html;
}}
        
        // Guardar estado (si existe la función)
        if (typeof guardarEstado === 'function') {{ guardarEstado(); }} 
    }}


aplicarPerfil();

    
    recalc();









import streamlit as st
import streamlit.components.v1 as components

# 1. ENLACE DE IMAGEN (Mapa de regiones)
ID_IMAGEN = "1M4GLEwFzhLrZjV-zmvGrdTQhC6IjwxOJ"
url_final = f"https://drive.google.com/thumbnail?id={ID_IMAGEN}&sz=w1000"

# 2. INFORMACIÓN OPERATIVA 100% COMPLETA
info_operativa = {
    "SDE": f"""
        <div style='text-align: center; margin-bottom: 25px;'>
            <img src="{url_final}" style="width: 100%; max-width: 800px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
        </div>

        <h3 style='color: #000; margin-bottom: 5px;'>ROL VP04</h3>
        <hr style='border: 1px solid #1E90FF; margin-bottom: 20px;'>
        
        <div style='background: white; border-left: 6px solid #1E90FF; padding: 15px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); color: #000; margin-bottom: 20px;'>
            <p style='margin: 0;'><strong>👉👉 PARA SDE</strong><br>
            - 🔷 Revisar si SVC agrega blancos<br>
            - Orígenes (imagen) + onway + despacho de hoy de las 3 pm en adelante + fecha promesa y/o quemada ...validar<br>
            - SPR 30<br>
            - ❌ delimitación / ❌ restricción<br>
            - Quito puntos muy lejanos</p>
        </div>

        <h3 style='color: #000; margin-top: 25px;'>🟪 SDE 🟪</h3>
        <hr style='border: 1px solid #FF00FF; margin-bottom: 20px;'>
        
        <div style='background: white; border-left: 6px solid #FF00FF; padding: 12px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); color: #000; margin-bottom: 12px;'>
            <p style='margin: 0;'><strong><span style="color: #FF00FF;">●</span> SMX9 PM2 - ⏰ 16:40 - 17:00</strong><br>
            - 📌 Orígenes: MXCD02, MXCD06<br>
            - 👉 Vol aprox. 800 / en peak puede aumentar hasta 1600<br>
            - 👉 fecha promesa</p>
        </div>

        <div style='background: white; border-left: 6px solid #FF00FF; padding: 12px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); color: #000; margin-bottom: 12px;'>
            <p style='margin: 0;'><strong><span style="color: #FF00FF;">●</span> SMX5 PM2 - ⏰ 17:20 - 17:40</strong><br>
             - 📌 Orígenes: MXCD02, MXCD06<br>
             - 👉 Vol aprox. 400<br>
             - 👉 fecha promesa + quemada</p>
        </div>

        <div style='background: white; border-left: 6px solid #FF00FF; padding: 12px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); color: #000; margin-bottom: 12px;'>
            <p style='margin: 0;'><strong><span style="color: #FF00FF;">●</span> SMX4 PM2 - ⏰ 17:40 - 18:00</strong><br>
            - 📌 Orígenes: MXCD02, MXCD06<br>
            - 👉 Vol aprox. 550<br>
            - 🏍️ Motos en donde sea con SPR 25<br>
            - 👉 fecha promesa + quemada</p> 
        </div>

        <div style='background: white; border-left: 6px solid #FF00FF; padding: 12px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); color: #000; margin-bottom: 12px;'>
            <p style='margin: 0;'><strong><span style="color: #FF00FF;">●</span> SMX2 PM1 - ⏰ 18:00 - 18:20</strong><br>
            - 📌 Orígenes: MXCD02, MXCD06<br>
            - 👉 fecha promesa + quemada</p>
            - 👉 Vol aprox. 250<br>
            - 👉 SPR 28</p>
        </div>

        <div style='background: white; border-left: 6px solid #FF00FF; padding: 12px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); color: #000; margin-bottom: 12px;'>
            <p style='margin: 0;'><strong><span style="color: #FF00FF;">●</span> SMT2 PM2 - ⏰ 18:40 - 19:00</strong><br>
            - 📌 Origen MXNL01<br>
            - 👉 Despacho hoy después 3 pm<br>
            - 👉 fecha promesa + quemada<br>
            - 👉 Vol. 800 aprox.<br>
            - 👉 SPR 27-28 / se van las 30 unidades<br>
            - 👉 Pido validación</p>
        </div>

        <h3 style='color: #000; margin-top: 25px;'>🟥 PRE-CARGAS 🟥</h3>
        <hr style='border: 1px solid #ff8c00; margin-bottom: 20px;'>

        <div style='background: white; border-left: 6px solid #ff8c00; padding: 15px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); color: #000; margin-bottom: 20px;'>
            <p style='margin: 0;'><strong>👉👉 INDICACIONES</strong><br>
            - 📌 Origen + despachos + onway<br>
            - 👉 Schedule del día siguiente / apartado en archivo AMO<br>
            - ➕ Mandan ids a agregar<br>
            - ✅ delimitación / ✅ dejar restricción</p>
        </div>
        
        <div style='background: white; border-left: 6px solid #ff8c00; padding: 12px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); color: #000; margin-bottom: 12px;'>
            <p style='margin: 0;'><strong><span style="color: #ff8c00;">●</span> SMX5 AM3 - ⏰ 21:50 - 22:30</strong><br>
             - 📌 Origen 09 + despacho de las 20:00 /21:00 hrs + onway<br>
             - ➕ Agregan ids a ciclo (revisar forms)<br>
             - ✅  Validan volumen / aprox. 2500-2600<br>
             - 🚛 Tlalpan norte, sur y Xochimilco con car 8h extra E1 (para no dropear)</p>
        </div>

        <div style='background: white; border-left: 6px solid #ff8c00; padding: 12px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); color: #000; margin-bottom: 12px;'>
            <p style='margin: 0;'><strong><span style="color: #ff8c00;">●</span> SMX2 AM3 - ⏰ 22:40 - 23:20</strong><br>
             - 📌 Orígenes: MXCD02 despacho 16:00 / MXCD09  despacho 14:00 / MXCD10  despacho 21:00<br>
             - 👉 Todo Onway<br>
             - 👀 Revisar si se agrega ➕ forms<br>
             - ✅  Validan volumen / aprox. 1900-2000<br>
             - 🚛 Revisar si se usa MLP hasta ahora solo Crowd 8h, Extendidas en Texcoco, Pueblos y Chalco</p>
        </div>




        <h3 style='color: #000; margin-top: 25px;'>👉 OTROS RUTEOS PM2 (SDE)</h3>
        <hr style='border: 1px solid #808080; margin-bottom: 20px;'> 


        

        <div style='background: white; border-left: 6px solid #808080; padding: 12px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); color: #000; margin-bottom: 12px;'>
            <p style='margin: 0;'><strong><span style="color: #808080;">●</span> SMX20 (SMX10) PM2 - ⏰ 0:20 pm</strong><br>
            - 📌 Origen 20 / ❌ SPR / ❌ Ocupación<br>
            - 👉 Meto ORH de 4 hrs para crowd 5 hrs / solo para dividir paquetes uso SPR 30<br>
            - 👉 Pido validación ➡️ @Luisa Itzel Perez y @Ibrahim</p>
        </div>

        <div style='background: white; border-left: 6px solid #808080; padding: 12px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); color: #000; margin-bottom: 12px;'>
            <p style='margin: 0;'><strong><span style="color: #808080;">●</span> SMX8 PM2 - ⏰ 5:30 pm</strong><br>
            - 👉 Sin schedule</p>
        </div>

        <div style='background: white; border-left: 6px solid #808080; padding: 12px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); color: #000; margin-bottom: 12px;'>
            <p style='margin: 0;'><strong><span style="color: #808080;">●</span> SMX3 PM2 - ⏰ 4:30 pm</strong><br>
            - 📌 Orígenes: MXCD02, MXCD06<br>
            - ✅ delimitación (salen planes) / ❌ restricción<br>
            - SPR 30/Moto y Crowd<br>
            - 🏍️ MOTOS ➡️ Cuauhtémoc-Polanco</p>
        </div>

        <div style='background: white; border-left: 6px solid #808080; padding: 12px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); color: #000; margin-bottom: 12px;'>
            <p style='margin: 0;'><strong><span style="color: #808080;">●</span> SBJ1 PM2 - ⏰ A partir de las 5:00 pm</strong><br>
            - 👉 Pido autorización para iniciar ruteo / SPR 28 / 200-300 pqt aprox</p>
        </div>

        <div style='background: white; border-left: 6px solid #808080; padding: 12px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); color: #000; margin-bottom: 12px;'>
            <p style='margin: 0;'><strong><span style="color: #808080;">●</span> SHM1 PM2 - ⏰ 7:20 pm</strong><br>
            - 👉 SPR 21 / crowd 5 hrs</p>
        </div>

        <div style='background: white; border-left: 6px solid #808080; padding: 12px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); color: #000; margin-bottom: 12px;'>
            <p style='margin: 0;'><strong><span style="color: #808080;">●</span> SMT1 PM2 - ⏰ 5:10 pm</strong><br>
            - 📌 Orígen: MXNL01<br>
            - 👉 SVC manda data (la envían tarde, solo hago el cruce para cotejo)</p>
        </div>

        <div style='background: white; border-left: 6px solid #808080; padding: 12px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); color: #000; margin-bottom: 12px;'>
            <p style='margin: 0;'><strong><span style="color: #808080;">●</span> SMT3 PM2 - ⏰ 5:15 pm</strong><br>
            - 👉 SPR 28 / crowd 5 hrs / 500 pqt aprox</p>
        </div>

        <div style='background: white; border-left: 6px solid #808080; padding: 12px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); color: #000; margin-bottom: 12px;'>
            <p style='margin: 0;'><strong><span style="color: #808080;">●</span> SGD1 PM2 - ⏰ 4:50 pm</strong><br>
             - 📌 Orígen: MXJC01</p>
        </div>

        <div style='background: white; border-left: 6px solid #808080; padding: 12px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); color: #000; margin-bottom: 12px;'>
            <p style='margin: 0;'><strong><span style="color: #808080;">●</span> SGD2 PM2 - ⏰ 0:00 pm</strong><br>
            - 👉 SPR 28</p>
        </div>

        <div style='background: white; border-left: 6px solid #808080; padding: 12px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); color: #000; margin-bottom: 12px;'>
            <p style='margin: 0;'><strong><span style="color: #808080;">●</span> SGD3 PM2 - ⏰ 4:50 pm</strong><br>
            - 👉 SPR 30 / crowd 5 y 3 hrs</p>
        </div>

        <div style='background: white; border-left: 6px solid #808080; padding: 12px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); color: #000; margin-bottom: 12px;'>
            <p style='margin: 0;'><strong><span style="color: #808080;">●</span> SMD2 PM1 - ⏰ 5:30 pm</strong><br>
            - 📌 Orígen: MXYU01<br>
            - 👉 Sin schedule / contemplo crowd 5 hrs<br>
            - 🚛 SVC manda en cuantas unidades y el SPR / entre 5 a 6 crowd 5 hrs con SPR 30<br>
            - 👉 Espero a que carguen volumen (x lo general lo cargan 10 min. antes de las 6:00 pm)<br>
            - 👉 Pido validación<br>
            - 👉 Piden mejor dispersion, indico: "Se publicó de acuerdo a la herramienta team, ya no podemos manipular la dispersión como antes"</p>
        </div>

        <div style='background: white; border-left: 6px solid #808080; padding: 12px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); color: #000; margin-bottom: 12px;'>
            <p style='margin: 0;'><strong><span style="color: #808080;">●</span> SPB1 PM2 - ⏰ 6:00 pm</strong><br>
            - 📌 Origen MXPB01<br>
            - 👉 Sin schedule / ocupo crowd 5 hrs a 30 SPR - depende puede mandarlas a 25 SPR<br>
            - 👉 Se carga en contingencia, no tiene ciclo normal creado<br>
            - 👉 Revisan volumen, notifican con palomita<br>
            - 👉 Pido validación</p>
        </div>

        
    """,
    "SIDE_LINE": """
        <h3 style='color: #000; margin-bottom: 5px;'>¿CÓMO LO HAGO?</h3>
        <hr style='border: 1px solid #1E90FF; margin-bottom: 20px;'>
        <div style='background: white; border-left: 6px solid #1E90FF; padding: 15px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); color: #000; margin-bottom: 20px;'>
            <p style='margin: 0;'>1️⃣ Descargo query de places (script job de SVC trabajado ▶️ ejecutar)<br>
            2️⃣ Routing matutino ▶️ busco lista places (sáb / dom)</p>
        </div>
        <div style='background: white; border-left: 6px solid #1E90FF; padding: 15px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); color: #000;'>
            <p style='margin: 0;'><strong>PASOS DETALLADOS:</strong><br>
            ▶️ Docto script job ▶️ BuscarV ▶️ columna U (customer id) ▶️ clic 1a celda<br>
            ▶️ En archivo places (copio desde place id / 5,0)<br>
            ▶️ Sale A, B ó C ▶️ copio y pego esos id´s ▶️ nueva pestaña en data (nombro "places")<br>
            ▶️ En data ▶️ buscarv para buscar en pestaña places<br>
            ▶️ No deben coincidir todos los id´s<br>
            ▶️ Lo que salga de cruce = places (no se rutea)<br><br>
            <strong>- Elijo "pasar al siguiente día"</strong><br>
            - C1 y C2 es el mismo proceso</p>
        </div>
    """,
    "ENLACES": """
        <h3 style='color: #000; margin-bottom: 5px;'>ENLACES</h3>
        <hr style='border: 1px solid #1E90FF; margin-bottom: 20px;'>
        <div style='background: white; border-left: 6px solid #1E90FF; padding: 15px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); color: #000;'>
            <div style='display: flex; flex-direction: column; gap: 15px;'>
                <a href="https://drive.google.com/drive/folders/1VNCUhdFxnV6MltnBFt4sH6AN_FJjL5jj" target="_blank" style="color: #1E90FF; text-decoration: none; font-weight: bold;">📁 SUBIR DATAS</a>
                <a href="https://docs.google.com/spreadsheets/d/1mj1krN2hXQQ1yFzswDoPscd9tPhguDnB-mAxB4aLPy0/edit" target="_blank" style="color: #1E90FF; text-decoration: none; font-weight: bold;">📅 SCHEDULE METRO</a>
                <a href="https://docs.google.com/spreadsheets/d/1lcrV9kxqwZB8007DPn4binDfDoD4enX26nISPWkOXDM/edit" target="_blank" style="color: #1E90FF; text-decoration: none; font-weight: bold;">📅 SCHEDULE CENTRO</a>
                <a href="https://docs.google.com/spreadsheets/d/1Gw1RG4XGfDCyz2lKmoj01OoOHQcaPpVagWCeKj-oCzE/edit" target="_blank" style="color: #1E90FF; text-decoration: none; font-weight: bold;">📅 SCHEDULE NORTE</a>
                <a href="https://docs.google.com/spreadsheets/d/1irZgPeFGGtJL2rRu2CYK6NHsjoieX-9DEA-rQCrRjKI/edit" target="_blank" style="color: #1E90FF; text-decoration: none; font-weight: bold;">📅 SCHEDULE SUR</a>
            </div>
        </div>
    """,
    "C1": "<div style='text-align:center; padding-top:100px; color:#666;'><i>Información C1 pendiente...</i></div>",
    "C2": "<div style='text-align:center; padding-top:100px; color:#666;'><i>Información C2 pendiente...</i></div>",
    "PREC": "<div style='text-align:center; padding-top:100px; color:#666;'><i>Información PRECARGA pendiente...</i></div>"
}

# 3. HTML/CSS (DISEÑO FINAL)
html_notitas = f"""
<style>
    body {{ background-color: #000000; font-family: 'Segoe UI', Tahoma, sans-serif; margin: 0; }}
    .main-box {{ background: #000000; padding: 10px; }}
    
    /* CONSOLA UNIFICADA (ARRIBA) */
    .unified-console {{
        background: #000000; border-radius: 15px; padding: 15px; 
        margin-bottom: 20px; border: 1px solid #000000; text-align: center;
    }}
    .display-screen {{
        background: #000000; border-radius: 10px; padding: 10px; margin-bottom: 15px; border: 2px solid #000000;
    }}
    .btn-3d {{
        background: linear-gradient(145deg, #1e90ff, #1c82e6);
        color: white; border: none; padding: 12px 25px; border-radius: 10px;
        font-weight: bold; cursor: pointer; box-shadow: 0 5px #0a56a3; transition: 0.1s;
    }}
    .btn-3d:active {{ box-shadow: 0 2px #0a56a3; transform: translateY(3px); }}

    .tab-bar {{ display: flex; gap: 8px; margin-bottom: 15px; overflow-x: auto; }}
    .tab-btn {{
        background: #333; color: white; border: none; padding: 10px 18px;
        border-radius: 8px; cursor: pointer; font-weight: bold; font-size: 12px; white-space: nowrap;
    }}
    .tab-btn.active {{ background: #add8e6; color: black; box-shadow: 0 0 12px #add8e6; }}





    
    .content-area {{ background: #c8dee0; border-radius: 12px; padding: 20px; min-height: 600px; color: #000; }}
</style>

<div class="main-box">
    <div class="unified-console"> 
        <div class="display-screen">
            <div style="color: #ffffff; font-size: 10px; margin-bottom: 5px;">HORA / RESTADOR / CONVERTIDOR</div>
            <div id="horaReal" style="font-size: 38px; color: #FF00FF; font-family: sans-serif; font-weight: bold;">--:--</div>
        </div>
        <div style="display: flex; justify-content: center; align-items: center; gap: 15px;">
            <div>
                <span style="color: #add8e6; font-size: 11px; display: block;">MINUTOS</span>
                <input type="number" id="minInput" value="10" 
                    style="background: #222; color: #FFE4E1; border: none; padding: 8px; border-radius: 5px; width: 70px; text-align: center; font-size: 20px; font-weight: bold;">
            </div>
            <button class="btn-3d" onclick="ejecutarTodo()">CALCULAR</button>
        </div>
    </div>

    <h3 style="color: #1E90FF; text-align: center; margin-bottom: 15px;">🍓 NOTITAS OPERATIVAS</h3>
    <div class="tab-bar">
        <button class="tab-btn active" onclick="changeTab(event, 'SDE')">SDE</button>
        <button class="tab-btn" onclick="changeTab(event, 'C1')">C1</button>
        <button class="tab-btn" onclick="changeTab(event, 'C2')">C2</button>
        <button class="tab-btn" onclick="changeTab(event, 'PREC')">PREC</button>
        <button class="tab-btn" onclick="changeTab(event, 'SIDE_LINE')">SIDE LINE</button>
        <button class="tab-btn" onclick="changeTab(event, 'ENLACES')">ENLACES</button>
    </div>
    <div id="visor" class="content-area">
        {info_operativa['SDE']}
    </div>
</div>

<script>
    const allData = {info_operativa}; 
    function changeTab(e, name) {{
        document.getElementById('visor').innerHTML = allData[name];
        let btns = document.getElementsByClassName('tab-btn');
        for (let b of btns) {{ b.classList.remove('active'); }}
        e.currentTarget.classList.add('active');
    }}
    function ejecutarTodo() {{
        const mins = document.getElementById('minInput').value || 0;
        const ahora = new Date();
        const nuevaFecha = new Date(ahora.getTime() - (mins * 60000));
        const h = String(nuevaFecha.getHours()).padStart(2, '0');
        const m = String(nuevaFecha.getMinutes()).padStart(2, '0');
        document.getElementById('horaReal').innerText = h + ":" + m;
    }}
    ejecutarTodo();
</script>
"""

# 4. RENDERIZADO EN STREAMLIT
st.markdown("---")
components.html(html_notitas, height=1200, scrolling=True)
