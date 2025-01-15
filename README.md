# forex-support-resistance-app
A Streamlit app to find support and resistance zones for Forex pairs
# 📈 Trading App
A **Streamlit-powered web app** that helps traders analyze **support and resistance zones** in **Forex pairs** using **technical indicators** like **ATR (Average True Range)** and **closing price reversals**. This app allows traders to detect key levels in various time frames and intervals, improving their decision-making in the financial markets.

---

## 🚀 Features
- Detect **support and resistance zones** dynamically based on **closing price reversals**.
- Uses **ATR-based tolerance** to adjust zone detection for different market conditions.
- Works with common **Forex pairs** (e.g., EUR/USD, GBP/USD, USD/JPY).
- Interactive **candlestick charts** with annotated support and resistance levels.
- Multi-timeframe support: daily, hourly, and minute intervals.

---

## 📊 How to Use
1. **Select a Forex pair** from the dropdown menu.
2. **Adjust the time frame and interval** using the sidebar controls.
3. **View the candlestick chart** with dynamically detected support and resistance levels.
4. Analyze **zone strength** (number of touches) to assess reliability.

---

## ⚙️ Installation
To run the app locally:

```bash
# Clone the repository
git clone https://github.com/your-username/trading.git

# Navigate to the app directory
cd trading

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run backtesting_tool_app.py
```

---

## 📚 Requirements
- **Python 3.8+**
- **Streamlit**
- **yfinance**
- **pandas**
- **numpy**
- **plotly**

Install all dependencies using:

```bash
pip install -r requirements.txt
```

---

## 🖥️ Deployment
This app can be deployed on **Streamlit Community Cloud**:
1. Push your code to a **GitHub repository**.
2. Go to **https://streamlit.io/cloud**.
3. Select your repository and configure your app settings.

---

## 🔎 Roadmap
- Add detection for **common trading patterns** (e.g., double tops, head & shoulders).
- Include **support/resistance breakout alerts**.
- Implement **custom backtesting strategies** for various pairs.

---

## 🤝 Contributing
Contributions are welcome! Feel free to submit a pull request or open an issue if you have ideas for improving the app.

---

## 📜 License
This project is licensed under the **MIT License**. See the `LICENSE` file for details.

