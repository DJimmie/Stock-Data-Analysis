""" Retrieve user reqested stock data. 
Input--->Ticker, Start Date, End Date
Output---> time series stock data in specied frequency (daily, weekly, etc,) as pandas, json, or csv
"""

from dependancies import *

class StockData():
    
    def __init__(self,ticker,**kwargs):

        self.ticker=ticker

        self.start_date = kwargs['start_date'] if 'start_date' in kwargs else None
        self.end_date = kwargs['end_date'] if 'end_date' in kwargs else None
        self.interval=kwargs['interval'] if 'interval' in kwargs else '1d'

        print(self.ticker)

        self.fdata=yf.Ticker(self.ticker)

        self.get_fundamentals()

    def get_fundamentals(self):
        
        fundamentals=['sector','previousClose','ask','bid','askSize','bidSize','strikePrice','fiftyTwoWeekLow','fiftyTwoWeekHigh']

        fun=dict()
        for k,v in self.fdata.info.items():
            if k in fundamentals:
                fun.update({k:v})

        print(fun)
        
        # print([{x:fdata.info.get(x)} for x in fundamentals])


        self.get_time_series_data()

    def get_time_series_data(self):
        # get historical market data
        hist = self.fdata.history(period='1y',interval=self.interval,start=self.start_date,end=self.end_date)

        print(hist)
        print(type(hist))

        self.option_data()

    def option_data(self):

        print(self.fdata.options)

        print(self.fdata.option_chain('2021-03-12'))

        # print(type(fdata.option_chain('2021-03-19')))



# StockData(ticker='GE',start_date='2019-01-01',end_date='2021-01-01')

G=StockData(ticker='GE',start_date='2020-01-01',end_date='2022-01-01',interval='1wk')


print(G.ticker)

print(G.fdata)
    
    
