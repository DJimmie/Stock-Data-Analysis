""" Retrieve user reqested stock data.
Input--->Ticker, Start Date, End Date
Output---> time series stock data in specied frequency (daily, weekly, etc,) as pandas, json, or csv
"""
# %%
from dependancies import *

# %%
class StockData():
    def __init__(self,ticker,**kwargs):
        """optional arguments:
        start_date (YYYY-MM-DD)
        end_date (YYYY-MM-DD)
        interval"""

        self.ticker=ticker.upper()

        self.start_date = kwargs['start_date'] if 'start_date' in kwargs else None
        self.end_date = kwargs['end_date'] if 'end_date' in kwargs else None
        self.interval=kwargs['interval'] if 'interval' in kwargs else '1d'

        print(self.ticker)

        self.fdata=yf.Ticker(self.ticker)

        # self.get_fundamentals()

    def get_fundamentals(self):
        fundamentals=['sector','previousClose','ask','bid','askSize','bidSize','fiftyTwoWeekLow','fiftyTwoWeekHigh']
        fun=dict()
        for k,v in self.fdata.info.items():
            if k in fundamentals:
                fun.update({k:v})

        # print(fun)

        return fun
     

        # self.get_time_series_data()

    def get_time_series_data(self):
        # get historical market data
        hist = self.fdata.history(period='1y',interval=self.interval,start=self.start_date,end=self.end_date)

        # make headers and index name lowercase
        hist.columns = [x.lower() for x in hist.columns]
        # hist.drop(columns=['dividends','stock splits'],inplace=True)
        hist=hist.rename_axis("date")  

        return hist

        # self.option_data()

    def option_data(self,expire_date,requested_data='option_chain',strike_price=None,optionType='calls'):

        option_expirations=self.fdata.options
        print(option_expirations)  ##---> the option expiration dates for the given ticker


        data=self.fdata.option_chain(expire_date)
        # print(data) 

        data=(data.calls if optionType=='calls' else 
        data.puts if optionType=='puts' else
        data)

        if requested_data=='option_chain':
            return data
        elif requested_data=='last_option_price':
            the_query=f'strike=={strike_price}'
            i=data.query(the_query)['strike'].index[0]
            lastPrice=data.query(the_query)['lastPrice'][i]
            return lastPrice





# %%


# G=StockData(ticker='cron',start_date='2018-01-01',interval='1d')
# print(G.ticker)
# print(G.fdata)
    
    

# %%
