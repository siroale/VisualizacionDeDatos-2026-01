"""
Visualización 1 — Waffle Chart
Percepción del grupo etario más vulnerable vs. realidad.
Integrante: Alexis Mellis
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
OUTPUT_PATH  = os.path.join(BASE, '..', '..', 'Informe_2', 'figures', 'vis1_waffle.png')

COLORS = {
    '5-14 years':  '#17BEBB',
    '15-24 years': '#D7263D',
    '25-34 years': '#F46036',
    '35-54 years': '#7B2D8E',
    '55-74 years': '#3185A7',
    '75+ years':   '#E84393',
}

AGE_ORDER = ['5-14 years', '15-24 years', '25-34 years',
             '35-54 years', '55-74 years', '75+ years']

SURVEY_TO_DATASET = {
    'Adolescentes y Adultos Jóvenes (15-24 años)': '15-24 years',
    'Adultos (25-34 años)': '25-34 years',
    'Adultos de Mediana Edad (35-54 años)': '35-54 years',
    'Adultos Mayores (55-74 años)': '55-74 years',
    'Personas de la Tercera Edad (75+ años)': '75+ years',
    'Niños y Pre-adolescentes (5-14 años)': '5-14 years',
}

DISPLAY_LABELS = {
    '5-14 years':  '5-14',
    '15-24 years': '15-24',
    '25-34 years': '25-34',
    '35-54 years': '35-54',
    '55-74 years': '55-74',
    '75+ years':   '75+',
}

BG_COLOR = '#FAFAFA'
TEXT_COLOR = '#1a1a2e'
GRID_COLOR = '#E0E0E0'

survey = pd.read_csv(SURVEY_PATH)
col_age = [c for c in survey.columns if 'grupos de edad' in c.lower()][0]
survey['age_mapped'] = survey[col_age].map(SURVEY_TO_DATASET)
survey_counts = survey['age_mapped'].value_counts()

for age in AGE_ORDER:
    if age not in survey_counts.index:
        survey_counts[age] = 0
survey_counts = survey_counts.reindex(AGE_ORDER)

df = pd.read_csv(DATASET_PATH)
real_rates = df.groupby('age')['suicides/100k pop'].mean()
for age in AGE_ORDER:
    if age not in real_rates.index:
        real_rates[age] = 0
real_rates = real_rates.reindex(AGE_ORDER)

real_pct = (real_rates / real_rates.sum() * 100).round(0).astype(int)
diff = 100 - real_pct.sum()
real_pct.iloc[real_pct.argmax()] += diff

survey_pct = (survey_counts / survey_counts.sum() * 100).round(0).astype(int)
diff = 100 - survey_pct.sum()
survey_pct.iloc[survey_pct.argmax()] += diff

fig, axes = plt.subplots(1, 2, figsize=(16, 7))
fig.patch.set_facecolor(BG_COLOR)

for ax in axes:
    ax.set_facecolor(BG_COLOR)

def draw_waffle(ax, data_dict, colors, rows=10, cols=10):
    values = list(data_dict.values())
    squares = []
    for i, (label, val) in enumerate(data_dict.items()):
        squares.extend([i] * val)
    while len(squares) < rows * cols:
        squares.append(len(data_dict))
    squares = squares[:rows * cols]

    for idx, cat_idx in enumerate(squares):
        row = idx // cols
        col = idx % cols
        color = colors[cat_idx] if cat_idx < len(colors) else '#E8E8E8'
        rect = plt.Rectangle((col, rows - 1 - row), 0.9, 0.9,
                              facecolor=color, edgecolor=BG_COLOR, linewidth=1.5,
                              alpha=0.9)
        ax.add_patch(rect)
    ax.set_xlim(-0.5, cols + 0.5)
    ax.set_ylim(-0.5, rows + 0.5)
    ax.set_aspect('equal')
    ax.axis('off')

survey_data = {DISPLAY_LABELS[k]: int(v) for k, v in survey_pct.items() if v > 0}
survey_colors = [COLORS[k] for k, v in survey_pct.items() if v > 0]
axes[0].set_title('Percepción de la Encuesta', fontsize=16, fontweight='bold',
                  color=TEXT_COLOR, pad=15)
draw_waffle(axes[0], survey_data, survey_colors)

real_data = {DISPLAY_LABELS[k]: int(v) for k, v in real_pct.items() if v > 0}
real_colors_list = [COLORS[k] for k, v in real_pct.items() if v > 0]
axes[1].set_title('Realidad según el Dataset', fontsize=16, fontweight='bold',
                  color=TEXT_COLOR, pad=15)
draw_waffle(axes[1], real_data, real_colors_list)

legend_patches = [mpatches.Patch(facecolor=COLORS[age], edgecolor='#999999',
                                 label=f'{DISPLAY_LABELS[age]} años')
                  for age in AGE_ORDER]
fig.legend(handles=legend_patches, loc='lower center', ncol=6,
           fontsize=11, frameon=False, labelcolor=TEXT_COLOR,
           bbox_to_anchor=(0.5, 0.01))

fig.suptitle('¿Qué grupo etario tiene la mayor tasa de suicidio?',
             fontsize=20, fontweight='bold', color=TEXT_COLOR, y=0.97)

plt.tight_layout(rect=[0, 0.08, 1, 0.92])
plt.savefig(OUTPUT_PATH, dpi=200, bbox_inches='tight', facecolor=BG_COLOR)
plt.close()
print(f'Guardado en: {OUTPUT_PATH}')
