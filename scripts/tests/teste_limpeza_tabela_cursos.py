import pandas as pd
import re
import os

# Caminho da pasta processed
CAMINHO_PASTA = r"C:\Users\john-\OneDrive - Universidade Federal da Paraíba\Área de Trabalho\Artigo - Estatística\projeto-evasao\data\processed"
ARQUIVO_ENTRADA = os.path.join(CAMINHO_PASTA, "resultado_match_cbo_cursos.xlsx")  # ajuste se necessário
ARQUIVO_SAIDA = os.path.join(CAMINHO_PASTA, "cursos_tratados_multiplos.xlsx")

# Lê o arquivo
df = pd.read_excel(ARQUIVO_ENTRADA)

# Função para extrair todos os nomes de cursos (em letras maiúsculas)
def extrair_cursos(texto):
    if pd.isna(texto):
        return []
    return re.findall(r'\b[A-Z]{2,}(?:\s+[A-Z]{2,})*\b', str(texto))

# Aplica a função e cria nova coluna temporária com lista de cursos
df['LISTA_CURSOS'] = df['CURSOS'].apply(extrair_cursos)

# Converte listas em colunas separadas
cursos_expandidos = df['LISTA_CURSOS'].apply(pd.Series)
cursos_expandidos.columns = [f'CURSO_{i+1}' for i in cursos_expandidos.columns]

# Junta com o CBO original
cursos_tratados = pd.concat([df[['cbo_ocup']], cursos_expandidos], axis=1)

# Salva como .xlsx
cursos_tratados.to_excel(ARQUIVO_SAIDA, index=False)

print(f"✅ Planilha com múltiplos cursos salva em:\n{ARQUIVO_SAIDA}")
