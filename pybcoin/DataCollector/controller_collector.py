"""
    Module name: controller_collector
    Description: Controller module for all data collection.
"""

import sys
import os

import pandas as pd
from configparser import SafeConfigParser

from pybcoin.DataCollector.btc_data_collector import BtcDataCollector
from pybcoin.DataCollector.google_trends_collector import GTrendsDataCollector
from pybcoin.DataCollector.market_data_collector import MarketDataCollector
from pybcoin.DataCollector.reddit_comment_collector import RedditDataCollector
from pybcoin.DataCollector.tweets_collector import TwitterDataCollector

__directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(__directory + "/..")
sys.path.append(__directory + "/../..")

FILES = {
    'btc': 'btc_prices.csv',
    'tcount': 'tweet_counts.csv',
    'vol': 'btc_volume.csv',
    'gtrend': 'GTrendsData.csv',
    'forex': 'usd_exchrate.csv',
    'nyse': 'nyse_index.csv',
    'oil': 'oil_price.csv',
    'tweet': 'tweets.csv',
    'reddit': 'reddit_comments.csv'
}

INDEX = 'Date'


class ControllerCollector(object):

    """
        The controller object for data collection pipeline. Responsible
        for triggering and monitoring the daily streaming data collection
        from all data sources.
            :member attributes: logger: logger instance
                                config: config file path

            :member functions: data_collect_pipeline
    """

    def __init__(self, config_file):
        self.config = SafeConfigParser()
        self.config.read(config_file)

    def data_collection_pipeline(self):
        """
            Method to call the data collector modules to retreive latest
            data.
            : param self
            : return ret_val(int)

        """
        try:
            # Collecting latest BTC price.
            collector = BtcDataCollector(self.config)

            path = self.config['Collector']['in_path_btc'] + FILES['btc']
            data = collector.fetch_btc_price()
            if isinstance(data, int):
                print('Failure while collecting btc price')
            else:
                hist_data = pd.read_csv(path, index_col=INDEX)
                hist_data = hist_data.append(data)
                hist_data.to_csv(path)

            # Collecting BTC Tweet Count

            path = self.config['Collector']['in_path_btc'] + FILES['tcount']
            data = collector.fetch_tweet_counts()
            if isinstance(data, int):
                print('Failure while collecting  btc tweet counts')
            else:
                hist_data = pd.read_csv(path, index_col=INDEX)
                hist_data = hist_data.append(data)
                hist_data.to_csv(path)

            # Collecting BTC Volume

            path = self.config['Collector']['in_path_btc'] + FILES['vol']
            data = collector.fetch_transaction_volume()
            if isinstance(data, int):
                print('Failure while collecting  btc trans. volume')
            else:
                hist_data = pd.read_csv(path, index_col=INDEX)
                hist_data = hist_data.append(data)
                hist_data.to_csv(path)

            # Collecting Google trends.
            collector = GTrendsDataCollector()
            path = self.config['Collector']['in_path_gtrends'
                                            ] + FILES['gtrend']
            data = collector.fetch_trends()
            if isinstance(data, int):
                print('Failure while collecting Google trends.')
            else:
                hist_data = pd.read_csv(path, index_col=INDEX)
                hist_data = hist_data.append(data)
                hist_data.to_csv(path)

            # Collecting USD/EURO forex rate

            collector = MarketDataCollector()

            path = self.config['Collector']['in_path_comm'
                                            ] + FILES['forex']
            data = collector.fetch_usd_exrate()
            if isinstance(data, int):
                print('Failure while collecting USD forex rate.')
            else:
                hist_data = pd.read_csv(path, index_col=INDEX)
                hist_data = hist_data.append(data)
                hist_data.to_csv(path)

            # Collecting NYSE composite index

            path = self.config['Collector']['in_path_comm'] + FILES['nyse']
            data = collector.fetch_nyse_index()
            if isinstance(data, int):
                print('Failure while collecting NYSE index.')
            else:
                hist_data = pd.read_csv(path, index_col=INDEX)
                hist_data = hist_data.append(data)
                hist_data.to_csv(path)

            # Collecting Crude Oil Price
            path = self.config['Collector']['in_path_comm'] + FILES['oil']
            data = collector.fetch_oil_price()
            if isinstance(data, int):
                print('Failure while collecting Oil price.')
            else:
                hist_data = pd.read_csv(path, index_col=INDEX)
                hist_data = hist_data.append(data)
                hist_data.to_csv(path)

            # Collecting Tweets
            path = self.config['Reddit']['data_path'] + FILES['tweet']
            collector = TwitterDataCollector(self.config)
            data = collector.fetch_tweets()
            if isinstance(data, int):
                print('Failure while collecting tweets.')
            else:
                data.to_csv(path, index=False)

            # Collecting Reddit comments
            path = self.config['Reddit']['data_path'] + FILES['reddit']
            collector = RedditDataCollector(self.config)
            data = collector.fetch_reddit_comments()
            if isinstance(data, int):
                print('Failure while collecting reddit comments.')
            else:
                data.to_csv(path, index=False)

            print('Data Collection complete')
            return True

        except Exception as e:
            print(e)
            return True
