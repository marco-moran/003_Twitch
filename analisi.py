import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os

def input_data(i):
    if i=="from_site":
        os.environ['KAGGLE_USERNAME'] = k_user
        os.environ['KAGGLE_KEY'] = k_key
        from kaggle.api.kaggle_api_extended import KaggleApi
        api = KaggleApi()
        api.authenticate()
        api.dataset_download_file('aayushmishra1512/twitchdata','twitchdata-update.csv')
        df = pd.read_csv('twitchdata-update.csv')
        return df
    elif i=="local":
        df = pd.read_csv(path_i)
        return df

def analysis(t):
    if t=="summ_d":
        return df.describe()
    elif t=="plot_d":
        fig, ax = plt.subplots(figsize=(18, 12), nrows=3, ncols=3)
        fig.suptitle("Distribution variable", fontsize=16)

        ax[0,0].hist(df.iloc[:,1])
        ax[0,0].set_title(df.columns[1], fontweight='bold')
        ax[0,1].hist(df.iloc[:,2])
        ax[0,1].set_title(df.columns[2], fontweight='bold')
        ax[0,2].hist(df.iloc[:,3])
        ax[0,2].set_title(df.columns[3], fontweight='bold')
        ax[1,0].hist(df.iloc[:,4])
        ax[1,0].set_title(df.columns[4], fontweight='bold')
        ax[1,1].hist(df.iloc[:,5])
        ax[1,1].set_title(df.columns[5], fontweight='bold')
        ax[1,2].hist(df.iloc[:,6])
        ax[1,2].set_title(df.columns[6], fontweight='bold')
        ax[2,0].hist(df.iloc[:,7])
        ax[2,0].set_title(df.columns[7], fontweight='bold')
        ax[2,1].set_visible(False)
        corr = df.corr().round(2)
        sns.heatmap(corr, xticklabels=corr.columns.values, yticklabels=corr.columns.values, vmin=-1, vmax=1, annot=True, ax=ax[2,2])

def data_output(path):
    if type_analysis == 'summ_d':
        if path_o.endswith(".txt"):
            file = open(path_o, 'w')
            file.write(analysis(type_analysis).to_string())
            file.close()
        elif path_o.endswith(".csv"):
            file = open(path_o, 'w')
            file.write(analysis(type_analysis).to_csv())
            file.close()
        elif path_o.endswith(".json"):
            file = open(path_o, 'w')
            file.write(analysis(type_analysis).to_json())
            file.close()
    if type_analysis == 'plot_d':
        analysis(type_analysis)
        plt.savefig(path_o, facecolor='w')

k_user = os.getenv("KAGGLE_USERNAME", '') #user name
k_key = os.getenv("KAGGLE_KEY", '') #key
get_i = os.getenv("GET_INPUT", 'from_site') #path input
path_i = os.getenv("PATH_INPUT", 'twitchdata-update.csv') #path input
type_analysis = os.getenv("ANALYSIS_TYPE", 'plot_d') #tipo di analisi
path_o = os.getenv("PATH_OUTPUT", 'prova.png') #percorso in cui salvare il file

df = input_data(get_i)
data_output(path_o)
