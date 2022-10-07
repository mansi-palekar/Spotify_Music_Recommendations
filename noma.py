import pandas as pd
import requests
import streamlit as st
from streamlit_lottie import st_lottie

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

# --- DATAFRAME ---
bb100 = pd.read_csv(r"C:\Users\mansi\ai & ml univ.ai\DS 1 - data sci basics\Billboards with Audio Features.csv")
        
# --- RECC SYSTEM ---

with st.container():
    st.title("Pick a song")
    left_col, center_col, right_col = st.columns([1,2,1])
    with center_col:
        st.selectbox("Search for the song's title", bb100["Song Name"].drop_duplicates()) 
        st.selectbox("Who's the artist of this song?", bb100["Artist Names"].drop_duplicates())
        #st.button("Recommend me", on_click=st.write("Making recommendations, please wait."))
        if st.button("Recommend me"):
            #recs = song_recommendation()
            st.subheader("Your song recommendations are:")
            
        