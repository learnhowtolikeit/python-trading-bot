import yfinance as yf
import time
from datetime import datetime, time as dtime
from win10toast import ToastNotifier # This is the new tool

# --- CONFIGURATION ---
ticker = "NVDA"
sma_window = 20       
sleep_interval = 30   

# Initialize the Notifier
toaster = ToastNotifier()

# --- THE TRICK (False Memory) ---
# We are lying to the bot. We tell it: "The trend WAS Bullish."
# Since the real trend is Bearish, it will see a "Change" and alert you instantly.
last_trend = "BULLISH" 

# Working Hours (Set to run all day for testing)
start_time = dtime(0, 0)
end_time   = dtime(23, 59)

print(f"--- 🔔 DESKTOP ALERT BOT INITIALIZED ---")
print(f"I will pop up a Windows notification if {ticker} flips trend.")
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
                # --- THE POPUP CODE ---
                print(f"[{timestamp}] 🚨 ALERT! Trend flipped to {current_trend}")
                
                toaster.show_toast(
                    f"NVDA Trade Alert!",
                    f"Price is now {current_trend} (${current_price:.2f})",
                    duration=10,
                    threaded=True
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