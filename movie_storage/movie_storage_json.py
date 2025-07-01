import json


def get_movies():
    """
    Returns a dictionary of dictionaries that
    contains the movies information in the database.

    The function loads the information from the JSON
    file and returns the data.

    For example, the function may return:
    {
      "Titanic": {
        "rating": 9,
        "year": 1999
      },
      "..." {
        ...
      },
    }
    """
    with open('movies_dict.json', 'r') as json_file:
        movies_dict = json.load(json_file)

    return movies_dict


def save_movies(movies):
    """
    Gets all your movies as an argument and saves them to the JSON file.
    """
    with open('movies_dict.json', 'w') as json_file:
        json.dump(movies, json_file)



def add_movie(title, year, rating):
    """
    Adds a movie to the movies database.
    Loads the information from the JSON file, add the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movie_dict = get_movies()
    movie_dict[title] = {}
    movie_dict[title]['rating'] = rating
    movie_dict[title]['year_released'] = year
    save_movies(movie_dict)


def delete_movie(title):
    """
    Deletes a movie from the movies database.
    Loads the information from the JSON file, deletes the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movie_dict = get_movies()
    del movie_dict[title]
    save_movies(movie_dict)


def update_movie(title, rating):
    """
    Updates a movie from the movies database.
    Loads the information from the JSON file, updates the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movie_dict = get_movies()
    movie_dict[title]['rating'] = rating
    save_movies(movie_dict)
