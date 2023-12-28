from CFUserBasedExecute import UserBasedCF
from LoadData import MovieLens
from tmdbv3api import TMDb, Movie
from CFUserBasedExecute import UserBasedCF
import pandas as pd

class RecommendMovies:
    def content_based_recommendation (ratingsdf,movie_mapping, number_movies=20):
        movie = Movie()

        # Create an instance of the MovieLens class
        ml = MovieLens()

        #     calculate the movie popularity to show for new user based on number of ratings
        movie_popularity = ratingsdf.groupby('movieId')['rating'].count().reset_index(name='popularity')

        # Sort by popularity in descending order
        movie_popularity = movie_popularity.sort_values(by='popularity', ascending=False)

        # Display the top N popular movies
        recommended_movies = movie_popularity['movieId'].head(number_movies).tolist()

        print("Type of recommended_movies:", type(recommended_movies))
        print("Recommended Movies:", recommended_movies)

        movie_titles=[]
        posters=[]
        tmdbIds=[]

        for recommendation in recommended_movies:
            movie_id=recommendation
            print("Movie id", movie_id)
            tmdbId=movie_mapping.get(str(movie_id),'Unknown ID')
            print("Content TMDBID",tmdbId)

            movies = movie.details(tmdbId)

            movie_titles.append(movies.title)
            tmdbIds.append(tmdbId)
            posters.append(ml.fetch_poster(tmdbId))


        return movie_titles, tmdbIds, posters

    # function to recommend movies
    def recommend_movies (model, no_movies, user_id, all_items, movie_mapping):

        # declare tmdb movie api
        movie=Movie()

        # Create an instance of the MovieLens class
        ml=MovieLens()

        # calling trainTestSplit function from LoadDatamodule
        trainset, testset, all_TrainItems=ml.trainTestSplit()
        # Get the list of items rated by the specific user
        rated_items_by_user = [item for item, _ in trainset.ur[trainset.to_inner_uid(user_id)]]

        # Get the list of items not rated by the user
        items_not_rated_by_user = list(set(all_TrainItems) - set(rated_items_by_user))

        # Make predictions for the items not rated by the user
        item_predictions = [model.predict(user_id, item_id) for item_id in items_not_rated_by_user]

        # Sort the predictions by estimated rating
        sorted_predictions = sorted(item_predictions, key=lambda x: x.est, reverse=True)

        # Get the top N recommendations
        top_n_recommendations = sorted_predictions[:no_movies]

        movie_titles = []
        predicted_ratings = []
        tmdbIDs = []
        posters = []

        for recommendation in top_n_recommendations:
            item_id = str(recommendation.iid)
            movie_title = movie_mapping.get(item_id, 'Unknown Movie')
            TMDBID = movie_mapping.get(item_id, 'Unknown ID')
            print("Movie id",item_id)
            print("TMDB ID", TMDBID)

            # get movie details
            movies = movie.details(TMDBID)

            movie_titles.append(movies.title)
            predicted_ratings.append(recommendation.est)
            tmdbIDs.append(TMDBID)
            posters.append(ml.fetch_poster(TMDBID))

        return movie_titles, predicted_ratings, tmdbIDs, posters