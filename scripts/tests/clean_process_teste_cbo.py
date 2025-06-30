import pandas as pd
import os
import re

# Caminhos
base_path = r"C:\Users\john-\OneDrive - Universidade Federal da Paraíba\Área de Trabalho\Artigo - Estatística\projeto-evasao\data\processed"
arquivo_entrada_cursos = "resultado_match_cbo_cursos.csv"
caminho_entrada_cursos = os.path.join(base_path, arquivo_entrada_cursos)

# Leitura do CSV
df_cursos = pd.read_csv(caminho_entrada_cursos)

# Exibe colunas disponíveis (debug)
print("Colunas disponíveis:", df_cursos.columns.tolist())

# Nome da coluna com os códigos dos cursos
coluna_codigo = "CO_CURSOS"

# Função para extrair apenas o primeiro grupo de 5 dígitos
def extrair_codigo(texto):
    if pd.isna(texto):
        return ''
    match = re.search(r"\b\d{5}\b", str(texto))
    return match.group(0) if match else ''

# Aplica a função
df_cursos[coluna_codigo] = df_cursos[coluna_codigo].apply(extrair_codigo)

# Define colunas para exportar
colunas_para_salvar = []
if "cbo_ocup" in df_cursos.columns:
    colunas_para_salvar.append("cbo_ocup")
colunas_para_salvar.append(coluna_codigo)

# Cria DataFrame final
df_final = df_cursos[colunas_para_salvar]

# Salvar os arquivos
saida_csv = os.path.join(base_path, "cursos_pronto.csv")
saida_xlsx = os.path.join(base_path, "cursos_pronto.xlsx")

df_final.to_csv(saida_csv, index=False)
df_final.to_excel(saida_xlsx, index=False, engine="openpyxl")

print(f"\n✅ Arquivos salvos com sucesso em:\n- {saida_csv}\n- {saida_xlsx}")





