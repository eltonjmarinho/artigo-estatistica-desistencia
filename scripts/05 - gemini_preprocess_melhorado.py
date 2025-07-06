#USA O GEMINI PARA ANALISAR CADA CBO E COMPATIBILIZAR COM CURSOS

import os
import time
import json
import pandas as pd
from difflib import get_close_matches
import google.generativeai as genai
from tqdm import tqdm
import tkinter as tk
from tkinter import messagebox

# === CONFIGURAÇÃO ===

API_KEY = "api key"  # 🔐 Substitua pela sua chave
CAMINHO_BASE = r"C:\Users\john-\OneDrive - Universidade Federal da Paraíba\Área de Trabalho\Artigo - Estatística\projeto-evasao\data\processed"

ARQUIVO_CBO = os.path.join(CAMINHO_BASE, "cbo_unicos.csv")
ARQUIVO_CURSOS = os.path.join(CAMINHO_BASE, "cursos_unicos.csv")
ARQUIVO_SAIDA_CSV = os.path.join(CAMINHO_BASE, "resultado_match_cbo_cursos.csv")
ARQUIVO_SAIDA_XLSX = os.path.join(CAMINHO_BASE, "resultado_match_cbo_cursos.xlsx")
ARQUIVO_LOG_ERROS = os.path.join(CAMINHO_BASE, "log_erros.txt")
ARQUIVO_CACHE = os.path.join(CAMINHO_BASE, "cache_gemini.json")

# === INICIALIZAÇÃO ===

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash-preview-05-20')

# === FUNÇÕES DE ARQUIVOS ===

def carregar_dados():
    df_cbo = pd.read_csv(ARQUIVO_CBO)
    df_cursos = pd.read_csv(ARQUIVO_CURSOS)
    return df_cbo, df_cursos

def gerar_lista_cursos(df_cursos):
    cursos_unicos = df_cursos['ÁREA_DE_AVALIAÇÃO'].dropna().unique()
    cursos_formatados = [f"{curso} - {str(index).zfill(5)}" for index, curso in enumerate(cursos_unicos, start=1)]
    return "\n".join(cursos_formatados)

# === FUNÇÕES DE CACHE ===

def carregar_cache():
    if os.path.exists(ARQUIVO_CACHE):
        with open(ARQUIVO_CACHE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def salvar_cache(cache):
    with open(ARQUIVO_CACHE, 'w', encoding='utf-8') as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)

# === GEMINI ===

def consultar_gemini(cbo_nome, cursos_lista):
    prompt = f"""

    Você receberá uma ocupação do CBO e uma lista de cursos universitários no formato:

    NOME DO CURSO

    Apenas escolha UM curso da lista que seja o MAIS COMPATÍVEL com a ocupação dada.  
    NÃO EXPLIQUE, NÃO JUSTIFIQUE, NÃO ADICIONE NENHUM TEXTO.

    NÃO FAÇA MAIS DE UMA ESCOLHA.  
    Formato obrigatório da resposta: Nome do Curso

    A partir do nome de uma ocupação do CBO: "{cbo_nome}",
    identifique o único curso universitário mais compatível da lista abaixo (formato "Curso"):

    {cursos_lista}

    Responda com o único curso mais compatível no mesmo formato.
    """
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        with open(ARQUIVO_LOG_ERROS, 'a', encoding='utf-8') as f:
            f.write(f"[ERRO] {cbo_nome}: {str(e)}\n")
        return ""

# === PROCESSAMENTO PRINCIPAL ===

def processar_ocupacoes(df_cbo, cursos_lista, limit=5):
    cache = carregar_cache()
    resultados_cursos = []

    # Lista de cursos válidos
    lista_cursos_validos = [linha.strip().rsplit('-', 1)[0].strip() for linha in cursos_lista.split('\n') if '-' in linha]
    cursos_validos_set = set(lista_cursos_validos)

    # Contadores
    total = 0
    validados = 0
    fuzzy_corrigidos = 0
    nao_identificados = 0

    df_cbo = df_cbo.head(limit) if limit else df_cbo

    for _, row in tqdm(df_cbo.iterrows(), total=len(df_cbo), desc="Processando ocupações"):
        cbo_nome = row['cbo_ocup']
        total += 1

        if cbo_nome in cache:
            resultado = cache[cbo_nome]
        else:
            resultado = consultar_gemini(cbo_nome, cursos_lista)
            cache[cbo_nome] = resultado
            time.sleep(1)

        curso_final = resultado.strip()

        if curso_final in cursos_validos_set:
            curso_validado = curso_final
            validados += 1
        else:
            sugestoes = get_close_matches(curso_final, lista_cursos_validos, n=1, cutoff=0.95)

            if sugestoes:
                curso_validado = sugestoes[0]
                fuzzy_corrigidos += 1
                with open(ARQUIVO_LOG_ERROS, 'a', encoding='utf-8') as f:
                    f.write(f"[FUZZY MATCH 95%] {cbo_nome}: '{curso_final}' → '{curso_validado}'\n")
            else:
                curso_validado = "NÃO IDENTIFICADO"
                nao_identificados += 1
                with open(ARQUIVO_LOG_ERROS, 'a', encoding='utf-8') as f:
                    f.write(f"[CURSO INVÁLIDO] {cbo_nome}: '{curso_final}'\n")

        resultados_cursos.append(curso_validado)

    df_cbo['CURSOS'] = resultados_cursos
    salvar_cache(cache)

    relatorio = (
        f"\n📊 Relatório do Processamento:\n"
        f"Total de ocupações processadas: {total}\n"
        f"✔️ Cursos validados diretamente: {validados}\n"
        f"🧠 Corrigidos com fuzzy matching (≥95%): {fuzzy_corrigidos}\n"
        f"❌ Não identificados: {nao_identificados}"
    )
    print(relatorio)

    return df_cbo, relatorio

# === EXPORTAÇÃO ===

def salvar_resultados(df_final):
    df_final.drop(columns=['CO_CURSOS'], errors='ignore', inplace=True)
    df_final.to_csv(ARQUIVO_SAIDA_CSV, index=False)
    df_final.to_excel(ARQUIVO_SAIDA_XLSX, index=False)
    print(f"\n✅ Arquivos salvos:\nCSV: {ARQUIVO_SAIDA_CSV}\nExcel: {ARQUIVO_SAIDA_XLSX}")

# === FLUXO PRINCIPAL ===

def executar_processo(limit=5):
    try:
        print("🔄 Carregando dados...")
        df_cbo, df_cursos = carregar_dados()

        print("🧠 Gerando lista de cursos...")
        lista_cursos_str = gerar_lista_cursos(df_cursos)

        print("🤖 Consultando Gemini...")
        df_resultado, relatorio = processar_ocupacoes(df_cbo, lista_cursos_str, limit=limit)

        print("💾 Salvando arquivos...")
        salvar_resultados(df_resultado)

        messagebox.showinfo("Concluído", f"Processamento finalizado com sucesso!\n\n{relatorio}")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro durante o processo:\n{str(e)}")

# === INTERFACE GRÁFICA ===

def iniciar_interface():
    window = tk.Tk()
    window.title("Match CBO x Cursos (Gemini)")
    window.geometry("420x250")

    tk.Label(window, text="Número de linhas a processar (ou 0 para tudo):").pack(pady=10)
    entry = tk.Entry(window)
    entry.insert(0, "5")
    entry.pack()

    def on_run():
        try:
            valor = int(entry.get())
            limite = None if valor <= 0 else valor
            executar_processo(limit=limite)
        except ValueError:
            messagebox.showerror("Entrada inválida", "Digite um número inteiro válido.")

    tk.Button(window, text="Iniciar Processamento", command=on_run, bg="#4CAF50", fg="white", padx=10, pady=5).pack(pady=20)
    tk.Button(window, text="Sair", command=window.destroy).pack(pady=5)

    window.mainloop()

# === EXECUÇÃO ===

if __name__ == "__main__":
    iniciar_interface()
