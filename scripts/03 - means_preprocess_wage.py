#CALCULA MÉDIA SALÁRIAL

import pandas as pd
import os
from functools import reduce

# Caminho da pasta onde estão os arquivos
CAMINHO_PASTA = r"C:\Users\john-\OneDrive - Universidade Federal da Paraíba\Área de Trabalho\Artigo - Estatística\projeto-evasao\data\processed"

# Lista de anos
ANOS = [2018, 2019, 2021, 2022, 2023]

# Lista para armazenar os DataFrames
dfs = []

for ano in ANOS:
    caminho = os.path.join(CAMINHO_PASTA, f"media_salarial_municipio_cbo_{ano}.csv")
    df = pd.read_csv(caminho)

    # Seleciona e renomeia
    df = df[['mun', 'cbo_ocup', 'media_salarial']].copy()
    df.rename(columns={'media_salarial': f'media_salarial_{ano}'}, inplace=True)

    # Converte 'mun' e 'cbo_ocup' para string
    df['mun'] = df['mun'].astype(str)
    df['cbo_ocup'] = df['cbo_ocup'].astype(str)

    dfs.append(df)

# Merge múltiplo usando reduce
df_merged = reduce(lambda left, right: pd.merge(left, right, on=['mun', 'cbo_ocup'], how='outer'), dfs)

# Calcula a média ignorando valores ausentes
df_merged['media_salarial_media_2018_2023'] = df_merged[
    [f'media_salarial_{ano}' for ano in ANOS]
].mean(axis=1)

# Cria DataFrame final
media_salarial_2018_2023 = df_merged[['mun', 'cbo_ocup', 'media_salarial_media_2018_2023']].copy()

# Salva na pasta processed
CAMINHO_SAIDA = os.path.join(CAMINHO_PASTA, "media_salarial_2018_2023.csv")
media_salarial_2018_2023.to_csv(CAMINHO_SAIDA, index=False, encoding='utf-8-sig')

print(f"✅ Arquivo final salvo com {len(media_salarial_2018_2023)} linhas em:\n{CAMINHO_SAIDA}")

