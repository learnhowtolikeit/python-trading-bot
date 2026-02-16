import yfinance as yf
import time
from datetime import datetime, time as dtime # Renamed to avoid confusion

# --- 1. CONFIGURATION (Edit these!) ---
ticker = "NVDA"
target_price = 180.00
sleep_interval = 30 

# Define your "Working Hours" (24-hour format)
start_time = dtime(9, 30)  # 9:30 AM
end_time   = dtime(14, 10)  # 4:00 PM

print(f"--- 🤖 SCHEDULED BOT INITIALIZED ---")
print(f"Checking {ticker} every {sleep_interval} seconds")
print(f"Operating Hours: {start_time} to {end_time}")
print("---------------------------------------")

# --- THE INFINITE LOOP ---
while True:
    # Get the current time (Time of day only)
    now = datetime.now().time()
    current_timestamp = datetime.now().strftime("%H:%M:%S")

    # --- THE "BOUNCER" LOGIC ---
    
    # CASE 1: It's too early? -> Wait
    if now < start_time:
        print(f"[{current_timestamp}] 💤 Market not open yet. Waiting...")
        time.sleep(60) # Sleep for a minute to save processing power
        continue # Skip the rest of the loop and start over

    # CASE 2: It's too late? -> Quit
    if now > end_time:
        print(f"[{current_timestamp}] 🛑 Market Closed. Shutting down bot.")
        break # This KILLS the loop and ends the program

    # CASE 3: We are in business! (Trading Logic)
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period="1d")
        
        if not data.empty:
            price = data['Close'].iloc[-1]
            
            if price > target_price:
                print(f"[{current_timestamp}] 🚨 ALERT: ${price:.2f} > ${target_price}")
            else:
                print(f"[{current_timestamp}] ... ${price:.2f} (Monitoring)")
        else:
            print(f"[{current_timestamp}] ⚠️ No Data Found")

    except Exception as e:
        print(f"⚠️ Error: {e}")

    # Wait for the next check
    time.sleep(sleep_interval)

print("--- End of Script ---")