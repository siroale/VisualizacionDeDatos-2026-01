# Criterio E -- Visualizacion Grupal

## Grafico seleccionado: Ridgeline Plot (Joy Plot)

**Variable independiente:** PIB per capita (GDP per capita), segmentado en quintiles.
**Variable dependiente:** Tasa promedio de suicidio por pais (suicides/100k pop).

---

## Resumen estadistico por quintil

| Quintil | Paises | Mediana | Media | Desv. Std |
|---|---|---|---|---|
| Q1 - Ingreso bajo | 20 | 6.61 | 10.32 | 9.97 |
| Q2 - Ingreso medio-bajo | 20 | 8.58 | 11.40 | 7.91 |
| Q3 - Ingreso medio | 19 | 12.57 | 15.56 | 12.05 |
| Q4 - Ingreso medio-alto | 20 | 9.47 | 10.48 | 7.78 |
| Q5 - Ingreso alto | 20 | 13.96 | 13.75 | 6.33 |

---

## Justificacion metodologica

El **Ridgeline Plot** (tambien conocido como Joy Plot) fue seleccionado como visualizacion de cierre del informe por las siguientes razones:

1. **Capacidad distributiva, no puntual.** A diferencia de un grafico de dispersion --que reduce cada pais a un punto--, el ridgeline revela la *forma completa de la distribucion* de tasas de suicidio dentro de cada estrato economico. Esto permite identificar asimetrias, bimodalidades y colas pesadas que un indicador de tendencia central ocultaria.

2. **Lectura comparativa inmediata.** Al apilar las curvas de densidad KDE (Kernel Density Estimation) en un eje vertical ordenado por nivel de ingreso, el lector puede comparar simultaneamente cinco distribuciones sin recurrir a facetas separadas. La superposicion controlada (overlap) genera una narrativa visual de "escalera" que invita a recorrer los estratos de menor a mayor ingreso.

3. **Complementariedad con los criterios anteriores.** Los criterios A-D analizan la dimension temporal (evolucion, cohortes etarias), la brecha de genero y la variacion entre paises. El Criterio E introduce una dimension socioeconomica transversal que cierra el arco narrativo del informe: tras documentar *cuanto*, *cuando*, *quien* y *donde*, este criterio responde al *por que estructural* vinculando las tasas a las condiciones materiales de desarrollo.

4. **Estetica no convencional.** El ridgeline plot no pertenece a las familias de graficos de uso comun (barras, lineas, dispersion, torta) ni repite los tipos ya empleados en el informe. Su popularizacion reciente en periodismo de datos (inspirado en la portada del album *Unknown Pleasures* de Joy Division, 1979) lo convierte en un recurso visualmente impactante y academicamente riguroso.

5. **Metodo estadistico subyacente.** Se utilizo estimacion de densidad por kernel (KDE) gaussiano con ancho de banda ajustado (bw=0.35) para suavizar las distribuciones sin perder la senal de los datos. Las medianas anotadas sobre cada curva permiten una lectura cuantitativa rapida.

---

## Conclusiones periodisticas

### Conclusion 1: La riqueza no protege -- los paises de ingreso alto lideran en tasas de suicidio

> Contrario a la intuicion de que el desarrollo economico mejora todos los indicadores de bienestar, los paises del quintil mas alto de PIB per capita (Q5) registran la mediana de suicidio mas elevada del dataset: **14.0 por cada 100,000 habitantes**. Esta cifra duplica la mediana de los paises de ingreso bajo (Q1 = 6.6). El hallazgo sugiere que las sociedades de alto ingreso enfrentan factores de riesgo propios --aislamiento social, presion competitiva, acceso a medios letales-- que contrarrestan los beneficios materiales del desarrollo.

### Conclusion 2: Los paises de ingreso bajo son los mas desiguales entre si

> El estrato Q1 presenta la cola derecha mas extensa de todas las distribuciones, con una desviacion estandar de **9.97** --la mas alta del analisis-- y una divergencia significativa entre su mediana (6.61) y su media (10.32). Esto revela que, si bien la mayoria de los paises pobres tiene tasas moderadas, un subgrupo experimenta incidencias extremadamente altas. La pobreza no es un factor protector uniforme: las condiciones geopoliticas, los conflictos armados y la ausencia de sistemas de salud mental generan realidades radicalmente distintas dentro del mismo estrato economico.

### Conclusion 3: El ingreso medio-alto exhibe un efecto protector relativo (la "paradoja del Q4")

> El quintil Q4 (ingreso medio-alto) muestra la distribucion mas compacta y centrada, con la menor desviacion estandar (**7.78**) y una mediana de **9.5** --inferior a la de los quintiles Q3 y Q5 que lo flanquean. Este patron, que rompe la secuencia lineal esperada entre riqueza y suicidio, sugiere que los paises en transicion economica avanzada --con servicios de salud en expansion pero sin las patologias sociales de las economias plenamente industrializadas-- representan un "punto optimo" relativo en la prevencion del suicidio. Este hallazgo respalda la hipotesis de que la relacion entre desarrollo y suicidio no es lineal sino curvilinea (forma de U invertida parcial).
