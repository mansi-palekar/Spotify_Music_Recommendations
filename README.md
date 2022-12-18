# Spotify Music Recommendations

![last commit](https://img.shields.io/github/last-commit/meraxes-99/Spotify_Music_Recommendations)
![repo size](https://img.shields.io/github/repo-size/meraxes-99/Spotify_Music_Recommendations)

[![Watch the video](https://drive.google.com/u/0/uc?id=1eoFOnI-6eEU3UwfIcwy3CknXHVqNKjYq&export=download)](https://youtu.be/gJBP81oExrA)

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

#

How to run the project:
1. Fork the repository to local machine
2. Install Python 3.10 and install all additional dependencies in `requirements.txt` using the command `pip install -r ./requirements.txt`.
3. Run the Jupyter notebook from the terminal using the command `python -m jupyterlab`.
4. Run the Streamlit app from the terminal using the command `streamlit run streamlit_frontend.py && streamlit run streamlit_backend.py`.
5. The Streamlit app will be hosted on `localhost:8501`.
