import yfinance as yf
import pandas_ta as ta
import time
from datetime import datetime, time as dtime
from plyer import notification

# --- CONFIGURATION ---
ticker = "NVDA"
sma_window = 20
rsi_window = 14
# MACD Settings (Standard: 12, 26, 9)
fast = 12
slow = 26
signal = 9

sleep_interval = 30 

# Memory for MACD (to detect crosses)
last_macd_cross = "NEUTRAL"

# Working Hours (Set to run all day for testing)
start_time = dtime(0, 0)
end_time   = dtime(23, 59)

print(f"--- 🚀 TRIFECTA BOT INITIALIZED ---")
print(f"Tracking: {ticker}")
print(f"Strategy: SMA({sma_window}) + RSI({rsi_window}) + MACD({fast},{slow},{signal})")
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
        # MACD needs more data to stabilize, fetching 3 months
        df = stock.history(period="3mo") 
        
        if len(df) > 30:
            # 1. CALCULATE ALL INDICATORS
            # SMA
            df['SMA'] = df['Close'].rolling(window=sma_window).mean()
            # RSI
            df['RSI'] = df.ta.rsi(length=rsi_window)
            # MACD (Returns 3 columns: MACD, Histogram, Signal)
            macd_df = df.ta.macd(fast=fast, slow=slow, signal=signal)
            
            # Merge MACD back into main dataframe
            df = df.join(macd_df)

            # Get latest values
            price = df['Close'].iloc[-1]
            sma   = df['SMA'].iloc[-1]
            rsi   = df['RSI'].iloc[-1]
            
            # MACD column names are dynamic, usually: MACD_12_26_9 and MACDs_12_26_9
            macd_col   = f'MACD_{fast}_{slow}_{signal}'
            signal_col = f'MACDs_{fast}_{slow}_{signal}'
            
            macd_line   = df[macd_col].iloc[-1]
            signal_line = df[signal_col].iloc[-1]

            # 2. INTERPRET SIGNALS
            
            # A. Trend (SMA)
            trend = "BULLISH" if price > sma else "BEARISH"
            
            # B. Momentum (RSI)
            rsi_status = "NEUTRAL"
            if rsi > 70: rsi_status = "OVERBOUGHT"
            elif rsi < 30: rsi_status = "OVERSOLD"

            # C. Engine (MACD Cross)
            # If MACD > Signal Line = Bullish Momentum
            macd_status = "BULLISH" if macd_line > signal_line else "BEARISH"

            # 3. PRINT DASHBOARD
            print(f"[{timestamp}] ${price:.2f} | Trend: {trend} | RSI: {rsi:.1f} ({rsi_status}) | MACD: {macd_status}")

            # 4. SMART ALERTS (The "Perfect Storm")
            # We look for CONFLUENCE: Trend is Up + RSI is Good + MACD Just Crossed Up
            
            # Check for MACD Crossover (The Trigger)
            if macd_status == "BULLISH" and last_macd_cross == "BEARISH":
                # Only alert if the Trend is ALSO Bullish (Safety Filter)
                if trend == "BULLISH":
                    msg = f"GOLDEN TRADE! MACD Crossed Up + Uptrend confirmed."
                    print(f">>> 💎 {msg}")
                    notification.notify(title=f"BUY {ticker}", message=msg, timeout=10)
                else:
                    print(">>> (MACD Crossed Up, but Trend is Bearish... waiting)")

            elif macd_status == "BEARISH" and last_macd_cross == "BULLISH":
                if trend == "BEARISH":
                    msg = f"DANGER! MACD Crossed Down + Downtrend confirmed."
                    print(f">>> 💀 {msg}")
                    notification.notify(title=f"SELL {ticker}", message=msg, timeout=10)

            # Update Memory
            last_macd_cross = macd_status

        else:
            print(f"⚠️ Not enough data.")

    except Exception as e:
        print(f"⚠️ Error: {e}")

    time.sleep(sleep_interval)