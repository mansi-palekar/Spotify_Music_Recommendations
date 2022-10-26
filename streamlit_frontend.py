# --- IMPORTING DEPENDENCIES ---

import pandas as pd
import requests
import streamlit as st
import streamlit.components.v1 as components
from streamlit_lottie import st_lottie
from streamlit_backend import getRecommendations, getMoodPlaylist, quality, getSongValues, getArtistValues, getGenreValues, plotArtist, plotGenre, plotPizza

# --- LOADING REQUIRED DATAFRAMES ---

df = pd.read_csv("Billboards with Audio Features + Genres,Artists OHE (Final).csv", low_memory = False)
artists = pd.Series([i.split('Artist: ', 1)[1] for i in list(df.filter(regex='Artist: ').columns)])
genres = pd.Series([i.split('Genre: ', 1)[1].title() for i in list(df.filter(regex='Genre: ').columns)])

# --- LINKS FOR REQUIRED ANIMATION AND IMAGES ---

# animation html scripts
spotify_animation_html = """
<script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
<lottie-player src="https://assets10.lottiefiles.com/packages/lf20_a6hjf7nd.json"  background="transparent"  speed="1"  style="width: 110px; height: 110px;"  loop  autoplay></lottie-player> """
astro_animation_html = """
<script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
<lottie-player src="https://assets4.lottiefiles.com/packages/lf20_euaveaxu.json"  background="transparent"  speed="1"  style="width: 170px; height: 160px;"  loop  autoplay></lottie-player> """


# images
spotify_logo = "https://www.freepnglogos.com/uploads/spotify-logo-png/spotify-icon-black-17.png"
casette = 'https://www.scdn.co/i/500/cassette.svg'

# ---------------------------------------------------------------------------------------------- #

# --- PAGE CONFIGURATION ---

st.set_page_config(page_title = "NOMA's Spotify Music Recommendation System", page_icon = ":notes:", layout = "wide")

# Removing whitespace from the top of the page
st.markdown("""
<style>
.css-18e3th9 { padding-top: 0rem; padding-bottom: 10rem; padding-left: 5rem; padding-right: 5rem; }
.css-1d391kg { padding-top: 3.5rem; padding-right: 1rem; padding-bottom: 3.5rem; padding-left: 1rem; }
</style>""", unsafe_allow_html=True)

# Button config
m = st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: #ffffff;
    color:#000000;
}
div.stButton > button:hover {
    background-color: #1DDA63;
    color:#FFFFFF;
    }
</style>""", unsafe_allow_html=True)

# Select widget config
s_box = st.markdown("""
<style> div[data-baseweb="select"] > div {background-color: #ffffff; color:#000000;}
</style>""", unsafe_allow_html = True)

# ---------------------------------------------------------------------------------------------- #

# --- WEBPAGE CODE ---

# Setting background
page_bg = """
<style>
[data-testid="stAppViewContainer"]{
background-color: #9bf0e1;
background-repeat: no-repeat;
background-position: left;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# Title and intro section
# Heading
heading_animation = "<p style = 'font-size: 70px;'><b>Spotify Music Recommendation System</b></p>"
# Intro lines
intro_para = """
<p style = "font-size: 24px;">
This recommendation system, along with the website, has been created by the team <span style="font-size:120%"><b>Not a Modelling Agency</b></span>.
<br> <br>
To try out the algorithm, pick out five songs from our database which consists of <b> Billboard Hot 100 tracks</b> from the time period <b>1960 to 2021</b> and our system will analyse various attributes such as artist, artist's genres, audio features, and more to recommend you songs that we hope you might like. <br> <br>
Along with the recommendations, you also get to see the song and artist profiles of your selected tracks. These song profiles have been created using the features Spotify itself provides. You can find out more in depth about each feature <a href = {https://developer.spotify.com/discover/#:~:text=Audio%20Features%20%26%20Analysis,-Explore%20audio%20features&text=For%20more%20advanced%20use%20cases,Context%3A%20Liveness%2C%20Acousticness}> <i>here</i></a>.
</p>"""

# --- INTRODUCTION ---
with st.container():
    st.subheader("Not a Modelling Agency is proud to present,")
    left_col, right_col = st.columns([1, 9])
    with left_col:
        components.html(spotify_animation_html)
    with right_col:
        st.markdown(heading_animation, unsafe_allow_html = True)
        
with st.container():
    left_col, right_col = st.columns([1.4, 1])
    with left_col:
        st.markdown(intro_para, unsafe_allow_html = True)
    with right_col:
        st.image(casette, use_column_width = False)
        

# --- RECC SYSTEM ---

user_df = None

with st.container():
    st.title("Pick your five favourite songs :musical_note:") 
    st.subheader("Search for the song's title")
    user_songs = st.multiselect(label = "Search", options = df["Song and Artist"].drop_duplicates(), label_visibility = 'collapsed')
    if st.button("Confirm Selection"):
        
        if len(user_songs) < 5 or len(user_songs) > 5:
            st.error("Please select 5 songs", icon="⚠️")
            
        else:
            user_df = df[df["Song and Artist"].isin(user_songs)]
            recs_df = getRecommendations(user_df)
        
            st.subheader("Below are the profiles of your chosen songs, using which we'll analyse your preferences..")
        
            cols = st.columns(5)
            for i in range(0,5):
                with cols[i]:
                    st.pyplot(plotPizza(getSongValues(user_df['Song and Artist'].values[i])))
                    st.markdown(f"""<p align = 'center'> <b> Song: </b> {user_df['Song'].values[i]} <br>
                                <b> Artist: </b> {user_df['Artist'].values[i]} <br>
                                <a href = {'https://open.spotify.com/track/' + user_df['URI'].values[i].split(":")[2]}>
                                <img alt="Spotify" src = {spotify_logo} width=30 height=30><b>Listen on Spotify</b></a>
                                </p>""", 
                                unsafe_allow_html = True)
                         
            st.write("<br>", unsafe_allow_html = True)
        
            st.subheader("Based on your music taste, you might also like:")
           
            with st.container():
                cols = st.columns(5)       
                for i in range(0,5):
                       with cols[i]:
                            st.image(recs_df['Album Cover Art'].values[i], use_column_width = True)
                            st.markdown(f"""<p align = 'center'> <b> Song: </b> {recs_df['Song'].values[i]} <br>
                                <b> Artist: </b> {recs_df['Artist'].values[i]} <br>
                                <a href = {'https://open.spotify.com/track/' + recs_df['URI'].values[i].split(":")[2]}>
                                <img alt="Spotify" src = {spotify_logo} width=30 height=30><b>Listen on Spotify</b></a>
                                </p>""", 
                                unsafe_allow_html = True)
            with st.container():
                cols = st.columns(5)
                for i in range(0,5):
                    with cols[i]:
                        st.image(recs_df['Album Cover Art'].values[5+i], use_column_width = True)
                        st.markdown(f"""<p align = 'center'> <b> Song: </b> {recs_df['Song'].values[5+i]} <br>
                                    <b> Artist: </b> {recs_df['Artist'].values[5+i]} <br>
                                    <a href = {'https://open.spotify.com/track/' + recs_df['URI'].values[5+i].split(":")[2]}>
                                    <img alt="Spotify" src = {spotify_logo} width=30 height=30><b>Listen on Spotify</b></a>
                                    </p>""", 
                                    unsafe_allow_html = True)
            with st.container():
                left_col, right_col = st.columns([1, 7])
                with left_col:
                    components.html(astro_animation_html)
                with right_col:
                    st.markdown("<p style = 'font-size: 36px; font-weight: bold;'> <br> Sit back and stream or ..</p>""",
                                unsafe_allow_html = True)
                
                        
# --- ARTIST AND GENRE PROFILES ---        

st.title("Explore more")
line1 = """<p style = "font-size: 22px;"> 
Explore the profiles of your favourite artists and their genres by opting for an artist or an artist's genre. The resultant visualisations will show the trajectory of its popularity as well as how dominant various audio features are for the selected choice. Moreover, you can also listen to some of our mood playlists in the Playlists tab.
</p> """
st.markdown(line1, unsafe_allow_html = True)


# --- TAB CONFIG ---

listTabs = ["Artist", "Genre", "Playlists"]
tabs_font_css = st.markdown("""
<style> button[data-baseweb="tab"] {font-size: 26px; font-weight: 520; background-color: #ffffff; color: #000000;}
button[data-baseweb="tab"]:hover {font-size: 26px; font-weight: 520; background-color: #1DDA63; color:#FFFFFF;}
button[data-baseweb="tab"]:focus {font-size: 26px; font-weight: 520; background-color: #1DDA63; color:#FFFFFF;}
</style>""", unsafe_allow_html = True)

chosen_artist = None
chosen_genre = None
chosen_mood = None

with st.container():   
    
    tabs = st.tabs([s.center(21,"\u2001") for s in listTabs])
    
    # TAB 1 ARTIST PROFILE
    
    with tabs[0]:
        # Code to enable choosing an artist
        st.subheader("Choose an Artist")
        col1, col2 = st.columns([1.6, 1])
        with col1:
            user_artist = st.selectbox(label = "Search", options = artists, label_visibility = 'collapsed')     
        with col2:
            if st.button("Confirm Selection", key = 1):
                chosen_artist = user_artist
        
        # Profile
        if chosen_artist!= None:
            st.subheader(f"Artist Profile for {chosen_artist},")
            
            cols = st.columns([2.5, 1, 2.2])
            
            with cols[0]:
                st.markdown('<br>', unsafe_allow_html = True)
                st.markdown('<p align = "center" style = "font-size: 24px; font-weight: bold"> Popularity w.r.t. Time </p>', unsafe_allow_html = True)
                st.pyplot(plotArtist(chosen_artist))
                st.markdown("<p align = 'center' style = 'font-size: 20px;'> The Hit Quality is a metric that measures the quality of the ranks.<br>To elaborate, instead of determining the popularity of an artist by counting the no. of times they've appeared in the Billboard Hot 100, the hit quality metric will try to emphasize the correction of ranking by giving more weightage to the higher ranks and less importance to the lower ones. This will result in a more robust judgement of an artist's popularity. </p>", unsafe_allow_html = True)
                
            with cols[1]:
                st.write("")
                
            with cols[2]:
                st.markdown('<p align = "center" style = "font-size: 24px; font-weight: bold"> Mean Percentile Ranks <br> </p>', unsafe_allow_html = True)
                vals = getArtistValues(chosen_artist)
                st.pyplot(plotPizza(vals))
                st.markdown(f"<p align = 'center' style = 'font-size: 20px;'> A percentile rank indicates the percentage of scores in the frequency distribution that are less than that score. <br> In simple terms, a mean percentile rank of {vals[1]} for Acousticness for the artist {chosen_artist} indicates that {vals[1]}% of the songs in our database fall below the mean acousticness of the songs by the artist {chosen_artist}.</p>", unsafe_allow_html = True)
    
    # TAB 2 GENRE PROFILE
    
    with tabs[1]:
        
        # Code to enable choosing a genre
        st.subheader("Choose a Genre") 
        col1, col2 = st.columns([1.6, 1])
        with col1:
            user_genre = st.selectbox(label = "Search", options = genres, label_visibility = 'collapsed')    
        with col2:
            if st.button("Confirm Selection", key = 2):
                chosen_genre = user_genre 
                
        # Profile
        if chosen_genre!= None:
            st.subheader(f"Genre Profile for {chosen_genre},")
            
            cols = st.columns([2.5, 1, 2.2])
            
            with cols[0]:
                st.markdown('<br>', unsafe_allow_html = True)
                st.markdown('<p align = "center" style = "font-size: 24px; font-weight: bold"> Popularity w.r.t. Time </p>', unsafe_allow_html = True)
                st.pyplot(plotGenre(chosen_genre))
                st.markdown("<p align = 'center' style = 'font-size: 20px;'> The Hit Quality is a metric that measures the quality of the ranks.<br>To elaborate, instead of determining the popularity of an artist's genre by counting the no. of times it has appeared in the Billboard Hot 100, the hit quality metric will try to emphasize the correction of ranking by giving more weightage to the higher ranks and less importance to the lower ones. This will result in a more robust judgement of a genre's popularity. </p>", unsafe_allow_html = True)
                
            with cols[2]:
                st.markdown('<p align = "center" style = "font-size: 24px; font-weight: bold"> Mean Percentile Ranks <br> </p>', unsafe_allow_html = True)
                vals = getGenreValues(chosen_genre)
                st.pyplot(plotPizza(vals))
                st.markdown(f"<p align = 'center' style = 'font-size: 20px;'> A percentile rank indicates the percentage of scores in the frequency distribution that are less than that score. <br> In simple terms, a mean percentile rank of {vals[1]} for Acousticness for the {chosen_genre} genre indicates that {vals[1]}% of the songs in our database fall below the mean acousticness of the songs belonging to the {chosen_genre} genre.</p>", unsafe_allow_html = True)
         
        
        # TAB 3 PLAYLISTS
        
        with tabs[2]:
            moods = ["Trending songs", "Dance party", "Monday blues", "Energizing", "Positive vibes"]
                
            # Code to enable choosing a mood
            st.subheader("Choose a Mood") 
            col1, col2 = st.columns([1.6, 1])
            with col1:
                user_mood = st.selectbox(label = "Search", options = moods, label_visibility = 'collapsed')    
            with col2:
                if st.button("Confirm Selection", key = 3):
                    chosen_mood = user_mood 
                
            # Playlist display
            if chosen_mood!= None:
                
                mood_df = getMoodPlaylist(chosen_mood)
                
                st.subheader(f"Here's a {chosen_mood} playlist for you,")
                
                with st.container():
                    cols = st.columns(5)       
                    for i in range(0,5):
                        with cols[i]:
                            st.image(mood_df['Album Cover Art'].values[i], use_column_width = True)
                            st.markdown(f"""<p align = 'center'> <b> Song: </b> {mood_df['Song'].values[i]} <br>
                                        <b> Artist: </b> {mood_df['Artist'].values[i]} <br>
                                        <a href = {'https://open.spotify.com/track/' + mood_df['URI'].values[i].split(":")[2]}>
                                        <img alt="Spotify" src = {spotify_logo} width=30 height=30><b>Listen on Spotify</b></a>
                                        </p>""", 
                                        unsafe_allow_html = True)
                with st.container():
                    cols = st.columns(5)
                    for i in range(0,5):
                        with cols[i]:
                            st.image(mood_df['Album Cover Art'].values[5+i], use_column_width = True)
                            st.markdown(f"""<p align = 'center'> <b> Song: </b> {mood_df['Song'].values[5+i]} <br>
                                        <b> Artist: </b> {mood_df['Artist'].values[5+i]} <br>
                                        <a href = {'https://open.spotify.com/track/' + mood_df['URI'].values[5+i].split(":")[2]}>
                                        <img alt="Spotify" src = {spotify_logo} width=30 height=30><b>Listen on Spotify</b></a>
                                        </p>""", 
                                        unsafe_allow_html = True)
    

# ---------------------------------------------------------------------------------------------- #    

# --- FOOTER ---
footer="""<style>
.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: #9bf0e1;
color: black;
text-align: center;
}
</style>
<div class="footer">
<p>Developed with ❤ by Mansi, Chaitanya, Aditya, and Vrish</p>
</div>
"""
st.markdown(footer, unsafe_allow_html=True)

