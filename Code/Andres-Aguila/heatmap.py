import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('suicide_dataset.csv')
top_countries = df.groupby('country')['suicides/100k pop'].mean().nlargest(15).index
df_top = df[df['country'].isin(top_countries)]
pivot_data = df_top.pivot_table(values='suicides/100k pop', index='country', columns='year', aggfunc='mean')

plt.figure(figsize=(14, 8))
sns.heatmap(pivot_data, cmap='YlOrRd', linewidths=.5, cbar_kws={'label': 'Tasa por 100k hab.'})
plt.title('Evolución de la Tasa de Suicidios en los 15 Países con Mayor Incidencia')
plt.xlabel('Año')
plt.ylabel('País')
plt.tight_layout()
plt.savefig("figure004.png", dpi=300, bbox_inches="tight")
plt.show()
