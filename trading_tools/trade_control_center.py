"""TRADE MONITORING & DECISION TOOL"""


from dependencies import *
import trade_scoring

# Create utility folder and logging file
ini_file,log_file,client=the_program_folder(os.path.basename(__file__))
logging.info('Start')


options_json_file=f'c:/my_python_programs/{client}/options.json'

stocks_json_file=f'c:/my_python_programs/{client}/stocks.json'

# a=WorkDirectory(client_sub_folder='options_trading',client_folder=client)
# b=WorkDirectory(client_sub_folder='stock_trading',client_folder=client)

header=['ticker','strike_price','option_price','contracts','purchase_date','expiration','bep','$100_profit','position','id']
if not os.path.isfile(options_json_file):
    options_data_dict=dict()
    # header=['ticker','strike_price','option_price','contracts','purchase_date','expiration','bep','$100_profit','position','id']
    for i in header:
        options_data_dict[i]=list()
    with open(options_json_file,'w') as f: 
        json.dump(options_data_dict, f, indent=4) 

if not os.path.isfile(stocks_json_file):
    stocks_data_dict=dict()
    with open(stocks_json_file,'w') as f: 
        json.dump(stocks_data_dict, f, indent=4) 

a=get_config_values(ini_file=ini_file,section='database server',option='sqlite_server')



class UserInterface():
    """Parent class for the UI. Instantiates the composite Window.
    User Interface with fields for entering data to the database."""

    logging.info('UserInterface()')

    def __init__(self):
        """Interface build."""
        UI(None,title='MY TRADING TOOL',
        banner='MY TRADING TOOL',
        win_color='#6334D0',
        fg='yellow',
        window_height=500)

        ControlCenter()

        mainloop()


class ControlCenter():
    """Build the GUI and implement it's methods"""
    logging.info('ControlCenter()')

    def __init__(self):
        self.build_the_gui()

    def build_the_gui(self):
        """Build GUI frames and widgets"""
        
         ## OPTIONS FRAME
        self.options_frame=Frames(row=1,col=0,bg='#00BFFF',relief='raised',
        banner_font='Ariel 16 bold',
        banner_text='OPTION TRADES',
        fg='black',
        sticky=NW)

        symbol_list=self.load_json_file('options')['ticker']
        self.symbol=Combos(the_frame=self.options_frame.F,name='Symbol',
        row=1,col=0,drop_down_list=symbol_list,fw=15,sticky=E+W,direction='HORZ')  

        self.strike_price=Entries(the_frame=self.options_frame.F,name='Strike Price',
        row=2,col=0,fw=15,sticky=E+W,direction='HORZ')  

        self.options_price=Entries(the_frame=self.options_frame.F,name='Option Price',
        row=3,col=0,fw=15,sticky=E+W,direction='HORZ') 

        self.num_contracts=Entries(the_frame=self.options_frame.F,name='Contracts',
        row=4,col=0,fw=5,sticky=E+W,direction='HORZ') 

        self.num_contracts.entry.insert(0,1)

        self.entry_date=DateEntry(self.options_frame.F,font='Ariel 12 bold',highlightbackground='pink',highlightthickness=5)
        self.entry_date_label=Label(self.options_frame.F,text='Options Purchase Date',bg='blue',fg='yellow',font='Ariel 12 bold')
        self.entry_date_label.grid(row=5,column=0,sticky=NW)
        self.entry_date.grid(row=5,column=1,sticky=NW)

        self.expire_date=DateEntry(self.options_frame.F,font='Ariel 12 bold',highlightbackground='pink',highlightthickness=5)
        self.expire_date_label=Label(self.options_frame.F,text='Expiration Date',bg='blue',fg='yellow',font='Ariel 12 bold')
        self.expire_date_label.grid(row=6,column=0,sticky=NW,pady=8)
        self.expire_date.grid(row=6,column=1,sticky=NW,pady=8)

        self.break_even_price=Entries(the_frame=self.options_frame.F,name='Break Even Price',
        row=7,col=0,fw=15,sticky=E+W,pady=1,direction='HORZ')

        self.one_hundred_price=Entries(the_frame=self.options_frame.F,name='$100 Profit Mark',
        row=8,col=0,fw=15,sticky=E+W,pady=1,direction='HORZ')

        self.strike_price.entry.bind("<FocusOut>", lambda x:self.options_calcs())
        self.options_price.entry.bind("<FocusOut>", lambda x:self.options_calcs())
        self.num_contracts.entry.bind("<FocusOut>", lambda x:self.options_calcs())

        self.option_submit_option_trade=Buttons(self.options_frame.F,name='Add Option Trade',row=9,col=0,width=20,command=self.options_trade_data,sticky=S,pady=20)

        # self.inspector_select.combo.bind("<<ComboboxSelected>>", lambda x:self.forklift_inspector_id('inspector'))

        

        ## STOCKS FRAME
        self.stocks_frame=Frames(row=1,col=1,bg='#808000',relief='sunken',
        banner_font='Ariel 16 bold',
        banner_text='STOCK TRADES',
        fg='black',
        sticky=NW)

        self.stock_ticker=Combos(the_frame=self.stocks_frame.F,name='Symbol',
        row=1,col=0,drop_down_list=None,fw=15,sticky=E+W,direction='HORZ')  

        self.share_price=Entries(the_frame=self.stocks_frame.F,name='Share Price',
        row=2,col=0,fw=15,sticky=E+W,direction='HORZ')

        self.num_shares=Entries(the_frame=self.stocks_frame.F,name='Number of Shares',
        row=3,col=0,fw=15,sticky=E+W,direction='HORZ')

        self.num_shares.entry.insert(0,100)

        self.total_cost=Entries(the_frame=self.stocks_frame.F,name='Total Cost',
        row=4,col=0,fw=15,sticky=E+W,direction='HORZ')

        self.stock_trade_date=DateEntry(self.stocks_frame.F,font='Ariel 12 bold',highlightbackground='pink',highlightthickness=5)
        self.stock_trade_date_label=Label(self.stocks_frame.F,text='Entry Date',bg='blue',fg='yellow',font='Ariel 12 bold')
        self.stock_trade_date_label.grid(row=5,column=0,sticky=NW)
        self.stock_trade_date.grid(row=5,column=1,sticky=NW)

        self.share_price.entry.bind("<FocusOut>", lambda x:self.stock_calcs())
        self.num_shares.entry.bind("<FocusOut>", lambda x:self.stock_calcs())

        self.stock_submit_option_trade=Buttons(self.stocks_frame.F,name='Add Stock Trade',row=6,col=0,width=20,command=None,sticky=S,pady=20)

        ## POSITIONS FRAME
        self.positions_frame=Frames(row=1,col=2,bg='#D2691E',relief='raised',
        banner_font='Ariel 16 bold',
        banner_text='POSITIONS',
        fg='white',
        sticky=NW)

        self.option_positions=List_box(self.positions_frame.F,name='Option Positions',row=1,col=0,sticky=E+W,fw=30,height=20)
        self.stock_positions=List_box(self.positions_frame.F,name='Stock Positions',row=1,col=1,sticky=E+W,fw=30,height=20)
        
        self.option_positions.list_label['bg']=bg='#00BFFF'
        self.stock_positions.list_label['bg']=bg='#00FF00'
        self.option_positions.list_label['fg']=bg='black'
        self.stock_positions.list_label['fg']=bg='black'

        self.option_positions.list_box.bind("<Double-Button-1>",lambda x: TradeProgressWin(tradeType='options',id=self.option_positions.list_box.get(ANCHOR)))
        self.populate_positions('options')

        ## STOCK WATCH FRAME

        self.stock_watch_frame=Frames(row=1,col=3,bg='#D2691E',relief='sunken',
        banner_font='Ariel 16 bold',
        banner_text='STOCK WATCH',
        fg='white',
        sticky=NW)

        stock_list=['APHA','KSHB','CBWTF','CRON','sndl','cgc','ammj','kern']
        self.swTicker=Combos(the_frame=self.stock_watch_frame.F,name='Symbol',
        row=1,col=0,drop_down_list=stock_list,fw=15,sticky=E+W,direction='HORZ') 

        self.swTicker.combo.bind("<Return>", lambda x: StockCheck(self.swTicker.combo.get()))
        self.swTicker.combo.bind("<<ComboboxSelected>>",lambda x: StockCheck(self.swTicker.combo.get()))
 
   
    def stock_calcs(self):

        a=float(self.share_price.entry.get())
        b=int(self.num_shares.entry.get())
        c=round(a*b,2)
        self.total_cost.entry.delete(0,'end')
        self.total_cost.entry.insert(0,c)

    def options_calcs(self):

        a=float(self.strike_price.entry.get())
        b=float(self.options_price.entry.get())
        c=round(a+b,2)
        d=c+1.00
        self.break_even_price.entry.delete(0,'end')
        self.break_even_price.entry.insert(0,c)
        self.one_hundred_price.entry.delete(0,'end')
        self.one_hundred_price.entry.insert(0,d)


    def options_trade_data(self):
        """Retrieves the option traded data from the GUI and adds it to the option_data dictionary."""

        header=['ticker','strike_price','option_price','contracts','purchase_date','expiration','bep','$100_profit','position','id']
        if not os.path.isfile(options_json_file):
            options_data_dict=dict()
            for i in header:
                options_data_dict[i]=list()
            with open(options_json_file,'w') as f: 
                json.dump(options_data_dict, f, indent=4) 

        option_data=dict()
        ticker=self.symbol.combo.get().upper()
        option_data[ticker]={}

        option_data[ticker].update({'strike_price':float(self.strike_price.entry.get())})
        option_data[ticker].update({'option_price':float(self.options_price.entry.get())})
        option_data[ticker].update({'contracts':int(self.num_contracts.entry.get())})
        option_data[ticker].update({'purchase_date':self.entry_date.get()})
        option_data[ticker].update({'expiration':self.expire_date.get()})
        option_data[ticker].update({'bep':float(self.break_even_price.entry.get())})
        option_data[ticker].update({'$100_profit':float(self.one_hundred_price.entry.get())})
        option_data[ticker].update({'position':'Open'})

        option_id=self.build_trade_id('options',option_data)
        option_data[ticker].update({'id':option_id})

        print(ticker)
        print(option_data)

        self.option_data=option_data

        a=self.load_json_file('options')

        print(a)
        print(type(a['ticker']))

        for i in header:
            if i=='ticker':
                a[i].append(ticker)
                a.update({'ticker':a[i]})
                continue
            a[i].append(option_data[ticker][i])
            a.update({i:a[i]})
            print(a)

        
        self.dump_to_json_file('options',a)

        self.populate_positions('options')


    @staticmethod
    def build_trade_id(a,data):
        if a=='options':
            key, val = next(iter(data.items()))
            t=key
            sp=str(val['strike_price'])
            ed=val['expiration']
            space=' '
            seq=(key,'$'+sp,ed,'CALL 100')

            option_id=space.join(seq)

            print(option_id)

            return option_id

        elif (a=='stocks'):
            b=stocks_json_file

    @staticmethod
    def load_json_file(a):
        if a=='options':
            b=options_json_file
        elif (a=='stocks'):
            b=stocks_json_file

        with open(b, "r") as read_file:
            data = json.load(read_file)

        return data

    @staticmethod
    def dump_to_json_file(a,data):
        if a=='options':
            b=options_json_file
        elif (a=='stocks'):
            b=stocks_json_file

        with open(b, "w") as write_file:
            json.dump(data, write_file)

    def populate_positions(self,a):
        data=self.load_json_file(a)
        index_list=[]
        for c,i in enumerate(data['position']):
            if i=='Open':
                index_list.append(c)

        print(index_list)

        open_positions=[data['id'][x] for x in index_list]
        print(open_positions)

        self.option_positions.list_box.delete(0,END)
        for c,k in enumerate(open_positions):
            self.option_positions.list_box.insert(c,k)

        # TradeProgressWin(data)




class TradeProgressWin():
    """Experimental---> testing use of toplevel to house the trade progress info"""

    def __init__(self,tradeType,id):
        self.tradeType=tradeType
        self.id=id
        self.data=ControlCenter.load_json_file(self.tradeType) ##--->pulling the json file
        self.top = Toplevel(
            bg='blue',
            bd=5,
            width=200,
            height=200)

        # self.top.title(f'OPTIONS CONTRACT-----> {self.data["ticker"][0].upper()}') 

        self.extracted_data=self.extract_trade_data()
        self.build_gui()

        trade_scoring.user_inputs(tradeType='options',ticker=self.extracted_data['ticker'])

        self.last_stock_price=trade_scoring.last_Close
       
        self.score_data=trade_scoring.trade_status_line[self.extracted_data['ticker']]
        print(self.score_data)

        self.populate_the_gui()


        self.top.mainloop()

    def extract_trade_data(self):
        """extracting instance of trade data from the json file"""

        # search data['id'] for the provided id value and get the list index
        for i in self.data['id']:
            if i==self.id:
                index=self.data['id'].index(i)
        
        print(self.data)
        print(index)

        # using the list index, pull all values from the other key-value(list) pairs corresponding to the provided id. # place the retrieve valuse in a dict and return
        d=dict()
        for i in header:
            d[i]=self.data[i][index]

        print(d)

        return d



    def build_gui(self):
        FONT_SIZE=16
        self.ticker=Label(
            master=self.top,
            text='TBD',
            bg='black',
            fg='white',
            font='Ariel 16 bold')
        self.ticker.grid(row=0,column=0,columnspan=5)

        # Form Labels
        width=18
        bg_entry='#F5F5F5'
        self.stock_price_label=Label(
            master=self.top,
            text='Stock Price',
            bg='white',
            fg='black',
            font=f'Ariel {FONT_SIZE} bold',
            width=width)
        self.stock_price_label.grid(row=1,column=0)

        self.stock_price=Entry(
            master=self.top,
            bg=bg_entry,
            fg='black',
            font=f'Ariel {FONT_SIZE} bold',
            width=width,bd=5)
        self.stock_price.grid(row=1,column=1)

        self.strike_price_label=Label(
            master=self.top,
            text='Strike Price',
            bg='white',
            fg='black',
            font=f'Ariel {FONT_SIZE} bold',
            width=width)
        self.strike_price_label.grid(row=2,column=0,columnspan=1)

        self.strike_price=Entry(
            master=self.top,
            bg=bg_entry,
            fg='black',
            font=f'Ariel {FONT_SIZE} bold',
            width=width,bd=5)
        self.strike_price.grid(row=2,column=1)

        self.num_contracts_label=Label(
            master=self.top,
            text='Contracts',
            bg='white',
            fg='black',
            font=f'Ariel {FONT_SIZE} bold',
            width=width)
        self.num_contracts_label.grid(row=3,column=0,columnspan=1)


        self.num_contracts=Entry(
            master=self.top,
            bg=bg_entry,
            fg='black',
            font=f'Ariel {FONT_SIZE} bold',
            width=width,bd=5)
        self.num_contracts.grid(row=3,column=1)


        self.option_price_label=Label(
            master=self.top,
            text='Option Price',
            bg='white',
            fg='black',
            font=f'Ariel {FONT_SIZE} bold',
            width=width)
        self.option_price_label.grid(row=4,column=0,columnspan=1)


        self.option_price=Entry(
            master=self.top,
            bg=bg_entry,
            fg='black',
            font=f'Ariel {FONT_SIZE} bold',
            width=width,bd=5)
        self.option_price.grid(row=4,column=1)

        self.last_price_label=Label(
            master=self.top,
            text='Last Price',
            bg='white',
            fg='black',
            font=f'Ariel {FONT_SIZE} bold',
            width=width)
        self.last_price_label.grid(row=5,column=0,columnspan=1)

        self.last_price=Entry(
            master=self.top,
            bg=bg_entry,
            fg='black',
            font=f'Ariel {FONT_SIZE} bold',
            width=width,bd=5)
        self.last_price.grid(row=5,column=1)

        self.bep_label=Label(
            master=self.top,
            text='Break-Even Point',
            bg='white',
            fg='black',
            font=f'Ariel {FONT_SIZE} bold',
            width=width)
        self.bep_label.grid(row=6,column=0,columnspan=1)

        self.bep=Entry(
            master=self.top,
            bg='#FF0000',
            fg='black',
            font=f'Ariel {FONT_SIZE} bold',
            width=width,bd=5)
        self.bep.grid(row=6,column=1)

        self.one_hundred_profit_label=Label(
            master=self.top,
            text='$100 Profit Milestone',
            bg='white',
            fg='black',
            font=f'Ariel {FONT_SIZE} bold',
            width=width)
        self.one_hundred_profit_label.grid(row=7,column=0,columnspan=1)

        self.one_hundred_profit=Entry(
            master=self.top,
            bg=bg_entry,
            fg='black',
            font=f'Ariel {FONT_SIZE} bold',
            width=width,bd=5)
        self.one_hundred_profit.grid(row=7,column=1)

        self.entry_date_label=Label(
            master=self.top,
            text='Entry Date',
            bg='white',
            fg='black',
            font=f'Ariel {FONT_SIZE} bold',
            width=width)
        self.entry_date_label.grid(row=8,column=0,columnspan=1)

        self.entry_date=Entry(
            master=self.top,
            bg=bg_entry,
            fg='black',
            font=f'Ariel {FONT_SIZE} bold',
            width=width,bd=5)
        self.entry_date.grid(row=8,column=1)

        self.expiration_date_label=Label(
            master=self.top,
            text='Expiration Date',
            bg='white',
            fg='black',
            font=f'Ariel {FONT_SIZE} bold',
            width=width)
        self.expiration_date_label.grid(row=9,column=0,columnspan=1)

        self.expiration_date=Entry(
            master=self.top,
            bg=bg_entry,
            fg='black',
            font=f'Ariel {FONT_SIZE} bold',
            width=width,bd=5)
        self.expiration_date.grid(row=9,column=1)

        # DATA FIELDS   

    
    def populate_the_gui(self):
        
        self.ticker['text']=self.extracted_data['id']
        self.stock_price.insert(0,round(self.last_stock_price,2))
        self.strike_price.insert(0,self.extracted_data['strike_price'])
        self.option_price.insert(0,self.extracted_data['option_price'])
        self.num_contracts.insert(0,self.extracted_data['contracts'])
        self.entry_date.insert(0,self.extracted_data['purchase_date'])
        self.expiration_date.insert(0,self.extracted_data['expiration'])
        self.bep.insert(0,self.extracted_data['bep'])
        self.one_hundred_profit.insert(0,self.extracted_data['$100_profit'])

        # 
        if self.last_stock_price>self.extracted_data['bep']:
            self.bep['bg']='#7CFC00'

        if self.last_stock_price>self.extracted_data['$100_profit']:
            self.one_hundred_profit['bg']='#7CFC00'


        if self.last_stock_price>self.extracted_data['strike_price']:
            self.strike_price['bg']='#7CFC00' 
        elif self.last_stock_price<self.extracted_data['strike_price'] :
            self.strike_price['bg']='#FF0000'



        self.score()

    def score(self):

        self.score_frame=Frames(row=10,col=0,host=self.top,bg='#808000',relief='sunken',
        banner_font='Ariel 16 bold',
        banner_text='TRADE SCORE',
        fg='black',
        pady=20,
        sticky=NW)

        criteria_labels=[x for x in self.score_data.keys()]
        criteria_values=[x for x in self.score_data.values()]
        trade_score=sum(criteria_values)/len(criteria_values)

        for c,i in enumerate(criteria_labels,1):
            if criteria_values[c-1]==1:
                bg='#7CFC00'
            elif criteria_values[c-1]==0:
                bg='#FF0000'
                
            self.labels=Label(master=self.score_frame.F,text=i,font='Ariel 12 bold',bg=bg)
            self.labels.grid(row=c,column=0,sticky=NW)

        if trade_score<=.50:
            bg='#FF0000'
            fg='black'
        elif trade_score>=.80:
            bg='#7CFC00'
            fg='black'
        else:
            bg='yellow'
            fg='#FF0000'

        trade_score=round(trade_score*100,2)

        self.trade_score_label=Label(master=self.score_frame.F,text=f'{trade_score}%',font='Ariel 12 bold',bg=bg,fg=fg)
        self.trade_score_label.grid(row=0,column=1,sticky=NW)



class StockCheck():
    """Retrieve trade score for selected stock"""
    def __init__(self,ticker):
        self.tradeType='stocks'
        self.ticker=ticker.upper()
        
        self.top = Toplevel(
            bg='grey',
            bd=5,
            width=200,
            height=200)

        self.build_gui()

        trade_scoring.user_inputs(tradeType=self.tradeType,ticker=self.ticker)

        self.last_stock_price=trade_scoring.last_Close
       
        self.score_data=trade_scoring.trade_status_line[self.ticker]
        print(self.score_data)

        self.score()

    def build_gui(self):
        FONT_SIZE=16
        self.ticker_label=Label(
            master=self.top,
            text=self.ticker,
            bg='black',
            fg='white',
            font='Ariel 16 bold')
        self.ticker_label.grid(row=0,column=0,columnspan=2)

        # Form Labels
        width=18
        self.stock_price_label=Label(
            master=self.top,
            text='Stock Price',
            bg='white',
            fg='black',
            font=f'Ariel {FONT_SIZE} bold',
            width=width)
        self.stock_price_label.grid(row=1,column=0)

        self.stock_price=Entry(
            master=self.top,
            bg='yellow',
            fg='black',
            font=f'Ariel {FONT_SIZE} bold',
            width=width,bd=5)
        self.stock_price.grid(row=1,column=1)

    def score(self):

        self.score_frame=Frames(row=2,col=0,host=self.top,bg='#808000',relief='sunken',
        banner_font='Ariel 16 bold',
        banner_text='EVALUATION SCORE',
        fg='white',
        pady=20,
        sticky=NW)

        self.stock_price.insert(0,round(self.last_stock_price,2))
        criteria_labels=[x for x in self.score_data.keys()]
        criteria_values=[x for x in self.score_data.values()]
        trade_score=sum(criteria_values)/len(criteria_values)

        for c,i in enumerate(criteria_labels,1):
            if criteria_values[c-1]==1:
                bg='#7CFC00'
            elif criteria_values[c-1]==0:
                bg='#FF0000'
                
            self.labels=Label(master=self.score_frame.F,text=i,font='Ariel 12 bold',bg=bg)
            self.labels.grid(row=c,column=0,sticky=NW)

        if trade_score<=.50:
            bg='#FF0000'
            fg='black'
        elif trade_score>=.80:
            bg='#7CFC00'
            fg='black'
        else:
            bg='yellow'
            fg='#FF0000'

        trade_score=round(trade_score*100,2)

        self.trade_score_label=Label(master=self.score_frame.F,text=f'{trade_score}%',font='Ariel 12 bold',bg=bg,fg=fg)
        self.trade_score_label.grid(row=0,column=1,sticky=NW)








UserInterface()