"""TRADE MONITORING & DECISION TOOL"""


from dependencies import *

# Create utility folder and logging file
ini_file,log_file=the_program_folder(os.path.basename(__file__))
logging.info('Start')

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

        symbol_list=['APHA','KSHB','CBWTF','CRON','sndl','cgc','ammj','kern']
        self.symbol=Combos(the_frame=self.options_frame.F,name='Symbol',
        row=1,col=0,drop_down_list=symbol_list,fw=15,sticky=E+W,direction='HORZ')  

        self.strike_price=Entries(the_frame=self.options_frame.F,name='Strike Price',
        row=2,col=0,fw=15,sticky=E+W,direction='HORZ')  

        self.options_price=Entries(the_frame=self.options_frame.F,name='Option Price',
        row=3,col=0,fw=15,sticky=E+W,direction='HORZ') 

        self.num_contracts=Entries(the_frame=self.options_frame.F,name='Contracts',
        row=4,col=0,fw=5,sticky=E+W,direction='HORZ') 

        self.num_contracts.entry.insert(0,1)

        self.expire_date=DateEntry(self.options_frame.F,font='Ariel 12 bold',highlightbackground='pink',highlightthickness=5)
        self.expire_date_label=Label(self.options_frame.F,text='Expiration Date',bg='blue',fg='yellow',font='Ariel 12 bold')
        self.expire_date_label.grid(row=5,column=0,sticky=NW)
        self.expire_date.grid(row=5,column=1,sticky=NW)

        self.break_even_price=Entries(the_frame=self.options_frame.F,name='Break Even Price',
        row=6,col=0,fw=15,sticky=E+W,pady=1,direction='HORZ')

        self.one_hundred_price=Entries(the_frame=self.options_frame.F,name='$100 Profit Mark',
        row=7,col=0,fw=15,sticky=E+W,pady=1,direction='HORZ')

        self.strike_price.entry.bind("<FocusOut>", lambda x:self.options_calcs())
        self.options_price.entry.bind("<FocusOut>", lambda x:self.options_calcs())
        self.num_contracts.entry.bind("<FocusOut>", lambda x:self.options_calcs())

        self.option_submit_option_trade=Buttons(self.options_frame.F,name='Add Option Trade',row=9,col=0,width=20,command=self.options_trade_data,sticky=S,pady=20)

        # self.inspector_select.combo.bind("<<ComboboxSelected>>", lambda x:self.forklift_inspector_id('inspector'))

        ## STOCKS FRAME
        self.stocks_frame=Frames(row=1,col=1,bg='#00FF00',relief='sunken',
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

        self.option_positions=List_box(self.positions_frame.F,name='Option Positions',row=1,col=0,sticky=E+W)
        self.stock_positions=List_box(self.positions_frame.F,name='Stock Positions',row=1,col=1,sticky=E+W)
        
        self.option_positions.list_label['bg']=bg='#00BFFF'
        self.stock_positions.list_label['bg']=bg='#00FF00'
        self.option_positions.list_label['fg']=bg='black'
        self.stock_positions.list_label['fg']=bg='black'
        
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

        option_data=dict()
        ticker=self.symbol.combo.get().upper()
        # option_data[f'{ticker}']={}
        option_data[ticker]={}

        option_data[ticker].update({'strike_price':float(self.strike_price.entry.get())})
        option_data[ticker].update({'option_price':float(self.options_price.entry.get())})
        option_data[ticker].update({'contracts':int(self.num_contracts.entry.get())})
        option_data[ticker].update({'expiration':self.expire_date.get()})
        option_data[ticker].update({'bep':float(self.break_even_price.entry.get())})
        option_data[ticker].update({'$100_profit':float(self.one_hundred_price.entry.get())})

        print(ticker)
        print(option_data)

        self.option_data=option_data

        self.positions_list()

    def positions_list(self):

        print(self.option_data.keys())



class options_trade():
    pass

class stock_trade():
    pass



class TradeProgressWin():
    """Experimental---> testing use of toplevel to house the trade progress info"""

    def __init__(self,data):
        self.data=data
        self.top = Toplevel(
            bg='blue',
            bd=5,
            width=200,
            height=200)

        self.top.title(f'OPTIONS CONTRACT-----> {self.data["symbol"].upper()}') 

        self.build_gui()

        self.top.mainloop()

    def build_gui(self):
        FONT_SIZE=16
        self.ticker=Label(
            master=self.top,
            text=self.data["symbol"],
            bg='black',
            fg='white',
            font='Ariel 16 bold')
        self.ticker.grid(row=0,column=0,columnspan=5)

        # Form Labels
        width=15
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
            bg='yellow',
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
            bg='yellow',
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
            bg='yellow',
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
            bg='yellow',
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
            bg='#FF33FF',
            fg='black',
            font=f'Ariel {FONT_SIZE} bold',
            width=width,bd=5)
        self.bep.grid(row=6,column=1)

        # DATA FIELDS   


    


UserInterface()