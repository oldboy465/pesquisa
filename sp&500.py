#S&P500

import yfinance as yf

# Obter dados históricos do S&P 500 (mensal)
sp500_data = yf.download('^GSPC', start='2000-01-01', end='2024-10-01', interval='1mo')

# Exibir os dados de fechamento mensal
print(sp500_data['Close'])
