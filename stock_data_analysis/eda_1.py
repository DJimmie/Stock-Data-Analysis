
import numpy as np
import pandas as pd
from pandas_profiling import ProfileReport

the_file='data.csv'

df =pd.read_csv(the_file)

profile = ProfileReport(df, 
title="Pandas Profiling Report", 
minimal=False, 
explorative=False, 
sensitive=False, 
dark_mode=False, 
orange_mode=False, 
sample=None)

profile.to_file("your_report.html")