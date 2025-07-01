import random
import statistics
import movie_storage_sql as storage




def main_menu(menu_list):
    """This function displays the menu items and returns the user choice"""
    print(f"{'*' * 12} My Movie Database {'*' * 12}")
    for option in menu_list:
        print(option)
    print()
    choice = input("Enter choice (0-10): ")
    return choice


def command_list_movies():
    """This function lists all the movies from the database with their ratings and their
    release year"""
    movies_dict = storage.list_movies()
    total_of_movies =len(movies_dict)
    print(f"There are a total of {total_of_movies} movies.")
    for title, info in movies_dict.items():
        print(f"{title} ({info["year"]}) : {info["rating"]}")
    input("Press Enter to return to the menu...\n")


def command_add_movie():
    """Adds movies to the database with its rating and release year"""
    movies_dict = storage.list_movies()
    new_movie = input("Enter the movie title: ")
    new_movie = new_movie.title()
    if new_movie not in movies_dict:
        while True:
            try:
                    storage.add_movie(new_movie)
                    break
            except ValueError:
                continue
    else:
        print(f"{new_movie} already in list.")
    input("Press Enter to return to the menu...\n")


def command_delete_movie():
    """Deletes movie from the database if it exists"""
    movies_dict = storage.list_movies()
    movie_to_delete = input("Enter the title of the movie to delete: ")
    movie_to_delete = movie_to_delete.title()
    if movie_to_delete in movies_dict.keys():
        storage.delete_movie(movie_to_delete)
    else:
        print(f"{movie_to_delete} not currently in list.")
    input("Press Enter to return to the menu...\n")



def command_update_movie():
    """Updates existing movies in the dictionary with a new rating"""
    movies_dict = storage.list_movies()
    movie_to_update = input("Enter the title of the movie to update it's rating: ")
    search_list =[]
    for movie, info in movies_dict.items():
        search_list.append(movie.lower())
    if movie_to_update.lower() not in search_list:
        print(f"{movie_to_update} not currently in list.")
    else:
        try:
            new_rating = float(input(f"Enter the new rating between (0-10) for {movie_to_update}: "))
            storage.update_movie(movie_to_update.title(), new_rating)
            print(f"{movie_to_update} now has the rating {new_rating}")
        except KeyError:
            print(f"{movie_to_update}, needs capital letters at the beginning of the words, please try again.")
            movie_to_update = input("Enter the title of the movie to update it's rating: ")

    input("Press Enter to return to the menu...\n")


def command_show_stats():
    """gets the data from the database and displays the stats of the movies using the statistics
    module to find the average, median, and worst and best movies and printing them"""
    movies_dict = storage.list_movies()
    ratings = []
    for movie in movies_dict.keys():
        ratings.append(movies_dict[movie]["rating"])
    average_rating = statistics.mean(ratings) #the average value in the dict
    median_rating = statistics.median(ratings) # the middle value in the dict
    worst_movie_dict = {}
    best_movie_dict = {}
    worst_rating = min(ratings)
    best_rating = max(ratings)
    for movie, info in movies_dict.items():
        rating = info["rating"]
        if rating == worst_rating:
            worst_movie_dict[movie] = rating
    for movie, info in movies_dict.items():
        rating = info["rating"]
        if rating == best_rating:
            best_movie_dict[movie] = rating

    print(f"Average Rating: {average_rating:.2f}")
    print(f"Median Rating: {median_rating:.1f}")

    for best_movie, best_rating in best_movie_dict.items():
        print(f"Best Movie: {best_movie} with a rating of {best_rating}")
    for worst_movie, worst_rating in worst_movie_dict.items():
        print(f"Worst Movie: {worst_movie} with a rating of {worst_rating}")

    input("Press Enter to return to the menu...\n")


def command_random_movie():
    """Gets the data from the database and displays a random movie from the dictionary"""
    movies_dict = storage.list_movies()
    random_sample_movie, random_info = random.sample(list(movies_dict.items()), 1)[0]
    print(f"Your randomly selected movie is {random_sample_movie} ({random_info["year"]}) with a rating of {random_info["rating"]}.")
    input("Press Enter to return to the menu...\n")


def command_search_movie():
    """Gets the data from the database, uses user input to search for a movie in the
    dictionary and display the results if it exists"""
    movies_dict = storage.list_movies()
    while True:
        user_search = input("Enter movie you wish to search for: ").lower()
        search_results_dict = {}
        for movie, info in movies_dict.items():
            if user_search in movie.lower():
                search_results_dict[movie] = {}
                search_results_dict[movie]["rating"] = info["rating"]
                search_results_dict[movie]["year"] = info["year"]
        if search_results_dict:
            print("Did you mean...")
            for searched_movie, searched_info in search_results_dict.items():
                print(f"{searched_movie} ({searched_info["year"]}) : {searched_info["rating"]}")
            answer = input("Is that the movie you were looking for? (y/n): ").lower()
            if answer == "n":
                continue
            else:

                break
        else:
            print(f"Sorry, {user_search} not currently in list of movies, feel free to add it!")
            break
    input("Press Enter to return to the menu...\n")



def command_movie_sorted_by_rating():
    """Gets the data from the database then sorts the movies in the dictionary by the
    rating and displays them from highest to lowest"""

    movies_dict = storage.list_movies()
    sorted_movies = sorted(movies_dict.items(), key=lambda item: item[1]["rating"], reverse=True)
    for movie, info in sorted_movies:
        print(f"{movie}: {info["rating"]}")
    input("Press Enter to return to the menu...\n")


def command_movie_sorted_by_year_released():
    """Gets the data from the database sorts the movies in the dictionary by the rating and
    displays them from earliest to lastest, or latest to earliest """
    movies_dict = storage.list_movies()
    while True:
        order_choice = input("Would you like the movies to be shown oldest to newest? (y/n): ").lower()
        print()
        if order_choice in ("y", "n"):
            reverse_order = order_choice == "n"
            if reverse_order:
                print("Showing movies from newest to oldest release.\n")

            sorted_movies = sorted(movies_dict.items(), key= lambda item: item[1]["year"], reverse=reverse_order)
            for movie, info in sorted_movies:
                print(f"{movie}: {info["year"]}")
            break
        else:
            print("Please enter a valid choice.")

    input("Press Enter to return to the menu...\n")

def command_filter_movies():
    """Gets the data from the database then filters movies by minimum rating, start year, and end year
    as wished for by the user."""
    movies_dict = storage.list_movies()
    while True:
        min_rating_input = input("Enter the minimum rating of the movie: ").strip()
        start_year_input = input("Enter the year to start filtering from: ").strip()
        end_year_input = input("Enter the year to end filtering from: ").strip()

        try:
            minimum_rating = float(min_rating_input) if min_rating_input else 0.0
            start_year = int(start_year_input) if start_year_input else 1000
            end_year = int(end_year_input) if end_year_input else 5000
        except ValueError:
            print("Invalid Input! Please enter a number.")
            continue
        break

    filtered_movies = {}
    for movie, info in movies_dict.items():
        if minimum_rating <= info["rating"] and start_year <= info["year"] <= end_year:
            filtered_movies[movie] = {}
            filtered_movies[movie]["rating"] = info["rating"]
            filtered_movies[movie]["year"] = info["year"]

    for movie, info in filtered_movies.items():
        print(f"{movie}({info["year"]}): {info['rating']}")
    input("Press Enter to return to the menu...\n")


def serialize_data():
    """Gets all the data from the storage.list_movies and then serializes it for use in the
    index-html document """
    movies_dict = storage.list_movies()
    output = ''
    for movie, info in movies_dict.items():
        output += f"""
            <li>
                <div class="movie">
                    <img class="movie-poster" src="{info["poster"]}" alt="Poster of the movie {movie}">
                    <div class="movie-title">{movie}</div>
                    <div class ="movie-year">{info["year"]}</div>
                </div>
            </li>"""
    return output


def command_generate_website():
    """First calls upon the serialize_data function in order to generate the index.html
    to showcase the poster and title and year released of the database"""
    output = serialize_data()

    with open("_static/index_template.html", "r") as template:
        template = template.read()

    template = template.replace("__TEMPLATE_TITLE__", "Funky Fresh Films")
    template = template.replace("__TEMPLATE_MOVIE_GRID__", output)

    with open("index.html", "w") as index_html:
        index_html.write(template)

    print("Website generated! See index.html.")
    input("Press Enter to return to the menu...\n")


def main():
    menu_list = ["Main Menu", "0. Exit Program", "1. List movies", "2. Add movie",
                 "3. Delete movie", "4. Update movie", "5. Stats",
                 "6. Random movie", "7. Search movie", "8. Movies sorted by rating",
                 "9. Movies sorted by year released", "10. Filter movies", "11. Generate Website"]

    func_dict = {
        '1': command_list_movies,
        '2': command_add_movie,
        '3': command_delete_movie,
        '4': command_update_movie,
        '5': command_show_stats,
        '6': command_random_movie,
        '7': command_search_movie,
        '8': command_movie_sorted_by_rating,
        '9': command_movie_sorted_by_year_released,
        '10': command_filter_movies,
        '11': command_generate_website
    }
    while True:
        choice = main_menu(menu_list)
        if choice == '0':
            print("Exiting program")
            break
        elif choice not in func_dict.keys():
            print("Invalid choice, please try again")
        else:

            func_dict[choice]()


if __name__ == "__main__":
    main()
