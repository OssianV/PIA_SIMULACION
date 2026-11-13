
# ==========================================================
# MODULO 3: TEST DE ESTRES ESTOCASTICO MEDIANTE GBM
# ==========================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas_market_calendars as mcal

from pathlib import Path

# ==========================================================
# 1. CONFIGURACION
# ==========================================================

NUM_PATHS = 500
TRADING_DAYS = 252
RANDOM_SEED = 42

START_DATE = "2026-01-01"
END_DATE = "2026-12-31"

OUTPUT_DIR = Path("data")
OUTPUT_DIR.mkdir(exist_ok=True)

np.random.seed(RANDOM_SEED)

# ==========================================================
# 2. CARGAR DATOS HISTORICOS
# ==========================================================

print("\nCargando rendimientos historicos...")

daily_returns = pd.read_csv(
    OUTPUT_DIR / "daily_returns.csv",
    index_col=0,
    parse_dates=True
)

# ==========================================================
# 3. CARGAR PORTAFOLIOS SELECCIONADOS
# ==========================================================

print("\nCargando portafolios seleccionados...")

selected = pd.read_csv(
    OUTPUT_DIR / "selected_portfolios.csv"
)

# Nos quedamos solamente con los tres criterios solicitados

portfolio_types = {
    "Maximo_Sharpe": "Maximo Sharpe",
    "Minima_Varianza": "Minima varianza",
    "Maximo_Rendimiento": "Maximo retorno"
}

selected = selected[
    selected["Criterio"].isin(portfolio_types.keys())
].copy()

if len(selected) != 3:
    raise ValueError(
        "No se encontraron los tres portafolios requeridos."
    )

# ==========================================================
# 4. OBTENER CALENDARIO DE LA BOLSA DE NUEVA YORK
# ==========================================================

print("\nObteniendo calendario bursatil NYSE...")

nyse = mcal.get_calendar("NYSE")

schedule = nyse.schedule(
    start_date=START_DATE,
    end_date=END_DATE
)

trading_dates = schedule.index

if len(trading_dates) == 0:
    raise ValueError("No se encontraron fechas bursatiles.")

print("Sesiones bursatiles de 2026:", len(trading_dates))

# ==========================================================
# 5. PARAMETROS DEL GBM PARA CADA PORTAFOLIO
# ==========================================================

print("\nEstimando parametros del modelo GBM...")

portfolio_weights = [
    col for col in selected.columns
    if col.startswith("Weight_")
]

tickers = [
    col.replace("Weight_", "")
    for col in portfolio_weights
]

daily_returns = daily_returns[tickers]

all_paths = []

# ==========================================================
# 6. SIMULAR TRAYECTORIAS
# ==========================================================

for _, portfolio in selected.iterrows():

    criterion = portfolio["Criterio"]

    portfolio_name = portfolio_types[criterion]

    print(f"\nSimulando: {portfolio_name}")

    # Recuperar los pesos del portafolio

    weights = portfolio[portfolio_weights].to_numpy(
        dtype=float
    )

    # Convertir porcentajes a fracciones si fuera necesario
    # El archivo Markowitz recomendado guarda pesos en porcentaje.

    if weights.sum() > 1.01:
        weights = weights / 100

    if not np.isclose(weights.sum(), 1.0, atol=1e-5):
        raise ValueError(
            f"Los pesos de {portfolio_name} no suman 100%."
        )

    # Calcular rendimientos diarios del portafolio

    portfolio_returns = (
        daily_returns.to_numpy() @ weights
    )

    # Parámetros históricos

    mu = portfolio_returns.mean() * TRADING_DAYS

    sigma = (
        portfolio_returns.std(ddof=1)
        * np.sqrt(TRADING_DAYS)
    )

    print(f"Rendimiento anual: {mu:.4%}")
    print(f"Volatilidad anual: {sigma:.4%}")

    # ======================================================
    # 7. GENERAR 500 TRAYECTORIAS
    # ======================================================

    dt = 1 / TRADING_DAYS

    drift = (mu - 0.5 * sigma**2) * dt

    diffusion = sigma * np.sqrt(dt)

    # Generar variables normales aleatorias
    # Dimensiones: 500 trayectorias x dias bursatiles

    Z = np.random.standard_normal(
        size=(NUM_PATHS, len(trading_dates))
    )

    # Calcular rendimientos logaritmicos simulados

    log_returns = drift + diffusion * Z

    # Acumular rendimientos para obtener precios
    # El valor inicial del dia cero es 1.0

    paths = np.exp(
        np.cumsum(log_returns, axis=1)
    )

    # ======================================================
    # 8. CONSTRUIR DATAFRAME DE RESULTADOS
    # ======================================================

    path_df = pd.DataFrame(
        paths,
        columns=trading_dates
    )

    path_df["Path_ID"] = np.arange(
        1, NUM_PATHS + 1
    )

    # Formato largo: una fila por trayectoria y fecha

    path_df = path_df.melt(
        id_vars="Path_ID",
        var_name="Fecha",
        value_name="Valor_portafolio"
    )

    path_df["Tipo_portafolio"] = portfolio_name

    # Formato de fecha solicitado: mm/dd/yyyy

    path_df["Fecha"] = pd.to_datetime(
        path_df["Fecha"]
    ).dt.strftime("%m/%d/%Y")

    # Organizar columnas

    path_df = path_df[
        [
            "Tipo_portafolio",
            "Path_ID",
            "Fecha",
            "Valor_portafolio"
        ]
    ]

    all_paths.append(path_df)

# ==========================================================
# 9. UNIR LOS RESULTADOS DE LOS TRES PORTAFOLIOS
# ==========================================================

print("\nUniendo trayectorias...")

final_paths = pd.concat(
    all_paths,
    ignore_index=True
)

# ==========================================================
# 10. EXPORTAR OUTPUT 2
# ==========================================================

output_file = OUTPUT_DIR / "gbm_stress_test_paths.csv"

final_paths.to_csv(
    output_file,
    index=False,
    float_format="%.10f"
)

# ==========================================================
# 11. VALIDACIONES
# ==========================================================

print("\nValidando archivo de resultados...")

print("\nCantidad de filas:", len(final_paths))

print("\nTrayectorias por portafolio:")

print(
    final_paths.groupby(
        "Tipo_portafolio"
    )["Path_ID"].nunique()
)

print("\nFechas por portafolio:")

print(
    final_paths.groupby(
        "Tipo_portafolio"
    )["Fecha"].nunique()
)

print("\nValores faltantes:")

print(final_paths.isna().sum())

print("\nPrimeras observaciones:")

print(final_paths.head())

# ==========================================================
# 12. GRAFICAR FAN CHARTS
# ==========================================================

print("\nGenerando Fan Charts...")

for portfolio_name in portfolio_types.values():

    subset = final_paths[
        final_paths["Tipo_portafolio"] == portfolio_name
    ].copy()

    subset["Fecha"] = pd.to_datetime(
        subset["Fecha"],
        format="%m/%d/%Y"
    )

    summary = subset.groupby("Fecha")[
        "Valor_portafolio"
    ].quantile(
        [0.05, 0.25, 0.50, 0.75, 0.95]
    ).unstack()

    plt.figure(figsize=(13, 7))

    plt.fill_between(
        summary.index,
        summary[0.05],
        summary[0.95],
        alpha=0.15,
        color="steelblue",
        label="Intervalo 5%-95%"
    )

    plt.fill_between(
        summary.index,
        summary[0.25],
        summary[0.75],
        alpha=0.30,
        color="steelblue",
        label="Intervalo 25%-75%"
    )

    plt.plot(
        summary.index,
        summary[0.50],
        color="darkblue",
        linewidth=2,
        label="Mediana"
    )

    plt.axhline(
        1.0,
        color="black",
        linestyle="--",
        alpha=0.6,
        label="Valor inicial"
    )

    plt.title(
        f"Fan Chart - {portfolio_name} - 2026"
    )

    plt.xlabel("Fecha")
    plt.ylabel("Valor del portafolio")

    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()

    filename = portfolio_name.replace(" ", "_")

    plt.savefig(
        OUTPUT_DIR / f"fan_chart_{filename}.png",
        dpi=300
    )

    plt.show()

# ==========================================================
# 13. FINALIZACION
# ==========================================================

print("\n======================================")
print("TEST DE ESTRES COMPLETADO")
print("======================================")

print("Archivo generado:")
print("gbm_stress_test_paths.csv")

print("Total de trayectorias:", NUM_PATHS * 3)

print("\nProceso finalizado correctamente.")
