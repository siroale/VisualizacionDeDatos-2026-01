import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('suicide_dataset.csv')
df_grouped = df.groupby(['year', 'sex'])['suicides/100k pop'].mean().unstack()

plt.figure(figsize=(10, 12))
plt.hlines(y=df_grouped.index, xmin=df_grouped['female'], xmax=df_grouped['male'], color='grey', alpha=0.5)
plt.scatter(df_grouped['female'], df_grouped.index, color='lightcoral', label='Female', zorder=3, s=50)
plt.scatter(df_grouped['male'], df_grouped.index, color='steelblue', label='Male', zorder=3, s=50)

plt.title('Brecha de Género en Tasas Promedio de Suicidio (1985-2016)')
plt.xlabel('Tasa Promedio de Suicidios por 100k habitantes')
plt.ylabel('Año')
plt.legend(title='Sexo')
plt.grid(axis='y', linestyle='--', alpha=0.3)
plt.tight_layout()
plt.savefig("figure003.png", dpi=300, bbox_inches="tight")
plt.show()
