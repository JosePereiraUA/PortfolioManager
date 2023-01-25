import yfinance as yf
data = yf.Ticker("0P0000ZFDE.F")
hist = data.history(period="max")