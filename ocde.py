import wbdata
import pandas as pd

# Definindo o país e o período de tempo
pais = 'BRA'  # Código do Brasil
start_date = '2010-01-01'  # Data de início
end_date = '2024-10-01'  # Data de fim

# Indicadores da OECD
indicadores = {
    "SL.UEM.TOTL.ZS": "Taxa de desemprego",  # Taxa de desemprego (% da força de trabalho total)
    "NY.GDP.MKTP.CD": "PIB",  # PIB (US$ correntes)
    "FP.CPI.TOTL": "Taxa de inflação"  # Taxa de inflação (variação percentual anual)
}

# Função para carregar os dados
def carregar_dados(indicador):
    df = wbdata.get_dataframe({indicador: indicadores[indicador]}, country=pais)
    df = df[(df.index >= start_date) & (df.index <= end_date)]
    return df

# Carregando e exibindo os dados
dados_oecd = {}
for codigo in indicadores.keys():
    try:
        dados_oecd[indicadores[codigo]] = carregar_dados(codigo)
    except Exception as e:
        print(f"Erro ao carregar dados para {indicadores[codigo]}: {e}")

# Exibindo os dados
for nome, df in dados_oecd.items():
    print(f"\n{nome}:")
    print(df)
