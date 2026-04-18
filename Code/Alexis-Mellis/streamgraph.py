import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("Datasets/suicide_dataset.csv")
df_grouped = df.groupby(["year", "age"])["suicides_no"].sum().reset_index()

age_order = ["5-14 years", "15-24 years", "25-34 years", "35-54 years", "55-74 years", "75+ years"]
df_grouped["age"] = pd.Categorical(df_grouped["age"], categories=age_order, ordered=True)

df_pivot = df_grouped.pivot(index="year", columns="age", values="suicides_no").fillna(0)
df_pivot = df_pivot[df_pivot.index <= 2015]

x = df_pivot.index
y = df_pivot.T.values
etiquetas = df_pivot.columns

fig, ax = plt.subplots(figsize=(12, 6))

ax.stackplot(x, y, labels=etiquetas, baseline="sym", colors=plt.cm.bone_r(np.linspace(0.15, 0.9, 6)))

ax.set_title("Distribución Etaria Global de Suicidios (1985 - 2015)\n", fontsize=16, fontweight="bold")
ax.set_xlabel("Año", fontsize=12)
ax.set_yticks([])

for spine in ["top", "right", "left"]:
    ax.spines[spine].set_visible(False)

ax.set_xlim(x.min(), x.max())
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles[::-1], labels[::-1], loc="center left", bbox_to_anchor=(1.02, 0.5), title="Grupo Etario", frameon=False)

plt.tight_layout()
plt.savefig("Informe/figures/figure002.png", dpi=300, bbox_inches="tight")
plt.show()