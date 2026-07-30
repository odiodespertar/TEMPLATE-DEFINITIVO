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
        "* 👉 Se pide validación\n"
        "* 👉 Prefijo SD3 siempre"
    ),
    "smx5_precarga": (
        "**Prioridades SMX5 (PRECARGA):**\n\n"
        "* 📌 Origen: MXCD09 + onway\n"
        "* 👉 Iztapalapa, Coyoacán y si alcanza Tláhuac = Small Van 9h\n"
        "* 👉 Resto de planes con car 8h\n"
        "* 👉 Revisar si mandan ids a agregar\n"
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
        "* 👉 Fecha promesa + fecha quemada + onway\n"
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
        "* 🔴 **Campeche:** ➤ Rental Large Van (excluír/sin nodos)\n"
        "* 🔴 **Campeche:** ➤ Delivery Cell (Dedicada/lleva todos nodos/paradas=nodos)\n"
        "* 🟣 **Delivery Cell** ➤ Parámetros de Large Van MLP\n"
        "* 🟢 **Resto planes:** ➤ Large Van MLP (si hay nodo=híbrida)."
    ),
    "smd1": (
        "**Prioridades SMD1 C1:**\n"
        "* 🟢 **Centro:** ➤ Rental(híbridas) / Crowd / LV(híbridas) / SV\n"
        "* 🟢 **Centro:** ➤ Extra large van H&B / MLP Bulk (ver en qué centro hay + voluminosos y ahí se meten)\n"
        "* 🔵 **Norte:** ➤ Crowd zon ext 10hrs / MLP\n"
        "* 🟣 **Kanasin:** ➤ Si sobran crowd colocarlas aquí\n"
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
        "* 🚛 FORÁNEOS = Large Van MLP / Con Nodos = Híbrida\n"
        "* 🚛 FORÁNEOS = Small Van MLP / Sin nodos\n"
        "* 🚛 FORÁNEOS = Xico y Tuzamapa / Mlp, Crowd\n"
        "* 🔵 **EJA1-SP:**➤  Media milla-ruteo fake\n"
        "* 🟤 **Alchichica ND-AM0:** ➤ 2 unidades Small Van MLP/330 min ó 65 ids c/u."
    )
}
