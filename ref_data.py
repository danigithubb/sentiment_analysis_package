import selenium
import requests
import pandas as pd
import numpy as np
import csv
import datetime as dt
import sys
import os
from itertools import groupby
from operator import itemgetter
from collections import defaultdict
import yfinance as yf


# function_1 : returns list of tickers in SP100 as of Sept 2022
def get_sp100():
    table = pd.read_html('https://en.wikipedia.org/wiki/S%26P_100', match = 'Symbol') # tickers webscraped from wikipedia
    table_df = pd.DataFrame(table[0])
    table_df.to_csv('S&P100-Info.csv')
    tickers_obj = pd.read_csv('S&P100-Info.csv', delimiter=',', index_col = None) 
    symbols_csv = tickers_obj.to_csv("S&P100-Symbols.csv", columns=['Symbol']) # creates a csv file of tickers
    csv_to_list_tickers = [list(row) for row in tickers_obj.values]

    new_ticker_list = []
    for i in csv_to_list_tickers:
        new_ticker_list.append(i[1])
    return new_ticker_list


#function 2 : returns yahoo financial data
def  get_yahoo_data(start_date, end_date, tickers):
    tickername = yf.Ticker(tickers) # demo ticker AMZN
    stage1 = pd.DataFrame(tickername.history(start = start_date, end = end_date))
    stage2 = stage1.reset_index()
    stage2['1daily_return'] = (stage2['Close'].shift(-1) - stage2['Close'])/stage2['Close']
    stage2['2daily_return'] = (stage2['Close'].shift(-2) - stage2['Close'])/stage2['Close']
    stage2['3daily_return'] = (stage2['Close'].shift(-3) - stage2['Close'])/stage2['Close']
    stage2['5daily_return'] = (stage2['Close'].shift(-5) - stage2['Close'])/stage2['Close']
    stage2['10daily_return'] = (stage2['Close'].shift(-10) - stage2['Close'])/stage2['Close']
    stage2['Symbol'] = tickers
    stage3 = stage2.drop('Open', axis = 'columns')
    stage4 = stage3.drop('Dividends', axis = 'columns')
    stage5 = stage4.drop('Stock Splits', axis = 'columns')
    return stage5


#function_3: return a dictionary containing LM sentiment words
# keys  - sentiment type
# proposed keys classification - negative, positive, uncertainty, litigious, strong modal, weak modal, and constraining
# keys value - words associated with particular sentiment

def get_sentiment_word_dict():
    cwd = os.getcwd() #find path name using OS library
    dict_lm = pd.read_csv(f'{cwd}/LM-SA-2020.csv',header=None, index_col=0, squeeze=True).to_dict() #convert csv Loughran_McDonald to a dictionary
    res = defaultdict(list)
    for key, val in sorted(dict_lm.items()):
        res[val].append(key)
    remove_word_sentiment = res.pop('sentiment') #remove column index from list of dictionary
    return dict(res)



