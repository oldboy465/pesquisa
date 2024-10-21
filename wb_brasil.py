#Biblioteca WB Brasil

import wbdata
import pandas as pd
import datetime

# Definindo a data inicial e final
start_date = datetime.datetime(2000, 1, 1)
end_date = datetime.datetime(2024, 10, 1)

# Listar todos os indicadores disponíveis
indicadores = wbdata.get_indicators()

# Exibir os códigos e os nomes dos indicadores
for indicador in indicadores:
    print(f"{indicador['id']}: {indicador['name']}")

# Criar um dicionário para os indicadores que você deseja
indicadores_desejados = {
    'SI.POV.GINI': 'Índice de Gini',              # Índice de Gini
    'NY.GDP.PCAP.CD': 'PIB per capita',           # PIB per capita
    'EP.PET.PROD': 'Produção de petróleo',         # Produção de petróleo
}

# Função para carregar os dados dos indicadores
def carregar_dados(indicador):
    # Obtendo dados do indicador apenas para o Brasil
    df = wbdata.get_dataframe({indicador: indicadores_desejados[indicador]}, 
                               country='BRA')

    # Garantindo que o índice seja do tipo datetime
    df.index = pd.to_datetime(df.index)

    # Filtrando os dados pelo intervalo de datas
    df = df[(df.index >= start_date) & (df.index <= end_date)]
    
    return df

# Criando um dicionário para armazenar os dados
dados_world_bank = {}

# Carregando os dados para cada indicador
for codigo in indicadores_desejados.keys():
    try:
        dados_world_bank[indicadores_desejados[codigo]] = carregar_dados(codigo)
    except Exception as e:
        print(f"Erro ao carregar dados para {indicadores_desejados[codigo]}: {e}")

# Exibir os dados combinados
for nome, df in dados_world_bank.items():
    print(f"Dados para {nome}:")
    print(df)
    print("\n")
