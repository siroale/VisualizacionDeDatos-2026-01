# Fuente de Datos: Tasas de Suicidio y Factores Socioeconómicos Globales (1985 - 2021)

## Origen
* **Plataforma:** [Kaggle - Suicide Rates Overview (1985 to 2021)](https://www.kaggle.com/datasets/omkargowda/suicide-rates-overview-1985-to-2021)
* **Autores/Recopiladores Originales:** El compilado original fue estructurado por Russell Yates a partir de cuatro fuentes globales (ONU, Banco Mundial, OMS y Szamil). Esta versión actualizada fue extendida por Omkar Gowda para incluir los registros mundiales hasta el año 2021.

## Descripción
Este conjunto de datos ofrece una visión multidimensional de las tasas de mortalidad por suicidio a nivel global, abarcando un período extenso de más de tres décadas (1985-2021). Su objetivo principal es permitir la evaluación y búsqueda de correlaciones entre la mortalidad autoinfligida y diversos factores socioeconómicos y demográficos a lo largo del tiempo. 

Al incluir datos recientes hasta 2021, esta base resulta especialmente valiosa para analizar variaciones contemporáneas en la mortalidad, incluyendo el posible impacto en la salud mental global de eventos recientes como la pandemia de COVID-19. El archivo `.csv` cruza la cantidad de defunciones con indicadores macroeconómicos y poblacionales, permitiendo un análisis profundo de cómo el entorno material influye en la mortalidad.

## Estructura de las Variables Principales
* **Demográficas:** País, año, sexo, grupo de edad (ej. 15-24 años, 75+ años) y generación de pertenencia (ej. Boomers, Gen X, Millennials).
* **Mortalidad:** Número absoluto de suicidios (`suicides_no`), población total del grupo (`population`), y la métrica estandarizada de suicidios por cada 100,000 habitantes (`suicides/100k pop`), vital para permitir comparaciones justas entre países de distinto tamaño.
* **Socioeconómicas:** Índice de Desarrollo Humano del año respectivo (`HDI for year`), Producto Interno Bruto anual del país (`gdp_for_year`), y PIB per cápita (`gdp_per_capita`).

## Relevancia para el Tema Central ("Muerte")
Dentro del macro-tema de la mortalidad, este dataset nos permite explorar la **dimensión socioeconómica, histórica y demográfica**. La variedad de datos continuos y categóricos nos otorga la flexibilidad necesaria para desarrollar cruces de variables poco comunes, superando los análisis tradicionales y facilitando la creación de visualizaciones de alto impacto sobre un problema de salud pública global.