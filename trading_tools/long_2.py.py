"""Retrievies requested stocks, calculates current day indicators and generates a trade 'enthusiasm' score based on the traders criteria.""" 

from dependencies import *

def user_inputs():
    """User specifies list of stocks to review and score. User also inputs the date range and the interval of the stock data.
    Inputs are stored in a dictionary."""
    
    my_stocks={
    'Cannibus':['APHA','KSHB','CBWTF','CRON','sndl','cgc','ammj','kern'],
    'Drones':['NVDA','AMBA','AVAV','nkla'],
    'Energy':['PBD','FAN'],
    'Healthcare':['ADMS','cern','kern','cslt','nspr','ontx'],
    'my_positions':['imgn','kern','ammj','apha','sndl','spy'],
    'current_paper_trades':['spy','slp','adxs','plug','fcx','cron','cgc']
    }


    inputs={
        'stock_list':my_stocks['Drones'],
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

    
    df=trade_criteria_dataset(df)

    print(df.head())

    send_results_to_file({'Ticker':symbol,'dataset':df.tail()},'a')


    print(df.loc[CURRENT_DATE])

    indicator_dict=df.loc[CURRENT_DATE].to_dict()

    print(indicator_dict)

    send_results_to_file({'Ticker':symbol,'Results':indicator_dict},'a')

    trade_criteria(indicator_dict)


def trade_criteria_dataset(df):

    # make a dataframe
    df.ta.macd(append=True)
    df.ta.rsi(append=True)
    df.ta.sma(length=5,append=True)
    df.ta.sma(length=50,append=True)
    df.ta.sma(length=180,append=True)

    df['dif_M50M180']=df['SMA_50']-df['SMA_180' ]
    df['ratio_M50M180'] = df['dif_M50M180'].div(df['dif_M50M180'].shift(1))

    df['ratio_MACDh_12_26_9'] = df['MACDh_12_26_9'].div(df['MACDh_12_26_9'].shift(1))

    df.dropna(inplace=True)

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

    if indicator_dict['SMA_5']>indicator_dict['SMA_50']:
        trade_status_line[symbol]['SMA5_ovr_SMA50']=1
    else:
        trade_status_line[symbol]['SMA5_ovr_SMA50']=0

    if indicator_dict['SMA_50']>indicator_dict['SMA_180']:
        trade_status_line[symbol]['SMA50_ovr_SMA180']=1
    else:
        trade_status_line[symbol]['SMA50_ovr_SMA180']=0

    if indicator_dict['ratio_M50M180']>=1:
        trade_status_line[symbol]['SMA50_diverge_SMA180']=1
    else:
        trade_status_line[symbol]['SMA50_diverge_SMA180']=0

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


if __name__ == '__main__':


    global trade_status_line, baseline_scores
    trade_status_line=dict()
    baseline_scores=dict()

    send_results_to_file({'TRADE TRACKER REPORT':'------------>'},'w')

    user_inputs()
    
    send_results_to_file({'* BASELINE SCORES--->':baseline_scores},'a')
    

