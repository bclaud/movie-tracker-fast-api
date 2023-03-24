import motor.motor_asyncio
import typing

from api.entities.movie import Movie
from api.repository.movie.abstractions import MovieRepository, RepositoryException


class MemoryMovieRepository(MovieRepository):
    """
    MemoryMovie Repository implements the repository pattern by uusing a simple memory database
    """

    def __init__(self):
        self.storage = {}

    async def create(self, movie: Movie):
        self.storage[movie.id] = movie

    async def get(self, movie_id: str) -> typing.Optional[Movie]:
        return self.storage.get(movie_id)

    async def get_by_title(self, movie_title: str) -> typing.List[Movie]:
        return_value = []
        for _, value in self.storage.items():
            if movie_title == value.title:
                return_value.append(value)

        return return_value

    async def update(self, movie_id: str, update_params: dict):
        movie = self.storage.get(movie_id)
        if movie is None:
            raise RepositoryException("movie not found")
        for key, value in update_params.items():
            if key == "id":
                raise RepositoryException("cant update movie id")

            # check that update_params are field from movie entity
            if hasattr(movie, key):
                setattr(movie, f"_{key}", value)

    async def delete(self, movie_id: str):
        self.storage.pop(movie_id, None)


class MongoMovieRepository(MovieRepository):
    """
    MongoMovieRepository implements the repository pattern for our Movie entity using MongoDB.
    """

    def __init__(self, connection_string: str = "mongodb://localhost:27017"):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(connection_string)
        # name of the database
        self._database = self._client["movie_track_db"]
        # name of the collection
        self._movies = self._database["movies"]

    async def create(self, movie: Movie):
        document = await self._movies.insert_one(
            {
                "id": movie.id,
                "title": movie.title,
                "description": movie.description,
                "release_year": movie.release_year,
                "watched": movie.watched,
            }
        )

    async def get(self, movie_id: str) -> typing.Optional[Movie]:
        document = await self._movies.find_one({"id": movie_id})
        if document:
            return Movie(
                movie_id=document.get("id"),
                title=document.get("title"),
                description=document.get("description"),
                watched=document.get("watched"),
                release_year=document.get("release_year"),
            )

        return None

    async def get_by_title(self, movie_title: str) -> typing.List[Movie]:
        return_value: typing.List[Movie] = []

        documents = self._movies.find({"title": movie_title})

        return return_value

    async def delete(self, movie_id: str):
        pass
