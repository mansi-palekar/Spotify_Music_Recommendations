# --- IMPORTING DEPENDENCIES ---

import pandas as pd
import numpy as np
import math
import scipy
from sklearn.metrics.pairwise import cosine_similarity
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials 
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import matplotlib as mpl
import seaborn as sns
from mplsoccer import PyPizza, FontManager
import matplotlib.patheffects as path_effects

# --- LOADING REQUIRED DATAFRAMES ---

# Loading the main dataframe
df = pd.read_csv("Billboards with Audio Features + Genres,Artists OHE (Final).csv", low_memory = False)
df.drop(['Artist 1', 'Artist 2', 'Artist 3', 'Artist 4', 'Artist 5', 'Artist 6', 'Artist 7', 'Song and Artist'],
        axis = 1, inplace = True)

# Loading the embeddings dataframe
embeddings_all_df = pd.read_csv("df_embeddings.csv")

# --- SETTING UP SPOTIFY ---
clientID = '60f1e0a91b764b9eac6b5d652f8bb384'
clientSecret = '5f34cf94b74c43ec853706b274e7675b'
client_credentials_manager = SpotifyClientCredentials(client_id=clientID, client_secret=clientSecret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

# --- SETTING REQUIRED FONTS AND COLOURS ---

# FONTS
robotoBold = FontManager(('https://github.com/Chaitanya98/Football-Analytics/blob/main/Barcalytix/Fonts/GothamBold.ttf?raw=true'))
robotoMed = FontManager(('https://github.com/Chaitanya98/Football-Analytics/blob/main/Barcalytix/Fonts/GothamMedium.ttf?raw=true'))

# COLOURS
spotifyGreen = '#1dda63'
bg_color_cas = "#9bf0e1"
grey = "#979797"
lightgrey = "#bdbdbd"

# ---------------------------------------------------------------------------------------------- #

# --- DEFINING REQUIRED FUNCTIONS ---

# 1
# Quality function that determines the quality of the rank

def quality(ranks):
    
    rankQuality = []
    for rank in ranks:
        rankQuality.append(100-rank+1)
    
    return sum(rankQuality)


# 2
# Song values function that obtains the required feature values for a given song

def getSongValues(songName):
    
    featColumns = ['Popularity','Acousticness','Danceability','Energy','Instrumentalness','Loudness','Speechiness','Tempo','Valence']
    
    songProfile = df[df['Song Name'].str.contains(songName)]
    songProfile.reset_index(inplace=True,drop=True)

    songFeats = songProfile.filter(featColumns)
    songFeats = list(songFeats.loc[0])

    values = []
    for x in range(len(featColumns)):
        values.append(math.floor(scipy.stats.percentileofscore(df[featColumns[x]],songFeats[x])))
        
    return values


# 3
# Artist values function that obtains the mean of required feature values for a given artist

def getArtistValues(artist):
    
    featColumns = ['Popularity','Acousticness','Danceability','Energy','Instrumentalness','Loudness','Speechiness','Tempo','Valence']
    
    artistData = df[df['Artist: '+artist]==1][featColumns]
    artistData.reset_index(drop=True,inplace=True)

    values = []
    for idx in range(len(artistData)):
        songFeats = list(artistData.loc[idx])
        valuesSong = []
        for x in range(len(featColumns)):
            valuesSong.append(math.floor(scipy.stats.percentileofscore(df[featColumns[x]],songFeats[x])))
        values.append(valuesSong)

    return np.round(np.mean(values, axis=0)).astype(int)


# 4
# Genre values function that obtains the mean of required feature values for a given genre

def getGenreValues(genre):
    
    featColumns = ['Popularity','Acousticness','Danceability','Energy','Instrumentalness','Loudness','Speechiness','Tempo','Valence']
    
    genre = genre.lower()
    genreData = df[df['Genre: '+genre]==1][featColumns]
    genreData.reset_index(drop=True,inplace=True)

    values = []
    for idx in range(len(genreData)):
        genreFeats = list(genreData.loc[idx])
        valuesGenre = []
        for x in range(len(featColumns)):
            valuesGenre.append(math.floor(scipy.stats.percentileofscore(df[featColumns[x]],genreFeats[x])))
        values.append(valuesGenre)

    return np.round(np.mean(values, axis=0)).astype(int)


# ---------------------------------------------------------------------------------------------- #


# --- DEFINING REQUIRED PLOTTING FUNCTIONS ---

# 1
# Plot Artist function that plots the trends of a given artist

def plotArtist(artist):
    
    dfArtist = df[df['Artist: '+artist]==1]
    dfYearArtist = pd.DataFrame()
    dfYearArtist['Year'] = [year for year in range(1960,2022)]
    tempArtist = dfArtist.groupby('Year')['Rank'].apply(list).apply(quality)
    dfYearArtist = dfYearArtist.merge(tempArtist,left_on='Year',right_index=True,how='left')
    dfYearArtist.columns = ['Year','Hit Quality']
    dfYearArtist['Year'] = dfYearArtist['Year'].astype(int) 
    dfYearArtist.fillna(0,inplace=True)
        
    # Setting the color and linewidth of the spines/borders
    mpl.rc('axes',edgecolor=grey)
    mpl.rc('axes',linewidth='2')

    fig, ax = plt.subplots(figsize=(8,6))
    
    #Adding bg color and setting the grid
    fig.set_facecolor(bg_color_cas)
    ax.set_facecolor('w')
    ax.set_axisbelow(True)
    ax.grid(color=lightgrey, which='major',linestyle='--',alpha=1)    
    #Plotting
    ax.plot(dfYearArtist['Year'],dfYearArtist['Hit Quality'],'-',color=spotifyGreen,lw=4)
    # Setting the limits for x and y axes 
    minYear = min(dfYearArtist[dfYearArtist['Hit Quality']>0]['Year'])
    ax.set_xlim([minYear,2021])
    ax.set_xticks(np.arange(minYear,2021,(2021-minYear)/10))
    # Setting the x label as year for every subplot
    ax.set_xlabel('Year', fontsize=16, labelpad=10,fontproperties=robotoMed.prop, color='k')
    ax.set_ylabel('Hit Quality', fontsize=16, labelpad=10,fontproperties=robotoMed.prop, color='k')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    # Customizing the x and y ticklabels
    for ticklabel in ax.get_yticklabels():
        ticklabel.set_fontproperties(robotoMed.prop)
        ticklabel.set_fontsize(14)
    for ticklabel in ax.get_xticklabels():
        ticklabel.set_fontproperties(robotoMed.prop)
        ticklabel.set_fontsize(14)
    ax.tick_params(axis='both', which='major',labelcolor='k',length=0,color='#2b2b2b')
    
    return fig


# 2
# Plot Genre function that plots the trends of a given genre

def plotGenre(genre):
    
    genre = genre.lower()
    dfGenre = df[df['Genre: '+genre]==1]
    dfYearGenre = pd.DataFrame()
    dfYearGenre['Year'] = [year for year in range(1960,2022)]
    tempGenre = dfGenre.groupby('Year')['Rank'].apply(list).apply(quality)
    dfYearGenre = dfYearGenre.merge(tempGenre,left_on='Year',right_index=True,how='left')
    dfYearGenre.columns = ['Year','Hit Quality']
    dfYearGenre.fillna(0,inplace=True)

    # Setting the color and linewidth of the spines/borders
    mpl.rc('axes',edgecolor='grey')
    mpl.rc('axes',linewidth='2')

    fig,ax = plt.subplots(figsize=(8,6))
    
    #Adding bg color and setting the grid
    fig.set_facecolor(bg_color_cas)
    ax.set_facecolor('w')
    ax.set_axisbelow(True)
    ax.grid(color=lightgrey,which='major',linestyle='--',alpha=1)
    #Plotting
    ax.plot(dfYearGenre['Year'],dfYearGenre['Hit Quality'],'-',color=spotifyGreen,lw=4)
    # Setting the limits for x and y axes 
    ax.set_xlim([1960,2021])
    # Setting the x label as year for every subplot
    ax.set_xlabel('Year', fontsize=16, labelpad=10,fontproperties=robotoMed.prop, color='k')
    ax.set_ylabel('Hit Quality', fontsize=16, labelpad=10,fontproperties=robotoMed.prop, color='k')
    # Customizing the x and y ticklabels
    for ticklabel in ax.get_yticklabels():
        ticklabel.set_fontproperties(robotoMed.prop)
        ticklabel.set_fontsize(14)
    for ticklabel in ax.get_xticklabels():
        ticklabel.set_fontproperties(robotoMed.prop)
        ticklabel.set_fontsize(14)
    ax.tick_params(axis='both', which='major',labelcolor='k',length=0,color='#2b2b2b')

    return fig


# 3
# Pizza plot function that takes values and plots a pizza chart

def plotPizza(values):
    
    featColumns = ['Popularity','Acousticness','Danceability','Energy','Instrumentalness','Loudness','Speechiness','Tempo','Valence']
    slice_colors = [spotifyGreen]*9
    text_colors = ["w"]*9

    #Instantiate PyPizza class
    baker = PyPizza(
        params=featColumns,             
        background_color=bg_color_cas,     
        straight_line_color=grey,  
        straight_line_lw=2,             
        straight_line_ls='-',
        last_circle_color=grey,    
        last_circle_lw=7,               
        last_circle_ls='-',
        other_circle_lw=2,              
        other_circle_color=lightgrey,
        other_circle_ls='--',
        inner_circle_size=20            
    )

    #Plot pizza
    fig, ax = baker.make_pizza(
                                values,                          
                                figsize=(8, 8),                  
                                color_blank_space=["w"]*9, 
                                slice_colors=slice_colors,       
                                value_bck_colors=slice_colors,   
                                param_location=115,
                                blank_alpha=1,                 
                                kwargs_slices=dict(edgecolor="k", zorder=2, linewidth=2,alpha=.8,linestyle='-'),                               
                                kwargs_params=dict(color="k", fontsize=22, fontweight='bold',
                                                   va="center",fontproperties=robotoMed.prop),
                                kwargs_values=dict(color="k", fontsize=18,va='center',
                                                   zorder=3,fontproperties=robotoMed.prop,
                                                   bbox=dict(edgecolor="k",boxstyle="round,pad=0.2", lw=1.5))                              
                              )

    ax.patch.set_facecolor('None')
    fig.set_alpha = 0.0
    fig.patch.set_visible(False)
    
    return fig


# ---------------------------------------------------------------------------------------------- #

# --- RECOMMENDATION SYSTEM ---

# Functions needed for the getRecommendation function

# 1 Get embeddings for the user's preference
def embed_without_enc(liked_songs_idx):
    user_pref_embeddings =  embeddings_all_df[embeddings_all_df.index.isin(liked_songs_idx)]
    return user_pref_embeddings    

# 2 Get similarity of the user's chosen songs with the other songs in the database
def get_similarity_df(user_pref_embeddings):
    embeddings_popped = embeddings_all_df.drop(list(user_pref_embeddings.index))
    mean_embedding_user = np.mean(user_pref_embeddings.values, axis = 0)
    similarity_df = pd.DataFrame(cosine_similarity(X = embeddings_popped, Y = mean_embedding_user.reshape(1,-1),dense_output=True))
    similarity_df.sort_values(0, ascending = False, inplace = True)
    similarity_df.drop_duplicates(inplace = True)
    return similarity_df

# 3 Get recommended songs and their album art
def get_rec_df(rec_songs_idx):
    top10_df = df[df.index.isin(rec_songs_idx)]
    uri_list = top10_df.URI.values
    album_art_list = []
    for uri in uri_list:
        song = sp.track(uri)
        album_art = song['album']['images'][0]['url']
        album_art_list.append(album_art)
    top10_df['Album Cover Art'] = album_art_list
    return top10_df


# MAIN FUNCTION
# The getRecommendation function to get the recommendations based on the user's preference

def getRecommendations(user_df):
    
    liked_songs_idx = list(user_df.index)
    user_pref_embeddings = embed_without_enc(liked_songs_idx = liked_songs_idx)
    similarity_df = get_similarity_df(user_pref_embeddings = user_pref_embeddings)
    rec_songs_idx = list(similarity_df.index)[0:10]
    recs_df = get_rec_df(rec_songs_idx = rec_songs_idx)
    
    return recs_df