# -*- coding: utf-8 -*-
# Criterio E: Ridgeline Plot (Joy Plot)
# Relacion entre nivel economico (PIB per capita) y tasas de suicidio

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from scipy.stats import gaussian_kde
import warnings
warnings.filterwarnings('ignore')

# ---------- Carga y preparacion ----------
df = pd.read_csv('suicide_dataset.csv')

df.rename(columns={
    'suicides/100k pop': 'rate',
    'gdp_per_capita ($)': 'gdp_pc'
}, inplace=True)

country_agg = (
    df.groupby(['country'])
    .agg(
        rate=('rate', 'mean'),
        gdp_pc=('gdp_pc', 'mean')
    )
    .reset_index()
)

country_agg = country_agg[(country_agg['rate'] > 0) & (country_agg['gdp_pc'] > 0)].copy()

quintile_labels = [
    'Q1 - Ingreso bajo',
    'Q2 - Ingreso medio-bajo',
    'Q3 - Ingreso medio',
    'Q4 - Ingreso medio-alto',
    'Q5 - Ingreso alto'
]

country_agg['gdp_quintile'] = pd.qcut(
    country_agg['gdp_pc'], q=5, labels=quintile_labels
)

# ---------- Parametros del ridgeline ----------
categories = quintile_labels[::-1]
n_cats = len(categories)
overlap = 0.55
x_min = country_agg['rate'].quantile(0.00)
x_max = country_agg['rate'].quantile(0.97)
x_grid = np.linspace(x_min, x_max, 500)

palette = ['#1b9e77', '#d95f02', '#7570b3', '#e7298a', '#66a61e']
palette_rev = palette[::-1]

# ---------- Figura ----------
fig, axes = plt.subplots(
    n_cats, 1, figsize=(12, 8),
    sharex=True,
    gridspec_kw={'hspace': -overlap}
)

fig.patch.set_facecolor('#0d1117')

stat_summary = {}

for i, cat in enumerate(categories):
    ax = axes[i]
    subset = country_agg.loc[country_agg['gdp_quintile'] == cat, 'rate'].values

    if len(subset) < 3:
        continue

    kde = gaussian_kde(subset, bw_method=0.35)
    density = kde(x_grid)

    color = palette_rev[i]
    ax.fill_between(x_grid, density, alpha=0.65, color=color, linewidth=0)
    ax.plot(x_grid, density, color=color, linewidth=1.8)

    median_val = np.median(subset)
    ax.axvline(median_val, color='white', linestyle='--', linewidth=0.9, alpha=0.7)

    stat_summary[cat] = {
        'mediana': round(median_val, 2),
        'media': round(np.mean(subset), 2),
        'desv_std': round(np.std(subset), 2),
        'n_paises': len(subset)
    }

    ax.set_facecolor('#0d1117')
    ax.set_xlim(x_min, x_max)
    ax.set_yticks([])
    ax.set_ylabel('')

    ax.text(
        -0.01, 0.3, cat,
        transform=ax.transAxes,
        fontsize=10, fontweight='bold',
        color=color, ha='right', va='center',
        fontfamily='sans-serif'
    )

    med_y = kde(np.array([median_val]))[0]
    ax.annotate(
        f'Md={median_val:.1f}',
        xy=(median_val, med_y * 0.85),
        fontsize=7.5, color='white', alpha=0.85,
        ha='center', va='bottom',
        fontfamily='monospace'
    )

    for spine in ax.spines.values():
        spine.set_visible(False)

    if i < n_cats - 1:
        ax.tick_params(bottom=False, labelbottom=False)

axes[-1].set_xlabel(
    'Tasa de suicidio promedio por pais (por 100k hab.)',
    fontsize=11, color='#c9d1d9', labelpad=12,
    fontfamily='sans-serif'
)
axes[-1].tick_params(axis='x', colors='#c9d1d9', labelsize=9)
axes[-1].xaxis.set_major_formatter(ticker.FormatStrFormatter('%.0f'))

fig.suptitle(
    'Distribucion de tasas de suicidio segun quintil de PIB per capita',
    fontsize=16, fontweight='bold', color='#f0f6fc',
    y=0.97, fontfamily='sans-serif'
)

fig.text(
    0.5, 0.92,
    'Ridgeline Plot  |  Densidad KDE por estrato economico  |  Linea punteada = mediana',
    ha='center', fontsize=9, color='#8b949e',
    fontstyle='italic', fontfamily='sans-serif'
)

plt.savefig(
    'criterio_e_ridgeline.png',
    dpi=300, bbox_inches='tight',
    facecolor=fig.get_facecolor(),
    edgecolor='none'
)

plt.show()

# ---------- Resumen estadistico ----------
print('\n--- Resumen estadistico por quintil de PIB per capita ---\n')
for cat in quintile_labels:
    s = stat_summary.get(cat, {})
    print(f'{cat}')
    print(f'  Paises: {s.get("n_paises", "N/A")}  |  '
          f'Mediana: {s.get("mediana", "N/A")}  |  '
          f'Media: {s.get("media", "N/A")}  |  '
          f'Desv. Std: {s.get("desv_std", "N/A")}')
    print()
