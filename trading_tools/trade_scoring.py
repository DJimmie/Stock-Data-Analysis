"""Retrievies requested stocks, calculates current day indicators and generates a trade 'enthusiasm' score based on the traders criteria.""" 

from dependencies import *
import csv


global trade_status_line, baseline_scores,last_Close
trade_status_line=dict()
baseline_scores=dict()
last_Close=None



def get_nasdaq_tickers(sector):
    """Getting a list of tickers"""

    tickers=[]
    line=0
    with open('nasdaq_screener.csv','r') as f:
        
        reader=csv.reader(f)
        if line==0:
            header=next(reader)
        
        if header!=None:
            line=1
            for row in reader:
                criteria=all([int(row[8])>5_000_000,row[9]==sector])
                if criteria:
                    tickers.append(row[0])
                
    print(tickers)

    return tickers


def user_inputs(tradeType,ticker):
    """User specifies list of stocks to review and score. User also inputs the date range and the interval of the stock data.
    Inputs are stored in a dictionary."""
    
    my_stocks={
    'options':[ticker],
    'stocks':[ticker],
    }

    print(f'03042021------->{my_stocks}')
    print(f'03042021------->{ticker}')

    inputs={
        'stock_list':my_stocks[tradeType],
        'start_date':'2020',
        'stop_date':'2021'}
    
    retrieve_OHLC_data(inputs)

def retrieve_OHLC_data(inputs):
    """
    Input---> list of stocks
    Output ---> dictionary with ticker symbol keys and the retrieve OHLC dataframe as values
    """
    global stock_dict,symbol,CURRENT_DATE
    stock_dict=dict()

    print(f'03042021---------->{inputs}')
    
    for i in inputs['stock_list']:
        # send_results_to_file({'TRADE DATA FOR------>':i.upper()},'a')
        symbol = i.upper() 
        stock_name=symbol
        stock =pdr.get_data_yahoo(symbol)[inputs['start_date']:inputs['stop_date']]
        if len(stock)<180:
            print(len(stock))
            continue
        stock_dict[i]=stock

        CURRENT_DATE=stock.iloc[[-1]].index.date[0].strftime("%Y-%m-%d")
        print(CURRENT_DATE)

        GenerateIndicators(stock_dict[i])


def GenerateIndicators(df):
    """generate the stock indictors for the stock OHLCV data"""

    df=trade_criteria_dataset(df)

    print(last_Close)

    print(df.head())

    print(df.tail())

    send_results_to_file({'Ticker':symbol,'dataset':df.tail()},'a')

    print(df.loc[CURRENT_DATE])
    indicator_dict=df.loc[CURRENT_DATE].to_dict()

    
    print(indicator_dict)

    send_results_to_file({'Ticker':symbol,'Results':indicator_dict},'a')

    trade_criteria(indicator_dict)


def trade_criteria_dataset(df):

    global last_Close
    # make a dataframe
    df.ta.macd(append=True)
    df.ta.rsi(append=True)
    df.ta.sma(length=5,append=True)
    df.ta.sma(length=20,append=True)
    df.ta.sma(length=50,append=True)
    df.ta.sma(length=180,append=True)

    df['dif_M50M180']=df['SMA_50']-df['SMA_180' ]
    df['ratio_M50M180'] = df['dif_M50M180'].div(df['dif_M50M180'].shift(1))

    df['dif_M5M20']=df['SMA_5']-df['SMA_20' ]
    df['ratio_M5M20'] = df['dif_M5M20'].div(df['dif_M5M20'].shift(1))

    df['dif_M20M50']=df['SMA_20']-df['SMA_50' ]
    df['ratio_M20M50'] = df['dif_M20M50'].div(df['dif_M20M50'].shift(1))

    df['ratio_MACDh_12_26_9'] = df['MACDh_12_26_9'].div(df['MACDh_12_26_9'].shift(1))

    df.dropna(inplace=True)

    last_Close=df['close'][CURRENT_DATE]
    
    

    return df

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

    if indicator_dict['SMA_5']>indicator_dict['SMA_20']:
        trade_status_line[symbol]['SMA5_ovr_SMA20']=1
    else:
        trade_status_line[symbol]['SMA5_ovr_SMA20']=0

    if indicator_dict['SMA_20']>indicator_dict['SMA_50']:
        trade_status_line[symbol]['SMA20_ovr_SMA50']=1
    else:
        trade_status_line[symbol]['SMA20_ovr_SMA50']=0

    if indicator_dict['SMA_50']>indicator_dict['SMA_180']:
        trade_status_line[symbol]['SMA50_ovr_SMA180']=1
    else:
        trade_status_line[symbol]['SMA50_ovr_SMA180']=0

    if indicator_dict['ratio_M5M20']>=1:
        trade_status_line[symbol]['SMA5_diverge_SMA20']=1
    else:
        trade_status_line[symbol]['SMA5_diverge_SMA20']=0

    if indicator_dict['ratio_M50M180']>=1:
        trade_status_line[symbol]['SMA50_diverge_SMA180']=1
    else:
        trade_status_line[symbol]['SMA50_diverge_SMA180']=0

    if indicator_dict['ratio_M20M50']>=1:
        trade_status_line[symbol]['SMA20_diverge_SMA50']=1
    else:
        trade_status_line[symbol]['SMA20_diverge_SMA50']=0

    if indicator_dict['close']>indicator_dict['SMA_5']:
        trade_status_line[symbol]['CLOSE_ovr_SMA5']=1
    else:
        trade_status_line[symbol]['CLOSE_ovr_SMA5']=0

    send_results_to_file({'Ticker':symbol,'Results':trade_status_line[symbol]},'a')

    print(f'{trade_status_line}\n')

    enthusiasm_score(trade_status_line)


def enthusiasm_score(trade_status_line):
    """Calculating a trade enthusiasm score per the criteria result in the trade_status_line"""
    sum=0
    for key, value in trade_status_line[symbol].items():
        print(key,":",value)

        sum=sum+value

    # Baseline score
    e_score_percent=round(sum/len(trade_status_line[symbol])*100)
    print(f'\n{symbol}---> E-score-->: {sum}---> {e_score_percent} %')


    send_results_to_file({'Ticker':symbol,'Score':{f'{e_score_percent}%'}},'a')

    baseline_scores[symbol]=e_score_percent



def send_results_to_file(data,file_action='a'):

    output_s = pprint.pformat(data)
    with open('long_2_results.txt', file_action) as file:
        file.write(output_s)
        file.write('\n\n')


    

send_results_to_file({'TRADE TRACKER REPORT':'------------>'},'w')
    
send_results_to_file({'* BASELINE SCORES--->':baseline_scores},'a')
    

