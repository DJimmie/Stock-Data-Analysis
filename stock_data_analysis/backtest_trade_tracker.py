"""Retrievies requested stocks, calculates current day indicators and generates a trade 'enthusiasm' score based on the traders criteria.""" 
# %%
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

NUM_SHARES=100

# %%
def user_inputs():
    """User specifies list of stocks to review and score. User also inputs the date range and the interval of the stock data.
    Inputs are stored in a dictionary."""
    
    my_stocks={
    'Cannibus':['NVDA'],
    'Drones':['NVDA','AMBA','AVAV'],
    'Energy':['PBD','FAN'],
    'Healthcare':['ADMS','cern','kern','cslt','nspr','ontx']
    }


    inputs={
        'stock_list':my_stocks['Cannibus'],
        'start_date':'2019',
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

# %%
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

   
    status=False
    start_list=[]
    stop_list=[]
    stock_buy=[]
    stock_sell=[]
    for index, row in df.iterrows():
        indicator_dict=df.loc[index].to_dict()
        trade_score=trade_criteria(indicator_dict)
        if status==False:
            if trade_score==100:
                start=index
                # print(f'START--->{index}--->{row["close"]}')
                # send_results_to_file({'MACD XOVR START':index},'a')
                start_list.append(start)
                stock_buy.append(df.loc[start]["close"])
                status=True

        if status==True:
            if trade_score<=50:
                stop=index
                # print(f'STOP--->{index}--->{row["close"]}')
                # send_results_to_file({'MACD XOVR STOP':index},'a')
                stop_list.append(stop)
                # print(f'CLOSE------->{df.loc[stop]["close"]}')
                stock_sell.append(df.loc[stop]['close'])
                status=False

    print(f'{start_list}\n\n{stop_list}\n')
    process_data(df,start_list,stop_list,stock_buy,stock_sell)
    print(indicator_dict)

    send_results_to_file({'Ticker':symbol,'Results':indicator_dict},'a')

    
# %%
def process_data(df,start_list,stop_list,stock_buy,stock_sell):

        # global macd_Xover_df
        PL=[a - b for a, b in zip(stock_sell, stock_buy)]
        PL=[round(i*NUM_SHARES,2) for i in PL]

        net_PL=sum(PL)

        print(f'\nPL---- ${PL}\n')
        print(f'gain: $ {gain(PL)}')
        print(f'loss: $ {loss(PL)}')

        print(f'Net PL------- ${round(net_PL)}')

        print(f'Successful Trade Percentage: {round(success(PL)*100,2)} %')
        
        duration=[a - b for a, b in zip(stop_list, start_list)]
        duration=[a.days for a in duration]
        
        print(f'\nDurations--->{duration}')

        send_results_to_file({'Loss':f'${loss(PL)}','Gain':f'${gain(PL)}','Net PL':f'${round(net_PL)}',
        'Successful Trade Percentage':f'{round(success(PL)*100,2)} %'},'a')

        start_list=[a.date().strftime("%Y-%m-%d") for a in start_list]  #----> dates formatted to datestamp
        stop_list=[a.date().strftime("%Y-%m-%d") for a in stop_list]    #----> dates formatted to datestamp
        if len(start_list)>len(PL):     # ---> removes the most recent in-progress trade
            start_list.pop()

        backtest_data={
            'start':start_list,
            'stop':stop_list,
            'PL':PL,
            'macd':[round(i,7) for i in df['MACD_12_26_9'][start_list]],
            'macd_H':[round(i,7) for i in df['MACDh_12_26_9'][start_list]],
            'rsi14':[round(i,7) for i in df['RSI_14'][start_list]],
            'outcome':[int(1) if i>0 else 0 for i in PL]}

        
        send_results_to_file({
        'Profit/Loss (USD)':PL,
        'Duration (days)':duration,
        'Start':backtest_data['start'],
        'Stop':backtest_data['stop'],
        'MACD':backtest_data['macd'],
        'MACD_H':backtest_data['macd_H'],
        'RSI14':backtest_data['rsi14'],
        'Trade_Outcome':backtest_data['outcome']},'a')

        print(backtest_data)
        
        # convert Dict to dataframe
        # a=pd.DataFrame.from_dict(backtest_data)

        # print(a)

        # append dataframe to the main dataframe
        # backtest_data_df=backtest_data_df.append(a,ignore_index=True)


        # print(backtest_data_df)

        # send_results_to_file({'DATASET FOR Baseline Stategy---->':backtest_data_df},'a')


# %%

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


    # send_results_to_file({'Ticker':symbol,'Results':trade_status_line[symbol]},'a')

    print(f'{trade_status_line}\n')

    return enthusiasm_score(trade_status_line)

# %%

def enthusiasm_score(trade_status_line):
    """Calculating a trade enthusiasm score per the criteria result in the trade_status_line"""
    sum=0
    for key, value in trade_status_line[symbol].items():
        print(key,":",value)

        sum=sum+value

    # Baseline score
    e_score_percent=round(sum/len(trade_status_line[symbol])*100)
    print(f'\n{symbol}---> E-score-->: {sum}---> {e_score_percent} %')


    # send_results_to_file({'Ticker':symbol,'Score':{f'{e_score_percent}%'}},'a')

    baseline_scores[symbol]=e_score_percent

    return e_score_percent



def send_results_to_file(data,file_action='a'):

    output_s = pprint.pformat(data)
    with open('tracker_output.txt', file_action) as file:
        file.write(output_s)
        file.write('\n\n')

success=lambda x:sum([1 if i>0 else 0 for i in x])/len(x)

gain=lambda  x:sum([i for i in x if i >= 0])

loss=lambda  x:sum([i for i in x if i <0])

# %%
if __name__ == '__main__':


    global trade_status_line, baseline_scores
    trade_status_line=dict()
    baseline_scores=dict()

    send_results_to_file({'TRADE TRACKER REPORT':'------------>'},'w')

    user_inputs()
    
    send_results_to_file({'* BASELINE SCORES--->':baseline_scores},'a')
    


# %%
