# Python Algorithmic Trading Bot 📈
**Phase 1: Desktop Automation & Paper Trading**

## 📖 Overview
This project is an autonomous trading bot built in Python. It monitors live stock market data, calculates technical indicators in real-time, and executes "Paper Trades" (simulations) based on a strict confluence strategy.

It was designed to run 24/7 on a local machine, providing desktop alerts and persistent CSV logging for performance analysis.

## 🧠 The Strategy ("The Trifecta")
The bot uses a "Council of Elders" approach, requiring three distinct indicators to agree before logging a trade:

1.  **Trend Filter (SMA 20):** Determines the long-term direction. The bot strictly forbids buying if the price is below the 20-day Simple Moving Average.
2.  **Momentum Engine (MACD):** Uses the 12-26-9 standard setting to detect momentum shifts and crossovers.
3.  **Value Gauge (RSI 14):** Ensures entries are not "Overbought" (RSI > 70) or exits are not "Oversold" (RSI < 30).

**The Rule:** `IF (Trend == UP) AND (Momentum == POSITIVE) AND (Value == GOOD) -> EXECUTE TRADE`

## 🛠️ Tech Stack
* **Language:** Python 3.13
* **Data Feed:** `yfinance` (Yahoo Finance API) - *Live market data.*
* **Analysis:** `pandas_ta` - *Technical Analysis library for calculating indicators.*
* **Notifications:** `plyer` - *Native Windows desktop notifications.*
* **Logging:** Python `csv` module - *Generates Excel-compatible trade logs.*

## 📂 Project Structure
* `bot_paper_trader.py`: The main engine. Runs the infinite loop, handles logic, and logs trades.
* `trade_log.csv`: The "Diary." Automatically created to record every Buy/Sell decision with timestamps.
* `strategies/`: (Future) Placeholder for testing different logic sets.

## 🚀 How to Run
1.  **Install Dependencies:**
    ```bash
    pip install yfinance pandas_ta plyer
    ```
2.  **Launch the Bot:**
    ```bash
    python bot_paper_trader.py
    ```
3.  **Monitor:**
    * Watch for Windows Desktop Notifications.
    * Check `trade_log.csv` for trade history.

---
*Disclaimer: This software is for educational purposes only. It is a "Paper Trading" simulation and should not be used for real financial transactions without professional financial advice.*