import os
import csv
#------------------------------------------------------------
def make_directories():
    path=(r'C:\Users\Sharyn\Desktop\Datasets\sandp500')
    os.mkdir(path+'\SP500_list')


def make_list():
    location=r'C:\Users\Sharyn\Desktop\Datasets\sandp500'
    read_from_here='\individual_stocks_5yr'
    put_in_here='\SP500_list'
    file_name='\All_SP500.csv'
    
    print(location+read_from_here)
    print(location+put_in_here)
    
    for i in os.listdir(location+read_from_here):
        print (i)
        ticker=i.split('_')
        print(ticker[0])
        with open(location+put_in_here+file_name,'a',newline='') as ticks:
            daywriter=csv.writer(ticks)
            daywriter.writerow([ticker[0]])
        ticks.close




    
#---------------------------------------------------------

#make_directories()
make_list()
