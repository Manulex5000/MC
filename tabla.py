import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# -------------------- Parámetros Fijos --------------------

Vcrudo = 12.50375  # bbl/día
errorVcrudo = 64.9298  # %
UVcrudo = 0.5  # %
k = 2  # factor de cobertura
driftVcrudo = 0  # %

u_UVcrudo = (UVcrudo / 100 * Vcrudo) / k
u_errorVcrudo = (errorVcrudo / 100 * Vcrudo)
u_driftVcrudo = (driftVcrudo / 100 * Vcrudo)

# -------------------- Configuración --------------------

nsim_list = [10**3, 10**4, 2*10**4, 3*10**4,4*10**4,5*10**4, 7*10**4, 10**5, 2*10**5, 10**6]
n_repeticiones = 20
tolerancia = 0.05  # bbl/día

resultados = {}

# -------------------- Simulaciones --------------------

for nsim in nsim_list:
    medias = []
    
    for _ in range(n_repeticiones):
        usim_UVcrudo = np.random.normal(0, u_UVcrudo, nsim)
        usim_errorVcrudo = np.random.uniform(-u_errorVcrudo, u_errorVcrudo, nsim)
        usim_driftVcrudo = np.random.uniform(-u_driftVcrudo, u_driftVcrudo, nsim)

        Vcrudo_sim = Vcrudo + usim_UVcrudo + usim_errorVcrudo + usim_driftVcrudo
        medias.append(np.mean(Vcrudo_sim))

    resultados[nsim] = np.array(medias)

# -------------------- Crear tabla de resultados --------------------

tabla = []

for nsim in nsim_list:
    medias_nsim = resultados[nsim]
    media_global = np.mean(medias_nsim)
    std_medias = np.std(medias_nsim, ddof=1)
    dos_sigma = 2 * std_medias
    cumple = "✅" if dos_sigma < tolerancia else "❌"

    tabla.append({
        'Número de iteraciones (M)': f'{nsim:,}',
        'Media global [bbl/día]': round(media_global, 6),
        'Desviación estándar de las medias [bbl/día]': round(std_medias, 6),
        '2×STD [bbl/día]': round(dos_sigma, 6),
        '¿Cumple 2×STD < d?': cumple
    })

# Convertir a DataFrame
df_resultados = pd.DataFrame(tabla)

# Mostrar la tabla
print("\n--- Tabla resumen de resultados ---\n")
print(df_resultados.to_string(index=False))

# -------------------- Gráfica de evolución de 2×STD --------------------

plt.figure(figsize=(10, 6))
M_values = np.array([int(m.replace(',', '')) for m in df_resultados['Número de iteraciones (M)']])
dos_sigma_values = df_resultados['2×STD [bbl/día]']

plt.plot(M_values, dos_sigma_values, marker='o', linestyle='-')
plt.axhline(y=tolerancia, color='red', linestyle='--', label=f'Tolerancia d = {tolerancia}')
plt.xscale('log')
plt.xlabel('Número de iteraciones (M)')
plt.ylabel('2×STD de las medias [bbl/día]')
plt.title('Evolución de 2×STD según el número de iteraciones')
plt.grid(True, which="both", ls="--")
plt.legend()
plt.tight_layout()
plt.show()