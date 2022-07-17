"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system('dropdb ratings')
os.system('createdb ratings')

model.connect_to_db(server.app)
model.db.create_all()


with open('data/movies.json') as f:
    movie_data = json.loads(f.read())

movies_in_db = []
for movie in movie_data:
    release_date = datetime.strptime(movie['release_date'], "%Y-%m-%d")

    title, overview, poster_path = (
        movie['title'],
        movie['overview'],
        movie['poster_path'],
    )

    db_movie = crud.create_movie(title, overview, release_date, poster_path)
    movies_in_db.append(db_movie)
    
model.db.session.add_all(movies_in_db)
model.db.session.commit()

users_in_db = []
ratings_in_db = []

for n in range(10):
    email = f'user{n}@test.com'  # Voila! A unique email!
    password = 'test'

    # TODO: create a user here
    new_user = crud.create_user(email, password)
    users_in_db.append(new_user)

    # TODO: create 10 ratings for the user
    for n in range(10):
        new_rating = crud.create_rating(new_user, choice(movies_in_db), randint(1, 5))
        ratings_in_db.append(new_rating)

model.db.session.add(users_in_db)
model.db.session.add_all(ratings_in_db)
# model.db.session.add_all([users_in_db, ratings_in_db])
model.db.session.commit()

