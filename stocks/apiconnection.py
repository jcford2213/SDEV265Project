import yfinance as yf

ticker = input("")

# Fetch stock information using yfinance
stock = yf.Ticker(ticker_symbol)

# Get stock information
stock_info = stock.info

# Access specific data from the stock_info dictionary
company_name = stock_info['longName']
stock_price = stock_info['regularMarketPrice']
# ... add more data points as needed

# Print the retrieved information
print("Company Name:", company_name)
print("Stock Price:", stock_price)

########################################
## Above is practice for the API and its data types.
########################################
## Below is all relevant stock information of
## the users selected ticker
########################################

