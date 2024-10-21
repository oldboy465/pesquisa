#IPEA DATA

import requests
import pandas as pd

# Função para obter dados do IPEADATA
def obter_dados_ipeadata(serie, start_date, end_date):
    url = f'https://api.ipeadata.gov.br/api/values/serie/{serie}/{start_date}/{end_date}/json'
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Erro ao obter dados: {response.status_code}")
        print(response.text)  # Exibir a resposta para depuração
        response.raise_for_status()  # Levanta um erro se a requisição falhar
    
    return response.json()

# Definir as séries do IPEADATA e as datas
series_ipeadata = {
    'IPCA': 433,               # IPCA
    'Índice de Gini': 4446,   # Índice de Gini
    'Salário mínimo': 421,     # Salário mínimo
    'Taxa de inflação': 433,   # Taxa de inflação (considerando IPCA)
    'PIB': 12,                 # PIB
    'Renda per capita': 193,   # Renda per capita
}

# Definir o período (T)
start_date = '2000-01-01'
end_date = '2024-10-01'

# Obter os dados das séries
dados_ipeadata = {}
for nome, codigo in series_ipeadata.items():
    dados_ipeadata[nome] = obter_dados_ipeadata(codigo, start_date, end_date)

# Função para transformar os dados em DataFrame
def transformar_dados_em_df(data):
    df = pd.DataFrame(data)
    df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y')
    df.set_index('data', inplace=True)
    return df[['valor']]

# Transformar os dados em DataFrames
dataframes_ipeadata = {nome: transformar_dados_em_df(dados) for nome, dados in dados_ipeadata.items()}

# Reamostrar para obter a periodicidade mensal (último valor de cada mês)
dados_mensais = {nome: df.resample('M').last() for nome, df in dataframes_ipeadata.items()}

# Combinar as variáveis em um único DataFrame
dados_macro = pd.concat(dados_mensais.values(), axis=1)

# Renomear as colunas
dados_macro.columns = dados_mensais.keys()

# Exibir os dados combinados
print(dados_macro)
