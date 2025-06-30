import pandas as pd
import os
import re

# Caminhos
base_path = r"C:\Users\john-\OneDrive - Universidade Federal da Paraíba\Área de Trabalho\Artigo - Estatística\projeto-evasao\data\processed"
arquivo_entrada_cursos = "resultado_match_cbo_cursos.xlsx"
arquivo_entrada_areas = "ml_iq_2018_2023.csv"

# Caminhos completos
caminho_entrada_cursos = os.path.join(base_path, arquivo_entrada_cursos)
caminho_entrada_areas = os.path.join(base_path, arquivo_entrada_areas)

# Ler arquivo Excel com openpyxl
df_cursos = pd.read_excel(caminho_entrada_cursos, engine='openpyxl')

# Ler arquivo CSV
df_areas = pd.read_csv(caminho_entrada_areas)

# Extrai lista de palavras únicas da coluna 'ÁREA_DE_AVALIAÇÃO' (em maiúsculas)
palavras_areas = set()
for area in df_areas['ÁREA_DE_AVALIAÇÃO'].dropna():
    for palavra in str(area).upper().split():
        palavras_areas.add(palavra)
palavras_areas = list(palavras_areas)

# Função para encontrar a primeira palavra da lista que aparece no texto
def buscar_primeira_palavra(texto):
    if pd.isna(texto):
        return ''
    texto_maiusculo = texto.upper()
    for palavra in palavras_areas:
        if re.search(rf'\b{re.escape(palavra)}\b', texto_maiusculo):
            return palavra
    return ''

# Aplica a função na coluna CURSOS
df_cursos['CURSOS'] = df_cursos['CURSOS'].apply(buscar_primeira_palavra)

# Seleciona as colunas necessárias
df_limpo = df_cursos[['cbo_ocup', 'CURSOS']]

# Salva o resultado
os.makedirs(base_path, exist_ok=True)
arquivo_saida = os.path.join(base_path, "cursos_pronto.csv")
df_limpo.to_csv(arquivo_saida, index=False)

print(f"Arquivo salvo em: {arquivo_saida}")