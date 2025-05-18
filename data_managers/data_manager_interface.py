from abc import ABC, abstractmethod


class DataManagerInterface(ABC):
    """Abstract base class defining the interface for movie data management."""

    @abstractmethod
    def get_all_users(self):
        """Retrieve all users from the data source."""
        pass

    @abstractmethod
    def get_user_movies(self, user_id):
        """Retrieve all movies for a given user."""
        pass

    @abstractmethod
    def add_user(self, name):
        """Add a new user to the data source."""
        pass

    @abstractmethod
    def add_movie(self, user_id, title, director, year, rating):
        """Add a new movie to the specified user's collection."""
        pass

    @abstractmethod
    def update_movie(self, movie):
        """Update the details of an existing movie."""
        pass

    @abstractmethod
    def delete_user(self, user_id):
        """Delete a user from the data source."""
        pass

    @abstractmethod
    def delete_movie(self, movie_id, user_id):
        """Delete a movie from a user's collection."""
        pass

    @abstractmethod
    def get_movie_by_id(self, movie_id):
        """Retrieve a movie by its ID."""
        pass