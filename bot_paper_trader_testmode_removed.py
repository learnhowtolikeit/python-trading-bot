import yfinance as yf
import pandas_ta as ta
import time
import csv  # <--- NEW TOOL: CSV Handler
import os   # <--- To check if file exists
from datetime import datetime, time as dtime
from plyer import notification

# --- CONFIGURATION ---
ticker = "NVDA"
sma_window = 20
rsi_window = 14
fast = 12
slow = 26
signal = 9
sleep_interval = 30 
log_file = "trade_log.csv" # The name of your diary

# --- TEST MODE (Set to True to force a CSV write immediately) ---
TEST_MODE = False 

# Working Hours
start_time = dtime(0, 0)
end_time   = dtime(23, 59)

# Memory
last_macd_cross = "NEUTRAL"

# --- THE LOGGER FUNCTION ---
def log_trade(action, price, reason):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Check if we need headers (first time run)
    file_exists = os.path.isfile(log_file)
    
    with open(log_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        # Write headers if new file
        if not file_exists:
            writer.writerow(["Timestamp", "Ticker", "Action", "Price", "Reason"])
        
        # Write the trade
        writer.writerow([timestamp, ticker, action, price, reason])
        print(f"📝 Logged to CSV: {action} at ${price}")

print(f"--- 📜 PAPER TRADER INITIALIZED ---")
print(f"I will save all trades to: {log_file}")
if TEST_MODE:
    print("⚠️ TEST MODE ON: I will force a fake trade log now.")
print("---------------------------------------------")

# --- FORCE TEST LOG ---
if TEST_MODE:
    print(">>> SIMULATING FAKE TRADE...")
    log_trade("BUY_TEST", 182.81, "Test Mode Verification")
    time.sleep(1) # Wait a second so you see it
    print(">>> Check your folder for trade_log.csv!")
    print("---------------------------------------------")

while True:
    now = datetime.now().time()
    timestamp = datetime.now().strftime("%H:%M:%S")

    # BOUNCER
    if now < start_time or now > end_time:
        print(f"[{timestamp}] 💤 Market Closed.")
        break

    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period="3mo") 
        
        if len(df) > 30:
            # 1. CALCULATE INDICATORS
            df['SMA'] = df['Close'].rolling(window=sma_window).mean()
            df['RSI'] = df.ta.rsi(length=rsi_window)
            macd_df = df.ta.macd(fast=fast, slow=slow, signal=signal)
            df = df.join(macd_df)

            # Get latest values
            price = df['Close'].iloc[-1]
            sma   = df['SMA'].iloc[-1]
            rsi   = df['RSI'].iloc[-1]
            
            macd_col   = f'MACD_{fast}_{slow}_{signal}'
            signal_col = f'MACDs_{fast}_{slow}_{signal}'
            macd_line   = df[macd_col].iloc[-1]
            signal_line = df[signal_col].iloc[-1]

            # 2. INTERPRET SIGNALS
            trend = "BULLISH" if price > sma else "BEARISH"
            
            rsi_status = "NEUTRAL"
            if rsi > 70: rsi_status = "OVERBOUGHT"
            elif rsi < 30: rsi_status = "OVERSOLD"

            macd_status = "BULLISH" if macd_line > signal_line else "BEARISH"

            # 3. PRINT DASHBOARD
            print(f"[{timestamp}] ${price:.2f} | Trend: {trend} | RSI: {rsi:.1f} | MACD: {macd_status}")

            # 4. DECISION LOGIC & LOGGING
            
            # BUY SIGNAL
            if macd_status == "BULLISH" and last_macd_cross == "BEARISH":
                if trend == "BULLISH":
                    msg = "MACD Cross + Uptrend"
                    notification.notify(title=f"BUY {ticker}", message=msg, timeout=10)
                    
                    # LOG IT!
                    log_trade("BUY", price, msg) 
                else:
                    print(">>> (Signal ignored: Trend is Bearish)")

            # SELL SIGNAL
            elif macd_status == "BEARISH" and last_macd_cross == "BULLISH":
                if trend == "BEARISH":
                    msg = "MACD Cross + Downtrend"
                    notification.notify(title=f"SELL {ticker}", message=msg, timeout=10)
                    
                    # LOG IT!
                    log_trade("SELL", price, msg) 

            # Update Memory
            last_macd_cross = macd_status

        else:
            print(f"⚠️ Not enough data.")

    except Exception as e:
        print(f"⚠️ Error: {e}")

    time.sleep(sleep_interval)