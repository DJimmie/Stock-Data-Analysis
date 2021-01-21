# %%
"""Exploring the use of the pandas-ta library""" 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import calendar
import os
import sys
import logging

import pprint

import pandas_ta as ta

import yfinance as yf
import pandas_datareader as pdr
import pandas_datareader.data as web

from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from scipy import stats

# %%
NUM_SHARES=100
MOVING_AVG_PERIOD=20
MACD_DIFFERENCE=1
SIGMA_PRICE_DIFF=3
START_DATE='2020'
END_DATE='2021'
FEATURE='Close' 
DATA_SCALING=False
REMOVE_OUTLIERS=False

# %%

macd_Xover_df=pd.DataFrame(columns=['start','stop','PL','macd','macd_H','outcome'])


# %%

def get_the_stock(ticker):
    symbol = ticker.upper() 
    stock_name=symbol
    stock =pdr.get_data_yahoo(symbol)[START_DATE:END_DATE]
    return stock

def macd_Xover(df):
        """Capture data from MACD crossover. 
        Input---->MACD,signal
        Output---->"""

        global macd_Xover_df

        # make a dataframe
        df.ta.macd(append=True)
        df.ta.rsi(append=True)
        df.dropna(inplace=True)

        print(df.head())
        
        # checking for crossovers and retrieving the xovr date index
        status=False
        start_list=[]
        stop_list=[]
        stock_buy=[]
        stock_sell=[]
        for index, row in df.iterrows():
            if status==False:
                if row['MACD_12_26_9']>row['MACDs_12_26_9']:
                    start=index
                    # print(f'START--->{index}--->{row["close"]}')
                    # send_results_to_file({'MACD XOVR START':index},'a')
                    start_list.append(start)
                    stock_buy.append(df.loc[start]["close"])
                    status=True
            
            if status==True:
                if row['MACD_12_26_9']<=row['MACDs_12_26_9']:
                    stop=index
                    # print(f'STOP--->{index}--->{row["close"]}')
                    # send_results_to_file({'MACD XOVR STOP':index},'a')
                    stop_list.append(stop)
                    # print(f'CLOSE------->{df.loc[stop]["close"]}')
                    stock_sell.append(df.loc[stop]['close'])
                    status=False

        # print(f'{start_list}\n{stock_buy}\n{stop_list}\n{stock_sell}')
        print(f'{start_list}\n\n{stop_list}\n')

        
        # Profit/Loss list---> element wise sum of stoc

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

        macd_Xover_data={
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
        'Start':macd_Xover_data['start'],
        'Stop':macd_Xover_data['stop'],
        'MACD':macd_Xover_data['macd'],
        'MACD_H':macd_Xover_data['macd_H'],
        'RSI14':macd_Xover_data['rsi14'],
        'Trade_Outcome':macd_Xover_data['outcome']},'a')

        print(macd_Xover_data)
        
        # convert Dict to dataframe
        a=pd.DataFrame.from_dict(macd_Xover_data)

        print(a)

        # append dataframe to the main dataframe
        macd_Xover_df=macd_Xover_df.append(a,ignore_index=True)


        print(macd_Xover_df)

        send_results_to_file({'DATASET FOR MACD CROOSVER---->':macd_Xover_df},'a')

        

        
def send_results_to_file(data,file_action='a'):

    output_s = pprint.pformat(data)
    with open('output.txt', file_action) as file:
        file.write(output_s)
        file.write('\n\n')

def tradeDataAnalysis(dataset):
    """Prep trade date for analysis"""

    features = ['macd','macd_H','rsi14','outcome']

    dataset['df']['outcome']= dataset['df']['outcome'].astype(int)  # convert the outcome to int type

    dataset['df'].drop('PL',inplace=True,axis=1)

    if DATA_SCALING:
    # autoscaler = StandardScaler()
        autoscaler = MinMaxScaler()
        dataset['df'][dataset['features']] = autoscaler.fit_transform(dataset['df'][dataset['features']])

    
    if REMOVE_OUTLIERS:
        df_no_outliers = dataset['df'][['macd','macd_H','rsi14']]
        df_no_outliers=df_no_outliers[(np.abs(stats.zscore(df_no_outliers)) < 3.0).all(axis=1)]

        # dataset['df']=df_no_outliers
        dataset['df'][['macd','macd_H','rsi14']]=df_no_outliers[['macd','macd_H','rsi14']]

        print(f'mofo--->{dataset["df"].info()}')
        print(f'damn--->{df_no_outliers}')


    send_results_to_file({'SCALED DATASET':dataset['df']})

    correlation_matrix(dataset=dataset)


def correlation_matrix(dataset):
    """Receives Dict of data package which consist of the collected dataframe 
    and the list of features to study"""

    feature_matrix=dataset['df'][dataset['features']]
    corr=feature_matrix.corr()
    corr
    
    plt.figure(figsize=(10,10))
    corr_plot=sns.heatmap(corr,cmap="Reds",annot=True)
    
    # corr_pair=sns.pairplot(dataset['df'],hue=dataset['df']['outcome'])
    corr_pair=sns.pairplot(dataset['df'],hue="outcome")

    # return corr,corr_plot,corr_pair

    histogram_plots(dataset)

def histogram_plots(dataset):

    plt.figure(figsize=(10,10))
    # sns.histplot(data=dataset['df'], x="macd_H",bins=20, log_scale=True, hue="outcome")

    print(f'size of dataset: {dataset["df"].info()}')

    sns.histplot(data=dataset['df'], x="macd_H",y='macd',bins=20,hue="outcome")

    boxplots(dataset)

def boxplots(dataset):

    plt.figure(figsize=(10,10))
    ax = sns.boxplot(x=dataset['df']['macd'])





success=lambda x:sum([1 if i>0 else 0 for i in x])/len(x)

gain=lambda  x:sum([i for i in x if i >= 0])

loss=lambda  x:sum([i for i in x if i <0])

# %%

if __name__ == '__main__':

    send_results_to_file({'TRADE DATA REPORT':'------------>'},'w')
    ticker=['AEHR','APHA','KSHB','ADXS','CBWTF']
    ticker=['AEHR','APHA','KSHB','ADXS','CBWTF','SNDL','TSLA','GE','SENS','AT','DBVT']
    # ticker=['cron']
    date='2021-01-15'
    for i in ticker:
        send_results_to_file({'TRADE DATA FOR------>':i.upper()},'a')
        df=get_the_stock(i)

        macd_Xover(df)

    macd_crossover_pkg={'df':macd_Xover_df,'features':['macd','macd_H','rsi14','outcome']}
    tradeDataAnalysis(macd_crossover_pkg)

        
# %%
        

# %%
    plt.show()
# %%
