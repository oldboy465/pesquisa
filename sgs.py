import requests
import pandas as pd

# Função para obter dados do SGS
def obter_dados_sgs(codigo, data_inicial, data_final):
    url = f'https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados?formato=json&dataInicial={data_inicial}&dataFinal={data_final}'
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Erro ao obter dados: {response.status_code}")
        print(response.text)  # Exibir a resposta para depuração
        response.raise_for_status()  # Levanta um erro se a requisição falhar
    
    return response.json()

# Definir os códigos das séries temporais e as datas
codigo_selic = 20542  # Taxa SELIC
codigo_ipca = 433     # IPCA
codigo_gini = 4446    # Índice de Gini

# Definir o período
start_date = '01/01/2000'
end_date = '01/10/2024'

# Obter os dados das séries
try:
    selic_data = obter_dados_sgs(codigo_selic, start_date, end_date)
    ipca_data = obter_dados_sgs(codigo_ipca, start_date, end_date)
    gini_data = obter_dados_sgs(codigo_gini, start_date, end_date)
except Exception as e:
    print(f"Ocorreu um erro: {e}")

# Função para transformar os dados em DataFrame
def transformar_dados_em_df(data):
    df = pd.DataFrame(data)
    df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y')
    df.set_index('data', inplace=True)
    return df[['valor']]

# Transformar os dados em DataFrames
selic_df = transformar_dados_em_df(selic_data)
ipca_df = transformar_dados_em_df(ipca_data)
gini_df = transformar_dados_em_df(gini_data)

# Reamostrar para obter a periodicidade mensal (último valor de cada mês)
selic_mensal = selic_df.resample('M').last()
ipca_mensal = ipca_df.resample('M').last()
gini_mensal = gini_df.resample('M').last()

# Combinar as variáveis em um único DataFrame
dados_macro = pd.concat([selic_mensal, ipca_mensal, gini_mensal], axis=1)

# Renomear as colunas
dados_macro.columns = ['Taxa SELIC', 'IPCA', 'Índice de Gini']

# Exibir os dados combinados
print(dados_macro)
