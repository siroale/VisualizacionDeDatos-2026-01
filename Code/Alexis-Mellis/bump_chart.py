import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

df = pd.read_csv('/home/immergreen/github/VisualizacionDeDatos-2026-01/Datasets/suicide_dataset.csv')

df['period'] = pd.cut(df['year'], bins=[1984, 1989, 1994, 1999, 2004, 2009, 2015],
                       labels=['1985-89', '1990-94', '1995-99', '2000-04', '2005-09', '2010-15'])

period_country = df.groupby(['period', 'country']).agg(
    total_suicides=('suicides_no', 'sum'),
    total_pop=('population', 'sum')
).reset_index()
period_country['rate'] = period_country['total_suicides'] / period_country['total_pop'] * 100000

min_records = df.groupby(['period', 'country']).size().reset_index(name='n')
period_country = period_country.merge(min_records, on=['period', 'country'])
period_country = period_country[period_country['n'] >= 6]

overall_top = period_country.groupby('country')['rate'].mean().nlargest(10).index.tolist()
top_data = period_country[period_country['country'].isin(overall_top)].copy()

top_data['rank'] = top_data.groupby('period')['rate'].rank(ascending=False, method='min')

periods = ['1985-89', '1990-94', '1995-99', '2000-04', '2005-09', '2010-15']

colors = [
    '#E63946', '#457B9D', '#2A9D8F', '#E9C46A', '#F4A261',
    '#264653', '#A8DADC', '#6A0572', '#1D3557', '#D4A373'
]
color_map = {c: colors[i] for i, c in enumerate(overall_top)}

fig, ax = plt.subplots(figsize=(14, 8))
fig.patch.set_facecolor('#FFFFFF')
ax.set_facecolor('#FFFFFF')

for country in overall_top:
    cdata = top_data[top_data['country'] == country].set_index('period')
    x_vals = []
    y_vals = []
    for i, p in enumerate(periods):
        if p in cdata.index:
            x_vals.append(i)
            y_vals.append(cdata.loc[p, 'rank'])

    ax.plot(x_vals, y_vals, color=color_map[country], linewidth=2.8, alpha=0.9,
            zorder=2, solid_capstyle='round')
    ax.scatter(x_vals, y_vals, color=color_map[country], s=60, zorder=3,
               edgecolors='#333333', linewidths=0.5)

    if len(x_vals) > 0:
        ax.text(x_vals[-1] + 0.15, y_vals[-1], country,
                fontsize=9, color=color_map[country], va='center',
                fontweight='bold', fontfamily='sans-serif')
        ax.text(x_vals[0] - 0.15, y_vals[0], f'{int(y_vals[0])}',
                fontsize=8, color=color_map[country], va='center', ha='right',
                fontweight='bold', fontfamily='sans-serif')

ax.set_xticks(range(len(periods)))
ax.set_xticklabels(periods, fontsize=11, color='#333333', fontfamily='sans-serif')
ax.set_yticks(range(1, 11))
ax.set_yticklabels([f'#{i}' for i in range(1, 11)], fontsize=9, color='#555555',
                    fontfamily='sans-serif')
ax.invert_yaxis()

ax.set_xlim(-0.5, len(periods) - 1 + 2.5)
ax.set_ylim(10.5, 0.5)

for spine in ax.spines.values():
    spine.set_visible(False)
ax.tick_params(axis='both', length=0)

for i in range(len(periods)):
    ax.axvline(x=i, color='#E0E0E0', linewidth=0.5, zorder=0)
for i in range(1, 11):
    ax.axhline(y=i, color='#E0E0E0', linewidth=0.3, zorder=0)

ax.set_title('Ranking de Tasas de Suicidio por Pais (Top 10)\nEvolucion por Periodo Quinquenal, 1985-2015',
             fontsize=15, color='#1A1A1A', fontweight='bold', fontfamily='sans-serif',
             pad=20)

ax.text(0.5, -0.08,
        'Fuente: Kaggle - Suicide Rates Overview 1985-2016 | Tasa por 100.000 habitantes',
        transform=ax.transAxes, fontsize=8, color='#777777', ha='center',
        fontfamily='sans-serif')

plt.tight_layout()
plt.savefig('/home/immergreen/github/VisualizacionDeDatos-2026-01/Informe_TP/figures/vis4_bump_chart.png',
            dpi=200, bbox_inches='tight', facecolor='#FFFFFF')
plt.close()
print("Bump chart saved.")
