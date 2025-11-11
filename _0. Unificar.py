import pandas as pd

df = pd.read_csv('2. Original.csv', encoding='utf-8')
df_grouped = df.groupby('URL')['Keyword'].agg(lambda x: '\n'.join(x)).reset_index()
df_grouped.columns = ['URL', 'Keywords']
df_grouped.to_csv('3. Unificado.csv', index=False, encoding='utf-8')
