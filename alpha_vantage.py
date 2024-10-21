import pandas as pd
from alpha_vantage.foreignexchange import ForeignExchange

# Substitua 'YOUR_API_KEY' pela sua chave da API
api_key = 'YOUR_API_KEY'
fx = ForeignExchange(key=api_key)

# Obter dados diários do USD/BRL (formato: daily)
dolar_data, _ = fx.get_currency_exchange_daily(from_symbol='USD', to_symbol='BRL', outputsize='full')

# Converter para DataFrame
dolar_df = pd.DataFrame(dolar_data).T  # Transpor para que as datas fiquem como índice
dolar_df.index = pd.to_datetime(dolar_df.index)  # Converter o índice para datas
dolar_df = dolar_df.astype(float)  # Converter colunas para numérico

# Reamostrar os dados para o último valor de cada mês (de 01/01/2000 até 01/10/2024)
dolar_monthly = dolar_df['4. close'].resample('M').last()

# Filtrar o período desejado
dolar_monthly = dolar_monthly['2000-01-01':'2024-10-01']

# Exibir o resultado
print(dolar_monthly)
