"""Dependancies for the trading_tool_2021.py programs""" 
# %%
import pandas as pd
import numpy as np
import os
import sys
import logging

import json

import csv

sys.path.insert(0,"C:\\Users\\dowdj\\OneDrive\\Documents\\GitHub\\my-modules-and-libraries\\program_work_dir")  # Temporary. Used to help finish development of modules.
# import program_work_dir as pwd
from program_work_dir import *

sys.path.insert(0,"C:\\Users\\dowdj\\OneDrive\\Documents\\GitHub\\my-modules-and-libraries\\sqlite_interface")  # Temporary. Used to help finish development of modules.
import sqlite_database_interface as sdb

sys.path.insert(0, "C:\\Users\\dowdj\\OneDrive\\Documents\\GitHub\\my-modules-and-libraries\\gui_maker")
from gui_build import *

sys.path.insert(0, "C:\\Users\\dowdj\\OneDrive\\Documents\\GitHub\\Stock-Data-Analysis\\sda_modules")
from source_stock_data import *



import yfinance as yf
import pandas_datareader as pdr
import pandas_datareader.data as web
import stockstats
from stockstats import StockDataFrame as Sdf
import pandas_ta as ta

from collections import deque

import pprint

import datetime as dt
from datetime import timedelta


# CURRENT_DATE=dt.date.today()
# check_non_BDay=any([dt.date.today().weekday()==5,dt.date.today().weekday()==6])
# if check_non_BDay:
#     if dt.date.today().weekday()==5:
#         CURRENT_DATE=dt.date.today()-timedelta(days=1)
#     elif dt.date.today().weekday()==6:
#         CURRENT_DATE=(dt.date.today()-timedelta(days=2))
# CURRENT_DATE=CURRENT_DATE.strftime("%Y-%m-%d")
# print(CURRENT_DATE)


def the_program_folder(x):
    config_parameters={'database server':{'sqlite_server':'N/A'}}

    client=ClientFolder(x,config_parameters)
    ini_file=f'c:/my_python_programs/{client}/{client}.ini'

    log_file=f'c:/my_python_programs/{client}/{client}_log.log'
    logging.basicConfig(filename=log_file, level=logging.INFO, filemode='w', format=' %(asctime)s -%(levelname)s - %(message)s')
    # logging.info('Start')

    return ini_file,log_file,client


def get_config_values(ini_file,section,option):
    """Used to retrieve values from the program's configuration file."""
    config=configparser.ConfigParser()
    config.read(ini_file)

    return config[section][option]


def exit_operations():
    """Operations to perform prior to the program exit"""
    # remove images from the image folder after each session

    # save the table as a json file in the working directory
    pass



# %%
# %%
