import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("Datasets/suicide_dataset.csv")
df_chile = df[df["country"] == "Chile"]

df_filtro = df_chile.groupby("year")["suicides_no"].sum().reset_index()
df_filtro = df_filtro[df_filtro["year"] <= 2015]
x = df_filtro["year"]
y = df_filtro["suicides_no"]

fig, ax = plt.subplots(figsize=(12, 6))
colors = plt.cm.Reds(y / y.max())

ax.vlines(x=x, ymin=0, ymax=y, color="gray", alpha=0.6, linewidth=2)
ax.scatter(x, y, color=colors, s=120, zorder=3, edgecolor="black", alpha=0.9)
ax.set_title("Evolución de la Cantidad de Suicidios en Chile (1985 - 2015)\n", fontsize=16, pad=20)
ax.set_xlabel("Año", fontsize=12)
ax.set_ylabel("Cantidad Total de Suicidios", fontsize=12)

for spine in ["top", "right"]:
    ax.spines[spine].set_visible(False)

ax.set_ylim(0, y.max() * 1.15)
ax.set_xlim(x.min() - 1, x.max() + 1)
ax.grid(axis="y", linestyle="--", alpha=0.4)
plt.tight_layout()
plt.savefig("Code/Alexis-Mellis/lollipop_chile_suicides.png", dpi=300, bbox_inches="tight")
plt.show()