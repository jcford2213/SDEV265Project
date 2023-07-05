import yfinance as yf

def getStockData(ticker):    
    stock = yf.Ticker(ticker)
    stockData = stock.info
    return stockData


