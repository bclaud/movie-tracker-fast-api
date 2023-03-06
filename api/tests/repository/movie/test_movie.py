import pytest

from api.entities.movie import Movie
from api.repository.movie.abstractions import RepositoryException
from api.repository.movie.movies import MemoryMovieRepository


@pytest.mark.asyncio
async def test_create():
    repo = MemoryMovieRepository()
    movie = Movie(
        movie_id="test",
        title="Test movie",
        description="description test",
        release_year=1990,
        watched=False,
    )

    await repo.create(movie)
    assert repo.get("test") is movie


# esta merda nao eh nenhum um pouco legivel
@pytest.mark.parametrize(
    "movies_seed,movie_id,expected_result",
    [
        pytest.param([], "my-id", None, id="empty"),
        pytest.param(
            [
                Movie(
                    movie_id="my-id",
                    title="Test movie",
                    description="description test",
                    release_year=1990,
                    watched=False,
                )
            ],
            "my-id",
            Movie(
                movie_id="my-id",
                title="Test movie",
                description="description test",
                release_year=1990,
                watched=False,
            ),
        ),
    ],
)
@pytest.mark.asyncio
async def test_get(movies_seed, movie_id, expected_result):
    repo = MemoryMovieRepository()

    for movie in movies_seed:
        await repo.create(movie)

    movie = repo.get(movie_id=movie_id)

    assert movie == expected_result


@pytest.mark.parametrize(
    "movies_seed,movie_title, expected_results",
    [
        pytest.param([], "some-title", [], id="empty_results"),
        pytest.param(
            [
                Movie(
                    movie_id="my-id",
                    title="some-title",
                    description="description test",
                    release_year=1990,
                    watched=False,
                )
            ],
            "some-title",
            [
                Movie(
                    movie_id="my-id",
                    title="some-title",
                    description="description test",
                    release_year=1990,
                    watched=False,
                )
            ],
            id="results",
        ),
    ],
)
@pytest.mark.asyncio
async def test_get_by_title(movies_seed, movie_title, expected_results):
    repo = MemoryMovieRepository()
    for movie in movies_seed:
        await repo.create(movie)

    result = await repo.get_by_title(movie_title=movie_title)
    assert result == expected_results


@pytest.mark.asyncio
async def test_update():
    repo = MemoryMovieRepository()
    movie = Movie(
        movie_id="test",
        title="Test movie",
        description="description test",
        release_year=1990,
        watched=False,
    )

    await repo.create(movie)

    await repo.update(movie_id="test", update_params={"title": "changed"})
    updated_movie = await repo.get(movie_id="test")

    assert updated_movie.title == "changed"


@pytest.mark.asyncio
async def test_update_fail():
    repo = MemoryMovieRepository()
    movie = Movie(
        movie_id="test",
        title="Test movie",
        description="description test",
        release_year=1990,
        watched=False,
    )

    await repo.create(movie)

    with pytest.raises(RepositoryException):
        await repo.update(movie_id="test", update_params={"id": "fail"})


@pytest.mark.asyncio
async def test_delete():
    repo = MemoryMovieRepository()
    movie = Movie(
        movie_id="test",
        title="Test movie",
        description="description test",
        release_year=1990,
        watched=False,
    )

    await repo.create(movie)

    await repo.delete(movie_id="test")
    assert repo.get(movie_id="test") is None
