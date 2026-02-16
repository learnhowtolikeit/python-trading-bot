import yfinance as yf
import pandas as pd
import time
from datetime import datetime, time as dtime

# --- CONFIGURATION ---
ticker = "NVDA"
sma_window = 20       
sleep_interval = 15 

# "Memory" Variable (This stores what happened last time)
last_trend = "BULLISH"

# Define Working Hours (00:00 to 23:59 for testing)
start_time = dtime(0, 0)
end_time   = dtime(23, 59)

print(f"--- 🎯 CROSSOVER HUNTER INITIALIZED ---")
print(f"Tracking: {ticker} | Signal: Price Crossing SMA({sma_window})")
print("---------------------------------------")

while True:
    now = datetime.now().time()
    timestamp = datetime.now().strftime("%H:%M:%S")

    # --- BOUNCER ---
    if now < start_time or now > end_time:
        print(f"[{timestamp}] 💤 Market Closed.")
        break

    try:
        # 1. GET DATA
        stock = yf.Ticker(ticker)
        df = stock.history(period="1mo") 
        
        if len(df) >= sma_window:
            # 2. CALCULATE SMA
            df['SMA'] = df['Close'].rolling(window=sma_window).mean()
            
            current_price = df['Close'].iloc[-1]
            current_sma   = df['SMA'].iloc[-1]
            
            # 3. DETERMINE CURRENT TREND
            current_trend = "NEUTRAL"
            if current_price > current_sma:
                current_trend = "BULLISH"
            elif current_price < current_sma:
                current_trend = "BEARISH"

            # 4. COMPARE WITH MEMORY (The "Smart" Part)
            
            # Scenario A: First Run (Initialize Memory)
            if last_trend is None:
                last_trend = current_trend
                print(f"[{timestamp}] 🏁 BASELINE ESTABLISHED: {current_trend}")
                print(f"Bot is now waiting for a change... (Quiet Mode)")

            # Scenario B: CHANGE DETECTED! (The Crossover)
            elif current_trend != last_trend:
                print("--------------------------------------------------")
                if current_trend == "BULLISH":
                    print(f"[{timestamp}] 🚀 GOLDEN CROSS ALERT! Price crossed ABOVE Average.")
                    print(f"Action: Consider BUY (Price: ${current_price:.2f})")
                else:
                    print(f"[{timestamp}] 📉 DEATH CROSS ALERT! Price crossed BELOW Average.")
                    print(f"Action: Consider SELL (Price: ${current_price:.2f})")
                print("--------------------------------------------------")
                
                # Update memory so it doesn't spam the same alert again
                last_trend = current_trend

            # Scenario C: No Change (Heartbeat)
            else:
                # Just print a small dot so you know it's alive
                print(f"[{timestamp}] ... No change (${current_price:.2f} is still {current_trend})")
            
        else:
            print(f"⚠️ Not enough data.")

    except Exception as e:
        print(f"⚠️ Error: {e}")

    time.sleep(sleep_interval)