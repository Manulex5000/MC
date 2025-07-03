import numpy as np
import math
from calculos.propLiq import Constants, calcular_densidad, calcular_CTL, calcular_CPL
from calculos.instOper import InstalLiqDin
from calculos.calvol import CSW

Pb = 14.65  # Base pressure, psi (from API Reference)
Tref = 87.0  # Reference Temperature, °F
corr = 0.01374979547  # Temperature shift value
dH2O = 999.016  # Water density in kg/m³


def u_simul(un, dist, nsim):
    if dist == "normal":
        u = np.random.normal(0, un, nsim)
    elif dist == "uniforme":
        u = np.random.uniform(-un, un, nsim)
    elif dist == "triangular":
        u = np.random.triangular(-un, 0, un, nsim)
    elif dist == "lognormal":
        u = np.random.lognormal(0, un, nsim)
    else:
        u = np.zeros(nsim)
    return u


def u_magntiud(nsim, Media, ur1, dist1, ur2, dist2, ur3, dist3, ur4=None, dist4=None, ur5=None, dist5=None):
    u1 = u_simul(ur1, dist1, nsim)
    u2 = u_simul(ur2, dist2, nsim)
    u3 = u_simul(ur3, dist3, nsim)
    u4 = u_simul(ur4, dist4, nsim)
    u5 = u_simul(ur5, dist5, nsim)

    simul = Media + u1 + u2 + u3 + u4 + u5

    return simul


def montecarloU(data):
    Pb = 14.65  # Base pressure, psi (from API Reference)
    Tref = 60.0  # Reference Temperature, °F
    corr = 0.01374979547  # Temperature shift value
    dH2O = 999.016  # Water density in kg/m³
    corrCTL = 0
    corrCPL = 0
    try:

        print(" Datos recibidos en Flask:", data)  # ✅ Depuración
        n_sim = int(float(data.get('nsim', 0)))
        # tipoMet = data.get('tipoMet')
        API = float(data.get('API', 0))
        product = data.get('product', 'Crude Oil')
        Tl = float(data.get('Tl', 0))
        Pl = float(data.get('Pl', 0))
        Pe = float(data.get('Pe', 0))
        MR = float(data.get('MR', 0))
        KF = float(data.get('KF', 0))
        MF = float(data.get('MF', 0))
        SW = float(data.get('SW', 0) or 0)/100

        # --------Entradas de incertidumbre---------
        # -------------Temperatura-----------
        resTl = float(data.get('resTl', 0))
        errorTl = float(data.get('errorTl', 0))
        ucalTL = float(data.get('ucalTl', 0))
        kcalTL = float(data.get('kcalTl', 0))
        uderTL = float(data.get('uderTl', 0))
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
        FW = float(data.get('FW', 0))
        uFW = float(data.get('uFW', 0))
        # -------------densidad-----------
        metdl = data.get('metdl', 'externo')
        uTdl = float(data.get('uTdl', 0))
        kTdl = float(data.get('kdl', 0))
        # -------------volumen-----------
        uTOV = float(data.get('uTOV', 0))
        ucalMet = float(data.get('ucalMet', 0))
        kcalMet = float(data.get('kcalMet', 0))
        ecalMet = float(data.get('ecalMet', 0))
        conditioner = data.get('conditioner', 'sin_acond')
        uplong = float(data.get('upLong', '0'))
        dwlong = float(data.get('dwLong', '0'))
        twlong = float(data.get('twLong', '0'))

        # ----Asignar distribuciones--------
        # ------------densidad--------------
        if metdl == "directo":
            # Desviación en la medición de viscosidad en la medición directa
            desvdl = 2/math.sqrt(3)
            ucaldl = uTdl/kTdl
            desvsample = 0
            simul_API = u_magntiud(
                n_sim, API, ucaldl, "normal", desvdl, "uniforme", desvsample, "uniforme")

        elif metdl == "externo":
            desvdl = 0
            ucaldl = uTdl/kTdl
            desvsample = 0
            simul_API = u_magntiud(
                n_sim, API, ucaldl, "normal", desvdl, "uniforme", desvsample, "uniforme")

        print(simul_API)
        # ------------temperatura--------------
        ucalTl = ucalTL/kcalTL
        uresTl = resTl/2
        uerrorTl = errorTl
        simul_Tl = u_magntiud(n_sim, Tl, ucalTl, "normal", uresTl,
                              "uniforme", uerrorTl, "uniforme", uderTL, "uniforme")

        # ------------presión--------------
        ucalPl = ucalPL/kcalPL
        uresPl = resPl/2
        uerrorPl = errorPl
        simul_Pl = u_magntiud(n_sim, Pl, ucalPl, "normal", uresPl,
                              "uniforme", uerrorPl, "uniforme", uderPL, "uniforme")

        print(simul_Pl)

        # ------------volumen--------------

        simul_VL = u_magntiud(n_sim, uTOV, "normal", uTOV/2,
                              "uniforme", uFW, "uniforme", uplong, "uniforme")
        Vl = MR
        # ucalMet esta en unidades relativa (%) de volumen
        ucalV = ucalMet/kcalMet*(Vl/100)
        uresV = 0
        uerrorV = ecalMet*(Vl/100)
        uinstV = InstalLiqDin(tipoMet, conditioner, uplong)*MR/100
        uoperV = 0
        simul_MR = u_magntiud(n_sim, MR, ucalV, "normal", uerrorV,
                              "uniforme", "uniforme", "uniforme")

        print(simul_MR)

        # ------------%SW--------------
        if metSW == "directo":
            ddesvsw = 0.05  # Desviación en la medición de viscosidad en la medición directa
            ucalsed = uTSed/kSed
            ucalw = 0
            desvsample = 0
            simul_dl = u_magntiud(n_sim, SW, ucalsed, "normal", ucalw,
                                  "normal", desvsw, "uniforme", desvsample, "uniforme")

        elif metSW == "externo":
            desvsw = 0
            ucalsed = uTSed/kSed
            ucalw = uTW/kTW
            desvsample = 0
            simul_sw = u_magntiud(n_sim, SW, ucalsed, "normal", ucalw,
                                  "normal", desvsw, "uniforme", desvsample, "uniforme")

        print(simul_sw)

        # Calculo de la densidad en kg/m3
        dl_value = calcular_densidad(API, dH2O)
        print("✅ densidad calculada correctamente")

        print(dl_value)

        dl_value1 = calcular_densidad(API, dH2O)
        print("✅ densidad calculada correctamente")

        # Constantes
        K0, K1, K2 = Constants(product, dl_value, simul_Tl)
        print("✅ constantes calculada correctamente")

        # CTL
        Bl_value = K0 / (dl_value ** 2) + K1 / dl_value + K2

        CTL_value = calcular_CTL(product, Bl_value, simul_Tl)
        print(CTL_value)

        # CPL
        F_value = np.exp(-1.9947 + 0.00013427 * simul_Tl + 0.79392 /
                         (dl_value / 1000) ** 2 + 0.002326 * simul_Tl / (dl_value / 1000) ** 2)
        CPL_value = calcular_CPL(product, simul_Pl, Pe, simul_Tl, dl_value)
        print(CPL_value)

        # CSW
        CSW_value = CSW(simul_sw)
        # GSV
        GSV_value = GSV(simul_MR, KF, MF, CTL_value,
                        CPL_value, CSW_value, corrCTL, corrCPL)

        print(f"✅ GSV calculado: {GSV_value}")

        print(f"✅ GSV convertido a float correctamente")

        return {
            "GSV": np.round(GSV_value, 4),
            "CTL": np.round(CTL_value, 4),
            "CPL": np.round(CPL_value, 4),
            "dl": np.round(dl_value, 4),
            "NSV": GSV_value

        }

    except Exception as e:
        return {"error": str(e)}
