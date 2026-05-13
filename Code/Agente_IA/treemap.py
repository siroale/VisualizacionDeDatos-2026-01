"""
Visualización 5 — Treemap
Vista consolidada: discrepancia entre percepción (encuesta) y realidad (dataset).
Visualización Grupal con IA Generativa.
Fuentes: Encuesta propia (2026) + Kaggle Suicide Rates Overview 1985-2016
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import squarify
import numpy as np
import os
from matplotlib.colors import LinearSegmentedColormap

BASE = os.path.dirname(os.path.abspath(__file__))
SURVEY_PATH = os.path.join(BASE, '..', '..', 'Datasets',
    'Percepciones sobre Tasas de Suicidio_ Mitos vs. Realidad (Respuestas) - Respuestas de formulario 1.csv')
DATASET_PATH = os.path.join(BASE, '..', '..', 'Datasets', 'suicide_dataset.csv')
OUTPUT_PATH  = os.path.join(BASE, '..', '..', 'Informe_2', 'figures', 'vis5_treemap.png')

BG_COLOR = '#FAFAFA'
TEXT_COLOR = '#1a1a2e'

survey = pd.read_csv(SURVEY_PATH)
df = pd.read_csv(DATASET_PATH)

# ═══════════════════════════════════════════════════════════════════════
# PREGUNTA 1: Relación riqueza - suicidio
# ═══════════════════════════════════════════════════════════════════════
col_alto = [c for c in survey.columns if 'Alto' in c][0]
df['gdp_tercile'] = pd.qcut(df['gdp_per_capita ($)'], 3, labels=['Bajo', 'Medio', 'Alto'])
real_rates_gdp = df.groupby('gdp_tercile')['suicides/100k pop'].mean()
p1_pct_correct = (survey[col_alto] == 'Mayor Tasa de Suicidio').sum() / len(survey) * 100

# ═══════════════════════════════════════════════════════════════════════
# PREGUNTA 2: Grupo etario más vulnerable
# ═══════════════════════════════════════════════════════════════════════
SURVEY_TO_DATASET = {
    'Adolescentes y Adultos Jóvenes (15-24 años)': '15-24 years',
    'Adultos (25-34 años)': '25-34 years',
    'Adultos de Mediana Edad (35-54 años)': '35-54 years',
    'Adultos Mayores (55-74 años)': '55-74 years',
    'Personas de la Tercera Edad (75+ años)': '75+ years',
    'Niños y Pre-adolescentes (5-14 años)': '5-14 years',
}

col_age = [c for c in survey.columns if 'grupos de edad' in c.lower()][0]
real_age_rates = df.groupby('age')['suicides/100k pop'].mean()
real_top_age = real_age_rates.idxmax()

survey['age_mapped'] = survey[col_age].map(SURVEY_TO_DATASET)
p2_pct_correct = (survey['age_mapped'] == real_top_age).sum() / len(survey) * 100

# ═══════════════════════════════════════════════════════════════════════
# PREGUNTA 3: Porcentaje femenino
# ═══════════════════════════════════════════════════════════════════════
col_pct = [c for c in survey.columns if 'porcentaje' in c.lower() or 'mujeres' in c.lower()][0]
total_by_sex = df.groupby('sex')['suicides_no'].sum()
real_female_pct = total_by_sex['female'] / total_by_sex.sum() * 100

survey_estimates = survey[col_pct].astype(float) * 10
p3_pct_correct = ((survey_estimates >= real_female_pct - 10) &
                  (survey_estimates <= real_female_pct + 10)).sum() / len(survey) * 100

# ═══════════════════════════════════════════════════════════════════════
# PREGUNTA 4: Tendencia temporal
# ═══════════════════════════════════════════════════════════════════════
col_trend = [c for c in survey.columns if 'décadas' in c.lower() or 'cambio' in c.lower()][0]
df['decade'] = (df['year'] // 10) * 10
decade_rates = df.groupby('decade')['suicides/100k pop'].mean()
first_rate = decade_rates.iloc[0]
last_rate = decade_rates.iloc[-1]
pct_change = ((last_rate - first_rate) / first_rate) * 100
real_trend = 'Han Disminuido Ligeramente' if pct_change < -5 else 'Se Han Mantenido Estables'
p4_pct_correct = (survey[col_trend] == real_trend).sum() / len(survey) * 100

# ═══════════════════════════════════════════════════════════════════════
# CONSTRUIR TREEMAP
# ═══════════════════════════════════════════════════════════════════════
questions = [
    'P1: Riqueza\nvs Suicidio',
    'P2: Grupo\nEtario',
    'P3: % Mujeres\nen Suicidios',
    'P4: Tendencia\nTemporal',
]

pct_correct = [p1_pct_correct, p2_pct_correct, p3_pct_correct, p4_pct_correct]
n_resp = len(survey)
sizes = [n_resp] * 4

def pct_to_color(pct):
    if pct < 50:
        r = 0.84
        g = 0.15 + (pct / 50) * 0.45
        b = 0.24 - (pct / 50) * 0.05
    else:
        r = 0.84 - ((pct - 50) / 50) * 0.75
        g = 0.60 + ((pct - 50) / 50) * 0.14
        b = 0.19 + ((pct - 50) / 50) * 0.55
    return (r, g, b)

colors = [pct_to_color(p) for p in pct_correct]

fig, ax = plt.subplots(figsize=(14, 9))
fig.patch.set_facecolor(BG_COLOR)
ax.set_facecolor(BG_COLOR)

squarify.plot(sizes=sizes, label=None, color=colors, alpha=0.85,
              ax=ax, edgecolor=BG_COLOR, linewidth=4)

normed = squarify.normalize_sizes(sizes, 100, 100)
padded = squarify.padded_squarify(normed, 0, 0, 100, 100)

for i, (rect_data, q, pct) in enumerate(zip(padded, questions, pct_correct)):
    x = rect_data['x'] + rect_data['dx'] / 2
    y = rect_data['y'] + rect_data['dy'] / 2

    ax.text(x, y + 5, q, ha='center', va='center', fontsize=14,
            fontweight='bold', color='white')
    ax.text(x, y - 5, f'{pct:.0f}% acertó', ha='center', va='center',
            fontsize=18, fontweight='bold', color='white',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='black', alpha=0.35))

    if i == 0:
        detail = f'Real: PIB alto = mayor tasa\n({real_rates_gdp["Alto"]:.1f}/100k)'
    elif i == 1:
        detail = f'Real: {real_top_age} mayor tasa\n({real_age_rates[real_top_age]:.1f}/100k)'
    elif i == 2:
        detail = f'Real: {real_female_pct:.1f}% mujeres'
    else:
        detail = f'Real: cambio de {pct_change:+.1f}%\nentre décadas'

    ax.text(x, y - 15, detail, ha='center', va='center', fontsize=9,
            color='white', fontstyle='italic', alpha=0.9)

ax.axis('off')

ax.set_title('Mitos vs. Realidad: ¿Qué tanto acierta la gente?\nDiscrepancia entre percepción y datos reales por pregunta',
             fontsize=20, fontweight='bold', color=TEXT_COLOR, pad=25)

gradient_ax = fig.add_axes([0.15, 0.02, 0.7, 0.025])
gradient = np.linspace(0, 100, 256).reshape(1, -1)
cmap_custom = LinearSegmentedColormap.from_list('accuracy',
    [pct_to_color(0), pct_to_color(50), pct_to_color(100)])
gradient_ax.imshow(gradient, aspect='auto', cmap=cmap_custom, extent=[0, 100, 0, 1])
gradient_ax.set_xlim(0, 100)
gradient_ax.set_xticks([0, 25, 50, 75, 100])
gradient_ax.set_xticklabels(['0%', '25%', '50%', '75%', '100%'],
                            fontsize=9, color=TEXT_COLOR)
gradient_ax.set_yticks([])
gradient_ax.set_xlabel('Porcentaje de encuestados que acertaron',
                       fontsize=10, color=TEXT_COLOR)
gradient_ax.tick_params(colors=TEXT_COLOR)
for spine in gradient_ax.spines.values():
    spine.set_color('#CCCCCC')

fig.text(0.5, -0.06,
         'Fuentes: Encuesta propia (2026) + Kaggle Suicide Rates Overview 1985-2016',
         ha='center', fontsize=9, color='#888888')

plt.savefig(OUTPUT_PATH, dpi=200, bbox_inches='tight', facecolor=BG_COLOR)
plt.close()
print(f'Guardado en: {OUTPUT_PATH}')
