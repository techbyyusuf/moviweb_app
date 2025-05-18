import os
from flask import Flask, flash, render_template, request, url_for, redirect
from extensions import db
from data_managers.data_manager_sqlite import SQLiteDataManager, Movie
from dotenv import load_dotenv
from utils.omdb_api import fetch_movie_details


load_dotenv()


def create_app(db_uri=None):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri or 'sqlite:///moviwebapp.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    return app

app = create_app()
app.secret_key = os.getenv('SECRET_KEY')


with app.app_context():
    db.create_all()

data_manager = SQLiteDataManager()

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/users')
def list_users():
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)


@app.route('/users/<user_id>')
def user_movies(user_id):
    movies = data_manager.get_user_movies(user_id)
    return render_template('movies.html', movies=movies, user_id=user_id)


@app.route('/add_user', methods = ['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        username = request.form.get('name')
        data_manager.add_user(username)
        flash(f"User '{username}' has been added!")

        return redirect(url_for('list_users'))

    return render_template('add_user.html')

@app.route('/users/<user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    if request.method == 'POST':
        title = request.form.get('title')
        movie_data = fetch_movie_details(title)

        if movie_data:
            year = movie_data.get('Year')
            director = movie_data.get('Director')
            rating = movie_data.get('imdbRating')

            data_manager.add_movie(
                title=title,
                user_id=user_id,
                year=year,
                director=director,
                rating=rating
            )

            flash(f"Movie '{title}' has been added!")
            return redirect(url_for('user_movies', user_id=user_id))
        else:
            flash("Movie not found in OMDb.")

    return render_template('add_movie.html', user_id=user_id)


@app.route('/users/<user_id>/update_movie/<movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    if request.method == 'POST':
        title = request.form.get('title')
        year = request.form.get('year')
        director = request.form.get('director')
        rating = request.form.get('rating')

        movie = Movie(
            movie_id=movie_id,
            title=title,
            year=year,
            director=director,
            rating=rating
        )

        data_manager.update_movie(movie)
        flash(f"Movie '{title}' has been updated!")

        return  redirect(url_for('user_movies', user_id=user_id))

    movie = data_manager.get_movie_by_id(movie_id)
    return render_template('update_movie.html', user_id=user_id, movie=movie)



@app.route('/users/<user_id>/delete_movie/<movie_id>', methods=['POST'])
def delete_movie(user_id,movie_id):
    data_manager.delete_movie(user_id=user_id, movie_id=movie_id)
    flash("Movie has been deleted!")

    return redirect(url_for('user_movies', user_id=user_id))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)