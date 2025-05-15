from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(db_uri=None):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri or 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    return app

app = create_app()

@app.route('/')
def home():
    return 'Welcome to MovieWeb App'


if __name__ == '__main__':
    app.run(debug=True)