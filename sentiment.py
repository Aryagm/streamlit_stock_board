import matplotlib.pyplot as plt
import nltk
import numpy as np
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from datetime import datetime
from wordcloud import WordCloud

from get_sentiment_data import get_sentiment_data

try:
    vader = SentimentIntensityAnalyzer()
except:
    nltk.download('vader_lexicon')
    vader = SentimentIntensityAnalyzer()


class Sentiment:
    """ 
    Instantiate ticker(s) for analysis.
    Provides several functions to analyze sentiments of stocks based on trusted news sources.
    
    :param ticker: The ticker or list of tickers.
    :type ticker: str/list
    """

    def __init__(self, ticker):
        self.ticker = ticker

    def get_sentiment(self, days=None):
        """
        Returns sentiment of given ticker(s).

        :param days: Number of days into the past you want the sentiment for. 
        :type days: int 
    
        """
        df = get_sentiment_data(self.ticker)
        if days is not None:
            now = datetime.now().date()
            day_neg = pd.to_timedelta(days, unit='d')
            oldest_date = now - day_neg
            df = df[df['date'] >= oldest_date]
        scores = df['headline'].apply(vader.polarity_scores).tolist()
        scores = [x['compound'] for x in scores]
        sentiment = float(np.mean(scores))
        final_sentiment = round(sentiment, 4)
        return final_sentiment

    def get_dataframe(self, days=None):
        """
        Returns dataframe of given ticker(s) with date, time, headlines, source and sentiment.

        :param days: Number of days into the past you want the sentiment for.
        :type days: int

        """
        df = get_sentiment_data(self.ticker)
        scores = df['headline'].apply(vader.polarity_scores).tolist()
        scores_df = pd.DataFrame(scores)
        scores_df.columns = ['Negative', 'Neutral', 'Positive', 'Overall']
        df = df.join(scores_df, rsuffix='_right')
        if days is not None:
            now = datetime.now().date()
            day_neg = pd.to_timedelta(days, unit='d')
            oldest_date = now - day_neg
            df = df[df['date'] >= oldest_date]
        return df

    def plot(self, days=None, save_figure=False):
        """
        Returns plot of given ticker(s) with sentiment across several days.

        :param days: Number of days into the past you want the plot for.
        :type days: int

        :param save_figure: Option for saving figure as png.
        :type save_figure: bool

        """
        df = get_sentiment_data(self.ticker)
        scores = df['headline'].apply(vader.polarity_scores).tolist()
        scores_df = pd.DataFrame(scores)
        scores_df.columns = ['Negative', 'Neutral', 'Positive', 'Overall']
        df = df.join(scores_df, rsuffix='_right')
        if days is not None:
            now = datetime.now().date()
            day_neg = pd.to_timedelta(days, unit='d')
            oldest_date = now - day_neg
            df = df[df['date'] >= oldest_date]

        plt.rcParams['figure.figsize'] = [10, 6]
        # Convert 'date' to datetime if it's not already
        if not pd.api.types.is_datetime64_any_dtype(df['date']):
            df['date'] = pd.to_datetime(df['date'])

        # Group by 'ticker' and 'date', and compute the mean of 'Overall'
        mean_scores = df.groupby(['ticker', df['date'].dt.date])['Overall'].mean()

        # Plot the mean scores
        mean_scores.plot(kind='bar', figsize=(10, 6))

        plt.tight_layout()
        plt.grid()
        if save_figure:
            plt.savefig(str(datetime.now().timestamp()) + ".png")
        plt.show()
        pass

    def word_cloud(self, days=None, save_figure=False, figsize=(15, 8)):
        """
        Returns a word cloud plot of given ticker(s).

        :param days: Number of days into the past you want the word cloud for.
        :type days: int

        :param save_figure: Option for saving figure as png.
        :type save_figure: bool

        :param figsize: Option for resizing plot.
        :type save_figure: tuple

        """
        df = get_sentiment_data(self.ticker)
        scores = df['headline'].apply(vader.polarity_scores).tolist()
        scores_df = pd.DataFrame(scores)
        scores_df.columns = ['Negative', 'Neutral', 'Positive', 'Overall']
        df = df.join(scores_df, rsuffix='_right')
        if days is not None:
            now = datetime.now().date()
            day_neg = pd.to_timedelta(days, unit='d')
            oldest_date = now - day_neg
            df = df[df['date'] >= oldest_date]

        unique_string = " ".join(df['headline'].tolist())
        wordcloud = WordCloud(width=1000, height=500).generate(unique_string)

        plt.figure(figsize=figsize)
        plt.imshow(wordcloud)
        plt.axis("off")
        if save_figure:
            plt.savefig(str(datetime.now().timestamp()) + ".png")
        plt.show()
        pass
