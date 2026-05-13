"""
Visualización 4 — Nightingale / Coxcomb Rose Chart
Percepción del cambio temporal en tasas de suicidio vs realidad.
Integrante: Andrés Águila
Fuentes: Encuesta propia (2026) + Kaggle Suicide Rates Overview 1985-2016
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

BASE = os.path.dirname(os.path.abspath(__file__))
SURVEY_PATH = os.path.join(BASE, '..', '..', 'Datasets',
    'Percepciones sobre Tasas de Suicidio_ Mitos vs. Realidad (Respuestas) - Respuestas de formulario 1.csv')
DATASET_PATH = os.path.join(BASE, '..', '..', 'Datasets', 'suicide_dataset.csv')
OUTPUT_PATH  = os.path.join(BASE, '..', '..', 'Informe_2', 'figures', 'vis4_nightingale.png')

BG_COLOR = '#FAFAFA'
TEXT_COLOR = '#1a1a2e'

survey = pd.read_csv(SURVEY_PATH)
col_trend = [c for c in survey.columns if 'décadas' in c.lower() or 'cambio' in c.lower()][0]
perception_counts = survey[col_trend].value_counts()

CATEGORIES = [
    'Han Aumentado Significativamente',
    'Han Aumentado Ligeramente',
    'Se Han Mantenido Estables',
    'Han Disminuido Ligeramente',
    'Han Disminuido Significativamente',
]

for cat in CATEGORIES:
    if cat not in perception_counts.index:
        perception_counts[cat] = 0
perception_counts = perception_counts.reindex(CATEGORIES).fillna(0)

df = pd.read_csv(DATASET_PATH)
df['decade'] = (df['year'] // 10) * 10
decade_rates = df.groupby('decade')['suicides/100k pop'].mean()
first_decade_rate = decade_rates.iloc[0]
last_decade_rate = decade_rates.iloc[-1]
pct_change = ((last_decade_rate - first_decade_rate) / first_decade_rate) * 100

COLORS = {
    'Han Aumentado Significativamente': '#D7263D',
    'Han Aumentado Ligeramente':       '#F4A261',
    'Se Han Mantenido Estables':       '#999999',
    'Han Disminuido Ligeramente':      '#17BEBB',
    'Han Disminuido Significativamente': '#2A9D8F',
}

SHORT_LABELS = {
    'Han Aumentado Significativamente': 'Aumento\nSignificativo',
    'Han Aumentado Ligeramente':       'Aumento\nLigero',
    'Se Han Mantenido Estables':       'Se Mantienen\nEstables',
    'Han Disminuido Ligeramente':      'Disminución\nLigera',
    'Han Disminuido Significativamente': 'Disminución\nSignificativa',
}

fig, ax = plt.subplots(figsize=(12, 12), subplot_kw=dict(polar=True))
fig.patch.set_facecolor(BG_COLOR)
ax.set_facecolor(BG_COLOR)

N = len(CATEGORIES)
angles = np.linspace(0, 2 * np.pi, N, endpoint=False)
width = 2 * np.pi / N * 0.85

values = [perception_counts[cat] for cat in CATEGORIES]
colors = [COLORS[cat] for cat in CATEGORIES]
labels = [SHORT_LABELS[cat] for cat in CATEGORIES]

bars = ax.bar(angles, values, width=width, bottom=0,
              color=colors, edgecolor=BG_COLOR, linewidth=2, alpha=0.85)

for angle, val, label in zip(angles, values, labels):
    if val > 0:
        ax.text(angle, val + 0.5, f'{int(val)}',
                ha='center', va='bottom', fontsize=14, fontweight='bold',
                color=TEXT_COLOR)

ax.set_xticks(angles)
ax.set_xticklabels(labels, fontsize=10, color=TEXT_COLOR, fontweight='bold')

ax.set_ylim(0, max(values) + 2)
ax.yaxis.set_tick_params(labelsize=0)
ax.spines['polar'].set_color('#CCCCCC')
ax.grid(color='#CCCCCC', linewidth=0.5, alpha=0.5)

ax.set_title('¿Cómo perciben el cambio en las tasas\nde suicidio a lo largo de las décadas?',
             fontsize=18, fontweight='bold', color=TEXT_COLOR, pad=35)

reality_text = f'Realidad:\n{pct_change:+.1f}%\n({decade_rates.index[0]}s → {decade_rates.index[-1]}s)'
fig.text(0.82, 0.15, reality_text, ha='center', va='center', fontsize=12,
         fontweight='bold', color='#E76F51',
         bbox=dict(boxstyle='round,pad=0.5', facecolor='white',
                   edgecolor='#E76F51', alpha=0.95),
         transform=fig.transFigure)

decade_text = '  |  '.join([f'{int(d)}s: {r:.1f}/100k' for d, r in decade_rates.items()])
fig.text(0.5, 0.04,
         f'Tasa promedio por década: {decade_text}',
         ha='center', fontsize=9, color='#555555', fontstyle='italic')

fig.text(0.5, 0.01,
         'Fuentes: Encuesta propia (2026) + Kaggle Suicide Rates Overview 1985-2016',
         ha='center', fontsize=9, color='#888888')

plt.tight_layout(rect=[0, 0.06, 1, 1])
plt.savefig(OUTPUT_PATH, dpi=200, bbox_inches='tight', facecolor=BG_COLOR)
plt.close()
print(f'Guardado en: {OUTPUT_PATH}')
