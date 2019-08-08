import pandas as pd
from time import sleep


class AlphaVantage(object):

    def __init__(self, api_key):
        super(AlphaVantage, self).__init__()

        self.BASE_URL = 'https://www.alphavantage.co/query?'
        self.KEY = api_key

    @staticmethod
    def retrieve_data(path, index_col='time'):
        """returns data from a specified path (local or url) and returns a DataFrame
        index_col can be specified, defaults to time if not specified.
        12 second sleep function included to comply with AlphaVantage's limit of 5 requests/minute.
        Only to be used internally, not intended to be called outside of the class"""
        df = pd.read_csv(path, index_col=index_col)
        sleep(12)
        return df

    def get_ma(self, symbol='SPY', ma_type='SMA', time_period=30, interval='daily', series_type='open'):
        """Retrieves moving average technical data. Defaults to 30 day simple moving average using open prices"""
        url = f'{self.BASE_URL}function={ma_type}&symbol={symbol}&interval={interval}&' \
            f'time_period={time_period}&series_type={series_type}&apikey={self.KEY}&datatype=csv'
        try:
            return self.retrieve_data(url, index_col='time')
        except Exception as e:
            print(e)
            return e

    def get_macd(self, symbol='SPY', fastperiod=12, slowperiod=26, signalperiod=9, interval='daily', series_type='open'):
        """Retrieves MACD, defaults to 12/26/9 daily open data"""
        url = f'{self.BASE_URL}function=MACD&symbol={symbol}&interval={interval}&' \
            f'series_type={series_type}&apikey={self.KEY}&fastperiod={fastperiod}&slowperiod={slowperiod}&' \
            f'signalperiod={signalperiod}&datatype=csv'
        try:
            return self.retrieve_data(url, index_col='time')
        except Exception as e:
            print(e)
            return e

    def get_rsi(self, symbol='SPY', interval='daily', time_period=60, series_type='open'):
        """Retrieves RSI, defaults to 60 day RSI using open prices"""
        url = f'{self.BASE_URL}function=RSI&symbol={symbol}&interval={interval}&' \
            f'time_period={time_period}&series_type={series_type}&apikey={self.KEY}&datatype=csv'
        try:
            return self.retrieve_data(url, index_col='time')
        except Exception as e:
            print(e)
            return e

    def get_daily_data(self, symbol='SPY', outputsize=None):
        """Retrieves daily stock ticker open high low close and volume.
        outputsize can be specified as full or compact. If not specified, default behavior is compact
        compact will only retrieve the most recent 100 values while full retrieves a full history"""
        if outputsize is None:
            url = f'{self.BASE_URL}function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={self.KEY}&datatype=csv'
        elif outputsize == 'full':
            url = f'{self.BASE_URL}function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&outputsize=full&apikey={self.KEY}&datatype=csv'
        try:
            return self.retrieve_data(url, index_col='timestamp')
        except Exception as e:
            print(e)
            return e
