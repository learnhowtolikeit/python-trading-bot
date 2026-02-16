import yfinance as yf
import pandas as pd
import time
from datetime import datetime, time as dtime

# --- CONFIGURATION ---
ticker = "NVDA"
sma_window = 20       # "The 20-Day Average"
sleep_interval = 30   # Check every 30 seconds

# Define "Working Hours" (Adjust to test right now!)
start_time = dtime(0, 0)   # Midnight (Runs all day for testing)
end_time   = dtime(23, 59) # Midnight

print(f"--- 📈 ANALYST BOT INITIALIZED ---")
print(f"Tracking: {ticker}")
print(f"Strategy: Price vs {sma_window}-Period SMA")
print("---------------------------------------")

while True:
    now = datetime.now().time()
    timestamp = datetime.now().strftime("%H:%M:%S")

    # --- THE BOUNCER (Simplified for testing) ---
    if now < start_time or now > end_time:
        print(f"[{timestamp}] 💤 Market Closed.")
        break

    try:
        # 1. GET DATA (We need 1 month to calculate a 20-day average)
        stock = yf.Ticker(ticker)
        # We fetch '1mo' history to ensure we have at least 20 days
        df = stock.history(period="1mo") 
        
        if len(df) >= sma_window:
            # 2. CALCULATE THE MATH (The "Data Science" part)
            # This one line does all the heavy lifting:
            df['SMA'] = df['Close'].rolling(window=sma_window).mean()
            
            # Get the very latest values
            current_price = df['Close'].iloc[-1]
            current_sma   = df['SMA'].iloc[-1]
            
            # 3. DECISION LOGIC (Bullish or Bearish?)
            trend = "NEUTRAL"
            signal = "⚪"
            
            if current_price > current_sma:
                trend = "BULLISH (Up Trend)"
                signal = "🟢"
            elif current_price < current_sma:
                trend = "BEARISH (Down Trend)"
                signal = "🔴"

            # 4. THE DASHBOARD PRINT
            print(f"[{timestamp}] {signal} {ticker}: ${current_price:.2f} | SMA({sma_window}): ${current_sma:.2f} | Trend: {trend}")
            
        else:
            print(f"⚠️ Not enough data to calculate SMA. Need {sma_window} days, got {len(df)}.")

    except Exception as e:
        print(f"⚠️ Error: {e}")

    time.sleep(sleep_interval)