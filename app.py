from flask import Flask, flash, render_template, request, url_for, redirect
from extensions import db
from data_managers.data_manager_sqlite import SQLiteDataManager, Movie


def create_app(db_uri=None):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri or 'sqlite:///moviwebapp.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    return app

app = create_app()
app.secret_key = 'supersupersecret11'


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

@app.route('/users/<user_id>/add_movie',  methods=['GET', 'POST'])
def add_movie(user_id):
    if request.method == 'POST':
        title = request.form.get('title')
        user_id = user_id
        year = request.form.get('release_year')
        director = request.form.get('director')
        rating = request.form.get('rating')

        data_manager.add_movie(title=title,
                               user_id=user_id,
                               year=year,
                               director=director,
                               rating=rating)

        flash(f" Movie '{title}' has been added!")
        return  redirect(url_for('user_movies', user_id=user_id))

    return render_template('add_movie.html', user_id=user_id)


@app.route('/users/<user_id>/update_movie/<movie_id>')
def update_movie(user_id):
    pass


@app.route('/users/<user_id>/delete_movie/<movie_id>')
def delete_movie(user_id,movie_id):
    pass


if __name__ == '__main__':
    app.run(debug=True)