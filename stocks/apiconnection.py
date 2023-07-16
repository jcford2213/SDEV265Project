import yfinance as yf

def getStockData(ticker):  
    try:  
      stock = yf.Ticker(ticker)
      stockData = stock.info
    except Exception as e:
       raise e
    else:
      return stockData


