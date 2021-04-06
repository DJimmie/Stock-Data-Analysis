"""K-Means cluster model"""
# %%
from dependancies import *

# %%
def get_data(csv_file):
    """RETRIEVING THE DATA in CSV FORMAT"""
    
    df=pd.read_csv(csv_file)
    
    pd.options.display.precision=2
        
    return df

def scatter(df,a,b):

    x1 = df[a].values
    x2 = df[b].values
    y=df['PL'].values

    plt.scatter(x1, x2, c=y,cmap='rainbow', s=15,label=None)
    plt.xlabel(a)
    plt.ylabel(b)

    plt.legend(('1','0'))

    plt.show()

def features_breakdown(the_data,feature_list,header):
    
    num_unique=the_data[header].nunique()
    for i in feature_list:
        group_by_output=the_data.groupby([(the_data[header])])[i].agg(['min','max','mean','std'])
        print('Output breakdown for %s:' %(i) ,'\n', group_by_output.T,'\n')
        
        if (num_unique==2):
            L0_data=the_data[(the_data[header]==0)]
            L1_data=the_data[(the_data[header]==1)]
            
            no=sns.distplot(L0_data[i],kde=True)
            yes=sns.distplot(L1_data[i],kde=True)
        
        if (num_unique==3):
            L0_data=the_data[(the_data[header]==0)]
            L1_data=the_data[(the_data[header]==1)]
            L2_data=the_data[(the_data[header]==2)]
           
            sns.distplot(L0_data[i],kde=True)
            sns.distplot(L1_data[i],kde=True)
            sns.distplot(L2_data[i],kde=True)
            
            
        if (num_unique==4):
            L0_data=the_data[(the_data[header]==0)]
            L1_data=the_data[(the_data[header]==1)]
            L2_data=the_data[(the_data[header]==2)]
            L3_data=the_data[(the_data[header]==3)]

            sns.distplot(L0_data[i],kde=True)
            sns.distplot(L1_data[i],kde=True)
            sns.distplot(L2_data[i],kde=True)
            sns.distplot(L3_data[i],kde=True)
          

#         plt.figure(figsize=(15,12))
        plt.legend()
        plt.show()



# %%


data_file=r'C:\Users\dowdj\OneDrive\Documents\GitHub\Stock-Data-Analysis\stock_data_analysis\data.csv'

data=get_data(data_file)

feature_list=['obv_pct_delta','ROC_2']
scatter(data,feature_list[0],feature_list[1])

features_breakdown(data,feature_list,'PL')



# %%
