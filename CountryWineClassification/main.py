import unicodedata

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split

data = pd.read_csv(r'WineKB.csv')
data.head(5)

#rimuovere i duplicati
data[data.duplicated('description',keep=False)].sort_values('description').head(5)
#in base alle descrizioni e ai prezzi mancanti
data = data.drop_duplicates('description')
data = data[pd.notnull(data.price)]
print(data.shape)

#Esplorativa Analisi
#esista una correlazione significativa tra il costo del vino e la sua valutazione
#che c'è un aumento medio di $ 1,18 per ogni punto di aumento della valutazione
from scipy.stats import pearsonr
import statsmodels.api as sm
print("Correlazione di Pearson:", pearsonr(data.price, data.points))
print(sm.OLS(data.points, data.price).fit().summary())
sns.lmplot(y = 'price', x='points', data=data)

#Tracciando tutti i paesi ci sono alcuni strani grafici
#causa della bassa dimensione del campione per alcuni paesi
fig, ax = plt.subplots(figsize = (20,7))
chart = sns.boxplot(x='country',y='points', data=data, ax = ax)
plt.xticks(rotation = 90)
#plt.show()

print(data.country.value_counts()[:17])
#Dopo aver rimosso tutti i paesi con meno di 100 osservazioni
#Germania, Austria e Canada hanno i punteggi mediani più alti (punti)
#Tuttavia, la distribuzione complessiva sembra essere abbastanza uniforme.

country=data.groupby('country').filter(lambda x: len(x) >100)
df2 = pd.DataFrame({col:vals['points'] for col,vals in country.groupby('country')})
meds = df2.median()
meds.sort_values(ascending=False, inplace=True)

fig, ax = plt.subplots(figsize = (20,7))
chart = sns.boxplot(x='country',y='points', data=country, order=meds.index, ax = ax)
plt.xticks(rotation = 90)

plt.show()

#Di seguito sono riportati i prezzi medi del vino ordinati per mediana (dal più alto al più basso)
#al fine di valutare le distorsioni dei prezzi dovute
df3 = pd.DataFrame({col:vals['price'] for col,vals in country.groupby('country')})
meds2 = df3.median()
meds2.sort_values(ascending=False, inplace=True)

fig, ax = plt.subplots(figsize = (20,5))
chart = sns.barplot(x='country',y='price', data=country, order=meds2.index, ax = ax)
plt.xticks(rotation = 90)
plt.show()

#mediane per il barplot precedente
print(meds2)

#c'è una grande varietà di vini nel set di dati
#ma c'è un calo esponenziale nel numero di osservazioni per ogni tipo di vino
#poichè tenteremo di utilizzare queste etichette per classificare il nostro modello
#Lascerò cadere qualsiasi tipo di vino con meno di 200 osservazioni,
#perché non credo che ci siano dati sufficienti in questi bucket per generare un modello accuarte per prevedere il rispettivo tipo di vino
data = data.groupby('variety').filter(lambda x: len(x) >200)
list = data.variety.value_counts().index.tolist()
fig4, ax4 = plt.subplots(figsize = (20,7))
sns.countplot(x='variety', data=data, order = list, ax=ax4)
plt.xticks(rotation = 90)
plt.show()

#varietà di vino
data['variety'].unique()

#Di seguito è riportato un grafico a scatola contenente tutte le varietà di vino (con> 200 osservazioni)
#con le rispettive distribuzioni dei punti.
#Il Sangiovese Grosso sembra avere il punteggio medio più alto di tutti i vini
#Ci sono alcuni cali interessanti che si verificano dopo Champagne Blend, Shiraz, Cabernet Sauvignon e Nero d'Avola.
#Di interesse è il Merlot, che tende ad avere un gran numero di valori anomali altamente recensiti.
#Nonostante queste lievi variazioni, nel complesso la distribuzione puntuale è sostanzialmente uniforme.
data = data.groupby('variety').filter(lambda x: len(x) >200)
df4 = pd.DataFrame({col:vals['points'] for col,vals in data.groupby('variety')})
meds3 = df4.median()
meds3.sort_values(ascending=False, inplace=True)

fig3, ax3 = plt.subplots(figsize = (20,7))
chart = sns.boxplot(x='variety',y='points', data=data, order=meds3.index, ax = ax3)
plt.xticks(rotation = 90)
plt.show()
#In 13
df5 = pd.DataFrame({col:vals['points'] for col,vals in data.groupby('variety')})
mean1 = df5.mean()
mean1.sort_values(ascending=False, inplace=True)
fig3, ax3 = plt.subplots(figsize = (20,7))
chart = sns.barplot(x='variety',y='points', data=data, order=mean1.index, ax = ax3)
plt.xticks(rotation = 90)
plt.show()

#Non è sicuramente la stessa storia quando si guarda il prezzo
#C'è una chiara variazione qui, che può aiutare a prevedere il tipo di vino.
df6 = pd.DataFrame({col:vals['price'] for col,vals in data.groupby('variety')})
mean2 = df6.mean()
mean2.sort_values(ascending=False, inplace=True)

fig3, ax3 = plt.subplots(figsize = (20,7))
chart = sns.barplot(x='variety',y='price', data=data, order=mean2.index, ax = ax3)
plt.xticks(rotation = 90)
plt.show()


#Modellazione: Regressione Logica
# Assegniamo i nomi di colonna al dataset
X = data.drop(['Unnamed: 0','country','designation','points','province','region_1','region_2','variety','winery'], axis = 1)
y = data.variety
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)

wine =data.variety.unique().tolist()
wine.sort()
print(wine[:10])

output = set()
for x in data.variety:
    x = x.lower()
    x = x.split()
    for y in x:
        output.add(y)

variety_list =sorted(output)
print(variety_list[:10])
#Sost. i nomi tedeschi con nomi inglesi per i vini
data['variety'] = data['variety'].replace(['weissburgunder'], 'chardonnay')
data['variety'] = data['variety'].replace(['spatburgunder'], 'pinot noir')
data['variety'] = data['variety'].replace(['grauburgunder'], 'pinot gris')
#Sost. la garnacha spagnola con la grenache francese
data['variety'] = data['variety']. replace(['garnacha'], 'grenache')
data['variety'] = data['variety']. replace(['alvarinho'], 'albarino')

print ("Ci sono così tante rose nel set di dati")
print (len (data [data.variety.str.contains('Rose') == True]))
data = data [data.variety.str.contains('Rose') == False]

#elimina le dieresi e le tilde per rendere coerenti i nomi delle tue varietà.
def remove_accents (input_str):
    nfkd_form = unicodedata.normalize ('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

data['variety'] = data['variety'].apply(remove_accents)
data['description'] = data['description'].apply(remove_accents)

print('Ci sono così tante varietà che contengono la parola blend')
print(len(data[data.variety.str.contains('Blend') == True]))
data=data[data.variety.str.contains('Blend') ==False]

extras = ['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}', 'cab',"%"]
from nltk.corpus import stopwords
stop = set(stopwords.words('english'))
stop.update(variety_list)
stop.update(extras)

#Features
#le caratteristiche utilizzate sono il prezzo del vino e la sua descrizione

from scipy.sparse import hstack
vect = CountVectorizer(stop_words = stop)
X_train_dtm = vect.fit_transform(X_train.description)
price = X_train.price.values[:,None]
X_train_dtm = hstack((X_train_dtm, price))
X_train_dtm

X_test_dtm = vect.transform(X_test.description)
price_test = X_test.price.values[:,None]
X_test_dtm = hstack((X_test_dtm, price_test))
X_test_dtm


from sklearn.linear_model import LogisticRegression
models = {}
for z in wine:
    model = LogisticRegression()
    y = y_train == z
    model.fit(X_train_dtm, y)
    models[z] = model

testing_probs = pd.DataFrame(columns = wine)

#accuratezza
for variety in wine:
    testing_probs[variety] = models[variety].predict_proba(X_test_dtm)[:, 1]

predicted_wine = testing_probs.idxmax(axis=1)

comparison = pd.DataFrame({'actual': y_test.values, 'predicted': predicted_wine.values})

from sklearn.metrics import accuracy_score

print('Accuracy Score:', accuracy_score(comparison.actual, comparison.predicted) * 100, "%")
print(comparison.head(5))

