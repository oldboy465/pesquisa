import wbdata
import pandas as pd
import datetime

# Definindo a data inicial e final
start_date = datetime.datetime(2000, 1, 1)
end_date = datetime.datetime(2024, 10, 1)

# Dicionário com os códigos dos indicadores do Banco Mundial
indicadores = {
    'SI.POV.GINI': 'Índice de Gini',              # Índice de Gini
    'NY.GDP.PCAP.CD': 'PIB per capita',           # PIB per capita
    'EP.PET.CONS': 'Produção de petróleo',         # Produção de petróleo
}

# Função para carregar os dados dos indicadores
def carregar_dados(indicador):
    # Obtendo dados do indicador
    df = wbdata.get_dataframe({indicador: indicadores[indicador]}, 
                               country='BRA')

    # Verifique a estrutura do DataFrame
    print(f"Dados para {indicadores[indicador]}: \n{df.head()}\n")  # Verifique as primeiras linhas do DataFrame

    # Checar se o índice é de fato um datetime
    if isinstance(df.index, pd.MultiIndex):
        df.index = df.index.get_level_values(1)  # Pega o nível do índice que representa o tempo

    # Garantindo que o índice seja do tipo datetime
    df.index = pd.to_datetime(df.index)

    # Filtrando os dados pelo intervalo de datas
    df = df[(df.index >= start_date) & (df.index <= end_date)]
    
    return df

# Criando um dicionário para armazenar os dados
dados_world_bank = {}

# Carregando os dados para cada indicador
for codigo in indicadores.keys():
    try:
        dados_world_bank[indicadores[codigo]] = carregar_dados(codigo)
    except Exception as e:
        print(f"Erro ao carregar dados para {indicadores[codigo]}: {e}")

# Exibir os dados combinados
for nome, df in dados_world_bank.items():
    print(f"Dados para {nome}:")
    print(df)
    print("\n")
