# PIA_SIMULACION

## 📌 Proyecto Elegido: Simulacion de Monte-Carlo para obtener un portafolio optimo + proyeccion de portafolios seleccionados

El proyecto consisitira en realizar una simulacion de Monte-Carlo para generar una lista de portafolios (generando aleatoriamente los pesos de cada activo), y aplicar metricas definidas para seleccionar el "mejor" portafolio. Usaremos 10 acciones del SYP100. Ademas, para los portafolios seleccionados, realizaremos varias proyecciones diaria de la evolucion de su rendimiento a lo largo de un año. Al final analizaremos los resultados, y acompañaremos el analisis con un dashboard en PowerBI.

### Entendiendo la simulacion

Para que quede claro que estamos haciendo podemos dividir el proyecto en 3. Aqui detallo cada una de las partes:

1. Simulacion estandar de Markowitz: Este es el corazon de la simulacion. Existen una infinidad de combinaciones de pesos para los 10 activos que tendra nuestra portafolio. Es computacionalmente imposible computar el rendimiento y riesgo de cada uno de dichas combinaciones. Es por esto que generaremos aletoriamente las combinaciones de pesos.

Para cada una de esas combinaciones, usaremos los datos historicos de precios ajustados al cierre para computar el rendimiento diario del portafolio. Posteriormente, computaremos el rendimiento esperado y el riesgo asociado al portafolio. Usando esto, calcularemos el ratio de sharpe y graficaremos la frontera eficiente de markowitz.

Por ultimo, en base a nuestros criterios de seleccion del "mejor" portafolio, seleccionaremos nuestro mejor portafolio para cada criterio.

2. Simulacion estocastica de mov. brow. geom. : Una vez obtenidos nuestros "mejores" portafolios, realizaremos una alta cantidad de proyecciones del precio diario de cada portafolio seleccionado a lo largo de un año (2026). Para cada portafolio haremos una grafica donde condensemos los resultados de todas las proyecciones, junto al historico real de este (pues tenemos precios de cierre hasta noviembre del 2026).

Esto se llama un test de estres, y como grafica podriamos hacer algo como esto:

[ejemplo_fan_chart](MISCELLANEOUS/png_jpg/)

3. Analisis: Esta parte es la que ira mas detallada en el documento final. Basicamente se reduce a analizar los resultados y el dashboard obtenido.

### Decisciones metodologicas por justificar

En el documento final necesitaremos argumentar bien las desiciones metodologicas tomadas para la elaboracion del proyecto. Aqui listo aquellas de las que soy conciente, puede no sean todas.

1. Indice ancla seleccionado.
2. Activos seleccionados.
3. Activo libre de riesgo seleccionado.
4. Periodo de datos historicos seleccionado.
5. Por que precios ajustados al cierre?
6. Periodo de proyeccion seleccionado.
7. Cantidad de pesos generados.
8. Supuestos asociados al modelo de markowitz estandar.
	- Como calcular el riesgo?
	- Como calcular el rendimiento esperado?
9. Supuestos asociados a la proyeccion de precios diarios
	- Cantidad de proyecciones por portafolio.
	- Supuestos asociados al mov. brow. geometrico (precios siguen log normal, rendimientos normal)
	- Por que normal y no t de student?
	- Desventajas de usar normal? (no contabiliza escenarios catastroficos)
	- Por que los resultados de la proyecicon de mbg deberian concordar con los del modelo de markowitz.
10. Stack tecnologico utilizado.

### Requisitos del codigo

Como se hara la visualizacion en PowerBI, sera necesario exportar los resultados de la simulacion hecha en Python a un archivo .csv. A continuacion detallo la estructura del output necesario para cada parte de la simulacion.

Output 1: Optimizacion estandar de markowitz

Este csv contiene los datos asociados a los 5000 portafolios generados.

- Nombre del archivo: markowitz_optimization_results.csv
- Columnas requeridas:
1. Portfolio_ID (Entero del 1 al 5000)
2. Retorno_anual_esperado (Float)
3. Riesgo_anual (Desviacion estandar, Float)
4. Ratio_de_sharpe (Float)
5. Weight_AAPL (Float, representing percentage)
6. Weight_MSFT (Float)
> ... (Repetir para los 10 activos)

Output 2: Test de estres estocastico

Este csv contiene los caminos dia a dia simulados para los portafolios optimos seleccionados

- Nombre del archivo: gbm_stress_test_paths.csv
- Columnas requeridas:
1. Tipo_portafolio (string: "Maximo Sharpe", "Minima varianza", "Maximo retorno")
2. Path_ID (Entero del 1 al 500)
3. Fecha (String: mm/dd/yyyy, solo para dias donde la bolsa de NY esta abierta en el 2026)
4. Valor_portafolio (Float, empezando en 1.0 en el dia 0)

Notese que como se seleccionaran 3 portafolios y hay 252 trading days en un ano, debera haber alreadedor de 756 filas.


# LEGACY - ESTO YA NO ES IMPORTANTE

## 1er Entregable

### Roles

Por el momento, se me ocurrio definir los roles de la siguiente manera:

Ossian: Desarrollo de visualizaciones (Dashboard)
Victoria: Fundamentos y analisis (Teoria de portafolios, supuestos, etc)
Meme: Fundamentos y analisis (Teoria de portafolios, supuestos, etc)
Jolette: Implementacion en codigo (Desarrollo del codigo de python)
Jimena: Implementacion en codigo (Desarrollo del codigo de python)

### 📝 Tareas por realizar

Semana 1: Fundamentos y Planificación
- Definición del problema (**VICTORIA**)
	- Uno o dos parrafos explicando que es lo que estamos haciendo: Que es un portafolio de inversiones? Por que es necesario optimizarlo? Cuales son los desafios iniciales de optimizarlo? Por que es necesario realizar una simulacion para hacerlo? etc.
- Justificación del sistema elegido (**VICTORIA**)
	- Uno o dos parrafos explicando por que usar simulacion montecarlo, etc.
- Objetivos del modelo (**MEME**)
	- Que buscamos obtener de la simulacion? Definir claramente qué se busca resolver o demostrar con esta simulación. Uno o dos parrafos.
- Identificación de variables, parámetros y supuestos (**MEME**)
	- El nombre lo dice claramente. Dos o tres parrafos.
- Tipo de simulación (discreta, continua, híbrida) (**VICTORIA**)
	- Un parrafo. Justificar por que una y no las otras.
- Cronograma y roles del equipo (**OSSIAN**)
	- Cronograma (Diagrama de Gantt)
	- Definicion de roles (a grandes rasgoz, que hara cada quien)
- Firma de integridad académica

Semana 2: Modelo Base y Programación
- Desarrollo del modelo conceptual (**OSSIAN**)
- Implementación inicial en Python u otro lenguaje (**JOLETTE**)
	- Script basico que genere lo mismo que [este proyecto](https://github.com/Gouldh/Monte-Carlo-Portfolio-Optimization). La diferencia es que no vas a simular los pesos, definiras una lista de unas 20 combinaciones diferentes de pesos y desarrollaras la simulacion. Nota que entonces no simularas el comportamiento del portafolio a lo largo del 2025. Generaras una grafica usando matplotlib para mostrar resultados.
- Estructura del sistema (eventos, estados, procesos) (**JIMENA**)
	- Aqui tenemos que identificar todas las caracteristicas de la simulacion que vimos en clase. 
- Documentación del código (**JOLETTE**)
	- El codigo que se genere tendra que estar documentado. Por el momento con que este bien comentado esta bien.
- Justificación del enfoque utilizado (**JIMENA**)
	- PENDIENTE (No se muy bien que pide)

A parte de las tareas previamente descritas, estan las decicione por tomar que siguen. Estas no se donde iran en el entregable 1, pero igual las tenemos que hacer.


## 🎯 Decisiones por Tomar


1. Selección de Activos (**MEME**)
	• Seleccionar 10 acciones iniciales basadas en el comportamiento del mercado del S&P 100.
	• Pendiente: Justificar técnicamente el criterio de selección de cada activo.
2. Criterio de Precios (**VICTORIA**)
	• Utilizar exclusivamente los precios de cierre de las acciones para la simulación.
	• Pendiente: Justificar por qué los precios de cierre son el estándar adecuado frente a otras métricas (apertura, máximos, mínimos).
3. Horizonte Temporal (**MEME**)
	• Usar el histórico de datos del periodo 2022 al 2024.
	• Pendiente: Justificar la elección de esta ventana de tiempo (ej. captura de volatilidad post-pandemia, tendencias de tasas de interés, etc.).
5. Métricas de Optimización (**OSSIAN**)
	• Pendiente: Determinar las métricas clave para evaluar el mejor portafolio (ej. Maximizar el Ratio de Sharpe, minimizar la volatilidad/riesgo, o buscar la Frontera Eficiente).
6. Contexto de Mercado (**MEME**)
	• Pendiente: Redactar el marco del entorno financiero actual tomando como referencia el S&P 100.
7. Modelo Matemático (**VICTORIA**)
	• Pendiente: Desarrollar la justificación teórica y práctica de por qué utilizar el Movimiento Browniano Geométrico (GBM) para modelar los precios.
8. Stack Tecnológico (**JIMENA**)
	• Pendiente: Justificar la arquitectura de herramientas elegida (¿Por qué Python para el backend/cálculo y Power BI para el frontend/visualización?).

## 📋 Tareas por Realizar

• Hacer el cronograma.
- Hacer el codigo de python (borrador).
- 

## 💡 Ideas Potenciales (Maybes)

• Perfiles de Inversión: Agregar una funcionalidad para que el usuario seleccione su perfil de riesgo (Aversión al riesgo, Neutral, Propenso al riesgo/Amante).

## 🛠️ Herramientas Utilizadas


## 🐍 Python

• Pandas: Procesamiento y manipulación de estructuras de datos.
• NumPy: Cálculos numéricos y operaciones matriciales eficientes.
• Matplotlib: Generación de gráficos estadísticos y de control internos.
• yfinance: Descarga de datos financieros históricos directamente de Yahoo Finance.

## 📊 Power BI

• Visualización: Creación de dashboards interactivos para la toma de decisiones y presentación del portafolio óptimo.

## Referencias

- Codigo de python de proyecto similar donde solo se simulan los pesos: https://github.com/Gouldh/Monte-Carlo-Portfolio-Optimization/blob/main/main.py
