import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("../../Datasets/suicide_dataset.csv")
df_grouped = df.groupby(['year', 'age'])['suicides_no'].sum().reset_index()

age_order = ["5-14 years", "15-24 years", "25-34 years", "35-54 years", "55-74 years", "75+ years"]
df_grouped['age'] = pd.Categorical(df_grouped['age'], categories=age_order, ordered=True)
df_pivot = df_grouped.pivot(index='year', columns='age', values='suicides_no').fillna(0)
df_pivot = df_pivot[df_pivot.index <= 2020]