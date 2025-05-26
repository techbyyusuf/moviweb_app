import os
from datetime import datetime

from dotenv import load_dotenv
from flask import abort, Flask, flash, render_template, request, url_for, redirect

from data_managers.data_manager_sqlite import SQLiteDataManager, Movie, User
from utils.extensions import db
from utils.omdb_api import fetch_movie_details

load_dotenv()


def create_app(db_uri=None):
    """Create and configure the Flask application."""
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


def handle_add_movie_post(user_id):
    """Process POST request to add a new movie for a user."""
    try:
        title = request.form.get('title')
        movie_data = fetch_movie_details(title)
        if not movie_data:
            flash(f"Movie '{title}' not found in OMDb.")
            return render_template('add_movie.html', user_id=user_id)
        data_manager.add_movie(
            title=movie_data.get('Title'),
            user_id=user_id,
            year=movie_data.get('Year') or "",
            director=movie_data.get('Director') or "",
            rating=movie_data.get('imdbRating')
        )
        flash(f"Movie '{title}' has been added!")
        return redirect(url_for('user_movies', user_id=user_id))
    except Exception as e:
        print(f"Error adding movie: {e}")
        flash("An error occurred while adding the movie.")
        return render_template('add_movie.html', user_id=user_id)


def handle_movie_update_post(user_id, movie_id):
    """Process POST request to update a movie's data."""
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

    try:
        if int(year) > datetime.now().year:
            raise ValueError("Release year cannot be in the future.")
        if 1888 > int(year):
            raise ValueError("Release year cannot be older then 1888.")
        if not (0 <= float(rating) <= 10):
            raise ValueError("Rating must be between 0 and 10.")

        data_manager.update_movie(movie)
        flash(f"Movie '{title}' has been updated!")
        return redirect(url_for('user_movies', user_id=user_id))

    except ValueError as ve:
        flash(str(ve))
    except Exception as e:
        flash("An error occurred while updating the movie.")
        print(f"Update Error: {e}")


@app.route('/')
def home():
    """Render the home page."""
    return render_template('home.html')


@app.route('/users')
def list_users():
    """List all users."""
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)


@app.route('/users/<user_id>')
def user_movies(user_id):
    """Display all movies for a specific user."""
    movies = data_manager.get_user_movies(user_id)
    return render_template('movies.html', movies=movies, user_id=user_id)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    """Handle user creation via form submission."""
    if request.method == 'POST':
        try:
            username = request.form.get('name')
            data_manager.add_user(username)
            flash(f"User '{username}' has been added!")
            return redirect(url_for('list_users'))
        except Exception as e:
            print(f"Error adding user: {e}")
            flash("An error occurred while adding the user.")
            return redirect(url_for('add_user'))
    return render_template('add_user.html')


@app.route('/users/<user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    """Handle GET or POST request to add a new movie for a user."""
    user = db.session.get(User, user_id)
    if not user:
        abort(404)

    if request.method == 'POST':
        return handle_add_movie_post(user_id)

    return render_template('add_movie.html', user_id=user_id)


@app.route('/users/<user_id>/update_movie/<movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    """Handle GET or POST request to update a movie."""
    if request.method == 'POST':
        return handle_movie_update_post(user_id, movie_id)

    movie = data_manager.get_movie_by_id(movie_id)
    if not movie:
        abort(404)

    return render_template(
        'update_movie.html',
        user_id=user_id,
        movie=movie,
        current_year=datetime.now().year
    )


@app.route('/users/<user_id>/delete_movie/<movie_id>', methods=['POST'])
def delete_movie(user_id, movie_id):
    """Delete a movie from a user's collection."""
    try:
        data_manager.delete_movie(user_id=user_id, movie_id=movie_id)
        flash("Movie has been deleted!")
    except Exception as e:
        print(f"Error deleting movie: {e}")
        flash("An error occurred while deleting the movie.")
    return redirect(url_for('user_movies', user_id=user_id))


@app.errorhandler(404)
def not_found_error(error):
    """Render custom 404 error page."""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """Render custom 500 error page."""
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)