import pandas as pd
import requests
import streamlit as st
from streamlit_lottie import st_lottie

from rec_eng_implementation import song_recommendations
from rec_eng_implementation import pizza_chart

# --- CONFIGURATION ---
st.set_page_config(page_title = "NOMA's Music Recommendation System", page_icon = ":notes:", layout = "wide")


# --- ANIMATION AND IMAGES ---

#Function to load lottie animations
def load_animation(url):
    req = requests.get(url)
    req.json()['op']=0
    return req.json()

#Lottie animation urls
animation1 = load_animation("https://assets4.lottiefiles.com/temp/lf20_ERpSsi.json")
animation2 = load_animation("https://assets6.lottiefiles.com/private_files/lf30_fjln45y5.json")
animation3 = load_animation("https://assets4.lottiefiles.com/packages/lf20_wcfkpodg.json")

#Background images
img1 = "https://images7.alphacoders.com/109/1093962.jpg" #spotify red hue
img2 = "https://www.nrj.be/build/images/test-format/1920x540--nrj_banner_marketing.jpg" #2women listening
img3 = "https://www.elicitmagazine.com/wp-content/uploads/2021/06/Spotify-Playlists-How-Do-They-Work.jpg" #spotify_genres

# --- WEBPAGE CODE ---

#Setting background image
page_bg_img = """
<style>
[data-testid="stAppViewContainer"]{
background-image: url("https://www.scdn.co/i/free/bubbles-dktp.svg");
background-repeat: no-repeat;
background-position: left;
background-size: 980px 700px;
}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

#Title and intro section

line1 = '<p style = "font-size: 20px;">This system, along with the website, has been created by the team <span style="font-size:120%"><b>Not a Modelling Agency</b></span> from Cohort 4 \nas part of the DS 1 Project.</p>'
line2 = '<p style = "font-size: 20px;">To try out the algorithm, pick a song from our database consisting of Billboard Hot 100 tracks from the last five decades and our \nsystem will analyse various attributes such as artist, genres, audio features, and more \nto recommend five songs that we hope you might like. &#129293;</p>'

with st.container():
    left_col, right_col = st.columns([1.9,1])
    with left_col:
        st.subheader("Not a Modelling Agency is proud to present,")
        st.title("A Spotify Music Recommendation System :headphones:")
        st.markdown(line1, unsafe_allow_html=True)
        st.markdown(line2, unsafe_allow_html=True)
    with right_col:
        #st_lottie(animation2, height = 570, width = 490)
        st_lottie(animation3, height = 570, width = 570)

# --- DATAFRAMES ---
df = pd.read_csv("Billboards with Audio Features + Genres, Artists OHE.csv")
        
# --- RECC SYSTEM ---


with st.container():
    st.title("Pick your five favourite songs")
    user_songs = st.multiselect("Search for the song's title", df["Song & Artist Names"].drop_duplicates())
    if st.button("Confirm Selection"):
        user_df = df[df['Song & Artist Names'].isin(user_songs)]
        recs_df = song_recommendations(user_df)
        
        st.subheader("Below are the profiles of your chosen songs, using which we'll analyse your music tastes..")
        cols = st.columns(5)
        for i in range(0,5):
            with cols[i]:
                st.pyplot(pizza_chart(user_df['Song Name'].values[i]))
                st.markdown(f"**Song:** {user_df['Song Name'].values[i]}")
                
        st.write("")
        st.write("")
        st.title("Based on your music taste, you might also like:")
        cols = st.columns(5)       
        for i in range(0,5):
            with cols[i]:
                st.image(recs_df['Album Cover Art'].values[i])
                rec_lines = f"""
                            <p>
                            <b> Song: </b> {recs_df['Song Name'].values[i]} <br>
                            <b> Artist: </b> {recs_df['Artist Names'].values[i]} <br>
                            <a href = {recs_df['Spotify Link'].values[i]}> <b>Listen on Spotify</b> <img alt="Spotify"
                            src = "https://1000logos.net/wp-content/uploads/2021/04/Spotify-logo.png"
                            width=42 height=25> </a>
                            </p>
                            """
                st.markdown(rec_lines, unsafe_allow_html = True)