# Spotify Music Recommendations

A recommender system, or a recommendation system, is a type of filtering system that seeks to predict the “rating” or “preference” a user would give to an item.

Recommender systems are typically classified into the following categories:

- Content-based filtering
- Collaborative filtering
- Hybrid systems

This project uses content-based filtering to make music recommendations to the user after receiving five songs as per their preference.

#

The aim of this project is to:

1) Acquire the metadata, audio features data, and lyrics of Billboard Hot 100 (henceforth referred as BBHOT100) tracks for each year in the time period 1960 to 2021. This is accomplished by web scraping and Spotify API.
2) Perform extensive exploratory data analysis on the processed BBHOT100 dataset to derive insights and see how music preferences have evolved over time.
3) Generate a content-based music recommendation system based on sparse overcomplete autoencoders and deploy the system on Streamlit using Streamlit Cloud.
4) Develop a XGBoost model to predict rank of a track and further study it using SHAP values to increase transparency and interpretability of the model.

#

The main notebook of the repository is titled `Billboard Hot 100 Analysis`. It contains data collection, data processing, EDA, construction of the recommendation system and the rank prediction model.
The remaining files in the repo are used for streamlit deployment.

#

Link to the Streamlit website: https://meraxes-99-spotify-music-recommendati-streamlit-frontend-ceca43.streamlitapp.com/
