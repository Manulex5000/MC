
def InstalLiqDin(tipo_med: str, elem_flujo: str, L: float) -> float:
    tipo_med = tipo_med.upper()
    elem_flujo = elem_flujo.lower()

    if tipo_med in ["UFM", "TUR"]:
        if elem_flujo == "con acondicionador":
            if L >= 10:
                UL = 0
            else:
                UL = 5
        elif elem_flujo == "con rectificador":
            if L >= 10:
                UL = 0.05
            else:
                UL = 5
        elif elem_flujo == "sin acondicionador":
            if L >= 25:
                UL = 0.1
            elif L >= 10:
                UL = 0.2
            else:
                UL = 5
        else:
            UL = None  # Si no coincide ningún caso
    elif tipo_med in ["DP", "COR"]:
        UL = 0
    else:
        UL = None  # Si no coincide ningún tipo

    return UL