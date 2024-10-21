#Bovespa
import yfinance as yf
bovespa_data = yf.download('^BVSP', start='2000-01-01', end='2024-10-01', interval='1mo')
print(bovespa_data['Close'])
