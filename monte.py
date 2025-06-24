import numpy as np
import matplotlib.pyplot as plt
nsim = 20000  # número de simulaciones
Vcrudo = 8613  # [bbl/dia] Corresponde al mejor estimado del mensurando que corresponde al promedio artimetico de las mediciones realizadas ocn el MPFM dado bbl/dia
# [%] Corresponde al error porcentual obtenido durante la pruebas en campo donde se compara el MPFM con las  mediciones despues del separador de prueba (uasdo como referencia)
errorVcrudo = 64.9298
# [%] Corresponde a la icertidumbre asociada al valor de medida del crudo obtenida en el sistema de medición usado como referencia (que corresponde a la medición despues de seaprador de prueba)
UVcrudo = 0.5
k = 2  # Es el factor de cobertura reportado por el reporte de incertidumbre del valor de medida del crudo obtenida en el sistema de medición usado como referencia
# [%] Corresponde a la variaciones en la medición de volumen que puede deberse a variaciones en las propiedades del fluido durante las mediciones en el tiempo
driftVcrudo = 0

# ---fuentes de incertidumbre----
u_UVcrudo = (UVcrudo / 100 * Vcrudo) / k
u_errorVcrudo = (errorVcrudo / 100 * Vcrudo)
u_driftVcrudo = (driftVcrudo / 100 * Vcrudo)

nsim_list = [20000, 30000, 40000, 50000, 65000, 100000,
             1000000]  # Diferentes números de simulaciones
n_repeticiones = 100  # Cuántas veces repetir cada nsim

# Guardar resultados
resultados = {}

for nsim in nsim_list:
    medias = []

    for _ in range(n_repeticiones):
        usim_UVcrudo = np.random.normal(0, u_UVcrudo, nsim)
        usim_errorVcrudo = np.random.uniform(-u_errorVcrudo,
                                             u_errorVcrudo, nsim)
        usim_driftVcrudo = np.random.uniform(-u_driftVcrudo,
                                             u_driftVcrudo, nsim)

        Vcrudo_sim = Vcrudo + usim_UVcrudo + usim_errorVcrudo + usim_driftVcrudo
        medias.append(np.mean(Vcrudo_sim))

    resultados[nsim] = np.array(medias)
    x_labels = []
x_positions = []
all_medias = []

p2_5 = []
p97_5 = []
x_central = []

for idx, nsim in enumerate(nsim_list):
    medias = resultados[nsim]
    x_labels.append(f'{nsim:,}')
    x_positions.extend([idx] * n_repeticiones)
    all_medias.extend(medias)

# -------------------- Gráfica de puntos --------------------

plt.figure(figsize=(10, 6))

# Graficar puntos individuales
plt.scatter(x_positions, all_medias, color='blue')

# Ajustes del gráfico
plt.xticks(ticks=range(len(nsim_list)), labels=x_labels)
plt.xlabel('Número de simulaciones (nsim)', fontsize=12)
plt.ylabel('Vcrudo promedio (bbl/día)', fontsize=12)
plt.title('Medias individuales de Vcrudo por número de simulaciones', fontsize=14)
plt.grid(True)
plt.tight_layout()
plt.show()

# -------------------- Cálculo de desviaciones estándar --------------------

print("\n--- Desviaciones estándar de las medias ---")
for nsim in nsim_list:
    std_medias = np.std(resultados[nsim], ddof=1)
    print(
        f"nsim = {nsim:,} → Desviación estándar de las medias: {std_medias:.6f} bbl/día")
