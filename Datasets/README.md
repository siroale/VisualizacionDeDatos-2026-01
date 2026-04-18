# Fuente de Datos: Tasas de Suicidio y Factores Socioeconómicos Globales (1985 - 2016)

## Origen
* **Plataforma:** [Kaggle - Suicide Rates Overview 1985 to 2016](https://www.kaggle.com/datasets/russellyates88/suicide-rates-overview-1985-to-2016)
* **Autores/Recopiladores Originales:** Este dataset es un compilado estructurado (mashup) construido a partir de cuatro fuentes globales oficiales: el Programa de las Naciones Unidas para el Desarrollo (UN), el Banco Mundial (World Bank), la Organización Mundial de la Salud (OMS) y la base de datos de Szamil sobre suicidios en el siglo XXI.

## Descripción
Este conjunto de datos ofrece una visión multidimensional de las tasas de mortalidad por suicidio a nivel global durante un período de más de tres décadas (1985-2016). Su objetivo principal es permitir la evaluación y búsqueda de correlaciones entre la mortalidad autoinfligida y diversos factores socioeconómicos y demográficos a lo largo del tiempo. 

El archivo `.csv` contiene registros que cruzan la cantidad de defunciones con indicadores macroeconómicos y poblacionales, lo que permite un análisis profundo de cómo el entorno material y la época de nacimiento influyen en la salud mental y la mortalidad.

## Estructura de las Variables Principales
* **Demográficas:** País, año, sexo, grupo de edad (ej. 15-24 años, 75+ años) y generación de pertenencia (ej. Boomers, Gen X, Millennials).
* **Mortalidad:** Número absoluto de suicidios (`suicides_no`), población total del grupo (`population`), y la métrica estandarizada de suicidios por cada 100,000 habitantes.
* **Socioeconómicas:** Índice de Desarrollo Humano del año respectivo (`HDI for year`), Producto Interno Bruto anual del país (`gdp_for_year`), y PIB per cápita (`gdp_per_capita`).
