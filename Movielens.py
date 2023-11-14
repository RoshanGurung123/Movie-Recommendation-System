import os
import csv
import re
from collections import defaultdict
from surprise import Dataset, Reader

class MovieLens:
    def __init__(self, ratings_path='Movielens dataset/ratings.csv', movies_path='Movielens dataset/movies.csv'):
        self.ratings_path = ratings_path
        self.movies_path = movies_path
        self.movieID_to_name = {}
        self.name_to_movieID = {}

    def load_movie_lens_latest_small(self):
        # Look for files relative to the directory we are running from
        os.chdir(os.path.dirname(__file__))

        # Load ratings dataset
        reader = Reader(line_format='user item rating timestamp', sep=',', skip_lines=1)
        ratings_dataset = Dataset.load_from_file(self.ratings_path, reader=reader)

        # Load movie names and IDs
        with open(self.movies_path, newline='', encoding='ISO-8859-1') as csvfile:
            movie_reader = csv.reader(csvfile)
            next(movie_reader)  # Skip header line
            for row in movie_reader:
                movie_id = int(row[0])
                movie_name = row[1]
                self.movieID_to_name[movie_id] = movie_name
                self.name_to_movieID[movie_name] = movie_id

        return ratings_dataset

    def get_user_ratings(self, user):
        user_ratings = []
        hit_user = False
        with open(self.ratings_path, newline='') as csvfile:
            rating_reader = csv.reader(csvfile)
            next(rating_reader)
            for row in rating_reader:
                user_id = int(row[0])
                if user == user_id:
                    movie_id = int(row[1])
                    rating = float(row[2])
                    user_ratings.append((movie_id, rating))
                    hit_user = True
                if hit_user and user != user_id:
                    break

        return user_ratings

    def get_popularity_ranks(self):
        ratings = defaultdict(int)
        rankings = defaultdict(int)
        with open(self.ratings_path, newline='') as csvfile:
            rating_reader = csv.reader(csvfile)
            next(rating_reader)
            for row in rating_reader:
                movie_id = int(row[1])
                ratings[movie_id] += 1
        rank = 1
        for movie_id, rating_count in sorted(ratings.items(), key=lambda x: x[1], reverse=True):
            rankings[movie_id] = rank
            rank += 1
        return rankings

    def get_genres(self):
        genres = defaultdict(list)
        genre_ids = {}
        max_genre_id = 0
        with open(self.movies_path, newline='', encoding='ISO-8859-1') as csvfile:
            movie_reader = csv.reader(csvfile)
            next(movie_reader)  # Skip header line
            for row in movie_reader:
                movie_id = int(row[0])
                genre_list = row[2].split('|')
                genre_id_list = []
                for genre in genre_list:
                    if genre in genre_ids:
                        genre_id = genre_ids[genre]
                    else:
                        genre_id = max_genre_id
                        genre_ids[genre] = genre_id
                        max_genre_id += 1
                    genre_id_list.append(genre_id)
                genres[movie_id] = genre_id_list

        # Convert integer-encoded genre lists to bitfields
        for movie_id, genre_id_list in genres.items():
            bitfield = [0] * max_genre_id
            for genre_id in genre_id_list:
                bitfield[genre_id] = 1
            genres[movie_id] = bitfield

        return genres

    def get_years(self):
        p = re.compile(r"(?:\((\d{4})\))?\s*$")
        years = defaultdict(int)
        with open(self.movies_path, newline='', encoding='ISO-8859-1') as csvfile:
            movie_reader = csv.reader(csvfile)
            next(movie_reader)
            for row in movie_reader:
                movie_id = int(row[0])
                title = row[1]
                m = p.search(title)
                year = m.group(1)
                if year:
                    years[movie_id] = int(year)
        return years

    def get_mise_en_scene(self):
        mes = defaultdict(list)
        with open("LLVisualFeatures13K_Log.csv", newline='') as csvfile:
            mes_reader = csv.reader(csvfile)
            next(mes_reader)
            for row in mes_reader:
                movie_id = int(row[0])
                avg_shot_length = float(row[1])
                mean_color_variance = float(row[2])
                stddev_color_variance = float(row[3])
                mean_motion = float(row[4])
                stddev_motion = float(row[5])
                mean_lighting_key = float(row[6])
                num_shots = float(row[7])
                mes[movie_id] = [avg_shot_length, mean_color_variance, stddev_color_variance,
                                 mean_motion, stddev_motion, mean_lighting_key, num_shots]
        return mes

    def get_movie_name(self, movie_id):
        return self.movieID_to_name.get(movie_id, "")

    def get_movie_id(self, movie_name):
        return self.name_to_movieID.get(movie_name, 0)
