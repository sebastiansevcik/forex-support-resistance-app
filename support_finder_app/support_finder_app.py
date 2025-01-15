import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# App title
st.title("📉 Support and Resistance Zones Finder for Forex")

# Sidebar for user input
st.sidebar.header("Forex Pair and Time Frame")

# Dropdown for common forex pairs
forex_pairs = [
    "EURUSD=X", "GBPUSD=X", "USDJPY=X", "AUDUSD=X", "USDCAD=X",
    "USDCHF=X", "NZDUSD=X", "EURGBP=X", "EURJPY=X", "GBPJPY=X"
]
ticker = st.sidebar.selectbox("Select Forex Pair", forex_pairs)

# Slider for time frame
time_frame = st.sidebar.slider("Time Frame (Days)", 1, 365, 30)

# Dropdown for time interval
interval = st.sidebar.selectbox("Time Interval", ["1d", "1h", "30m", "15m", "5m"])

# Fetch historical forex data
st.write(f"Fetching data for {ticker}...")
end_date = pd.Timestamp.now()
start_date = end_date - pd.DateOffset(days=time_frame)

# Check if the interval is supported
supported_intervals = ["1d", "1h", "30m", "15m", "5m"]
if interval not in supported_intervals:
    st.error("The selected interval is not supported. Please choose a valid interval.")
    st.stop()

try:
    data = yf.download(ticker, start=start_date, end=end_date, interval=interval, progress=False)
except Exception as e:
    st.error(f"Error fetching data: {e}")
    st.stop()

# Adjust column names for Forex pairs
if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)

# Check if data is empty or partially empty
if data.empty or data.isnull().values.any():
    st.warning("The retrieved data is partially empty or contains missing values. Proceeding with available data.")
    data.dropna(inplace=True)

# Ensure the necessary columns are present
required_columns = ["Low", "High", "Close", "Open"]
for col in required_columns:
    if col not in data.columns:
        st.error(f"The required column '{col}' is missing from the data. Please check the selected pair and interval.")
        st.stop()

# Display sample data
st.write("### Sample Data Retrieved")
st.dataframe(data.head())

# Function to calculate Average True Range (ATR)
def calculate_atr(data, period=14):
    data['High-Low'] = data['High'] - data['Low']
    data['High-PrevClose'] = np.abs(data['High'] - data['Close'].shift(1))
    data['Low-PrevClose'] = np.abs(data['Low'] - data['Close'].shift(1))
    true_range = data[['High-Low', 'High-PrevClose', 'Low-PrevClose']].max(axis=1)
    atr = true_range.rolling(window=period).mean()
    return atr

# Calculate ATR and use it as a dynamic tolerance
atr = calculate_atr(data)
data['ATR'] = atr
average_atr = atr.mean()

# Function to find support zones based on closing price reversals and ATR
def find_support_zones(data, min_tests=3):
    tolerance = average_atr / data['Close'].mean()  # Dynamic tolerance based on ATR
    support_levels = []
    support_strength = {}

    for i in range(1, len(data) - 1):
        if data['Close'].iloc[i] < data['Close'].iloc[i - 1] and data['Close'].iloc[i] < data['Close'].iloc[i + 1]:
            level = float(data['Close'].iloc[i])
            support_levels.append(level)
            support_strength[level] = support_strength.get(level, 0) + 1

    # Group nearby levels into zones and filter by the number of tests
    support_zones = []
    grouped_strength = []
    support_levels.sort()

    for level in support_levels:
        if not support_zones or abs(level - support_zones[-1]) > level * tolerance:
            support_zones.append(level)
            grouped_strength.append(support_strength[level])
        else:
            grouped_strength[-1] += support_strength[level]

    # Filter zones based on the minimum number of tests
    filtered_zones = [(zone, strength) for zone, strength in zip(support_zones, grouped_strength) if strength >= min_tests]

    return filtered_zones

# Function to find resistance zones based on closing price reversals and ATR
def find_resistance_zones(data, min_tests=3):
    tolerance = average_atr / data['Close'].mean()  # Dynamic tolerance based on ATR
    resistance_levels = []
    resistance_strength = {}

    for i in range(1, len(data) - 1):
        if data['Close'].iloc[i] > data['Close'].iloc[i - 1] and data['Close'].iloc[i] > data['Close'].iloc[i + 1]:
            level = float(data['Close'].iloc[i])
            resistance_levels.append(level)
            resistance_strength[level] = resistance_strength.get(level, 0) + 1

    # Group nearby levels into zones and filter by the number of tests
    resistance_zones = []
    grouped_strength = []
    resistance_levels.sort()

    for level in resistance_levels:
        if not resistance_zones or abs(level - resistance_zones[-1]) > level * tolerance:
            resistance_zones.append(level)
            grouped_strength.append(resistance_strength[level])
        else:
            grouped_strength[-1] += resistance_strength[level]

    # Filter zones based on the minimum number of tests
    filtered_zones = [(zone, strength) for zone, strength in zip(resistance_zones, grouped_strength) if strength >= min_tests]

    return filtered_zones

# Detect support and resistance zones
try:
    support_zones = find_support_zones(data)
    resistance_zones = find_resistance_zones(data)
except Exception as e:
    st.error(f"Error detecting zones: {e}")
    support_zones, resistance_zones = [], []

# Plot the candlestick chart with Plotly
fig = go.Figure()
fig.add_trace(go.Candlestick(
    x=data.index,
    open=data['Open'],
    high=data['High'],
    low=data['Low'],
    close=data['Close'],
    increasing_line_color='green',
    decreasing_line_color='red'
))

# Plot support zones with strength indicators
for level, strength in support_zones:
    fig.add_hline(y=level, line_color='green', line_dash='dash', annotation_text=f"Support: {level:.4f} ({strength} touches)")

# Plot resistance zones with strength indicators
for level, strength in resistance_zones:
    fig.add_hline(y=level, line_color='red', line_dash='dash', annotation_text=f"Resistance: {level:.4f} ({strength} touches)")

fig.update_layout(title=f"Support and Resistance Zones on {ticker} Chart ({interval} Interval)",
                  xaxis_title="Date",
                  yaxis_title="Price",
                  xaxis_rangeslider_visible=False)

# Display the chart
st.plotly_chart(fig)

# Show detected support and resistance zones with strength
st.write("### Detected Support Zones with Strength")
support_df = pd.DataFrame(support_zones, columns=["Support Zone Level", "Strength (Touches)"])
st.dataframe(support_df)

st.write("### Detected Resistance Zones with Strength")
resistance_df = pd.DataFrame(resistance_zones, columns=["Resistance Zone Level", "Strength (Touches)"])
st.dataframe(resistance_df)



