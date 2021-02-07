# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import calendar
import os
import sys
import logging

from pylab import rcParams
import statsmodels.api as sm
rcParams['figure.figsize'] = 11, 9

from statsmodels.tsa.seasonal import STL
from pandas.plotting import register_matplotlib_converters

sys.path.insert(0,"C:\\Users\\dowdj\\OneDrive\\Documents\\GitHub\\my-modules-and-libraries\\program_work_dir")  # Temporary. Used to help finish development of modules.
import program_work_dir as pwd

import yfinance as yf
import pandas_datareader as pdr
import pandas_datareader.data as web

from collections import deque

import pprint

import stockstats
from stockstats import StockDataFrame as Sdf

import pandas_ta as ta



register_matplotlib_converters()
# sns.set_style('darkgrid')

plt.rc('figure',figsize=(16,12))
plt.rc('font',size=13)

# %%

NUM_SHARES=100
MOVING_AVG_PERIOD=20
MACD_DIFFERENCE=1
sigma_price_diff=3
START_DATE='2020-10'
END_DATE='2021'
feature='Close'   

# %%
# Create program working folder and its subfolders
config_parameters={'database server':{'sqlite_server':'N/A'}}
client=pwd.ClientFolder(os.path.basename(__file__),config_parameters)
ini_file=f'c:/my_python_programs/{client}/{client}.ini'

log_file=f'c:/my_python_programs/{client}/{client}_log.log'
logging.basicConfig(filename=log_file, level=logging.INFO, filemode='w', format=' %(asctime)s -%(levelname)s - %(message)s')
logging.info('Start')




# %%
# ------> get the time series data; setting the Datetime as Index

class RawData():
    """Get the csv file and output a pandas dataframe with the Datetime as an index."""

    def __init__(self,datafile,index_col):
        self.datafile=datafile
        self.index_col=index_col
        self.get_raw_data()

    def get_raw_data(self):

        self.df = pd.read_csv(self.datafile, parse_dates=True, index_col = self.index_col)
        print(self.df.head())
        print(self.df.info())

        # self.p=DataPlot(self.df)

    def data_sub_set(self,start,stop,cols):

        self.subset=self.df.loc[start:stop, cols]

        subset=pd.DataFrame(self.subset)
        print(subset.head())
        
        return subset

    def resample(self,freq):

        self.rs=self.df.resample(freq).mean()

        print(self.rs)

        return self.rs


     
class DataPlot():
    """Visuallizations the various Time Series plots"""

    def __init__(self,df,show=False):
        self.df=df
        self.show=show
        # self.plot1()

    def plot1(self):

        self.df.plot(subplots=True, layout=None, figsize=(15, 10), sharex=True)
        plt.grid()

        # if self.show:
        #     plt.show()

    def shift_plot(self,col,shift=1,yscale='linear'):

        fig, ax = plt.subplots(nrows=3,ncols=1,sharex=True,figsize=(10, 6))
        fig.suptitle(f'Shift Plot: {col.upper()}-{stock_name}', fontsize=16)
        ax[0].set_title(f'{col}')
        ax[0].set_yscale(yscale)
        ax[0].plot(self.df[col], color='black')
        ax[0].grid()
        shift_name=f'{col}_shift_{shift}'
        shift_value = self.df[col].div(self.df[col].shift(shift))
        ax[1].set_title(f'{col}--->shift({shift})')
        ax[1].set_yscale(yscale)
        ax[1].plot(shift_value, color='coral')
        ax[1].grid()

        ax[2].set_yscale(yscale)
        ax[2].bar(shift_value.index,abs(shift_value), color=['red' if i<1 else 'green' for i in shift_value])
        ax[2].grid()

        # if self.show:
        #     plt.show()

    def pct_change_plot(self,col,shift=1,yscale='linear'):

        fig, ax = plt.subplots(nrows=2,ncols=1,sharex=True,figsize=(10, 6))
        fig.suptitle(f'Percent Change Plot: {col.upper()}-{stock_name}', fontsize=16)
        ax[0].set_title(f'{col}')

        ax[0].set_yscale(yscale)

        ax[0].plot(self.df.loc[:, col], color='black')
        ax[0].grid()

        shift_name=f'{col}_percent_change_{shift}'
        pct = self.df[col].pct_change(shift)*100
        ax[1].set_title(f'{col}--->percent change({shift})')

        ax[1].set_yscale(yscale)
        ax[1].bar(pct.index,abs(pct), color=['red' if i<0 else 'green' for i in pct])
        ax[1].grid()


        # if self.show:
        #     plt.show()

    def diff_plot(self,col,shift=1,yscale='linear'):

        fig, ax = plt.subplots(nrows=3,ncols=1,sharex=True,figsize=(10, 6))
        fig.suptitle(f'Difference Plot: {col.upper()}-{stock_name}', fontsize=16)
        ax[0].set_title(f'{col}')
        ax[0].plot(self.df.loc[:, col], color='black')
        ax[0].grid()

        shift_name=f'{col}_Differencing_{shift}'
        diff = self.df[col].diff(shift)
        ax[1].set_title(f'{col}--->Difference({shift})')
        # ax[1].set_yscale('log')
        ax[1].plot(diff, color='blue')
        ax[1].grid()

        ax[2].set_yscale(yscale)
        ax[2].bar(diff.index,abs(diff), color=['red' if i<0 else 'green' for i in diff])
        ax[2].grid()


        # if self.show:
        #     plt.show()

    def expanding_window(self,col,shift=1):
        fig, ax = plt.subplots(nrows=1,ncols=1,sharex=False,figsize=(10, 6))
        fig.suptitle(f'Expanding Window: {col.upper()}-{stock_name}', fontsize=16)
        ax.set_title(f'{col}')
        ax=self.df[col].plot(label=f'{col}')
        ax=self.df[col].expanding().mean().plot(label=f'{col} expanding mean')
        ax=self.df[col].expanding().median().plot(label=f'{col} expanding median')
        ax=self.df[col].expanding().std().plot(label=f'{col} expanding std')
        # ax=self.df[col].expanding().sum().plot(label=f'{col} expanding sum')

        ax.legend()
        plt.grid()

        # if self.show:
        #     plt.show()
        
    def rolling_window(self,col,period=MOVING_AVG_PERIOD):
        fig, ax = plt.subplots(nrows=1,ncols=1,sharex=False,figsize=(10, 6))
        fig.suptitle(f'Rolling Window: {col.upper()}-{stock_name}', fontsize=16)
        ax.set_title(f'{col}')
        ax=self.df[col].plot(label=f'{col}')
        mu=self.df[col].rolling(period,center=False).mean()
        ax=self.df[col].rolling(period,center=False).mean().plot(label=f'{col} {period} Moving Avg')
        sigma=self.df[col].rolling(period,center=False).std()
        minus_2sigma=(mu-2*sigma)
        plus_2sigma=(mu+2*sigma)
        ax=minus_2sigma.plot(label=f'{col} {period} -2 sigma',color='red',alpha=0.2)
        ax=plus_2sigma.plot(label=f'{col} {period} +2 sigma',color='red',alpha=0.2)
        ax=plt.fill_between(self.df[col].index,plus_2sigma,minus_2sigma,alpha=0.2)
        print(f'sigma:{minus_2sigma}')

        mu_10=self.df[col].rolling(10,center=False).mean() #---> 10 period moving avg
        ax=mu_10.plot(label=f'{col} 10 Moving Avg')

        mu_50=self.df[col].rolling(50,center=False).mean() #---> 50 period moving avg
        ax=mu_50.plot(label=f'{col} 50 Moving Avg',color='black')

        plt.legend()
        plt.grid()
        
        # if self.show:
        #     plt.show()

        self.volume()
        self.macd(col)
        self.two_sigma_delta(col,minus_2sigma=minus_2sigma,plus_2sigma=plus_2sigma,mavg=mu)
        self.rsi()
        

    def hist_plot(self,col):
        fig, ax = plt.subplots(nrows=2,ncols=1,sharex=False,figsize=(10, 6))
        fig.suptitle(f'Histogram Plot: {col.upper()}-{stock_name}', fontsize=16)
        ax[0].set_title(f'{col}')
        ax[0].plot(self.df.loc[:, col], color='black')
        ax[0].grid()

        ax[1].set_title(f'{col}--->Histogram')
        # ax[1].set_yscale('log')
        ax[1].hist(self.df[col],bins=100, density=True, color='blue')
        ax[1].grid()


    def macd(self,col,yscale='linear'):
        fig, ax = plt.subplots(nrows=2,ncols=1,sharex=True,figsize=(10, 6))
        fig.suptitle(f'MACD: {col.upper()}-{stock_name}', fontsize=16)
        

        exp1 = self.df[col].ewm(span=12, adjust=False).mean()
        exp2 = self.df[col].ewm(span=26, adjust=False).mean()
        macd = self.macd = exp1-exp2
        exp3 = self.exp3=macd.ewm(span=9, adjust=False).mean()   # ---> signal

        ax[0].set_title(f'{col}')
        ax[0].plot(macd.index,macd,label='MACD', color = '#4C0099',marker='o')
        ax[0].plot(exp3.index,exp3,label='Signal Line', color='#FF9933')
        ax[0].axhline(0,color='black',linestyle='--')
        ax[0].fill_between(macd.index, macd,exp3, where=(macd > exp3), facecolor='green', alpha=0.5)
        ax[0].fill_between(macd.index, macd,exp3, where=(macd < exp3), facecolor='red', alpha=0.5)

        ax[0].grid()
        ax[0].legend()

        diff = macd.diff(MACD_DIFFERENCE)
        ax[1].set_yscale(yscale)
        ax[1].bar(diff.index,diff, color=['red' if i<0 else 'green' for i in diff])
        ax[1].set_title(f'{col}-MACD DIFF({MACD_DIFFERENCE})')
        ax[1].grid()

        plt.legend()
        # plt.grid()

        self.macd_Xover(macd=macd,signal=exp3)

        self.macd_inversions(macd=diff)

    def macd_Xover(self,macd,signal):
        """Capture data from MACD crossover. 
        Input---->MACD,signal
        Output---->"""

        # make a dataframe
        d={'macd': macd, 'signal': signal}
        c=pd.DataFrame(data=d)
        print(f'macd_xovr_dataframe: {c}')

        
        # checking for crossovers and retrieving the xovr date index
        status=False
        start_list=[]
        stop_list=[]
        stock_buy=[]
        stock_sell=[]
        for index, row in c.iterrows():
            if status==False:
                if row[0]>row[1]:
                    start=index
                    print(f'START--->{index}--->{row[0]}')
                    send_results_to_file({'MACD XOVR START':index},'a')
                    start_list.append(start)
                    stock_buy.append(self.df.loc[start]['Close'])
                    status=True
            
            if status==True:
                if row[0]<=row[1]:
                    stop=index
                    print(f'STOP--->{index}--->{row[0]}')
                    send_results_to_file({'MACD XOVR STOP':index},'a')
                    stop_list.append(stop)
                    print(f'CLOSE------->{self.df.loc[stop]["Close"]}')
                    stock_sell.append(self.df.loc[stop]['Close'])
                    status=False

        # print(f'{start_list}\n{stock_buy}\n{stop_list}\n{stock_sell}')
        print(f'{start_list}\n\n{stop_list}\n')

        # Tally results---->

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

        send_results_to_file({'Profit/Loss (USD)':PL,'Duration (days)':duration},'a')

        my_data={
            'start':[a.date().strftime("%Y-%m-%d") for a in start_list],
            'PL':PL}

        print(my_data)

        collect_data(trade_data=my_data,strategy='MACD Xover')


    def macd_inversions(self,macd):
        """Triggering on the MACD shift(1) inversions"""

        # diff = pd.DataFrame(macd.diff()).dropna()
        diff = pd.DataFrame(macd).dropna()
        print(diff)

        start_list=[]
        stop_list=[]
        stock_buy=[]
        stock_sell=[]
        q = deque()
        
        trade_in_progress=0
        verify=0

        assume_above_signal=True
        for c,k in enumerate(diff[feature]):
            q.append(k)
            if len(q)==2:
                down=all([q[0]>0,q[1]<0])
                up=all([q[0]<0,q[1]>0])
                if assume_above_signal: #-->latching feature to get macd started from down looking up.
                    below_signal_check=all([q[0]<0,q[1]<0])  #-->two negative macd diff to ensure starting with macd below signal.
                    if not below_signal_check:
                        q.popleft()
                        continue
                    else:
                        assume_above_signal=False

                if up==True and trade_in_progress==0:
                    trigger_date=diff.index[c]
                    trigger_price=self.df[feature][trigger_date]
                    print(f'{q}---->{trigger_date}--->{trigger_price}')
                    print('up')
                    start_list.append(trigger_date)
                    stock_buy.append(trigger_price)
                    trade_in_progress=1
                    q.popleft()
                    continue
                
                # elif (down==True and (self.macd[c+1]<self.exp3[c+1]) and trade_in_progress==1):
                elif (trade_in_progress==1):
                    # print(f'index check:{self.macd[c+1]}--->{self.exp3[c+1]}--->{diff.index[c]}')
                    
                    if verify==0:
                        if down==True:
                            verify=1
                    if verify==1:
                        if (self.macd[c+1]<self.exp3[c+1]):
                            trade_in_progress=0
                            verify=0

                            exit_date=diff.index[c]
                            exit_price=self.df[feature][exit_date]
                            print(f'{q}---->{exit_date}--->{exit_price}')
                            print('get out')
                            stop_list.append(exit_date)
                            stock_sell.append(exit_price)
                    
                    q.popleft()
                    continue
                else:
                    # print(q)
                    q.popleft()
                    continue

        print(f'diff---->{diff.head()}')
        inversion_in_trigger=[a.date().strftime("%Y-%m-%d") for a in start_list]
        inversion_out_trigger=[a.date().strftime("%Y-%m-%d") for a in stop_list]
        inversion_entry_price=[round(i,2) for i in stock_buy]
        inversion_exit_price=[round(i,2) for i in stock_sell]

        duration=[a - b for a,b in zip(stop_list, start_list)]
        duration=[a.days for a in duration]

        PL=[i-k for i,k in zip(inversion_exit_price,inversion_entry_price)]
        PL=[round(i*NUM_SHARES,2) for i in PL]
        net_PL=sum(PL)

        print(f'Start: {inversion_in_trigger}\nEntry Price: {inversion_entry_price}\n')
        print(f'Stop: {inversion_out_trigger}\nExit Price: {inversion_exit_price}')

        print(f'PL: {PL}')
        print(f'gain: $ {gain(PL)}')
        print(f'loss: $ {loss(PL)}')
        print(f'Net PL: ${net_PL}')
        print(f'Successful Trade Percentage: {round(success(PL)*100,2)} %')

        print(f'Inversion Durations: {duration}')

        send_results_to_file({'--------------------------------->':'Inversion Study'.upper()},'a')
        send_results_to_file({'Trigger In Date':inversion_in_trigger,'Trigger Out Date':inversion_out_trigger},'a')
        send_results_to_file({
        'Entry Price':inversion_entry_price,
        'Exit Price':inversion_exit_price,
        'Profit/Loss':PL})

        send_results_to_file({
        'Gain':gain(PL),
        'Loss':loss(PL),
        'Net PL':net_PL,
        'Successful Trade Percentage':f"{round(success(PL)*100,2)} %"})

        print(f'size of start:{len(start_list)}\nsize of stop:{len(stop_list)}')

        my_data={
            'start':[a.date().strftime("%Y-%m-%d") for a in start_list],
            'PL':PL}

        print(my_data)

        collect_data(trade_data=my_data,strategy='MACD Inversion')



    def two_sigma_delta(self,col,minus_2sigma,plus_2sigma,mavg):
        fig, ax = plt.subplots(nrows=1,ncols=1,sharex=True,figsize=(10, 6))
        fig.suptitle(f'2-Sigma Width: {col.upper()}-{stock_name}\nDiff({sigma_price_diff})', fontsize=16)

        color=['red' if i<0 else 'green' for i in self.df[col].diff(sigma_price_diff)]
        color[0]='black'

        
        # width=plus_2sigma-minus_2sigma
        width=((plus_2sigma-minus_2sigma)/mavg)*100

        ax.set_title(f'{col}')
        # ax.plot(width.index,width,label='2-Sigma Width', color ='blue' ,marker='o',markerfacecolor=color)  # --->original color: '#4C0099'
        ax.bar(width.index,width,label='2-Sigma Width', color =color)
        ax.set_ylim([0,100])
        ax.grid()

    def rsi(self):
        """Compute and plot the RSI using the stockstats library. """
        
        rsi_indicator=['close','rsi_6','rsi_14']
        a=self.rsi_data=stock_indicators(df=self.df,indicators=rsi_indicator)
        print(a.head())

        fig, ax = plt.subplots(nrows=3,ncols=1,sharex=True,figsize=(10, 6))
        fig.suptitle(f'RSI: {feature.upper()}-{stock_name}', fontsize=16)

        ax[0].set_title(f'{feature}')
        ax[0].plot(a.index,a[feature.lower()],label='Close', color = '#4C0099',marker='o')
        ax[0].grid()
        ax[0].legend()

        # ax[1].set_title(f'{feature}')
        ax[1].plot(a.index,a[rsi_indicator[1]],label=rsi_indicator[1], color = '#4C0099',marker='o')
        ax[1].axhline(80,color='black',linestyle='--')
        ax[1].axhline(30,color='black',linestyle='--')
        ax[1].fill_between(a.index, a[rsi_indicator[1]],80, where=(a[rsi_indicator[1]] > 80), facecolor='red', alpha=0.5)
        ax[1].fill_between(a.index, a[rsi_indicator[1]],30, where=(a[rsi_indicator[1]] < 30), facecolor='red', alpha=0.5)
        ax[1].set_ylim([0,100])
        ax[1].grid()
        ax[1].legend()

        # ax[1].set_title(f'{feature}')
        ax[2].plot(a.index,a[rsi_indicator[2]],label=rsi_indicator[2], color = '#4C0099',marker='o')
        ax[2].axhline(80,color='black',linestyle='--')
        ax[2].axhline(30,color='black',linestyle='--')
        ax[2].fill_between(a.index, a[rsi_indicator[2]],80, where=(a[rsi_indicator[2]] > 80), facecolor='red', alpha=0.5)
        ax[2].fill_between(a.index, a[rsi_indicator[2]],30, where=(a[rsi_indicator[2]] < 30), facecolor='red', alpha=0.5)
        ax[2].set_ylim([0,100])
        ax[2].grid()
        ax[2].legend()


        # return self.rsi_data

        
        
    def volume(self):
        "Plot volume shares"

        a=self.df[['Close','Volume']]

        fig, ax = plt.subplots(nrows=2,ncols=1,sharex=True,figsize=(10, 6))
        fig.suptitle(f'VOLUME: {feature.upper()}-{stock_name}', fontsize=16)

        ax[0].set_title(f'{feature}')
        ax[0].plot(a.index,a[feature],label='Close', color = '#4C0099',marker='o')
        ax[0].grid()
        ax[0].legend()

        diff = a['Close'].diff()
        mu=a['Volume'].rolling(14,center=False).mean()
        # ax[1].set_yscale(yscale)
        ax[1].bar(a.index,a['Volume'], color=['red' if i<0 else 'green' for i in diff])
        ax[1].plot(mu.index,mu,label='14 day mavg', color = 'black',marker=None)
        ax[1].set_title(f'VOLUME:{stock_name}')
        ax[1].grid()

        plt.legend()

        return


class TSAnalysis():
    """TS Analysis"""

    def __init__(self,df):
        self.df=df
        self.decompose()

    def decompose (self,col=feature):
        # decomposition = sm.tsa.seasonal_decompose(pd.DataFrame(self.df[col]), model='Additive')
        # fig = decomposition.plot()
        a=self.df[col]
        b=a.index
        c=pd.infer_freq(b)
        
        d = pd.Series(a, index=pd.date_range(b.date[0], b.date[len(a)-1], periods=None, freq=c), name = col)
        
        print(d)
        # x=pd.Series(p.values,index=p.index.values)
        stl = STL(d, seasonal=7)
        res = stl.fit()
        fig = res.plot()
        plt.show()


# %%

def stock_indicators(df,indicators,**kwargs):
    """ Stock indicators generated by the stockStat library"""

    s=Sdf.retype(df)
    # s[indicators].plot(subplots=True,figsize=(10,6), grid=True)

    print(s.head())
    print(s[indicators].dropna())

    
    return s[indicators].dropna()


def collect_data(trade_data,strategy):
    """Assemble specified stock indicators when entering trade"""

    # bring in dict with the list of entry (start) dates and the PL list
    print(f'TRADE DATA---->{trade_data}')

    # remove the most recent start date if the trade is still open. This make all list equal in length.
    if len(trade_data['start'])>len(trade_data['PL']):
        trade_data['start'].pop()

    
    df=stock.df.copy(deep=True)  #--->** It is essential to make a copy.

    # create the trade outcome list 
    trade_data['outcome']=[1 if i>0 else 0 for i in trade_data['PL']]

    print(f'OUTCOME---->{trade_data["outcome"]}')
    
    # gather stock indicator data at the trade entry date
    indicators=['macd','rsi_6','rsi_14','boll','boll_ub','boll_lb','volume_delta']
    k=Sdf.retype(df)
    # s[indicators].plot(subplots=True,figsize=(10,6), grid=True)
    df[indicators]=k[indicators].dropna()
    print(f'DATA HEAD---->{df.tail()}')

    # ---> Loop thru the start dates and pull the indicators for those dates

    trade_data['MACD']=[round(df.at[i,'macd'],7) for i in trade_data['start']]
    trade_data['MACDH']=[round(df.at[i,'macdh'],7) for i in trade_data['start']]
    trade_data['RSI14']=[round(df.at[i,'rsi_14'],7) for i in trade_data['start']]
    trade_data['RSI6']=[round(df.at[i,'rsi_6'],7) for i in trade_data['start']]
    trade_data['BOLL']=[round(df.at[i,'boll'],7) for i in trade_data['start']]
    trade_data['BOLL_UB']=[round(df.at[i,'boll_ub'],7) for i in trade_data['start']]
    trade_data['BOLL_LB']=[round(df.at[i,'boll_lb'],7) for i in trade_data['start']]
    trade_data['BOLL_WIDTH']=[i-k for i,k in zip(trade_data['BOLL_UB'],trade_data['BOLL_LB'])]
    trade_data['BOLL_WIDTH_PCT']=[((i-k)/j)*100 for i,k,j in zip(trade_data['BOLL_UB'],trade_data['BOLL_LB'],trade_data['BOLL'])]
    trade_data['VOL_DELTA']=[round(df.at[i,'volume_delta'],7) for i in trade_data['start']]

    print(f'TRADE DATA DICT---->\n{trade_data}')

    tradeData=pd.DataFrame.from_dict(trade_data)

    print(tradeData)

    send_results_to_file({'--------------------------------->':'Trade Data for Analysis'.upper()},'a')
    send_results_to_file({'Dataset':tradeData},'a')

    trade_data_analysis(tradeData,strategy)


def trade_data_analysis(tradeData,strategy):

    x="VOL_DELTA"
    return

    fig, ax = plt.subplots(nrows=1,ncols=1,sharex=False,figsize=(10, 6))
    fig.suptitle(f'Histogram Plot: {strategy}', fontsize=16)
    ax.set_title(f'{x}')

    # p=[i for i in tradeData.loc[:,x] if i<]

    pos=[]
    neg=[]
    for index,row in tradeData.iterrows():
        if row['outcome']==1:
            pos.append(row[x])
        else:
            neg.append(row[x])


    # ax.hist(tradeData.loc[:, x],bins=50,density=True, color='blue')
    ax.hist(pos,bins=80,density=True, color='blue',alpha=.5)
    ax.hist(neg,bins=80,density=True, color='red',alpha=.5)
    ax.grid()




   
def ta_stock_Indicators(df):
    """Stock indicators genereted by the pandas-ta library"""

    df.ta.vwap(cumulative=True, append=True)

    df=df.dropna()
    print(df.columns)

    print(df.tail())

    print(df.ta.indicators())

    #   
    # df.VWAP.plot()
    print(help(ta.linreg))






## FUNCTIONS----------------------------------FUNCTIONS----------------------------------FUNCTIONS
def get_config_values(section,option):
    """Used to retrieve values from the program's configuration file."""
    config=pwd.configparser.ConfigParser()
    config.read(ini_file)

    return config[section][option]


def exit_operations():
    """Operations to perform prior to the program exit"""
    # remove images from the image folder after each session

    # save the table as a json file in the working directory
    pass


def send_results_to_file(data,file_action='a'):

    output_s = pprint.pformat(data)
    with open('output.txt', file_action) as file:
        file.write(output_s)
        file.write('\n\n')



success=lambda x:sum([1 if i>0 else 0 for i in x])/len(x)

gain=lambda  x:sum([i for i in x if i >= 0])

loss=lambda  x:sum([i for i in x if i <0])


## MAIN----------------------------------MAIN----------------------------------MAIN
# %%

if __name__ == '__main__':
    

    data_source='from Web'  # options--> 'from Web' --- 'on PC'

    stock_list=['ASX','ABUS','CBWTF']

    position_list=['AEHR','APHA','KSHB','ADXS','CBWTF']

    my_stocks={
        'Cannibus':['APHA','KSHB','CBWTF','CRON'],
        'Drones':['NVDA','AMBA','AVAV'],
        'Energy':['PBD','FAN'],
        'Healthcare':['ADMS']
    }

    if data_source=='on PC':
        data="BDR.csv"   
        data_file=f'c:/my_python_programs/{client}/{data}'
        stock_name=symbol=data.split('.')[0]
        stock=DataPlot(RawData(data_file,'Date').df)
    elif (data_source=='from Web'):
        symbol = 'ammj'.upper() #'ALOT'  
        stock_name=symbol
        stock =DataPlot(pdr.get_data_yahoo(symbol)[START_DATE:END_DATE])

    send_results_to_file({'NUM_SHARES':NUM_SHARES,'Ticker':symbol},'w')

    # %%
    
    stock.rolling_window(feature,MOVING_AVG_PERIOD)

# %%
    # stock.rsi(feature)

# %%
    # rsi_indicator=['close','rsi_6','rsi_14']

    # stock_indicators(stock.df,'macd')

# %%
    # ta_stock_Indicators(df=stock.df)




# %%
    # stock_tsa=TSAnalysis(stock.df)

    plt.show()

# %%
