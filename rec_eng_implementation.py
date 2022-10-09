import pandas as pd
import numpy as np
import math
import scipy
import matplotlib.pyplot as plt
import seaborn as sns
from mplsoccer import PyPizza, FontManager
import matplotlib.patheffects as path_effects

# FONTS
robotoBold = FontManager(('https://github.com/Chaitanya98/Football-Analytics/blob/main/Barcalytix/Fonts/GothamBold.ttf?raw=true'))
robotoMed = FontManager(('https://github.com/Chaitanya98/Football-Analytics/blob/main/Barcalytix/Fonts/GothamMedium.ttf?raw=true'))

# Loading the main dataframe
df = pd.read_csv("Billboards with Audio Features + Genres, Artists OHE.csv")

# Loading the given songs dataframe
user_df = df.iloc[4000:4005]

# Loading the rec songs dataframe
rec_df = df.iloc[5000:5005]

def song_recommendations(user_df):
    return rec_df

# PIZZA CHART

def pizza_chart(song_name):
    featColumns = ['Popularity','Acousticness','Danceability','Energy','Instrumentalness','Loudness','Speechiness','Tempo','Valence']
    dfPizza = df[['Song Name','Artist Names (Str)']+featColumns]

    songName = song_name
    songProfile = dfPizza[dfPizza['Song Name'].str.contains(songName)]
    songProfile.reset_index(inplace=True,drop=True)

    songFeats = songProfile.filter(featColumns)
    songFeats = list(songFeats.loc[0])

    values = []
    for x in range(len(featColumns)):
        values.append(math.floor(scipy.stats.percentileofscore(dfPizza[featColumns[x]],songFeats[x])))

    def path_effect_stroke(**kwargs):
        return [path_effects.Stroke(**kwargs), path_effects.Normal()]

    spotifyGreen = '#1dda63'
    bg_color = "#6f0fdf"

    slice_colors = [bg_color]*9
    text_colors = ["w"]*9

    # instantiate PyPizza class
    baker = PyPizza(
        params=featColumns,                  # list of parameters
        background_color="#181818",     # background color
        straight_line_color="#bdbdbd",  # color for straight lines
        straight_line_lw=3,             # linewidth for straight lines
        straight_line_ls='-',
        last_circle_color="#bdbdbd",    # color for last line
        last_circle_lw=7,               # linewidth of last circle
        last_circle_ls='-',
        other_circle_lw=2,              # linewidth for other circles
        other_circle_color='#bdbdbd',
        other_circle_ls='--',
        inner_circle_size=20            # size of inner circle
    )

    pe1 = path_effect_stroke(linewidth=2, foreground="k")
    pe2 = path_effect_stroke(linewidth=2, foreground="w")

    # plot pizza
    fig, ax = baker.make_pizza(
        values,                          # list of values
        figsize=(8, 8),                # adjust the figsize according to your need
        color_blank_space=["#181818"]*9,        # use the same color to fill blank space
        slice_colors=slice_colors,       # color for individual slices
        # color for the value-text
        value_bck_colors=slice_colors,   # color for the blank spaces
        param_location=110,
        blank_alpha=0.4,                 # alpha for blank-space colors
    
    
        kwargs_slices=dict(
            edgecolor="w", zorder=2, linewidth=3,alpha=.9,linestyle='-'
        ),                               # values to be used when plotting slices
        kwargs_params=dict(
            color="w", fontsize=18, fontweight='bold',path_effects=pe1,
            va="center",fontproperties=robotoMed.prop
        ),                               # values to be used when adding parameter labels
        kwargs_values=dict(
            color="w", fontsize=16,path_effects=pe1,va='center',
            zorder=3,fontproperties=robotoMed.prop,
            bbox=dict(
                edgecolor="w",boxstyle="round,pad=0.2", lw=2.5
            )
        )                                # values to be used when adding parameter-values labels
    )
    
    return fig
