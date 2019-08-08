import pandas as pd
import configparser
import logging
from alpha_vantage import AlphaVantage
from datetime import datetime


def get_config(env):
    """Retrieves any necessary configuration information from config/config.cfg"""
    config = configparser.ConfigParser()
    config.read(['config/config.cfg'])
    return config


def possible_outliers(series):
    """Identifies potential outliers in the data by identifying any values more than 5
    standard deviations from the mean"""
    mean = series.mean()
    sd = series.std()
    above_5_sd = [i for i in series if i > mean+sd*5]
    below_5_sd = [i for i in series if i < mean-sd*5]
    print(f'Extreme values found in {series.name}:')
    print(above_5_sd)
    print(below_5_sd)
    return len(above_5_sd)+len(below_5_sd)


if __name__ == '__main__':
    # Start logger, overwrite print function with logger.info to record all program output to file
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    logger = logging.getLogger()
    now = datetime.strftime(datetime.now(), '%Y%m%d %H%M%S %f')
    logger.addHandler(logging.FileHandler(f'{now}.log', 'a'))
    print = logger.info

    # Retrieve API key, create AlphaVantage object
    configuration = get_config('DEV')
    key = configuration.get('credentials', 'apikey')
    alpha = AlphaVantage(key)

    # Retrieve market data
    daily_data = alpha.get_daily_data('AMD', 'full')
    sma = alpha.get_ma('AMD')
    ema = alpha.get_ma('AMD', 'EMA')
    wma = alpha.get_ma('AMD', 'WMA')
    macd = alpha.get_macd('AMD')
    rsi = alpha.get_rsi('AMD')
    adx = alpha.get_ma('AMD', 'ADX')

    # join all frames together by index, write to file
    full_df = pd.concat([daily_data, sma, ema, wma, macd, adx, rsi], axis=1, sort=False)
    full_df.to_csv('output.csv')

    # check for possible duplicate entries
    print(f'Potential duplicate entries: {len(full_df[full_df.duplicated()])}')

    # check for outliers/bad data
    for column in full_df.columns:
        print(possible_outliers(full_df[column]))
