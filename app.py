from flask import Flask
from extensions import db
from data_managers.data_manager_sqlite import SQLiteDataManager


def create_app(db_uri=None):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri or 'sqlite:///moviwebapp.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    return app

app = create_app()

with app.app_context():
    db.create_all()

data_manager = SQLiteDataManager()

@app.route('/')
def home():
    return 'Welcome to MovieWeb App'


@app.route('/users')
def list_users():
    data_manager.add_user('Yusuf')
    users = data_manager.get_all_users()
    return str(users)


if __name__ == '__main__':
    app.run(debug=True)