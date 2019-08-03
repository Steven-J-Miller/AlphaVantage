import pandas as pd
from time import sleep


class AlphaVantage(object):

    def __init__(self, api_key, **kwargs):
        super(AlphaVantage, self).__init__()

        self.BASE_URL = 'https://www.alphavantage.co/query?'
        self.KEY = api_key

    def retrieve_data(self, path, index_col='time'):
        df = pd.read_csv(path, index_col=index_col)
        sleep(1)
        return df

    def get_ma(self, symbol='SPY', ma_type='SMA', time_period=30, interval='daily', series_type='open'):
        url = f'{self.BASE_URL}function={ma_type}&symbol={symbol}&interval={interval}&' \
            f'time_period={time_period}&series_type={series_type}&apikey={self.KEY}&datatype=csv'
        try:
            return self.retrieve_data(url, index_col='time')
        except Exception as e:
            print(e)

    def get_macd(self, symbol='SPY', fastperiod=12, slowperiod=26, signalperiod=9, interval='daily', series_type='open'):
        url = f'{self.BASE_URL}function=MACD&symbol={symbol}&interval={interval}&' \
            f'series_type={series_type}&apikey={self.KEY}&fastperiod={fastperiod}&slowperiod={slowperiod}&' \
            f'signalperiod={signalperiod}&datatype=csv'
        try:
            return self.retrieve_data(url, index_col='time')
        except Exception as e:
            print(e)

    def get_rsi(self, symbol='SPY', interval='daily', time_period=60, series_type='open'):
        url = f'{self.BASE_URL}function=RSI&symbol={symbol}&interval={interval}&' \
            f'time_period={time_period}&series_type={series_type}&apikey={self.KEY}&datatype=csv'
        try:
            return self.retrieve_data(url, index_col='time')
        except Exception as e:
            print(e)

    def get_daily_data(self, symbol='SPY', outputsize=None):
        if outputsize is None:
            url = f'{self.BASE_URL}function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={self.KEY}&datatype=csv'
        elif outputsize == 'full':
            url = f'{self.BASE_URL}function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&outputsize=full&apikey={self.KEY}&datatype=csv'
        try:
            return self.retrieve_data(url, index_col='timestamp')
        except Exception as e:
            print(e)
