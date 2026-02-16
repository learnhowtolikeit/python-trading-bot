print("1. Starting the bot...") 
import yfinance as yf
print("2. Library loaded successfully. Connecting to Yahoo Finance...")

# Define the stock
ticker_symbol = "NVDA" 
stock = yf.Ticker(ticker_symbol)

# Get data
print(f"3. Fetching data for {ticker_symbol}...")
data = stock.history(period="1d")
last_price = data['Close'].iloc[0]

# Print result
print("--------------------------------------------------")
print(f"SUCCESS: The price of {ticker_symbol} is ${last_price:.2f}")
print("--------------------------------------------------")