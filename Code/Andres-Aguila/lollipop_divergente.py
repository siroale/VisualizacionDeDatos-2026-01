"""
Visualización 3 — Lollipop Chart Divergente
Percepción del porcentaje femenino en suicidios vs realidad.
Integrante: Andrés Águila
Fuentes: Encuesta propia (2026) + Kaggle Suicide Rates Overview 1985-2016
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

BASE = os.path.dirname(os.path.abspath(__file__))
SURVEY_PATH = os.path.join(BASE, '..', 'Datasets',
    'Percepciones sobre Tasas de Suicidio_ Mitos vs. Realidad (Respuestas) - Respuestas de formulario 1.csv')
DATASET_PATH = os.path.join(BASE, '..', 'Datasets', 'suicide_dataset.csv')
OUTPUT_PATH  = os.path.join(BASE, 'tarea2_lollipop.png')

BG_COLOR = '#FBFBF9'
TEXT_COLOR = '#1B263B'

df = pd.read_csv(DATASET_PATH)
total_suicides = df.groupby('sex')['suicides_no'].sum()
real_female_pct = total_suicides['female'] / total_suicides.sum() * 100

survey = pd.read_csv(SURVEY_PATH)
col_pct = [c for c in survey.columns if 'porcentaje' in c.lower() or 'mujeres' in c.lower()][0]
survey['female_pct_estimate'] = survey[col_pct].astype(float) * 10

estimates = survey['female_pct_estimate'].values
n_responses = len(estimates)
deviations = estimates - real_female_pct

sorted_idx = np.argsort(deviations)
deviations_sorted = deviations[sorted_idx]
estimates_sorted = estimates[sorted_idx]

fig, ax = plt.subplots(figsize=(10, 7))
fig.patch.set_facecolor(BG_COLOR)
ax.set_facecolor(BG_COLOR)

y_pos = np.arange(n_responses)

for i, (dev, est) in enumerate(zip(deviations_sorted, estimates_sorted)):
    color = '#B8282A' if dev > 0 else '#31C2B8'
    alpha = min(0.4 + abs(dev) / max(abs(deviations)) * 0.6, 1.0)

    ax.hlines(y=i, xmin=0, xmax=dev, color=color, linewidth=2.5, alpha=alpha)
    ax.scatter(dev, i, color=color, s=200, zorder=5, alpha=alpha,
               edgecolors='white', linewidths=0.5)
    offset = 1.5 if dev > 0 else -1.5
    ha = 'left' if dev > 0 else 'right'
    ax.text(dev + offset, i, f'{est:.0f}%', fontsize=11, color=color,
            fontweight='bold', va='center', ha=ha)

ax.axvline(x=0, color='#4A5568', linewidth=2, linestyle='--', alpha=0.9, zorder=4)
ax.text(0.5, n_responses + 0.5,
        f'Realidad: {real_female_pct:.1f}%',
        fontsize=12, color='#4A5568', fontweight='bold', ha='left')

ax.set_yticks(y_pos)
ax.set_yticklabels([f'Resp. {i+1}' for i in range(n_responses)],
                   fontsize=10, color='#555555')

ax.set_xlabel('Desviación respecto a la realidad (pp)', fontsize=13,
              color=TEXT_COLOR, fontweight='bold', labelpad=10)

ax.set_xlim(deviations.min() - 8, deviations.max() + 8)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_color('#CCCCCC')
ax.spines['left'].set_color('#CCCCCC')
ax.tick_params(axis='x', colors='#555555', labelsize=10)
ax.tick_params(axis='y', colors='#555555')
ax.grid(axis='x', color='#E0E0E0', linewidth=0.5, alpha=0.7)

legend_elements = [
    mpatches.Patch(facecolor='#B8282A', label='Sobreestimación'),
    mpatches.Patch(facecolor='#31C2B8', label='Subestimación'),
    plt.Line2D([0], [0], color='#4A5568', linewidth=2, linestyle='--',
               label=f'Realidad ({real_female_pct:.1f}%)'),
]
ax.legend(handles=legend_elements, loc='lower right', fontsize=11,
          frameon=True, facecolor='white', edgecolor='#CCCCCC',
          labelcolor=TEXT_COLOR)

plt.tight_layout()
plt.savefig(OUTPUT_PATH, dpi=200, bbox_inches='tight', facecolor=BG_COLOR)
plt.close()
print(f'Guardado en: {OUTPUT_PATH}')
