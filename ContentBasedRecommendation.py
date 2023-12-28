import pandas as pd
import numpy as np
import tmdbv3api.exceptions
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from LoadData import MovieLens
from tmdbv3api import tmdb, Movie

class ContentBasedRecommender:
    movie=Movie()

    ml=MovieLens()
    def __init__ (self, movies, ratings):
        self.movies = movies
        self.ratings = ratings
        self.movie_data = pd.merge(ratings, movies[['movieId', 'genres']], on='movieId', how='left')

        # Preprocess genres for TF-IDF
        self.movies['genres'] = self.movies['genres'].fillna('')
        self.tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = self.calculate_tfidf()

    # function to calculate tfidf
    def calculate_tfidf(self):
        tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.movies['genres'])
        return tfidf_matrix


    # Function to get the movie id using the movie name
    def get_movie_id(self, movie_name):
       try:
           movie_id = self.movies[self.movies['title'] == movie_name]['movieId'].index[0]
           return movie_id
       except IndexError:
           print(f"Movie with title '{movie_name}' not found in the dataset.")
           return None

    # function to recommend movies
    def contentBasedRecommender(self, movie_name, number_of_recommendation, movie_mapping):
        # Get the movie ID based on the provided movie name
        movie_id = self.get_movie_id(movie_name)
        print({movie_id})
        if movie_id is None:
            return None
        # Calculate the similarity between the input movie and all other movies
        cosine_similarities = linear_kernel(self.tfidf_matrix[movie_id],self.tfidf_matrix).flatten()
        print("TFIDF matrix",pd.DataFrame(self.tfidf_matrix.toarray(), columns=self.tfidf_vectorizer.get_feature_names_out()))

        # Get the indices of movies with highest similarity scores
        similar_movies = list(enumerate(cosine_similarities))

        # Sort the movies based on similarity scores
        similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)

        # Exclude the input movie itself
        similar_movies = similar_movies[1:number_of_recommendation+1]

        # Get the movie indices and titles of recommended movies
        movie_indices = [index for index, _ in similar_movies]

        print("Selected Indices:", movie_indices)
        recommended_movies = self.movies.iloc[movie_indices][['movieId', 'title']]
        # similarity_scores = [score for _, score in similar_movies[:number_of_recommendation]]

        # get the movie posters and titles using the tmdb API
        movie_titles=[]
        tmdbIDs=[]
        posters=[]

        # Extract the recommended movie IDs for tmdbid mapping
        recommended_movie_ids = recommended_movies['movieId'].tolist()

        for movie_id in recommended_movie_ids:
            item_id=str(movie_id)
            TMDBID=movie_mapping.get(item_id, 'Unknown Movie')
            try:
            #     get movies details
                movies=self.movie.details(TMDBID)
                movie_titles.append(movies.title)
                tmdbIDs.append(TMDBID)
                posters.append(self.ml.fetch_poster(TMDBID))

            except tmdbv3api.exceptions.TMDbException as e:
                print(f"Error fetching movie details for TMDBID {TMDBID}: {e}")
                continue

        return movie_titles, tmdbIDs, posters
