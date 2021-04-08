"""K-Means cluster model"""
# %%
from dependancies import *
from sklearn.cluster import KMeans

# %%
def get_data(csv_file):
    """RETRIEVING THE DATA in CSV FORMAT"""
    
    df=pd.read_csv(csv_file)
    
    pd.options.display.precision=2
        
    return df

def scatter(df,a,b):
    global x1,x2

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
            
            no=sns.distplot(L0_data[i],kde=True,label='0')
            yes=sns.distplot(L1_data[i],kde=True,label='1')
        
        if (num_unique==3):
            L0_data=the_data[(the_data[header]==0)]
            L1_data=the_data[(the_data[header]==1)]
            L2_data=the_data[(the_data[header]==2)]
           
            sns.distplot(L0_data[i],kde=True,label='0')
            sns.distplot(L1_data[i],kde=True,label='1')
            sns.distplot(L2_data[i],kde=True,label='2')
            
            
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

def clustering(data,features):

    X=data[features].values

    print(X[0:5])

    kmeans = KMeans(n_clusters=3, random_state=0).fit(X)

    kmeans_results=kmeans.labels_
    
    print(kmeans_results)

    the_centroids=kmeans.cluster_centers_

    print(f'Centroids--->\n{the_centroids}')

    plt.scatter(the_centroids[:,0],the_centroids[:,1],marker='o',s=60,c='black')

    for i in range(0,len(kmeans_results)):
        if (kmeans_results[i]==0):
            plt.scatter(x1[i],x2[i],marker='D',color='purple',s=30)
    #         print (x1[i])
        if (kmeans_results[i]==1):
            plt.scatter(x1[i],x2[i],marker='+',color='green',s=30)
    #         print (x1[i])
        if (kmeans_results[i]==2):
            plt.scatter(x1[i],x2[i],marker='*',color='blue',s=30)
    #         print (x1[i])
        if (kmeans_results[i]==3):
            plt.scatter(x1[i],x2[i],marker='*',color='red',s=30)
    #         print (x1[i])           


    data['clusters']=kmeans_results

    print(data.head())

    print(data.groupby([data['PL'],data['clusters']])['RSI_14'].count())


    plt.show()

    return data



# %%


data_file=r'C:\Users\dowdj\OneDrive\Documents\GitHub\Stock-Data-Analysis\stock_data_analysis\data.csv'

data=get_data(data_file)

feature_list=['RSI_14','ROC_2']
scatter(data,feature_list[0],feature_list[1])

features_breakdown(data,feature_list,'PL')

data=clustering(data,feature_list)

features_breakdown(data,feature_list,'clusters')

features_breakdown(data,['clusters'],'PL')





# %%
