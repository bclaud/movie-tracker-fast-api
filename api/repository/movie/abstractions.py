import abc
import typing

from api.entities.movie import Movie


class RepositoryException(Exception):
    pass


# wtf is abc.ABC?????
class MovieRepository(abc.ABC):
    def create(self, movie: Movie):
        """
        creates an movie and returns true if success
        :raises RepositoryException on failure
        """
        raise NotImplementedError

    def get(self, movie_id: str) -> typing.Optional[Movie]:
        """
        retrieves a movie by its ID. If not found it will return None
        """
        raise NotImplementedError

    def get_by_title(self, movie_title: str) -> typing.List[Movie]:
        """
        returns a list of movies that shares the same title
        """
        raise NotImplementedError

    def update(self, movie_id: str, update_params: dict):
        """
        Update a movie by its ID
        """

    def delete(self, movie_id: str):
        """
        deletes a movie by its ID

        :raises RepositoryException on failure
        """
        raise NotImplementedError
