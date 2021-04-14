"""K-Means cluster model"""
# %%
from dependancies import *
from sklearn.cluster import KMeans

# %%
def get_data(csv_file,normalize_data=False):
    """RETRIEVING THE DATA in CSV FORMAT"""
    
    df=pd.read_csv(csv_file)

    df=remove_outliers(df)

    if normalize_data==True:
        df=standardize_data(df)
    
    pd.options.display.precision=2
        
    return df


def remove_outliers(df):
    
    # z-score method
    df = df[(np.abs(stats.zscore(df)) < 3).all(axis=1)]
    return df


def standardize_data(df,scale_to_range=True):
    
    if scale_to_range:
        df_standardized=(df-df.min())/(df.max()-df.min())
    else:
        df_standardized=(df-df.mean())/df.std()
        

    return df_standardized


def scatter(df,a,b):
    global x1,x2

    x1 = df[a].values
    x2 = df[b].values
    y=df['PL'].values

    x1_0 = df[a][(df['PL']==0)]
    x1_1 = df[a][(df['PL']==1)]
    x2_0 = df[b][(df['PL']==0)]
    x2_1 = df[b][(df['PL']==1)]
    y=df['PL'].values

    plt.scatter(x1_0, x2_0, c='red',cmap='rainbow', s=15,label='0')
    plt.scatter(x1_1, x2_1, c='green',cmap='rainbow', s=15,label='1')

    # p=plt.scatter(x1, x2, c=y, s=15,cmap='seismic')
    
    # groups = df.groupby('PL')
    # for name, group in groups:
    #     plt.plot(group.x, group.y, marker='o', linestyle='', markersize=12, label=name)

    plt.xlabel(a)
    plt.ylabel(b)

    plt.legend()

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

            sns.distplot(L0_data[i],kde=True,label='0')
            sns.distplot(L1_data[i],kde=True,label='1')
            sns.distplot(L2_data[i],kde=True,label='2')
            sns.distplot(L3_data[i],kde=True,label='3')


        if (num_unique==5):
            L0_data=the_data[(the_data[header]==0)]
            L1_data=the_data[(the_data[header]==1)]
            L2_data=the_data[(the_data[header]==2)]
            L3_data=the_data[(the_data[header]==3)]
            L4_data=the_data[(the_data[header]==4)]

            sns.distplot(L0_data[i],kde=True,label='0')
            sns.distplot(L1_data[i],kde=True,label='1')
            sns.distplot(L2_data[i],kde=True,label='2')
            sns.distplot(L3_data[i],kde=True,label='3')
            sns.distplot(L4_data[i],kde=True,label='4')
          

#         plt.figure(figsize=(15,12))
        plt.legend()
        plt.show()

def boxplots(df,feature_list):
    data=[]
    fig, ax = plt.subplots(nrows=len(feature_list),ncols=1,sharex=False,figsize=(10, 6))
    
    for c,i in enumerate(feature_list,0):
        
        x0 = df[i][(df['PL']==0)]
        data.append(x0)
        x1 = df[i][(df['PL']==1)]
        data.append(x1)

        ax[c].set_title(f'{feature_list[c]}',fontsize= 15)
        ax[c].boxplot(data)
        ax[c].set_xticklabels(['PL=0','PL=1'])

        data.clear()
    

    plt.show()


def clustering(data,features):

    X=data[features].values

    print(X[0:5])

    kmeans = KMeans(n_clusters=4, random_state=0).fit(X)

    kmeans_results=kmeans.labels_
    
    print(kmeans_results)

    the_centroids=kmeans.cluster_centers_

    print(f'Centroids--->\n{the_centroids}')
    print(f'kmeans labels--->{kmeans.labels_[:5]}')

    if length_of_feature_list==2:
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

    # print(data.groupby([data['PL'],data['clusters']])['RSI_14'].count())


    plt.show()

    return data,kmeans


def load_json_file():
    
    d=r'C:\Users\dowdj\OneDrive\Documents\GitHub\Stock-Data-Analysis\stock_data_analysis\model_input.json'
    with open(d, "r") as read_file:
        data = json.load(read_file)

    return data

def the_model(kmeans_results,feature_list):

    # get the data
    data_dict=load_json_file()

    model_inputs=[data_dict[i] for i in feature_list]

    print(model_inputs)

    # feed data to model and get cluster

    results=kmeans_results.predict([model_inputs])

    return results







# %%


data_file=r'C:\Users\dowdj\OneDrive\Documents\GitHub\Stock-Data-Analysis\stock_data_analysis\data.csv'

data=get_data(data_file,normalize_data=False)

# feature_list=['RSI_14','M_ovr_S','Z_30','PSL_3','ROC_2']
feature_list=['RSI_14','ROC_2']
# feature_list=['RSI_14','Z_30','ROC_2','M_ovr_S','obv_pct_delta','ratio_MACDh_12_26_9']
# feature_list=['RSI_14','ratio_M5M20','ratio_MACDh_12_26_9','PSL_3','M_ovr_S']
length_of_feature_list=len(feature_list)

if length_of_feature_list==2:
    scatter(data,feature_list[0],feature_list[1])

features_breakdown(data,feature_list,'PL')

boxplots(data,feature_list)

data,kmeans_results=clustering(data,feature_list)

features_breakdown(data,feature_list,'clusters')

features_breakdown(data,['clusters'],'PL')

assigned_cluster=the_model(kmeans_results,feature_list)

print(assigned_cluster)





# %%
