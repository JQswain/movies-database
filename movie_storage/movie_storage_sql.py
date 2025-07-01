from sqlalchemy import create_engine, text
import requests

import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("API_KEY")
API_URL = "https://www.omdbapi.com/?"
DB_URL = "sqlite:///movies.db"

engine = create_engine(DB_URL, echo=False)

with engine.connect() as connection:
    connection.execute(text("""
    CREATE TABLE IF NOT EXISTS movies ( 
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT UNIQUE NOT NULL,
        year INTEGER NOT NULL,
        rating REAL NOT NULL,
        poster TEXT NOT NULL
        )
                            """))
    connection.commit()


def list_movies():
    """Retrieve all movies from the database."""
    with engine.connect() as connection:
        result = connection.execute(text("SELECT title, year, rating, poster FROM movies"))
        movies = result.fetchall()
    return {row[0]: {"year": row[1], "rating": row[2], "poster": row[3]} for row in movies}


def add_movie(title):
    """connects to the API OmDb to get info on the movie,
    then adds the new movie to the database."""

    try:
        response = requests.get(f"{API_URL}apikey={API_KEY}&t={title}")
        response.raise_for_status()
        movie_data = response.json()

        if movie_data.get("Response") == "False":
            print(f"{title} is not available")
            return

        movie_title = movie_data["Title"]
        movie_year = movie_data["Year"]
        movie_rating = movie_data["Ratings"][0]["Value"][0:3]
        movie_poster = movie_data["Poster"]

    except requests.exceptions.RequestException as req_err:
        print(f"Error fetching products: {req_err}")
        return
    except KeyError as error:
        print(f"{title} not found due to missing key: {error}")
        return

    with engine.connect() as connection:
        try:
            connection.execute(text("INSERT INTO movies (title, year, rating, poster) VALUES (:title, :year, :rating, :poster)"),
            ({"title": movie_title, "year": movie_year, "rating": movie_rating, "poster": movie_poster}))
            connection.commit()
            print(f"Movie '{title}' added successfully.")
        except Exception as e:
            print(f"Error: {e}")


def delete_movie(title):
    """Delete a movie from the database."""
    with engine.connect() as connection:
        try:
            connection.execute(text("DELETE FROM movies WHERE title = :title"),
                            {"title": title})
            connection.commit()
            print(f"Movie '{title}' deleted successfully.")
        except Exception as e:
            print(f"Error: {e}")


def update_movie(title, rating):
    """Update a movie from the database."""
    with engine.connect() as connection:
        try:
            search_result = connection.execute(text("SELECT * FROM movies WHERE title = :title;"),
                               {"title": title})
            if search_result.first() is None:
                print(f"Movie '{title}' not found.")
            else:
                connection.execute(text("UPDATE movies SET title = :title, rating = :rating WHERE title = :title;"),
                                   {"title": title, "rating": rating})
                connection.commit()
                print(f"Movie '{title}' updated successfully.")
        except Exception as e:
            print(f"Error: {e}")
