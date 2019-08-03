# TODO: Add functions for CCI, AROON, BBANDS, AD, OBV
# https://www.alphavantage.co/documentation/

import pandas as pd
import configparser
import logging
from alpha_vantage import AlphaVantage
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


if __name__ == '__main__':
    configuration = get_config('DEV')
    key = configuration.get('credentials', 'apikey')
    alpha = AlphaVantage(key)
    daily_data = alpha.get_daily_data('FXI', 'full')
    sma = alpha.get_ma('FXI')
    ema = alpha.get_ma('FXI', 'EMA')
    wma = alpha.get_ma('FXI', 'WMA')
    macd = alpha.get_macd('FXI')
    rsi = alpha.get_rsi('FXI')
    adx = alpha.get_ma('FXI', 'ADX')
    full_df = pd.concat([daily_data, sma, ema, wma, macd, adx, rsi], axis=1, sort=False)
    full_df.to_csv('output.csv')
