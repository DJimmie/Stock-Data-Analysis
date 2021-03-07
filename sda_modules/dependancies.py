"""Various dependacies and constants required to support source_stock_data.py"""

import pandas as pd 
import numpy as np  
import yfinance as yf
import pandas_datareader as pdr
import pandas_datareader.data as web
import sys


sys.path.insert(0,"C:\\Users\\dowdj\\OneDrive\\Documents\\GitHub\\my-modules-and-libraries\\program_work_dir")  # Temporary. Used to help finish development of modules.
# import program_work_dir as pwd
from program_work_dir import *

sys.path.insert(0, "C:\\Users\\dowdj\\OneDrive\\Documents\\GitHub\\my-modules-and-libraries\\gui_maker")
from gui_build import *

import tkcalendar