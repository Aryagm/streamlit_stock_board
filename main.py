import streamlit as st
import matplotlib.pyplot as plt
import yfinance as yf
import plotly.graph_objs as go
from sentiment import Sentiment  # Assuming sentiment.py contains the Sentiment class
import subprocess

# Streamlit configurations
st.set_option('deprecation.showPyplotGlobalUse', False)

# Application title
st.title('Advanced Stock Data and Sentiment Analysis App')

# User input for the stock ticker
ticker = st.text_input("Enter a stock ticker (e.g., AAPL, TSLA):")

# Date input for start and end date
start_date = st.date_input("Start date")
end_date = st.date_input("End date")

# Function to fetch stock data
def get_stock_data(ticker, start, end):
    start_date_str = start.strftime('%Y-%m-%d')
    end_date_str = end.strftime('%Y-%m-%d')
    stock_data = yf.download(ticker, start=start_date_str, end=end_date_str)
    return stock_data

# Function to fetch news, sentiment, and generate word cloud
def get_news_and_sentiment(ticker):
    stock = Sentiment(ticker)
    sentiment_score = stock.get_sentiment()
    df_headlines = stock.get_dataframe()
    return sentiment_score, df_headlines

# Display the stock data
if ticker:
    stock_data = get_stock_data(ticker, start_date, end_date)
    sentiment_score, df_headlines = get_news_and_sentiment(ticker)

    # Save stock data and sentiment score to a text file
    with open('stock_data.txt', 'w') as file:
        for index, row in stock_data.iterrows():
            file.write(f"{index},{row['Close']},{row['Volume']}\n")
        file.write(f"Sentiment Score: {sentiment_score}\n")

    # Running the C++ program
    subprocess.run(["./stock_prediction"])

    # Reading the prediction result
    with open('prediction_result.txt', 'r') as file:
        prediction = file.read()

    # Display the prediction result
    st.title(f"Prediction: {prediction}")

    # ... [Rest of your existing Streamlit code for plotting, etc.] ...


    if not stock_data.empty:
        # Plotting the stock data using Plotly
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['Close'], mode='lines', name='Close Price', line=dict(color='blue', width=2)))
        fig.update_layout(title=f'Closing Price of {ticker}', xaxis_title='Date', yaxis_title='Price (USD)', template="plotly_dark")
        st.plotly_chart(fig)

        # Additional Plotly plots
        # Plotting Volume with pattern
        fig_volume = go.Figure(data=[go.Bar(x=stock_data.index, y=stock_data['Volume'], marker_pattern_shape="x", marker_color='blue')])
        fig_volume.update_layout(title='Trading Volume', xaxis_title='Date', yaxis_title='Volume', template="plotly_dark")
        st.plotly_chart(fig_volume)

        # Plotting Moving Average with confidence range
        moving_average = stock_data['Close'].rolling(window=20).mean()
        std_dev = stock_data['Close'].rolling(window=20).std()
        upper_band = moving_average + (std_dev * 2)
        lower_band = moving_average - (std_dev * 2)

        fig_ma = go.Figure()
        fig_ma.add_trace(go.Scatter(x=stock_data.index, y=moving_average, mode='lines', name='20-Day Moving Average', line=dict(color='green', width=2)))
        fig_ma.add_trace(go.Scatter(x=stock_data.index, y=upper_band, fill=None, mode='lines', name='Upper Band', line=dict(color='lightgreen', width=1)))
        fig_ma.add_trace(go.Scatter(x=stock_data.index, y=lower_band, fill='tonexty', mode='lines', name='Lower Band', line=dict(color='lightgreen', width=1)))
        fig_ma.update_layout(title='20-Day Moving Average with Confidence Bands', xaxis_title='Date', yaxis_title='Price (USD)', template="plotly_dark")
        st.plotly_chart(fig_ma)

    if not df_headlines.empty:
        # Displaying sentiment score
        st.title(f"Sentiment Score: {sentiment_score}")

        # Displaying headlines
        st.write("Recent News Headlines:")
        st.dataframe(df_headlines[['date', 'headline']].head(10))

        # Generating and displaying word cloud
        stock = Sentiment(ticker)
        fig, ax = plt.subplots()
        plot_word = stock.word_cloud()
        st.pyplot(stock.word_cloud())

        # Sentiment plot from stocksent
        fig_sentiment, ax_sentiment = plt.subplots()
        stock.plot()
        st.pyplot(stock.plot())
    else:
        st.write("No news data available for the selected ticker.")