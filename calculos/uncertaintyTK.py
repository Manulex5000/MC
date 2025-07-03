import numpy as np
# import metrolopy as met
from calculos.propLiq import Constants, calcular_densidad, calcular_CTL, calcular_CPL
from calculos.calvol import CSW

Pb = 14.65  # Base pressure, psi (from API Reference)
Tref = 60.0  # Reference Temperature, °F (from API Reference)
corr = 0.01374979547  # Temperature shift value (from API Reference)
dH2O = 999.016
corrCTL = 0
corrCPL = 0


def calcular_incertidumbre(data):
    try:

        print("📡 Datos recibidos en Flask:", data)  # ✅ Depuración
        API = float(data.get('API', 0))
        product = data.get('product', 'Crude Oil')
        Tl = float(data.get('Tl', 0))
        Pl = float(data.get('Pl', 0))
        Pe = float(data.get('Pe', 0))
        # MR = float(data.get('MR', 0))
        # KF = float(data.get('KF', 0))
        # MF = float(data.get('MF', 0))
        Tamb = float(data.get('Tamb', 0))
        TOV = float(data.get('TOV', 0))
        SW = float(data.get('SW', 0) or 0)/100

        # --------Entradas de incertidumbre---------
        # -------------Temperatura-----------
        resTl = float(data.get('resTl', 0))
        errorTl = float(data.get('errorTl', 0))
        ucalTL = float(data.get('ucalTl', 0))
        kcalTL = float(data.get('kcalTl', 0))
        uderTL = float(data.get('uderTl', 0))
        # Se agregó en el modelo de Tanques
        uTamb = float(data.get('uTamb', 0))
        # -------------Presión-----------
        resPl = float(data.get('resPl', 0))
        errorPl = float(data.get('errorPl', 0))
        ucalPL = float(data.get('ucalPl', 0))
        kcalPL = float(data.get('kcalPl', 0))
        uderPL = float(data.get('uderPl', 0))

        # -------------%SW-----------
        metSW = data.get('metSW', 'externo')
        uTSed = float(data.get('uTSed', 0))
        uTW = float(data.get('uTW', 0))
        kTW = float(data.get('kTW', 0))
        kSed = float(data.get('kSed', 0))
        # -------------densidad-----------
        metdl = data.get('metdl', 'externo')
        uTSed = float(data.get('uTdl', 0))
        kTW = float(data.get('kdl', 0))
        # -------------volumen-----------
        uTOV = float(data.get('uTOV', 0))  # Se agregó en el modelo de Tanques
        uFW = float(data.get('FW', 0))  # Se agregó en el modelo de Tanques
        uSW = float(data.get('uSW', 0))  # Se agregó en el modelo de Tanques
        tipoMet = data.get('tipoMet')
        ucalMet = float(data.get('ucalMet', 0))
        kcalMet = float(data.get('kcalMet', 0))
        ecalMet = float(data.get('ecalMet', 0))
        conditioner = data.get('conditioner', 'sin_acond')
        uplong = data.get('upLong', '0')
        dwlong = data.get('dwLong', '0')
        twlong = data.get('twLong', '0')

        print("✅ Variables extraídas correctamente")

        # Calculo de la densidad en kg/m3
        dl_value = calcular_densidad(API, dH2O)
        print("✅ densidad calculada correctamente")

        # Constantes
        K0, K1, K2 = Constants(product, dl_value, Tl)
        print("✅ dconstantes calculada correctamente")

        # CTL
        Bl_value = K0 / (dl_value ** 2) + K1 / dl_value + K2
        CTL_value = calcular_CTL(product, Bl_value, Tl, Tref)
        print("✅ ctl calculada correctamente")

        # CPL
        F_value = np.exp(-1.9947 + 0.00013427 * Tl + 0.79392 /
                         (dl_value / 1000) ** 2 + 0.002326 * Tl / (dl_value / 1000) ** 2)
        CPL_value = calcular_CPL(product, Pl, Pe, Pb, F_value)
        print("✅ cpl calculada correctamente")

        # CSW
        CSW_value = CSW(SW)
        # GSV
        # GSV_value = GSV(MR, KF, MF, CTL_value, CPL_value,
        #                CSW_value, corrCTL, corrCPL)

        # print(f"✅ GSV calculado: {GSV_value}")

        # print(f"✅ GSV convertido a float correctamente")

        print(CTL_value, CPL_value)

        return {
            "CTL": {CTL_value},
            "CPL": {CPL_value},
            "dl": {dl_value}
        }

    except Exception as e:
        return {"error": str(e)}
