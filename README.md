# PIA_SIMULACION


## 📌 Proyecto Elegido: Simulacion de Monte-Carlo para obtener un portafolio optimo

Vamos a utilizar una simulacion de monte-carlo para obtener el portafolio optimo en base a una lista de acciones a considerar. Lo que obtendremos seran los pesos que cada accion debe tener en nuestro portafolio.

Usaremos una simulacion de Monte-Carlo en dos partes especificas: (1) obtener combinaciones aleatorias de pesos, y (2) simular la evolucion de los portafolios en un año. Por el momento, usaremos los precios de cierre ajustados del 2022 al 2024, y usaremos los precios de cierre del 2025 como "test". Falta determinar muchas cosas del proyecto, estas se listan en la seccion [Decisiones por Tomar](#Decisiones por Tomar).

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
