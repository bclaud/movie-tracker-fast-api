import typing

from api.entities.movie import Movie
from api.repository.movie.abstractions import MovieRepository, RepositoryException


class MemoryMovieRepository(MovieRepository):
    def __init__(self):
        self.storage = {}

    def create(self, movie: Movie):
        self.storage[movie.id] = movie

    def get(self, movie_id: str) -> typing.Optional[Movie]:
        return self.storage.get(movie_id)

    def get_by_title(self, movie_title: str) -> typing.List[Movie]:
        return_value = []
        for _, value in self.storage.items():
            if movie_title == value.title:
                return_value.append(value)

        return return_value

    def update(self, movie_id: str, update_params: dict):
        movie = self.storage.get(movie_id)
        if movie is None:
            raise RepositoryException("movie not found")
        for key, value in update_params.items():
            if key == "id":
                raise RepositoryException("cant update movie id")

            # check that update_params are field from movie entity
            if hasattr(movie, key):
                setattr(movie, key, value)

    def delete(self, movie_id: str):
        self.storage.pop(movie_id, None)
