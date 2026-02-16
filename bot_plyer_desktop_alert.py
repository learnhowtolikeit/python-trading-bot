import yfinance as yf
import time
from datetime import datetime, time as dtime
from plyer import notification  # <--- NEW MODERN TOOL

# --- CONFIGURATION ---
ticker = "NVDA"
sma_window = 20       
sleep_interval = 30   

# --- THE TRICK (False Memory) ---
# We force the bot to think the trend WAS Bullish.
# Since it is currently Bearish, it will scream immediately.
last_trend = "BULLISH" 

# Working Hours
start_time = dtime(0, 0)
end_time   = dtime(23, 59)

print(f"--- 🔔 DESKTOP ALERT BOT INITIALIZED ---")
print(f"I will pop up a notification if {ticker} flips trend.")
print("---------------------------------------")

while True:
    now = datetime.now().time()
    timestamp = datetime.now().strftime("%H:%M:%S")

    # BOUNCER
    if now < start_time or now > end_time:
        print(f"[{timestamp}] 💤 Market Closed.")
        break

    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period="1mo") 
        
        if len(df) >= sma_window:
            df['SMA'] = df['Close'].rolling(window=sma_window).mean()
            current_price = df['Close'].iloc[-1]
            current_sma   = df['SMA'].iloc[-1]
            
            # Trend Logic
            current_trend = "BULLISH" if current_price > current_sma else "BEARISH"

            # --- DECISION ---
            if current_trend != last_trend:
                # --- NEW POPUP CODE ---
                print(f"[{timestamp}] 🚨 ALERT! Trend flipped to {current_trend}")
                
                notification.notify(
                    title=f"NVDA Trade Alert!",
                    message=f"Price is now {current_trend} (${current_price:.2f})",
                    timeout=10
                )
                # ----------------------
                
                last_trend = current_trend

            else:
                print(f"[{timestamp}] ... {ticker} is {current_trend}")
            
        else:
            print(f"⚠️ Not enough data.")

    except Exception as e:
        print(f"⚠️ Error: {e}")

    time.sleep(sleep_interval)