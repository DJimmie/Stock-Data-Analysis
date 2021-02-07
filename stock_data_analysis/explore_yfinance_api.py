"""Exploring the use of the pandas-ta library""" 
# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import calendar
import os
import sys
import logging

import pprint

import pandas_ta as ta

import yfinance as yf
import pandas_datareader as pdr
import pandas_datareader.data as web

from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from scipy import stats

# %%
ticker='APHA'
data = yf.download(tickers=ticker, period='1y', interval='1d')
# %%
print(data.head())
# %%
