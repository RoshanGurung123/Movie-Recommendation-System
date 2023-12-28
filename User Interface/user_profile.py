import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud
import seaborn as sns


# load the dataset for profiling
data=pd.read_csv('../Movielens dataset/ratings.csv')
movies_df=pd.read_csv('../Movielens dataset/movies.csv')

merged_df=pd.merge(data, movies_df, on='movieId')

def user_profile():
    st.title("User profile")

    # Sidebar for user selection
    user_id = st.selectbox('Select User ID:', data['userId'].unique())

    # def filter_user(user_id, data):
    selected_user_df=merged_df[merged_df['userId']==user_id]

    # Display user information and preferences
    st.subheader(f'User Profile for User ID {user_id}')

    # Display basic user information (customize based on your dataset)
    st.write(f"Total ratings given by the user: {selected_user_df['rating'].count()}")
    st.write(f"Average rating given by the user: {selected_user_df['rating'].mean()}")

    # Display user preferences or other relevant information
    # Extract and count genres from the user's rated movies
    all_genres = '|'.join(selected_user_df['genres']).split('|')
    genre_counts = pd.Series(all_genres).value_counts()

    # Display user genre preferences using a horizontal bar chart
    st.bar_chart(genre_counts)

    # Display a table of the user's rated movies
    st.subheader('Movies Rated by the User')
    top_10_movies = selected_user_df.sort_values(by='rating', ascending=False).head(10)
    st.table(top_10_movies[['movieId', 'title', 'rating', 'genres']])
