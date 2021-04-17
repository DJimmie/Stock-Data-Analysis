"""Request data from stock data source
--->receive data
--->clean-up
--->store data as pickle or json"""

# %%

import trade_scoring

global training_data

stock_indicated_data=None

class Data():

    def __init__(self, ticker,**kwargs):

        self.ticker=ticker
        
        self.start_date = kwargs['start_date'] if 'start_date' in kwargs else None
        self.stop_date = kwargs['stop_date'] if 'stop_date' in kwargs else None


        self.df=self.request_data()
        print(self.df.head())
        print(self.df.info())
        print(self.df.tail())

        self.data_clean_up()
        print(self.df.head())
        print(self.df.info())
        print(self.df.tail())


    def request_data(self):

        trade_scoring.user_inputs(ticker=self.ticker,start_date=self.start_date,stop_date=self.stop_date)

        print(trade_scoring.stock_indicated_data.head())

        return trade_scoring.stock_indicated_data



    def data_clean_up(self):
        keep=set(['close','RSI_14', 
       'INC_2', 'ROC_2', 'PSL_3', 'CDL_DOJI_3_0.1',
       'TRUERANGE_1', 'Z_30', 'ratio_M50M180',
       'ratio_M5M20', 'ratio_M20M50',
       'ratio_MACDh_12_26_9', 'obv_pct_delta',
       'LRm_3_pct_delta','tr_pct_delta','M_ovr_S',
       'sma5_ovr_sma20',
       'sma20_ovr_sma50',
       'sma50_ovr_sma180',
       'Z_30_pct_delta'
       ])


        list_of_headers=list(self.df.columns)

        all_headers=set(list_of_headers)

    #     all_headers=set(['high', 'low', 'open', 'close', 'volume', 'adj_close', 'MACD_12_26_9',
    #    'MACDh_12_26_9', 'MACDs_12_26_9', 'RSI_14', 'SMA_5', 'SMA_20', 'SMA_50',
    #    'SMA_180', 'LRm_3', 'LR_3', 'INC_2', 'ROC_2', 'PSL_3', 'CDL_DOJI_3_0.1',
    #    'TRUERANGE_1', 'Z_30', 'OBV', 'dif_M50M180', 'ratio_M50M180',
    #    'dif_M5M20', 'ratio_M5M20', 'dif_M20M50', 'ratio_M20M50',
    #    'ratio_MACDh_12_26_9', 'obv_pct_delta', 'obv_pct_slope', 'sma_5_slope',
    #    'macd_slope','LRm_3_pct_delta','tr_pct_delta'])

 

        required_headers=list(all_headers.difference(keep))

        # remove un-needed columns (features)
        self.df.drop(required_headers, axis=1,inplace=True)
        print(self.df.head())

        # remove datetime index
        self.df.reset_index(drop=True, inplace=True)
        print(self.df.head())

        # get the price (close) delta
        self.df.loc[self.df['close'].diff()<0, 'PL'] = 0
        self.df.loc[self.df['close'].diff()>=0, 'PL'] = 1



        self.df.dropna(inplace=True)

        self.df=self.df.sample(frac=1)

        # pass data to storage

        if training_data==True:
            self.df.to_csv('data.csv',index=False)


    


    
# %%

training_data=False

if training_data==True:
    the_stock=Data(ticker='ge',start_date='2016-01-01',stop_date=None)
else:
    the_stock=Data(ticker='cdev',stop_date='2021-03-16')








# %%

