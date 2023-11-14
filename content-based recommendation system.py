from surprise import AlgoBase, Dataset, Reader
from surprise.model_selection import train_test_split
# from MovieLens import MovieLens
import math

class ContentBasedRecommender(AlgoBase):

    ratings='ratings.csv'
    moviesdf='movies.csv'
    def __init__(self):
        AlgoBase.__init__(self)

    def fit(self, trainset):
        AlgoBase.fit(self, trainset)

        # Load movie genres
        ml = MovieLens()
        self.genres = ml.getGenres()

        # Compute item similarity matrix based on content attributes
        self.similarities = {}

        for movie1 in self.genres.keys():
            self.similarities[movie1] = {}
            for movie2 in self.genres.keys():
                if movie1 != movie2:
                    genreSimilarity = self.computeGenreSimilarity(movie1, movie2)
                    self.similarities[movie1][movie2] = genreSimilarity

        return self

    def computeGenreSimilarity(self, movie1, movie2):
        genres1 = self.genres[movie1]
        genres2 = self.genres[movie2]
        sumxx, sumxy, sumyy = 0, 0, 0

        for genre in genres1:
            if genre in genres2:
                sumxx += 1
                sumyy += 1
                sumxy += 1

        if sumxx == 0 or sumyy == 0:
            return 0

        return sumxy / math.sqrt(sumxx * sumyy)

    def recommend_similar_movies(self, movie_name, top_n=10):
        # Find the movie ID based on the provided movie name
        movieID = ml.getMovieID(movie_name)

        if movieID in self.genres:
            # Build a list of similar movies
            neighbors = []
            for movie, similarity in self.similarities[movieID].items():
                neighbors.append((movie, similarity))

            # Extract the top-N most-similar movies
            top_neighbors = sorted(neighbors, key=lambda x: x[1], reverse=True)[:top_n]

            # Get the names of the top-N recommended movies
            recommended_movies = [ml.getMovieName(neighbor[0]) for neighbor in top_neighbors]

            return recommended_movies
        else:
            return []

# Load the MovieLens dataset
reader = Reader(line_format='user item rating timestamp', sep=',', skip_lines=1)
data = Dataset.load_from_file(ContentBasedRecommender.ratings, reader=reader)
trainset, testset = train_test_split(data, test_size=0.2, random_state=42)

# Create and train the content-based recommender
content_based_recommender = ContentBasedRecommender()
content_based_recommender.fit(trainset)

# Get user input for a movie name
user_input_movie = input("Enter the name of a movie: ")

# Get and display recommendations based on the user input
recommendations = content_based_recommender.recommend_similar_movies(user_input_movie)
if recommendations:
    print(f"Recommended movies similar to '{user_input_movie}':")
    for idx, movie in enumerate(recommendations, start=1):
        print(f"{idx}. {movie}")
else:
    print(f"No recommendations found for '{user_input_movie}'.")
