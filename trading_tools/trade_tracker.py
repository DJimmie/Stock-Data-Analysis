"""Retrievies requested stocks, calculates current day indicators and generates a trade 'enthusiasm' score based on the traders criteria.""" 

import pandas as pd
import numpy as np
import os
import sys
import logging

import json

sys.path.insert(0,"C:\\Users\\dowdj\\OneDrive\\Documents\\GitHub\\my-modules-and-libraries\\program_work_dir")  # Temporary. Used to help finish development of modules.
import program_work_dir as pwd

import yfinance as yf
import pandas_datareader as pdr
import pandas_datareader.data as web
import stockstats
from stockstats import StockDataFrame as Sdf
import pandas_ta as ta

from collections import deque

import pprint





def user_inputs():
    """User specifies list of stocks to review and score. User also inputs the date range and the interval of the stock data.
    Inputs are stored in a dictionary."""
    
    inputs={
        'stock_list':['csgs','adt','gnw'],
        'start_date':'2020',
        'stop_date':'2021'}
    
    retrieve_OHLC_data(inputs)

def retrieve_OHLC_data(inputs):
    """
    Input---> list of stocks
    Output ---> dictionary with ticker symbol keys and the retrieve OHLC dataframe as values
    """
    global stock_dict,symbol
    stock_dict=dict()
    
    for i in inputs['stock_list']:
        # send_results_to_file({'TRADE DATA FOR------>':i.upper()},'a')
        symbol = i.upper() 
        stock_name=symbol
        stock =pdr.get_data_yahoo(symbol)[inputs['start_date']:inputs['stop_date']]
        stock_dict[i]=stock

        GenerateIndicators(stock_dict[i])


def GenerateIndicators(df):
    """generate the stock indictors for the stock OHLCV data"""

    # make a dataframe
    df.ta.macd(append=True)
    df.ta.rsi(append=True)
    df.ta.sma(length=5,append=True)
    df.ta.sma(length=50,append=True)
    df.ta.sma(length=180,append=True)
    df.dropna(inplace=True)

    print(df.head())

    print(df.loc['2021-02-05'])

    indicator_dict=df.loc['2021-02-05'].to_dict()

    print(indicator_dict)

    send_results_to_file({'Ticker':symbol,'Results':indicator_dict},'a')

    trade_criteria(indicator_dict)


def trade_criteria(indicator_dict):
    """Run indictors thru the trade criteria"""

    # MACD above MACDs

    trade_status_line[symbol]={}

    if indicator_dict['MACD_12_26_9']>indicator_dict['MACDs_12_26_9']:
        trade_status_line[symbol]['M_ovr_S']=1
    else:
        trade_status_line[symbol]['M_ovr_S']=0

    if indicator_dict['MACD_12_26_9']>0:
        trade_status_line[symbol]['M_>_0']=1
    else:
        trade_status_line[symbol]['M_>_0']=0

    if indicator_dict['RSI_14']>50:
        trade_status_line[symbol]['RSI14_>_50']=1
    else:
        trade_status_line[symbol]['RSI14_>_50']=0

    if indicator_dict['SMA_5']>indicator_dict['SMA_50']:
        trade_status_line[symbol]['SMA5_ovr_SMA50']=1
    else:
        trade_status_line[symbol]['SMA5_ovr_SMA50']=0

    if indicator_dict['SMA_50']>indicator_dict['SMA_180']:
        trade_status_line[symbol]['SMA50_ovr_SMA180']=1
    else:
        trade_status_line[symbol]['SMA50_ovr_SMA180']=0

    if indicator_dict['close']>indicator_dict['SMA_5']:
        trade_status_line[symbol]['CLOSE_ovr_SMA5']=1
    else:
        trade_status_line[symbol]['CLOSE_ovr_SMA5']=0


    send_results_to_file({'Ticker':symbol,'Results':trade_status_line[symbol]},'a')

    print(trade_status_line)


def send_results_to_file(data,file_action='a'):

    output_s = pprint.pformat(data)
    with open('tracker_output.txt', file_action) as file:
        file.write(output_s)
        file.write('\n\n')


if __name__ == '__main__':


    global trade_status_line
    trade_status_line=dict()

    send_results_to_file({'TRADE TRACKER REPORT':'------------>'},'w')

    user_inputs()
    
    

