import pandas as pd
from fonction import log
from sklearn.neighbors import NearestNeighbors
import numpy as np

'''
Fichier contenant l'intégralité du machine learnin pour la recommandation de film.
fontion.py utilisé pour l'affichage des log pour le DEBBUG (plus esthétique)
'''

#Fonction qui va faire la recommandation de film
def recommandation_film(df, reponse):

    #Création du df pour la recommandation de film, selection des ligne utile, tries, nettoyage, factorize...
    df_ml = df[['backdrop_path', 'tconst','averageRating','primaryTitle','title','category','primaryName','Action','Adult','Adventure','Animation','Biography','Comedy','Crime','Documentary','Drama','Family','Fantasy','Film-Noir','Game-Show','History','Horror','Music','Musical','Mystery','News','Reality-TV','Romance','Sci-Fi','Short','Sport','Talk-Show','Thriller','War','Western','30','30-40','40-50','50-60','60-70','70-80','80-90','90-00','00-10','10-20','20-30']]
    df_ml = df_ml.dropna()
    df_ml = df_ml[df_ml['Adult'] == 0]
    df_ml['backdrop_path'] = df_ml['backdrop_path'].dropna()


    df_ml = df_ml[df_ml['category'].str.contains('producer', case=False)]
    df_ml['primaryName'], _ = pd.factorize(df_ml['primaryName'])
    df_ml['director'] = df_ml['primaryName']


    df_ml[['30','30-40','40-50','50-60','60-70','70-80','80-90','90-00','00-10','10-20','20-30']] = df_ml[['30','30-40','40-50','50-60','60-70','70-80','80-90','90-00','00-10','10-20','20-30']] *0.5

    df_ml['Action'] =  df_ml['Action'] * 2
    df_ml['Animation'] =  df_ml['Animation'] * 4
    

    min_val = df_ml['director'].min()
    max_val = df_ml['director'].max()
    df_ml['director'] = (df_ml['director'] - min_val) / (max_val - min_val) * 500

    df_ml = df_ml.drop_duplicates(subset = 'tconst')

    #Définition de X, les colonnes utlisé pour le KNN
    X = df_ml[['director','averageRating','Action','Adult','Adventure','Animation','Biography','Comedy','Crime','Documentary','Drama','Family','Fantasy','Film-Noir','Game-Show','History','Horror','Music','Musical','Mystery','News','Reality-TV','Romance','Sci-Fi','Short','Sport','Talk-Show','Thriller','War','Western','30','30-40','40-50','50-60','60-70','70-80','80-90','90-00','00-10','10-20','20-30']]

    #Définition du modèle avec 6 voisins (lui même + 5) + entrainement
    modelNN = NearestNeighbors(n_neighbors=6)
    modelNN.fit(X)

    #Selection des colonnes utilisé pour le KNN en fonction de la reponse de l'utilisateur
    film = df_ml.loc[df_ml['title'] == reponse, X.columns]

    if film.empty:
        return -1

    #KNN
    neighbors = modelNN.kneighbors(film)
    print(neighbors)

    #Selectionne seulement la liste d'indice ou se trouve les films renvoyé par le KNN
    indice = neighbors[1][0]

    #Extraction des titres des film pour chaque indice de neighbors
    resultat = []
    log('Machine Learning réussis')
    print("ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ---------------Film choisis---------------")
    for i in range(0,6):
        print("ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ", df_ml.iloc[indice[i]]['title'])
        if reponse != df_ml.iloc[indice[i]]['title']:
            resultat.append(df_ml.iloc[indice[i]]['title'])
    print('ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ------------------------------------------')

    #Return la liste de film
    return resultat

log('Fichier ml.py chargé')