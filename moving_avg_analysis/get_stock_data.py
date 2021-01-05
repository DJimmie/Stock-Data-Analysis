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


register_matplotlib_converters()
# sns.set_style('darkgrid')

plt.rc('figure',figsize=(16,12))
plt.rc('font',size=13)

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
        
    def rolling_window(self,col,period=1):
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
        plt.legend()
        plt.grid()
        
        # if self.show:
        #     plt.show()

        self.macd(col)
        self.two_sigma_delta(col,minus_2sigma=minus_2sigma,plus_2sigma=plus_2sigma)

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
        macd = exp1-exp2
        exp3 = macd.ewm(span=9, adjust=False).mean()

        ax[0].set_title(f'{col}')
        ax[0].plot(macd.index,macd,label='MACD', color = '#4C0099',marker='o')
        ax[0].plot(exp3.index,exp3,label='Signal Line', color='#FF9933')
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
        
        assume_above_signal=True
        for c,k in enumerate(diff[feature]):
            q.append(k)
            if len(q)==2:
                down=all([q[0]>0,q[1]<0])
                up=all([q[0]<0,q[1]>0])
                if assume_above_signal:
                    below_signal_check=all([q[0]<0,q[1]<0])  # two negative macd diff.
                    if not below_signal_check:
                        q.popleft()
                        continue
                    else:
                        assume_above_signal=False
                if up==True:
                    trigger_date=diff.index[c]
                    trigger_price=self.df[feature][trigger_date]
                    print(f'{q}---->{trigger_date}--->{trigger_price}')
                    print('up')
                    start_list.append(trigger_date)
                    stock_buy.append(trigger_price)
                    q.popleft()
                    continue
                
                elif (down==True):
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

    def two_sigma_delta(self,col,minus_2sigma,plus_2sigma):
        fig, ax = plt.subplots(nrows=1,ncols=1,sharex=True,figsize=(10, 6))
        fig.suptitle(f'2-Sigma Width: {col.upper()}-{stock_name}\nDiff({sigma_price_diff})', fontsize=16)

        color=['red' if i<0 else 'green' for i in self.df[col].diff(sigma_price_diff)]
        color[0]='black'

        # print(f'color:{color}\nlen of color:{len(color)}\nlen of width:{len(plus_2sigma)}')

        width=plus_2sigma-minus_2sigma
        ax.set_title(f'{col}')
        # ax.plot(width.index,width,label='2-Sigma Width', color ='blue' ,marker='o',markerfacecolor=color)  # --->original color: '#4C0099'
        ax.bar(width.index,width,label='2-Sigma Width', color =color)
        ax.grid()

    def rsi(self,col):
        pass

class TSAnalysis():
    """TS Analysis"""

    def __init__(self,df):
        self.df=df

    def decompose (self,col):
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
NUM_SHARES=100
MACD_DIFFERENCE=1
sigma_price_diff=1

data_source='from Web'  # options--> 'from Web' --- 'on PC'

stock_list=['ASX','ABUS','CBWTF']
position_list=['AEHR','APHA','KSHB']

if data_source=='on PC':
    data="BDR.csv"   #"TSLA.csv" #"APHA.csv" #"KSHB.csv" #"CBWTF.csv" 
    data_file=f'c:/my_python_programs/{client}/{data}'
    stock_name=symbol=data.split('.')[0]
    stock=DataPlot(RawData(data_file,'Date').df)
elif (data_source=='from Web'):
    symbol = 'APHA'.upper() #'ALOT'  
    stock_name=symbol
    stock =DataPlot(pdr.get_data_yahoo(symbol)['2019':'2021'])

feature='Close'          #'Adj Close'

send_results_to_file({'NUM_SHARES':NUM_SHARES,'Ticker':symbol},'w')

# %%
stock


# stock.plot1()


# %%
stock.rolling_window(feature,20)

# stock.diff_plot('Volume')

plt.show()

# %%
