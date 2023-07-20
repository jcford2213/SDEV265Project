import yfinance as yf

def getStockData(ticker):  
    try:  
      stock = yf.Ticker(ticker)
      stockInfo = stock.info
      ## Contain dataframes for historical price data for weeks and months
      dfWeek = stock.history(period="1wk")
      dfMonth = stock.history(period="1mo")
      ## Closing prices returned as pandas dataframes by yfinance
      closePricesWeek = dfWeek["Close"]
      closePricesMonth = dfMonth["Close"]
    except Exception as e:
       raise e
    else:
      return {
        'stockInfo': stockInfo,
        'closePricesWeek': closePricesWeek,
        'closePricesMonth': closePricesMonth,
      }






# ## Loop in selection to prevent error
# while True:
#     selection = input("View data for week or month? ")

#     if selection.lower() == "week":
#         print("Historical data for the prior week:")
#         print(close_prices_week)
#         break
#     elif selection.lower() == "month":
#         print("Historical data for the prior month:")
#         print(close_prices_month)
#         break
#     else:
#         print("Invalid")
