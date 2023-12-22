import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

class ContentBasedRecommender:

    def __init__ (self, movies, ratings):
        self.movies = movies
        self.ratings = ratings
        self.movie_data = pd.merge(ratings, movies[['movieId', 'genres']], on='movieId', how='left')

        # Preprocess genres for TF-IDF
        self.movie_data['genres'] = self.movie_data['genres'].fillna('')
        self.tfidf_matrix = self.calculate_tfidf()

    # function to calculate tfidf
    def calculate_tfidf(self):
        tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf_vectorizer.fit_transform(self.movie_data['genres'])
        return tfidf_matrix


    def get_movie_id(self, movie_name):
       try:
           movie_id = self.movies[self.movies['title'] == movie_name]['movieId'].values[0]
           return movie_id
       except IndexError:
           print(f"Movie with title '{movie_name}' not found in the dataset.")
           return None

    # function to recommend movies
    def contentBasedRecommender(self, movie_name, number_of_recommendation=5):
        # Get the movie ID based on the provided movie name
        movie_id = self.get_movie_id(movie_name)
        print({movie_id})
        if movie_id is None:
            return None
        # Calculate the similarity between the input movie and all other movies
        cosine_similarities = linear_kernel(self.tfidf_matrix, self.tfidf_matrix[movie_id])

        # Get the indices of movies with highest similarity scores
        similar_movies = list(enumerate(cosine_similarities))

        # Sort the movies based on similarity scores
        similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)

        # Exclude the input movie itself
        similar_movies = similar_movies[1:]

        # Get the movie indices and titles of recommended movies
        movie_indices = [index for index, _ in similar_movies[:number_of_recommendation]]
        recommended_movies = self.movies.iloc[movie_indices][['movieId', 'title']]
        similarity_scores = [score for _, score in similar_movies[:number_of_recommendation]]

        return recommended_movies, similarity_scores

# Load MovieLens data
movies = pd.read_csv('Movielens dataset/movies.csv')
ratings = pd.read_csv('Movielens dataset/ratings.csv')

# Create a ContentBasedRecommender instance
content_based_recommender = ContentBasedRecommender(movies, ratings)

# Example: Recommend movies similar to the movie with name 'Toy Story (1995)'
movie_name_to_recommend = 'Jumanji (1995)'
recommended_movies, similarity_scores = content_based_recommender.contentBasedRecommender(movie_name_to_recommend)

# Display the recommended movies and similarity scores
if recommended_movies is not None:
    print(f"Movies similar to '{movie_name_to_recommend}':")
    for movie, score in zip(recommended_movies.itertuples(), similarity_scores):
        print(f"{movie.title} (Movie ID: {movie.movieId}) - Similarity Score: {score}")
