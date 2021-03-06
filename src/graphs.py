from api.movie_api import MovieAPI
from api.user_api import UserAPI
from api.rating_api import RatingAPI

import pandas as pd
from matplotlib import pyplot as plt


users: list = []
genres: list = []
ratings: list = []

usersGenresDf = pd.DataFrame()


def loadUsers(users: list) -> None:
    users_data: dict = UserAPI().getAllUsers()

    for user in users_data.get("users"):
        users.append({"email": user.get("email"), "favGenres": user.get("favGenres")})


def loadGenres(genres: list) -> None:
    genres_data: dict = MovieAPI().getMovieGenres()

    for genre in genres_data.get("genres"):
        genres.append(genre.get("name"))


def loadRatings(ratings: list) -> None:
    ratings_data: dict = RatingAPI().getAllRatings()

    for rating in ratings_data.get("ratings"):
        user_ratings: list = []
        for user_rate in rating.get("ratings"):
            user_ratings.append(user_rate.get("userRate"))

        ratings.append({"movieId": rating.get("movieId"), "ratings": user_ratings})


loadUsers(users)
loadGenres(genres)
loadRatings(ratings)


def createUsersGenresTable(users: list, genres: list, dataframe: pd.DataFrame) -> None:
    for genre in genres:
        column_data: list = []
        for user in users:
            if genre in user.get("favGenres"):
                column_data.append(1)
            else:
                column_data.append(0)
                
        dataframe[genre] = column_data


createUsersGenresTable(users, genres, usersGenresDf)


def createCharts(dataframe: pd.DataFrame):
    data: dict = {}
    
    for column in dataframe.columns:
        if 1 in dataframe[column].value_counts().keys().tolist():
            data[column] = dataframe[column].value_counts()[1]

    plt.subplot(1, 2, 1)
    plt.pie(data.values(), labels=data.keys(), autopct="%1.1f%%", startangle=10, wedgeprops={"edgecolor": "white"})
    plt.title("What our users like?")

    x_axis: list = []
    y_axis: list = []
    for rating in ratings:
        y_axis.append(str(rating.get("movieId")))
        x_axis.append(sum(rating.get("ratings")) / len(rating.get("ratings")))
    
    plt.subplot(1, 2, 2)
    plt.barh(y_axis, x_axis)
    plt.title("Ratings")
    plt.xlabel("Rating")
    plt.ylabel("Movie ID")
    plt.show()


createCharts(usersGenresDf)