import yfinance as yf
import time
from datetime import datetime

# --- CONFIGURATION ---
ticker = "NVDA"
target_price = 180.00  # We want to know if it's above this

print(f"--- STARTING BOT FOR {ticker} ---")
print(f"Tracking price... (Press Ctrl+C in the terminal to stop)")

# --- THE INFINITE LOOP ---
while True:
    # 1. Get the data
    stock = yf.Ticker(ticker)
    data = stock.history(period="1d")
    current_price = data['Close'].iloc[-1]
    
    # 2. Get the current timestamp (so we know when it checked)
    now = datetime.now().strftime("%H:%M:%S")

    # 3. Decision Logic (The "Brain")
    if current_price > target_price:
        # If price is HIGH, print an ALERT with an emoji
        print(f"[{now}] 🚨 ALERT: {ticker} is ${current_price:.2f} (Above ${target_price})")
    else:
        # If price is LOW, just print a status update
        print(f"[{now}] ... {ticker} is ${current_price:.2f} (Waiting...)")

    # 4. The Pause (Crucial!)
    # Wait for 10 seconds before looping again
    time.sleep(30)