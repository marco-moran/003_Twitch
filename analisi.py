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
    else:
        raise ValueError("input not supported (supported input: from_site, local)")

def analysis(t):
    if t=="summ_d":
        return df.describe()
    elif t=="summ_i":
        a = df_datatypes.rename(columns={0:'DType'})
        b = df_null_count.to_frame().rename(columns={0:'Non-Null Count'})
        df = b.merge(a, left_index=True, right_index=True).reset_index().rename(columns={'index':'Column'})
        return df
    elif t=="summ_p":
        df_pivot = pd.pivot_table(df, values=['Average viewers', 'Followers','Stream time(minutes)'],
                                 index = 'Language',
                                 columns = 'Partnered', aggfunc=np.mean, fill_value=0)
        df_pivot = df_pivot.reindex(df_pivot['Average viewers'].sort_values(by=True, ascending=False).index)
        return df_pivot
    elif t=="plot_d":
        df.select_dtypes(include='number').hist(figsize=(22,9), bins=12)
    elif t=="plot_c":
        corr = df.corr().round(2)
        sns.heatmap(corr, xticklabels=corr.columns.values, yticklabels=corr.columns.values, vmin=-1, vmax=1, annot=True)
    else:
        raise ValueError("Analysis not supported (supported analysis: summ_d, summ_i, summ_p, plot_d, plot_c)")

def data_output(path):
    if type_analysis == 'summ_d' or type_analysis == 'summ_i' or type_analysis == 'summ_p':
        if path_o.endswith(".txt"):
            file = open(path_o, 'w')
            file.write(analysis(type_analysis).to_string())
            file.close()
        elif path_o.endswith(".csv"):
            file = open(path_o, 'w', newline='')
            file.write(analysis(type_analysis).to_csv())
            file.close()
        elif path_o.endswith(".json"):
            file = open(path_o, 'w')
            file.write(analysis(type_analysis).to_json())
            file.close()
        else:
            raise ValueError("Format not supported (supported formats: txt, csv, json)")
    if type_analysis == 'plot_d' or type_analysis == 'plot_c':
        analysis(type_analysis)
        plt.savefig(path_o, facecolor='w', bbox_inches='tight')

k_user = os.getenv("KAGGLE_USERNAME", '') #user name
k_key = os.getenv("KAGGLE_KEY", '') #key
get_i = os.getenv("GET_INPUT", 'local') #path input
path_i = os.getenv("PATH_INPUT", 'twitchdata-update.csv') #path input
type_analysis = os.getenv("ANALYSIS_TYPE", 'plot_d') #tipo di analisi
path_o = os.getenv("PATH_OUTPUT", 'prova.png') #percorso in cui salvare il file

df = input_data(get_i)
data_output(path_o)
