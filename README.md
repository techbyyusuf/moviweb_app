# 🎬 Movieweb App

A web application built with Flask that allows users to manage their personal movie collection. Movie data is fetched from the [OMDb API](https://www.omdbapi.com/).

## 🚀 Features

- Add movies by title (fetched from OMDb)
- View all movies for each user
- Update movie details (title, year, rating, etc.)
- Delete movies and users
- Error handling with flash messages
- SQLite database with SQLAlchemy ORM
- Modular code structure using a data manager layer

## 🛠 Tech Stack

- Python 3.10+
- Flask
- SQLAlchemy (with Flask-SQLAlchemy)
- OMDb API (via `requests`)
- pytest (for testing)
- SQLite (as database backend)

## 📦 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/techbyyusuf/moviweb_app.git
   cd movieweb_app
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create a `.env` file with your OMDb API key and flash key:**
   ```env
   OMDB_API_KEY=your_omdb_api_key_here
   SECRET_KEY=your_secret_key
   ```

4. **Run the application:**
   ```bash
   flask run
   ```

   The app will be available at: http://127.0.0.1:5000/

## 🧪 Running Tests

```bash
pytest
```

Make sure the test database path is set in the `test_app_context` fixture.

## 🗃️ Project Structure

```
movieweb_app/
├── app.py                   # Flask routes
├── models/                  # SQLAlchemy models (User, Movie)
├── data_managers/           # Interface and SQLite data manager
├── utils/                   # Extensions (db) and OMDb helper
├── templates/               # HTML templates
├── static/                  # CSS and static files
├── tests/                   # pytest test files
└── requirements.txt         # Python dependencies
```

## 📬 Contact

Maintained by Yusuf.  
Feel free to contribute or report issues!