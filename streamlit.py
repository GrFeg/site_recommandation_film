################################################## Importation des librairies ##################################################################
if 1:
    from fonction import log

    print('')
    print('')
    print('')
    print('')
    log('Démarrage de Streamlit',0)

    import streamlit as st
    import streamlit.components.v1 as components
    import pandas as pd
    import ml
    import language_fr
    import language_en
    from PIL import Image
    import requests
    from io import BytesIO
    import json
    import numpy as np
    import streamlit.components.v1 as com
    from streamlit_lottie import st_lottie
    from matplotlib.animation import FuncAnimation, PillowWriter
    from streamlit_option_menu import option_menu
    import base64
    import time
    import streamlit.components.v1 as components

################################################################################################################################################

############################################################ API #################################################################################

def api():
    api_key = "" #Entrer sa clé API TBDM
    
    #FR
    url = "https://api.themoviedb.org/3/trending/movie/day?language=fr"
    headers = {
        "accept": "application/json",
        "Authorization": api_key} 
    response = requests.get(url, headers=headers)
    top5_fr = json.loads(response.text)
    top5_fr = top5_fr['results'][0:5]

    #EN
    url = "https://api.themoviedb.org/3/trending/movie/day?language=en-US"
    headers = {
        "accept": "application/json",
        "Authorization": api_key} 
    response = requests.get(url, headers=headers)
    top5_en = json.loads(response.text)
    top5_en = top5_en['results'][0:5]

    st.session_state.top5_fr = top5_fr
    st.session_state.top5_en = top5_en

def resume_recherme_film(tconst):
    if st.session_state.langue == "Français":
        langue = 'fr'
    else:
        langue = "en-US"
    print(tconst)
    url = f"https://api.themoviedb.org/3/movie/{tconst}?language={langue}"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmODBhNGQ0ZTRlZmFhNTFmN2NmYTEyMWJkZDU4MjViNSIsInN1YiI6IjY2NGE1YmI0ZGVjY2IyOGNjNDdjYjRmMyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.2fhn_7G72_ZS8Klwn-sisfLd-4rzPvMZEhuM70PodAA"
    }

    reponse = json.loads(requests.get(url, headers=headers).text)
    return reponse['overview']
##################################################################################################################################################

############################################### Définition des variables principales ###########################################################

#Création du data frame en utilisant notre csv.
df = pd.read_csv('C:\\Users\\Greg\\Desktop\\bot discord py\\projet2\\test2.csv' , sep = ',')
print("\nLignes où la colonne 'primaryName' est NaN:")

df = df[df['Adult'] == 0]
df = df.drop('endYear', axis = 1)
df = df[df['primaryTitle'].notna() & (df['primaryTitle'] != '')]
df = df[df['numVotes'].notna() & (df['numVotes'] != '')]
df = df[df['title'].notna()]


df['backdrop_path'] = df['backdrop_path'].dropna()
df['primaryName'] = df['primaryName'].dropna()

derniere_sorties = df['tconst'][df['startYear'] > 2023].unique()[:5]

#print(df.info())

#Initialisation des variables du cache du site pour stocker les états des bouton, selecbox.
def init():
    if "langue" not in st.session_state:
        st.session_state.langue = "Français"

    if "menus" not in st.session_state:
        st.session_state.menus = "menus"

    #With 2
    if 'rechercher' not in st.session_state:
        st.session_state.rechercher = False
    if 'choix_recherche' not in st.session_state:
        st.session_state.choix_recherche = False

    #With 3
    if 'recomandation' not in st.session_state:
        st.session_state.recomandation = False
    if 'selectbox_recommandation' not in st.session_state:
        st.session_state.selectbox_recommandation = False

    st.session_state.init = False
    api()

##################################################################################################################################################

###################################################### Définition des fonctions ##################################################################

#Fonction pour récuperer le css d'un fichier
def lire_css(fichier: str):
    with open(fichier, "r", encoding = 'utf8') as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

#Fonction pour récuperer le html d'un fichier
def lire_html(fichier: str):
    with open(fichier, 'r', encoding = 'utf8') as f:
        return f.read()  

#Fonction pour renvoyer une liste de film en fonction de la recherche
def choix(df, recherche: str):
    '''
    Fonction qui va ressortir une liste avec tout les nom de films contenant 'reponse' présent dans le df
    df: DatFrame contenant la base de donnée
    recherche: str contenant le film que l'utilisateur recherche
    '''
    if st.session_state.langue == "Français":
        df_contient_resultat = df[df['title'].str.contains(recherche, case = False)].sort_values(by = 'numVotes', ascending= False)
    else:
        df_contient_resultat = df[df['primaryTitle'].str.contains(recherche, case = False)].sort_values(by = 'numVotes', ascending= False)

    df_resultat = df_contient_resultat.sort_values(by = 'numVotes', ascending= False)

    if st.session_state.langue == "Français":
        df_resultat_tconst = df_resultat['title'].unique()
    else:
        df_resultat_tconst = df_resultat['primaryTitle'].unique()
    choix = []
    for i in df_resultat_tconst:
        choix.append(i)

    return choix

#Affichage des tendances
def affichage_tendance():

    st.write(f"<br><span style=' font-size:40px; color: #141826; padding: 10px; box-shadow: 10px 5px  #141826; border: 3px solid #141826; '>:movie_camera: {texte['t_derniere_sorties']}</span>", unsafe_allow_html= True)
    st.write("<br>", unsafe_allow_html= True)
    #Si recuperation_film jamais executé pour une langue l'execute et stock dans le cache, sinon va directement chercher dans le cache.
    print(st.session_state.langue)
    if st.session_state.langue == "Français":
            if ('top5_fr_rasultat' not in st.session_state):
                st.session_state.top5_fr_rasultat = recuperation_film(st.session_state.top5_fr)
                print(st.session_state.top5_fr_rasultat)
                titre, lien_image = st.session_state.top5_fr_rasultat
            else:
                titre, lien_image = st.session_state.top5_fr_rasultat
    if st.session_state.langue == "English":
            if ('top5_en_rasultat' not in st.session_state):
                st.session_state.top5_en_rasultat = recuperation_film(st.session_state.top5_en)
                titre, lien_image = st.session_state.top5_en_rasultat
            else:
                titre, lien_image = st.session_state.top5_en_rasultat
        
    film1, film2, film3, film4, film5 =  st.columns([1, 1, 1, 1, 1])

    with film1:
            st.image(lien_image[0])#sss
            st.write(titre[0])
    with film2:
            st.image(lien_image[1])
            st.write(titre[1])
    with film3:
            st.image(lien_image[2])
            st.write(titre[2])
    with film4:
            st.image(lien_image[3])
            st.write(titre[3])
    with film5:
            st.image(lien_image[4])
            st.write(titre[4])

#Fonction pour gérer l'affichage de la rubrique "Rechercher un film"
def recherche_film(df, reponse):

    lire_css('recherche_film.css') 
    html_content = lire_html('recherche_film.html')  

    #Recherche dans le df les résultat contenant ce que l'utilisateur a chercher, et les tries par numVotes.
    if st.session_state.langue == "Français":
        df_contient_resultat = df[df.title.str.contains(reponse, case = False)].sort_values(by = 'numVotes', ascending= False)
    else:
        df_contient_resultat = df[df['primaryTitle'].str.contains(reponse, case = False)].sort_values(by = 'numVotes', ascending= False)

    df_resultat = df_contient_resultat.sort_values(by = 'numVotes', ascending= False)
    df_resultat_unique = df_resultat.head(1)
    image = str(df_resultat_unique['backdrop_path'].unique())
    image = image.replace('[','').replace("'",'').replace("]",'')

    st.write(f"{texte['t_lf_result_1']} {reponse} : {len(df_contient_resultat['title'].unique())} {texte['t_lf_result_2']}")
    lien_image = 'https://image.tmdb.org/t/p/original' + image
    tconst = df_resultat_unique['tconst'].iloc[0]

    dico_affichage = {'producer': [],
                      'director': [],
                      'actor'   : [],
                      'actress' : []}
    
    #Pour chaque nom travaillant sur le film le filtre en fonction de category (acteur, actrice, producteur etc...)
    for _, nom in df_resultat[df_resultat['tconst'] == tconst].iterrows():

        if nom['category'] == "actor":
            nom_a = nom['characters'].replace('[','').replace(']','').replace('"','')
            dico_affichage['actor'].append([nom['primaryName'], nom_a])

        elif nom['category'] == "actress":
            nom_a = nom['characters'].replace('[','').replace(']','').replace('"','')
            dico_affichage['actress'].append([nom['primaryName'], nom_a])

        elif nom['category'] == "producer":
            dico_affichage['producer'] = [nom['primaryName']]

        elif nom['category'] == "director":
            dico_affichage['director'] = [nom['primaryName']]
            
        revenue = texte['t_html_1'][3] + str(round(nom['revenue'] / 1000000)) + "M$"
        budget = texte['t_html_1'][2] + str(round(nom['budget'] / 1000000)) + "M$"

        #Calcul du gain que le film à réalisé en fonction de budget et des recettes
        gain = ""
        if nom['revenue'] != 0 or nom['budget'] != 0:
            if nom['revenue'] / nom['budget'] < 1:
                gain = f"(  -{round(nom['revenue'] / nom['budget'] * 100)}% )"
            if nom['revenue'] / nom['budget'] > 1:
                gain = f"(  +{round(nom['revenue'] / nom['budget'] * 100)}% )"

    #Affichage des différentes personnes travaillant sur le film
    affichage_createur = ""
    if dico_affichage["director"] != []:
        affichage_createur += f"{texte['t_html_1'][0]} {dico_affichage['director'][0]} <br>"
    if dico_affichage["producer"] != []:
        affichage_createur += f"{texte['t_html_1'][1]} {dico_affichage['producer'][0]} <br>"

    affichage_acteur = f"{texte['t_html_1'][4]} <br>"
    for nom in dico_affichage['actor']:
            
        if nom[0] == 'Tom Holland':
            affichage_acteur += f'- {nom[0]} <3 --> {nom[1]} <br>'
        else:
            affichage_acteur += f'- {nom[0]} --> {nom[1]} <br>'

    affichage_actrice = f"{texte['t_html_1'][5]} <br>"
    for nom in dico_affichage['actress']:
        affichage_actrice += f'- {nom[0]} --> {nom[1]} <br>'

    if st.session_state.langue == "Français":
        titre = df_resultat_unique['title'].iloc[0]
    else:
        titre = df_resultat_unique['primaryTitle'].iloc[0]

    resume = resume_recherme_film(df_resultat_unique['tconst'].iloc[0])

    #Affichage du bloc du site avec le site.html et style.csss
    html_content = html_content.format( lien_image =  lien_image,
                                        acteur     =  affichage_acteur,
                                        actrice    =  affichage_actrice, 
                                        creation   =  affichage_createur,
                                        revenue    =  revenue,
                                        budget     =  budget,
                                        titre      =  titre,
                                        gain       =  gain,
                                        resume     =  resume)
        
    bloc = st.container()
    bloc.markdown(html_content, unsafe_allow_html=True)  

def affichage_recommandation_film(df, recherche):


    liste_titre = ml.recommandation_film(df, recherche)
    if liste_titre == -1:
        st.write('Erreur recherche du titre')
        return
    print(liste_titre)


    lire_css('recommandation_film.css') 
    html_content = lire_html('recommandation_film.html')

    lien_image = []
    note = []
    note_graph = []
    budget = []
    revenu = []
    producteur = []
    annee = []

    if st.session_state.langue == "English":
        nom_film = []
        for titre in liste_titre:
            nom_film.append(df['primaryTitle'][df['title'] == titre].unique()[0])
    else:
        nom_film  = liste_titre


    for i in range(len(liste_titre)):

        #Image
        image = str(df['backdrop_path'][df['title'] == liste_titre[i]].unique())
        print(image)
        #Test si plusieurs images dispo, si oui prend la première.
        if ' ' in image:
            image = image.split(' ')[0]
        if 'jpg' not in image:
            lien_image.append('nan')
        else:
            image = image.replace('[','').replace("'",'').replace("]",'')
            lien_image.append('https://image.tmdb.org/t/p/original' + image)
        print(lien_image[-1])

        #Note
        note.append(df['averageRating'][df['title'] == liste_titre[i]].unique()[0])
        note_graph.append(note[-1]* 326/ 10) #Pour le graph
        
        if not np.isnan(df['budget'][df['title'] == liste_titre[i]].unique()[0]):
            if int(df['budget'][df['title'] == liste_titre[i]].unique()[0]) == 0:
                budget.append("N/A")
            else:
                budget.append(str(round(df['budget'][df['title'] == liste_titre[i]].unique()[0] / 1000000, 2)) + "M")
        else:
            budget.append("NaN")
            
        if not np.isnan(df['revenue'][df['title'] == liste_titre[i]].unique()[0]):
            if int(df['revenue'][df['title'] == liste_titre[i]].unique()[0]) == 0:
                revenu.append("N/A")
            else:
                revenu.append(str(round(df['revenue'][df['title'] == liste_titre[i]].unique()[0] / 1000000, 2)) + "M")
        else:
            revenu.append("NaN")

        producteur.append(df['primaryName'][(df['title'] == liste_titre[i]) & (df['category'] == 'director')].unique()[0])
        annee.append(int(df['startYear'][df['title'] == liste_titre[i]].unique()[0]))


    print(len(lien_image), len(liste_titre), len(note), len(note_graph), len(budget), len(revenu), len(producteur), len(annee))
    #Affichage du bloc du site avec le site.html et style.csssssss
    html_content = html_content.format(t_html_2_1 = texte['t_html_2_1'],
                                       t_html_2_2 = texte['t_html_2_2'],
                                       lien_image =  lien_image,
                                       titre = nom_film,
                                       note = note,
                                       note_graph = note_graph,
                                       budget = budget,
                                       revenu = revenu,
                                       producteur = producteur,
                                       annee = annee)
        
    bloc = st.container()
    bloc.markdown(html_content, unsafe_allow_html=True)  
    return True

#Quelle langue choisissSssssssssssssssssssssss
def set_language():
    st.session_state.langue = st.session_state.selected_langue

#retourne les informations clé d'une liste films généré par l'API
def recuperation_film(top):

    titre = []
    images = []

    for film in top:
        titre.append(film['title'])

        image = film["backdrop_path"]
        lien_image = 'https://image.tmdb.org/t/p/original' + image

        response = requests.get(lien_image)
        image = Image.open(BytesIO(response.content))

        width, height = image.size
        new_width = 1400  
        new_height = 2100  

        left = (width - new_width) / 2
        top = (height - new_height) / 2
        right = (width + new_width) / 2
        bottom = (height + new_height) / 2

        images.append(image.crop((left, top, right, bottom)))


    return titre, images

##################################################################################################################################################

if 'init' not in st.session_state:
        st.session_state.init = True
    
if st.session_state.init:
    init()

#Langue
if st.session_state.langue == "Français":
    texte = language_fr.texte
if st.session_state.langue == "English":
    texte = language_en.texte

####################################################### Début du Site ############################################################################

#Paramètre global du site
st.set_page_config(layout="wide")

streamlit_style = """
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Bungee+Shade&family=Fredericka+the+Great&display=swap');

            html, body, div, p, span, [class*="css"]  {
            font-family: "Fredericka the Great", sans-serif;
            font-weight: 400;
            font-style: normal;
            font-size: 22px;
            color: #141826;
            }
            </style>
            """
st.markdown(streamlit_style, unsafe_allow_html=True)

def sidebar_bg(side_bg):
   side_bg_ext = 'png'
   st.markdown(
      f"""
      <style>
      [data-testid="stSidebar"] > div:first-child {{
          background: url(data:image/{side_bg_ext};base64,{base64.b64encode(open(side_bg, "rb").read()).decode()});
      }}
      </style>
      """,
      unsafe_allow_html=True,
      )
sidebar_bg('image/affiche.png')


#Vidéosssssssssssss
@st.cache_resource
def Base64CacheIt(filename):
    # Read the video file as bytes
    with open(filename, "rb") as file:
        video_bytes = file.read()
    
    # Encode the video bytes as base64
    video_base64 = base64.b64encode(video_bytes).decode()
    
    # Create the HTML video elements
    video_html = f"""
    <video controls autoplay width="100%">
        <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
        Your browser does not support the video element.
    </video>
    """
    
    return video_html
if 'video' not in st.session_state:
        st.session_state.video = True

if st.session_state.video == True:
    st.session_state.video = False
    video_placeholder = st.empty()
    video_html = Base64CacheIt("Curtains.mp4")

    video_placeholder.empty()
    time.sleep(1)
    video_placeholder.markdown(video_html, unsafe_allow_html=True)

    time.sleep(8)
    st.experimental_rerun()

with st.sidebar:
    "."

#Bannière du site
components.html(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee+Shade&family=Fredericka+the+Great&display=swap');
        .test{
            display: flex;
            justify-content: center;        
            background: url(http://illetterista.it/img/text-paper/text-paper-dark@2x.png) repeat-x;
            background-repeat: repeat;
            background-attachment: scroll;
            background-clip: border-box;
            background-color: rgb(20, 24, 38);
            background-image: url("http://illetterista.it/img/bg-texture.png");
            background-origin: padding-box;
            background-position-x: 0%;
            background-position-y: 0%;
            background-repeat: repeat;
            background-size: auto
            width: auto;
            height: 550px;
            }
        .image_ban{
            margin-left: 280px;
            text-align : center;
            width: 500px;
            height: 50px;
        }
        .texte{
            margin-top: 50px;
            color: #C99C59;
            font-family: "Fredericka the Great", sans-serif;
            font-size: 25px
        }
            
    </style>
    <div class = "test">
        <div class = "image_ban">
            <img class="logo" src="https://i.ibb.co/nfZNS3t/tes5.png" alt="Prouuuuuuuuuuuuuuuuuuuuuuuuuuuuuut">
        </div>
    <div class = "texte">Trouvez le film fait pour vous</div>
    </div>
    """
)


#st.image('image/cinema.png', width= 2000, use_column_width='True')sssssssssssssssssss

left, center, right = st.columns([1, 16, 4])

with right:
    st.write('<br>', unsafe_allow_html= True)
    st.markdown(
    '''
    <style>
    .streamlit-expanderHeader {
        background-color: white;
        color: black; # Adjust this for expander header color
    }
    .streamlit-expanderContent {
        background-color: white;
        color: black; # Expander content color
    }
    </style>
    ''',
    unsafe_allow_html=True
)
    with st.expander("Language"):
        options = ["Français", "English"]
        index = options.index(st.session_state.langue)

        selected_langue = st.radio(texte['select_langue'],
                                   options,
                                   index = index,
                                   key='selected_langue', 
                                   on_change=set_language)
        st.session_state.langue = selected_langue  # Mettre à jour la session state avec la valeur sélectionnée
        st.write(st.session_state.langue)

with center:
    #Définition de la Barre de naviguation verticale
    st.write('<br>', unsafe_allow_html= True)
    selected_tab = option_menu(
                                menu_title=None,  # pas de titre de menu
                                options=[texte['tabs_title1'], texte['tabs_title2'], texte['tabs_title3']],
                                icons=["house", "search", "list"],
                                menu_icon="cast",  # icône de menu principal
                                default_index=0,  # sélection initiale
                                orientation="horizontal",
                                styles={
                                    "container": {"padding": "0!important", "background-color": "#141826"},
                                    "icon": {"color": "#B5B5B4", "font-size": "25px"},
                                    "nav-link": {
                                        "font-family": '"Fredericka the Great", sans-serif',
                                        "font-size": "20px",
                                        "text-align": "center",
                                        "margin": "0px",
                                        "color": "#C99C59",
                                        "font-weight": "bold",
                                    },
                                    "nav-link-selected": {"background-color": "#D2C8BE"},
                                }
                                )
    
    print(selected_tab)                     
    #Page de bienvenue
    if selected_tab == texte['tabs_title1']:
        affichage_tendance()
        st.session_state.rechercher = False
        st.session_state.recomandation = False

    #Recherche de film
    if selected_tab == texte['tabs_title2']:

        #Petite form pour la partie recherche de film.ddssssssssssssssssss
        st.write(f"<br><span style=' font-size:40px; color: #141826; padding: 10px; box-shadow: 10px 5px  #141826; border: 3px solid #141826; '>:popcorn: {texte['title_lf_film']}</span>", unsafe_allow_html= True)
        film = st.form('film', border = False)


        #Définition de la première boite avec la zone de texte et le bouton rechercher
        reponse = film.text_input(texte['t_select_box_main_lf'] + ':popcorn:', '')
        boutton_rechercher = film.form_submit_button(texte['buton_lf'],)

        #Si le bouton rechercher est appuyé.s
        if boutton_rechercher:
            #Met à jour l'état dans le cache
            st.session_state.rechercher = True

        #Si le bouton rechercher est appuyé.
        if st.session_state.rechercher:
            log('Page Rechercher un film --> boutton_rechercher appuyé', 0)

            #Définition de la form
            resultat = st.form('resultat_film')

            #Créer la selectbox si le film n'est pas le bon, pour que l'utilisateur puisse choisir celui qu'il souhaite.
            choix = choix(df, reponse)
            solect = st.selectbox(texte['t_select_box_other_result'], choix)

            #Si un film est choisis dans la selecbox choix (plus utilisé)
            if solect:
                st.session_state.choix_recherche = True
            
            #Si bouton rechercher appuyé.
            if st.session_state.rechercher:
                #Affichaque du film en fonction de la select_box
                recherche_film(df, solect)
            else:
                #Affichaque du film en fonction de la zone de texte
                recherche_film(df, reponse)

    #Recommandation de film
    if selected_tab == texte['tabs_title3']:

        st.write(f"<br><span style=' font-size:40px; color: #141826; padding: 10px; box-shadow: 10px 5px  #141826; border: 3px solid #141826; '>:clapper: {texte['title_recomandation']}</span>", unsafe_allow_html= True)

        #Petite form pour la partie recherche de film.ss
        zone_reco = st.form('reco',border = False)

        #Zone de texte et bouton pour valider la recherche
        if st.session_state.langue == "Français":
            reponse_reco = zone_reco.selectbox(texte['t_select_box_main_lf'], df['title'].unique())
        else:
            reponse_reco = zone_reco.selectbox(texte['t_select_box_main_lf'], df['primaryTitle'].unique())
        boutton_recomandation = zone_reco.form_submit_button(texte['buton_lf'])

        #Si le bouton rechercher est appuyé (pas très utile).
        if boutton_recomandation:
            log('Page Recomandation de film --> boutton_recomandation appuyé !', 0)
            st.session_state.recomandation = True


        #Si boutton Appuyé
        if st.session_state.recomandation:

            #Recherche du film entré par l'utilisateur
            if st.session_state.langue == "Français":
                df_resultat_reco = df[df.title.str.contains(reponse_reco, case = False)].sort_values(by = 'numVotes', ascending= False)['title']
                resultat_reco = df_resultat_reco.iloc[0]
            else:
                df_resultat_reco = df[df.primaryTitle.str.contains(reponse_reco, case = False)].sort_values(by = 'numVotes', ascending= False)['title']
                resultat_reco = df_resultat_reco.iloc[0]

            f"{texte['t_result']} "

            #Affichage dans la console pour DEBBUG
            print('')
            log('Etat des variables:', 0)
            print("ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ\033[1m- etat de selectbox_recommandation:\033[0m ", st.session_state.selectbox_recommandation )
            print("ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ\033[1m- resultat_reco:\033[0m ", resultat_reco)
            print('')

            affichage_recommandation_film(df, resultat_reco)

##################################################################################################################################################
