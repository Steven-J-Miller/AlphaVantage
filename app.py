# TODO: Add functions for CCI, AROON, BBANDS, AD, OBV
# https://www.alphavantage.co/documentation/

import pandas as pd
import configparser
import logging
from datetime import datetime


def start_logger():
    now = datetime.strftime(datetime.now(), '%Y-%m-%d %H%M%S %f')
    logging.basicConfig(filename=f'logs/report_{now}.log', level=logging.DEBUG)


def get_config(env):
    config = configparser.ConfigParser()
    if env == "DEV":
        config.read(['config/development.cfg'])
    elif env == "PROD":
        config.read(['config/production.cfg'])
    return config


def get_daily_data(key, symbol='SPY', outputsize=None):
    if outputsize is None:
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={key}&datatype=csv'
    elif outputsize == 'full':
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&outputsize=full&apikey={key}&datatype=csv'
    try:
        df = pd.read_csv(url, index_col='timestamp')
    except Exception as e:
        print(e)
    return df


def get_ma(key, symbol='SPY', ma_type ='SMA', time_period=30, interval='daily', series_type='open'):
    url = f'https://www.alphavantage.co/query?function={ma_type}&symbol={symbol}&interval={interval}&' \
        f'time_period={time_period}&series_type={series_type}&apikey={key}&datatype=csv'
    try:
        df = pd.read_csv(url, index_col='time')
    except Exception as e:
        print(e)
    return df


def get_macd(key, symbol='SPY', fastperiod=12, slowperiod=26, signalperiod=9, interval='daily', series_type='open'):
    url = f'https://www.alphavantage.co/query?function=MACD&symbol={symbol}&interval={interval}&' \
        f'series_type={series_type}&apikey={key}&fastperiod={fastperiod}&slowperiod={slowperiod}&' \
        f'signalperiod={signalperiod}&datatype=csv'
    try:
        df = pd.read_csv(url, index_col='time')
    except Exception as e:
        print(e)
    return df


def get_rsi(key, symbol='SPY', interval='daily', time_period=60, series_type='open'):
    url = f'https://www.alphavantage.co/query?function=RSI&symbol={symbol}&interval={interval}&' \
        f'time_period={time_period}&series_type={series_type}&apikey={key}&datatype=csv'
        try:
            df = pd.read_csv(url, index_col='time')
        except Exception as e:
            print(e)
        return df


def main():
    configuration = get_config('DEV')
    key = configuration.get('credentials', 'apikey')
    daily_data = get_daily_data(key, 'FXI', 'full')
    sma = get_ma(key, 'FXI')
    ema = get_ma(key, 'FXI', 'EMA')
    wma = get_ma(key, 'FXI', 'WMA')
    macd = get_macd(key, 'FXI')
    rsi = get_rsi(key, 'FXI')
    adx = get_ma(key, 'FXI', 'ADX')
    full_df = pd.concat([daily_data,sma,ema,wma,macd, adx, rsi], axis=1, sort=False)
