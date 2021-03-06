# Prova d’esame di Cloud, Distributed and Parallel Computing<br />Master in Data Science for economics, business and finance 2020/2021<br />Marco Richard Morandi

### Introduzione:
Build, deployment e run di un docker per l'analisi di dati di uno specifico dataset(https://www.kaggle.com/aayushmishra1512/twitchdata).


### Requisiti:
Docker desktop


## Relazione di Progetto

Il progetto si prefigge come obiettivo di restituire cinque tipologie di analisi effettuate su un dataset riportante i top Streamers di Twitch. (dataset reperibile su Kaggle al seguente link (https://www.kaggle.com/aayushmishra1512/twitchdata).

Seguendo la metodologia dei Twelve-Factor:

 1. **CODEBASE**: è presente una sola codebase, per la quale è stato utilizzato un unico sistema di versione, in questo caso Github.
 2. **DEPENDENCIES**: Tutte le dipendenze, nel nostro caso le librerie utili a python per far funzionare l’applicazione, sono state inserite all’interno del file requirements.txt.
 3. **CONFIG**: La configurazione dell’applicazione, per permettere il deployment anche in altri ambienti, è possibile settando i parametri voluti all’interno del file config.txt.
4.	**BACKING SERVICE**: A livello di backing service non è stato utilizzato alcun servizio di terze parti. L’output generato dall’applicazione verrà salvato in una cartella all’interno del docker la quale, tramite una operazione di binding sarà collegata ad una cartella del dockerhost.
5.	**BUILD, RELEASE, RUN**: La fase di build dell’applicazione, avvenuta tramite un linguaggio specifico (Python) e le librerie necessarie, ha permesso al codice all’interno del repository di essere una app totalmente eseguibile.\
Nella fase di release viene combinato quanto ottenuto dalla fase di build con le configurazioni impostabili all’interno del file config.txt.\
La fase di esecuzione esegue l’applicazione nell’ambiente di destinazione, utilizzando le configurazioni impostate assieme ad eventuali backing services.
7.	**PROCESSES**: L’applicazione all’interno del docker risulta un processo stateless, motivo per il quale viene effettuato un binding con una cartella del docker host (in alternativa si poteva utilizzare un servizio di terze parti come backing services).
8.	**PORT BINDING**: Non essendo stata costruita come una webapp non viene utilizzato il binding delle porte
9.	**CONCURRENCY**: Tramite l’utilizzo di docker, e di strumenti aggiuntivi come kubernetes o DockerSwarm, è possibile gestire una molteplicità di docker riuscendo ad ottenere una ottima scalabilità, sia per il numero di processi da gestire sia per la pesantezza dei singoli processi. Vista la semplicità dell’app non sono stati implementati nessuno di questi servizi.
10.	**DISPOSABILITY**: Trattandosi di una applicazione semplice la rilasciabilità è quasi irrelevante ed è data principalmente al prevedere ogni eventuale possibile fail, come la mancanza di del dataset all’interno della cartella indicata o la scelta di parametri inesistenti.(es: `raise ValueError("Analysis not supported (supported analysis: summ_d, summ_i, summ_p, plot_d, plot_c)")`)
11.	**DEV/PROD PARITY**: Discorso simile per la dev/prod parity, in quanto l’applicazione è estremamente semplice. La creazione di un virtual enviroment in python come ambiente di sviluppo e l’utilizzo all’interno del docker del medesimo ambiente di sviluppo aiuta a mantenere la parità tra le due fasi così come un rilascio continuo di ogni eventuale modifica.
12.	**LOGS**: Per la gestione dei logs si potrebbero utilizzare servizi come Elasticksearch, Logstash e Kibana e salvarli in un backing service, ma vista la semplicità dell’applicazione creata nessuno di questi servizi è stato implementato.
13.	**ADMIN PROCESSES**: I processi di amministrazioni vengono eseguiti un’unica volta durante la build del docker seguendo i passaggi indicati nel Dockerfile permettendo così la creazione di una applicazione pronta per l’uso.

Il codice creato utilizza le seguenti funzioni:

`def data_input(i):` scelta della provenienza dell'input\
`def analysis(a, df):` scelta dell'analisi da effettuare sul dataset\
`def data_output(o):` scelta del nominativo/formato dell'output

e le seguenti variabili d'ambiente settabili nel file config.txt:

`k_user = os.getenv("KAGGLE_USERNAME", '')` user name Kaggle\
`k_key = os.getenv("KAGGLE_KEY", '')` key Kaggle\
`get_i = os.getenv("GET_INPUT", 'local')` tipologia di acquisizione input\
`path_i = os.getenv("PATH_INPUT", 'twitchdata-update.csv')` path input\
`type_analysis = os.getenv("ANALYSIS_TYPE", 'plot_d')` tipologia di analisi sul dataset\
`path_o = os.getenv("PATH_OUTPUT", 'prova.png')` nominativo/formato output

## Manuale dettagliato di build e deployment

1.	Scaricare e installare Docker Desktop da https://www.docker.com/products/docker-desktop
2.	Verificare di avere abilitata la virtualizzazione all’interno della propria macchina.
3.	Fare un git pull dal seguente repository: https://github.com/marco-moran/Esame
4.	Entrare all'interno della cartella Esame appena scaricata
5.	Aprire il terminale ed eseguire i seguenti comandi: `docker build -t analisi ./`
6.	Una volta creata l’immagine del docker è possibile procedere alla configurazione dei seguenti parametri all’interno del file config.txt :
	- **KAGGLE_USERNAME**: parametro utile al download del dataset direttamente dal sito di Kaggle. L’utilizzo delle API del sito è concesso unicamente agli utenti registrati. 
Per recuperare l’USERNAME e la KEY bisogna registrarsi sul sito di Kaggle, andare nel proprio profilo e selezionare ‘Create API Token’. Questo permetterà il download del file ‘kaggle.json’ dove all’interno sono indicati l’USERNAME e la KEY (https://github.com/Kaggle/kaggle-api)
	- **KAGGLE_KEY**: vedi punto a.
	- **GET_INPUT**: parametro per indicare da quale fonte recuperare il dataset.\
	***from_site*** indica che verranno utilizzati i parametri a. e b. per scaricare il dataset direttamente da kaggle.\
	***local*** indica che il dataset verrà recuperato dalla cartella che verrà collegata al docker tramite operazione di binding.\
	*(default=local)*
	- **PATH_INPUT**: parametro che indica il nominativo completo del dataset presente all’interno dalla cartella che verrà collegata al docker tramite operazione di binding.\
	Utilizzato quando GET_INPUT=local.\
	*(default= twitchdata-update.csv)*
	- **ANALYSIS_TYPE**: parametro che indica la tipologia di analisi da effettuare sul dataset.\
	***plot_d*** restituirà una serie di grafici relativi alla distribuzione delle variabili numeriche.\
	***plot_c*** restituirà un grafico relativo alla correlazione tra le variabili numeriche.\
	***summ_d*** restituirà una serie di indicatori statistici relativi alle variabili numeriche.\
	***summ_i*** restituirà un riepilogo delle colonne, tipo di dato e conteggio dei valori nulli.\
	***summ_p*** restituirà una tabella pivot che avrà sulle colonne *Average viewers*, *Followers*, *Stream time(minutes)*, suddivise se o meno *Partnered*, con il loro valore medio per ogni valore della variabile *Language* posto sulle righe.\
	*(default=plot_d)*
	- **PATH_OUTPUT**: parametro che indica il nominativo completo che si vuole associare all’output dell’applicazione. A seconda dell’analisi scelta si potranno scegliere i seguenti formati:
***summ_d, summ_i, summ_p:*** .txt, .csv, .json
***plot_d, plot_c:*** eps, jpeg, jpg, pdf, pgf, png, ps, raw, rgba, svg, svgz, tif, tiff\
*(default=prova.png)*
7.	Procedere quindi all’esecuzione del docker con il seguente comando da terminale: `docker run -v <percorso della cartella da collegare>:/usr/app/data --env-file config.txt analisi`.\
La cartella da collegare sarà il luogo dove verrano salvati gli output dell'applicazione e dovrà contenere il dataset al proprio interno qualora si sia scelto GET_INPUT=local