import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# App title
st.title("📈 Investment Strategy Backtester")

# Sidebar for user input
st.sidebar.header("Strategy Parameters")
ticker = st.sidebar.text_input("Stock Ticker (e.g., AAPL, TSLA)", "AAPL")
buy_drop = st.sidebar.slider("Buy when stock drops (%)", 1, 20, 5)
sell_gain = st.sidebar.slider("Sell when stock gains (%)", 1, 50, 20)
time_frame = st.sidebar.slider("Time Frame (Years)", 1, 10, 2)

# Fetch historical stock data
st.write(f"Fetching data for {ticker}...")
end_date = pd.Timestamp.now()
start_date = end_date - pd.DateOffset(years=time_frame)
data = yf.download(ticker, start=start_date, end=end_date, progress=False)

# Check if data is empty
if data.empty:
    st.error("Failed to retrieve data. Please check the stock ticker and try again.")
    st.stop()

# Display sample data
st.write("### Sample Data Retrieved")
st.dataframe(data.head())

# Flatten multi-index columns if needed
if isinstance(data.columns, pd.MultiIndex):
    data.columns = ['_'.join(col).strip() for col in data.columns.values]

# Dynamically detect the correct close price column
close_column = None
for col in data.columns:
    if "Close" in col:
        close_column = col
        break

if close_column is None:
    st.error("Close price column not found. Please check the data format.")
    st.stop()

# Convert Date to datetime if necessary
if 'Date' in data.columns:
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index('Date', inplace=True)

# Plot stock price chart
st.write("### Historical Price Chart")
st.line_chart(data[close_column])

# Backtesting function
def backtest(data, buy_drop, sell_gain, close_column):
    balance = 10000  # Initial balance in USD
    holdings = 0  # Number of stocks held
    last_buy_price = None
    trades = []

    for i in range(1, len(data)):
        daily_change = ((data[close_column].iloc[i] - data[close_column].iloc[i - 1]) / data[close_column].iloc[i - 1]) * 100

        if daily_change <= -buy_drop and holdings == 0:
            last_buy_price = data[close_column].iloc[i]
            holdings = 1  # Buy one stock
            balance -= last_buy_price
            trades.append({"date": data.index[i], "action": "BUY", "price": last_buy_price})
            st.write(f"✅ Bought at {last_buy_price:.2f} on {data.index[i].strftime('%Y-%m-%d')}")

        if holdings > 0 and ((data[close_column].iloc[i] / last_buy_price - 1) * 100) >= sell_gain:
            sell_price = data[close_column].iloc[i]
            balance += sell_price
            holdings = 0  # Sell the stock
            trades.append({"date": data.index[i], "action": "SELL", "price": sell_price})
            st.write(f"🔴 Sold at {sell_price:.2f} on {data.index[i].strftime('%Y-%m-%d')}")

    final_balance = balance + (holdings * data[close_column].iloc[-1] if holdings > 0 else 0)
    return final_balance, trades

# Run backtest
if st.sidebar.button("Run Backtest"):
    final_balance, trades = backtest(data, buy_drop, sell_gain, close_column)

    # Show results
    st.write("### Backtest Results")
    st.write(f"Final Portfolio Balance: ${final_balance:.2f}")

    # Display trade history
    st.write("### Trade History")
    trades_df = pd.DataFrame(trades)

    if not trades_df.empty:
        # Plot trades on the price chart
        fig, ax = plt.subplots()
        ax.plot(data[close_column], label="Stock Price", color="blue")
        buy_dates = trades_df[trades_df['action'] == 'BUY']['date']
        sell_dates = trades_df[trades_df['action'] == 'SELL']['date']
        ax.scatter(buy_dates, data.loc[buy_dates, close_column], marker="^", color="green", label="Buy", alpha=1)
        ax.scatter(sell_dates, data.loc[sell_dates, close_column], marker="v", color="red", label="Sell", alpha=1)
        ax.legend()
        st.pyplot(fig)

    st.dataframe(trades_df)


