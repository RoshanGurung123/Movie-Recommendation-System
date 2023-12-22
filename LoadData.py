# import necessary libraries
import pandas as pd
from tmdbv3api import TMDb, Movie
from surprise import Reader, Dataset
from surprise.model_selection import train_test_split



class MovieLens:
    moviesdf = pd.read_csv('Movielens dataset/movies.csv')
    ratingsdf = pd.read_csv('Movielens dataset/ratings.csv')
    linksdf = pd.read_csv('Movielens dataset/links.csv')

    # setup tmdb api
    tmdb = TMDb()
    tmdb.api_key = '9b799ab26d05d3bfc18975a3607bcfa9'
    movie = Movie()

# function to  load data
    def load_data(self):
        reader= Reader(rating_scale=(1,5))
        data=Dataset.load_from_df(self.ratingsdf[['userId', 'movieId', 'rating']], reader)
        return data

    # function to return merged data
    def merge_data(self):
        final_moviedf=self.moviesdf.merge(self.linksdf, on='movieId')
        movie_mapping=dict(zip(final_moviedf['movieId'].astype(str), final_moviedf['tmdbId']))
        # Extract the names of all movies
        all_movie_names = final_moviedf['title'].tolist()
        return movie_mapping, all_movie_names

    # Function to fetch poster
    def fetch_poster (self, movie_id):
        movie_details = self.movie.details(movie_id)
        poster_path = movie_details.poster_path
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path

    def trainTestSplit(self):
        data=self.load_data()
        trainset, testset =train_test_split(data, test_size=0.25, random_state=42 )
        # taking all trainset data
        all_trainItems=trainset.all_items()
        return trainset, testset, all_trainItems

