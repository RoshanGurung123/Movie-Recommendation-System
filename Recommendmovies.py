from CFUserBasedExecute import UserBasedCF
from LoadData import MovieLens
from tmdbv3api import TMDb, Movie
from CFUserBasedExecute import UserBasedCF

class RecommendMovies:

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

            # get movie details
            movies = movie.details(TMDBID)

            movie_titles.append(movies.title)
            predicted_ratings.append(recommendation.est)
            tmdbIDs.append(TMDBID)
            posters.append(ml.fetch_poster(TMDBID))

        return movie_titles, predicted_ratings, tmdbIDs, posters