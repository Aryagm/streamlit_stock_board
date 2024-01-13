import pandas as pd

# Function to read stock data and sentiment score from a file
def read_stock_data(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            stock_data = [line.strip().split(',') for line in lines if not line.startswith("Sentiment Score")]
            sentiment_line = [line for line in lines if line.startswith("Sentiment Score")][0]
            sentiment_score  = float(sentiment_line.split(":")[1].strip())
            return stock_data, sentiment_score
    except Exception as e:
        print(f"Error reading file: {e}")
        return [], 0

# Function to predict stock trend based on data and sentiment score
def predict_trend(stock_data, sentiment_score):
    df = pd.DataFrame(stock_data, columns=['Date', 'Price', 'Volume'])
    df['Price'] = df['Price'].astype(float)

    avg_price = df['Price'].mean()
    last_price = df.iloc[-1]['Price']

    if sentiment_score > 0 and avg_price > last_price:
        return "Likely to Rise"
    elif sentiment_score < 0 and avg_price < last_price:
        return "Likely to Fall"
    else:
        return "Uncertain Trend"

# Main function to execute the script
def main():
    stock_data, sentiment_score = read_stock_data('stock_data.txt')
    if stock_data:
        prediction = predict_trend(stock_data, sentiment_score)
        with open('prediction_result.txt', 'w') as file:
            file.write(f"Predicted Trend: {prediction}\n")
    else:
        print("No stock data available.")

if __name__ == "__main__":
    main()
