# ==========================================
# 📚 BASE DE CONOCIMIENTO Y REGLAS DE RUTEO
# ==========================================

reglas_ruteo = {
    "smx9_extendido": (
        "**Prioridades SMX9 SD2:**\n\n"
        "* 📌 Orígenes: MXCD02, MXCD06\n"
        "* 👉 Último despacho de hoy (3 pm en adelante)\n"
        "* 👉 Fecha promesa + fecha quemada + onway"
    ),
    "sgd2_extendido": (
        "**Prioridades SGD2 SD3:**\n\n" 
        "* 📌 Orígenes: MXJC01 para SD3 y MXJC02 para SD2 (en caso de que no hayan ruteado sd2 en la mañana)\n"
        "* 👉 MXJC01 - último despacho de hoy (3 pm adelante) + fecha promesa + onway\n"
        "* 👉 MXJC02 - último despacho de hoy (1 pm) + fecha promesa + onway // si salen poquitos, agarra todo el despacho del día + fecha promesa y quemada + todo at station y manda pivot para que SVC te valide vol.\n"
        "* 👉 Revisar unidades con SVC (a veces indica usar Small Van con la cantidad indicada para las car 5h de schedule\n"
        "* 👉 Puedes pedir validación (no es necesario)\n"
        "* 👉 Prefijo SD3 siempre"
    ),
    "smx5_precarga": (
        "**Prioridades SMX5 (PRECARGA):**\n\n"
        "* 📌 Origen: MXCD09 + onway\n"
        "* 👀 OJO: últimamente piden usar Small Van en Chalco y Xochimilco (revisar)\n"
        "* 👀 OJO: con indicaciones de reducción de ORH en Xochimilco (u otro polígono)\n"
        "* 👉 Resto de planes asignar Car 8h y Extendidas\n"
        "* 👉 Revisar si mandan ids a agregar del origen 10\n"
        "* 👉 **Cercanía de SVC:** Coyoacán, Iztapalapa, Tláhuac, Tlalpan nte, Tlalpan sur, Xochi, Chalco y Milpa Alta"
    ),
    "smx5_extendido": (
        "**Prioridades SMX5 (EXTENDIDO):**\n\n"
        "* 📌 Orígenes: MXCD02, MXCD06\n"
        "* 👉 Último despacho de hoy (3 pm en adelante)\n"
        "* 👉 Fecha promesa + fecha quemada + onway"
    ),
    "smx4_extendido": (
        "**Prioridades SMX4:**\n\n"
        "* 👉 Preguntar si habrá ids a descartar\n"
        "* 📌 Orígenes: MXCD02, MXCD06\n"
        "* 👉 Último despacho de hoy (3 pm en adelante)\n"
        "* 👉 Fecha promesa + onway\n"
        "* 🏍️ Motos SPR 30"
    ),
    "smx2_extendido": (
        "**Prioridades SMX2:**\n\n"
        "* 📌 Orígenes: MXCD02, MXCD06\n"
        "* 👉 Último despacho de hoy (3 pm en adelante)\n"
        "* 👉 fecha promesa + quemada + onway\n"
        "* 👉 Rutear con parámetros precargados en logis SIN SPR"
    ),
    "smt2_extendido": (
        "**Prioridades SMT2:**\n\n"
        "* 📌 Origen MXNL01\n"
        "* 👉 Último despacho de hoy (3 pm en adelante)\n"
        "* 👉 fecha promesa + quemada + onway\n"
        "* 👉 Se pide validación"
    ),
    "scp1": (
        "**Prioridades SCP1 C1:**\n\n"
        "* 📌 Ellos envían el volumen a tomar\n"
        "* 📌 Sale cherry (no olvidar compartir al SVC)\n"
        "* 📌 Si no te especifican el despacho a excluir haz tu pivot con todo el volumen y ahí revisas cuál despacho o salida coincide con la cantidad a excluir, eso lo pones como NO RUT (recuerda que debe ser onway) y le pides validación al SVC antes de subirlo a logis\n"
        "* 🔴 **Campeche:** ➤ Rental Large Van (excluír/sin nodos)\n"
        "* 🔴 **Campeche:** ➤ Delivery Cell (Dedicada/lleva todos nodos/paradas=nodos)\n"
        "* 🟣 **Delivery Cell** ➤ Parámetros de Large Van MLP\n"
        "* 🟢 **Resto planes:** ➤ Large Van MLP (si hay nodo=híbrida)."
    ),
    "smd1": (
        "**Prioridades SMD1 C1:**\n"
        "* 📌 Sale cherry (no olvidar compartir al SVC-compartir captura de pantalla antes del cherry)\n"
        "* 🔴 **Centro:** ➤ Prioridad = Rental (híbridas) / Crowd / LV (híbridas) / SV\n"
        "* 🔴 **Centro:** ➤ Extra large van H&B (son 3 de 50 ids c/u = ciudad Mérida) / MLP Bulk (pueden ir 2 en un centro y 1 en otro /depende en cuál haya + voluminosos)\n"
        "* 🟠 **Norte:** ➤ Prioridad = Crowd zon ext 10hrs / MLP\n"
        "* 🟡 **Kanasin:** ➤ Si sobran crowd colocarlas aquí\n"
        "* 🟣 **Resto de planes:** ➤ Large Van MLP\n"
        "* 🔵 **Planes ND:** ➤ Tekax y ___ = Large Van MLP\n"
        "* 🟤 Priorizar las LV y Rentals"
    ),
    "sch1": (
        "**Prioridades SCH1 C1:**\n\n"
        "* 🟢 Falta info\n"
        "* 🟢 Falta info\n"
        "* 🟢 Falta info\n"
        "* 🟢 Falta info\n"
        "* 🟣 Falta info\n"
        "* 🔵 Falta info\n"
        "* 🟤 Falta info"
    ),
    "sja1": (
        "**Prioridades SJA1 C1:**\n\n"
        "* 📌 Ellos envían el volumen a tomar /Apagado CP\n"
        "* 🟢 **Centro 1/2:** ➤ PRIORIDAD\n"
        "* 1. Rental Electric 2. Rental LV 3. Rental Replacement 4. MLP y Crowd\n"
        "* 🟢 **Centro 1/2:** ➤ 3.5 tons (dedicada=3 paradas) y delivery (dedicada=3 paradas)\n"
        "* 🟢 **Centro 1/2:** ➤ H&B (bulk=híbrida)\n"
        "* 🔴 **BULK:** ➤ 60 ids de Xalapa = Voluminosos se cargan después de lo no ruteado del ciclo\n"
        "* 🚛 FORÁNEOS = Large Van MLP / Con Nodos = Híbrida\n"
        "* 🚛 FORÁNEOS = Small Van MLP / Sin nodos\n"
        "* 🚛 FORÁNEOS = Xico y Tuzamapa / Mlp, Crowd\n"
        "* 🔵 **EJA1-SP:**➤  Media milla-ruteo fake\n"
        "* 🟤 **Alchichica ND-AM0:** ➤ 2 unidades Small Van MLP/330 min ó 65 ids c/u."
    )
}


# ==========================================
# 🗺️ BASE DE DATOS DE ORIGENES (MAPA OPERATIVO)
# ==========================================
MAPA_ORIGENES = {
    # 🔵 REGIÓN METRO (CDMX)
    "smx2": {"region": "Metro (CDMX)", "origen": "MXCD02, MXCD06", "val": "❌ No"},
    "smx3": {"region": "Metro (CDMX)", "origen": "MXCD02, MXCD06", "val": "❌ No"},
    "smx4": {"region": "Metro (CDMX)", "origen": "MXCD02, MXCD06", "val": "❌ No"},
    "smx5": {"region": "Metro (CDMX)", "origen": "MXCD02, MXCD06", "val": "❌ No"},
    "smx7": {"region": "Metro (CDMX)", "origen": "MXCD02, MXCD06", "val": "❌ No"},
    "smx8": {"region": "Metro (CDMX)", "origen": "MXCD10", "val": "❌ No"},
    "smx9": {"region": "Metro (CDMX)", "origen": "MXCD02, MXCD06", "val": "❌ No"},
    "smx10": {"region": "Metro (CDMX)", "origen": "MXCD02, MXCD06, MXCD20", "val": "❌ No"},
    "smx10 sd3": {"region": "Metro (CDMX)", "origen": "MXCD20", "val": "❌ No"},
    "stl1": {"region": "Metro (CDMX)", "origen": "MXCD02", "val": "❌ No"},
    "shp1": {"region": "Metro (CDMX)", "origen": "MXCD10", "val": "❌ No"},

    # 🟡 REGIÓN CENTRO
    "ssl1": {"region": "Centro", "origen": "MXGT01", "val": "❌ No"},
    "sbj1": {"region": "Centro", "origen": "MXGT01", "val": "❌ No"},
    "sle1": {"region": "Centro", "origen": "MXGT01", "val": "❌ No"},
    "sgd1": {"region": "Centro", "origen": "MXJC01", "val": "❌ No"},
    "sgd2": {"region": "Centro", "origen": "MXJC01", "val": "❌ No"},
    "sgd3": {"region": "Centro", "origen": "MXJC01", "val": "❌ No"},

    # 🩵 REGIÓN NORTE
    "smt1": {"region": "Norte", "origen": "MXNL01", "val": "✔️ Sí"},
    "smt2": {"region": "Norte", "origen": "MXNL01", "val": "✔️ Sí"},
    "smt3": {"region": "Norte", "origen": "MXNL01", "val": "✔️ Sí"},
    "shm1": {"region": "Norte", "origen": "MXSO01", "val": "✔️ Sí"},

    # 🟠 REGIÓN SUR
    "smd2": {"region": "Sur", "origen": "MXYU01", "val": "✔️ Sí"}
}


# ==========================================
# 💡 PREGUNTAS FRECUENTES Y REGLAS OPERATIVAS ADICIONALES
# ==========================================
PREGUNTAS_FRECUENTES = {
    "large_van_sdd": (
        "🚐 **Large Van SDD (SCP1 C1 y SJA1 C1):**\n\n"
        "* Ya vienen precargadas en Logis por defecto.\n"
        "* Se deben utilizar para **ambos services**."
    ),
    "large_van_scp1": (
        "🚐 **Large Van MLP / Large Van SDD para SCP1 C1:**\n\n"
        "* En **SCP1 C1**, las unidades **Large Van MLP** aparecen en Logis registradas con el nombre **Large Van SDD**.\n"
        "* Ya vienen precargadas por defecto en el sistema para usarse en ambos services.\n"
        "* 🟢 **Regla para resto de planes:** Asignar Large Van MLP (si el plan lleva nodo, se configura como híbrida)."
    ),
    "bulk_general": (
        "📦 **Ubicación de unidades Bulk (General):**\n\n"
        "* Las unidades Bulk se deben asignar en los polígonos que tengan **mayor cantidad de paquetes voluminosos**."
    ),
    "bulk_sja1": (
        "📦 **Bulk en SJA1 C1:**\n\n"
        "* Van asignadas en **Centro 1** ó **Centro 2**, dependiendo en cuál de los dos haya mayor volumen de voluminosos."
    ),
    "prioridades_centro_sja1": (
        "🎯 **Prioridades de Asignación en Centro (SJA1):**\n\n"
        "Se deben asignar en este orden prioritario (en Centro 1 ó Centro 2):\n"
        "1. 🚛 **Truck 3.5 Tons**\n"
        "2. 📦 **Delivery Cell Large Van**\n"
        "3. ⚡ **Rental Electric Large Van**\n"
        "4. 🚐 **Rental Large Van**\n"
        "5. 🔄 **Rental Replacement**\n"
        "6. 📦 **Extra Large Van H&B**"
    ),
    "prioridades_foraneos_sja1": (
        "🚛 **Prioridades Foráneos (SJA1):**\n\n"
        "* **1º Lugar:** Large Van MLP (en Logis aparecen como *Large Van SDD*).\n"
        "  * 👉 **PRIORIDAD ABSOLUTA:** Llenar primero los planes que llevan **nodos** (como Perote y Tlaltetela).\n"
        "  * 👉 Después cubrir el resto de foráneos hasta agotar las Large Van.\n"
        "* **2º Lugar:** Small Van MLP (en Logis aparecen como *Small Van SDD*)."
    ),
    "tuzamapa_xico": (
        "🏞️ **Reglas Especiales para Xico y Tuzamapa (SJA1):**\n\n"
        "* **Orden de prioridad:** Large Van MLP ➡️ Small Van MLP ➡️ Crowd (*Car 8h* y *Small Van 9h extra*).\n"
        "* ⚠️ **Mínimos obligatorios de MLP (Restricción de Logis):**\n"
        "  * **Xico:** Debe llevar **al menos 2 ó 3 MLP**.\n"
        "  * **Tuzamapa:** Con **1 MLP** es suficiente.\n"
        "  * **Nota:** El resto del volumen se cubre con Crowd. Es crucial poner las MLP mínimas porque, aunque sobren Crowds en schedule, Logis no acepta más de cierto límite y deja paquetes fuera por restricción."
    ),
    "dropeo_nodos_sja1": (
        "⚠️ **Dropeo de Nodos (SJA1):**\n\n"
        "* Se cargan en **contingencia** utilizando las unidades disponibles del schedule.\n"
        "* Si sobran **Rentals**, se usan primero.\n"
        "* El resto se cubre con **MLP** (si hay disponibles) y luego con **Crowd**.\n"
        "* 📌 *Ten en cuenta que igual pueden quedar paquetes fuera por zona de restricción.*"
    ),
    "alchichica": (
        "🚛 **Plan Alchichica ND (SJA1):**\n\n"
        "* Se carga en **AM0** (Next Day).\n"
        "* Se le asignan **2 unidades Small Van MLP** (en Logis aparecen como *Small Van SDD*).\n"
        "* Si el sistema bota una unidad por bajo volumen, déjala así.\n"
        "* 📏 **Requisitos obligatorios (debe cumplir al menos 1):**\n"
        "  1. Tener **65 IDs** por cada unidad.\n"
        "  2. Tener un **ORH de 300 minutos (5 hrs)**."
    ),
    "scp1_cambios": (
        "🔄 **Ajustes y Quitar Unidades en SCP1:**\n\n"
        "* Las Large Van MLP en logis aparecen como Large Van SDD, esas se usan.\n"
        "* Pueden solicitar quitar unidades o pasar planes a **Ciclo 2** (se realizan los cambios y se pide validación al SVC).\n"
        "* 📏 **Regla de oro:** Las unidades deben cumplir con nuestro **ORH**; mientras cumplan con el tiempo, no hay problema.\n"
        "* 📌 *Nota:* Cuando el SVC pide quitar unidades, generalmente es porque van un poco bajas en ORH."
    ),
    "smd1_prioridad": (
        "📊 **Prioridades en SMD1:**\n\n"
        "* Recuerda que en SMD1 la prioridad de unidades y asignación de flota es **diferente** al resto de las estaciones."
    )
}
