#GERA UMA LISTA COM VALORES ÚNICOS DE CBOS

import pandas as pd
import os

# Caminho da pasta
CAMINHO_PASTA = r"C:\Users\john-\OneDrive - Universidade Federal da Paraíba\Área de Trabalho\Artigo - Estatística\projeto-evasao\data\processed"

# Caminho do arquivo de entrada
ARQUIVO_ENTRADA = os.path.join(CAMINHO_PASTA, "media_salarial_municipio_cbo_2018.csv")

# Caminho do arquivo de saída
ARQUIVO_SAIDA = os.path.join(CAMINHO_PASTA, "cbo_unicos.csv")

# Carrega o CSV
df = pd.read_csv(ARQUIVO_ENTRADA)

# Filtra valores únicos da coluna cbo_ocup
cbo = df[['cbo_ocup']].drop_duplicates().dropna()

# Salva o DataFrame em CSV
cbo.to_csv(ARQUIVO_SAIDA, index=False, encoding='utf-8-sig')

# Confirmação
print(f"✅ Arquivo salvo com {len(cbo)} ocupações únicas em:\n{ARQUIVO_SAIDA}")
