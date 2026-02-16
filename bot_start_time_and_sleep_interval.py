import yfinance as yf
import time
from datetime import datetime

# --- CONFIGURATION ---
ticker = "NVDA"
target_price = 170.00
sleep_interval = 30  # You can change this number easily here now

# 1. Capture the "Start Time" (Before the loop begins)
start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

print("--------------------------------------------------")
print(f"🤖 BOT INITIALIZED: {ticker} Tracker")
print(f"🕒 STARTED AT:      {start_time}")
print(f"⏱️  INTERVAL:        Every {sleep_interval} seconds")
print(f"🛑 STOP:            Press Ctrl + C")
print("--------------------------------------------------")

# --- THE INFINITE LOOP ---
while True:
    try:
        # Get the data
        stock = yf.Ticker(ticker)
        data = stock.history(period="1d")
        
        # Check if we actually got data (Sometimes internet hiccups happen)
        if not data.empty:
            current_price = data['Close'].iloc[-1]
            
            # Get current timestamp for this specific check
            check_time = datetime.now().strftime("%H:%M:%S")

            # Decision Logic
            if current_price > target_price:
                print(f"[{check_time}] 🚨 ALERT: ${current_price:.2f} (Target Met!)")
            else:
                print(f"[{check_time}] ... ${current_price:.2f} (Watching...)")
        else:
            print("⚠️ Error: No data received from Yahoo.")

    except Exception as e:
        # If the internet cuts out, don't crash! Just print the error and keep trying.
        print(f"⚠️ Connection Error: {e}")

    # Wait
    time.sleep(sleep_interval)