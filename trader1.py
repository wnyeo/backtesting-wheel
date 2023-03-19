import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf # For downloading historical price data of the ETF

# Download historical price data for SPDR S&P 500 ETF Trust
symbol = "SPY"
data = yf.download(symbol, start="2010-01-01", end="2019-12-31")

# Calculate daily returns and cumulative returns
data["daily_return"] = data["Close"].pct_change()
data["cumulative_return"] = (1 + data["daily_return"]).cumprod()

# Calculate buy and hold returns
start_price = data.iloc[0]["Close"]
end_price = data.iloc[-1]["Close"]
buy_hold_return = (end_price / start_price - 1)

# Print the buy and hold return
print("Buy and Hold Return: {:.2f}%".format(buy_hold_return * 100))

# Plot cumulative returns
data["cumulative_return"].plot(figsize=(10,6))
plt.title("Cumulative Return of SPDR S&P 500 ETF Trust (SPY)")
plt.xlabel("Date")
plt.ylabel("Cumulative Return")
plt.show()
