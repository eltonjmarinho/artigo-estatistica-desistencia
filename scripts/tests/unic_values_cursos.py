import pandas as pd
import os
import sys

# --- Constantes ---
# Define o caminho do projeto dinamicamente, subindo um nível a partir da pasta 'scripts'.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DATA_PATH = os.path.join(PROJECT_ROOT, "data", "processed")

# Arquivos de entrada e saída
INPUT_FILE_PATH = os.path.join(PROCESSED_DATA_PATH, "ml_iq_2018_2023.csv")
OUTPUT_FILE_PATH = os.path.join(PROCESSED_DATA_PATH, "cursos_unicos.csv")

# Nomes das colunas para evitar "strings mágicas"
AREA_AVALIACAO_COL = 'ÁREA_DE_AVALIAÇÃO'
CODIGO_CURSO_COL = 'CÓDIGO_DO_CURSO'


def extrair_cursos_unicos(arquivo_entrada: str, arquivo_saida: str):
    """
    Carrega um arquivo CSV, extrai os cursos únicos com base nas colunas
    de área de avaliação e código, e salva o resultado em um novo CSV.
    """
    # 1. Checa se o arquivo de entrada existe
    if not os.path.exists(arquivo_entrada):
        print(f"❌ Erro: Arquivo de entrada não encontrado em:\n{arquivo_entrada}")
        sys.exit(1)

    # 2. Carrega o arquivo CSV
    print(f"🔄 Carregando dados de {os.path.basename(arquivo_entrada)}...")
    df = pd.read_csv(arquivo_entrada)

    # 3. Filtra valores únicos e remove nulos
    print("🔎 Filtrando cursos únicos...")
    colunas_interesse = [AREA_AVALIACAO_COL, CODIGO_CURSO_COL]
    cursos = df[colunas_interesse].drop_duplicates().dropna()

    # 4. Salva o DataFrame em um novo arquivo CSV
    print(f"💾 Salvando arquivo em {os.path.basename(arquivo_saida)}...")
    cursos.to_csv(arquivo_saida, index=False, encoding='utf-8-sig')

    # 5. Confirmação final
    print(f"✅ Arquivo salvo com {len(cursos)} cursos únicos em:\n{arquivo_saida}")


def main():
    """Função principal para executar o script."""
    extrair_cursos_unicos(INPUT_FILE_PATH, OUTPUT_FILE_PATH)


if __name__ == "__main__":
    main()
