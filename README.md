# movies-database
A project that combines: python, api, html and sql to create a new movie databse using user input, and information saerched from the OMDb API.
It cann then be used to generate an html page with the information sourced and showcase the poster images, title and year released for the movies added to the "Funky Fresh Films" Database.

## Installation
to install simply clone this repositiory to your own computer and get an individual API Key.
An individual API Key is availble from the OMDb website for free by submitting an email address, and can then be added to a .env file for safety.
All required libraries and modules are listed in the requirements text, but in short this proram uses sqlalchemy for the sql queries, requests for using the API, the os module and dotenv to conceal the API key and access it for the program. 


## Usage
This program starts empty and movies must be added by title and the information gathered using the API, you can then view the movies in the database, ask for a random movie, see the average and min/max ratings for the database search for movies that were added and geta  random movei from the database.
All of this through a simple command Line interface. 
An html can be gebnerated from the individually made databse to view the posters and release dates in a nice format.

## Collaboration
I encourage all users to experiemnt and try out the features with the only requirement that a new branch be created so as not to affect the original code, if any of this experimentation seems promising pull requests can be granted upon review. 


