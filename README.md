# Projeto de Análise de Desistência no Ensino Superior

## Descrição do Projeto
Este projeto tem como objetivo analisar os fatores que contribuem para a desistência em cursos de graduação oferecidos por instituições federais de ensino superior no Brasil, utilizando dados do INEP entre os anos de 2018 e 2023. Técnicas de aprendizado de máquina foram aplicadas para prever a probabilidade de desistência e identificar padrões relacionados a desistência estudantil.

````

## Principais Funcionalidades
````
- **Pré-processamento de Dados**: Limpeza e transformação dos dados brutos.
- **Análise Exploratória (EDA)**: Identificação de padrões e insights iniciais.
- **Modelagem Preditiva**: Uso de ML para prever desistência.
- **Visualização de Dados**: Geração de gráficos para interpretação dos resultados.
````

## Como Usar
1. **Clone o repositório**:
   ```bash
   git clone https://github.com/eltonjmarinho/artigo-estatistica-desistencia.git
   cd projeto-evasao
````

2. **Instale as dependências**:

   ```bash
   pip install -r requirements.txt
   pip install -t requirements-dev.txt
   ```

3. **Incie o ambiente virtual**:
   ```
   # Ambiente virtual
   pip install virtualenv
   python -m venv venv
   source venv/Scripts/activate

   # Instalando os pacotes requeridos
   pip install -r requirements.txt
   ```
   
4. **Prepare os dados**:

   * Baixe os dados em: https://drive.google.com/drive/folders/1zi4h16h79umFseChfkg0X4p0SDzATSLy?usp=sharing
   * Coloque os arquivos de dados na mesma pasta dos scripts e notebooks.
   * Execute os scripts e notebooks que estão nas pastas /scripts e /notebooks.
   * obs: antes de executar os scripts altere o local padrão dos dados


5. **Leia o artigo**:

   ```bash
   python main.py
   ```

## Bibliotecas Utilizadas

* [Pandas](https://pandas.pydata.org/)
* [NumPy](https://numpy.org/)
* [Matplotlib](https://matplotlib.org/)
* [Seaborn](https://seaborn.pydata.org/)
* [Scikit-learn](https://scikit-learn.org/)

## Resultados Esperados

* Relatórios em /report em tex com as variáveis mais relevantes para a desistência.
* Visualizações que auxiliam na interpretação dos dados.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma issue ou enviar um pull request.

## Contato

* **Autor**: Elton John Marinho de Lima
* **E-mail**: [eltonjmarinho@gmail.com](mailto:eltonjmarinho@gmail.com)