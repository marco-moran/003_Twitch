# librerie utilizzate
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os


# scelta della provenienza dell'input
def data_input(i):
    if i == "from_site":
        os.environ['KAGGLE_USERNAME'] = k_user
        os.environ['KAGGLE_KEY'] = k_key
        from kaggle.api.kaggle_api_extended import KaggleApi
        api = KaggleApi()
        api.authenticate()
        api.dataset_download_file('aayushmishra1512/twitchdata', 'twitchdata-update.csv')
        datafrane = pd.read_csv('twitchdata-update.csv')
        return datafrane
    elif i == "local":
        datafrane = pd.read_csv(path_i)
        return datafrane
    else:
        raise ValueError("input not supported (supported input: from_site, local)")


# scelta dell'analisi da effettuare sul dataset
def analysis(a, dataframe):
    if a == "summ_d":
        return dataframe.describe()
    elif a == "summ_i":
        df_datatypes = pd.DataFrame(dataframe.dtypes)
        df_null_count = dataframe.count()
        a = df_datatypes.rename(columns={0: 'DType'})
        b = df_null_count.to_frame().rename(columns={0: 'Non-Null Count'})
        dataframe = b.merge(a, left_index=True, right_index=True).reset_index().rename(columns={'index': 'Column'})
        return dataframe
    elif a == "summ_p":
        df_pivot = pd.pivot_table(df, values=['Average viewers', 'Followers', 'Stream time(minutes)'],
                                  index='Language',
                                  columns='Partnered', aggfunc=np.mean, fill_value=0)
        df_pivot = df_pivot.reindex(df_pivot['Average viewers'].sort_values(by=True, ascending=False).index)
        return df_pivot
    elif a == "plot_d":
        df.select_dtypes(include='number').hist(figsize=(22, 9), bins=12)
    elif a == "plot_c":
        corr = df.corr().round(2)
        sns.heatmap(corr, xticklabels=corr.columns.values, yticklabels=corr.columns.values, vmin=-1, vmax=1, annot=True)
    else:
        raise ValueError("Analysis not supported (supported analysis: summ_d, summ_i, summ_p, plot_d, plot_c)")


# scelta del nominativo/formato dell'output
def data_output(o):
    if type_analysis == 'summ_d' or type_analysis == 'summ_i' or type_analysis == 'summ_p':
        if o.endswith(".txt"):
            file = open(path_o, 'w')
            file.write(analysis(type_analysis, df).to_string())
            file.close()
        elif o.endswith(".csv"):
            file = open(path_o, 'w', newline='')
            file.write(analysis(type_analysis, df).to_csv())
            file.close()
        elif o.endswith(".json"):
            file = open(path_o, 'w')
            file.write(analysis(type_analysis, df).to_json())
            file.close()
        else:
            raise ValueError("Format not supported (supported formats: txt, csv, json)")
    if type_analysis == 'plot_d' or type_analysis == 'plot_c':
        analysis(type_analysis, df)
        plt.savefig(o, facecolor='w', bbox_inches='tight')


# variabili d'ambiente
k_user = os.getenv("KAGGLE_USERNAME", 'marc0rm')  # user name Kaggle
k_key = os.getenv("KAGGLE_KEY", '1270b13d3ee3685961cb75e510f8aa5b')  # key Kaggle
get_i = os.getenv("GET_INPUT", 'local')  # acquisizione input
path_i = os.getenv("PATH_INPUT", 'twitchdata-update.csv')  # path input
type_analysis = os.getenv("ANALYSIS_TYPE", 'plot_d')  # tipo di analisi
path_o = os.getenv("PATH_OUTPUT", 'prova3.png')  # nominativo/formato output

df = data_input(get_i)
data_output(path_o)
