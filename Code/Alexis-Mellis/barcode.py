import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import Normalize

df = pd.read_csv("Datasets/suicide_dataset.csv")
df_chile = df[df["country"] == "Chile"]
df_year_filter = df_chile.groupby("year")["suicides_no"].sum().reset_index()
df_year_filter = df_year_filter[df_year_filter["year"] <= 2015].sort_values("year")

years = df_year_filter["year"].values
suicides_no = df_year_filter["suicides_no"].values

fig, ax = plt.subplots(figsize=(12, 3))
cmap = plt.cm.Reds
norm = Normalize(vmin=suicides_no.min(), vmax=suicides_no.max())

for i in range(len(years)):
    ax.axvspan(years[i] - 0.5, years[i] + 0.5, color=cmap(norm(suicides_no[i])))

ax.set_yticks([]) 
ax.set_ylim(0, 1)
ax.set_xlim(years.min() - 0.5, years.max() + 0.5)
ax.set_xticks(years[::2])
ax.set_xticklabels(years[::2], rotation=0, fontsize=10)

for spine in ax.spines.values():
    spine.set_visible(False)

sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = fig.colorbar(sm, ax=ax, orientation="horizontal", fraction=0.15, pad=0.2, aspect=40)
cbar.set_label("Cantidad Total de Suicidios", fontsize=11, fontweight="bold")
cbar.outline.set_visible(False)

plt.title("Evolución de la Cantidad de Suicidios en Chile (1985 - 2015)", fontsize=16, fontweight="bold")
plt.tight_layout()
plt.savefig("Code/Alexis-Mellis/barcode_chile_cantidad_suicidios.png", dpi=300, bbox_inches="tight")
plt.show()