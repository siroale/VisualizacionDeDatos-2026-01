"""
Visualización 2 — Radar Chart
Percepción riqueza vs tasa de suicidio (encuesta) vs realidad (dataset).
Integrante: Alexis Mellis
Fuentes: Encuesta propia (2026) + Kaggle Suicide Rates Overview 1985-2016
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

BASE = os.path.dirname(os.path.abspath(__file__))
SURVEY_PATH = os.path.join(BASE, '..', '..', 'Datasets',
    'Percepciones sobre Tasas de Suicidio_ Mitos vs. Realidad (Respuestas) - Respuestas de formulario 1.csv')
DATASET_PATH = os.path.join(BASE, '..', '..', 'Datasets', 'suicide_dataset.csv')
OUTPUT_PATH  = os.path.join(BASE, '..', '..', 'Informe_2', 'figures', 'vis2_radar.png')

BG_COLOR = '#FAFAFA'
TEXT_COLOR = '#1a1a2e'

survey = pd.read_csv(SURVEY_PATH)
col_alto = [c for c in survey.columns if 'Alto' in c or 'alto' in c][0]
col_medio = [c for c in survey.columns if 'Medio' in c or 'medio' in c][0]
col_bajo = [c for c in survey.columns if 'Bajo' in c or 'bajo' in c][0]

RATE_MAP = {
    'Menor Tasa de Suicidio': 1,
    'Tasa de Suicidio Media': 2,
    'Mayor Tasa de Suicidio': 3,
}

survey_alto  = survey[col_alto].map(RATE_MAP).mean()
survey_medio = survey[col_medio].map(RATE_MAP).mean()
survey_bajo  = survey[col_bajo].map(RATE_MAP).mean()

survey_vals = np.array([survey_alto, survey_medio, survey_bajo])
survey_norm = (survey_vals - 1) / 2

df = pd.read_csv(DATASET_PATH)
df['gdp_tercile'] = pd.qcut(df['gdp_per_capita ($)'], 3, labels=['Bajo', 'Medio', 'Alto'])
real_rates = df.groupby('gdp_tercile')['suicides/100k pop'].mean()
real_vals = np.array([real_rates['Alto'], real_rates['Medio'], real_rates['Bajo']])
real_norm = (real_vals - real_vals.min()) / (real_vals.max() - real_vals.min())

categories = ['Nivel Económico\nAlto', 'Nivel Económico\nMedio', 'Nivel Económico\nBajo']
N = len(categories)
angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
angles += angles[:1]
survey_plot = survey_norm.tolist() + [survey_norm[0]]
real_plot   = real_norm.tolist()   + [real_norm[0]]

fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))
fig.patch.set_facecolor(BG_COLOR)
ax.set_facecolor(BG_COLOR)

ax.set_rlabel_position(0)
ax.yaxis.set_tick_params(labelsize=0)
ax.set_ylim(0, 1.1)

ax.fill(angles, survey_plot, alpha=0.25, color='#D7263D', label='Percepción (Encuesta)')
ax.plot(angles, survey_plot, color='#D7263D', linewidth=2.5, linestyle='-', marker='o', markersize=10)

ax.fill(angles, real_plot, alpha=0.25, color='#17BEBB', label='Realidad (Dataset)')
ax.plot(angles, real_plot, color='#17BEBB', linewidth=2.5, linestyle='-', marker='s', markersize=10)

ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, fontsize=13, fontweight='bold', color=TEXT_COLOR)

ax.spines['polar'].set_color('#CCCCCC')
ax.grid(color='#CCCCCC', linewidth=0.5, alpha=0.7)
ax.tick_params(axis='x', colors=TEXT_COLOR)

for i, (sv, rv) in enumerate(zip(survey_norm, real_norm)):
    angle = angles[i]
    real_rate_val = real_vals[i]
    ax.annotate(f'{real_rate_val:.1f}/100k',
                xy=(angle, rv), xytext=(10, 10),
                textcoords='offset points',
                fontsize=10, color='#0E8A87', fontweight='bold')

ax.set_title('Percepción vs Realidad:\nTasa de Suicidio según Nivel Económico',
             fontsize=18, fontweight='bold', color=TEXT_COLOR, pad=30)

legend = ax.legend(loc='lower right', bbox_to_anchor=(1.3, -0.05),
                   fontsize=12, frameon=True, facecolor='white',
                   edgecolor='#CCCCCC', labelcolor=TEXT_COLOR)

fig.text(0.5, 0.02,
         f'Tasas reales promedio — Alto: {real_vals[0]:.1f} | Medio: {real_vals[1]:.1f} | Bajo: {real_vals[2]:.1f} (por 100k hab.)',
         ha='center', fontsize=11, color='#555555', fontstyle='italic')

fig.text(0.5, -0.01,
         'Fuentes: Encuesta propia (2026) + Kaggle Suicide Rates Overview 1985-2016',
         ha='center', fontsize=9, color='#888888')

plt.tight_layout()
plt.savefig(OUTPUT_PATH, dpi=200, bbox_inches='tight', facecolor=BG_COLOR)
plt.close()
print(f'Guardado en: {OUTPUT_PATH}')
