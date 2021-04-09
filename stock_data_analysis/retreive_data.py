"""Request data from stock data source
--->receive data
--->clean-up
--->store data as pickle or json"""

# %%

import trade_scoring

stock_indicated_data=None

class Data():

    def __init__(self, ticker,**kwargs):

        self.ticker=ticker
        # self.start_date=start_date
        # self.stop_date=stop_date

        self.df=self.request_data()
        print(self.df.head())
        print(self.df.info())
        print(self.df.tail())

        self.data_clean_up()
        print(self.df.head())
        print(self.df.info())
        print(self.df.tail())





    def request_data(self):

        trade_scoring.user_inputs(self.ticker)

        print(trade_scoring.stock_indicated_data.head())

        return trade_scoring.stock_indicated_data



    def data_clean_up(self):
        keep=set(['close','RSI_14', 
       'INC_2', 'ROC_2', 'PSL_3', 'CDL_DOJI_3_0.1',
       'TRUERANGE_1', 'Z_30', 'ratio_M50M180',
       'ratio_M5M20', 'ratio_M20M50',
       'ratio_MACDh_12_26_9', 'obv_pct_delta','LRm_3_pct_delta','tr_pct_delta'])

        all_headers=set(['high', 'low', 'open', 'close', 'volume', 'adj_close', 'MACD_12_26_9',
       'MACDh_12_26_9', 'MACDs_12_26_9', 'RSI_14', 'SMA_5', 'SMA_20', 'SMA_50',
       'SMA_180', 'LRm_3', 'LR_3', 'INC_2', 'ROC_2', 'PSL_3', 'CDL_DOJI_3_0.1',
       'TRUERANGE_1', 'Z_30', 'OBV', 'dif_M50M180', 'ratio_M50M180',
       'dif_M5M20', 'ratio_M5M20', 'dif_M20M50', 'ratio_M20M50',
       'ratio_MACDh_12_26_9', 'obv_pct_delta', 'obv_pct_slope', 'sma_5_slope',
       'macd_slope','LRm_3_pct_delta','tr_pct_delta'])

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

        self.df.to_csv('data.csv',index=False)






    @staticmethod
    def dump_to_json_file(data):
                
        with open('data_as_json.json', "w") as write_file:
            json.dump(data, write_file)

    @staticmethod
    def load_json_file(a):
        
        with open('data_as_json.json', "r") as read_file:
            data = json.load(read_file)

        return data


    
# %%

# ge=Data('ge')

# tsla=Data('tsla')

# apha=Data('apha')

mro=Data('mro')






# %%

# %%
