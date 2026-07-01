import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as FancyBboxPatch
from matplotlib.path import Path
import matplotlib.patches as mpatches
import numpy as np
import matplotlib.patheffects as pe

df = pd.read_csv('/home/andres/Documents/VisualizacionDeDatos-2026-01/Datasets/suicide_dataset.csv')

region_map = {
    'Russian Federation': 'Europa del Este', 'Ukraine': 'Europa del Este',
    'Lithuania': 'Europa del Este', 'Latvia': 'Europa del Este',
    'Estonia': 'Europa del Este', 'Belarus': 'Europa del Este',
    'Hungary': 'Europa del Este', 'Poland': 'Europa del Este',
    'Romania': 'Europa del Este', 'Bulgaria': 'Europa del Este',
    'Croatia': 'Europa del Este', 'Serbia': 'Europa del Este',
    'Slovenia': 'Europa del Este', 'Czech Republic': 'Europa del Este',
    'Slovakia': 'Europa del Este', 'Bosnia and Herzegovina': 'Europa del Este',
    'Montenegro': 'Europa del Este', 'Albania': 'Europa del Este',
    'Republic of Korea': 'Asia-Pacifico', 'Japan': 'Asia-Pacifico',
    'Thailand': 'Asia-Pacifico', 'Sri Lanka': 'Asia-Pacifico',
    'Philippines': 'Asia-Pacifico', 'Singapore': 'Asia-Pacifico',
    'Australia': 'Asia-Pacifico', 'New Zealand': 'Asia-Pacifico',
    'Kazakhstan': 'Asia-Pacifico', 'Kyrgyzstan': 'Asia-Pacifico',
    'Uzbekistan': 'Asia-Pacifico', 'Turkmenistan': 'Asia-Pacifico',
    'Georgia': 'Asia-Pacifico', 'Armenia': 'Asia-Pacifico',
    'Azerbaijan': 'Asia-Pacifico', 'Israel': 'Asia-Pacifico',
    'Turkey': 'Asia-Pacifico', 'Cyprus': 'Asia-Pacifico',
    'Macau': 'Asia-Pacifico', 'Fiji': 'Asia-Pacifico',
    'Maldives': 'Asia-Pacifico', 'Mongolia': 'Asia-Pacifico',
    'Oman': 'Asia-Pacifico', 'Bahrain': 'Asia-Pacifico',
    'Kuwait': 'Asia-Pacifico', 'Qatar': 'Asia-Pacifico',
    'United Arab Emirates': 'Asia-Pacifico',
    'United States': 'Norteamerica', 'Canada': 'Norteamerica',
    'Cuba': 'Norteamerica', 'Puerto Rico': 'Norteamerica',
    'Mexico': 'Latinoamerica', 'Brazil': 'Latinoamerica',
    'Argentina': 'Latinoamerica', 'Chile': 'Latinoamerica',
    'Colombia': 'Latinoamerica', 'Ecuador': 'Latinoamerica',
    'Uruguay': 'Latinoamerica', 'Paraguay': 'Latinoamerica',
    'Suriname': 'Latinoamerica', 'Guatemala': 'Latinoamerica',
    'Costa Rica': 'Latinoamerica', 'Panama': 'Latinoamerica',
    'El Salvador': 'Latinoamerica', 'Nicaragua': 'Latinoamerica',
    'Belize': 'Latinoamerica', 'Guyana': 'Latinoamerica',
    'Trinidad and Tobago': 'Latinoamerica', 'Jamaica': 'Latinoamerica',
    'Bahamas': 'Latinoamerica', 'Barbados': 'Latinoamerica',
    'Antigua and Barbuda': 'Latinoamerica', 'Grenada': 'Latinoamerica',
    'Saint Kitts and Nevis': 'Latinoamerica', 'Saint Lucia': 'Latinoamerica',
    'Saint Vincent and Grenadines': 'Latinoamerica', 'Dominica': 'Latinoamerica',
    'Aruba': 'Latinoamerica',
    'France': 'Europa Occ.', 'Germany': 'Europa Occ.',
    'United Kingdom': 'Europa Occ.', 'Spain': 'Europa Occ.',
    'Italy': 'Europa Occ.', 'Netherlands': 'Europa Occ.',
    'Belgium': 'Europa Occ.', 'Austria': 'Europa Occ.',
    'Switzerland': 'Europa Occ.', 'Sweden': 'Europa Occ.',
    'Norway': 'Europa Occ.', 'Denmark': 'Europa Occ.',
    'Finland': 'Europa Occ.', 'Ireland': 'Europa Occ.',
    'Iceland': 'Europa Occ.', 'Luxembourg': 'Europa Occ.',
    'Portugal': 'Europa Occ.', 'Greece': 'Europa Occ.',
    'Malta': 'Europa Occ.', 'San Marino': 'Europa Occ.',
    'South Africa': 'Africa', 'Mauritius': 'Africa',
    'Cabo Verde': 'Africa', 'Seychelles': 'Africa',
}

df['region'] = df['country'].map(region_map).fillna('Otros')

regions = ['Europa del Este', 'Europa Occ.', 'Norteamerica', 'Latinoamerica', 'Asia-Pacifico']
sexes = ['male', 'female']
sex_labels = {'male': 'Hombres', 'female': 'Mujeres'}
age_order = ['5-14 years', '15-24 years', '25-34 years', '35-54 years', '55-74 years', '75+ years']
age_short = {'5-14 years': '5-14', '15-24 years': '15-24', '25-34 years': '25-34',
             '35-54 years': '35-54', '55-74 years': '55-74', '75+ years': '75+'}

filtered = df[df['region'].isin(regions)]
reg_sex = filtered.groupby(['region', 'sex'])['suicides_no'].sum().reset_index()
sex_age = filtered.groupby(['sex', 'age'])['suicides_no'].sum().reset_index()

grand_total = filtered['suicides_no'].sum()

region_colors = {
    'Europa del Este': '#B8282A', 'Europa Occ.': '#C0C0C0',
    'Latinoamerica': '#C0C0C0', 'Norteamerica': '#C0C0C0', 'Asia-Pacifico': '#C0C0C0'
}
sex_colors = {'male': '#1B263B', 'female': '#A0A0A0'}
age_colors = {
    '5-14 years': '#8A99A8', '15-24 years': '#8A99A8', '25-34 years': '#8A99A8',
    '35-54 years': '#4A5568', '55-74 years': '#4A5568', '75+ years': '#4A5568'
}

def make_bezier(x0, y0_start, y0_end, x1, y1_start, y1_end, alpha=0.3, color='white'):
    verts = [
        (x0, y0_start),
        (x0 + (x1 - x0) * 0.5, y0_start),
        (x1 - (x1 - x0) * 0.5, y1_start),
        (x1, y1_start),
        (x1, y1_end),
        (x1 - (x1 - x0) * 0.5, y1_end),
        (x0 + (x1 - x0) * 0.5, y0_end),
        (x0, y0_end),
        (x0, y0_start),
    ]
    codes = [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4,
             Path.LINETO, Path.CURVE4, Path.CURVE4, Path.CURVE4, Path.CLOSEPOLY]
    return mpatches.PathPatch(Path(verts, codes), facecolor=color, alpha=alpha,
                               edgecolor='none', linewidth=0)

fig, ax = plt.subplots(figsize=(16, 9))
fig.patch.set_facecolor('#FBFBF9')
ax.set_facecolor('#FBFBF9')

col_x = [0.08, 0.48, 0.88]
bar_w = 0.06
gap = 0.008
y_bot = 0.05
y_top = 0.92
y_range = y_top - y_bot

region_totals = {r: reg_sex[reg_sex['region'] == r]['suicides_no'].sum() for r in regions}
sex_totals = {s: reg_sex[reg_sex['sex'] == s]['suicides_no'].sum() for s in sexes}
age_totals = {a: sex_age[sex_age['age'] == a]['suicides_no'].sum() for a in age_order}

total_with_gaps = grand_total
gap_space_r = gap * (len(regions) - 1)
gap_space_s = gap * (len(sexes) - 1)
gap_space_a = gap * (len(age_order) - 1)
usable_r = y_range - gap_space_r
usable_s = y_range - gap_space_s
usable_a = y_range - gap_space_a

def draw_column(ax, x, items, totals, colors_dict, label_func, usable, gap_count):
    positions = {}
    cum = y_bot
    for i, item in enumerate(items):
        h = totals[item] / grand_total * usable
        rect = plt.Rectangle((x - bar_w / 2, cum), bar_w, h,
                               facecolor=colors_dict[item], edgecolor='#CCCCCC',
                               linewidth=1, zorder=3)
        ax.add_patch(rect)
        lbl = label_func(item)
        mid = cum + h / 2
        positions[item] = (cum, cum + h)
        if h > 0.025:
            fs = 13 if len(lbl) > 12 else 14
            ax.text(x, mid, lbl, ha='center', va='center', fontsize=fs,
                    color='white', fontweight='bold', fontfamily='sans-serif', zorder=4,
                    path_effects=[pe.withStroke(linewidth=2, foreground="black")])
            pct = totals[item] / grand_total * 100
            ax.text(x, cum + h + 0.003, f'{pct:.1f}%', ha='center', va='bottom',
                    fontsize=12, color='#333333', fontweight='bold', fontfamily='sans-serif', zorder=4,
                    path_effects=[pe.withStroke(linewidth=1.5, foreground="white")])
        cum += h + gap
    return positions

r_pos = draw_column(ax, col_x[0], regions, region_totals, region_colors,
                     lambda r: r, usable_r, len(regions) - 1)
s_pos = draw_column(ax, col_x[1], sexes, sex_totals, sex_colors,
                     lambda s: sex_labels[s], usable_s, len(sexes) - 1)
a_pos = draw_column(ax, col_x[2], age_order, age_totals, age_colors,
                     lambda a: age_short[a], usable_a, len(age_order) - 1)

r_cum_out = {r: r_pos[r][0] for r in regions}
s_cum_in_left = {s: s_pos[s][0] for s in sexes}
s_cum_out_right = {s: s_pos[s][0] for s in sexes}
a_cum_in = {a: a_pos[a][0] for a in age_order}

for r in regions:
    for s in sexes:
        val = reg_sex[(reg_sex['region'] == r) & (reg_sex['sex'] == s)]['suicides_no']
        if len(val) == 0 or val.values[0] == 0:
            continue
        v = val.values[0]
        h_left = v / grand_total * usable_r
        h_right = v / grand_total * usable_s
        patch = make_bezier(
            col_x[0] + bar_w / 2, r_cum_out[r], r_cum_out[r] + h_left,
            col_x[1] - bar_w / 2, s_cum_in_left[s], s_cum_in_left[s] + h_right,
            alpha=0.25, color=region_colors[r]
        )
        ax.add_patch(patch)
        r_cum_out[r] += h_left
        s_cum_in_left[s] += h_right

for s in sexes:
    for a in age_order:
        val = sex_age[(sex_age['sex'] == s) & (sex_age['age'] == a)]['suicides_no']
        if len(val) == 0 or val.values[0] == 0:
            continue
        v = val.values[0]
        h_left = v / grand_total * usable_s
        h_right = v / grand_total * usable_a
        patch = make_bezier(
            col_x[1] + bar_w / 2, s_cum_out_right[s], s_cum_out_right[s] + h_left,
            col_x[2] - bar_w / 2, a_cum_in[a], a_cum_in[a] + h_right,
            alpha=0.25, color=sex_colors[s]
        )
        ax.add_patch(patch)
        s_cum_out_right[s] += h_left
        a_cum_in[a] += h_right

for x, label in zip(col_x, ['Region', 'Sexo', 'Grupo Etario']):
    ax.text(x, y_top + 0.035, label, ha='center', va='bottom', fontsize=16,
            color='#333333', fontweight='bold', fontfamily='sans-serif')

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')

plt.savefig('/home/andres/Documents/VisualizacionDeDatos-2026-01/infografia_TP/vis5_sankey.png',
            dpi=200, bbox_inches='tight', facecolor='#FBFBF9')
plt.close()
print("Sankey diagram saved.")
