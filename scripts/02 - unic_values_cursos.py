#GERA UMA LISTA COM VALORES UNICOS DE CURSOS

import pandas as pd
import os

# Caminho da pasta
CAMINHO_PASTA = r"C:\Users\john-\OneDrive - Universidade Federal da Paraíba\Área de Trabalho\Artigo - Estatística\projeto-evasao\data\processed"

# Caminho do arquivo de entrada
ARQUIVO_ENTRADA = os.path.join(CAMINHO_PASTA, "ml_iq_2018_2023.csv")

# Caminho do arquivo de saída
ARQUIVO_SAIDA = os.path.join(CAMINHO_PASTA, "cursos_unicos.csv")

# Carrega o arquivo CSV
df = pd.read_csv(ARQUIVO_ENTRADA)

# Filtra valores únicos e remove nulos
cursos = df[['ÁREA_DE_AVALIAÇÃO', 'CÓDIGO_DO_CURSO']].drop_duplicates().dropna()

# Salva o DataFrame em CSV
cursos.to_csv(ARQUIVO_SAIDA, index=False, encoding='utf-8-sig')

# Confirmação
print(f"✅ Arquivo salvo com {len(cursos)} cursos únicos em:\n{ARQUIVO_SAIDA}")
